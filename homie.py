# d = {}
# k=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']
# for i,v in enumerate(['C','D','H','S']):
#     s = set()
#     for j in range(2, 15):
#         if j != 8:
#             c = j + 13*i
#             s.add(c)
#             d[c] = f'{k[j-2]}{v}'
#         else:
#             print(s)
#             s = set()
#     print(s)
            # print(j + 13 * i, end=", ")
#     # print("")
# print(d)

# b ={}

# for k in d:
#     b[d[k]] = k

# print(b)

import time

start = time.time()
size = 10000
s = {1,2,3,4,5,6,7,8}
for _ in range(size):
    if 5 in s:
        s.remove(5)
    s.add(5)
end = time.time()

print(f'{end - start:.10f} seconds')

start = time.time()
s = {1,2,3,4,5,6,7,8}
for _ in range(size):
    s -= {5}
    s.add(5)
end = time.time()

print(f'{end - start:.10f} seconds')