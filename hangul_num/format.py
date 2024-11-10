import re
from change_list import changeList


def parse_korean_number(ko_text, num_list):
    """한글 숫자를 아라비아 숫자로 변환 (억, 만 등 상위 단위 완전 분리 및 초기화)."""
    unit_values = {k: v for k, v in num_list if v >= 10}  # 자릿수 단위
    digit_values = {k: v for k, v in num_list if v < 10}  # 한 자릿수

    total = 0  # 전체 합산 결과
    section_result = 0  # 현재 섹션(억, 만 등)의 계산값
    current = 0  # 현재 숫자 값

    for char in ko_text:
        if char in digit_values:  # 한 자릿수 처리
            current += digit_values[char]
        elif char in unit_values:  # 자릿수 단위 처리
            unit = unit_values[char]
            if unit >= 10000:  # 상위 단위 (만, 억 등)
                section_result += current  # 현재 값을 섹션에 추가
                total += section_result * unit  # 섹션 값을 상위 단위로 누적
                section_result = 0  # 섹션 초기화
                current = 0  # 현재 값 초기화
            else:  # 하위 단위 (십, 백, 천)
                current = max(current, 1) * unit
                section_result += current
                current = 0
        else:
            if current > 0:
                section_result += current
                current = 0

    total += section_result + current  # 남은 값을 총합에 누적
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
        arabic_number = parse_korean_number(hangul_number, full_num_list)
        return str(arabic_number) + unit

    return pattern.sub(replacer, raw_text)


if __name__ == "__main__":
    text = "피카츄의 오십가지 돈까스, 라이츄의 백가지 놀이도구, 고라파덕의 천오백억삼십삼가지 보물, 냐옹이의 만구백십팔개의 동전"
    print(hangul2num(text))  # 피카츄의 50가지 돈까스, 라이츄의 100가지 놀이도구, 고라파덕의 1500000033가지 보물, 냐옹이의 918개의 동전
