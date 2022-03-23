from datetime import datetime
import re

months = {'January': 1,
          'February': 2,
          'March': 3,
          'April': 4,
          'May': 5,
          'June': 6,
          'July': 7,
          'August': 8,
          'September': 9,
          'October': 10,
          'November': 11,
          'December': 12
          }


def get_timestamp(input_string):
    strings = re.split(r',|:|\|| ', input_string)
    temp = [s for s in strings if s]
    y = int(temp[2])
    m = months[temp[0]]
    d = int(temp[1])
    h = int(temp[3]) if 'am' in temp[4] else int(temp[3]) + 12
    h = 0
    mm = int(re.sub(r'am|pm', '', temp[4]))

    result = datetime(y, m, d, h, mm).timestamp()
    print(result)

    return result

print(get_timestamp('March 23, 2022 | 12:05pm'))