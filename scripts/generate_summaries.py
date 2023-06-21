import csv
import math

import nltk
from gradio_client import Client

nltk.download('popular')

client = Client("https://4ab1aac92e43b48920.gradio.live/")

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
        try:
            result = client.predict(
                query,
                len(query) + 500,
                api_name="/predict"
            )

            summaries.append(result.split("Summary:")[1])
        except Exception as e:
            print("ERROR in INTERMIDIATE SUMMARIZATION TASK")
            summaries.append("")

    return ' '.join(summaries)


with open ('responses.csv', 'w', encoding='UTF-8') as w:
    writer = csv.writer(w, delimiter=';')
    writer.writerow(['URL','TITLE','RAW','SUMMARY','LANG','DATE'])

with open('summary-data.CSV', 'r', encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=';')

    #Skip header
    next(reader)

    for r in reader:
        print("###########\nNEW REPORT: %s\nURL: %s" % (r[1], r[0]))
        command = "Generate a summary of the partial IT-Security Report given below. Include all relevant information contained in the report including but not limited to threat actor, attack vector and potential targets. Do not make up information that is not explicitly stated within the report. "
        summary = SplitAndRequest(r[2], command, 1200)
        counter = 0
        print("LENGTH AFTER SUMMARY 1: %i" % len(summary))
        while len(summary) > 1829:
            summary = SplitAndRequest(summary, command, 1000)
            counter = counter + 1
            print("LENGHT AFTER %ith summarization is: %i" % (counter, len(summary)))

        with open('responses.csv', 'a', encoding='UTF-8') as w:
            writer = csv.writer(w, delimiter=';')
            writer.writerow([r[0], r[1], r[2].replace(';',','), summary.replace('\t','').replace('\n', ' '), r[3], r[4]])
            
        raw_len = len(r[2])
        summary_len = len(summary)
        
        print("""RAW LEN: %i
SUMMARY LEN: %i""" % (raw_len, summary_len))
