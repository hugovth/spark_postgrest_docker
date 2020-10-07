CREATE TABLE IF NOT EXISTS outlet (
    "id" varchar(2550) NOT NULL,
    "id_outlet" varchar(2550) NOT NULL,
    "address" varchar(2550),
    "city" varchar(255),
    "country" varchar(255),
    "cuisines" varchar(255),
    "features" varchar(2550),
    "lat" double precision,
    "lon" double precision,
    "menu" varchar(2550),
    "name" varchar(2550),
    "opening_hours" varchar(255),
    "phone" varchar(255),
    "postal_code" varchar(255),
    "price_level" varchar(255),
    "price_range" varchar(255),
    "rating" double precision,
    "region" varchar(255),
    "reviews_nr" double precision,
    "street" varchar(2550),
    "tags" varchar(2550),
    "url" varchar(2550),
    "website" varchar(2550),
    "source" varchar(255),
    "special_diets" varchar(2550)
);

CREATE TABLE IF NOT EXISTS menu (
    "id" varchar(255),
    "id_outlet" varchar(255),
    "name" varchar(255),
    "brand" varchar(255),
    "price" double precision,
    "volume" double precision,
    "source" varchar(255)
    -- FOREIGN KEY ("id") REFERENCES outlet("id")
);

CREATE FUNCTION getoutletperbrand(br varchar(255)) RETURNS SETOF outlet AS $$
  SELECT o.*   
  FROM
	outlet o
  INNER JOIN menu m 
      ON o.id = m.id
  WHERE
      m.brand ILIKE ('%'|| br || '%');
$$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION getitempermenu(treshold double precision) RETURNS SETOF menu AS $$
  SELECT *   
  FROM
	menu m
  WHERE m.price > treshold;
$$ LANGUAGE SQL IMMUTABLE;




