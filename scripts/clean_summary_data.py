import csv

with open("clean-summary-data.CSV", "w", encoding="UTF-8") as wr:
    writer = csv.writer(wr, delimiter=";")

    with open("summary-data.CSV", "r", encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)

        for r in reader:
            r[2] = r[2].replace(";","")
            writer.writerow(r)