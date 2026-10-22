# Classical and mechanism priority audit: PR 952 / problem 10400145

Audit date: 16 October 2026. Bound candidate head: `989a532ae1d50894190d010a0a02ba8c3d71ee05`.

## Verdict

**The cubic-rank/Casson mechanism is classical. No qualifying earlier complete resolution of the exact ordinary-completion statement was located in the bounded primary-source coverage described here. Novelty and firstness are not cleared.**

The candidate's existing description as a deduction from established results, with no novelty or current-open claim, is appropriate. This audit finds no required mathematical revision and no verified earlier complete predecessor. Those statements do not establish that the combination was previously unknown. A literal resolution and a novel research contribution are separate questions.

The most useful additional attribution is Lê–Murakami–Ohtsuki (1998), Proposition 5.3 and Remark 5.4, pp.563–564: both the Casson theta term and the type-A cubic weight already occur there. Garoufalidis–Lê–Mariño (2008), §3 p.8, independently makes the same rank-growth mechanism explicit and places it in an all-rank parameter space that permits poles. The candidate's controlling first-coefficient citation to Lê (2000), p.821, is already direct and sufficient for its topology input.

## Independence and test

All 33 supplied originals were authenticated against both pin files and the bound Git head before mathematical intake. The initial priority criterion and five-family approach map were saved before reading the candidate proof, source metadata, or earlier audit conclusions. Initial searches also preceded that intake. Earlier audit conclusions were subsequently used as leads and scope comparisons, never as proof of historical absence. START and END receipts identify the original files; the originals were not modified.

The qualifying-predecessor test was deliberately weak: any earlier primary-source exact counterexample, theorem, or equivalent full impossibility for the printed completion and standard invariants counts, regardless of title, conjecture number, ranks, manifold, or mechanism. An ingredient or an immediate corollary available to a reader is distinguished from a source that actually states or establishes that full impossibility. Positive constructions in other rings do not silently count as either a proof or disproof of the target.

## Exact mathematical comparison

The printed source defines

\[
R=\varprojlim_m\mathbb Z[q,q^{-1}]/\bigl(\prod_{j=1}^m(q^j-1)\bigr),\qquad
S=\varprojlim_m R[t]/\bigl(\prod_{j=1}^m(t-q^j)\bigr).
\]

