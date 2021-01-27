import math
import string

y = 0
l = list(string.ascii_uppercase)
while True:
    i = ""
    if y >= 26:
        for k in range(int(math.log(y, 26))):
            m = (y - (y % 26)) % 26
            i += l[m]
    i += l[(y % 26)]
    print(y, i)
    y += 1
    if y >= 702:
        break
