from dataeval.db.db import db


class GRADING(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary_id = db.Column(db.Integer, db.ForeignKey('summaries.id'))
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))
    rank = db.Column(db.Integer)