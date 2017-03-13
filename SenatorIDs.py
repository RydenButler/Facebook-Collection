import csv

senators = []
with open('SenatorURLs.csv', 'rb') as csvfile:
  links = csv.reader(csvfile, delimiter=' ', quotechar='|')
  for row in links:
    senators.append(row)
