"""Reproduce bounded lexical observations on source texts downloaded in ignored tmp.

This is a locator aid, not a proof that equivalent mathematics is absent.
"""
from pathlib import Path
import hashlib
import json
import re

RAW = Path(__file__).resolve().parents[6] / "tmp" / "priority_exact" / "subsequent_checker"
NAMES = ["primary_mdpi_pdf", "primary_arxiv_v1_pdf", "similarity_arxiv_pdf", "later_2025"]
TERMS = ["koszul", "complete intersection", "multiplication", "matrix", "matrices", "syzyg", "rank", "generated", "generators"]

def main():
    result = {}
    for name in NAMES:
        path = RAW / (name + ".txt")
        data = path.read_bytes()
        text = data.decode()
        result[name] = {
            "text_sha256": hashlib.sha256(data).hexdigest(),
            "counts": {term: len(re.findall(re.escape(term), text, re.I)) for term in TERMS},
        }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
