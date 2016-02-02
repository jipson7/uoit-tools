from uoit_tools import db
from sqlalchemy.ext.hybrid import hybrid_property

class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer, primary_key=True)
    class_type = db.Column(db.String(16)) # Max Found = 5
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    day = db.Column(db.String(1))
    location = db.Column(db.String(128))
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    section_type = db.Column(db.String(32)) # Max found = 17
    instructors = db.Column(db.String(256)) # Max found = 202
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'))

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))              # Max found = 57
    department = db.Column(db.String(4))
    code = db.Column(db.String(5))
    reg = db.Column(db.Integer)
    section = db.Column(db.String(3))
    capacity_total = db.Column(db.Integer)
    capacity_taken = db.Column(db.Integer)
    capacity_remaining = db.Column(db.Integer)
    semester = db.Column(db.String(6))
    days = db.relationship(Day, backref='course', passive_deletes=True)

    @hybrid_property
    def course_code(self):
        return self.department + self.code

    @hybrid_property
    def type(self):
       return (self.days[0]).section_type


