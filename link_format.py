import re

"""
Set of functions used to format different formats of YouTube links
"""

__long_link = "https://www.youtube.com/watch?v="
__short_link = "https://youtu.be/"
__long_link_safe = "https:\/\/www.youtube.com\/watch\?v="
__short_link_safe = "https:\/\/youtu.be\/"
__live_link = "https:\/\/www.youtube.com\/live\/"
__pattern = f"^({__long_link_safe}|{__short_link_safe}|{__live_link})"

def __turn_list(input: list | str) -> list:
    if isinstance(input, str):
        return [input]
    elif isinstance(input, list):
        return input

def filter_valid(list: list | str):
    output = []
    for i in __turn_list(list):
        tested = re.search(__pattern + "(.{11})", i)
        if tested is not None:
            output.append(tested.string)
    return output

def filter_ids(list: list | str):
    output = []
    for i in filter_valid(__turn_list(list)):
        output.append(re.sub(__pattern, '', i)[:11])
    return output 

def __unsafe_format(list: list, header: str):
    return [f"{header}{i}" for i in list]

def __format(list: list, header: str):
    return [f"{header}{i}" for i in filter_ids(list)]

def __format_id_header(list: list, header: str):
    ids = filter_ids(list)
    return ids, __unsafe_format(ids, header)

def format_short(list: list | str):
    return __format(__turn_list(list), __short_link)

def format_id_short(list: list | str):
    return __format_id_header(__turn_list(list), __short_link)

def format_long(list: list | str):
    return __format(__turn_list(list), __long_link)

def format_id_long(list: list | str):
    return __format_id_header(__turn_list(list), __long_link)

if __name__ == "__main__":
    print(format_short("https://www.youtube.com/watch?v=K_JIEPooIYA"))