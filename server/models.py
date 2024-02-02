from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    # All authors have a name
    # Author phone numbers are exactly ten digits
    @validates("name", "phone_number")
    def validate_author(self, key, value):
        if key == "name":
            assert value != ""
        if key == "phone_number":
            assert len(value) == 10
        return value
   
    

      
    
    
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    # All posts have a title
    # Post content is at least 250 characters long
    # Post summary is a maximum of 250 characters 
    @validates("title", "content", "summary")
    def validate_post(self, key, value):
        if key == "title":
            assert value != ""
        if key == "content":
            assert len(value) >= 250
        if key == "summary":
            assert len(value) <= 250
        return value
    
    def validate_clickbait_title(self, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top [0-9]+", "Guess"]
        for phrase in clickbait_phrases:
            if re.search(phrase, title):
                return
        raise ValueError("Title must be sufficiently clickbait-y. It should contain phrases like 'Won't Believe', 'Secret', 'Top [number]', or 'Guess'.")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
