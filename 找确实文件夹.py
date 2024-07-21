import os

def find_missing_files(folder_path, prefix, start, end):
    # 创建一个包含所有预期文件编号的集合
    expected_numbers = set(range(start, end + 1))
    
    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        # 检查文件名是否以指定前缀开头
        if filename.startswith(prefix):
            # 提取文件编号
            try:
                file_number = int(filename.replace(prefix, ''))
                # 从预期编号集合中移除存在的编号
                expected_numbers.discard(file_number)
            except ValueError:
                # 如果文件名不符合预期格式，跳过该文件
                continue
    
    # 打印缺失的文件名
    for missing_number in sorted(expected_numbers):
        print(f"Missing file: {prefix}{missing_number}")

if __name__ == "__main__":
    folder_path = r"C:\Users\yy\Desktop\labels_my-project-name_2024-07-18-04-47-29l"  # 替换为你的文件夹路径
    prefix = "5-"
    start = 0
    end = 249

    find_missing_files(folder_path, prefix, start, end)
