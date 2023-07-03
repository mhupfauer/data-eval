import rouge
from rouge import Rouge
import csv

counter = 0

with open("scored-summaries-alpaca.csv", 'w', encoding="UTF-8") as fx:
    writer = csv.writer(fx, delimiter=";")
    writer.writerow(("URL", "TITLE", "TEXT", "LANG", "ROUGE-1", "ROUGE-2", "ROUGE-L"))

with open("responses-alpaca.csv", 'r', encoding="UTF-8") as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)

    for l in reader:
        if counter == 249:
            print("SKIPPING 249")
            continue
        print("CALCULATING SCORE #%i" % counter)
        counter = counter + 1
        l.pop()
        report = l[2]
        l[3] = " ".join(l[3].replace('-','').split())
        summary = l[3]
        scorer = rouge.Rouge()
        score = scorer.get_scores(summary, report)

        with open("scored-summaries-alpaca.csv", 'a', encoding="UTF-8") as fx:
            writer = csv.writer(fx, delimiter=";")
            for v in score[0].values():
                l.append(v)
            writer.writerow(l)