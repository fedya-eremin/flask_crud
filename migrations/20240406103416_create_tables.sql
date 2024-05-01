-- migrate:up

create extension if not exists "uuid-ossp";
create table repository (
    id uuid primary key default uuid_generate_v4(),
    name varchar(50) not null,
    description varchar(200),
    stars int,
    constraint stars_unsigned check (stars >= 0)
);

create table developer (
    id uuid primary key default uuid_generate_v4(),
    name varchar(50) not null,
    signup_date timestamp not null default current_timestamp
);

create table repository_developer (
    developer_id uuid not null references developer,
    repository_id uuid not null references repository,
    primary key(developer_id, repository_id)
);

create table ticket (
    id uuid primary key default uuid_generate_v4(),
    name varchar(50) not null,
    description varchar(200),
    status varchar(10),
    repository_id uuid not null references repository,
    constraint status_valid check (status in ('Created', 'In work', 'Done'))
);

-- migrate:down

