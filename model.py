import argparse
import glob
import os
from collections import Counter
import matplotlib.pyplot as plt

def parse_args() -> str:
    parser = argparse.ArgumentParser(description="F-Prez")
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    return args.path

def file_walker_leveled(path):
    paths = glob.glob(f'{path}/*')
    result = []
    for p in paths:
        if os.path.isfile(p):
            result.append(p)
    return result

def file_walker_gen(path):
    paths = glob.glob(f'{path}/*')
    for p in paths:
        if os.path.isfile(p):
            yield p
        if os.path.isdir(p):
            rs = file_walker(p)
            for r in rs:
                yield r

def file_walker(path) -> list:
    results = []
    paths = glob.glob(f'{path}/*')
    for p in paths:
        if os.path.isfile(p):
            results.append(p)
        if os.path.isdir(p):
            rs = file_walker(p)
            rs = [r.lower() for r in rs]
            results+=rs
    return results 

def letters(path):
    return [p.split("/")[-1][0] for p in file_walker(path)]

def letters_counter(path):
    ps = [p.split("/")[-1][0] for p in file_walker(path)]
    return dict(Counter(ps))

def create_bar(xs, ys, title="Analysis"):
    _, ax = plt.subplots()
    bars = plt.bar(xs, ys)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.title(title)
    plt.xticks(rotation=10)
    plt.savefig("data.png")
    for bar in bars:
        height = round(bar.get_height(), 1)
        ax.annotate(f'{height}', 
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.savefig('data.png') 

#path = parse_args()
# path = "/home/doms/Projects/git"
# #results = file_walker(path)
# gs = file_walker_gen(path)
# print(next(gs))