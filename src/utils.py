import shutil
from pathlib import Path
import os

from blocknode import markdown_to_html_node, extract_title


def delete_directory_content(dest_path: str = "public"):
    home = Path.cwd()
    public = home / dest_path
    if public.exists():
        shutil.rmtree(public)


def create_public_content(from_path: str = "static", dest_path: str = "public"):
    home = Path.cwd()

    for content in os.walk(from_path):
        content_path = content[0]
        new_path = content[0].replace(from_path, dest_path, 1)
        current = home / new_path
        current.mkdir()

        new_files = content[2]
        if new_files:
            for new_file in new_files:
                shutil.copy(home / content_path / new_file, current)


def create_html_content_from_md(basepath, from_path, template_path, dest_path):
    home = Path.cwd()

    for content in os.walk(from_path):
        content_path = content[0]
        new_path = content[0].replace(from_path, dest_path, 1)
        current = home / new_path
        current.mkdir(exist_ok=True)

        new_files = content[2]
        if new_files:
            for new_file in new_files:
                new_html_file = new_file
                new_html_file = new_html_file.replace(".md", ".html")
                generate_page(
                    basepath,
                    home / content_path / new_file,
                    template_path,
                    current / new_html_file,
                )


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as t:
        template_file = t.read()

    html_title = extract_title(markdown)
    html_body = markdown_to_html_node(markdown)

    template_file = template_file.replace("{{ Title }}", html_title)
    template_file = template_file.replace("{{ Content }}", html_body.to_html())
    template_file = template_file.replace('href="/', f'href="{basepath}')
    template_file = template_file.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as d:
        d.write(template_file)
    print("Finished generating page")
