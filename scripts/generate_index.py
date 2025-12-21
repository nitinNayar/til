import os

ROOT_DIR = 'tips'
README_PATH = 'README.md'
START_MARKER = '``'
END_MARKER = '``'

def generate_markdown():
    content = []
    if not os.path.exists(ROOT_DIR):
        return "No tips folder found."
        
    for category in sorted(os.listdir(ROOT_DIR)):
        cat_path = os.path.join(ROOT_DIR, category)
        if os.path.isdir(cat_path):
            pretty_cat = category.replace('-', ' ').title()
            content.append(f"### 📂 {pretty_cat}")
            
            files = [f for f in os.listdir(cat_path) if f.endswith('.md')]
            if not files:
                content.append("_No tips yet._")
            
            for filename in sorted(files):
                file_path = os.path.join(cat_path, filename)
                title = filename
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('#'):
                            title = first_line.lstrip('# ').strip()
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                
                relative_path = f"tips/{category}/{filename}".replace(" ", "%20")
                content.append(f"- [{title}]({relative_path})")
            
            content.append("") 
            
    return "\n".join(content)

def update_readme():
    new_content = generate_markdown()
    
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return

    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    if START_MARKER not in readme_content or END_MARKER not in readme_content:
        print("Error: Markers not found in README.md")
        return

    before = readme_content.split(START_MARKER)[0]
    after = readme_content.split(END_MARKER)[1]
    
    updated_readme = f"{before}{START_MARKER}\n{new_content}\n{END_MARKER}{after}"
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    
    print("README.md updated successfully.")

if __name__ == "__main__":
    update_readme()
