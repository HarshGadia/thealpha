with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("\"Vaibhav Domkundwar's thesis on where the next  companies are built.',", 
                    "\"Vaibhav Domkundwar's thesis on where the next companies are built.\",")

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed syntax error in data.js!")
