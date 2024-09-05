import pygame
import os
import csv

class LevelData:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.levels_path = os.path.join(self.script_path, "levels")
        self.level_data = self.load_level_data()

    def load_level_data(self):
        gameStages = []

        for stage in sorted(os.listdir(self.levels_path)):
            level_data = [[] for i in range(32)]

            with(open(f"{self.levels_path}/{stage}", newline = "")) as csvFile:
                reader = csv.reader(csvFile, delimiter = ",")

                for i, row in enumerate(reader):
                    for j, tile in enumerate(row):
                        level_data[i].append(int(tile))
        
            gameStages.append(level_data)

        return gameStages

    def save_level_data(self, level_data):
        number = len(level_data)

        for i in range(number):
            num = i + 1 if len(str(i + 1)) > 1 else "0" + str(i + 1)
            
            with open(f"{self.levels_path}/BattleCityLevel{str(num)}.csv", "w", newline = "") as csvFile:
                writer = csv.writer(csvFile, delimiter = ",")

                for row in level_data[i]:
                    writer.writerow(row)

        return 