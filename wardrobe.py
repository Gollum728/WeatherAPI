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



def loadWardrobe():
    clothesDict = {}
    with open("clothes.csv", "r") as f:
        data = csv.reader(f)
        for row in data:
            clothesDict[row[0]] = row[-1].replace(" ", "") 
    print(clothesDict)
    return clothesDict

# def getClothingImages(wardrobe, recommendation):
#     imagesDict = {}
#     mainTop = recommendation["primary_outfit"]["top"]
#     mainBottom = recommendation["primary_outfit"]["bottom"]
#     topImage = wardrobe[mainTop]["image"]
#     bottomImage = wardrobe[mainBottom]["image"]
#     imagesDict["Top"] = topImage
#     imagesDict["Bottom"] = bottomImage
#     if len(recommendation["primary_outfit"]["outerwear"]) > 0:
#         mainOutwerwear = recommendation["primary_outfit"]["outerwear"]
#         imagesDict["Outerwear"] = wardrobe[mainOutwerwear]["image"]
#     else:
#         imagesDict["Outerwear"] = None
#     return imagesDict