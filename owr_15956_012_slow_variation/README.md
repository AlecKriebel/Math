# The odd-part ratio under slow variation

A short note on the printed Hilberdink problem, OWR-15956-012.

**Verified mathematical result.** For every nonzero nonnegative multiplicative f, if F(2x)/F(x) tends to 1, then the ratio of the odd-part sum to F(x) tends to the reciprocal of sum f(2^k), interpreted as zero if the sum diverges. The proof answers the catalogue's exact existence question.

**Scope matters.** The original report prints a conflicting weighted constant. The note disproves that prediction under the printed hypothesis, and does not settle the possible intended index-one regular-variation question. No exact earlier resolution was found in a bounded priority audit; originality is not certified.

- [Paper PDF](output/paper.pdf) and [LaTeX source](manuscript/paper.tex)
- [Verification report](audit/VERIFICATION_REPORT.md)
- [Independent proof audit](audit/adversarial-proof.md) and [independent derivation](audit/independent-derivation.md)
- [Source fidelity](audit/source-match.md) and [priority audit with search log](audit/priority-independent.md)
- [Zenodo upload kit](zenodo/zenodo-upload-kit.zip) and [copy-and-paste instructions](zenodo/UPLOAD.md)
- [Public paper site](https://aleckriebel.github.io/Math/papers/odd-part-slow-variation/)

## Verify in seconds

From this folder, run `python3 verification/verify.py` (Python 3.9+, standard library only). The script checks exact finite identities, inequalities, and examples. The universal limit is proved in the paper, not certified by finite testing. No proof assistant is used.

To rebuild the PDF, use `tectonic manuscript/paper.tex --outdir output` (or another LaTeX engine with the listed packages). To rebuild the archives and publication mirror after checks, run `python3 build_package.py`. It updates only this effort's directory and its dedicated `docs/papers/odd-part-slow-variation/` mirror. The PDF build is mathematically reproducible; PDF binary identity can vary by TeX version and build date. Archives are deterministic for fixed input bytes.

## Attribution

Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Version 1.0.0, 23 September 2026 UTC. Unrefereed preprint. Candidate supplied from prior AI-assisted work; OpenAI Codex assisted with preparation and separate AI audits. No external person was contacted. Text is CC BY 4.0; code is MIT; see [LICENSES.md](LICENSES.md).

The upload kit is prepared for manual deposit. No Zenodo deposit, DOI, or GitHub release is created by the build.
