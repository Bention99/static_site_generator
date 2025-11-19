import os
import logging
import shutil
import re
from pathlib import Path
from markdown_blocks import markdown_to_html_node


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("--------- GENERATING STARTED ---------")
    print("Hello from static-site-generator!")
    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/blog/glorfindel/index.md", "template.html", "public//blog/glorfindelindex.html")
    '''generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/index.md", "template.html", "public/index.html")'''

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_text = f.read()
    node = markdown_to_html_node(markdown_text)
    html = node.to_html()
    title = extract_title(markdown_text)
    title_string = ""
    for i in title:
        title_string = "".join(i)
    template_text_new = template_text.replace("{{ Title }}", title_string).replace("{{ Content }}", html)
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(template_text_new, encoding="utf-8")
    logging.info(f"Created 'index.html' File in {dest_path} successfully.")
    

def extract_title(markdown_text):
    return re.findall(r'^\s*#\s+(.+)$', markdown_text, re.MULTILINE)

def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
        logging.info("Directory 'public' deleted.")
    
    os.mkdir("public")
    logging.info("Directory 'public' created successfully.")

    static_path_items = os.listdir(os.path.join(os.getcwd(), "static"))

    for item in static_path_items:
        abs_path = os.path.join(os.getcwd(), f"static/{item}")
        if os.path.isdir(abs_path):
            copy_directory(abs_path)
        elif os.path.isfile(abs_path):
            copy_file(abs_path)
    
def copy_directory(abs_path):
    rel_path = os.path.relpath(abs_path, "static")
    public_path = os.path.join("public", rel_path)
    os.makedirs(public_path, exist_ok=True)
    logging.info(f"Ensured directory exists: {public_path}")

    for name in os.listdir(abs_path):
        child = os.path.join(abs_path, name)
        if os.path.isdir(child):
            copy_directory(child)
        elif os.path.isfile(child):
            copy_file(child)

def copy_file(abs_path):
    rel_path = os.path.relpath(abs_path, "static")
    public_path = os.path.join("public", rel_path)
    shutil.copy2(abs_path, public_path)
    logging.info(f"File '{rel_path}' copied successfully to '{public_path}'")

if __name__ == "__main__":
    main()
