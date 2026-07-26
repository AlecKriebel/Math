#!/usr/bin/env python3
"""Deterministic local checker for the accepted gamma-theta public-site bytes."""

from __future__ import annotations

from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

CONDITIONAL_VERDICT = "ACCEPT_SITE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH"
TAGGED_VERDICT = "ACCEPT_SITE_BYTES_TAG_BOUND"
TAG = "gamma-theta-order12-frontier-v1.0.0"
ROOT = Path(__file__).resolve().parents[3]
EXPECTED = {
    "README.md": "1a66969b4734dd2eaacfba02e5373f08282fc6d6b27bea52103382d43b1835e8",
    "docs/index.html": "6772d7de5014e91437111cfe40897413b8aa8874745093b28ba025c55bfa505b",
    "docs/sitemap.xml": "5bc452cf14985d31d1fbcc50ac71267d29091074420209678651b309eedd9158",
    "docs/research/gamma-theta-conjecture/index.html": "3f2e951e5d7ee69984fb27f2387bf64ecabdb3da2bf405f0d894706b6ff21459",
    "docs/papers/gamma-theta-order-12-frontier/index.html": "a5d54c1f8bc997b81740c1bddb99a46468b2ccd4c696d31aae82a96e2d3a9a09",
    "docs/papers/gamma-theta-order-12-frontier/paper.pdf": "b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2",
    "docs/papers/gamma-theta-order-12-frontier/paper.sha256": "184df74e9e4d5dc3165ef807fde9f1fa35831b2c0aad325397fea1d40c74faeb",
    "docs/papers/cyclic-bell-tsirelson-bound/index.html": "d870c1368678902cb1bdc19e4e6a89456cee4882fe6aafc1f425ab2ed18b6e36",
    "docs/papers/cyclic-bell-tsirelson-bound/paper.pdf": "947b601903de18ea6ffbd8e49ba2bfe261c32342c4d1a71dd96ed9f283ec6c94",
    "gamma_theta_eternal_domination/README.md": "5bb3053bc03b1d0abec557c15856ece982c9b526bfd70a41b59eca881d4501c2",
    "gamma_theta_eternal_domination/RELEASE_NOTES_order12_frontier_v1.0.0.md": "fdb7043d86482aaf5cd05c495c7889b16e04621a9d9a892df3b7f1ec15a77779",
    "gamma_theta_eternal_domination/paper/c035_order12_k3/README.md": "55bfe784f0b9355929f154af573361f44000af33259a69b5a04a72766c7902c4",
    "gamma_theta_eternal_domination/paper/order12_frontier/README.md": "5dd9578ca712c5449a6146544b4002f5aefb73b055cba405f9388b9065394cc0",
}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit(f"FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.refs: list[str] = []
        self.jsonld: list[str] = []
        self._json = False
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(data["id"])
        for key in ("href", "src", "data"):
            if data.get(key):
                self.refs.append(data[key])
        if tag == "script" and data.get("type") == "application/ld+json":
            self._json, self._chunks = True, []

    def handle_data(self, data: str) -> None:
        if self._json:
            self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json:
            self.jsonld.append("".join(self._chunks))
            self._json = False


for relative, expected in EXPECTED.items():
    path = ROOT / relative
    need(path.is_file() and not path.is_symlink(), f"bad file: {relative}")
    need(sha256(path) == expected, f"hash mismatch: {relative}")

paper_dir = ROOT / "docs/papers/gamma-theta-order-12-frontier"
cyclic_dir = ROOT / "docs/papers/cyclic-bell-tsirelson-bound"
research_dir = ROOT / "docs/research/gamma-theta-conjecture"
need({p.name for p in paper_dir.iterdir()} == {"index.html", "paper.pdf", "paper.sha256"},
     "unexpected paper-page package entry")
need({p.name for p in research_dir.iterdir()} == {"index.html"},
     "unexpected research-page package entry")
need({p.name for p in cyclic_dir.iterdir()} == {"index.html", "paper.pdf"},
     "unexpected cyclic-Bell package entry")
need((paper_dir / "paper.sha256").read_text() ==
     EXPECTED["docs/papers/gamma-theta-order-12-frontier/paper.pdf"] + "  paper.pdf\n",
     "paper.sha256 content mismatch")

pages: dict[Path, Page] = {}
for relative in (
    "docs/index.html",
    "docs/research/gamma-theta-conjecture/index.html",
    "docs/papers/gamma-theta-order-12-frontier/index.html",
    "docs/papers/cyclic-bell-tsirelson-bound/index.html",
):
    path = ROOT / relative
    parser = Page()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    need(len(parser.ids) == len(set(parser.ids)), f"duplicate id: {relative}")
    pages[path] = parser
    for document in parser.jsonld:
        value = json.loads(document)
        need(value["author"]["name"] == "Alec Kriebel", f"JSON-LD author: {relative}")
    for ref in parser.refs:
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc or ref.startswith("//"):
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        if target.is_dir():
            target /= "index.html"
        need(target.exists() and not target.is_symlink(), f"broken local reference: {ref}")
        if parsed.fragment and target.suffix == ".html":
            other = Page()
            other.feed(target.read_text(encoding="utf-8"))
            need(parsed.fragment in other.ids, f"broken fragment: {ref}")

xml_root = ET.fromstring((ROOT / "docs/sitemap.xml").read_bytes())
ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
need(xml_root.tag == ns + "urlset", "sitemap namespace/root")
locations = [item.findtext(ns + "loc") for item in xml_root.findall(ns + "url")]
need(len(locations) == 19 and len(locations) == len(set(locations)), "sitemap locations")
for url in (
    "https://aleckriebel.github.io/Math/",
    "https://aleckriebel.github.io/Math/papers/cyclic-bell-tsirelson-bound/",
    "https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/",
    "https://aleckriebel.github.io/Math/papers/gamma-theta-order-12-frontier/",
):
    need(url in locations, f"missing sitemap URL: {url}")

research = (research_dir / "index.html").read_text(encoding="utf-8")
paper = (paper_dir / "index.html").read_text(encoding="utf-8")
home = (ROOT / "docs/index.html").read_text(encoding="utf-8")
root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
sitemap = (ROOT / "docs/sitemap.xml").read_text(encoding="utf-8")
campaign = (ROOT / "gamma_theta_eternal_domination/README.md").read_text(encoding="utf-8")
release = (ROOT / "gamma_theta_eternal_domination/RELEASE_NOTES_order12_frontier_v1.0.0.md").read_text(encoding="utf-8")
c035 = (ROOT / "gamma_theta_eternal_domination/paper/c035_order12_k3/README.md").read_text(encoding="utf-8")
for required in (
    "attacks occur only at unoccupied vertices, and exactly one adjacent guard moves",
    "clique-cover number",
    "It is not the Lovász theta function",
    "C_{11}\\) branch — proved impossible",
    "C_9\\) branch — certified impossible",
    "C_5\\) and \\(C_7\\) branches — still live",
    "Parameters \\(4\\) and \\(5\\) — still live",
    "They are not counterexamples",
):
    need(required in research, f"research scope text missing: {required}")
need("Assume the published exhaustive result" in paper, "paper premise missing")
need("does not resolve the universal conjecture" in paper, "paper universal disclaimer missing")
need("Relative to MacGillivray--Mynhardt--Virgile" in campaign, "C-050 premise missing")
need("C-057 is a certified finite template exclusion, not a complete" in campaign,
     "C-057 boundary missing")
need("The parameter-five lane now has the accepted structural reduction C-056" in campaign,
     "C-056 boundary missing")
need("This is a finite frontier result.  It is not a universal proof" in release,
     "release scope boundary missing")
need("not counterexamples and not a novelty or priority claim" in
     (ROOT / "gamma_theta_eternal_domination/CLAIMS.md").read_text(encoding="utf-8"),
     "C-054 boundary missing")
need("Archival component draft" in c035 and "not a separate current publication" in c035,
     "C-035 archival status missing")
need("Eight provisional artifacts remain current" in home, "integrated paper count missing")
for required in (
    "The exact quantum value of a cyclic Bell operator",
    "./papers/cyclic-bell-tsirelson-bound/",
    "A certified order-twelve extension of the γ–θ frontier",
    "./papers/gamma-theta-order-12-frontier/",
):
    need(required in home, f"integrated homepage card missing: {required}")
need("**The exact quantum value of a cyclic Bell operator**" in root_readme,
     "cyclic-Bell README entry missing")
need("**A Certified Order-Twelve Extension" in root_readme,
     "gamma-theta README entry missing")
need("papers/cyclic-bell-tsirelson-bound/" in sitemap and
     "papers/gamma-theta-order-12-frontier/" in sitemap,
     "integrated sitemap publication URL missing")
for marker in ("<<<<<<<", "=======", ">>>>>>>"):
    need(marker not in root_readme + home + sitemap, f"conflict marker remains: {marker}")
need("og:image" not in research + paper, "unexpected social-card metadata")
for text in (research, paper, campaign, release):
    need("\ufffd" not in text, "replacement character")
    need("Author metadata to be supplied" not in text, "author placeholder")

tag_result = subprocess.run(
    ["git", "show-ref", "--verify", "--quiet", f"refs/tags/{TAG}"], cwd=ROOT
)
need(tag_result.returncode in (0, 1), "cannot determine local tag status")
tag_present = tag_result.returncode == 0
if tag_present:
    for relative, expected in EXPECTED.items():
        data = subprocess.run(
            ["git", "show", f"{TAG}:{relative}"],
            cwd=ROOT, check=True, stdout=subprocess.PIPE,
        ).stdout
        need(hashlib.sha256(data).hexdigest() == expected,
             f"tagged-byte mismatch: {relative}")
    print(TAGGED_VERDICT)
    print("TAG_STATE=BYTE_BOUND")
else:
    print(CONDITIONAL_VERDICT)
    print("TAG_STATE=ATOMIC_PUSH_REQUIRED")
print("PAPER_PAGE_SHA256=" + EXPECTED["docs/papers/gamma-theta-order-12-frontier/index.html"])
print("RESEARCH_PAGE_SHA256=" + EXPECTED["docs/research/gamma-theta-conjecture/index.html"])
