-- ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=Jerry user=postgres password=supersecurepassword" ~/Documents/precincts-with-results.geojson -nln Jerry -nlt PROMOTE_TO_MULTI

CREATE EXTENSION postgis;

select votes_total, substring(geoid from 3 for 3) as county, ST_GeomFromWKB(wkb_geometry), ST_Centroid(ST_GeomFromWKB(wkb_geometry)) from jerry
where starts_with(geoid, '39') and substring(geoid from 3 for 3) <> '035';
--group by substring(geoid from 3 for 3)
--order by county

select SUM(votes_total), ST_Union(ST_MakeValid(ST_GeomFromWKB(wkb_geometry))), substring(geoid from 3 for 3) from jerry
where starts_with(geoid, '39')
group by substring(geoid from 3 for 3)
order by substring(geoid from 3 for 3);

drop table jerryTransform;

create table jerryTransform as
select ogc_fid as id, ST_CollectionExtract(ST_MakeValid(ST_GeomFromWKB(wkb_geometry))) as geo, substring(geoid from 1 for 2)::integer as state, substring(geoid from 3 for 3)::integer as county, votes_dem as dem, votes_rep as rep, votes_total as tot
from jerry;

drop table trans2;

create table trans2 as
select *, ST_ClusterKMeans(
        ST_Force4D(
        	ST_Force3DZ(ST_GeneratePoints(geo, 1, (100000*random()+1)::int), 0.15*random()),
            mvalue => 1000*random() -- set clustering to be weighed by population
        ),
        880
    ) over () as cluster1
from jerryTransform
where state = 39;

select * from trans2;

drop table trans22;

create table trans22 as
select SUM(tot) as tot, SUM(dem) as dem, SUM(rep) as rep, ST_CollectionExtract(ST_Union(geo)) as geo from trans2
group by cluster1;

select * from trans22;

drop table trans222;

create table trans222 as
select *, ST_ClusterKMeans(
        ST_Force4D(
        	ST_Force3DZ(ST_GeneratePoints(ST_CollectionExtract(geo), 1, (100000*random()+1)::int), 0.15*random()),
            mvalue => 1000*random() -- set clustering to be weighed by population
        ),
        88
    ) over () as cluster2
from trans22;

drop table trans2222;

create table trans2222 as
select SUM(tot) as tot, SUM(dem) as dem, SUM(rep) as rep, SUM(dem) > SUM(rep) as dem_win, ST_Union(geo) as geo from trans222
group by cluster2;

select SUM(dem_win::integer), COUNT(*) from trans2222;
