import os

def generate_file_tree(dir_path, depth=3, output_file='file_tree.txt'):
    with open(output_file, 'w', encoding='utf-8') as f:
        generate_file_tree_recursive(dir_path, 0, depth, f, '')

def generate_file_tree_recursive(dir_path, current_depth, max_depth, file, prefix):
    if current_depth > max_depth:
        return
    
    files = os.listdir(dir_path)
    for i, item in enumerate(files):
        item_path = os.path.join(dir_path, item)
        
        # Skip __pycache__ folder
        if item == '__pycache__':
            continue
        
        if os.path.isdir(item_path):
            if i == len(files) - 1:
                # Last item
                file.write(f'{prefix}└── {item}/\n')
                new_prefix = prefix + '    '
            else:
                # Not the last item
                file.write(f'{prefix}├── {item}/\n')
                new_prefix = prefix + '|   '
            generate_file_tree_recursive(item_path, current_depth + 1, max_depth, file, new_prefix)
        else:
            if i == len(files) - 1:
                # Last item
                file.write(f'{prefix}└── {item}\n')
            else:
                # Not the last item
                file.write(f'{prefix}├── {item}\n')

if __name__ == "__main__":
    dir_path = r"D:\高行周的资料\大二上\analysis_app\v1"
    generate_file_tree(dir_path)
    print(f"文件树已生成并保存为 file_tree.txt")
