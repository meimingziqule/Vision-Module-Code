import os
import shutil
import random

def split_dataset(base_dir, train_ratio=0.8):
    images_dir = os.path.join(base_dir, 'images')
    labels_dir = os.path.join(base_dir, 'labels')
    
    train_images_dir = os.path.join(images_dir, 'train')
    train_labels_dir = os.path.join(labels_dir, 'train')
    val_images_dir = os.path.join(images_dir, 'val')
    val_labels_dir = os.path.join(labels_dir, 'val')
    
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)
    
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    
    if len(image_files) != len(label_files):
        raise ValueError("The number of image files and label files does not match.")
    
    paired_files = list(zip(image_files, label_files))
    random.shuffle(paired_files)
    
    num_train = int(len(paired_files) * train_ratio)
    train_files = paired_files[:num_train]
    val_files = paired_files[num_train:]
    
    for img_file, lbl_file in train_files:
        shutil.copy(os.path.join(images_dir, img_file), os.path.join(train_images_dir, img_file))
        shutil.copy(os.path.join(labels_dir, lbl_file), os.path.join(train_labels_dir, lbl_file))
    
    for img_file, lbl_file in val_files:
        shutil.copy(os.path.join(images_dir, img_file), os.path.join(val_images_dir, img_file))
        shutil.copy(os.path.join(labels_dir, lbl_file), os.path.join(val_labels_dir, lbl_file))

if __name__ == "__main__":
    base_dir = r'd:\k210_use_file\k210-yolov5-test'
    split_dataset(base_dir)
