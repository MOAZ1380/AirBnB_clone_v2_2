from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import Base
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place

class DBStorage:
    """Interacts with the MySQL database."""
    __engine = None
    __session = None
    
    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}', pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        objects = {}
        if cls:
            Query = self.__session.query(cls).all()
            for obj in Query:
                key = f"{self.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for c in [User, State, City, Amenity, Place, Review]:
                query = self.__session.query(c).all()
                for obj in query:
                    key = f"{self.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects
    
    
    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)
    
    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()
    
    
    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj:
            self.__session.delete(obj)
    
    
    def reload(self):
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)
        Session = scoped_session(session)
        self.__session = Session()
    
    