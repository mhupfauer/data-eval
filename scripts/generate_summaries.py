import csv
from gradio_client import Client

client = Client("https://102da3ce8a8bd9b34c.gradio.live/")


with open('summary-data.CSV', 'r') as f:
    reader = csv.reader(f, delimiter=';')

    #Skip header
    next(reader)

    for r in reader:
        if len(r) > 5000:
            continue

        query = """Summarize the below IT-Security Incident report. Make sure to include all relevant data in your summary and limit your response to 300 words. Include all relevant contextual information that is necessary to understand the summary  but exclude general recommendations that could apply a lot of incidents. Only include information that is actually contained within the report and do not generate any information that is not actually contained within the original report.

Report:
%s

Summary:

""" % r[2]
        result = client.predict(
            query,
            len(query)+1024,
            api_name="/predict"
        )

        print(result)