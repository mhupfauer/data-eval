import random

from flask import Blueprint, render_template, request
from dataeval.db.db import db
from dataeval.models.GRADING import GRADING
from dataeval.models.RAW_REPORTS import RAW_REPORTS
from dataeval.models.RESULTS import RESULTS
from dataeval.models.SUMMARIES import SUMMARIES

bp = Blueprint('eval', __name__, url_prefix='/eval')


@bp.route("/report")
def eval_data():
    summaries = SUMMARIES.query.all()
    resultdata = {}

    for summary in summaries:
        """
        Iterate over all summaries (generated by AI for each RAW-REPORT) and then average all received grades for
        each individual summary. The average grade per summary is then stored with the generator information.
        Lastly the information is iterated again and the average over all individual summaries of one generator
        is calculated.
        """
        grades = 0
        for grade in summary.grades:
            grades += grade.rank
        avg = grades / len(summary.grades)

        curr = resultdata.get(summary.generator)
        if curr is None:
            curr = [avg]
        else:
            curr.append(avg)

        resultdata[summary.generator] = curr

    for k, v in resultdata.items():
        grade = 0
        for n in v:
            grade += n
        grade = grade / len(v)
        resultdata[k] = grade

    print(resultdata)
    return resultdata


@bp.route("/results", methods=["POST"])
def store_result():
    request_data = request.get_json()
    report_id = list(request_data.keys())[0]
    summary_grades = request_data[report_id]

    new_result = RESULTS(raw_report_id=report_id)
    db.session.add(new_result)
    db.session.commit()

    for k, v in summary_grades.items():
        to_create = GRADING(
            summary_id=k,
            rank=v,
            result_id=new_result.id
        )
        db.session.add(to_create)
        db.session.commit()

    return '{"response":"200"}'


@bp.route("/present", methods=["GET"])
@bp.route("/present/<guid>", methods=["GET"])
def present_question(guid=None):
    if guid is None:
        guid = RAW_REPORTS.query.first().id

    try:
        report = RAW_REPORTS.query.get(guid)
        next_report = RAW_REPORTS.query.order_by(RAW_REPORTS.id.asc()).filter(RAW_REPORTS.id > report.id).first()
        if next_report is None:
            next_report = RAW_REPORTS.query.first()
    except Exception as e:
        print(e)

    return render_template('present.html', questionid=report.id, nextquestionid=next_report.id,
                           report=report.text,
                           item1=report.summaries[0],
                           item2=report.summaries[1],
                           item3=report.summaries[2],
                           item4=report.summaries[3])