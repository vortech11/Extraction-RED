import json
printrect = []
printpoly = []
with open("level.json", "r") as levelfile:
    leveldict = json.load(levelfile)
    levelfile.close()

for x in range(len(leveldict['rect'])):
    printrect.extend(leveldict['rect']['rect'+str(x+1)]['points'])
    printrect.extend(leveldict['rect']['rect'+str(x+1)]['color'])

for x in range(len(leveldict['tri'])):
    printpoly.extend(leveldict['tri']['tri'+str(x+1)]['points'])

print(printrect)
print('')
print(printpoly)