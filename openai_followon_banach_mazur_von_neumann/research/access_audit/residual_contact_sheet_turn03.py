#!/usr/bin/env python3
"""Make a small local contact sheet only from already retained residual PNGs.

No PDF is opened or detector rerun. Labels contain only hash prefixes and page
numbers, with no unrelated path/title/page text. Pillow must already be available.
The output must remain in the operator's ignored local temporary image directory.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = json.loads(args.metadata.read_text())["records"]
    selected = [(record["original_sha256"], image)
                for record in records if record["status"] == "partially_checked_no_match"
                for image in record["images"] if image.get("retained")]
    columns, width, height = 2, 560, 760
    rows = (len(selected) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * width, max(1, rows) * height), "#dddddd")
    draw = ImageDraw.Draw(sheet)
    for index, (digest, image_record) in enumerate(selected):
        with Image.open(image_record["path"]) as image:
            image = image.convert("RGB")
            image.thumbnail((width - 20, height - 40))
            x, y = (index % columns) * width, (index // columns) * height
            sheet.paste(image, (x + (width - image.width) // 2, y + 30))
        draw.text((x + 10, y + 8), digest[:12] + " page " + str(image_record["page"]), fill="black")
    sheet.save(args.output)
    print(json.dumps({"rendered_retained_images": len(selected), "size_pixels": sheet.size}))


if __name__ == "__main__":
    main()
