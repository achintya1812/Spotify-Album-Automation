import csv 

with open("liked_songs.csv", "r") as file:
    data = csv.reader(file, delimiter=",")
    
