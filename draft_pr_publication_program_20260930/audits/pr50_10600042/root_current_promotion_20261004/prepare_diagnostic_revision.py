"""Prepare v3 without overwriting the exact reviewed v2 payload."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil

A = Path(__file__).resolve().parent.parent
old, new = A / "publication_package_v2", A / "publication_package_v3"
assert not new.exists()
pins = {"even_strand_markov.tex": "d6f663f6efc3295b546f0e061bd2d8b918082bcf932f501c774ebebfe4822493",
        "even_strand_markov.pdf": "2afa0517148f0b44f3cab081e3c2ca64c9e73699498c81770e2addf147961d57",
        "even-strand-markov-verification-v2.zip": "b5da353b660ed0f261e7fe617e6ff347ee0561c8269d5a67606f0d3699e97481",
        "zenodo-deposit.json": "6cd1cecbd1779f20fcf48dbf998993c7159058c47a8a2ec97332cbeba0b91945"}
for name, digest in pins.items():
    assert hashlib.sha256((old / name).read_bytes()).hexdigest() == digest
members = ("LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS", "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py", "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py")
new.mkdir()
for name in members:
    shutil.copyfile(old / name, new / name)
checker = (old / "verify_even_calculus.py").read_text()
assert checker.count('"""Independent definition of an unrestricted Markov edge."""') == 1
checker = checker.replace('"""Independent definition of an unrestricted Markov edge."""', '"""Separately prescribed unrestricted edge; shares elementary helpers."""')
anchor = "def main():\n    rng = random.Random(10600042)"
assert checker.count(anchor) == 1
controls = '''def source_bound_left_controls():
    """Literal Kamada/Kauffman-Lambropoulou left formulas, not shared shift construction.
    Nonempty blocks catch a common-mode error in both endpoint generators.
    These small tests are diagnostics, not a proof of the imported theorem.
    """
    before = CHECKS
    a = b = (("s", 1, 1),)
    literal_left = (
        State(4, (("s", 2, 1), ("s", 1, -1), ("s", 2, 1), ("s", 1, 1))),
        State(4, (("s", 2, 1), ("v", 1, 1), ("s", 2, 1), ("v", 1, 1))),
    )
    literal_buffered = (
        State(4, (("s", 2, 1), ("s", 1, -1), ("s", 2, 1), ("s", 1, 1), ("s", 3, 1))),
        State(4, (("s", 2, 1), ("v", 1, 1), ("s", 2, 1), ("v", 1, 1), ("s", 3, 1))),
    )
    require(unrestricted("left_exchange", 4, a, b, ()) == literal_left,
            "primary literal unrestricted left index shift")
    require(even_scheme("L", 4, a, b) == literal_left,
            "primary literal even left index shift")
    require(tuple(map(pad, unrestricted("left_exchange", 3, a, b, ()))) == literal_buffered,
            "primary literal odd left exchange and retained padding tail")
    require(even_scheme("BL", 4, a, b) == literal_buffered,
            "primary literal buffered left index shift and unshifted tail")
    require(all(len(components(x)) == 2 and ordered_crossings(x) == ((0, 0), (0, 0))
                for x in literal_left), "literal L closure necessary-invariant control")
    require(all(len(components(x)) == 1 and ordered_crossings(x) == ((0,),)
                for x in literal_buffered), "literal BL closure necessary-invariant control")
    wrong_left = (
        State(4, (("s", 1, 1), ("s", 1, -1), ("s", 1, 1), ("s", 1, 1))),
        State(4, (("s", 1, 1), ("v", 1, 1), ("s", 1, 1), ("v", 1, 1))),
    )
    wrong_buffered = tuple(State(4, x.word + (("s", 3, 1),)) for x in wrong_left)
    require(all(len(components(x)) == 4 for x in wrong_left) and
            all(len(components(x)) == 3 for x in wrong_buffered) and
            not relabels(*map(ordered_crossings, wrong_left)) and
            not relabels(*map(ordered_crossings, wrong_buffered)),
            "zero-shift false L/BL pair distinguished despite equal component counts")
    require(shift((("s", 2, -1), ("v", 1, 1), ("s", 1, 1))) ==
            (("s", 3, -1), ("v", 2, 1), ("s", 2, 1)),
            "source-defined shift retains virtual type and classical signs")
    return {"checks": CHECKS - before, "literal_nonempty_L_BL_endpoints": True,
            "zero_shift_false_pairs_distinguished": True,
            "signs_and_virtual_type_preserved": True,
            "limits": "Source-bound diagnostics, not independent proof or an equivalence oracle"}


def main():
    source_controls = source_bound_left_controls()
    rng = random.Random(10600042)'''
checker = checker.replace(anchor, controls)
out = '"relation_context_cases":relations,"scheme_coverage":dict(sorted(COVER.items())),'
assert checker.count(out) == 1
checker = checker.replace(out, '"relation_context_cases":relations,"source_bound_left_controls":source_controls,"scheme_coverage":dict(sorted(COVER.items())),')
(new / "verify_even_calculus.py").write_text(checker)

tex = (old / "even_strand_markov.tex").read_text()
anchor_t = "historical priority for our formulation.\n"
assert tex.count(anchor_t) == 1
tex = tex.replace(anchor_t, anchor_t + r"""We have identified fuller related texts~\cite{Nencka98,Nencka99}, whose bodies
have not yet been accessed; the bearing of those texts on exact
ordinary-closure priority remains unresolved.
""")
anchor_d = "universal proof; they are not a link-equivalence oracle"
assert tex.count(anchor_d) == 1
tex = tex.replace(anchor_d, "universal proof. Literal nonempty left-exchange endpoints transcribed from the\nprimary formulas check the index shift and separate padding tail without using\nthe shared shift helper to construct expected endpoints. Zero-shift\ncountercontrols are separated by ordered crossing matrices despite equal\ncomponent counts. These diagnostics are not a link-equivalence oracle")
anchor_b = r"\bibitem{Fiedler}"
assert tex.count(anchor_b) == 1
tex = tex.replace(anchor_b, r"""\bibitem{Nencka98} H.~Nencka, \emph{Cantorian braid groups},
Methods Funct. Anal. Topology \textbf{4} (1998), no.~2, 66--75.
\href{https://mfat.imath.kiev.ua/article/?id=71}{Publisher record; MR1770817}.
\bibitem{Nencka99} H.~Nencka, \emph{On some extensions of Artin's braid relations},
Contemporary Mathematics \textbf{233} (1999), 221--233.
\href{https://doi.org/10.1090/conm/233/03432}{doi:10.1090/conm/233/03432}.
""" + anchor_b)
(new / "even_strand_markov.tex").write_text(tex)
readme = (old / "README.md").read_text().replace("even-strand-markov-verification-v2.zip", "even-strand-markov-verification-v3.zip")
readme += "\nThe strengthened diagnostics include primary-source literal nonempty L/BL endpoint controls. Their expected words do not use the shared shifting helper. A zero-shift mutant gives false left-exchange pairs with differing ordered crossing matrices even though component counts agree. These controls address a real common-mode weakness in the earlier diagnostics; they do not replace the universal proof. Fuller Nencka1998/1999 text remains unaccessed, and exact historical ordinary-closure priority remains unresolved.\n"
(new / "README.md").write_text(readme)
q = (old / "SOURCE_QUALIFICATIONS.md").read_text()
q += "\n## Authenticated fuller texts and remaining priority hold\n\nHanna Nencka, *Cantorian braid groups*, Methods Funct. Anal. Topology **4** (1998), no. 2, **66–75**, MR1770817, is authenticated by its [official publisher record](https://mfat.imath.kiev.ua/article/?id=71); the full-text section says Coming Soon. *On some extensions of Artin’s braid relations*, Contemporary Mathematics **233** (1999), **221–233**, DOI [10.1090/conm/233/03432](https://doi.org/10.1090/conm/233/03432), is authenticated by publisher contents and deposited metadata; the official chapter link requires institutional access. Neither full body has been read. Their relationship to the two-page1996 announcement and bearing on ordinary-closure completeness remain unresolved. No absence, invalidity, difference of a proved model, or novelty inference follows from unavailable text. Fair credit does not resolve the global priority gate.\n\nThe strengthened checker independently fixes expected nonempty L/BL words from the cited primary formulas rather than generating both sides through a shared shift helper. Zero-shift countercontrols are distinguished by ordered crossing matrices. These are source-bound diagnostics, not an independent proof, and the universal proof and imported-theorem boundary are unchanged.\n"
(new / "SOURCE_QUALIFICATIONS.md").write_text(q)
builder = (old / "build_verification_zip.py").read_text().replace("even-strand-markov-verification-v2.zip", "even-strand-markov-verification-v3.zip")
(new / "build_verification_zip.py").write_text(builder)
manifest = json.loads((old / "zenodo-deposit.json").read_text())
assert manifest["metadata"]["description"].count("finite checks supplement the universal proof.") == 1
manifest["files"][1] = {"path": "even-strand-markov-verification-v3.zip", "name": "even-strand-markov-verification-v3.zip"}
manifest["metadata"]["description"] = manifest["metadata"]["description"].replace("finite checks supplement the universal proof.", "finite checks supplement the universal proof. Source-bound literal nonempty left-exchange controls separately verify the index shift and retained buffer. Fuller related Nencka1998/1999 texts have been identified but not accessed, so their bearing on exact ordinary-closure priority remains unresolved.")
(new / "zenodo-deposit.json").write_text(json.dumps(manifest, indent=2) + "\n")
now = dt.datetime.now(dt.timezone.utc).isoformat()
report = {"UTC": now, "status": "V3_DIAGNOSTIC_AND_SOURCE_REVISION_DRAFT_ACTUAL_RUN_PENDING",
          "frozen_v2_pins": pins, "universal_proof_and_schemes_unchanged": True,
          "new_central_proof_attempts": 0, "original_budget": "1/5", "publication_approval": False,
          "priority_pending": True, "revision_preparation_percent": 50, "PR50_workflow_percent": 0}
(new / "REVISION_PREPARATION.json").write_text(json.dumps(report, indent=2) + "\n")
(new / "RESEARCH_LOG.md").write_text("# PR50 diagnostic strengthening revision\n\n## " + now + " — prospective v3 prepared\n\nMathematical estimate95%; diagnostic repair preparation50%; exact priority resolution60%; publication workflow0%. Preserve the exact reviewed v2 and its source-controlled common-mode mutation finding. Add literal primary-grounded nonempty L/BL endpoints, unshifted buffer and necessary-invariant false-shift controls; rename the shared-helper unrestricted constructor's misleading independence description. Credit authenticated fuller Nencka sources while leaving the exact priority gate unresolved. No new central proof attempt. Genuine new checker run/result/provenance, checksums, archive, compilation/PDF, visual review and a NEW adversary are still required.\n")
for name, digest in pins.items():
    assert hashlib.sha256((old / name).read_bytes()).hexdigest() == digest
print(json.dumps(report, indent=2))
