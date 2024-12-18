-- ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=Jerry user=postgres password=supersecurepassword" ~/Documents/precincts-with-results.geojson -nln Jerry -nlt PROMOTE_TO_MULTI

CREATE TABLE transformed AS
SELECT
    ogc_fid AS id,
    ST_CollectionExtract(ST_MakeValid(ST_GeomFromWKB(wkb_geometry))) AS geo,
    substring(geoid from 1 for 2)::INT AS state,
    substring(geoid from 3 for 3)::INT AS county,
    votes_dem AS dem,
    votes_rep AS rep,
    votes_total AS total
from jerry;

INSERT INTO meta (state, type, level)
    SELECT state, 0, 0
    FROM transformed
    GROUP BY state;

INSERT INTO groups (runid, geo, dem, rep, total)
    SELECT m.runid, t.geo, COALESCE(t.dem, 0), COALESCE(t.rep, 0), COALESCE(t.total, 0)
    FROM transformed AS t
    JOIN meta AS m ON t.state = m.state;
