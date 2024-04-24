from __future__ import annotations

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base class for declarative class definitions
Base = declarative_base()


class SearchModel(Base):
    __tablename__ = "search"
    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False)


class ArticleModel(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, nullable=False)
    meta = Column(String, nullable=True)


class SimpleORM:
    context = {"session": None}

    @classmethod
    def create(cls, **kwargs) -> SimpleORM:
        """
        Inserts sample data into the database.

        Parameters:
            session (Session): The SQLAlchemy session object.
        """
        # Creating a new search record
        new_object = cls.model(**kwargs)
        cls.context["session"].add(new_object)
        cls.context["session"].commit()
        return new_object

    @classmethod
    def filter(cls, **kwargs) -> SimpleORM:
        # Filtering data based on a condition
        query = cls.context["session"].query(cls.model)

        # Apply filters based on kwargs
        for key, value in kwargs.items():
            if not hasattr(cls.model, key):
                print(f"Warning: '{key}' is not a valid attribute of Article")
                continue

            # Construct a filter using the 'like' operator if the value
            # contains a wildcard character
            if "%" in value:
                query = query.filter(getattr(cls.model, key).like(value))
            else:
                query = query.filter(getattr(cls.model, key) == value)

        return query.all()

    @classmethod
    def setup(cls, url: str = "sqlite:///example.db"):
        """
        Setup the database by creating tables and initializing the session.

        Parameters:
            url (str): The database URL.

        Returns:
            session (Session): A SQLAlchemy Session object.
        """
        engine = create_engine(
            url, echo=False
        )  # Set echo=False to turn off verbose logging
        Base.metadata.create_all(engine)  # Create all tables
        Session = sessionmaker(bind=engine)
        cls.context["session"] = Session()
        cls.reset()
        return cls.context["session"]

    @classmethod
    def reset(cls):
        """
        Resets the database by dropping all tables and recreating them.
        """
        # Get the engine from the current session
        engine = cls.context["session"].get_bind()
        # Drop all tables
        Base.metadata.drop_all(engine)
        # Create all tables
        Base.metadata.create_all(engine)
        print("Database has been reset.")


class Search(SimpleORM):
    model = SearchModel


class Article(SimpleORM):
    model = ArticleModel
