import csv

def prettify(csv_file):
    with open(csv_file, "r") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        data = []
        for row in csvreader:
            data.append(row)
    for datum in data:
        data[data.index(datum)] = " count is ".join(datum) + "\n"
    fileOut = open("data.txt", "a")
    fileOut.writelines(data)

prettify("data.csv")