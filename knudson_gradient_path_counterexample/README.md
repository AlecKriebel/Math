# A four-vertex counterexample to Knudson's persistence-gradient conjecture

**Alec Kriebel** · [ORCID](https://orcid.org/0009-0001-9320-500X) · Version 1.0.1 · 2026-09-23

The candidate is a complete counterexample to **Conjecture 2, p. 1629**, in
Kevin P. Knudson's *Persistent homology and discrete Morse theory*, Oberwolfach
Report 29/2008 ([original report](https://doi.org/10.4171/OWR/2008/29)).
It uses a triangulated interval with filtration `a,b,c,d,cd,bd,ac`:

```text
P   = {(d,cd), (c,bd), (b,ac)}
V_P = {(d,cd)}
reachable from ac = {ac,a,c}; hence zero paths to b.
```

This refutes the conjecture in its stated fixed matching, including existence
of a path. It is compatible with paths appearing after earlier cancellations.
No minimality or resolution of other conjectures is claimed.

- [Paper (3 pages)](paper/paper.pdf) and [LaTeX source](paper/paper.tex)
- [Public paper page](https://aleckriebel.github.io/Math/papers/knudson-gradient-path/)
- [Verification report](audit/verification_report.md)
- [Fresh preprint review: final clean pass](audit/preprint_round2.md) and [corrections](audit/preprint_changes.md)
- [Independent mathematical audit](audit/adversarial_math.md)
- [Priority audit and 39-query search record](audit/priority_independent.md)
- [Zenodo copy-and-paste metadata](zenodo/UPLOAD.md)
- [Research log](research_log.md)

## Verify in seconds

Python 3.9 or later; no external packages:

```sh
python3 verification/verify.py
python3 verification/independent_check.py
```

The first program checks boundary reduction, union-find, the matching,
acyclicity and exhaustive paths. The second reconstructs the barcode from
ranks of H0 inclusion maps and checks signed boundaries and path reversal.
Both also work with `python3 -O`. See [verification instructions](verification/README.md).
The original supplied files are preserved unchanged in `inputs/`.

## Rebuild

```sh
tectonic --outdir paper paper/paper.tex
python3 build_package.py
```

Tectonic needs its TeX packages available or network access on first use.
The package command uses only the standard library and the existing PDF;
it creates a deterministic source/verification archive and a manual Zenodo
upload kit. It does not submit anything to Zenodo. To also refresh the existing
repository's project page, run `python3 build_package.py --site` from this folder.

## Scope and provenance

The proof and two exact implementations passed independent AI adversarial
checks. A bounded public-literature audit found no earlier explicit refutation;
this is not a guarantee of historical priority. In particular, related work is
listed as in preparation, and the full 2015 Knudson book and 2011 Bauer thesis
were unavailable. The user associates this conjecture with OWR-2040-002 /
30000990; the catalogue itself returned HTTP 429 and its current status was
not independently verified. The paper is grounded in the original report.

The candidate came from prior AI-assisted work supplied by the author. OpenAI
Codex prepared this publication and verification package, with separate AI
agents for mathematical and priority audits. This is an unrefereed preprint,
not a proof-assistant formalization. No person was contacted. No GitHub release,
Zenodo deposit, or DOI is created by this package.

Text and manuscript: CC BY 4.0. Code: MIT. See [LICENSE.md](LICENSE.md).
