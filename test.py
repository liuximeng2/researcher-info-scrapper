import os

count = 0
neg = 0
for dirpath, dirnames, filenames in os.walk('images'):
    if len(os.listdir(dirpath)) > 0:
        count += 1
    else:
        neg += 1
        print('Directory:', dirpath)

print(count)
print(neg)

