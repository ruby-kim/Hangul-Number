from change_list import changeList


def parse_korean_number(text, num_list):
    """한글 숫자를 아라비아 숫자로 변환"""
    unit_values = {k: v for k, v in num_list if v >= 10}
    digit_values = {k: v for k, v in num_list if v < 10}

    result = 0
    current = 0
    temp_word = ""
    
    for char in text:
        temp_word += char  # 한 글자씩 누적
        if temp_word in digit_values:  # 단일 숫자 매칭
            current = digit_values[temp_word]
            temp_word = ""
        elif temp_word in unit_values:  # 자릿수 단위 매칭
            current = max(current, 1) * unit_values[temp_word]
            result += current
            current = 0
            temp_word = ""
    result += current
    return result

def hangul_num(text):
    """TODO"""
    change_list = changeList()
    text = convert_text(text, change_list, is_cardinal=True)
    return text
