import csv
import matplotlib.pyplot as pyplt

with open("scored-summaries.csv", "r", encoding="UTF-8") as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)

    count = 0

    raw = []
    data = {}

    for r in reader:
        raw.append(r)
        data[count] = (float(r[5].split(":")[3].replace(" ","").replace("}","").replace("'","")),
                       float(r[6].split(":")[3].replace(" ","").replace("}","").replace("'","")),
                       float(r[7].split(":")[3].replace(" ","").replace("}","").replace("'","")))
        count = count + 1


    max_l = 0
    min_l = 1
    sumdata = 0

    plot_data = {}

    for k,v in data.items():
        if v[2] > max_l:
            max_l = v[2]
        if v[2] < min_l:
            min_l = v[2]

        sumdata = sumdata+v[2]

        plot_data[k] = v[2]


    rouge_l = sumdata/len(data.values())

    pyplt.plot(plot_data.values())
    pyplt.show()

    print(data)