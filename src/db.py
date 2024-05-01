import os
import psycopg
from psycopg.rows import dict_row
from psycopg.sql import SQL, Literal
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    HOST = os.getenv('POSTGRES_HOST') if os.getenv(
        'DEBUG_MODE') == 'false' else 'localhost'
    PORT = os.getenv('POSTGRES_PORT')
    DATABASE = os.getenv('POSTGRES_DB')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    CONNECTION_STRING = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    connection = psycopg.connect(CONNECTION_STRING, row_factory=dict_row)
    connection.autocommit = True
    return connection


def get_repositories(connection):
    query = """
    with repository_with_developer as (
        select r.id, r.name, r.description, r.stars,
            coalesce(json_agg(json_build_object(
            'id', d.id, 'name', d.name, 'signup_date', d.signup_date))
            filter (where d.id is not null), '[]') as developer
        from api.repository r
        left join api.repository_developer rp on rp.repository_id = r.id
        left join api.developer d on rp.developer_id = d.id
        group by r.id
    ), repository_with_ticket as (
        select re.id,
            coalesce(json_agg(json_build_object(
            'id', t.id, 'name', t.name, 'description', t.description, 'status', t.status))
            filter (where t.id is not null), '[]') as ticket
        from api.repository re
        left join api.ticket t on t.repository_id = re.id
        group by re.id
    )
    select rwd.id, name, description, stars, developer, ticket
    from repository_with_developer rwd
    join repository_with_ticket rwt on rwd.id = rwt.id
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def create_repository(connection, body):
    query = SQL("""
    insert into api.repository (name, description, stars)
    values
        ({name}, {description}, {stars})
    returning id;
    """).format(
        name=Literal(body.get("name")),
        description=Literal(body.get("description")),
        stars=Literal(body.get("stars"))
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()


def update_repository(connection, body):
    query = SQL("""
    update api.repository set
        name = {name},
        description = {description},
        stars = {stars}
    where id = {id}
    returning id
    """).format(
        id=Literal(body.get("id")),
        name=Literal(body.get("name")),
        description=Literal(body.get("description")),
        stars=Literal(body.get("stars"))
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()


def delete_repository(connection, body):
    query_links = SQL("""
    delete from api.repository_developer where repository_id = {id}
    """).format(id=Literal(body.get("id")))
    query = SQL("""
    delete from api.repository where id = {id} returning id
    """).format(id=Literal(body.get("id")))

    with connection.cursor() as cursor:
        cursor.execute(query_links)
        cursor.execute(query)
        return cursor.fetchone()
