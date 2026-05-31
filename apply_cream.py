import os

def apply():
    with open('build_new_ui_v3.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add alpha-cream to tailwind config
    content = content.replace(
        '"surface-variant": "#f1f5f9"',
        '"surface-variant": "#f1f5f9",\n                "alpha-cream": "#fdfbf7"'
    )

    # Add bg-alpha-cream to body
    content = content.replace(
        '<body class="font-sans text-sm">',
        '<body class="font-sans text-sm bg-alpha-cream">'
    )

    # Replace bg-white with bg-alpha-cream globally
    content = content.replace('bg-white', 'bg-alpha-cream')

    with open('build_new_ui_v3.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    apply()
