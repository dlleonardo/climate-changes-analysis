CREATE TABLE city (
    id serial,
    city_name varchar(255),
    latitude double precision,
    longitude double precision,
    start_date date,
    end_date date,
    PRIMARY KEY(id)
);

CREATE TABLE weather_data (
    id serial,
    city_id int,
    time timestamp,
    temperature double precision,
    precipitation double precision,
    PRIMARY KEY(id),
    CONSTRAINT city_fk FOREIGN KEY (city_id)     
    REFERENCES City(id)
);

CREATE TABLE season (
    id serial,
    city_id int,
    year int,
    mean_precipitation double precision,
    season_name varchar(50),
    PRIMARY KEY(id),
    CONSTRAINT city_fk FOREIGN KEY (city_id)
    REFERENCES City(id)
);

INSERT INTO city(city_name, latitude, longitude, start_date, end_date) VALUES ('Rome', 41.9027, 12.4963, '2012-01-01', '2022-12-31');
