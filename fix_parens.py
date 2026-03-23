import os

directory = r"d:\climateScope"
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".py") and "site-packages" not in root and ".venv" not in root:
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Fix the trailing parenthesis syntax error
            content = content.replace("st.container() for _ in range(2)]", "st.container() for _ in range(2)]")
            content = content.replace("st.container() for _ in range(3)]", "st.container() for _ in range(3)]")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

print("Fixed SyntaxError parenthesis loops.")
