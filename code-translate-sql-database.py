# This is a coding sample from a personal project: Code Translate, 2021.
# I used a SQL Database to collect feedback. Below you will see my implementations of 1) a Feedback Class, 2) Feedback functions, and 3) a database initialization script.

"""
1. FeedbackDB.py
Feedback Class
"""
from sqlalchemy import Column, Integer, String, Boolean
from random import randint
from server.init_db import Base, db_session

class Feedback(Base):
    __tablename__ = 'feedback'
    # name, type, primary_key
    id = Column('id', Integer, primary_key=True)
    data = Column('data', String(64), unique=False, nullable=False)

    def __init__(self, data):
        self.data = data

def addFeedback(feedback):
    if feedback:
        db_session.add(feedback)
        db_session.commit()
        print("Added Feedback to DB")

def getFeedback():
    print("Getting Feedback from DB")
    return Feedback.query.all()
    
    
""" 
2. routes.py
Feedback route functions
Request data provides: { 'feedback': feedback }
"""
@routes.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        if data is None:
            return jsonify(**{'message': 'No data found'})
        print(data)

        if data:
            feedback = data['feedback']
            newFeedback = Feedback(feedback)
            addFeedback(newFeedback)
            print("Added feedback in routes.py")

            feedback_from_db= getFeedback()
            all_feedback = []
            print("Received feedback in routes.py")
            for fb in feedback_from_db:
                all_feedback.append({"id": fb.id, "feedback": fb.data})
            print(all_feedback)

            return jsonify(**{'message': "Success", 'feedbackId': newFeedback.id})
        return jsonify(**{'message': "Somewhere went wrong when sending feedback!"})
    except:
        print(request)
        return jsonify(**{'message': 'Feedback was unsupported. :('})

"""
3. init_db.py
Initialize the database using SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from SECRET_KEY import mysql_key
import os

# FROM AMAZON RDS
engine = create_engine(mysql_key)

# LOCAL
# parent_directory = (os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))

if not os.path.exists(os.path.abspath(parent_directory + '/tmp')):
    os.makedirs(parent_directory + '/tmp')

engine = create_engine('sqlite:///tmp/feedback.db'.format(dir=parent_directory), convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import database modules here for models
    import server.modelsDB.FeedbackDB
    Base.metadata.create_all(bind=engine)