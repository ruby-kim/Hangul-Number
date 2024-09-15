# Hangul-Number

한글 숫자 텍스트를 숫자로 변환합니다.

<!-- [![Python](https://img.shields.io/pypi/pyversions/hangul_num.svg?style=plastic)](https://badge.fury.io/py/hangul_num) -->
<!-- [![PyPI](https://badge.fury.io/py/hangul_num.svg)](https://badge.fury.io/py/hangul_num)   -->
<!--Change **[Korean number text -> Arabic number]** or<br>
**[Arabic number -> Korean number text]**-->

### Installation

- pypi: (준비 중)<!--`pip install hangul_number`-->
- source code:
  ```bash
  git clone https://github.com/ruby-kim/hangul_number.git
  cd hangul
  python setup.py install
  ```

### Getting Started

- pypi
  ```python
  >>> from hangul_number.chgFormat import hangul_num
  >>> text1 = "맛있는 포카칩이 구천팔백칠십육억오천사백삼십이만천백십일원!"
  >>> print(hangul_num(text1))
  맛있는 포카칩이 987654321111원!
  >>> text2 = "맛있는 포카칩이 구천팔백칠십육억오천사백삼십이만천백십일원에서 오백십만육십구원, 만사천칠백원을 거쳐 이제는 천오백원으로!"
  >>> print(hangul_num(text2))
  맛있는 포카칩이 987654321111원에서 5100069원, 14700원을 거쳐 이제는 1500원으로!
  ```
- source code:
  `python run.py`

### Note

<!-- - only operate about cardinal number(기수: 일, 이, 삼, 사, ...) text -> real num -->
<!-- - You can see more information here: [docs/README.md](https://github.com/study-ai-data/hangul_num/blob/master/docs/README.md) -->
