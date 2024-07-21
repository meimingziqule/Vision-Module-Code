import os

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.startswith('x-'):
            continue  # 跳过以 'x-' 开头的文件

        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if lines:
                first_line = lines[0].strip()
                parts = first_line.split()
                if parts:
                    try:
                        x = int(filename.split('-')[0])
                        first_number = int(parts[0])
                        if first_number != x:
                            parts[0] = str(x)
                            new_first_line = ' '.join(parts)
                            lines[0] = new_first_line + '\n'
                            with open(file_path, 'w') as file:
                                file.writelines(lines)
                    except ValueError:
                        print(f"文件 {filename} 的第一行内容格式不正确，跳过处理。")

if __name__ == "__main__":
    directory = r'D:\k210_use_file\k210-yolov5-test\labels_2\val'  # 替换为你的文件夹路径
    process_files(directory)
