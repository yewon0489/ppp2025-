def caesar_encode(text: str, shift: int = 3) -> str:
    result = []
    for ch in text:
        if 'a' <= ch <= 'z':

            new_code = (ord(ch) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(new_code))
        elif 'A' <= ch <= 'Z':
            new_code = (ord(ch) - ord('A') + shift) % 26 + ord('A')
            result.append(chr(new_code))
        else:
            result.append(ch)
    return "".join(result)

def caesar_decode(text: str, shift: int = 3) -> str:
    return caesar_encode(text, -shift)

def main():
    en = input("암호화할 메시지를 입력하세요: ")
    encoded = caesar_encode(en, 3)
    print(f"인코딩 결과: {encoded}")

    de = input("복호화할 메시지를 입력하세요: ")
    decoded = caesar_decode(de, 3)
    print(f"디코딩 결과: {decoded}")

if __name__ == "__main__":
    main()
