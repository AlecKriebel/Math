"""Prepare a new credited-prior-work draft; confers no promotion approval."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil

A = Path(__file__).resolve().parent.parent
old = A / "publication_package_v1"
new = A / "publication_package_v2"
assert not new.exists(), "Preserve any existing revision"
fixed = {
    "even_strand_markov.tex": "cd141a55da2241764d4fbbe8a145d8d4be29370803e24704e645c60cf8f2d0dc",
    "even_strand_markov.pdf": "ea3e6f6b647de0acd71219a2840ee515fe6548f7d4dbba828558b7fb0e01624e",
    "even-strand-markov-verification-v1.zip": "2b519b4ba59ccd2e5ed9c88a79aa96d273481b45bb18b6a1ecc6fcbd0381a48d",
    "zenodo-deposit.json": "4636f8b65dc2906097967a3fa963b0ae0fc652d645e2a5bcf17558c6f7493b82",
}
for name, digest in fixed.items():
    assert hashlib.sha256((old / name).read_bytes()).hexdigest() == digest, name
members = (
    "LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS",
    "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py",
    "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py",
)
checksums = dict(row.split("  ", 1)[::-1] for row in (old / "SHA256SUMS").read_text().splitlines())
assert set(checksums) == set(members) - {"SHA256SUMS"}
for name, digest in checksums.items():
    assert hashlib.sha256((old / name).read_bytes()).hexdigest() == digest
new.mkdir()
for name in members:
    shutil.copyfile(old / name, new / name)

tex = (old / "even_strand_markov.tex").read_text()
anchor = "The block restrictions have mathematical content."
assert tex.count(anchor) == 1
addition = r"""An earlier related announcement is Nencka's two-page contribution
\cite{Nencka}. After introducing a new representation by interwoved strings,
it states a ``Markov generalized equivalence'' theorem using conjugacy at
$2^n$ strands and signed stabilization tails from $2^n$ to $2^{n+1}$.
For $n\ge1$ these are even counts; each such tail is a composite of double
stabilizations by grouping its $2^n$ crossings into successive pairs.
Thus a proved ordinary-closure interpretation of that announcement would be
materially relevant to the classical question. The contribution does not
define its generalized equivalence or supply a proof sufficient to verify
that interpretation, and its convention for possible one-strand participation
is not specified. We neither certify an earlier ordinary-closure resolution
nor refute its announced result. The current proof uses the explicitly stated
ordinary-closure inputs above and includes (BC) and (T); the announcement
supplies no virtual exchange calculus. This distinction does not establish
historical priority for our formulation.

