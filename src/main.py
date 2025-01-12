from utils import (
    delete_directory_content,
    create_public_content,
    create_html_content_from_md,
)


def main():
    delete_directory_content()
    create_public_content()
    create_html_content_from_md("content", "template.html", "public")


if __name__ == "__main__":
    main()
