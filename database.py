from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://java:java7834@localhost:5432/fastapi")

Base = declarative_base()
Session = sessionmaker(bind=engine)