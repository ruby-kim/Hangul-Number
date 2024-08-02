from hangul_num import ChangeList


def get_guessed_num_idx(text):
    """
    Args:
        :param: text(str)
    Returns:
        :param: result(list)
    """
    # 1. get cardinal number unit & ordinal number unit list
    changes = chgList()
    care_unit, ord_unit = changes.care_unit, changes.ord_unit

    # 2. find start index of each word in words list
    words = text.split(" ")
    flag_idx = [0]
    total_len = 0
    for i in range(len(words)):
        if i == 0:
            flag_idx = [0]
            total_len += len(words[i])+1
        else:
            flag_idx.append(total_len)
            total_len += len(words[i])+1

    # 3. find cardinal number unit start index,
    #         ordinal number unit start index,
    card_idx, ord_idx = [], []
    for i in range(len(words)):
        for value in care_unit.values():
            for idx, val in enumerate(value):
                if val in words[i] and words[i].index(val)+flag_idx[i] not in card_idx:
                    card_idx += [words[i].index(val)+flag_idx[i]]
        for value in ord_unit.values():
            for idx, val in enumerate(value):
                if val in words[i] and words[i].index(val)+flag_idx[i] not in ord_idx:
                    ord_idx += [words[i].index(val)+flag_idx[i]]

    return card_idx, ord_idx


def judge_exist_num_text(text):
    """
    judge whether num text exists or not in text
    Args:
        :param: text(str)
    Returns:
        :param: carResult(boolean): exist cardinal num text-True / not exist cardinal num text-False
        :param: ord_result(boolean): exist ordinal num text-True / not exist ordinal num text-False
    """
    card_idx, ord_idx = get_guessed_num_idx(text)
    card_result, ord_result = False, False

    if len(card_idx) is not 0:
        card_result = True
    if len(ord_idx) is not 0:
        ord_result = True
    return card_result, ord_result


def find_num_text_section(text, Num, Idx):
    """
    find number text section
    Args:
        :param: text(str): origin text
        :param: Num(list): num_list(c.f. korNum/chgList.py)
        :param: Idx(list): the number start unit list in text
    Returns:
        :param: results_list(list): a list included each num text range
    """
    fir_idx = 0
    pass_val = 0
    results_list = list()
    for idx in Idx:
        for i in range(idx, -1, -1):
            if text[i-pass_val] == ' ':
                break
            else:
                for num in Num:
                    if len(num[0]) == 2 and i-pass_val is not 0:
                        text[i-pass_val] = text[i-pass_val-1] + text[i-pass_val]
                        pass_val += 1
                    if text[i-pass_val] == num[0]:
                        fir_idx = i - pass_val
        results_list.append((fir_idx, idx))
    print(results_list)
    return results_list


def text_of_num_text_section(text, results_list):
    num_text = list()
    for elem in results_list:
        num_text.append(text[elem[0]:elem[1]])
    return num_text


def separate_each_num_text_to_list(text, results_list, unit_kor_num):
    result = list()
    for card_list in results_list:
        word_list = list()
        tmp = ""
        for i in range(card_list[1] - 1, card_list[0] - 1, -1):
            if text[i] not in unit_kor_num:
                word_list.append(text[i] + tmp)
                tmp = ""
            else:
                if i != card_list[0] and text[i - 1] in unit_kor_num:
                    word_list.append(text[i])
                    continue
                tmp = text[i] + tmp
                if i == card_list[0]:
                    word_list.append(tmp)
        word_list.reverse()
        result.append(word_list)
    return result


def calc_element(word_list):
    """
    calculate numbers: addition, multiplication
    Args:
        :param: word_list(list): list of each korean text num
    Returns:
        :param: result(int): real num value
    """
    num_list = list()
    for word in word_list:
        result = 0
        tmp = 0
        for i in range(len(word)):
            if i is not 0 and word[i] > word[i - 1]:
                result += tmp * word[i]
                tmp = 0
            else:
                tmp += word[i]
        result += tmp
        num_list.append(result)
    return num_list


