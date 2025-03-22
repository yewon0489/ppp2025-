#두 지점 사이 거리 구하기
x=int(input("첫 번째 점의 x좌표를 입력해주세요=>"))
y=int(input("첫 번째 점의 y좌표를 입력해주세요=>"))
if x>0 and y>0:
    print("제 1사분면입니다.")

elif x<0 and y>0:
    print("제 2사분면입니다.")
elif x<0 and y<0:
    print("제 3사분면입니다.")
elif x > 0 and y<0:
    print("4사분면입니다.")
else:
    print("사분면위에 위치하지 않습니다.")

