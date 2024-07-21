import os
import shutil

def rename_and_copy_files(source_folder, target_folder):
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        # 构建源文件的完整路径
        source_file = os.path.join(source_folder, filename)

        # 检查是否是文件
        if os.path.isfile(source_file):
            # 去掉文件扩展名
            base_name, ext = os.path.splitext(filename)

            # 将文件名转换为整数
            try:
                file_number = int(base_name)
            except ValueError:
                print(f"Skipping non-integer filename: {filename}")
                continue

            # 构建新的文件名
            new_filename = f"{file_number + 1}-0{ext}"

            # 构建目标文件的完整路径
            target_file = os.path.join(target_folder, new_filename)

            # 复制文件到目标文件夹
            shutil.copy2(source_file, target_file)
            print(f"Copied and renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    source_folder = r"D:\Mx-yolov3_EN_3.0.0\datasets\test\picture\1_out"  # 使用原始字符串避免转义问题
    target_folder = r"D:\Mx-yolov3_EN_3.0.0\datasets\test\picture\1-222222222222222"  # 使用原始字符串避免转义问题

    rename_and_copy_files(source_folder, target_folder)
