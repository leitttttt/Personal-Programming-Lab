import sys
from collections import Counter

def count_letters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("文件不存在")
        return

    # 只保留英文字母
    letters = [ch.lower() for ch in content if ch.isalpha() and ch.isascii()]
    total = len(letters)
    
    if total == 0:
        print("没有英文字母")
        return

    # 统计
    counts = Counter(letters)
    # 排序：先按频率降序，频率相同按字典序升序
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    print(f"总字母数: {total}")
    for char, count in sorted_counts:
        percentage = (count / total) * 100
        print(f"{char.upper()}: {percentage:.2f}%")

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        count_letters(sys.argv[2])
    else:
        print("用法: python WF.py -c <文件名>")