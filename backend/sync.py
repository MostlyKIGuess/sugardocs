import os
import re
import shutil
import subprocess
from pathlib import Path
import frontmatter

SUGAR_DOCS_REPO = "https://github.com/sugarlabs/sugar-docs.git"
TEMP_CLONE_DIR = "sugar-docs-temp"
TARGET_DIR = "src/site/notes/src"
EXCLUDED_DIRS = [".git", ".github", "images"]
EXCLUDED_FILES = ["README.md"]  

def run_command(command):
    """Run a shell command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(f"Error: {result.stderr}")
        exit(1)
    return result.stdout.strip()

def clone_repo():
    """Clone the sugar-docs repository"""
    print(f"Cloning {SUGAR_DOCS_REPO} into {TEMP_CLONE_DIR}...")
    if os.path.exists(TEMP_CLONE_DIR):
        shutil.rmtree(TEMP_CLONE_DIR)
    run_command(f"git clone {SUGAR_DOCS_REPO} {TEMP_CLONE_DIR}")

def fix_links(content, filename):
    """Fix markdown links in the content"""
    # Replace relative links that don't have src/ prefix
    content = re.sub(r'\[([^\]]+)\]\((?!http|src/)([^)]+)\.md\)', r'[\1](src/\2)', content)
    
    # Remove .md extension from links
    content = re.sub(r'\[([^\]]+)\]\((src/[^)]+)\.md\)', r'[\1](\2)', content)
    
    return content

def process_file(src_path, dest_path):
    """Process a single file: add frontmatter and fix links"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_links(content, dest_path.name)
    
    metadata = {
        'dg-publish': True,
        'permalink': f"/src/{dest_path.stem}/",
        'noteIcon': ''
    }
    
    post = frontmatter.Post(content, **metadata)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
    
    print(f"Processed: {dest_path}")

def sync_files():
    """Sync files from cloned repo to target directory"""
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    src_dir = Path(TEMP_CLONE_DIR) / "src"
    if not src_dir.exists():
        print(f"Source directory {src_dir} not found!")
        return
    
    for src_file in src_dir.glob("**/*.md"):
        if any(excluded in src_file.parts for excluded in EXCLUDED_DIRS):
            continue
        
        if src_file.name in EXCLUDED_FILES:
            continue
        
        dest_filename = src_file.name.lower().replace(' ', '-')
        dest_path = Path(TARGET_DIR) / dest_filename
        
        process_file(src_file, dest_path)
    
    src_images = Path(TEMP_CLONE_DIR) / "images"
    if src_images.exists():
        dest_images = Path(TARGET_DIR) / "img"
        if os.path.exists(dest_images):
            shutil.rmtree(dest_images)
        shutil.copytree(src_images, dest_images)
        print(f"Copied images to {dest_images}")

def cleanup():
    """Clean up temporary files"""
    if os.path.exists(TEMP_CLONE_DIR):
        shutil.rmtree(TEMP_CLONE_DIR)
    print("Cleanup complete")

def main():
    """Main function"""
    print("Starting Sugar-Docs sync process...")
    clone_repo()
    sync_files()
    cleanup()
    print("Sync completed successfully!")

if __name__ == "__main__":
    main()