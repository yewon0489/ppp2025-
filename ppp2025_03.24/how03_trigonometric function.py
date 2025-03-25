import math
for i in range(1, 91):
    rad=math.radians(i)
    sin=math.sin(rad)
    cos=math.cos(rad)
    tan=math.tan(rad)
    print(f"{rad:.5f},{sin:.5f},{cos:.5f},{tan:.5f}")