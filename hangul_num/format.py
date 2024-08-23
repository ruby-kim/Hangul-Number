from change_list import changeList


def get_num_unit_indices(text, unit_dict):
    """Get starting indices for units in text."""
    words = text.split(" ")
    flag_idx = [
        sum(len(words[j]) + 1 for j in range(i)) for i in range(len(words))
    ]
    indices = []
    for i, word in enumerate(words):
        for unit_list in unit_dict.values():
            if any(val in word for val in unit_list):
                indices.append(flag_idx[i] + word.index(unit_list[0]))
    return indices


def parse_num_sections(text, indices):
    """Identify number sections based on indices."""
    sections = []
    for idx in indices:
        start = next((i for i in range(idx, -1, -1) if text[i] == " "), -1) + 1
        sections.append((start, idx))
    return sections


def get_converted_num_list(text, num_dict):
    """Return converted number list from text."""
    return [num_dict.get(num, num) for num in text]


def calc_elements(word_list, base_num, unit_num):
    """Calculate number based on base and unit num."""
    num_list = []
    for word in word_list:
        result, tmp = 0, 0
        for num in map(lambda w: unit_num.get(w, base_num.get(w, 0)), word):
            if num and tmp and num > tmp:
                result += tmp * num
                tmp = 0
            else:
                tmp += num
        num_list.append(result + tmp)
    return num_list


def convert_text(text, change_list, is_cardinal=True):
    """Main function to convert text to numerical representation."""
    unit_dict = change_list.card_unit if is_cardinal else change_list.ord_unit

    indices = get_num_unit_indices(text, unit_dict)
    sections = parse_num_sections(text, indices)
    word_lists = [text[start:end] for start, end in sections]

    num_base, num_unit = (
        {k: v for k, v in change_list.card_num[:9]},
        {k: v for k, v in change_list.card_num[9:]},
    )
    result = calc_elements(word_lists, num_base, num_unit)

    return {text[s:e]: num for (s, e), num in zip(sections, result)}


def hangul_num(text):
    """TODO"""
    change_list = changeList()
    text = convert_text(text, change_list, is_cardinal=True)
    return text
