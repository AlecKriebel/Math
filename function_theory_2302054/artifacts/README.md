# Rubel's simultaneous boundedness problem: a known negative answer

**Catalogue:** 2302054 / AMR-022-2054, rank 519.  
**Result:** already solved negatively by Sakari Toppila (1983), Theorem 2.  
**Research date:** 2026-10-03. **Attempts:** 1/5; a complete prior result was found during the first substantive source-and-proof investigation.

## Exact scope

Let \(\mathcal T\) denote the transcendental entire functions on \(\mathbb C\). The question asks whether every closed \(E\subset\mathbb C\) satisfying

\[
(\exists f\in\mathcal T)(\exists M<\infty)\ (\forall z\in E)\ |f(z)|\le M,
\]
\[
(\exists g\in\mathcal T)(\exists m>0)\ (\forall z\in\mathbb C\setminus E)\ |g(z)|\ge m
\]

also admits an \(h\in\mathcal T\) with both properties. The witnesses and constants in the premises may be different. All bounds are uniform on the indicated whole sets. There is no finite-order, normalization, exceptional-set, derivative, or meromorphic-function hypothesis.

## Historical resolution

Toppila's Theorem 2 uses
\[
E=[0,\infty)\ \cup\ \bigcup_{k\ge1}\{z:|z-e^{4k}|\le1\}.
\]
Two separate witnesses exist, but every entire function satisfying both bounds is constant. Thus the requested transcendental simultaneous witness does not exist. The article explicitly identifies the question as Rubel's Problem 2.54 from the 1977 collection.

- Sakari Toppila, [*Solutions of problems of Miller and Rubel*](https://www.acadsci.fi/mathematica/Vol08/vol08pp369-370.pdf), Ann. Acad. Sci. Fenn. Ser. A I Math. **8** (1983), 369–370, Theorem 2 and §3; [DOI](https://doi.org/10.5186/aasfm.1983.0826).
- The [2018 Hayman–Lingham edition](https://arxiv.org/abs/1809.07200), printed p.43, reproduces the question but its Update 2.54 reports no progress. That update is inconsistent with the already published 1983 resolution. No change to the mathematical question is needed.

## Verification

Both pages of Toppila's paper were read, including the proof, and visually checked against the PDF to resolve damaged OCR in exponents and inequalities. [PROOF.md](PROOF.md) supplies an independent detailed verification of the construction, an explicit global lower bound for the infinite product, and a uniform Harnack-chain argument for rigidity. The latter replaces the paper's short Schottky-chain argument; it is an explanatory verification, with no novelty claim.

[verify.py](verify.py) checks the rational and symbolic algebra used in that verification. These finite checks supplement the analytic proof; they do not establish infinite-product convergence or Liouville's theorem by computation. Run `python3 verify.py`; the expected output is in [verification.json](verification.json).

See [SOURCES.md](SOURCES.md) for provenance, scope and literature-search limits. This packet credits the existing theorem and makes no claim of a new solution. AI tools were used extensively; the exposition is unrefereed and should receive qualified independent scrutiny.
