import csv
import math

import nltk
from gradio_client import Client

client = Client("")

def SplitAndRequest(text, task, lim):
    required_slices = math.ceil(len(text) / lim)
    sentences = nltk.sent_tokenize(text)
    shards = []
    step_size = math.ceil(len(sentences) / required_slices)
    for i in range(required_slices):
        if i == 0:
            first_setence = 0
            last_sentence = step_size + 1
        else:
            last_sentence = i * step_size + step_size + 1
            first_setence = last_sentence - (step_size + 1)
        shard = ' '.join(sentences[first_setence:last_sentence])
        if len(shard) > 0:
            shards.append(shard)

    summaries = []
    for s in shards:
        query = """%s

Report:
%s

Summary:
    """ % (task, s)
        result = client.predict(
            query,
            len(query) + 500,
            api_name="/predict"
        )

        summaries.append(result.split("Summary:")[1])

    return ' '.join(summaries)


with open ('responses.csv', 'w', encoding='UTF-8') as w:
    writer = csv.writer(w, delimiter=';')
    writer.writerow(['URL','TITLE','RAW','SUMMARY','LANG','DATE'])

with open('summary-data.CSV', 'r') as f:
    reader = csv.reader(f, delimiter=';')

    #Skip header
    next(reader)

    for r in reader:
        summary = SplitAndRequest(r[2], "You will be given individual parts of an IT-Security report to summarize. Keep your response short and include the all important information like the threat actors, attack vectors and potential targets. Exclude general informations and reccomendations", 1500)
        while len(summary) > 1900:
            summary = SplitAndRequest(summary, "You will be given individual parts of an IT-Security report to summarize. Keep your response short while including the all important information but exclude general informations and reccomendations.", 1500)

        query = """You will be given several partial summaries of the a report to summarize them into one coherent summary. Include all important information contained within the summaries.

Summaries:
%s

Summary:
""" % summary
        result = client.predict(
            query,
            2048,
            api_name="/predict"
        )

        print(result.split("Summary:")[1])

        raw_len = len(r[2])
        summary_len = len(summary)

        with open('responses.csv', 'a', encoding='UTF-8') as w:
            writer = csv.writer(w, delimiter=';')
            writer.writerow([r[0], r[1], r[2], result.split("Summary:")[1].replace('\n',''), r[3], r[4]])

        print("""RAW LEN: %i
SUMMARY LEN: %i""" % (raw_len, summary_len))