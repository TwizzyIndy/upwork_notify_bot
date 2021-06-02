from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.schema import Base

engine = create_engine('sqlite:///file.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()