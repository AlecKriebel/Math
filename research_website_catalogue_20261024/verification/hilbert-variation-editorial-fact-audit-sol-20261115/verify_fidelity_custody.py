"""Read-only editorial source comparison; standard library, no project imports."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import html
import json
import re

OWN = Path(__file__).resolve().parent
PROJECT = OWN.parents[1]
WRITER = PROJECT / "papers/23204591/reviews/editorial"


def require(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    require(path.is_file() and not path.is_symlink(), "Nonregular file: " + str(path))
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "SHA256": hashlib.sha256(raw).hexdigest()}


def snapshot(root):
    files, directories = [], []
    for path in sorted(root.rglob("*")):
        require(not path.is_symlink(), "Symlink: " + str(path))
        if path.is_dir():
            directories.append(str(path.relative_to(root)))
        else:
            row = pin(path)
            row["path"] = str(path.relative_to(root))
            files.append(row)
    raw = json.dumps({"files": files, "directories": directories}, sort_keys=True, separators=(",", ":")).encode()
    return len(files), len(directories), hashlib.sha256(raw).hexdigest()


class TextById(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.text = [], {}

    def handle_starttag(self, tag, attributes):
        element_id = dict(attributes).get("id")
        if element_id:
            require(element_id not in self.text, "Duplicate ID")
            self.text[element_id] = []
        if tag not in {"br", "meta", "link", "img", "hr", "input", "source", "wbr"}:
            self.stack.append((tag, element_id))

    def handle_endtag(self, tag):
        require(bool(self.stack) and self.stack[-1][0] == tag, "Unbalanced HTML")
        self.stack.pop()

    def handle_data(self, text):
        for _, element_id in self.stack:
            if element_id:
                self.text[element_id].append(text)


frozen = json.loads((OWN / "INITIAL_PINS.json").read_text())
exposure = json.loads((OWN / "WRITER_EXPOSURE.json").read_text())
for row in frozen["references_by_exact_pin"] + frozen["original_manuscript_and_native_metadata"] + frozen["core_17_original_pins"] + [frozen["sole_separately_authorized_helper_pin"], exposure["root_forwarded_FINAL"], exposure["writer_current_guard"], exposure["writer_manifest"]]:
    require(pin(Path(row["path"])) == row, "Frozen original pin mismatch: " + row["path"])

namespace_results = []
for row in frozen["complete_protected_namespaces"] + [exposure["writer_namespace"]]:
    observed = snapshot(Path(row["path"]))
    require(observed == (row["files"], row["directories"], row["canonical_full_namespace_SHA256"]), "Complete namespace mismatch: " + row["path"])
    namespace_results.append({"path": row["path"], "files": observed[0], "directories": observed[1], "unchanged": True})

source = PROJECT / "papers/23204591/sources"
ready = json.loads((source / "SOURCE_READY.json").read_text())
record = json.loads((source / "record.response.body").read_text())
tex = Path(ready["controlling_TeX"]["extracted_path"]).read_text()
abstract = tex.split("\\begin{abstract}", 1)[1].split("\\end{abstract}", 1)[0]
abstract = abstract.replace("\\in", "∈").replace("$", "").replace("^", "").replace("{", "").replace("}", "")
compact = lambda text: re.sub(r"\s+", "", text)
main = (WRITER / "public-main.html").read_text()
parsed = TextById()
parsed.feed(main)
require(not parsed.stack, "Unclosed MAIN markup")
require(compact(abstract) == compact("".join(parsed.text["printed-abstract"])), "Entire printed abstract mismatch")
require("".join(parsed.text["native-description"]) == html.unescape(record["metadata"]["description"]), "Entire separate deposit description mismatch")
assets = []
for row in ready["all_native_assets_in_original_order"]:
    name = row["original_api_file_object"]["key"]
    require((WRITER / "assets" / name).read_bytes() == Path(row["path"]).read_bytes(), "Native asset altered: " + name)
    assets.append(name)
require(assets == ["README.md", "verification-supplement.zip", "source.zip", "paper.pdf"], "Native asset order changed")
print(json.dumps({"status": "PASS_INDEPENDENT_FIDELITY_CUSTODY", "complete_namespaces": namespace_results, "original_core_files": 17, "sole_checkpoint_helper_checked_separately": True, "printed_abstract_entire": True, "distinct_deposit_description_entire": True, "unchanged_native_assets_in_original_order": assets, "writer_FINAL": exposure["root_forwarded_FINAL"], "scientific_programs_executed": 0, "network_requests": 0, "writes": 0}, indent=2))
