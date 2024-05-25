Alembic installation and processes:
1.Initialize Alembic with alembic init by adding a directory name
2.Go to env.py file and import below, which will get the env variables from config which in itself fetches them from .env and get the Base from models.py
    from app.config import settings
    from app.models import Base
3.Change the metadata to this:
    target_metadata = Base.metadata
4.Then set similar code like this:
    #this line of code will be used to update anything related to tables that we change which will be shown in the database changes
    config.set_main_option("sqlalchemy.url", f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
5.Alembic running part:
    alembic revision -m "message for migration"
6.Next we define the upgrade and downgrade functions for database migrations in the versions/revision_file inside the alembic folder
7.Actually the command to execute the table: alembic upgrade {revision id}
8.alembic downgrade -1  to downgrade to lower revision
9.Example of creating a table with alembic via upgrading in the revision file:
    def upgrade() -> None:
    op.add_column("users",
                  sa.Column("id",sa.Integer(),nullable=False),
                  sa.Column("email",sa.String(),nullable=False), # type: ignore
                  sa.Column("password",sa.String(),nullable=False),
                  sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                  sa.PrimaryKeyConstraint("id"),
                  sa.UniqueConstraint("email")
    )
10.