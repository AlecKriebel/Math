#!/usr/bin/env python3
"""Check release PDFs for page-count, extraction, and semantic regressions."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class Document:
    relative_path: str
    pages: int
    semantic_text: bool = False
    producer: str | None = None


FULL_DOCUMENTS = (
    Document("manuscript/main.pdf", 19, True, "pdfTeX-1.40.24"),
    Document("manuscript/supplement.pdf", 19, True, "pdfTeX-1.40.24"),
    Document("external_audit/theorem_summary.pdf", 3, True, "pdfTeX-1.40.24"),
    Document("external_audit/proof_skeleton.pdf", 6, True, "pdfTeX-1.40.24"),
    Document("figures/network_family.pdf", 1, False, "pdfTeX-1.40.24"),
    Document("figures/stable_tradeoff.pdf", 1),
    Document("figures/stable_profiles.pdf", 1),
    Document("figures/amplitude_scaling.pdf", 1),
)

# The portable replay builds the two standalone audit exports before invoking
# this profile, so their rendered hypotheses belong to the portable PDF gate.
PUBLIC_DOCUMENTS = FULL_DOCUMENTS

JOURNAL_DOCUMENTS = (
    Document("submission/journal/manuscript.pdf", 24, True, "pdfTeX-1.40.24"),
    Document("submission/journal/supplement.pdf", 24, True, "pdfTeX-1.40.24"),
    Document("submission/journal/cover_letter_SIADS.pdf", 1, True, "pdfTeX-1.40.24"),
)

FORBIDDEN_PHRASES = (
    "Theorem 3.1",
    "Theorems 4.1 and 5.1",
    "The shaded principal species set",
    "The marked point is",
    "python verify_symbolic_certificates.py",
    "universal trade-off",
    "universal minimax lower bound",
    "globally optimal",
    "universal necessary bound",
    "universal cost",
    "biological cost",
    "price paid in concentrations",
    "All listed coefficients are nonnegative",
    "a conservation-compatible Lyapunov–Schmidt reduction has",
    "Lyapunov–Schmidt coefficients",
    "The dashed outline marks the principal species set",
    "explicit two-parameter Jacobian image",
    "topology-wide over-realizations theorem",
    "physical fixed-mass vector becomes",
    "reduces max(χD, χH)",
    "reduces the larger of the two contrasts",
    "two surviving cycle covers",
    "two feed-forward chain fragments, followed by",
    "or equivalently the exact infimum of",
    "Author confirmation required",
    "No funding information supplied",
)

FORBIDDEN_PATTERNS = (
    ("mislabeled P_C coefficient row", r"polynomial whose sign gives\s*S\s*m\s*<\s*0"),
    ("old transformed-left-vector notation", r"\bq\s*m\s*\(L\)\s*="),
    ("false stoichiometric-minor determinant", r"absolute determinant\s+2\s*m\s*[−-]\s*2"),
    ("old scaled-state notation", r"\bz\s*=\s*H\s*m\s*\(L\)\s*x"),
    ("near-threshold dimension-variable typo", r"\bν\s*=\s*1\s*\+\s*\(2\s*[−-]\s*t\)\s*ε"),
    ("near-threshold damping-parameter collision", r"\bu\s*=\s*1\s*\+\s*\(2\s*[−-]\s*t\)\s*ε"),
    ("threshold omits flux parameters", r"\bs\s*[∗*]\s*\(\s*H\s*,\s*D\s*\)"),
    ("X_m components used as full vectors", r"ℓ\s*T\s*m\s*r\s*m"),
)

SUPPLEMENT_SECTION_PREFIXES = (
    "Reaction matrices",
    "All-spectrum",
    "The principal-minor",
    "Order-",
    "Improved unit-equilibrium",
    "Conservation-compatible",
    "Equilibrium-scaled",
    "Exact coefficient",
    "Near-threshold",
    "Semilinear",
    "Numerical protocol",
)


def normalize(text: str) -> str:
    ligatures = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
    }
    for glyph, expansion in ligatures.items():
        text = text.replace(glyph, expansion)
    return " ".join(text.split())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def embedded_fonts(reader: PdfReader) -> tuple[int, list[str]]:
    """Return the number of distinct page fonts and any unembedded names."""

    fonts: dict[tuple[str, str], bool] = {}
    font_file_keys = ("/FontFile", "/FontFile2", "/FontFile3")
    for page in reader.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        font_dictionary = resources.get_object().get("/Font")
        if font_dictionary is None:
            continue
        for font_reference in font_dictionary.get_object().values():
            font = font_reference.get_object()
            identity = (str(font.get("/BaseFont", "unnamed")), str(font.get("/Subtype")))
            if identity in fonts:
                continue
            is_embedded = font.get("/Subtype") == "/Type3"
            descriptor = font.get("/FontDescriptor")
            if descriptor is not None:
                descriptor = descriptor.get_object()
                is_embedded = is_embedded or any(
                    descriptor.get(key) is not None for key in font_file_keys
                )
            descendants = font.get("/DescendantFonts")
            if descendants is not None:
                is_embedded = True
                for descendant_reference in descendants:
                    descendant = descendant_reference.get_object()
                    descendant_descriptor = descendant.get("/FontDescriptor")
                    if descendant_descriptor is None or not any(
                        descendant_descriptor.get_object().get(key) is not None
                        for key in font_file_keys
                    ):
                        is_embedded = False
            fonts[identity] = is_embedded
    missing = sorted(name for (name, _subtype), present in fonts.items() if not present)
    return len(fonts), missing


def audit_modulus_table_spacing(root: Path, pdf_path: Path) -> tuple[int, float]:
    """Check every generated modulus-table row using Poppler word boxes."""

    generated = root / "data" / "certificate_tables.tex"
    if not generated.is_file():
        raise AssertionError("missing generated modulus-certificate table")
    generated_text = generated.read_text(encoding="utf-8")
    if r"\frac{" in generated_text:
        raise AssertionError("modulus-certificate table uses stacked fractions")
    if re.search(r"\d+/\d+[AU](?:\^\{\d+\})?", generated_text):
        raise AssertionError(
            "modulus-certificate table has an ambiguous slash fraction adjacent to a parameter"
        )

    with tempfile.TemporaryDirectory(prefix="modulus-table-bbox-") as directory:
        bbox_path = Path(directory) / "supplement.xhtml"
        result = subprocess.run(
            ["pdftotext", "-bbox-layout", str(pdf_path), str(bbox_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        raw = bbox_path.read_text(encoding="utf-8", errors="replace")

    page_pattern = re.compile(
        r'<page\s+width="(?P<width>[^"]+)"\s+height="(?P<height>[^"]+)">(?P<body>.*?)</page>',
        re.S,
    )
    word_pattern = re.compile(
        r'<word\s+xMin="(?P<x0>[^"]+)"\s+yMin="(?P<y0>[^"]+)"\s+'
        r'xMax="(?P<x1>[^"]+)"\s+yMax="(?P<y1>[^"]+)">(?P<text>.*?)</word>',
        re.S,
    )
    line_pattern = re.compile(r'<line\s+[^>]*yMin="(?P<y0>[^"]+)"[^>]*>(?P<body>.*?)</line>', re.S)

    pages: list[dict[str, object]] = []
    for page_index, page_match in enumerate(page_pattern.finditer(raw)):
        words = []
        for word_match in word_pattern.finditer(page_match.group("body")):
            words.append(
                (
                    float(word_match.group("x0")),
                    float(word_match.group("y0")),
                    float(word_match.group("x1")),
                    float(word_match.group("y1")),
                    html.unescape(re.sub(r"<[^>]+>", "", word_match.group("text"))).strip(),
                )
            )
        lines = []
        for line_match in line_pattern.finditer(page_match.group("body")):
            texts = [
                html.unescape(re.sub(r"<[^>]+>", "", match.group("text"))).strip()
                for match in word_pattern.finditer(line_match.group("body"))
            ]
            lines.append((float(line_match.group("y0")), " ".join(filter(None, texts))))
        pages.append(
            {
                "index": page_index,
                "width": float(page_match.group("width")),
                "height": float(page_match.group("height")),
                "words": words,
                "lines": lines,
            }
        )

    positions = [
        (page["index"], y0, text)
        for page in pages
        for y0, text in page["lines"]
    ]
    starts = [
        (page_index, y0)
        for page_index, y0, text in positions
        if "35-term homogeneous certificate" in text
    ]
    ends = [
        (page_index, y0)
        for page_index, y0, text in positions
        if "Signed scalar and rational-function certificates" in text
    ]
    if not starts:
        raise AssertionError("could not isolate the four rendered modulus tables")
    start = max(starts)
    later_ends = [position for position in ends if position > start]
    if not later_ends:
        raise AssertionError("could not isolate the four rendered modulus tables")
    end = min(later_ends)

    headers = []
    for page in pages:
        page_index = page["index"]
        for coefficient_word in page["words"]:
            if coefficient_word[4] != "coefficient":
                continue
            y0 = coefficient_word[1]
            position = (page_index, y0)
            if not (start <= position < end):
                continue
            arity = sum(
                word[4] == "deg" and abs(word[1] - y0) < 0.2
                for word in page["words"]
            )
            if arity not in (2, 3):
                continue
            headers.append(
                {
                    "page": page_index,
                    "y": y0,
                    "arity": arity,
                    "boundary": coefficient_word[0] - 2.0,
                }
            )
    if not headers:
        raise AssertionError("no modulus-table headers found in rendered supplement")

    row_count = 0
    minimum_gap = float("inf")
    for header_index, header in enumerate(headers):
        page = pages[header["page"]]
        next_y = float(page["height"]) - 35.0
        if header_index + 1 < len(headers) and headers[header_index + 1]["page"] == header["page"]:
            next_y = headers[header_index + 1]["y"] - 4.0
        numeric_by_y: dict[float, list[tuple[float, float, float, float, str]]] = {}
        for word in page["words"]:
            if not (header["y"] + 5.0 < word[1] < next_y):
                continue
            if word[0] >= header["boundary"] or not re.fullmatch(r"\d+", word[4]):
                continue
            numeric_by_y.setdefault(round(word[1], 1), []).append(word)
        baselines = sorted(
            y for y, words in numeric_by_y.items() if len(words) == header["arity"]
        )
        row_count += len(baselines)
        if not baselines:
            continue

        coefficient_words = [
            word
            for word in page["words"]
            if header["y"] + 5.0 < word[1] < next_y
            and word[0] >= header["boundary"]
            and word[4] != "coefficient"
        ]
        row_boxes: list[list[tuple[float, float, float, float, str]]] = [
            [] for _ in baselines
        ]
        for word in coefficient_words:
            nearest = min(range(len(baselines)), key=lambda index: abs(word[1] - baselines[index]))
            if abs(word[1] - baselines[nearest]) <= 7.0:
                row_boxes[nearest].append(word)
        if any(not boxes for boxes in row_boxes):
            raise AssertionError("a rendered modulus-table row has no coefficient ink")
        for boxes in row_boxes:
            if min(word[0] for word in boxes) < 40.0 or max(word[2] for word in boxes) > page["width"] - 40.0:
                raise AssertionError("rendered modulus-table coefficient crosses the text bounds")
        for current, following in zip(row_boxes, row_boxes[1:]):
            current_x0 = min(word[0] for word in current)
            current_x1 = max(word[2] for word in current)
            following_x0 = min(word[0] for word in following)
            following_x1 = max(word[2] for word in following)
            if min(current_x1, following_x1) <= max(current_x0, following_x0):
                continue
            gap = min(word[1] for word in following) - max(word[3] for word in current)
            minimum_gap = min(minimum_gap, gap)
            if gap < 1.0:
                raise AssertionError(
                    f"modulus-table coefficient rows overlap or nearly touch: {gap:.3f} pt"
                )

    if row_count != 35 + 77 + 22 + 84:
        raise AssertionError(f"expected 218 rendered modulus-table rows, found {row_count}")
    if minimum_gap == float("inf"):
        raise AssertionError("could not measure adjacent modulus-table row clearance")
    return row_count, minimum_gap


def audit(root: Path, output_dir: Path, documents: tuple[Document, ...]) -> None:
    failures: list[str] = []
    output_dir.mkdir(parents=True, exist_ok=True)
    report_names = [
        document.relative_path.replace("/", "_").replace(".", "_") + ".txt"
        for document in documents
    ]
    for report_name in (*report_names, "SUMMARY.txt"):
        (output_dir / report_name).unlink(missing_ok=True)

    extracted: dict[str, str] = {}
    for document in documents:
        path = root / document.relative_path
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty PDF: {document.relative_path}")
            continue
        try:
            reader = PdfReader(path)
            if reader.is_encrypted:
                failures.append(f"encrypted PDF: {document.relative_path}")
                continue
            pages = len(reader.pages)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            font_count, missing_fonts = embedded_fonts(reader)
            producer = str((reader.metadata or {}).get("/Producer", ""))
        except Exception as error:  # pypdf errors have several version-specific types.
            failures.append(f"unreadable PDF {document.relative_path}: {error}")
            continue

        if pages != document.pages:
            failures.append(
                f"page-count regression for {document.relative_path}: "
                f"expected {document.pages}, found {pages}"
            )
        if document.semantic_text and not text.strip():
            failures.append(f"no extractable text in {document.relative_path}")
        if document.producer is not None and producer != document.producer:
            failures.append(
                f"producer regression for {document.relative_path}: "
                f"expected {document.producer!r}, found {producer!r}"
            )
        if missing_fonts:
            failures.append(
                f"unembedded fonts in {document.relative_path}: {', '.join(missing_fonts)}"
            )
        extracted[document.relative_path] = normalize(text)

        report_name = document.relative_path.replace("/", "_").replace(".", "_") + ".txt"
        report = (
            f"PDF: {document.relative_path}\n"
            f"SHA-256: {sha256(path)}\n"
            f"Pages: {pages}\n"
            f"Producer: {producer}\n"
            "Encrypted: False\n"
            f"Extracted characters: {len(text)}\n"
            f"Distinct page fonts: {font_count}\n"
            "All page fonts embedded: True\n"
        )
        (output_dir / report_name).write_text(report, encoding="utf-8")

    semantic_corpus = " ".join(
        extracted.get(document.relative_path, "")
        for document in documents
        if document.semantic_text
    )
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in semantic_corpus.lower():
            failures.append(f"forbidden rendered phrase: {phrase!r}")
    for label, pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, semantic_corpus, re.I):
            failures.append(f"forbidden rendered pattern ({label}): {pattern!r}")

    for match in re.finditer(r"rates,\s*equilibrium coordinates", semantic_corpus, re.I):
        context = semantic_corpus[max(0, match.start() - 260) : match.end() + 260]
        if not re.search(
            r"(?:positive-equilibrium|equilibrium[- ]realization)\s+manifold",
            context,
            re.I,
        ):
            failures.append("rendered robustness statement leaves rate/equilibrium perturbations unqualified")

    export_sections = (
        (
            "external_audit/theorem_summary.pdf",
            r"Principal-minor\s+diffusion-ray\s+theorem",
            r"Exact\s+network\s+diffusion\s+law",
            False,
        ),
        (
            "external_audit/proof_skeleton.pdf",
            r"Principal-minor\s+diffusion-ray\s+theorem\s+and\s+exact\s+network\s+law",
            r"For\s*A\s*m\s*\(\s*a\s*,\s*b\s*\)\s*H",
            True,
        ),
    )
    for export_path, start_pattern, end_pattern, require_singular_j in export_sections:
        export_text = extracted.get(export_path, "")
        if not export_text:
            continue
        section_match = re.search(
            start_pattern + r"(.*?)" + end_pattern,
            export_text,
            re.I,
        )
        if section_match is None:
            failures.append(f"{export_path} lacks an isolatable generic diffusion-ray statement")
            continue
        generic_section = section_match.group(1)
        if not re.search(
            r"D\s*=\s*diag\s*\(\s*d\s*1\s*,.*?d\s*n\s*\).*?d\s*j\s*>\s*0",
            generic_section,
            re.I,
        ):
            failures.append(f"{export_path} omits positive diagonal D in the generic theorem")
        if require_singular_j and not re.search(r"det\s*J\s*=\s*0", generic_section):
            failures.append("proof skeleton factors out s without a rendered det J=0 hypothesis")

    supplement = extracted.get("manuscript/supplement.pdf", "") or extracted.get(
        "submission/journal/supplement.pdf", ""
    )
    for supplement_path in (
        "manuscript/supplement.pdf",
        "submission/journal/supplement.pdf",
    ):
        if supplement_path in extracted:
            rendered_supplement = extracted[supplement_path]
            if re.search(r"\d+\s*/\s*\d+\s*[AU](?:\s*\^\s*\d+)?", rendered_supplement):
                failures.append(
                    f"{supplement_path} renders an ambiguous slash fraction adjacent to a parameter"
                )
            if len(re.findall(r"\d+\s*A\s*/\s*\d+", rendered_supplement)) != 50:
                failures.append(
                    f"{supplement_path} does not render all 50 rational-A coefficients unambiguously"
                )
            try:
                row_count, minimum_gap = audit_modulus_table_spacing(
                    root, root / supplement_path
                )
                report_name = supplement_path.replace("/", "_").replace(".", "_") + ".txt"
                with (output_dir / report_name).open("a", encoding="utf-8") as handle:
                    handle.write(f"Modulus-certificate rows: {row_count}\n")
                    handle.write(f"Minimum adjacent coefficient clearance: {minimum_gap:.3f} pt\n")
            except (AssertionError, OSError) as error:
                failures.append(f"modulus-table layout in {supplement_path}: {error}")
    if supplement:
        for section, title_prefix in enumerate(SUPPLEMENT_SECTION_PREFIXES, start=1):
            pattern = rf"(?:^|\s)S{section}\.?\s*{re.escape(title_prefix)}"
            if not re.search(pattern, supplement):
                failures.append(f"supplement lacks rendered S{section} section numbering")

    main_text = extracted.get("manuscript/main.pdf", "") or extracted.get(
        "submission/journal/manuscript.pdf", ""
    )
    if main_text:
        if not re.search(r"0\s*<\s*\|I\|\s*<\s*m", main_text):
            failures.append("main theorem does not visibly exclude the empty principal set")
        for phrase, label in (
            ("one-dimensional center-manifold normal form is", "center-manifold normal-form attribution"),
            ("selected positive realization", "selected-realization scope in Corollary 3.3"),
            ("reduced vector field is odd", "reflection-equivariant odd normal form"),
            ("long-circuit complexes associated with the principal species block", "literal Figure 1 outline description"),
            ("Fredholm of index zero", "stationary Fredholm interface"),
            ("cokernel pairing is", "Crandall–Rabinowitz transversality pairing"),
            ("If a generalized eigenvector", "scaled-family algebraic-simplicity closure"),
            ("Thus all hypotheses of Theorem", "network diffusion-ray hypothesis bridge"),
            ("homogeneous Neumann boundary conditions, consider", "self-contained scaled-family PDE domain"),
            ("physical fixed-mass covector becomes", "fixed-mass covector terminology"),
            ("componentwise strictly positive", "patterned-branch positivity closure"),
            ("uniquely minimized", "within-family contrast-minimum statement"),
            ("fixed interval", "fixed-interval stationary-bifurcation convention"),
            ("finite-wavelength selection", "finite-wavelength scope qualification"),
            ("numerically continue nonlinear patterned branches", "Conradi nonlinear numerical comparison"),
            ("numerically stable segments", "Conradi stable-segment comparison"),
        ):
            if phrase.lower() not in main_text.lower():
                failures.append(f"main PDF lacks {label}")
        order_markers = (
            "3. Determine the constant-optimal stable diffusion–equilibrium frontier",
            "4. Determine the exact threshold for oscillatory diffusion-driven instability",
            "9 Numerical illustrations",
            "Figure 3: Numerical illustrations",
        )
        positions = [main_text.find(marker) for marker in order_markers]
        if any(position < 0 for position in positions):
            failures.append("main PDF lacks one or more Figure 3 placement markers")
        elif positions != sorted(positions):
            failures.append("Figure 3 interrupts the open-problem list or precedes Section 9")
        if not re.search(
            r"\bs\s*[∗*]\s*\(\s*a\s*,\s*b\s*,\s*H\s*,\s*D\s*\)",
            main_text,
        ):
            failures.append("main PDF does not show the flux-dependent threshold notation")
        # PDF extractors differ in whether subscripts are separated by spaces and
        # in how the positive-definite glyph is represented.  Accept either the
        # explicit prose declaration or a rendered comparison, while retaining
        # the complete diagonal endpoints as semantic anchors.
        if not re.search(
            r"(?:"
            r"positive\s+diagonal\s*:\s*D\s*=\s*diag\s*\(\s*d\s*1\s*,.*?d\s*Z\s*\)"
            r"|"
            r"D\s*=\s*diag\s*\(\s*d\s*1\s*,.*?d\s*Z\s*\)\s*[^\w=,;:.]{1,8}\s*0\b"
            r")",
            main_text,
            re.I,
        ):
            failures.append("main PDF does not quantify the positive diagonal D in the exact diffusion law")
        if not re.search(r"c\s*m\s*\(L\)\s*=\s*N\s*m\s*\(L\)", main_text):
            failures.append("main PDF does not show the scaled cubic quotient")

    journal_text = extracted.get("submission/journal/manuscript.pdf", "")
    if journal_text:
        for phrase, label in (
            ("Keywords:", "visible keywords"),
            ("2020 Mathematics Subject Classification:", "visible MSC codes"),
        ):
            if phrase.lower() not in journal_text.lower():
                failures.append(f"journal PDF lacks {label}")
        # pypdf appends right-margin line numbers to the preceding line,
        # whereas pdftotext may place them first.  Require the first two
        # distinct title-line numbers in either extractor ordering.
        if not (
            re.search(r"Turing\s*1\s+Patterns\s*2", journal_text)
            or re.search(r"(?:^|\s)1\s+Exact Diffusion Design", journal_text)
        ):
            failures.append("journal PDF does not visibly begin continuous line numbering")

    cover_text = extracted.get("submission/journal/cover_letter_SIADS.pdf", "")
    if cover_text:
        for phrase in (
            "Dear Editors",
            "Exact Diffusion Design for Maximally Collective Stable Turing Patterns",
            "Alec Kriebel",
            "not under consideration by, and has not been submitted to, another journal",
            "no specific funding",
            "no competing interests",
        ):
            if phrase.lower() not in cover_text.lower():
                failures.append(f"journal cover letter lacks {phrase!r}")

    if supplement:
        if not re.search(
            r"\bu\s*=\s*1\s*\+\s*\(2\s*[−-]\s*ω\)\s*ε",
            supplement,
        ):
            failures.append("supplement PDF lacks the omega-renamed near-threshold path")
        if not re.search(r"c\s*m\s*\(L\)\s*=\s*N\s*m\s*\(L\)", supplement):
            failures.append("supplement PDF does not show the scaled cubic quotient")
        for phrase, label in (
            ("reduced vector field is odd", "reflection-equivariant odd normal form"),
            ("The four boundary values are the unique solution", "printed second-harmonic boundary system"),
            ("affine-chain critical vector", "printed near-threshold affine-vector ansatz"),
            ("The crossing numerator is unchanged", "scaled-family transversality numerator"),
            ("all-dimensional identity", "selected-zero derivative identity"),
            ("generalized eigenvector", "scaled-family algebraic-simplicity closure"),
            ("componentwise strictly positive", "patterned-branch positivity closure"),
            ("uniquely minimized", "within-family contrast-minimum statement"),
            ("All four entries are positive", "exact near-threshold diffusion positivity"),
            ("numerator and denominator polynomials", "near-threshold exact coefficient certificate"),
            ("hence zero is simple", "near-threshold simple-crossing certificate"),
            ("every higher Neumann mode", "near-threshold higher-mode certificate"),
        ):
            if phrase.lower() not in supplement.lower():
                failures.append(f"supplement PDF lacks {label}")
        # pypdf 6.10.0 may join the adjacent roman and math glyphs as
        # ``withu``.  Require every word but tolerate extractor whitespace.
        if not re.search(r"with\s*u\s+the\s+Latin\s+letter", supplement, re.I):
            failures.append("supplement PDF lacks unambiguous Latin near-threshold parameter")

    summary = output_dir / "SUMMARY.txt"
    if failures:
        summary.write_text("PDF_SEMANTIC_AUDIT_FAIL\n" + "\n".join(failures) + "\n")
        raise SystemExit("\n".join(failures))
    summary.write_text("PDF_SEMANTIC_AUDIT_PASS\n", encoding="utf-8")
    print("PDF_SEMANTIC_AUDIT_PASS")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=project_root)
    parser.add_argument("--profile", choices=("full", "public", "journal"), default="full")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir
    if output_dir is None:
        output_dir = (
            root / "release" / "pdf_preflight"
            if args.profile == "full"
            else root / "verification_outputs" / "pdf_preflight"
        )
    documents = {
        "full": FULL_DOCUMENTS,
        "public": PUBLIC_DOCUMENTS,
        "journal": JOURNAL_DOCUMENTS,
    }[args.profile]
    audit(root, output_dir.resolve(), documents)


if __name__ == "__main__":
    main()
