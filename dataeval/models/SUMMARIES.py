from dataeval.db.db import db

class SUMMARIES(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    generator = db.Column(db.String)
    raw_report_id = db.Column(db.Integer, db.ForeignKey('raw_reports.id'))
    grades = db.relationship('GRADING', backref='summary')