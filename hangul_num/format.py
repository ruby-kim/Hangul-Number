"""format.py."""

import re

from change_list import changeList


def parse_korean_number(ko_text, num_list):
    """텍스트 내에서 한글로 작성된 숫자 여부 판단 및 숫자로 반환."""
    unit_values = {k: v for k, v in num_list if v >= 10}
    digit_values = {k: v for k, v in num_list if v < 10}

    result = 0
    current = 0
    temp_word = ""

    for char in ko_text:
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


def hangul2num(raw_text):
    """텍스트 내 한글을 숫자로 변환."""
    data = changeList()

    # 순서 숫자와 기본 숫자를 모두 합침
    full_num_list = data.card_num + data.ord_num

    # 숫자와 단위 매핑 생성
    pattern = re.compile(
        r"((?:"
        + "|".join(re.escape(k) for k, _ in full_num_list)
        + r")+)("
        + "|".join(data.ord_unit.keys())
        + r")"
    )

    def replacer(match):
        hangul_number = match.group(1)
        unit = match.group(2)
        arabic_number = parse_korean_number(hangul_number, full_num_list)
        return str(arabic_number) + unit

    return pattern.sub(replacer, raw_text)

