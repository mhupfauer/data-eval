import csv
import math
import re
import unidecode

import nltk
from gradio_client import Client

nltk.download('popular', quiet=True)

client = Client("http://10.20.62.95:7860/")


def SplitAndRequest(text, task, lim):
    required_slices = math.ceil(len(text) / lim)
    sentences = nltk.sent_tokenize(text)
    shards = []
    step_size = math.ceil(len(sentences) / required_slices)
    print("Chunks: %i | Chunk-Size: %i" % (required_slices, step_size))
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
        command = "Summarize the IT-Security report"
        try:
            result = client.predict(
                command,
                s,
                0.2,
                0.75,
                50,
                4,
                400,
                False,
                api_name="/predict"
            )

            summaries.append(result)
        except Exception as e:
            print("ERROR in INTERMEDIATE SUMMARIZATION TASK:%s" % e)
            summaries.append("")

    return ' '.join(summaries)


with open('responses-alpaca.csv', 'w', encoding='UTF-8') as w:
    writer = csv.writer(w, delimiter=';')
    writer.writerow(['URL', 'TITLE', 'RAW', 'SUMMARY', 'LANG', 'DATE'])

with open('summary-data.CSV', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=';')

    # Skip header
    next(reader)

    for r in reader:
        print("###########\nNEW REPORT: %s\nURL: %s" % (r[1], r[0]))

        command = "Summarize the IT-Security report"
        summary = ""

        temp = 0.2
        maxNewToken = 400
        topp = 0.75
        topk = 50

        deltasummaries = False

        r[2] = unidecode.unidecode(r[2])
        r[2] = r[2].replace("#", "")
        r[2] = re.sub("\_{3,}", "", r[2])

        inputtext = r[2]

        if len(inputtext) > 5000:
            print("Splitting...")
            inputtext = SplitAndRequest(inputtext, command, 4000)
            deltasummaries = True
            print("DELTA SUMMARIES:\n%s" % inputtext)


        Errors = True
        try:
            while Errors:
                summary = client.predict(
                    command,
                    inputtext,
                    temp,
                    topp,
                    topk,
                    4,
                    400,
                    False,
                    api_name="/predict"
                )
                Errors = False
        except Exception as e:
            print("ERROR in SUMMARIZATION TASK: %s" % e)

        if len(summary) <= 500:
            print("Could not generate long enough summary. If there has been a delta summary we take this as overall summary")
            if deltasummaries:
                print("Delta summary found... Taking this as overall summary")
                summary = inputtext
            else:
                print("Delta summary not found. Shit.")
                summary = "NOPE"

        print("OVERALL SUMMARY:\n%s" % summary)

        with open('responses-alpaca.csv', 'a', encoding='UTF-8') as w:
            writer = csv.writer(w, delimiter=';')
            writer.writerow([r[0], r[1], r[2].replace(';', ','), summary.replace('\t', '').replace('\n', ' '), r[3], r[4]])

        raw_len = len(r[2])
        summary_len = len(summary)

        print("""RAW LEN: %i
SUMMARY LEN: %i""" % (raw_len, summary_len))