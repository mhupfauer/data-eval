from dataeval.db.db import db

class RESULTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_report_id = db.Column(db.Integer, db.ForeignKey('raw_reports.id'))
    grades = db.relationship('GRADING', backref='result')