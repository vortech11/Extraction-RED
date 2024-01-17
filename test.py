d = {0:0, 1:1, 2:2, 3:3}
print({"two" if k == 2 else k:v for k,v in d.items()})