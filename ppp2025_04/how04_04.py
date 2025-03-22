#원의 둘레
import math
pi=math.pi
r=int(input("반지름이 얼마인가요?"))
width=math.pow(r,2)*pi
circumference=2*pi*r
print(f"반지름이 {r}인 원의 둘레는{circumference:.1f}이고 넓이는{width:.2f}")