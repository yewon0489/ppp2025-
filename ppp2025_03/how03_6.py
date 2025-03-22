#두 지점 사이 거리 구하기
import math
x1=int(input("첫 번째 점의 x좌표를 입력해주세요=>"))
y1=int(input("첫 번째 점의 y좌표를 입력해주세요=>"))
x2=int(input("두 번째 점의 x좌표를 입력해주세요=>"))
y2=int(input("두 번째 점의 y좌표를 입력해주세요=>"))
distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
print(f"두점 사이의 거리는{distance:.3f}")