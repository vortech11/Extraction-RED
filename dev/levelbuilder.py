import json, os

rectangles = []
polygons = []
triggers = []

rectangles.extend([0, 300, 1000, 400, 31, 158, 27]) #main green floor
rectangles.extend([200, 200, 100, 30, 50, 50, 50]) #start floating platform
rectangles.extend([0, 200, 50, 200, 70, 70, 70])
rectangles.extend([450, 100, 50, 200, 70, 70, 70])
rectangles.extend([620, 80, 150, 30, 50, 50, 50])
rectangles.extend([720, 240, 200, 60, 100, 100, 100])
rectangles.extend([920, 120, 50, 180, 70, 70, 70])
rectangles.extend([-10, 5, 10, 5, 100, 100, 100])

polygons.extend([350, 300, 450, 250, 450, 300, 450, 301, 100, 100, 100])
polygons.extend([590, 300, 720, 240, 720, 300, 719, 300, 100, 100, 100])

triggers.extend([0, 0, 1, 1, "levelload", "level2.json"])

Geometry = {
    "rect": [
    ],
    "tri": [
    ],
    "triggers": [
    ]
}

for x in range(0, len(rectangles), 7):
    Geometry["rect"].append([{"points": [rectangles[x], rectangles[x+1], rectangles[x+2], rectangles[x+3]]}, 
                             {"color": [rectangles[x+4], rectangles[x+5], rectangles[x+6]]}])

for x in range(0, len(polygons), 11):
    Geometry["tri"].append([{"points": [polygons[x], polygons[x+1], polygons[x+2], polygons[x+3], polygons[x+4], polygons[x+5], polygons[x+6], polygons[x+7]]}, 
                            {"color": [polygons[x+8], polygons[x+9], polygons[x+10]]}])

for x in range(0, len(triggers), 6):
    Geometry['triggers'].append([{"points": [triggers[x], triggers[x+1], triggers[x+2], triggers[x+3]]}, 
                                 {"func": triggers[x+4]}, {"perameters": triggers[x+5]}])

Geometry["player"] = {}
Geometry["player"]["startpos"] = [250, 170]
Geometry["player"]["save"] = {}
Geometry["player"]["save"]["pos"] = Geometry["player"]["startpos"]
Geometry["player"]["save"]["velosity"] = [0, 0]

script_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_directory, "../levels/level.json")
levelfile = open(json_file_path, "w")
json.dump(Geometry, levelfile, indent=6)
levelfile.close()