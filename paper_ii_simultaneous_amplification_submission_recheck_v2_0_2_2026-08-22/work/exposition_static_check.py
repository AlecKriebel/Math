#!/usr/bin/env python3
"""Independent static cross-reference and citation check for the frozen TeX."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX = (
    ROOT
    / "delivered_copy/source_and_certificates/universal_simultaneous_amplification"
    / "phase4_landmark_closure/paper_hybrid_threshold/main.tex"
)

text = TEX.read_text(encoding="utf-8")


def keys(pattern: str) -> list[str]:
    return re.findall(pattern, text)


labels = keys(r"\\label\{([^}]+)\}")
refs = keys(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}")
bibitems = keys(r"\\bibitem(?:\[[^]]*\])?\{([^}]+)\}")
cite_groups = keys(r"\\cite(?:t|p|alp|author|year|yearpar)?(?:\[[^]]*\])?(?:\[[^]]*\])?\{([^}]+)\}")
cites = [key.strip() for group in cite_groups for key in group.split(",")]


def duplicates(items: list[str]) -> list[str]:
    counts = collections.Counter(items)
    return sorted(item for item, count in counts.items() if count > 1)


print(f"TeX: {TEX}")
print(f"labels={len(labels)} refs={len(refs)} bibitems={len(bibitems)} cites={len(cites)}")
print(f"duplicate labels: {duplicates(labels)}")
print(f"undefined references: {sorted(set(refs) - set(labels))}")
print(f"unused labels: {sorted(set(labels) - set(refs))}")
print(f"duplicate bibitems: {duplicates(bibitems)}")
print(f"undefined citations: {sorted(set(cites) - set(bibitems))}")
print(f"uncited bibitems: {sorted(set(bibitems) - set(cites))}")

if duplicates(labels) or set(refs) - set(labels) or duplicates(bibitems) or set(cites) - set(bibitems):
    raise SystemExit(1)
