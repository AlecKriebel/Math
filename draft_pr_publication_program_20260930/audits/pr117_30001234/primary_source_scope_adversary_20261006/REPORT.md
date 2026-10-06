# PR117 independent primary-source and scope audit

## Verdict

**PASS for the exact mathematical scope of the proposed counterexample.** No mandatory source-scope correction was found in the original `CANDIDATE.md`. This audit independently read the original source record and the empty prior report, then the actual primary sources, before any other family's report. It checks immutable submitted head `8163ee0dc7a0f944570925984cef2dc0fb291ad8` for problem 30001234 / OWR-3471-008. It does not establish novelty, current openness, publication readiness, or permission to merge.

The original question is answered negatively by the displayed six-variable, three-generator example. The proof must be presented as an answer to a condition on optimal fibers of the *augmented* matrix. It is not a new computation of a determinantal log canonical threshold or a contradiction of the conditional Shibuta–Takagi theorem.

## Primary sources actually inspected

1. The official EMS PDF of OWR 21/2009, DOI [10.4171/owr/2009/21](https://doi.org/10.4171/owr/2009/21), retrieved from [the official full report](https://ems.press/content/serial-article-files/46224). The full Takagi contribution was read: printed pp.1136–1139, physical PDF pp.36–39. Proposition 5 starts on printed p.1137 and continues on p.1138; Question 8 is on p.1139. Relevant printed pp.1137–1139 were inspected visually, and the decisive formulas, hypotheses and question were separately inspected in complete 300 dpi crops.
2. Shibuta–Takagi, [*Log canonical thresholds of binomial ideals*, arXiv:0810.1278v3](https://arxiv.org/abs/0810.1278v3), dated 9 April 2009. The exact version's entire sixteen-page PDF was read. The operative portion is Proposition 2.1 and its complete proof, pp.6–8; Question 2.2, p.8; Theorem 2.4 and its complete proof, pp.8–10; and the explicit space-monomial-curve setting of Theorem 3.1, pp.10–14. The decisive p.6 and p.8 hypotheses and inequality/quantifier were separately inspected in 300 dpi crops. The published publisher PDF was not retrieved, so this audit does not assert bytewise or linewise identity between the preprint and the journal version.
3. LaClair, [*Invariants of Binomial Edge Ideals via Linear Programs*, arXiv:2304.13299v2](https://arxiv.org/abs/2304.13299v2), dated 16 June 2023. Actual pp.3, 9–11 and 14 were read, including the definition of the allowed vertex subsets, program (8), its biconnected variant, and Remark 3.15. Program (8)'s constraints were visually inspected at 300 dpi. This is a bounded check of the candidate's LP distinction, not an audit of the entire paper or of the later published version.

All complete PDF bodies, extracted text, page images and bounding-box intermediates remain private and ignored. Public metadata records their actual SHA256 hashes, sizes, exact versions, retrieval endpoints, read ranges, and decisive visual observations. No outside individual was contacted. No citation or access gap was filled by assumption.

## Exact source hypotheses and their mapping

| Source requirement | Candidate and audit |
| --- | --- |
| A polynomial ring over a field of characteristic zero | `S=k[x1,x2,x3,y1,y2,y3]`, with any characteristic-zero field `k`. Algebraic closure is not a hypothesis of Proposition 5 or Proposition 2.1. |
| Binomial generators of the form `x^a_i-gamma_i*x^b_i` | All three cyclic minors have this form with `gamma_i=1`, which is nonzero in every field. No coefficient genericity is required. |
| Nonzero vectors in `Z^n_{>=0}` | Every term has a nonzero squarefree degree-two exponent vector; zero coordinates are allowed. The sources do not require every coordinate to be positive. |
| No monomial in the ideal | Evaluation at the all-ones point annihilates all generators. Every nonzero scalar multiple of a monomial evaluates to a nonzero scalar; therefore no such monomial belongs to the ideal. This is an unrestricted argument, not a bounded computation. |
| Minimal binomial generating system in Question 8 / Question 2.2 | The ideal is homogeneous and generated in degree two. Its degree-two component has basis the three minors because their six monomials are pairwise distinct. Thus its quotient by the homogeneous maximal ideal times the ideal has dimension three; no two elements can generate it, even in the localization at the origin. |
| Matrix with exponent columns and the entire `(I_r I_r)` bottom block | Reconstructing from the three minors gives precisely the candidate's nine-by-six matrix. None of the three bottom rows is dropped. |
| Nonstrict constraints `Az<=1`, with nonnegative rational coordinates | Both primary sources print `<=`, not `<`. The endpoints and all rational points of the optimal segment meet these literal constraints. |
| There exists an optimizer whose augmented image differs from every other optimizer's augmented image | This means a singleton fiber among optimal points. It is neither merely uniqueness of the optimizer nor uniqueness of the image vector of the whole face. Every point of the candidate's face has a second rational point with the same image, so the exact existential condition fails. |

The Question 8 formulation adds the absence of monomials and minimality to the binomial setup of Proposition 5. It imposes no regular-sequence, space-curve, primeness, or irreducibility restriction. The counterexample is prime, but primeness is unnecessary to negate this target. The candidate's independent primeness argument was read and contains no source-scope dependency.

## Complete quantifier check and LP argument

Write the cyclic generators as

`f1=x1*y2-x2*y1`, `f2=x2*y3-x3*y2`, `f3=x3*y1-x1*y3`.

Let `z=(mu1,mu2,mu3,nu1,nu2,nu3)` and let `F` be the rational optimal face. The bottom three rows impose `mu_i+nu_i<=1`, giving objective at most three. For every rational `t` in `[0,1]`, the point

`z(t)=(t,t,t,1-t,1-t,1-t)`

has full nine-coordinate augmented image equal to one and objective three. Hence three is the optimum. Conversely, optimality forces equality in all three bottom rows, so `nu_i=1-mu_i`. The first three exponent rows then impose `mu1<=mu3`, `mu2<=mu1`, and `mu3<=mu2`. Consequently all three `mu_i` equal one number `t`; nonnegativity gives `0<=t<=1`. This determines the entire rational optimal face, not just several optimizers.

Every rational point of that face has a distinct rational companion: choose `z(0)` when `t!=0`, and choose `z(1)` when `t=0`. Both have the same full augmented image. Thus the negation proved is

`for every z in F, there exists z' in F with z'!=z and Az'=Az`.

This is exactly the negation of the source's existential singleton-fiber hypothesis. The entire face has one image vector, but no fiber is a singleton. Merely finding two coincident optimizers would not suffice for the source question; the complete-face argument closes that gap. It also works over real points, although the target requires only rational points. No rational density argument, numerical tolerance, threshold computation, or positive-characteristic theorem is needed.

Because the objective is the sum of the bottom three image coordinates, any feasible point sharing an optimizer's augmented image is automatically another optimizer. This explains why a feasible-fiber formulation would be equivalent here; it does not allow replacing augmented-image separation by separation under the exponent rows alone.

## Localization boundary and the positive special cases

The source polynomial ideal and the local threshold at the origin must be kept distinct from Laurent localization. The relation

`x3*f1+x1*f2+x2*f3=0`

makes `f3` redundant after `x2` is inverted. It does not make `f3` redundant in the polynomial ring or the local ring at the homogeneous maximal ideal, where `x2` is not a unit. The actual Question 8 explicitly places the ideal in a polynomial ring. Proposition 2.1 similarly uses a polynomial ring; localization at the origin appears only in its threshold/reduction conclusion. The Laurent ring in Theorem 2.4's proof is an intermediate device for proving a rank statement under the additional regular-sequence hypothesis. It is not a replacement for the question's minimal-generation setting.

Theorem 2.4 assumes a monomial-free binomial part generated by a regular sequence; it can also include specified monomial generators in the total ideal. In the pure-binomial case its proof establishes full column rank `rank A=2r`, so every fiber is already singleton. Our matrix has rank five rather than six. In particular this example does not meet that additional hypothesis. Theorem 3.1 treats the canonical generators of defining ideals of space monomial curves in three variables with the stated numerical-semigroup hypotheses. A generic two-by-three determinantal ideal in six variables is not such a space-curve ideal.

Example 3.2, pp.14–15, further shows that one bad optimizer can coexist with a good optimizer. Its bad optimizer therefore is not a counterexample to the existential condition. The candidate correctly proves failure for *all* of its optimizers instead.

## LaClair program distinction

In the actual v2 preprint, the allowed vertex subsets contain the full three-vertex set. Program (8) imposes a subset bound on the sum of the two weights of all edges within a subset: at most the subset size minus one. For the triangle, the full-subset constraint is therefore total weight at most two. It excludes the candidate's entire optimal face, whose total edge weight is three. The two-vertex subset constraints reproduce the individual edge bounds, while the vertex constraints correspond to monomial-exponent bounds, after adjusting the harmless orientation of the third minor.

Thus LaClair's feasible polytope is a strict modification of the Proposition 5 polytope in this example. Remark 3.15 discusses obtaining an upper bound after removing the extra subset constraints. These are accurate mathematical distinctions in the candidate. They do not establish novelty or demonstrate that later authors explicitly answered the numbered singleton-fiber question. The 2025 publisher version and the Blanco–Encinas context have not been independently read in this bounded source audit and require separate priority/context checks before publication-level claims are promoted.

## Checkable controls and audit limits

The accompanying independent `source_scope_controls.py` reconstructs all exponent and augmented rows, checks rank and kernel, tests exact rational segment/image/alternate-point identities, checks the cyclic inequality directions, distinguishes singleton-fiber semantics from unique point/image semantics, checks the localized syzygy, and verifies exclusion by the LaClair full-subset bound. Its guards explicitly raise errors and remain active with Python optimization. Normal and `-O` runs both execute 810 guards, including 81 distinct rational parameters and 125 cyclic-grid controls. Deliberate false-guard runs must fail in both modes. The actual process receipts include executable arguments, child PIDs, exit codes, complete small outputs and body hashes.

These controls support the written unrestricted proofs; finite samples do not prove the complete face, minimality, or absence of monomials. The source record's dated literature assessment and the candidate's bounded search are hypotheses for a later priority audit. This review certifies no original-openness or absolute-first claim. It made no new central proof attempt and changed no original body, shared status, Git index/reference, PR, publication service, or tracker.

**Mandatory scope findings: none. Source gate completion: 100%. Novelty/publication gate: not evaluated.**
