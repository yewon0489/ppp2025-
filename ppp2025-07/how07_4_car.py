#  딸기 300g, 한라봉 150g 섭취하였을 때, 입력자료를 사전형으로 전달하면, 총 칼로리를 계
# 산하는 함수를 만드시오. fruits={“딸기”: 300, “한라봉”: 150}, fruits_calorie_dic={"한라봉":
# 50, "딸기": 34, "바나나": 77}. 과제 #06-01 활용. 함수명은 total_calorie(fruits,
# fruits_calorie_dic)

def total_calorie(fruits,fruits_calorie_dic):
    total = 0
    for i in fruits:
        total+=(fruits[i]/100)*fruits_calorie_dic[i]
    return total


def main():
    fruits= {"딸기": 300, "한라봉":150}
    fruits_calorie_dic={"한라봉": 50, "딸기": 34, "바나나": 77}
    total_calorie(fruits,fruits_calorie_dic)
    print(f"{total_calorie(fruits,fruits_calorie_dic):.2f}kcal")
if __name__ == "__main__" :
    main()
