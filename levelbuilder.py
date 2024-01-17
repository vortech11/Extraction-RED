import json

rectangles = []
polygons = []

rectangles.extend([0, 300, 1000, 400, 31, 158, 27]) #main green floor
rectangles.extend([200, 200, 100, 30, 50, 50, 50]) #start floating platform
rectangles.extend([0, 200, 50, 200, 70, 70, 70])
rectangles.extend([450, 100, 50, 200, 70, 70, 70])
rectangles.extend([620, 80, 150, 30, 50, 50, 50])
rectangles.extend([720, 240, 200, 60, 100, 100, 100])
rectangles.extend([920, 120, 50, 180, 70, 70, 70])

polygons.extend([350, 300, 450, 250, 450, 300, 450, 301])
polygons.extend([590, 300, 720, 240, 720, 300, 719, 300])

Geometry = {
    "rect": {
    },
    "tri": {
    }
}

for x in range(0, len(rectangles), 7):
    Geometry["rect"]["rect"+str(int(x/7+1))] = {}
    Geometry["rect"]["rect"+str(int(x/7+1))]["points"] = [rectangles[x], rectangles[x+1], rectangles[x+2], rectangles[x+3]]
    Geometry["rect"]["rect"+str(int(x/7+1))]["color"] = [rectangles[x+4], rectangles[x+5], rectangles[x+6]]
    print(int(x/7+1))

for x in range(0, len(polygons), 8):
    Geometry["tri"]["tri"+str(int(x/8+1))] = {}
    Geometry["tri"]["tri"+str(int(x/8+1))]["points"] = [polygons[x], polygons[x+1], polygons[x+2], polygons[x+3], polygons[x+4], polygons[x+5], polygons[x+6], polygons[x+7]]
    print(int(x/7+1)) 

Geometry["player"] = {}
Geometry["player"]["startpos"] = [250, 170]
Geometry["player"]["save"] = {}
Geometry["player"]["save"]["pos"] = Geometry["player"]["startpos"]
Geometry["player"]["save"]["velosity"] = [0, 0]

levelfile = open("level.json", "w")
json.dump(Geometry, levelfile, indent=6)
levelfile.close()