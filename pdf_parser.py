from PyPDF2 import PdfReader
import re
import csv

def parse(PDF):
	reader = PdfReader(PDF)

	text = ""

	for page in reader.pages:
		text += page.extract_text()

	tokenized_text = text.split("\n")

	data = [datum for datum in tokenized_text[18:39] if re.search(r"\d", datum) != None]

	for datum in data:
		datum_index = datum.find(re.search(r"\d", datum).group())
		data_index = data.index(datum)
		data[data_index] = datum[:datum_index] + "," +  datum[datum_index:]
		data[data_index] = data[data_index].split(",")
		if len(data[data_index]) > 2:
			data[data_index].pop(1)

	fields = ["Test", "Result"]

	with open("data.csv", 'w') as file:
		csvwriter = csv.writer(file)
		csvwriter.writerow(fields)
		csvwriter.writerows(data)

parse("CBC-sample-blood-test-report.pdf")