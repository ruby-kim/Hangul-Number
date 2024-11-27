"""함수 변환 코드."""

import re

from change_list import changeList


def parse_korean_number_with_units(ko_text, num_list):
    """한글 숫자를 아라비아 숫자로 변환하며 단위를 고려하여 계산."""
    unit_values = {k: v for k, v in num_list if v >= 10}  # 자릿수 단위
    digit_values = {k: v for k, v in num_list if v < 10}  # 한 자릿수

    total = 0  # 최종 결과값
    current = 0  # 현재 숫자 계산값
    section_total = 0  # 상위 단위 섹션 합산 결과

    for char in ko_text:
        if char in digit_values:
            current += digit_values[char]  # 숫자를 누적
        elif char in unit_values:
            unit = unit_values[char]
            if unit >= 10000:  # 상위 단위 (만, 억 등)
                section_total += current  # 현재 값 누적
                total += section_total * unit  # 상위 단위와 결합하여 결과 추가
                section_total = 0  # 섹션 초기화
                current = 0  # 현재 값 초기화
            else:  # 하위 단위 (천, 백 등)
                current = max(current, 1) * unit
                section_total += current
                current = 0
        else:
            section_total += current
            current = 0

    total += section_total + current  # 마지막 값 추가
    return total


def hangul2num(raw_text):
    """텍스트 내 한글 숫자를 숫자로 변환."""
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
        arabic_number = parse_korean_number_with_units(
            hangul_number, full_num_list
        )
        return str(arabic_number) + unit

    return pattern.sub(replacer, raw_text)
