from dataeval.db.db import db

class RAW_REPORTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    source = db.Column(db.String)
    summaries = db.relationship('SUMMARIES', backref='raw_report')