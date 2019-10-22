from PIL import Image, ImageStat
import os
import sys
import argparse
from pathlib import Path


# dHash algorithm
def hash_image(image_path):
    img = Image.open(image_path, mode='r').resize((8, 8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    results = sum((1 if p > mean else 0) << i for i, p in enumerate(img.getdata()))
    return results


# find image in folder
def find_img(parent_folder):
    dups = {}
    for dir, subdirs, fileList in os.walk(parent_folder):
        for filename in fileList:
            path = os.path.join(dir, filename)
            # Calculate Dhash
            file_hash = hash_image(path)
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


# Joins two dictionaries with similar image
def join(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


# Printing results
def print_results(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('_______________________________')
        for result in results:
            for subresult in result:
                print(subresult)
            print('_______________________________')

    else:
        print('No duplicate/modification files found.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('-p', '--path', type=Path, required=True, help='folder with images')
    args = parser.parse_args()

    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            if args.path:
                join(dups, find_img(i))
            else:
                print('%s is not a valid path' % i)
                sys.exit()
        print_results(dups)
    else:
        print('Usage: python solution.py')


