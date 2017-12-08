Create table IF NOT EXISTS campaign(
id integer primary key  ,
name varchar(100) not null
);

create table  IF NOT EXISTS template(
id integer primary key  ,
name varchar(100) not null,
subject varchar(100) not null,
message varchar(500) not null
);

create table IF NOT EXISTS campaign_template(
id integer primary key  ,
campaign_id integer not null references campaign(id),
template_id integer not null references template(id)
);

create table IF NOT EXISTS user(
id integer primary key ,
name varchar(100) not null,
email varchar(50) not null,
address varchar(100)
);

