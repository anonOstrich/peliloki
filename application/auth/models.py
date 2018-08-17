from application import db 
from application.models import Base
from application.reviews.models import Review
from application.reactions.models import Reaction
from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"
    
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    
    reviews = db.relationship("Review", backref="account", lazy=True)
    reactions = db.relationship("Reaction", backref="account", lazy=True)
    
    def __init__(self, name, username, password): 
        self.name = name
        self.username = username
        self.password = password
        
        
    def has_reviewed(self, game_id):
        return Review.query.filter_by(account_id=self.id, game_id=game_id).first() is not None
        
    def has_reacted(self, review_id):
        return Reaction.query.filter_by(account_id=self.id, review_id=review_id).first() is not None
    
    @staticmethod
    def find_users_with_no_reviews():
        stmt = text("SELECT Account.username FROM Account"
                    " WHERE Account.id NOT IN (SELECT DISTINCT Review.account_id FROM Review);")

        res = db.engine.execute(stmt)
        users=[]
        for row in res:
            users.append({"username": row[0]})
        return users
        
    def get_id(self):
        return self.id
    
    def is_active(self): 
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self): 
        return True
