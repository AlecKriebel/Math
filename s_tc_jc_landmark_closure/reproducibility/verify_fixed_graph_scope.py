#!/usr/bin/env python3
"""Regression guard against the rejected unrestricted cleanup-rooting fibre."""

from __future__ import annotations

from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent


def retained_edges_after_one_step(
    arcs: tuple[tuple[str, str], ...], root: str, reticulations: set[str]
) -> list[tuple[str, str, tuple[str, ...]]]:
    children = [v for u, v in arcs if u == root]
    if len(children) != 2:
        raise AssertionError("binary root must have exactly two children")
    result: list[tuple[str, str, tuple[str, ...]]] = []
    for u, v in arcs:
        if u == root:
            continue
        a, b = sorted((u, v))
        result.append((a, b, (v,) if v in reticulations else ()))
    a, b = sorted(children)
    heads = tuple(sorted(v for v in children if v in reticulations))
    result.append((a, b, heads))
    return sorted(result)


def assert_hidden_zipper_is_not_a_fixed_graph_rooting() -> None:
    one = (
        ("r", "P"),
        ("r", "Q"),
        ("P", "Q"),
        ("P", "L1"),
        ("Q", "L2"),
    )
    two = (
        ("r", "P"),
        ("r", "Q"),
        ("P", "Q"),
        ("P", "p"),
        ("Q", "q"),
        ("p", "q"),
        ("p", "L1"),
        ("q", "t"),
        ("t", "L2"),
        ("t", "L3"),
    )
    for name, arcs, retics in (
        ("single_zipper", one, {"Q"}),
        ("double_zipper", two, {"Q", "q"}),
    ):
        edges = retained_edges_after_one_step(arcs, "r", retics)
        endpoint_counts = Counter((u, v) for u, v, _ in edges)
        if max(endpoint_counts.values()) < 2:
            raise AssertionError(f"{name} unexpectedly became already-simple")
        # The active convention stops here and rejects the presentation.  It
        # must never iterate cleanup to call this a rooting of the final tree.


def assert_active_text_uses_fixed_graph_scope() -> None:
    forbidden = (
        "Outcome" + " Q",
        "Root" + "_clean",
        "S_TC" + "(clean)",
        "canonical cleanup" + " quotient",
        "rooting-fibre" + " quotient",
        "root zipper" + " quotient",
        "e634" + "0199",
        "abb83" + "eff",
        "Convention_Closed" + "_Level2_JC_Theorem",
    )
    roots = [PROJECT]
    if (PROJECT / "biorxiv_submission").exists():
        roots.append(PROJECT / "biorxiv_submission")
    suffixes = {".md", ".tex", ".json", ".py", ".sh", ".cff", ".txt"}
    this_file = Path(__file__).resolve()
    failures: list[str] = []
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file() or path.resolve() == this_file:
                continue
            if "history" in path.parts or path.suffix.lower() not in suffixes:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                if token.casefold() in text.casefold():
                    failures.append(f"{path.relative_to(REPO)} contains {token!r}")
    if failures:
        raise AssertionError("rejected cleanup-fibre language is active:\n" + "\n".join(failures))

    manuscript = (PROJECT / "source/paper/main.tex").read_text(encoding="utf-8")
    normalized = " ".join(manuscript.split())
    required = (
        "single suppression produces a simple binary mixed graph",
        "No later degree-two or parallel cleanup is part of",
        "image is exactly that graph",
    )
    missing = [phrase for phrase in required if phrase not in normalized]
    if missing:
        raise AssertionError(f"fixed-graph convention language missing: {missing}")


def main() -> None:
    assert_hidden_zipper_is_not_a_fixed_graph_rooting()
    assert_active_text_uses_fixed_graph_scope()
    print("VERIFIED: fixed already-simple rooting scope; hidden zippers rejected")


if __name__ == "__main__":
    main()
