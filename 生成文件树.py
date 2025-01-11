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
        
        # Skip __pycache__ folder, .git folder, .vscode folder, and 生成文件树.py file
        if item in ['__pycache__', '.git', '.vscode', '生成文件树.py',".gitignore","data_loader原.py","data_analysis原.py","example","test","test折线图.py"]:
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
    dir_path = r"."
    generate_file_tree(dir_path)
    print(f"文件树已生成并保存为 file_tree.txt")
