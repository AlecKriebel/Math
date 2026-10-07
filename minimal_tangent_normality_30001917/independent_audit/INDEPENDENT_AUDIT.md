# Independent acceptance audit: VMRT normality

Problem 30001917 / OWR-11139-010. Queue rank 982.

**Accepted disposition: credited prior result (disproved). Research turns: 0/5.**

The frozen v1 packet is mathematically sound for its stated purpose. It reconciles the question with prior literature; it does not claim a new theorem or a new explicit numerical construction. No mathematical correction patch is required. The original packet is preserved byte-for-byte. This audit is separate from the author's scope audit and does not retroactively edit its historical status fields.

Audited manifest SHA-256:

`ab219c442efbac0927009ed5c346fd02e3555e9573374a1961b2efb30188c295`

## 1. Exact scope

The original Hwang contribution defines the relevant component through completeness and nonemptiness of its general-point family. Least degree among covering families is not part of that definition. Its normality question concerns the entire VMRT attached to a general ambient point. The adjacent classification result adds normality as a hypothesis and focuses on family dimension `dim(X)-2`; disproving that hypothesis does not disprove the conditional classification theorem. These points were checked directly in the contribution, including visual inspection of printed pages 2690–2691. [OWR 47/2011, contribution pp. 2690–2692](https://ems.press/content/serial-article-files/46361).

Consequently, three distinctions are mandatory:

- Local unsplitting is sufficient for the original problem, even when a different dominating family has smaller degree.
- Normality at a general ambient point means normality of the resulting whole tangent image. It does not mean normality only at the generic point of that image. The latter would not address this question.
- A normalized family parameter space and the tangent image are different varieties. Smoothness of the former does not automatically imply normality of the latter.

The packet observes all three distinctions. It also restricts its counterexamples to irreducible images, so no conclusion depends on interpreting normality for intersecting components.

## 2. Primary inputs and admissibility

### Casagrande–Druel

Example 1.6 and Proposition 1.7 apply with `(n,a,d)=(3,2,4)`. The inequalities for the smooth Fano construction hold, and the family is an irreducible component of the normalized rational-curve space. Its dominance and proper general-point fibers are justified in the proof of Proposition 1.7, using Construction 5.1 and Lemma 5.3. Theorems 1.9–1.10 identify the smooth connected normalized fiber and irreducible tangent image. Example 5.8 specializes them to the genus-seven normalization of a sextic. Remark 5.4 rules out least degree for every ample polarization; that qualification is explicitly retained in the packet. [Full article](https://druel.perso.math.cnrs.fr/textes/minimal.pdf).

The finite family normalization does not create a false properness condition. Properness of a parameter space and its finite surjective normalization are equivalent in this setting. Moreover, the curves through the chosen general point in this construction are smooth, so the distinction between a member and its marked branch introduces no ambiguity. Smooth connected varieties over the complex numbers have disjoint irreducible components; connectedness therefore establishes irreducibility here.

The numerical specialization is admissible:

- `n=3`, `d=4`, and `0≤a=2≤d`;
- `a≤n−1` and `d−a≤n−1`, both equalities;
- `2≤a≤d−2`, both equalities;
- family anticanonical degree `n=3` gives general-point dimension `3−2=1`.

The last line is the required codimension-one case: a curve in a two-dimensional projective tangent space.

### Hwang–Kim

Their definition uses actual minimum anticanonical degree. Theorem 1.3 permits `(n,d)=(6,3)` with a general degree-six weighted polynomial. Propositions 6.3–6.7 supply smoothness, the Picard generator, canonical class, degree-one curves, and the normalized general-point family. The final proof explicitly establishes irreducibility and a single dominating family for `n>d`, and nonimmersion for `n≥2d`. The introduction records unsplitting. Propositions 4.7, 5.2–5.3 and 2.9 were checked for the generality and dimension requirements behind the nonimmersion statement. [Journal article](https://content.algebraicgeometry.nl/2015-2/2015-2-008.pdf).

The specialization has `d=3` odd, `n=6>d`, and `n=2d`. The ambient weights are six ones, two, and three, with hypersurface degree six. Thus dimension is six and the anticanonical index is `(6+2+3)−6=5`. The normalized family dimension is `n−d=3`. Its finite image lies in projective dimension five, so its codimension is two. This second example strengthens the minimality and Picard-number assertions; it is not substituted for the first example's codimension-one role.

An ample generator has positive integral degree on every curve. A family with generator-degree one is therefore genuinely degree-minimal and cannot split into two nonzero effective curve classes of smaller positive degrees. Generality of the polynomial is essential. The packet asserts an existence result on the source's general locus; it does not assert that every smooth polynomial qualifies or supply a numerical coefficient list.

### Tangent-map normalization

Hwang–Mok's definition of a minimal component uses dominant evaluation and a projective general evaluation fiber. Their Theorem 1 gives birationality, and the discussion preceding Corollary 1 supplies general-point smoothness and invokes Kebekus's finiteness theorem. The normalized general-point tangent family therefore maps finitely and birationally to its image. Both counterexample articles also explicitly use this normalization description, avoiding reliance on an identification of an unnormalized coarse fiber with a smooth variety. [Hwang–Mok full text](https://hkumath.hku.hk/~nmok/IMR2004-011.pdf).

## 3. Verification of the deductions

### Finite birational normalization argument

The argument in the packet is correct. On an affine open of an integral target, a finite birational map from a normal source corresponds to rings `A⊆B⊆Frac(A)`, where `B` is integral over `A` and integrally closed in their common fraction field. An element integral over `A` satisfies the same monic polynomial over `B`, so it belongs to `B`; conversely every element of `B` is integral over `A`. Hence `B` is precisely the integral closure of `A`.

If the target is normal, the finite birational map is an isomorphism. Its composite with a closed embedding into projective tangent space would then be a closed embedding, with injective differential. The stated nonimmersion contradicts that consequence. This is not the invalid inference that singularity by itself implies nonnormality in arbitrary dimension.

### Curve arithmetic and exact defect

The family degree formula gives `binomial(4,2)=6`. The supplied genus formula specializes to

`1 + (1/2)·6·(2·(4−2)−2) = 7`.

The plane-curve arithmetic genus is `(6−1)(6−2)/2=10`. Thus the Euler characteristics of the target and normalization are `−9` and `−6`, respectively, and they cannot be isomorphic.

For an integral projective curve, the cokernel of its structure sheaf inside the finite normalization pushforward has finite support. Its length equals the difference of these Euler characteristics, namely three. The packet's exact defect is therefore justified. It does not identify three singular points or three ordinary nodes. The source's immersion statement for this curve is fully compatible with its failure of injectivity and normality.

The independent combinatorial consistency check also works: a transposition of four sheets moves four of the six two-element subsets in two pairs; twelve simple branch points each contribute two to ramification. Riemann–Hurwitz then gives `2g−2=−12+24=12`, hence `g=7`. This check is arithmetic conditional on the generic-projection facts, not an independent proof of those geometric facts.

## 4. Source and provenance checks

All four locally available full PDFs independently matched the frozen source metadata in bytes, SHA-256, and page count. Relevant definitions, complete theorem statements, numerical restrictions, and the passages establishing component/properness, general-point irreducibility, and normalization were inspected. The decisive curve example and the sixfold theorem's final proof were additionally checked visually.

The public OWR, Casagrande–Druel and Hwang–Mok PDF endpoints were re-opened successfully. The web reader returned an internal error for the Hwang–Kim endpoint; the complete local journal PDF remained available and matched its recorded hash. This is a reader-access limitation, not a missing mathematical source. The author publication list independently confirms the Casagrande–Druel 2015 publication, and arXiv confirms the December 2012 initial submission and January 2015 revision. No claim about the contents of its first arXiv version is made. [Author bibliography](https://druel.perso.math.cnrs.fr/publications.html), [arXiv history](https://arxiv.org/abs/1212.5083).

The two complete cached public corpora were independently rehashed and recounted. They match the recorded 15,458 problem records and 6,701 research-result records. There is exactly one exact problem match and no exact research-result match. Broad semantic scans produced four problem hits and eleven research-result hits; manual review found no same-target substantive research attempt. Broad hits concern other tangent-map questions and are not evidence of an inherited solution. The saved repository search receipts show seven PR queries and nine distinct branch queries, including pagination. Those historical remote searches were inspected, not rerun in this audit; their absence conclusions remain bounded by snapshots, indexing, and terminology.

## 5. Executable and corruption controls

The frozen verifier passes all 28 checks under ordinary Python, `-O`, and `-OO`. Its explicit exception checks survive optimization; it does not depend on removable `assert` statements.

Thirty-nine controlled runs were executed on disposable copies: thirteen cases in each of the three modes. All behaved as intended:

1. unchanged baseline accepted;
2. attempts to use the pre-freeze results-writing option on a frozen packet rejected;
3. wrong normalization genus rejected after resealing the local manifest;
4. malformed source digest rejected after resealing;
5. a nonzero research-turn count rejected after resealing;
6. a mathematical-turn chronology flag rejected after resealing;
7. a changed report byte rejected;
8. inconsistent stored check output rejected;
9. a missing declared file rejected;
10. an extra undeclared file rejected;
11. an extra directory rejected;
12. a nonlocal manifest entry rejected;
13. a coordinated report-and-manifest rewrite accepted internally but produced a different manifest digest and was rejected by the independently pinned digest.

The last control records an important trust boundary rather than a mathematical defect. The verifier validates a manifest's contents and reports its SHA-256; it does not independently know a trusted external manifest digest. Acceptance in this audit therefore requires the exact pinned digest above. Replacing both content and manifest does not preserve that identity.

All nine manifest-listed files were separately byte-checked. The tenth file is the manifest itself. The ZIP is 16,237 bytes, SHA-256 `ae0ee4bf1381861080eba7b0a84cedb84c266dcac3834f7703226c1f14aef913`, and its files exactly match the frozen packet. Neither arithmetic checks nor hashes certify the published geometric theorems; the packet correctly states that limitation.

## 6. Acceptance, dependencies, and corrections

Accept the negative answer in the original locally-unsplit scope, including its codimension-one focus. Also accept the separately stated negative answer for a genuinely degree-minimal unsplit family on a Picard-number-one Fano sixfold.

The indispensable dependencies are the cited geometric existence/family results and tangent-map finiteness and birationality. Their full proofs are not rederived or formally verified by this audit. Conditional on those published results, the elementary deductions contain no remaining gap. Nothing here claims novel mathematical research, a numerical general polynomial, or a classification of the surviving normal cases.

No correction patch is needed. Keep the original packet unchanged and accompany it with this independent acceptance record. Recommended queue disposition remains:

- Status: `credited prior result (disproved)`
- Turns: `0/5`
- Findings: Casagrande–Druel's codimension-one counterexample and Hwang–Kim's genuinely degree-minimal Picard-one counterexample, with their existing attribution.

This audit contains authored analysis and public verification metadata only. It contains no copied PDF, source extract, dataset record, or private coordination material. No publication or remote write was performed.
