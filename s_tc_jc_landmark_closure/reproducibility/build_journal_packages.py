#!/usr/bin/env python3
"""Build deterministic Systematic Biology and JMB submission packages.

The canonical article and supplement remain ``source/paper/main.tex`` and
``source/supplement/supplement.tex``.  This script creates journal-specific
review copies without changing the mathematical text:

* Systematic Biology: 12 point, one-and-a-half spacing, continuous line
  numbers, running heads, ragged-right text, and figure alt text.
* Journal of Mathematical Biology: the canonical article grouped under one
  ``Statements and Declarations`` heading, plus editable LaTeX sources.

All ZIP timestamps and TeX build timestamps are fixed for reproducibility.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
SOURCE = PROJECT / "source"
SB = PROJECT / "journal_submission/systematic_biology"
JMB = PROJECT / "journal_submission/journal_of_mathematical_biology"
SOURCE_DATE_EPOCH = "1786838400"  # 2026-08-16 00:00:00 UTC
ZIP_TIME = (2026, 8, 16, 0, 0, 0)

ALT_TEXT = {
    "bridge_projective.tex": (
        "Three colored component ellipses form a path.  Two bridge scales "
        "connect their projective tensors, and a displayed formula gives the "
        "incidence-scaling action on local tensors and bridge multipliers."
    ),
    "core_atlas.tex": (
        "Five directed network skeletons are shown from left to right: one "
        "cycle and four theta orientations.  Tree vertices are blue, "
        "reticulations are red double circles, and arrows enter reticulations."
    ),
    "fixed_mixed_convention.tex": (
        "A rooted three-leaf network maps to a fixed simple mixed graph after "
        "one root deletion.  Only arrows entering the red reticulation remain "
        "directed in the mixed graph."
    ),
    "leaf_substitution.tex": (
        "A single labelled leaf attached to a port tensor is replaced by a "
        "two-leaf cherry with positive edge multipliers u and v."
    ),
    "omega_pair.tex": (
        "Two triangle-free four-leaf theta graphs share the same arrowhead "
        "pattern but have different labelled pendant attachments."
    ),
    "theta_pair.tex": (
        "Two four-leaf theta networks have identical internal graphs but swap "
        "the leaf labels attached at vertices B and E."
    ),
    "triangle_redirection.tex": (
        "Three copies of one labelled triangle place the reticulation in turn "
        "at vertices A, B, and C while preserving all three external arms."
    ),
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tectonic() -> str:
    candidate = shutil.which("tectonic") or "/opt/homebrew/bin/tectonic"
    if not Path(candidate).is_file():
        raise RuntimeError("Tectonic is required to build journal packages")
    return candidate


def compile_tex(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    with tempfile.TemporaryDirectory(prefix="stc-jc-journal-pdf-") as name:
        outdir = Path(name)
        subprocess.run(
            [tectonic(), "-X", "compile", str(source), "--outdir", str(outdir),
             "--keep-logs"],
            cwd=source.parent,
            env=env,
            check=True,
        )
        log = outdir / f"{source.stem}.log"
        log_text = log.read_text(encoding="utf-8", errors="replace")
        for fatal in ("Overfull \\hbox", "Undefined control sequence"):
            if fatal in log_text:
                raise RuntimeError(f"{fatal} in {source}")
        shutil.copyfile(outdir / f"{source.stem}.pdf", output)


def copy_paper_tree(destination: Path) -> None:
    shutil.copytree(SOURCE / "paper", destination / "paper")
    shutil.copytree(SOURCE / "supplement", destination / "supplement")
    (destination / "BUILD.md").write_text(
        "# Deterministic LaTeX build\n\n"
        "Requirements: Tectonic 0.15 or later with its standard cached bundle.\n\n"
        "From this extracted source directory:\n\n"
        "```bash\n"
        "cd paper\ntectonic main.tex\ncd ../supplement\ntectonic supplement.tex\n"
        "```\n",
        encoding="utf-8",
    )


def inject_alt_text(figure: Path, description: str) -> None:
    content = figure.read_text(encoding="utf-8")
    marker = "\\label{fig:"
    if marker not in content:
        raise AssertionError(f"figure label missing in {figure}")
    addition = (
        "\\par\\smallskip\\noindent\\textit{Alt text:} "
        + description
        + "\n"
    )
    figure.write_text(content.replace(marker, addition + marker, 1), encoding="utf-8")


def make_sb_variant(root: Path) -> Path:
    copy_paper_tree(root)
    paper = root / "paper/main.tex"
    content = paper.read_text(encoding="utf-8")
    content = content.replace(
        "\\documentclass[11pt]{article}",
        "\\documentclass[12pt]{article}",
        1,
    )
    package_marker = "\\usepackage[nameinlink,noabbrev]{cleveref}\n"
    journal_packages = r"""\usepackage{setspace}
