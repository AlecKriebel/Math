#!/usr/bin/env python3
"""Apply mechanical LaTeX-rendering fixes to generated proof fragments.

The authenticated Markdown inputs remain untouched.  These transformations
only normalize legacy display syntax that Pandoc preserves literally.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


TAG_BEFORE_INNER_END = re.compile(
    r"(?m)^(?P<body>[^\n]*?)\s+\\tag\{(?P<tag>[^}]+)\}\s*\n"
    r"(?P<indent>[ \t]*)(?P<end>\\end\{(?:split|aligned|gathered)\})"
)
BARE_BRACKET_DISPLAY = re.compile(
    r"(?m)^\{\[\}\s*\n(?P<body>.*?)\n(?P<end>\\end\{(?:split|aligned|gathered)\})"
    r"(?P<tag>\\tag\{[^}]+\})?\s*$",
    re.DOTALL,
)
LONG_TEXTTT = re.compile(r"\\texttt\{(?P<body>[^{}\n]{40,})\}")
LONG_ESCAPED_IDENTIFIER = re.compile(
    r"(?<![A-Za-z0-9\\{])"
    r"(?P<body>[A-Za-z0-9.]+(?:\\_[A-Za-z0-9.]+){3,})"
)
AUTO_LABEL = re.compile(r"\\label\{[^{}]+\}")


def normalize(text: str) -> str:
    # One legacy theorem wrote visible set-closing braces without the LaTeX
    # escape.  Repair the rendered fragment, while retaining the frozen source.
    for members in ("0,A", "0,2A", "A,2A", "0,A,2A"):
        text = text.replace(rf"\{{{members}}}", rf"\{{{members}\}}")

    # amsmath permits a display tag on the outer display, not inside its
    # split/aligned child.  Move a terminal tag one syntactic level outward.
    text = TAG_BEFORE_INNER_END.sub(
        lambda match: (
            f"{match.group('body').rstrip()}\n"
            f"{match.group('indent')}{match.group('end')}"
            f"\\tag{{{match.group('tag')}}}"
        ),
        text,
    )
    # A few legacy sources use a bare opening `\[` that Pandoc escaped as
    # literal `{[}` while leaving the inner amsmath environment raw.
    text = BARE_BRACKET_DISPLAY.sub(
        lambda match: (
            "\\[\n"
            f"{match.group('body')}\n"
            f"{match.group('end')}{match.group('tag') or ''}\n"
            "\\]"
        ),
        text,
    )
    # Make long inline identifiers and hashes breakable without changing
    # their printed characters, and use a line-breaking listing environment
    # for fenced literal blocks.
    text = LONG_TEXTTT.sub(
        lambda match: rf"\texttt{{\seqsplit{{{match.group('body')}}}}}",
        text,
    )
    text = LONG_ESCAPED_IDENTIFIER.sub(
        lambda match: rf"\texttt{{\seqsplit{{{match.group('body')}}}}}",
        text,
    )
    # Forty independently authored notes reuse automatic Pandoc heading
    # labels such as ``proof``. None contains a label reference, so strip
    # those generated labels when assembling the single publication volume.
    text = AUTO_LABEL.sub("", text)
    text = text.replace(
        r"{\def\LTcaptype{none}", r"{\small\def\LTcaptype{none}"
    )
    return text.replace(r"\begin{verbatim}", r"\begin{CodeBlock}").replace(
        r"\end{verbatim}", r"\end{CodeBlock}"
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: postprocess_supplement.py FRAGMENT.tex")
    path = Path(sys.argv[1])
    original = path.read_text(encoding="utf-8")
    path.write_text(normalize(original), encoding="utf-8")


if __name__ == "__main__":
    main()
