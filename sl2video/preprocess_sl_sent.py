import re

def remove_tonemark(string : str):
    from_ = [
        '[àảãáạ]', '[ằẳẵắặ]', '[ầẩẫấậ]',
        '[ÀẢÃÁẠ]', '[ẰẲẴẮẶ]', '[ẦẨẪẤẬ]',
        '[èẻẽéẹ]', '[ềểễếệ]', '[ìỉĩíị]',
        '[ÈẺẼÉẸ]', '[ỀỂỄẾỆ]', '[ÌỈĨÍỊ]',
        '[òỏõóọ]', '[ồổỗốộ]', '[ờởỡớợ]',
        '[ÒỎÕÓỌ]', '[ỒỔỖỐỘ]', '[ỜỞỠỚỢ]',
        '[ùủũúụ]', '[ừửữứự]', '[ỳỷỹýỵ]',
        '[ÙỦŨÚỤ]', '[ỪỬỮỨỰ]', '[ỲỶỸÝỴ]',
    ]

    to_ = [
        'a', 'ă', 'â', 'A', 'Ă', 'Â',
        'e', 'ê', 'i', 'E', 'Ê', 'I',
        'o', 'ô', 'ơ', 'O', 'Ô', 'Ơ',
        'u', 'ư', 'y', 'U', 'Ư', 'Y',
    ]

    for i, c in enumerate(from_):
        string = re.sub(rf"{c}", to_[i], string)

    return string

def is_number_using_try_except(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def convert_into_token_list(word_infor_list):
    finger_pos_list = ['Np', 'Ny', 'Ni', 'Np', 'NNP', 'Ny']
    remove_pos_list = ['CH']
    token_list = []
    for word_infor in word_infor_list:
        if(word_infor['posTag'] in finger_pos_list):
            word = word_infor['wordForm'].replace("_", "")
            no_tonemark_word = remove_tonemark(word)
            c_list = [c for c in no_tonemark_word]
            token_list.extend(c_list)
        elif word_infor['posTag'] in remove_pos_list:
            continue
        elif word_infor['posTag'] == 'M' and is_number_using_try_except(word_infor['posTag']):
            c_list = [c for c in str(word_infor['wordForm'])]
            token_list.append(c_list)
        else:
            token_list.append(word_infor['wordForm'])
        token_list.append("")
    return token_list



# text = "tôi có 2 quả cam"
# print(remove_tonemark(text))
word_infor_list = [{'index': 1, 'wordForm': 'Trần_Đề', 'posTag': 'Np', 'nerLabel': 'B-LOC', 'head': '_', 'depLabel': '_'}, {'index': 2, 'wordForm': 'tiết_kiệm', 'posTag': 'V', 'nerLabel': 'O', 'head': '_', 'depLabel': '_'}, {'index': 3, 'wordForm': 'công_nghiệp', 'posTag': 'N', 'nerLabel': 'O', 'head': '_', 'depLabel': '_'}, {'index': 4, 'wordForm': 'thúc_đẩy', 'posTag': 'V', 'nerLabel': 'O', 'head': '_', 'depLabel': '_'}, {'index': 5, 'wordForm': 'xã_hội', 'posTag': 'N', 'nerLabel': 'O', 'head': '_', 'depLabel': '_'}, {'index': 6, 'wordForm': 'phát_triển', 'posTag': 'V', 'nerLabel': 'O', 'head': '_', 'depLabel': '_'}]
print(convert_into_token_list(word_infor_list))