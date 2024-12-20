import os
import json

def info_sanity_check():
    total_count = 0
    john_doe_count = 0
    empty_count = 0
    for dirpath, dirnames, filenames in os.walk('info'):
        for file in os.listdir(dirpath):
            total_count += 1
            with open(os.path.join(dirpath, file)) as f:
                data = json.load(f)
            if data['last_name'] == 'Doe':
                john_doe_count += 1
                print('Directory:', file)
            if data['first_name'] == '':
                empty_count += 1
                print('Directory:', file)

    print(total_count)
    print(john_doe_count)
    print(empty_count)

def image_sanity_check():
    too_much_count = 0
    count = 0
    neg = 0
    for dirpath, dirnames, filenames in os.walk('images'):
        if len(os.listdir(dirpath)) > 1:
            too_much_count += 1
            print('too much Directory:', dirpath)
        elif len(os.listdir(dirpath)) == 1:
            count += 1
        else:
            neg += 1
            print('Directory:', dirpath)

    print(too_much_count)
    print(count)
    print(neg)

if __name__ == '__main__':
    # info_sanity_check()
    image_sanity_check()