def card_function(text, card_idx):
    """
    change text num -> real num [cardinal number]
    Args:
        :param: text(str): origin text
    Returns:
        :param: text(str): changed text(text num -> real num)
    """
    changes = chgList()
    card_num = changes.card_num

    # 1. find num text section
    cardresults_list = find_num_text_section(text, card_num, card_idx)
    cardr_results_list_text = text_of_num_text_section(text, cardresults_list)

    # 2. separate kor and num to list
    korcard_num, realcard_num = list(), list()
    for card in card_num:
        korcard_num.append(card[0])
        realcard_num.append(card[1])

    base_kor_card_num = korcard_num[:9]  # 일, 이, 삼, 사, 오, 육, 칠, 팔, 구
    unit_kor_card_num = korcard_num[9:]  # 십, 백, 천, 만, 억, 조, 경, 해
    base_real_card_num = realcard_num[:9]  # 일, 이, 삼, 사, 오, 육, 칠, 팔, 구
    unit_real_card_num = realcard_num[9:]  # 십, 백, 천, 만, 억, 조, 경, 해

    # 3. separate each num text to list
    word_list = separate_each_num_text_to_list(text, cardresults_list, unit_kor_card_num)

    # 4. separate two length texts to one-one in specific condition
    for word in word_list:
        for i in range(len(word)):
            if len(word[i]) == 2:
                if word[i][1] != '십' and word[i][1] != '백' and word[i][1] != '천':
                    word.insert(i + 1, word[i][1])
                    word[i] = word[i][0]

    # 5. change each num text to real num
    for word in word_list:
        for i in range(len(word)):
            if len(word[i]) == 2:
                tmp1 = base_real_card_num[base_kor_card_num.index(word[i][0])]
                tmp2 = unit_real_card_num[unit_kor_card_num.index(word[i][1])]
                word[i] = tmp1 * tmp2
            else:
                if word[i] not in korcard_num:
                    continue
                word[i] = realcard_num[korcard_num.index(word[i][0])]

    # 6. multiply & plus all of elements
    result = calc_element(word_list)

    # 7. grouping text<->num pair as dictionary & descending
    pair_text_num = dict()
    for i in range(len(result)):
        pair_text_num[cardr_results_list_text[i]] = result[i]
    pair_text_num = sorted(pair_text_num.items(), reverse=True, key=lambda item: item[1])

    # 8. change entire num text(word) to real num
    for key, value in pair_text_num:
        text = text.replace(key, str(value))

    return text


def ord_function(text, ord_idx):
    """
    change text num -> real num [cardinal number]
    Args:
        :param: text(str): origin text
    Returns:
        :param: text(str): changed text(text num -> real num)
    """
    changes = chgList()
    ord_num = changes.ord_num

    # 1. find num text section
    ordresults_list = find_num_text_section(text, ord_num, ord_idx)
    ord_results_list_text = text_of_num_text_section(text, ordresults_list)
    exit()

    # 2. separate kor and num to list
    korcard_num, realcard_num = list(), list()
    for card in ord_num:
        korcard_num.append(card[0])
        realcard_num.append(card[1])

    base_kor_card_num = korcard_num[:9]  # 일, 이, 삼, 사, 오, 육, 칠, 팔, 구
    unit_kor_card_num = korcard_num[9:]  # 십, 백, 천, 만, 억, 조, 경, 해
    base_real_card_num = realcard_num[:9]  # 일, 이, 삼, 사, 오, 육, 칠, 팔, 구
    unit_real_card_num = realcard_num[9:]  # 십, 백, 천, 만, 억, 조, 경, 해

    # 3. separate each num text to list
    word_list = separate_each_num_text_to_list(text, ordresults_list, unit_kor_card_num)

    # 4. separate two length texts to one-one in specific condition
    for word in word_list:
        for i in range(len(word)):
            if len(word[i]) == 2:
                if word[i][1] != '십' and word[i][1] != '백' and word[i][1] != '천':
                    word.insert(i + 1, word[i][1])
                    word[i] = word[i][0]

    # 5. change each num text to real num
    for word in word_list:
        for i in range(len(word)):
            if len(word[i]) == 2:
                tmp1 = base_real_card_num[base_kor_card_num.index(word[i][0])]
                tmp2 = unit_real_card_num[unit_kor_card_num.index(word[i][1])]
                word[i] = tmp1 * tmp2
            else:
                if word[i] not in korcard_num:
                    continue
                word[i] = realcard_num[korcard_num.index(word[i][0])]

    # 6. multiply & plus all of elements
    result = calc_element(word_list)

    # 7. grouping text<->num pair as dictionary & descending
    pair_text_num = dict()
    for i in range(len(result)):
        pair_text_num[ord_results_list_text[i]] = result[i]
    pair_text_num = sorted(pair_text_num.items(), reverse=True, key=lambda item: item[1])

    # 8. change entire num text(word) to real num
    for key, value in pair_text_num:
        text = text.replace(key, str(value))

    return text


def kor2num(text):
    """
    Args:
        :param: text(str)
    Returns:
        :param: result(list)
    """
    card_idx, ord_idx = get_guessed_num_idx(text)
    ord_result = ord_function(text, ord_idx)
    card_result = card_function(ord_result, card_idx)
    return card_result


def num2kor(text):
    return
