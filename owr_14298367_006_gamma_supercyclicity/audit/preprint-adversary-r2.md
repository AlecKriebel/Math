# Independent adversarial preprint review, round 2

Date: 2026-09-23. Artifact consistency checkpoint: 2026-09-23 15:06:21 UTC.

Reviewer: a fresh independent AI subagent. Review goal: try to falsify the argument and its stated scope in version 1.0.1, with particular attention to arbitrary scalar sets, one-sided boundedness, the composition model, infinite-dimensional coefficient spaces, and the actual hypotheses of the cited theorems. Review completion estimate: **100% of this assigned round**. This is an internal mathematical audit, not external peer review or a proof-assistant certificate.

I read the repository's `AGENTS.md`, then the manuscript and primary sources. I did not read any earlier review report or its conclusions. No individual was contacted. No manuscript, website, build, package, or source file was edited; no commit or push was performed. Scratch output is confined to `tmp/review-r2/`.

## Verdict

**No actionable findings.**

| Grade | Findings |
| --- | --- |
| Blocking | None |
| Worthwhile correction | None |
| Cosmetic correction | None |

The stated equivalence follows from the written direct proof under the stated hypotheses. The independent deduction from Abbar--Kuznetsova also checks out. The attribution accurately describes an explicit application of earlier criteria, and the separability qualification agrees with the original report. I found no counterexample within the theorem's scope and no unproved central step disguised as a reduction.

## Exact reviewed artifacts

| Artifact | SHA-256 |
| --- | --- |
| `manuscript/note.tex` | `3b16fbb6a78491f117dd2d50345c1863dad7b6486863a403ecccf74d6b4a9794` |
| `output/pdf/note.pdf` | `671cf6be89c45cbda49c207c2a656064958494fce60f05619d63a3061ee123c7` |
| `output/note-source.zip` | `7ef22e4bdf8a34289384f25d2fb481d76059910b9caf21b6d1d8ff92c4d47385` |
| `output/zenodo-upload-kit.zip` | `838ed43c0f91a402e608a72421b7564288ed9a2b1d1bb15881c61af9b8001e22` |
| `site/index.html` | `7743252cb1d8ed0b9cb21a1728f2af9fa4f4e83f94b026b6a5722db8abf73079` |
| `zenodo/metadata.json` | `b16eb38ce910522cf1187a5235391cc1ba9c06fedafb41326f67a437f2088f3c` |

The TeX and PDF hashes agree with the review assignment. Both display version 1.0.1 and the date 23 September 2026.

## Independent attempts to break the direct proof

### Necessity of the finite-block criterion

I checked lines 89--106 without assuming that right translation is bounded. A dense restricted projective orbit meets every nonempty open set at arbitrarily large times: remove the closed nowhere-dense finite union of complex lines spanned by the first finitely many iterates, then use orbit density in the remaining open set. This argument does not assume that the set of allowed scalars is a group, a semigroup, measurable, closed, or countable.

A vector whose support is bounded above cannot have a dense restricted projective orbit for left translation. Thus the choice of a fixed nonzero coordinate `x_k` with `k >= max F` is justified. Approximation to the indicator of `F` gives the forward-tail estimate because `F+n_r` escapes finite intervals. At the coordinate `k-n_r`, the target vanishes for large `r`, giving the backward-tail estimate. The only comparison needed is

`c_(t-d)^(1/p) <= ||S||^d c_t^(1/p)` for nonnegative integers `d`.

It follows from bounded left translation. Both estimates use the same allowed scalar. There is no need to divide by an arbitrary element of the scalar set and demand that its reciprocal still belong to that set.

### Sufficiency and the Baire step

For finitely supported `a` and `b`, the sequence `R_n b` belongs to the weighted sequence space even when global right translation is unbounded. Direct reindexing gives

`||lambda^(-1) R_n b||_c^p = |lambda|^(-p) sum_(j in supp b) c_(j+n) ||b_j||^p`,

`||lambda S_E^n a||_c^p = |lambda|^p sum_(j in supp a) c_(j-n) ||a_j||^p`.

Consequently the two errors in lines 108--113 have exactly the claimed bounds. No disjointness of supports is needed for these bounds. The identity `S_E^n R_n b = b` holds on finite sequences.

The space `Y_E` is a separable Banach space because `E` is separable Banach and `p` is finite. For every basic open set, the union in lines 115--119 is open, even if the union is indexed by an arbitrary uncountable scalar set. It is dense by the preceding two-open-set construction. Baire is applied to the countable base, not to the scalar set. The intersection therefore consists of vectors with dense restricted orbits.

