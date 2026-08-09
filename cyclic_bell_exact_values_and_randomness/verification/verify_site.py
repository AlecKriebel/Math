#!/usr/bin/env python3
"""Dependency-free validation for the scoped cyclic-Bell website merger."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
CANONICAL_ROUTE = "/Math/papers/cyclic-bell-exact-values-and-randomness/"
CANONICAL_URL = "https://aleckriebel.github.io" + CANONICAL_ROUTE
CANONICAL = DOCS / "papers/cyclic-bell-exact-values-and-randomness/index.html"
OLD = {
    "cyclic-bell-tsirelson-bound":
        "c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f",
    "cyclic-bell-randomness-counterexample":
        "3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975",
    "permutation-blind-bell-randomness":
        "2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.hrefs: list[str] = []
        self.script_text: list[str] = []
        self._script: list[str] | None = None
        self._script_attrs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "meta":
            self.metas.append(data)
        elif tag == "link":
            self.links.append(data)
        elif tag == "script":
            self.scripts.append(data)
            self._script = []
            self._script_attrs = data
        if tag in {"a", "object"}:
            target = data.get("href") or data.get("data")
            if target:
                self.hrefs.append(target)

    def handle_data(self, data: str) -> None:
        if self._script is not None:
            self._script.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script is not None:
            self.script_text.append("".join(self._script))
            self._script = None
            self._script_attrs = {}


def parse(path: Path) -> tuple[PageParser, str]:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return parser, text


def meta_value(parser: PageParser, key: str, value: str) -> str | None:
    for meta in parser.metas:
        if meta.get(key) == value:
            return meta.get("content")
    return None


def local_target(page: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith("#"):
        return None
    raw = parsed.path
    if not raw:
        return None
    target = (page.parent / raw).resolve()
    if raw.endswith("/"):
        target /= "index.html"
    return target


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    parser, text = parse(CANONICAL)

    required_meta = {
        "citation_title": "Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell Inequalities",
        "citation_author": "Alec Kriebel",
        "citation_publication_date": "2026-08-09",
        "citation_pdf_url": CANONICAL_URL + "paper.pdf",
        "version": "1.1.0",
    }
    for name, expected in required_meta.items():
        require(meta_value(parser, "name", name) == expected,
                f"canonical metadata {name!r} mismatch", failures)
    require("citation_doi" not in text.lower(), "canonical page contains citation_doi", failures)
    require(not re.search(r'"(?:doi|identifier)"\s*:', text, re.I),
            "JSON-LD contains a DOI/identifier field", failures)
    canonical_links = [link.get("href") for link in parser.links
                       if link.get("rel") == "canonical"]
    require(canonical_links == [CANONICAL_URL], "canonical link mismatch", failures)
    require(meta_value(parser, "property", "og:url") == CANONICAL_URL,
            "OpenGraph URL mismatch", failures)
    require("mathjax@3" in text.lower(), "MathJax v3 script missing", failures)
    require("unrefereed" in text.lower() and "ai-assisted" in text.lower(),
            "status/AI disclosure missing", failures)
    require("has not been submitted" in text.lower(), "non-submission status missing", failures)
    require("source-author review" in text.lower(), "source-author packet link missing", failures)
    require("equal supported" in text.lower(), "support-rigidity scope missing", failures)
    require("conjecture 2" in text.lower(), "precise source-claim boundary missing", failures)
    require("5-\\log_2 3" in text, "four-outcome entropy statement missing", failures)

    json_blocks: list[dict[str, object]] = []
    for attrs, script in zip(parser.scripts, parser.script_text):
        if attrs.get("type") == "application/ld+json":
            try:
                json_blocks.append(json.loads(script))
            except json.JSONDecodeError as error:
                failures.append(f"invalid JSON-LD: {error}")
    require(len(json_blocks) == 1, "expected exactly one JSON-LD block", failures)
    if json_blocks:
        data = json_blocks[0]
        require(data.get("@type") == "ScholarlyArticle", "JSON-LD type mismatch", failures)
        require(data.get("url") == CANONICAL_URL, "JSON-LD URL mismatch", failures)
        require(data.get("version") == "1.1.0", "JSON-LD version mismatch", failures)
        require(data.get("datePublished") == "2026-08-09",
                "JSON-LD publication date mismatch", failures)
        require(data.get("dateModified") == "2026-08-09",
                "JSON-LD modification date mismatch", failures)

    for slug, expected_hash in OLD.items():
        page = DOCS / "papers" / slug / "index.html"
        old_parser, old_text = parse(page)
        require(meta_value(old_parser, "name", "robots") == "noindex,follow",
                f"{slug}: robots metadata mismatch", failures)
        links = [link.get("href") for link in old_parser.links
                 if link.get("rel") == "canonical"]
        require(links == [CANONICAL_URL], f"{slug}: canonical mismatch", failures)
        refresh = meta_value(old_parser, "http-equiv", "refresh")
        require(bool(refresh and CANONICAL_URL in refresh),
                f"{slug}: meta refresh missing/mismatch", failures)
        require(f'location.replace("{CANONICAL_URL}")' in old_text,
                f"{slug}: JavaScript fallback mismatch", failures)
        require("../cyclic-bell-exact-values-and-randomness/" in old_parser.hrefs,
                f"{slug}: ordinary canonical link missing", failures)
        require("./paper.pdf" in old_parser.hrefs,
                f"{slug}: historical PDF link missing", failures)
        require("/tree/" in old_text and expected_hash in old_text,
                f"{slug}: immutable source/hash record missing", failures)
        pdf = page.with_name("paper.pdf")
        require(sha256(pdf) == expected_hash, f"{slug}: historical PDF hash changed", failures)
        require(CANONICAL_URL not in str(pdf), f"{slug}: impossible redirect loop", failures)

    expected_new = CANONICAL.parent / "paper.pdf"
    expected_summary = CANONICAL.parent / "two-page-summary.pdf"
    require(expected_new.is_file() and expected_new.stat().st_size > 0,
            "canonical paper.pdf missing/empty", failures)
    require(expected_summary.is_file() and expected_summary.stat().st_size > 0,
            "two-page-summary.pdf missing/empty", failures)
    source_paper = ROOT / "cyclic_bell_exact_values_and_randomness/output/pdf/cyclic_bell_exact_values_and_randomness.pdf"
    source_summary = ROOT / "cyclic_bell_exact_values_and_randomness/review_packet/two_page_summary.pdf"
    require(sha256(expected_new) == sha256(source_paper),
            "deployed canonical PDF differs from package PDF", failures)
    require(sha256(expected_summary) == sha256(source_summary),
            "deployed two-page summary differs from reviewer-packet PDF", failures)

    relevant_pages = [CANONICAL, DOCS / "index.html"] + [
        DOCS / "papers" / slug / "index.html" for slug in OLD
    ]
    for page in relevant_pages:
        page_parser, _ = parse(page)
        for href in page_parser.hrefs:
            target = local_target(page, href)
            if target is not None and not target.exists():
                failures.append(f"broken local link from {page.relative_to(ROOT)}: {href}")

    home = (DOCS / "index.html").read_text(encoding="utf-8")
    require("Sixteen provisional artifacts" in home, "homepage count not sixteen", failures)
    require("Version 1.1.0" in home, "homepage cyclic-paper version not updated", failures)
    require(home.count("cyclic-bell-exact-values-and-randomness/") == 2,
            "homepage should link canonical cyclic paper page and PDF exactly once each", failures)
    for slug in OLD:
        require(f'./papers/{slug}/' not in home,
                f"homepage still links historical route {slug}", failures)

    sitemap_path = DOCS / "sitemap.xml"
    try:
        tree = ET.parse(sitemap_path)
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text or "" for node in tree.findall(".//s:loc", namespace)]
        require(urls.count(CANONICAL_URL) == 1, "canonical route missing/duplicated in sitemap", failures)
        for slug in OLD:
            old_url = f"https://aleckriebel.github.io/Math/papers/{slug}/"
            require(old_url not in urls, f"historical redirect remains in sitemap: {slug}", failures)
    except ET.ParseError as error:
        failures.append(f"sitemap XML parse failed: {error}")

    if failures:
        print("FAIL: cyclic-Bell website validation")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PASS: canonical metadata, JSON-LD, MathJax, and disclosure")
    print("PASS: three redirect stubs and no redirect loop")
    print("PASS: three historical PDF hashes unchanged")
    print("PASS: canonical PDF and two-page summary present and byte-identical to package outputs")
    print("PASS: relevant local links, homepage consolidation, and sitemap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