It asks for standard unified `sl_n` values at `t=q^n`, for every `n≥1`, with the rank-one value set to 1. The index `n` labels `sl_n`; its Lie rank is `n−1`. Printed pp.490–492 fix the ring, the perturbative interpretation, and the orientation-specific Poincare example. No inverse of `q−1` occurs. [O](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

The finite third quotient of S permits a quadratic representative in t. Substituting `q=1+x`, `x²=0`, makes its first x coefficient affine in n at nodes 1,2,3. Thus the second difference must vanish. Lê's formula for an integral homology sphere is `c_1(n)=n(n²−1)λ_C(M)`. At those nodes it gives `0,6λ_C,24λ_C`, with second difference `12λ_C`. The oriented Poincare example yields `0,−6,−24`. This is an elementary incompatibility with a classical coefficient formula. [L](https://people.math.gatech.edu/~letu/Papers/PERT_NEW01.pdf)

Habiro–Lê's fixed-g theorem, projective specialization, and Taylor identification supply the standard unified-invariant bridge; their q is `v²=exp(h)` uniformly in type A. [HL, Theorem 1.1, Proposition 1.2, Proposition 1.9, §3A2](https://msp.org/gt/2016/20-5/gt-v20-n5-p04-s.pdf) This bridge must be retained in a rigorous modern account. The earlier printed conditional question itself describes the perturbative interpretation, but the later theorem removes reliance on the historical unproved premise.

## Classical chain and what it establishes

**CP-001 — Classical mechanism, verified.** LMO's Proposition 5.3 identifies the theta coefficient with the Casson–Lescop–Walker invariant; Remark 5.4 explicitly evaluates the `sl_N` theta graph as `2N(N²−1)`. This shows that the nonlinear rank dependence was established in the original universal perturbative framework. It is an ingredient and strong explanatory antecedent, not a personally verified published ordinary-S impossibility. The page uses a different Poincare orientation and Casson normalization; its displayed numerical manifold value should not be copied into the candidate without conversion. [LMO (1998), pp.563–564](https://people.math.gatech.edu/~letu/Papers/LMO.pdf)

**CP-002 — Direct coefficient attribution, verified.** Lê's 2000 article gives the coefficient in the exact `x=q−1` perturbative convention. Its 1998 arXiv v2 already contains the homology-sphere specialization, while its rational-homology normalization displays an additional Legendre-symbol convention. The published formula controls the citation; the earlier version establishes a verified antecedent date, not an earliest-possible priority claim. [L](https://people.math.gatech.edu/~letu/Papers/PERT_NEW01.pdf), [L-preprint](https://arxiv.org/pdf/math/9802032v2)

**CP-003 — All-rank degree constraints, verified.** Garoufalidis–Lê–Mariño explicitly writes `W_glN(Θ)=2(N³−N)hbar`; its connected-graph bound at degree d is rank degree at most `d+2`, rather than d. Its free energy belongs to `hbar^(-2) Q[[tau,hbar²]]`, with `tau=N hbar`. At the theta level, substituting `N=tau/hbar` produces `2tau³/hbar²−2tau`. This last displayed conversion is this audit's deduction, and explains precisely why that classical construction permits the growth excluded by regular first-order interpolation in S. Its inspected statements do not themselves assert the full target impossibility. [FE (2008), pp.1–3,8](https://letu.math.gatech.edu/Papers/Free_Energy.pdf)

**CP-004 — LMO universality history, verified scope.** Kuriya–Lê–Ohtsuki proves the all-simple-Lie-algebra perturbative bridge. Its introduction explicitly distinguishes its complete proof from an earlier unpublished announcement and a partially incomplete proof. Therefore neither the 1998 universal-program language nor a later abstract alone should be used to backdate the complete all-g bridge. The explicit theta calculation and Lê coefficient formula remain independent classical evidence. [KLO (2012), pp.458–460](https://letu.math.gatech.edu/Papers/LMO_Conjecture.pdf)

## Completion and alternate-construction comparisons

| Primary route | Personally verified scope | Why it does not establish the exact S assertion or its earlier complete negation |
|---|---|---|
| Habiro, cyclotomic completions, 2002 preprint / 2004 publication | Monic completions; Taylor maps; invertibility of q; localization by cyclotomic polynomials | The coefficient ring R is the ordinary Habiro ring. Localization by `Phi_1(q)=q−1` is an explicitly different algebra. The inspected algebraic statements do not apply the rank obstruction to standard homology-sphere invariants. |
| Habiro, 2006 v1 unified SU(2) paper | Fixed-g invariant; two-variable colored-Jones construction for knots; concluding generalizations | Its extra knot variable labels representation color for fixed `sl_2`, not varying Lie algebra `sl_n`. §16.2 explicitly points to Conj. 7.29. Its desired cyclotomic LMO object is another completion question. |
| Habiro, bottom tangles, 2006 | Universal construction and introduction's homology-sphere application | The stated application explicitly points to fixed-g Conj. 7.29. It does not identify a rank-unifying S element. |
| Beliakova–Gorsky, 2021 v2 / 2024 publication | Theorem 9.3 constructs the invariant for fixed N in the Habiro ring; Proposition 11.5 gives HOMFLY interpolation stability | Stability of interpolation polynomials is not uniform ordinary-S convergence after the surgery/Kirby-color operation. Corollary 11.6 visibly permits factors `(1−q)…(1−q^k)` in denominators of the generic-A expansion. |
| Tsuji, 2018 / 2019 / selected 2022 follow-up | `Q[rho][[h]]` skein invariant; 2019 announced quantum-series recovery | Polynomial dependence on rho allows cubic degree at first order in h. It is a different parameter space. In the 2018 version recovery is an expectation; the 2019 theorem points to a paper in preparation. That announced proof was not located in the present coverage. |
| Rozansky, 2001/2002 rationality/RCC work | Knot/color expansions and Lie-algebra-universal graph invariants with Alexander denominators | The color and graph variables and their denominator conditions differ from varying Lie rank in S. The rationality results/conjectures inspected are not ordinary-S impossibility statements. |
| Fang–Zhou, 2026 v1 | Rank-uniform symmetric-color knot construction over an integer-valued subring of `Q(q)[A±1]` | Its coefficient ring permits q poles; rank and color are fixed before root-of-unity evaluation. Its figure-eight sharpness example is a knot-coefficient obstruction, not the exact homology-sphere impossibility. Its proofs were not audited here. |

References and exact reading scopes for each row are in `READING_SCOPES.json` and `BIBLIOGRAPHY.md`. No row is claimed to exhaust its author's work.

## Source status and corrections

**CP-005 — No verified correction located; bounded finding.** The publisher body still displays the same S and rank-one convention. The author's project page links a solutions page; its three entries concern other numbered problems. The hosted Bigelow draft also displays the same completion. Ohtsuki's arXiv record lists one version. These facts do not prove that the statement remains open, was never corrected elsewhere, or was not known false informally. No typo or intended replacement ring has been identified by this audit. [Publisher record](https://msp.org/gtm/2002/04/p024.xhtml), [official solutions page](https://www.kurims.kyoto-u.ac.jp/~tomotada/solution.html)

**CP-006 — Version/date precision, optional bibliographic improvement.** The source's volume year is 2002, but the MSP landing page states publication on 1 June 2004, following revision in 2002 and acceptance in 2004. A PDF creation timestamp should not replace that publication history. Beliakova–Gorsky now has a 2024 published version, personally retrieved and compared at the relevant statements; its theorem scope agrees with the 2021 v2 scope used above. The candidate's older repository source was not freshly served: that URL returned an empty 202 HTML response. The newly retrieved publisher PDF supplies the comparison instead. [O publication record](https://msp.org/gtm/2002/04/p024.xhtml), [BG publication record](https://link.springer.com/article/10.1007/s00029-024-00990-y)

## Required constraints, optional additions, and gaps

No required manuscript change is identified by this priority audit. The following constraints remain required for promotion and are already substantially met by the candidate: attribute the coefficient and unification bridge; state the literal ring and normalization; make no novelty, firstness, global absence, or current-open claim. Do not upgrade this audit into a certificate that no predecessor exists.

Optional improvements are an explanatory citation to LMO (1998) Remark 5.4 and FE (2008) §3; a precise note on the 2002 volume year versus 2004 publication date; and citation of the published BG version. Tsuji is useful related context only if its version-dependent theorem status and different ring are explained.

Coverage gaps are concrete:

1. Only selected passages of large papers were personally read. Full-body hashes authenticate bytes, not complete-paper review. The reading-scope inventory distinguishes page selections and visual checks from text-search hits.
2. Habiro's Tokyo/Kyoto personal-page probes and Tsuji's researchmap page returned 403; a guessed Lê papers directory returned403 and guessed papers.html returned404. Some alternate official sources were accessible, but inaccessible unique material remains a gap.
3. Tsuji's 2019 in-preparation reference and its possible later publication were not located. The selected 2022 scanned follow-up cites the 2018 preprint; only its first and final pages were visually read, and its empty text extraction was not treated as negative evidence.
4. The search is not an exhaustive citation graph, database review, non-English literature audit, thesis review, or conference-notes review. Informal prior knowledge cannot be ruled out without external evidence. No external communication or outreach draft was made.
5. No public source found in this audit establishes the author's intended corrected formulation. Outside author input could clarify intent or unpublished history; that fact is recorded without preparing contact.

## Attribution recommendation

A precise formulation is: “For the completion and normalization printed in Ohtsuki's Conjecture 7.30, an elementary finite-jet constraint contradicts Lê's classical first-coefficient formula whenever the Casson invariant is nonzero; Habiro–Lê supplies the unified-invariant identification.” Historical context may add that the same cubic type-A behavior is already explicit in LMO (1998) and in the 2008 all-rank free-energy formalism. This recommendation makes no priority claim about the elementary combination itself.

Completion of the assigned bounded audit: 100%. Historical absence/novelty clearance remains unresolved and is not represented by that workflow percentage.