### Counterexample probes and boundary cases

- **Empty or zero-only scalar sets:** no dense orbit is possible on these nonzero infinite-dimensional sequence spaces; the criterion cannot hold because it requires a nonzero scalar. The separate treatment is correct.
- **Singleton, sparse, nonclosed, or nonmeasurable scalar sets:** the proof retains the exact selected scalar and makes no closure or algebraic operation on the allowed set. The construction does not silently replace it by its modulus, closure, or multiplicative hull.
- **`p=1`:** every norm estimate and density argument remains valid. No duality identification, reflexivity, or use of a finite conjugate exponent is hidden in the proof.
- **Bounded but noninvertible translation:** take `c_j = exp(-j^2)` for `j <= 0` and `c_j = exp(-j)` for `j >= 0`. Then `sup_j c_(j-1)/c_j = e`, while the ratios defining right translation are unbounded. Both tails tend to zero for every fixed finite block with scalar `1`. This tests the broader lemma: the proof still works, precisely because its right translation is used only on finite sequences. The main composition theorem separately assumes bounded invertibility.
- **Infinite-dimensional and nonreflexive `E`:** finite support is dense in `Y_E`; the functional quotient only uses a nonzero vector and a bounded linear functional with value one on it. There is no finite-dimensional or reflexive coefficient-space assumption.
- **Zero coefficient space:** this could invalidate a general amplification statement, but it is expressly excluded. In the composition application, `0 < mu(W) < infinity` guarantees a nonzero coefficient space.

### Quotients and conjugacies

For the functional quotient in line 126, the right inverse is `(a_j) -> (a_j e)`, so the asserted surjectivity is valid. A continuous map with dense range sends a dense set to a dense subset of its target: the inverse image of each target open set is nonempty and open. In particular, this applies both to the surjective quotient and to the dense-range map later used in Section 4. Commutation preserves the same restricted orbit exactly.

For the composition model, the finite measure bounds yield positive finite `m_j` and bounded ratios in both directions. The pullback measures `nu_j(C)=mu(f^j C)` are countably additive because the transformation is injective and bimeasurable. Bounded distortion gives their two-sided domination by `c_j mu|_W`, which establishes the displayed integral and norm identities.

These measure-class bounds make pullback well-defined on equivalence classes. Conversely, choosing representatives `u_j` and gluing `u_j composed with f^(-j)` on the disjoint measurable layers gives a measurable representative in the original `L^p` space. Different representatives only change null sets. Countability of the partition is enough; no standard-Borel, countable-generation, or regularity assumption on the measure space is needed. A null remainder is harmless because the union of all layers, and hence its complement, is invariant. This verifies onto-ness as well as injectivity and bounded inverse.

The calculations `J T_f = S_E J` and `D B_w = S D` have the correct shift direction and weight indices. The factor `m_0` cancels in the latter calculation. These maps are complex-linear, so they preserve every fixed allowed scalar set without changing its phases.

The nonseparable example is also valid: the countably many layers have finite total measure `3`, distortion constant `1`, and adjacent mass ratios between `1/2` and `2`. Uncountably many coordinate indicators on the zeroth Bernoulli layer are pairwise separated by `(1/2)^(1/p)`, so its `L^p` space is nonseparable. Every projective orbit lies in a separable closed linear span. Meanwhile the scalar weights `c_j=2^(-|j|)` satisfy both tails with scalar `1`. The example correctly shows why sigma-finiteness alone is insufficient.

## Primary-source checks and attribution

I checked the relevant primary texts directly, rather than taking the earlier audit files as authority.

