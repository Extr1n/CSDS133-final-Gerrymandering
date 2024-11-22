CREATE EXTENSION postgis;

select votes_total, substring(geoid from 3 for 3) as county, ST_GeomFromWKB(wkb_geometry), ST_Centroid(ST_GeomFromWKB(wkb_geometry)) from jerry
where starts_with(geoid, '39') and substring(geoid from 3 for 3) <> '035';
--group by substring(geoid from 3 for 3)
--order by county

select SUM(votes_total), ST_Union(ST_MakeValid(ST_GeomFromWKB(wkb_geometry))), substring(geoid from 3 for 3) from jerry
where starts_with(geoid, '39')
group by substring(geoid from 3 for 3)
order by substring(geoid from 3 for 3);

drop table jerrycluster;

create table jerrycluster as
select
	ST_GeomFromWKB(wkb_geometry) as geo,
	votes_total as pop,
	ST_ClusterKMeans(
        ST_Force4D(
            ST_GeomFromWKB(wkb_geometry), -- cluster in 3D XYZ CRS
            mvalue => votes_total -- set clustering to be weighed by population
        ),
        88
    ) over () as clc
from jerry
where starts_with(geoid, '39');

create table jerrycluster2 as
select
	ST_GeomFromWKB(wkb_geometry) as geo,
	votes_total as pop,
	ST_ClusterKMeans(
        ST_Force4D(
            ST_GeomFromWKB(wkb_geometry), -- cluster in 3D XYZ CRS
            mvalue => votes_total -- set clustering to be weighed by population
        ),
        88
    ) over () as clc
from jerry
where starts_with(geoid, '39');

select SUM(pop), ST_Union(ST_MakeValid(geo)) from jerrycluster2
group by clc;