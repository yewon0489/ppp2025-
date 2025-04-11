def total_calorie(fruits,fruits_calorie_dic):
    total = 0
    for i in fruits:
        total+=(fruits[i]/100)*fruits_calorie_dic[i]
    return total

#파일을 어떻게 딕셔너리에 넣는지 배우는 과정
def read_db(filename):
    calorie_dic = {}
    with open(filename, encoding="utf-8-sig") as f:
        lines= f.readlines()
        print(lines)
        for line in lines[1:]:
            line = line.strip()
            token= line.split(",")
            calorie_dic[token[0]] = int(token[1])/int(token[2])       
    return calorie_dic


def main(): 
    fruit_cal= read_db("./calorie_db.csv")
    fruit_eat={"쑥":100,"바나나":200,}

    total= 0
    for item in fruit_eat:
        total += (fruit_cal[item]*fruit_eat[item])


    print(f"총 칼로리는 {total}kcal입니다. ")
if __name__ == "__main__" :
    main()