from database.models import SessionLocal, Video


def run_migrations_offline():
    # ...
    context.configure(url=sqlalchemy_url, target_metadata=Video.__table__)
    # ...


def run_migrations_online():
    # ...
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Video.__table__)

        with context.begin_transaction():
            context.run_migrations()