"""
tex = tex.replace(anchor, addition + anchor)
bib = r"\bibitem{Fiedler}"
assert tex.count(bib) == 1
entry = r"""\bibitem{Nencka} H.~Nencka,
\emph{Generalization of the Markov theorem and Cantorian-like braid groups},
in \emph{Topology and Applications: International Topological Conference
dedicated to P.~S.~Alexandroff's 100th Birthday, Moscow, May 27--31, 1996},
PHASIS, Moscow (1996), 147--148.
\href{https://ru.djvu.online/file/OzKCMNnU4ojPn}{ISBN 5-7036-0017-0; scanned contribution}.
"""
tex = tex.replace(bib, entry + bib)
(new / "even_strand_markov.tex").write_text(tex)

qualification = (old / "SOURCE_QUALIFICATIONS.md").read_text()
old_line = "- Fiedler, *Markov moves cannot be replaced by double Markov moves*,"
assert qualification.count(old_line) == 1
qualification = qualification.replace(old_line,
    "- Hanna Nencka, *Generalization of the Markov theorem and Cantorian-like braid groups*, in *Topology and Applications: International Topological Conference dedicated to P. S. Alexandroff's 100th Birthday, Moscow, May 27–31, 1996*, Moscow: PHASIS (1996), **147–148**, ISBN **5-7036-0017-0**. Both actual printed pages and the copyright/ISBN leaf were inspected in a [public scan of the authored contribution](https://ru.djvu.online/file/OzKCMNnU4ojPn); volume metadata was independently checked in the [institutional library catalog](https://plus-legacy.cobiss.net/cobiss/si/sl/bib/7463513). This authenticates an older related announcement; it is not a certification of the announced theorem. No third-party scan is redistributed.\n" + old_line)
anchor_q = "A bounded primary-source priority review did not verify an exact earlier answer to this formulation."
assert qualification.count(anchor_q) == 1
new_q = """Nencka's contribution first defines ordinary Markov equivalence by same-link closure, then introduces a new interwoved-string representation and states a theorem about **Markov generalized equivalence** at power-of-two braid counts. Its stabilization tail has printed **± signs**, which are lost in the indexed OCR; a positive-only interpretation is incorrect. The generalized relation and representation are not sufficiently defined in those two pages, and no proof of the generalized theorems is supplied there. The convention concerning a possible one-strand level is also unspecified. For n >= 1, the long signed tail from 2^n to 2^(n+1) groups into 2^(n-1) ordinary double stabilizations. Power-of-two counts would still be relevant to an even-strand classical formulation if a valid ordinary-closure equivalence were established; they cannot be dismissed merely because they form a subset of even counts. The announcement supplies no virtual exchange calculus.

We do not certify that announcement as an exact earlier ordinary-closure resolution, and do not claim to refute it by Fiedler's partially accessed result. Its existence must be credited even though the source alone leaves that interpretation unverified. Our explicitly defined calculus and proof import ordinary classical and virtual closure theorems and include the extra BC and T schemes.

A bounded primary-source priority review did not verify an exact earlier valid answer to the full classical-and-virtual formulation; Nencka's older related announcement is an explicit qualification to that finding."""
qualification = qualification.replace(anchor_q, new_q)
(new / "SOURCE_QUALIFICATIONS.md").write_text(qualification)

readme = (old / "README.md").read_text().replace("even-strand-markov-verification-v1.zip", "even-strand-markov-verification-v2.zip")
anchor_r = "AI tools were used extensively"
assert readme.count(anchor_r) == 1
readme = readme.replace(anchor_r,
    "The prior-work discussion explicitly acknowledges Nencka's related 1996 power-of-two braid announcement. Its generalized equivalence and ordinary-closure interpretation are not certified from the two-page source. This note makes no first-priority claim.\n\n" + anchor_r)
(new / "README.md").write_text(readme)
builder = (old / "build_verification_zip.py").read_text()
assert builder.count("even-strand-markov-verification-v1.zip") == 1
(new / "build_verification_zip.py").write_text(builder.replace("even-strand-markov-verification-v1.zip", "even-strand-markov-verification-v2.zip"))

record = json.loads((old / "VERIFICATION_RECORD.json").read_text())
previous = record["manuscript_provenance"]
source_bytes = (new / "even_strand_markov.tex").read_bytes()
record["manuscript_provenance"] = {
    "historical_v1_provenance": previous,
    "submission_tex_binding": {"bytes": len(source_bytes), "sha256": hashlib.sha256(source_bytes).hexdigest()},
    "change": "Credit and carefully qualify Nencka's related 1996 announcement; synchronize source qualifications and support filenames. Mathematical scheme statements, universal proof, diagnostic code and genuine historical execution are unchanged.",
    "source_change_is_not_new_computation": True,
}
(new / "VERIFICATION_RECORD.json").write_text(json.dumps(record, indent=2) + "\n")
manifest = json.loads((old / "zenodo-deposit.json").read_text())
description = manifest["metadata"]["description"]
anchor_d = "The accompanying compact verification package"
assert description.count(anchor_d) == 1
description = description.replace(anchor_d,
    "It explicitly credits Nencka's related 1996 power-of-two braid announcement; its generalized equivalence and ordinary-closure interpretation are not certified from the two-page source, and historical priority is not asserted. " + anchor_d)
manifest["metadata"]["description"] = description
assert manifest["files"][1] == {"path": "even-strand-markov-verification-v1.zip", "name": "even-strand-markov-verification-v1.zip"}
manifest["files"][1] = {"path": "even-strand-markov-verification-v2.zip", "name": "even-strand-markov-verification-v2.zip"}
(new / "zenodo-deposit.json").write_text(json.dumps(manifest, indent=2) + "\n")
(new / "SHA256SUMS").write_text("".join(hashlib.sha256((new / name).read_bytes()).hexdigest() + "  " + name + "\n" for name in members if name != "SHA256SUMS"))
for name, digest in fixed.items():
    assert hashlib.sha256((old / name).read_bytes()).hexdigest() == digest
for name in ("verify_even_calculus.py", "expected_results.json", "LICENSE-TEXT.md", "LICENSE-CODE.txt"):
    assert (old / name).read_bytes() == (new / name).read_bytes()
report = {"status": "PRIORITY_QUALIFIED_REVISION_AUTHORED_NOT_APPROVED", "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
          "frozen_v1_four_pins_unchanged": fixed, "unchanged_mathematical_schemes_proof_code": True,
          "v2_source": record["manuscript_provenance"]["submission_tex_binding"], "new_central_proof_attempts": 0,
          "compile_pdf_archive_review_priority_decision_publication_pending": True,
          "mathematical_confidence_estimate_percent": 95, "priority_resolution_estimate_percent": 60,
          "publication_workflow_percent": 0, "whole_goal_complete": False}
(new / "REVISION_PREPARATION.json").write_text(json.dumps(report, indent=2) + "\n")
(new / "RESEARCH_LOG.md").write_text("# PR50 named-prior-work revision\n\n## " + report["timestamp_utc"] + " — new draft prepared\n\nMathematical verification estimate 95%; priority resolution 60%; manuscript revision preparation 60%; publication workflow 0%. Preserve the frozen v1 package and its genuine historical diagnostics. Name and qualify the newly authenticated Nencka 1996 announcement across source, bibliography, README, source qualifications, verification provenance and intended metadata. No mathematical scheme or proof change and no new central attempt. This draft confers no priority, publication or merge approval. Fuller-source audit, built-in compilation, exported PDF visual verification, ZIP build and a new independent whole-package adversary remain pending.\n")
print(json.dumps(report, indent=2))
