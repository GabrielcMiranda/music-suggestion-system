import uuid
from sqlalchemy import Column, String, JSON, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ ='user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique= True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    favorite_music_genre = Column(String)
    profile_picture = Column(String)
    recommendations = relationship('Recommendation', back_populates='user')

class Recommendation(Base):
    __tablename__ = 'recommendation'
    id = Column(BigInteger, primary_key= True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='recommendations')
    song_input = Column(String, nullable=False)
    musicas = Column(JSON, nullable=False)
