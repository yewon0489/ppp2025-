def c2f(t_c):
    temp_f = (t_c*1.8)+32
    print("{}c => {}℉".format(t_c, temp_f))
    return True

t_c= int(input("썹시는 몇 도인가요?") )

def main():
    c2f(t_c)

if __name__ == "__main__":
    main()