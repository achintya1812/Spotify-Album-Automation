import csv

with open("liked_songs.csv", "r", encoding="utf-8") as file:
    data = csv.reader(file, delimiter=",")

    for row in data:
        print(row)
