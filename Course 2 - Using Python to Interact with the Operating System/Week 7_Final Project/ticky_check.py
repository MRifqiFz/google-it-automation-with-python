#!/usr/bin/env python3

import re
import sys
import csv

per_user = {}
error = {}

with open('syslog.log') as file:
    line = [i.strip() for i in file]
    for l in line:
        error_detail = re.search(r"ticky: [\w]* ([\w ]*)", l).group(1)
        error_name = re.search(r"ticky: ([\w]*)", l).group(1)
        username = re.search(r" \((.*)\)", l).group(1)
        error[error_detail] = error.get(error_detail, 0) + 1
        if username not in per_user.keys():
            per_user[username] = {}
            per_user[username]['INFO'] = 0
            per_user[username]['ERROR'] = 0
        else:
            if error_name == 'ERROR':
                per_user[username]['ERROR'] += 1
            else:
                per_user[username]['INFO'] += 1

dict_error = dict(sorted(error.items(), reverse=True))
dict_per_user = dict(sorted(per_user.items()))

# file.close()

print(error)
print(per_user)
with open('user_statistics.csv', 'w') as us:
    us.write("Username, INFO, ERROR\n")
    for key in dict_per_user:
        us.write("{}, {}, {}\n".format(
            key, dict_per_user[key]['INFO'], dict_per_user[key]['ERROR']))

with open('error_message.csv', 'w') as em:
    em.write("Error, Count\n")
    for key in dict_error:
        em.write("{}, {}\n".format(key, dict_error[key]))
