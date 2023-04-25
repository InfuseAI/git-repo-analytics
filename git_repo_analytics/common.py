import csv


def read_repo():
    with open('repos.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield tuple(row.values())
