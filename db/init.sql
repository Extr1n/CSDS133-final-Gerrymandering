
CREATE EXTENSION postgis;

CREATE TABLE meta (
    runid BIGSERIAL PRIMARY KEY,
    state INT NOT NULL,
    type INT NOT NULL,
    previd INT,
    level INT NOT NULL,
    size INT
);

CREATE TABLE groups (
    groupid BIGSERIAL PRIMARY KEY,
    runid BIGINT NOT NULL,
    geo GEOMETRY NOT NULL,
    dem INT NOT NULL,
    rep INT NOT NULL,
    total INT NOT NULL,
    FOREIGN KEY (runid) REFERENCES meta(runid)
);

CREATE TABLE result_group (
    resid BIGSERIAL PRIMARY KEY,
    layers INT[2][] NOT NULL,
    runid BIGINT NOT NULL
);

CREATE TABLE results (
    runid BIGINT PRIMARY KEY,
    resid BIGINT NOT NULL,
    dem INT NOT NULL,
    rep INT NOT NULL,
    total INT NOT NULL,
    FOREIGN KEY (runid) REFERENCES meta(runid),
    FOREIGN KEY (resid) REFERENCES result_group(resid)
);

CREATE FUNCTION cluster_group(v_previd BIGINT, v_size INT, v_seed DOUBLE PRECISION, v_type INT DEFAULT -1)
RETURNS BIGINT AS $$
DECLARE
    v_runid BIGINT;
BEGIN
    if v_type = -1 then
        SELECT type-1 into v_type
        from meta
        where runid=v_previd;
    end if;

    INSERT INTO meta (state, type, previd, level, size) (
        SELECT
            state,
            v_type,
            v_previd,
            level + 1,
            v_size
        FROM meta
        WHERE runid=v_previd
    )
    RETURNING runid INTO v_runid;

    PERFORM setseed(v_seed);

    INSERT INTO groups (runid, dem, rep, total, geo) (
        SELECT
            v_runid,
            SUM(dem) AS dem,
            SUM(rep) AS rep,
            SUM(total) AS total,
            ST_CollectionExtract(ST_Union(geo)) AS geo
        FROM (
            SELECT 
                g.*,
                ST_ClusterKMeans(
                    ST_Force4D(
                        ST_Force3DZ(ST_GeneratePoints(g.geo, 1, (100000*random()+1)::INT), 0.15*random()),
                        mvalue => 1000*random() -- set clustering to be weighed by population
                    ),
                    v_size
                ) OVER () AS clustering
            FROM groups AS g
            WHERE g.runid = v_previd
        )
        GROUP BY clustering
    );

    RETURN v_runid;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION create_layers(layers INT[2][], prevrunid BIGINT)
RETURNS BIGINT AS $$
DECLARE
    runids BIGINT[];
    nextrunids BIGINT[];
    v_type INT;
    num_layers INT;
    v_runid BIGINT;
    v_resid BIGINT;
    count INT;
BEGIN
    runids := array_append('{}', prevrunid);
    v_type := array_length(layers, 1);
    num_layers := v_type;
    FOR i IN 1..v_type
    LOOP
        nextrunids := '{}';
        FOR count IN 1..layers[i][2]
        LOOP
            FOREACH v_runid IN ARRAY runids
            LOOP
                nextrunids := array_append(
                    nextrunids,
                    cluster_group(
                        v_runid, layers[i][1], count::double precision/layers[i][2], v_type
                    )
                );
            END LOOP;
        END LOOP;
        v_type := -1;
        runids := nextrunids;
    END LOOP;

    INSERT INTO result_group (layers, runid) VALUES (
        layers,
        prevrunid
    ) RETURNING resid INTO v_resid;

    INSERT INTO results (runid, resid, dem, rep, total) (
        SELECT
            runid,
            v_resid,
            SUM(CASE WHEN dem > rep THEN 1 ELSE 0 END) AS dem,
            SUM(CASE WHEN rep > dem THEN 1 ELSE 0 END) AS rep,
            COUNT(total)
        FROM groups
        WHERE groups.runid = ANY(runids)
        GROUP BY runid
    );

    return v_resid;
END;
$$ LANGUAGE plpgsql;
