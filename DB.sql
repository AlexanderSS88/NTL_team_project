CREATE TABLE IF NOT EXISTS user_info (
id integer PRIMARY KEY,
user_name varchar(40) NOT NULL,
user_surname varchar(40) NOT NULL,
age int,
sex int,
city varchar (40),
account_link varchar(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS photos (
id integer PRIMARY KEY,
photo_link varchar(300),
photo_id_user integer REFERENCES user_info(id)
)
;
CREATE TABLE IF NOT EXISTS interests(
id integer PRIMARY KEY,
interest_name varchar(40) NOT NULL,
interest_id_user integer REFERENCES user_info(id)
);