- **[Abbar 2019, publisher PDF](https://bulmathmc.enu.kz/index.php/main/article/download/55/93/364), printed pp. 74--75:** Theorem A uses positive weights, bounded backward translation, `1 <= p < infinity`, and an arbitrary scalar set with a nonzero member. Its single-offset estimates have the orientation used in the note. Theorem 2 supplies a restricted-scalar universality criterion. The publisher's [record](https://bulmathmc.enu.kz/index.php/main/article/view/55) confirms the author, year, volume/issue, and pages. The PDF text was readable through the web tool; a separate screenshot request timed out.
- **[Abbar--Kuznetsova, arXiv v2](https://arxiv.org/pdf/2005.11230v2), pp. 1--3 and Section 6:** Theorem B inherits second countability, local compactness, noncompactness, local `p`-integrability, admissibility for the selected translations, finite `p >= 1`, and a nonzero allowed scalar. It additionally requires an abelian generated subgroup. The note's two discrete groups and parameter sets satisfy these conditions. The translation convention and the two maximum estimates agree. The [arXiv record](https://arxiv.org/abs/2005.11230v2) confirms the 2020 version and 2021 journal citation.
- **[Oberwolfach Report 19/2024](https://publications.mfo.de/bitstream/handle/mfo/4214/OWR_2024_19.pdf?isAllowed=y&sequence=1), printed pp. 1078--1083:** both relevant contributions explicitly start with separable Banach spaces. The report imposes boundedness for the composition operator and its inverse, states the bounded-distortion condition used here, and gives the same associated shift weights. The arbitrary-scalar-set question appears on printed p. 1083 in D'Aniello's contribution reporting joint work with Maiuriello. The note's scope and attribution match.
- **[D'Aniello--Maiuriello publisher record](https://link.springer.com/article/10.1007/s43037-025-00463-0):** the 2025 journal publication details and preceding real/complex supercyclicity work agree with the note.

The finite-block conversion in lines 82--86 is correct: choose `q >= max(F union {1})`, iterate the one-sided norm comparison downward from `q+n` and `q-n`, and take a finite sum. Conversely, the finite-block statement applied to a singleton yields the single-offset condition. The increasing times required for Theorem 2 can be chosen successively using the explicit lower-time cutoff, on blocks `[-k,k]` with errors tending to zero. This verifies the first attributed amplification route.

For the second route, counting measure and error tolerance below one force the retained subset to equal the finite set. On `Z`, taking parameter `-n` produces left translation; the two signs in the estimates agree with the note. A finite set of times cannot satisfy arbitrarily small simultaneous estimates, because their product cancels the scalar and has a positive minimum. On `Z^2`, compact sets are finite, and their first-coordinate projections give precisely the estimates required by Theorem B. The weight is locally `p`-integrable and admissible on both groups, including for a bounded but noninvertible left translation.

Finally, the series defining `R` in lines 163--165 converges absolutely, including for `p=1`, and is bounded by the stated norm. Every chosen `e_k` is in its range after multiplying a scalar coordinate vector by `2^k`. Thus its range is dense. Applying `R` coordinatewise is bounded and has dense range by approximation of finitely supported targets. This completes the asserted deduction without invoking the proof of Lemma 2.

These checks support the note's limited attribution claim. This round was not a new exhaustive literature-priority search, and the note does not claim priority for the scalar criterion or amplification mechanism.

## PDF and artifact consistency

I rendered the exact reviewed PDF with Poppler at 125 dpi and visually inspected all five complete pages. The theorem statement, equations, proof continuations, references, links, and author footnote are legible. No clipping, overlap, missing glyphs, broken numbering, or misleading page break was found. The final bibliography page and the proof continuation across pages 3--4 are coherent.

The independent consistency check recorded in `tmp/review-r2/artifact-checks.json` passed all 35 checks. In particular:

- The canonical PDF agrees byte-for-byte with both downloadable copies and the Pages copy in `docs/papers/gamma-supercyclicity/`.
- The current source, built website, and Pages files agree; the source ZIP's four members agree with their canonical files.
- Both ZIP CRC checks pass. Every Zenodo-kit member agrees with its staging counterpart, including the nested source ZIP and PDF.
- The three direct metadata copies agree, and both API metadata files wrap exactly that metadata.
- Every entry in the current downloadable-site and Zenodo-upload checksum manifests validates.
- The manuscript, website, citation file, source README, copy-and-paste fields, and metadata consistently say version 1.0.1, retain separability, attribute the criteria, and describe the note as AI-assisted and unrefereed.

The root `SHA256SUMS` and historical `audit/live-deployment.json` were intentionally outside this current-artifact comparison because the review assignment identifies them as records of the preceding published snapshot. I did not mistake those historical records for the rebuilt files. I did not test a newly published live deployment or create a Zenodo deposit.

## Remaining gap

No manuscript correction remains from this review. The strongest result verified here is the theorem and both written proof routes, under the explicit assumptions, together with consistency of the reviewed version's current local distribution artifacts. An internal adversarial review does not establish exhaustive priority or formal machine verification; neither is claimed by the note.
