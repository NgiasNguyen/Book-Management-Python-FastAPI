from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.sql.schema import ForeignKey
from app.db.base import Base
from sqlalchemy import DateTime

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255),nullable=False, index=True)
    description = Column(Text,nullable=True)
    publication_year = Column(Integer,nullable=False)
    
    author_id = Column(
    Integer,
    ForeignKey("authors.id", ondelete="RESTRICT"),
    nullable=False
    )
    category_id = Column(
    Integer,
    ForeignKey("categories.id", ondelete="RESTRICT"),
    nullable=False
    )

    cover_image = Column(String(255),nullable=True) #save path, example: /static/cover/xxx.jpg
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")

    