# Problem 30000971: fiber regularity and obstruction length

## Result

**The original two-question target remains unsolved after five substantive approaches.** A complete candidate proof refutes its stronger obstruction-length comparison; the main uniform regularity bound is unresolved. The counterexample must pass fresh independent audit before promotion.

For a general linear projection of the quadratic Veronese embedding of P^40 to P^46, the candidate constructs an entire single-point fiber with algebra k[z_1,z_2,z_3,z_4]/(z_1,z_2,z_3,z_4)^2. It has ideal-sheaf regularity 2 and obstruction length 10. Therefore

    reg(Z)=2 > length(Q)/c=10/6.

The main bound is 40/6+1=23/3, so this is not a counterexample to that bound. The proof covers an infinite family, with e>=4, n=e^2(e+1)/2 and c=e(e-1)/2, where q=(e+1)/(e-1)<2.

## Why this is a general-projection construction

- An explicit quadratic normal matrix has determinant 2^e, proving actual incidence dominance by an etale point.
- Only a first jet at one point and a value at a second point are prescribed; no false two-first-jet independence is used.
- A two-point incidence has parameter codimension c>0, excluding all additional support points of the bad fiber for general parameters.
- Formal elimination followed by Nakayama gives the fiber ideal m^2 exactly, including higher terms.
- The argument descends from ordered section tuples to an open set of projection centers.
- The Q computation uses the full fiber and the conormal definition, including all n-e eliminated source variables.

All details are in [PROOF.md](PROOF.md).

## Scope and sources

The [2008 Oberwolfach source](https://ems.press/content/serial-article-files/46169) states the two questions in Roya Beheshti's contribution, printed pages 1440--1442. They are Conjectures 1.3 and 1.4 of [Beheshti--Eisenbud, arXiv:0806.1928v3](https://arxiv.org/abs/0806.1928v3). That paper works over an algebraically closed characteristic-zero field, a hypothesis omitted from the compact catalogue wording. The conjectures use regularity of the ideal sheaf of the fiber.

The [Ein--Lazarsfeld preliminary lecture notes dated May 4, 2024](https://www.math.stonybrook.edu/robert.lazarsfeld/LSGAV.Prelim.Draft.pdf) still formulate the weaker bound as Conjecture 4.2.15. The dated search made here found no later full resolution or published source for this stronger-comparison counterexample. This is a bounded literature check, not a novelty certificate or a claim of exhaustive worldwide coverage. No first-discovery claim is made.

The live catalogue URL returned HTTP 403. The exact numeric record was read from the supplied pinned corpus and then checked against the primary sources. The separate prior-report corpus has no matching OWR record; the repository's historical desk review was read instead and is not presented as a prior proof. Live checks found the row queued at 0/5, no existing target attempt directory, no ID-matching PR, and no exact group in the related-target register before this work.

## Five approaches and mathematical limits

1. Linkage and Hilbert-scheme tangent lengths: both inequalities hold for all-licci fibers. The gap is non-licci components.
2. Corank stratification: both hold when n<3(c+3), and for c=1 when n<20, by credited linkage/corank inputs. High-corank fibers remain.
3. Local square-zero deformation modules plus transverse jet incidence: complete candidate counterexample to the stronger comparison only.
4. Loewy-length interpolation: proved reg(Z)<=sum of the local nilpotency exponents. The needed all-dimensional generic-fiber budget remains unproved; the Q-based sufficient criterion is refuted by approach 3.
5. Asymptotic ideal powers: the weaker bound is equivalent to a sharp eventual containment by the Eisenbud--Harris theorem. The sharp intercept remains unsupported.

The checkable partial proofs and exact residual target are in [PARTIALS.md](PARTIALS.md); timestamps and stopping decisions are in [RESEARCH_LOG.md](RESEARCH_LOG.md).

## Reproduction

Run `python check.py` from this directory and compare its JSON output with `control-results.json`. Python's standard library suffices. Every arithmetic operation is exact. The bounded run checks e=2 through e=6, including the e=2 positive and e=3 equality controls and an intentionally nontransverse jet control. It completed in approximately 0.1 seconds with about 12 MiB maximum RSS in the recorded environment.

These controls do not numerically solve a random projection, replace the incidence proof, or certify the unresolved first question. The public SHA256SUMS binds the frozen files. SOURCE_PROVENANCE.json records source versions and hashes; source PDFs and imported corpora are not redistributed.
