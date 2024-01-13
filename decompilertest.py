import json

with open("level.json", "r") as levelfile:
    leveldict = json.load(levelfile)
    levelfile.close()

for z in range(2):
    for x in range(2):
        print(leveldict['rect']['rect'+str(z+1)]['points'][x], leveldict['rect']['rect'+str(z+1)]['points'][x+1])
    print("")

