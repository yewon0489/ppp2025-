weight=int(input("몸무게게가 얼마인가요?=>"))
height=int(input("키가 얼마인가요?=>"))
import math
height_m= height/100
BMI= weight/ math.pow(height_m,2)
print('{}kg, {}m, BMI: {}'.format(weight, height, int(BMI)))
