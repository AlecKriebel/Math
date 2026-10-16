"""Repeat the source-only forbidden-token check from the authenticated manifest."""
from pathlib import Path
import datetime
import json
import re
from zoneinfo import ZoneInfo


def without_comments_and_strings(text):
    output, position, nesting, in_string = [], 0, 0, False
    while position < len(text):
        if nesting:
            if text[position:position + 2] == "/-":
                nesting += 1
                position += 2
            elif text[position:position + 2] == "-/":
                nesting -= 1
                position += 2
            else:
                if text[position] == "\n":
                    output.append("\n")
                position += 1
        elif in_string:
            if text[position] == "\\":
                output.extend("  ")
                position += 2
            elif text[position] == '"':
                in_string = False
                output.append(" ")
                position += 1
            else:
                output.append("\n" if text[position] == "\n" else " ")
                position += 1
        elif text[position:position + 2] == "/-":
            nesting = 1
            output.extend("  ")
            position += 2
        elif text[position:position + 2] == "--":
            end = text.find("\n", position)
            if end < 0:
                break
            output.append("\n")
            position = end + 1
        elif text[position] == '"':
            in_string = True
            output.append(" ")
            position += 1
        else:
            output.append(text[position])
            position += 1
    return "".join(output)


folder = Path(__file__).resolve().parent
manifest = json.loads((folder / "import_closure.json").read_text())
tokens = re.compile(r"\b(sorry|admit|axiom|opaque|unsafe|implemented_by|extern|native_decide|run_cmd|elab)\b")
hits = []
for entry in manifest["sources"]:
    code = without_comments_and_strings(Path(entry["path"]).read_text())
    for number, line in enumerate(code.splitlines(), 1):
        if tokens.search(line) or re.match(r"^\s*(?:(?:private|protected|noncomputable)\s+)*constant\s+\S+\s*[:(\[{]", line):
            hits.append({"module": entry["module"], "line": number, "text": line})
result = {
    "timestamp": datetime.datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
    "source_count": len(manifest["sources"]),
    "tokens": tokens.pattern,
    "method": "Removed nested Lean block comments, line comments and strings before scanning.",
    "limitation": "Source token scan only; not kernel checking or a proof-term axiom audit.",
    "hits": hits,
}
(folder / "code_token_scan.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"{len(manifest['sources'])} sources checked; {len(hits)} code-level token hits")
