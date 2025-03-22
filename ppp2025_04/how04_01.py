#bmi지수 구하기기
import math
weight=int(input("몸무게게가 얼마인가요=>"))
height=int(input("키가 얼마인가요?=>"))
height_m=height/100
BMI= weight/ math.pow(height_m,2)
if 23<= BMI <= 24.9:
    print("비만 전단계 입니다.")
elif 25<= BMI <= 29.9:
    print("1단계 비만입니다.")
elif 30<= BMI <= 34.9:
    print("2단계 비만입니다.")
elif 35<= BMI:
    print('3단계 비만입니다')        
   
#print('{}kg, {}m, BMI: {}'.format(weight, height, int(BMI)))
