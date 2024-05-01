-- migrate:up
create schema api;
set search_path = public, api;
alter table developer set schema api;
alter table repository set schema api;
alter table repository_developer set schema api;
alter table ticket set schema api;

-- migrate:down

