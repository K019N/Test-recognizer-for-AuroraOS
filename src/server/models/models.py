from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Table

from .database import Base


class Test(Base):
    __tablename__ = "test"

    test_id = Column(Integer, primary_key=True, index=True, nullable=False)
    answer = Column(JSON, nullable=False)   #fromat: {question(int): answer_number(int)}
    results = Column(JSON)  #fromat: {name(str): mark(int)}
    #user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __init__(self, test_id, answer):
        self.answer = answer
        self.test_id = test_id

    def set_id(self, id):
        self.test_id = id

    def set_answers(self, answers):
        self.answer = answers

    def set_results(self, results):
        self.results = results


class Result(Base):
    __tablename__ = "result"

    sending_id = Column(Integer, primary_key=True, index=True, nullable=False)
    test_id = Column(Integer, ForeignKey("test.id"), nullable=False)
    answers = Column(JSON, nullable=False)
    #mark = Column(Integer, nullable=False)

    def __init__(self, sending_id, test_id, answers):
        self.answers = answers
        self.test_id = test_id
        self.sending_id = sending_id



'''
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, index=True, nullable=False)     
'''
