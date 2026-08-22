#!/usr/bin/env python3
"""Check release PDFs for page-count, extraction, and semantic regressions."""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class Document:
    relative_path: str
    pages: int
    semantic_text: bool = False


FULL_DOCUMENTS = (
    Document("manuscript/main.pdf", 18, True),
    Document("manuscript/supplement.pdf", 18, True),
    Document("external_audit/theorem_summary.pdf", 3, True),
    Document("external_audit/proof_skeleton.pdf", 6, True),
    Document("figures/network_family.pdf", 1),
    Document("figures/stable_tradeoff.pdf", 1),
    Document("figures/stable_profiles.pdf", 1),
    Document("figures/amplitude_scaling.pdf", 1),
)

PUBLIC_DOCUMENTS = tuple(
    document
    for document in FULL_DOCUMENTS
    if not document.relative_path.startswith("external_audit/")
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

    supplement = extracted.get("manuscript/supplement.pdf", "")
    if supplement:
        for section, title_prefix in enumerate(SUPPLEMENT_SECTION_PREFIXES, start=1):
            pattern = rf"(?:^|\s)S{section}\.?\s*{re.escape(title_prefix)}"
            if not re.search(pattern, supplement):
                failures.append(f"supplement lacks rendered S{section} section numbering")

    main_text = extracted.get("manuscript/main.pdf", "")
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
        if not re.search(r"D\s*=\s*diag\s*\(d1,.*?dZ\)\s*[≻>]\s*0", main_text, re.I):
            failures.append("main PDF does not quantify the positive diagonal D in the exact diffusion law")
        if not re.search(r"c\s*m\s*\(L\)\s*=\s*N\s*m\s*\(L\)", main_text):
            failures.append("main PDF does not show the scaled cubic quotient")

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
            ("with u the Latin letter", "unambiguous Latin near-threshold parameter"),
            ("The crossing numerator is unchanged", "scaled-family transversality numerator"),
            ("all-dimensional identity", "selected-zero derivative identity"),
            ("generalized eigenvector", "scaled-family algebraic-simplicity closure"),
            ("componentwise strictly positive", "patterned-branch positivity closure"),
            ("uniquely minimized", "within-family contrast-minimum statement"),
        ):
            if phrase.lower() not in supplement.lower():
                failures.append(f"supplement PDF lacks {label}")

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
    parser.add_argument("--profile", choices=("full", "public"), default="full")
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
    documents = FULL_DOCUMENTS if args.profile == "full" else PUBLIC_DOCUMENTS
    audit(root, output_dir.resolve(), documents)


if __name__ == "__main__":
    main()
