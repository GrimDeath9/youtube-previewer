import re

"""
Set of functions used to format different formats of YouTube links
"""

__long_link = 'https://www.youtube.com/watch?v='
__short_link = 'https://youtu.be/'
__long_link_safe = 'https:\/\/www.youtube.com\/watch\?v='
__short_link_safe = 'https:\/\/youtu.be\/'
__live_link = 'https:\/\/www.youtube.com\/live\/'
__pattern = f'^({__long_link_safe}|{__short_link_safe}|{__live_link})'

def __turn_list(input: list | str) -> list:
    """
    Converts the given input into a list
    """
    if isinstance(input, str):
        return [input]
    elif isinstance(input, list):
        return input

def filter_valid(list: list | str):
    """
    Filters out only valid YouTube links. 
    Valid formats are:
      - https://www.youtube.com/watch?v=
      - https://youtu.be/
      - https://www.youtube.com/live/
    """
    output = []
    for i in __turn_list(list):
        tested = re.search(__pattern + "(.{11})", i)
        if tested is not None:
            output.append(tested.string)
    return output

def filter_ids(list: list | str):
    """
    Filters out video ids from valid YouTube links.
    For example: https://www.youtube.com/watch?v=dQw4w9WgXcQ -> dQw4w9WgXcQ
    """
    output = []
    for i in filter_valid(__turn_list(list)):
        output.append(re.sub(__pattern, '', i)[:11])
    return output 

def __unsafe_format(list: list, header: str):
    """
    Add given header to all given elements of list.
    """
    return [f"{header}{i}" for i in list]

def __format(list: list, header: str):
    """
    Adds given header to all valid video ids.
    """
    return [f"{header}{i}" for i in filter_ids(list)]

def __format_id_header(list: list, header: str):
    """
    Returns formatted header and id in a pair
    Returns: id, formatted_link
    """
    ids = filter_ids(list)
    return ids, __unsafe_format(ids, header)

def format_short(input: list | str) -> list | str:
    """
    Formats the given link into the format https://youtu.be/{id}.
    """
    formatted = __format(__turn_list(input), __short_link)
    return formatted[0] if isinstance(input, str) else formatted

def format_id_short(input: list | str):
    """
    Formats given input into a a tuple of containing the id and short link.
    """
    formatted = __format_id_header(__turn_list(input), __short_link)
    return (formatted[0][0], formatted[1][0])  if isinstance(input, str) else formatted

def format_long(input: list | str):
    """
    Formats the given link into the format https://www.youtube.com/watch?v=.
    """
    formatted = __format(__turn_list(input), __long_link)
    return formatted[0] if isinstance(input, str) else formatted

def format_id_long(list: list | str):
    """
    Formats given input into a a tuple of containing the id and long link.
    """
    formatted = __format_id_header(__turn_list(list), __long_link)
    return (formatted[0][0], formatted[1][0])  if isinstance(input, str) else formatted

if __name__ == '__main__':
    print(format_id_short('https://www.youtube.com/watch?v=K_JIEPooIYA'))