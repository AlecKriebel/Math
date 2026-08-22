from pathlib import Path

from PIL import Image, ImageOps


AUDIT_ROOT = Path(__file__).resolve().parents[1]
PAGE_DIR = AUDIT_ROOT / "rendered_pages"


def main() -> None:
    page_paths = sorted(PAGE_DIR.glob("page-*.png"))
    if len(page_paths) != 20:
        raise RuntimeError(f"expected 20 rendered pages, found {len(page_paths)}")

    for group_start in range(0, len(page_paths), 4):
        pages = []
        for page_path in page_paths[group_start : group_start + 4]:
            with Image.open(page_path) as image:
                page = image.convert("RGB")
                page.thumbnail((850, 1100), Image.Resampling.LANCZOS)
                pages.append(ImageOps.expand(page, border=2, fill="black"))

        cell_width = max(page.width for page in pages) + 36
        cell_height = max(page.height for page in pages) + 36
        sheet = Image.new("RGB", (2 * cell_width, 2 * cell_height), "#d8d8d8")
        for index, page in enumerate(pages):
            x = (index % 2) * cell_width + (cell_width - page.width) // 2
            y = (index // 2) * cell_height + (cell_height - page.height) // 2
            sheet.paste(page, (x, y))

        first_page = group_start + 1
        sheet.save(PAGE_DIR / f"contact-{first_page:02d}.png")


if __name__ == "__main__":
    main()
