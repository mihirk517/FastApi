# FastAPI backend for a Social Media App

This is a Backend framework built for a Social Media application where people can create posts, see posts created by others and Vote on them.

The backend is based on [FastAPI](https://fastapi.tiangolo.com/) a python based backend framework utilising OAuth2 authentication, pydantic data models and combining them with [Sqlalchemy](https://www.sqlalchemy.org/),[alembic](https://alembic.sqlalchemy.org/en/latest/)  & [PostgresQL](https://www.postgresql.org/). The entire backend is then Dockerized for hosting.

## Video

The following video shows working of the backend in processing & storing OAuth2 login information in hashed format inside the database along with the posts created by the user along with his votes. It also shows the complete dockerization of both the back & the front end suitabe for hosting.

[Video](./assets/FullStack.mp4)