\usepackage[switch]{lineno}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Kriebel}
\fancyhead[R]{SHARP LEVEL-2 JC IDENTIFIABILITY BOUNDARY}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt}
"""
    if package_marker not in content:
        raise AssertionError("cleveref package marker missing")
    content = content.replace(package_marker, package_marker + journal_packages, 1)
    content = content.replace("\\setlist{nosep}", "\\setlist{itemsep=.2em}", 1)
    content = content.replace(
        "\\setlength{\\parskip}{0.35em}\n\\setlength{\\parindent}{0pt}",
        "\\setlength{\\parskip}{0pt}\n\\setlength{\\parindent}{0.5in}",
        1,
    )
    content = content.replace(
        "\\begin{document}\n",
        "\\begin{document}\n\\onehalfspacing\n\\raggedright\n\\linenumbers\n",
        1,
    )
    long_omega_coordinates = r"""\[
(u_0,u_1,u_2,u_3,u_4,u_5,p_0,p_1,p_2)
=(a_0,a_1,a_2,a_3,a_4,a_7,a_8,a_9,a_{10}),
\quad g=u_4+2u_5,\quad h=u_0u_5+2u_4.
\]"""
    broken_omega_coordinates = r"""\[
\begin{aligned}
(u_0,u_1,u_2,u_3,u_4,u_5,p_0,p_1,p_2)
  &=(a_0,a_1,a_2,a_3,a_4,a_7,a_8,a_9,a_{10}),\\
g&=u_4+2u_5,\qquad h=u_0u_5+2u_4.
\end{aligned}
\]"""
    if long_omega_coordinates not in content:
        raise AssertionError("Omega coordinate display marker missing")
    content = content.replace(long_omega_coordinates, broken_omega_coordinates, 1)
    paper.write_text(content, encoding="utf-8")
    for name, description in ALT_TEXT.items():
        inject_alt_text(root / "paper/figures" / name, description)
    return paper


def make_jmb_variant(root: Path) -> Path:
    copy_paper_tree(root)
    paper = root / "paper/main.tex"
    content = paper.read_text(encoding="utf-8")
    replacements = (
        (
            "\\section*{Data and code availability}",
            "\\section*{Statements and Declarations}\n\n"
            "\\subsection*{Data and code availability}",
        ),
        ("\\section*{Author contributions}", "\\subsection*{Author contributions}"),
        ("\\section*{Funding}", "\\subsection*{Funding}"),
        ("\\section*{Competing interests}", "\\subsection*{Competing interests}"),
        ("\\section*{Use of generative AI}", "\\subsection*{Use of generative AI}"),
    )
    for old, new in replacements:
        if old not in content:
            raise AssertionError(f"JMB declaration marker missing: {old}")
        content = content.replace(old, new, 1)
    support_marker = "Our three principal statements are as follows."
    support_sentence = (
        "Further exact parameter data and the theorem-to-certificate map are "
        "provided in Online Resource~1.\n\n"
    )
    if support_marker not in content:
        raise AssertionError("JMB Online Resource insertion marker missing")
    content = content.replace(support_marker, support_sentence + support_marker, 1)
    paper.write_text(content, encoding="utf-8")
    supplement = root / "supplement/supplement.tex"
    supplement_text = supplement.read_text(encoding="utf-8")
    supplement_text = supplement_text.replace(
        "\\title{Supplement to\\\\\n",
        "\\title{Supplementary Information (Online Resource 1)\\\\\n"
        "for\\\\\n",
        1,
    )
    supplement_text = supplement_text.replace(
        "\\author{Alec Kriebel\\\\\\small Independent Researcher}",
        "\\author{Alec Kriebel\\\\\\small Independent Researcher\\\\"
        "\\small Corresponding author: \\texttt{me@aleckriebel.com}\\\\"
        "\\small Intended journal: Journal of Mathematical Biology}",
        1,
    )
    if (
        "Online Resource 1" not in supplement_text
        or "Journal of Mathematical Biology" not in supplement_text
    ):
        raise AssertionError("JMB supplement identification transformation failed")
    supplement.write_text(supplement_text, encoding="utf-8")
    return paper


def deterministic_zip(root: Path, output: Path, prefix: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix in {
                ".aux", ".bbl", ".blg", ".log", ".out", ".pdf"
            }:
                continue
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{relative}", ZIP_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), zipfile.ZIP_DEFLATED, 9)


def write_sums(directory: Path, names: list[str]) -> None:
    lines = [f"{digest(directory / name)}  {name}" for name in names]
    (directory / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_systematic_biology() -> None:
    SB.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="stc-jc-sb-") as name:
        variant = Path(name) / "SB_LaTeX_Source"
        article = make_sb_variant(variant)
        compile_tex(article, SB / "SB_Main_Manuscript.pdf")
        deterministic_zip(variant, SB / "SB_LaTeX_Source.zip", "SB_LaTeX_Source")
    shutil.copyfile(
        PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf",
        SB / "SB_Supplementary_Material.pdf",
    )
    compile_tex(SB / "SB_Cover_Letter.tex", SB / "SB_Cover_Letter.pdf")
    write_sums(SB, [
        "SB_Main_Manuscript.pdf",
        "SB_Supplementary_Material.pdf",
        "SB_LaTeX_Source.zip",
        "SB_Cover_Letter.tex",
        "SB_Cover_Letter.pdf",
        "SB_SUBMISSION_METADATA.md",
        "SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    ])


def build_jmb() -> None:
    JMB.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="stc-jc-jmb-") as name:
        variant = Path(name) / "JMB_LaTeX_Source"
        article = make_jmb_variant(variant)
        compile_tex(article, JMB / "JMB_Main_Manuscript.pdf")
        compile_tex(
            variant / "supplement/supplement.tex",
            JMB / "JMB_Supplementary_Information.pdf",
        )
        deterministic_zip(variant, JMB / "JMB_LaTeX_Source.zip", "JMB_LaTeX_Source")
    compile_tex(JMB / "JMB_Cover_Letter.tex", JMB / "JMB_Cover_Letter.pdf")
    write_sums(JMB, [
        "JMB_Main_Manuscript.pdf",
        "JMB_Supplementary_Information.pdf",
        "JMB_LaTeX_Source.zip",
        "JMB_Cover_Letter.tex",
        "JMB_Cover_Letter.pdf",
        "JMB_SUBMISSION_METADATA.md",
        "JMB_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    ])


def main() -> None:
    build_systematic_biology()
    build_jmb()
    print("BUILT: Systematic Biology and Journal of Mathematical Biology packages")


if __name__ == "__main__":
    main()
