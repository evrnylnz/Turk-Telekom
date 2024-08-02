drop table if exists device;
create table device
(
    id                        integer primary key autoincrement,
    province_id               integer,
    district_id               integer,
    station                   varchar(50),
    location_name             varchar(50),
    location_floor            varchar(50),
    router_id                 integer,
    router_count              integer,
    number_of_ports           varchar(50),
    connected_router_id       integer,
    connection_port           varchar(50),
    connected_router_location varchar(50),
    loopback_ip               varchar(50),
    vlan                      varchar(50),
    connection                varchar(50),
    energy_type               varchar(50),
    temos                     varchar(50),

    foreign key (province_id) references province (id),
    foreign key (district_id) references district (id),
    foreign key (router_id) references router (id),
    foreign key (connected_router_id) references router (id)
);

drop table if exists router_brand;
create table router_brand
(
    id   integer primary key autoincrement,
    name varchar(50)
);

drop table if exists router;
create table router
(
    id       integer primary key autoincrement,
    name     varchar(50),
    brand_id integer,
    foreign key (brand_id) references router_brand (id)
);

-- Insert values into router_brand
insert into router_brand(name)
values ('Cisco');
insert into router_brand(name)
values ('Huawei');
insert into router_brand(name)
values ('LANTECH');

-- Insert values into router
insert into router(name, brand_id)
values ('2960x', (select id from router_brand where name = 'Cisco'));
insert into router(name, brand_id)
values ('3750', (select id from router_brand where name = 'Cisco'));
insert into router(name, brand_id)
values ('4510 Gi4', (select id from router_brand where name = 'Cisco'));
insert into router(name, brand_id)
values ('4510 Gi5', (select id from router_brand where name = 'Cisco'));
insert into router(name, brand_id)
values ('4510 Gi6', (select id from router_brand where name = 'Cisco'));
insert into router(name, brand_id)
values ('AR2220', (select id from router_brand where name = 'Huawei'));

-- Verify the inserted data
select *
from router_brand;
select *
from router;

-- Insert values into device
insert into device(province, district, station, location_name, location_floor, router_id, router_count, number_of_ports,
                   connected_router_id,
                   connection_port, connected_router_location, loopback_ip, vlan, connection, energy_type, temos)
values ('İzmir',
        'Konak',
        'Konak',
        'Makam Katı',
        NULL, -- Use NULL if the location_floor is not specified
        (select id from router where brand_id = (select id from router_brand where name = 'Cisco' limit 1) and name = '2960x'),
    3,
    "3x24",
    (
select id
from router
where brand_id = (select id from router_brand where name = 'Cisco' limit 1)
  and name = '4510 Gi6')
    , '5'
    , NULL
    ,      -- Use NULL if the connected_router_location is not specified
    '10.35.27.166'
    , NULL
    ,      -- Use NULL if the vlan is not specified
    'Direk'
    , 'AC'
    , NULL -- Use NULL if the temos is not specified
    )
    ,
;