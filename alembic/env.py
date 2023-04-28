from logging.config import fileConfig

from sqlalchemy import create_engine, engine

from alembic import context
from bot_template import db
from bot_template.core.config_manager import ConfigManager
from bot_template.database.models import *

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

bot_config = ConfigManager("config.toml")
target_metadata = db.Base.metadata


def get_url():
    return engine.URL.create(
        drivername="postgresql+psycopg",
        username=bot_config.get_item("features.database", "username"),
        password=bot_config.get_item("features.database", "password"),
        host=bot_config.get_item("features.database", "addr"),
        port=bot_config.get_item("features.database", "port"),
        database=bot_config.get_item("features.database", "database_name"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(url=url,
                      target_metadata=target_metadata,
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
