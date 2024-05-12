from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


url = "mysql://root:fast21@127.0.0.1:3306/dboperations"
engine = create_engine(url)

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
