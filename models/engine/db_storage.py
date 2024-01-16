#!/usr/bin/python3
"""
This module defines a class to manage mysql db storage for hbnb clone.

Classes:
    DBStorage: database storage engine

Dependencies:
    sqlalchemy: ORM
    models: contains all classes used
    environ: environment variables

"""
from os import environ  # Environment variables
from sqlalchemy import create_engine  # ORM engine instantiator
from sqlalchemy.orm import sessionmaker, scoped_session  # ORM session manager


class DBStorage:
    """This class manages storage of hbnb models in database using sqlalchemy

    Attributes:
        __engine: private attribute to manage database engine
        __session: private attribute to manage database session

    Methods:
        __init__: instantiates a new DBStorage object
        all: queries current database session based on class name
        new: adds new object to current database session
        save: commits all changes of current database session
        delete: deletes obj from current database session if not None
        reload: creates all tables in database and current database session
        close: closes the current session
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new DBStorage object"""
        # Get environment variables
        user = environ.get('HBNB_MYSQL_USER')
        pwd = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST')
        db = environ.get('HBNB_MYSQL_DB')
        env = environ.get('HBNB_ENV')

        # Create engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        # Drop tables if testing
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries current database session based on class name

        Args:
            cls: class name to query in database (default=None)

        Returns:
            returns dictionary of queried classes in database
        """
        # Query all classes in database
        if cls is None:
            classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
            objs = {}
            for cls in classes:  # Query each class in database
                query = self.__session.query(eval(cls)).all()
                for obj in query:  # Add each returned object to dictionary
                    key = obj.__class__.__name__ + '.' + obj.id
                    objs[key] = obj  # Key = <class name>.<object id>
        # Query specific class in database
        else:
            query = self.__session.query(cls).all()  # Query class in database
            objs = {}
            for obj in query:  # Add each returned object to dictionary
                key = obj.__class__.__name__ + '.' + obj.id
                objs[key] = obj  # Key = <class name>.<object id>
        return objs

    def new(self, obj):
        """
        Add object to current database session.

        Args:
            obj: object to add to current database session
        """
        self.__session.add(obj)  # Add object to current database session

    def save(self):
        """
        Commits all changes of current database session.
        """
        self.__session.commit()  # Commit changes to database

    def delete(self, obj=None):
        """
        Deletes obj from current database session.
        If obj is None, nothing happens.

        Args:
            obj: object to delete from current database session (default=None)
        """
        if obj is not None:  # Case where obj has a value
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in database and current database session.
        """
        from models.base_model import Base, BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)  # Create all tables in db
        # Create session factory
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)  # Create current session

    def close(self):
        """
        Close the current session.
        """
        self.__session.close()
