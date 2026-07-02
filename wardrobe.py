import csv

def getClothes():
    clothesString = ""
    with open("clothes.csv", "r") as f:
        data = csv.reader(f)
        for row in data:
            del row[-1]
            newRow = ",".join(row)
            clothesString = clothesString + newRow + "\n"
    return clothesString
location = input("Enter a city : ")


def loadWardrobe():
    clothesDict = {}
    with open("clothes.csv", "r") as f:
        data = csv.reader(f)
        for row in data:
            clotheDict = {}
            clothesDict[row[0]] = clotheDict
            clotheDict["image"] = row[-1].replace(" ", "")
    return clothesDict

def getClothingImages(wardrobe, recommendation):
    imagesDict = {}
    mainTop = recommendation["primary_outfit"]["top"]
    mainBottom = recommendation["primary_outfit"]["bottom"]
    topImage = wardrobe[mainTop]["image"]
    bottomImage = wardrobe[mainBottom]["image"]
    imagesDict["Top"] = topImage
    imagesDict["Bottom"] = bottomImage
    return imagesDict