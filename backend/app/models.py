from sqlalchemy import Column, UUID, String, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ ='user'
    id = Column(UUID, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    favorite_music_genre = Column(String)
    recommendations = relationship('Recommendation', backref='user')

    def match_password(self, raw_password:str):
        return raw_password == self.password

class Recommendation(Base):
    __tablename__ = 'recommendation'
    id = Column(BigInteger, primary_key= True, autoincrement=True)
    user_id = Column(UUID, ForeignKey('user.id'), nullable= False)
    musicas = Column(JSON, nullable=False)
