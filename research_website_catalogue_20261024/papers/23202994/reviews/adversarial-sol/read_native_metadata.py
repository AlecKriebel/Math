"""Passive extraction of the assigned original native HTML metadata only."""
from pathlib import Path
from html.parser import HTMLParser
import json

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parents[1] / "sources"


class MetadataReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.text = []
        self.meta = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "template"):
            self.skip += 1
        if tag == "meta":
            self.meta.append(dict(attrs))

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data.strip())


parser = MetadataReader()
parser.feed((SOURCE / "native-metadata/record-page.html").read_text())
assert parser.skip == 0
visible = "\n".join(parser.text) + "\n"
(LANE / "native-record-visible-text.txt").write_text(visible)
(LANE / "native-html-meta-tags.json").write_text(json.dumps(parser.meta, indent=2) + "\n")
print(visible)
print(json.dumps(parser.meta, indent=2))
