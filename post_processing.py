import re
def post_processing(text: str) -> str:
    text_list = text.split(". ")
    text_list = list(dict.fromkeys(text_list))
    text = " ".join(text_list)
    
    dot_check = re.compile(r'[^A-Za-z0-9가-힣]')
    
    final_result = ""
    if text:
        if re.match(dot_check, text[-1]) is None:
            dot_idx = 0
            for idx, char in enumerate(text[::-1]):
                if char == ".":
                    dot_idx += idx
                    break
            text = text[::-1][dot_idx:]
            final_result += text[::-1]
        else:
            final_result += text
    
    return final_result