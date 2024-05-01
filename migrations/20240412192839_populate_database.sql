-- migrate:up

insert into repository (name, description, stars)
values
    ('dbmate', 'you better use alembic', 0),
    ('sway', 'i3-compatible Wayland compositor', 14000),
    ('zig', 'General-purpose programming language and toolchain.', 30200);

insert into ticket (name, description, status, repository_id)
values
    ('not working', 'the docker containers error messages are terrible', 'Created',
        (select id from repository where name = 'dbmate')),
    ('custom screen layouts', 'examples are attached', 'In work',
        (select id from repository where name = 'sway')),
    ('package manager', 'implement a pm', 'Done',
        (select id from repository where name = 'zig')),
    ('456', '123', 'In work',
        (select id from repository where name = 'zig'));


insert into developer (name)
values
    ('Victor'),
    ('Ann'),
    ('Tally Man');

insert into repository_developer (developer_id, repository_id)
values
    ((select id from developer where name = 'Victor'),
        (select id from repository where name = 'dbmate')),
    ((select id from developer where name = 'Ann'),
        (select id from repository where name = 'zig')),
    ((select id from developer where name = 'Tally Man'),
        (select id from repository where name = 'sway')),
    ((select id from developer where name = 'Tally Man'),
        (select id from repository where name = 'zig'));

-- migrate:down

