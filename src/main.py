import sys

from utils import (
    delete_directory_content,
    create_public_content,
    create_html_content_from_md,
)


def main(basepath):
    delete_directory_content(dest_path="docs")
    create_public_content(dest_path="docs")
    create_html_content_from_md(basepath, "content", "template.html", "docs")


if __name__ == "__main__":
    arguements = sys.argv
    basepath = "/"
    if len(arguements) == 2:
        basepath = arguements[1]

    main(basepath)
