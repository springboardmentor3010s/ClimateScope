import os
import re

def replace_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    # Replace st.columns with st.container lists
    def replacer(match):
        arg = match.group(1)
        if arg.isdigit():
            n = int(arg)
            return f"[st.container() for _ in range({n})]"
        else:
            # It's a tuple like (1.4, 1.6)
            n = arg.count(',') + 1
            return f"[st.container() for _ in range({n})]"
            
    content = re.sub(r'st\.columns\(([^)]+)\)', replacer, content)
    
    # Let's also increase the chart height from height=3xx to height=500
    # or height=4xx since they are full width now
    content = re.sub(r'height=3\d\d', 'height=450', content)
    content = re.sub(r'height=500', 'height=500', content)
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")

directory = r"d:\climateScope"
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".py") and "site-packages" not in root and ".venv" not in root:
            replace_in_file(os.path.join(root, file))

print("Layout refactor complete!")
