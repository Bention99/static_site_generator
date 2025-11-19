import os
import logging
import shutil


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

def main():
    print("Hello from static-site-generator!")
    copy_static_to_public()

if __name__ == "__main__":
    main()
