# Independent review: canonical basepoints, problem 11000020

Date: 2026-10-03. Target: rank 421, AMR-109-0020, Farb Problem 2.19.

## Verdict

**PASS for the scoped, credited negative answer to the nilpotent uniqueness example.** No mathematical defect requiring an author revision was found in that certificate. The four genus-9 surfaces are supported by the cited primary classification, their full automorphism groups are nilpotent of order 128, and 128 is the universal nilpotent upper bound in genus 9. The conclusion is a consequence of prior literature, not a new discovery.

**The cited positive criteria also supply actual instances of the broader request to find other properties.** Their genus restrictions must remain visible, but those restrictions do not by themselves identify a missing requirement: Farb does not explicitly ask for one uniform criterion covering every genus or an exhaustive classification of all such properties. No further finite mathematical obligation can be extracted from the exact wording with confidence. This review therefore does not declare the full response partial merely because an open-ended research programme has not been exhausted.

A scoped `already_solved` / prior-literature-response disposition is defensible for the concrete record: prior work answers the explicit yes/no example and provides the requested kind of positive criteria. It must not be described as a new discovery or exhaustion of the entire canonical-basepoint programme. A coordinator may instead preserve a qualified status if the repository's labels cannot express that scope, but this is an administrative choice, not a mathematical defect or an established remaining subproblem.

The frozen count remains 1/5, and this independent review does not consume an author turn. There is no proof-audit basis to require four more author turns on an unspecified stronger target. If an independently established user requirement really demands a further genuswise/uniform construction, that requirement should be stated explicitly before treating its absence as a gap. No further author proof search is needed for the nilpotent example.

## 1. Exact input and integrity

- Repository: AlecKriebel/Math.
- Author branch supplied: `math/11000020-canonical-basepoints-prior`.
- Immutable commit reviewed: `1792dcf4b4a04fc072d6f311cb349de6c1c5052a`.
- Remote directory: `unsolved_math_prioritization/attempts/11000020`.
- Input manifest SHA-256: `441c21fe437955edfaedf0a13f32c25115d1ce1cc0f849c2e4a5b8c1b3941794`.

All nine local packet files were checked against the immutable remote directory's Git blob hashes and byte counts. All eight files bound by the author manifest match their SHA-256 and byte counts; the manifest itself matches the requested freeze. All six PDF sources match the author's source manifest. The author packet was not modified. This review creates only a separate local review directory. No remote write or pull request was performed.

The author verifier was read and rerun. Its 69 assertions pass, and its JSON output exactly reproduces the saved verifier output. It correctly says that it does not reproduce the MSSV classification. Independent controls described below pass 115 assertions.

## 2. Primary source and scope

Farb's author-book PDF page 30, printed page 23, was inspected as a page image and by fresh extraction. Problem 2.19 requests automorphism-theoretic properties selecting a unique point of M_g and offers nilpotent maximal-order uniqueness as its example. The full automorphism group is the natural interpretation of the example's wording. The packet's explicit full-group optimization is therefore faithful.

The following paragraph about Hurwitz surfaces is introductory text for Question 2.20. It is not an additional counting task in Problem 2.19. The source boundary is visibly clear. The imported problem JSON merges that lead-in paragraph into its statement; the packet correctly repairs the scope by going to the primary source.

The live UnsolvedMath page was not independently retrieved in this review. That does not block this mathematical audit because the precise primary problem page was inspected. Nor does this review independently rerun every historical branch/PR search in SOURCE_GATE.md; those administrative negative searches are not premises of the counterexample.

Source: [Farb, Problem 2.19, page 30](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=30).

## 3. Existence, fullness, and distinctness

The original MSSV v1 PDF was inspected at section 1.5 (group-ID convention), sections 7.1–7.2 (meaning of the loci and rows), and Table 4. The v1 section 7.2 page and genus-9 table page were also inspected visually. Fresh PDF extraction checks repeat the decisive locations. The same relevant entries were checked in v2.

The crucial source statement in section 7.2 is explicitly an existence assertion for a curve with G as its full automorphism group. It is stronger than merely listing groups that can act. Section 7.1 defines the starred loci using existence of a full-group point on the component. In dimension zero, that distinction cannot hide an exceptional point with larger full group. More importantly, the packet needs only the explicit existence assertion for each group-signature pair, so it does not rely on delicate generic-point reasoning.

The table's genus-9, dimension-zero rows 5–8 list `(128,138)`, `(128,136)`, `(128,134)`, and `(128,75)`, all with branch orders `(2,4,8)`. Large-group actions here have quotient genus zero; writing `(0;2,4,8)` restores the convention correctly. Section 1.5 explains that the first ID entry is the group order and the second indexes the group among groups of that order.

Distinct fixed-order library IDs identify nonisomorphic abstract groups. An isomorphism of compact Riemann surfaces conjugates their full holomorphic automorphism groups, so surfaces with these four full groups cannot represent the same moduli point. Thus the packet is not mistakenly counting distinct actions on one curve or blindly counting Hurwitz-space components. Its modest claim of at least four points is justified.

Each full group has order 2^7 and hence is nilpotent. The source need not additionally label the groups nilpotent. No explicit equations or fresh group presentations are needed for this source-based existence certificate.

The existence/fullness classification remains a declared literature dependency. Neither the author's arithmetic verifier nor this review reconstructs BRAID computations or independently proves all of MSSV's classification. This is acceptable for a credited prior-result certificate, but would not justify describing the artifact as a self-contained new construction or a formal verification.

Sources: [MSSV v1, section 7.2](https://arxiv.org/pdf/math/0205314v1#page=14), [MSSV v1, Table 4](https://arxiv.org/pdf/math/0205314v1#page=17), [arXiv version history](https://arxiv.org/abs/math/0205314). The version history independently confirms v1 on 30 May 2002 and v2 on 12 July 2024. A fresh web fetch of the v1 PDF encountered a cache miss; the complete local v1 PDF was available, hash-verified, and directly inspected. The current official v2 HTML was reachable.

## 4. Audit of maximality proof

The Riemann–Hurwitz argument in RESULT.md is valid for a finite nilpotent subgroup H acting faithfully on a compact genus-g surface, g at least 2. Finiteness is automatic for such a subgroup of the holomorphic automorphism group. With quotient genus h and branch orders m_i, put

    D = 2h - 2 + sum(1 - 1/m_i),  2g - 2 = |H| D > 0.

The case split is complete:

1. h at least 2 gives D at least 2.
2. h=1 forces at least one branch point when D is positive, giving D at least 1/2.
3. h=0 with at least five branch points gives D at least 1/2.
4. h=0 with four branch points has D=0 when all orders are 2. Otherwise the least positive possible deficit is 1/6, from `(2,2,2,3)`.
5. h=0 with zero, one, or two branch points cannot have positive D.
6. The sole remaining case has three branch points.

For a sorted triple a<=b<=c, elementary reciprocal inequalities justify finite reduction without an arbitrary computational cutoff. If a>=4 the deficit is at least 1/4. If a=3 and b>=4 it is at least 1/6; b=3 leaves only c=4 below 1/8. If a=2 and b>=6 it is at least 1/6; b=5 leaves c=5; b=4 leaves c=5,6,7; b=3 leaves 7<=c<=23. The case a=b=2 is never hyperbolic. Thus the author's 22-item list is exhaustive.

For sphere-three-point actions, branch monodromies x,y,z have exact orders a,b,c and xyz=1. Finite nilpotent groups are direct products of their Sylow subgroups. Every one of the author's four contradictions follows:

- Orders 2 and 3 lie in different commuting Sylow factors, so their product has order 6, excluding `(2,3,c)` for c>=7.
- Orders 2 and 4 lie in the unique Sylow 2-subgroup, so their product has 2-power order, excluding c=5,6,7.
- Commuting elements of orders 2 and 5 have product order 10, excluding `(2,5,5)`.
- Elements of order 3 lie in the unique Sylow 3-subgroup, excluding product order 4 in `(3,3,4)`.

Therefore D>=1/8 and |H|<=16(g-1). In genus 9 this upper bound is 128. Every classified group under consideration attains it, and `128(1-1/2-1/4-1/8)=16=2*9-2` checks the genus. Consequently both the full-nilpotent and nilpotent-subgroup maxima equal 128 in genus 9, with at least four distinct underlying surfaces attaining the bound. No assumed equivalence between these two optimization problems is used.

The cited Schweizer theorem was inspected at PDF/printed page 5. Theorem 2.2 explicitly concerns subgroups of Aut(X), part (c) gives the bound, and its proof cites Zomorrodian's Theorems 1.8.4 and 2.1.2. The source table also says there are no genus exceptions for the nilpotent bound. The packet is transparent that the original 1985 PDF was not retrieved. Its direct bound proof means the certificate does not pretend to rely on inspection of that original proof.

Source: [Schweizer, Theorem 2.2(c)](https://arxiv.org/pdf/1701.00325#page=5).

## 5. Independent controls and adversarial checks

`reviewer_checks.py` is separate from the author's checker. It performs these controls:

- freeze, all local/remote Git blobs, all source hashes, and fresh PDF-page extraction checks;
- sorted triangle enumeration through branch order 100, together with the preceding analytic tail proof;
- a generic Sylow-projection obstruction independent of the author's four hard-coded cases;
- equality and negative controls, other quotient-signature boundaries, and the genus-9 arithmetic;
- exact replay of the author output.

The independent Sylow test projects xyz=1 onto each Sylow factor. If exactly one projected element is nonidentity, the relation is impossible. If exactly two are nonidentity, they are inverse and must have the same order. This necessary condition excludes all 22 positive-deficit triples below 1/8. It is not claimed sufficient for existence.

The numerical equality triples are `(2,3,24)` and `(2,4,8)`. The same test excludes the first and retains the second. The Hurwitz triple `(2,3,7)` is correctly rejected, whereas the Euclidean triple `(2,3,6)` survives the group-theoretic filter but has zero deficit and is correctly excluded from the genus-g>=2 argument. These controls help detect accidental use of a merely numerical upper bound or failure to impose positivity.

The reviewer script initially encountered a PDF-extraction spacing mismatch in the literal string for `16(g-1)`; the extraction check was changed to accept the actual spacing. No mathematical or author-packet change was needed. The final independent run passes 115 assertions and the author replay passes 69.

The script's finite enumeration remains only a control; the analytic tail bounds and group-theoretic arguments establish the universal result. Likewise, source text-presence tests supplement the actual visual/contextual read; they do not prove the published classification.

## 6. Positive examples and the genus-21 exception

The 2025 Reyes-Carocca–Speziali PDF page 5 was checked visually and by fresh extraction. Theorem 3.1 says that the subgroup-existence condition of order 3g characterizes one surface for odd g>=3 except g=21. The even-genus condition of order 3g+3 applies when g>=4 and g is not 2 modulo 3. The theorem immediately explains that uniqueness fails in genus 21. The packet preserves this exception despite its omission from the abstract.

These are existence-of-a-subgroup predicates, not assertions that the full group has exactly the given order. The packet's statement is faithful. Theorem 3.2 indeed allows larger full groups in some of those cases, which is why retaining the subgroup distinction matters.

The Reyes-Carocca 2021 paper was also checked for the rejected family lead: its hypotheses explicitly concern positive-dimensional families, with the one-dimensional maximum 8(g-1). In genus 3 that is 16, while MSSV Table 3 supplies a full order-32 group on `y^2=x^8-1`. Consequently that family could not by itself refute uniqueness of the absolute nilpotent maximum. The packet correctly rejects that inference.

Sources: [Reyes-Carocca–Speziali, Theorem 3.1](https://arxiv.org/pdf/2310.07520v2#page=5), [Reyes-Carocca, Theorem 1](https://arxiv.org/pdf/2004.06506v2#page=3).

## 7. Publication and disposition guidance

No correction is required to the mathematical counterexample before publishing it as a credited source correction. The broad “find other properties” sentence is also served by the correctly stated positive 2025 subgroup-existence criteria. These are genuine automorphism-group properties selecting unique moduli points for the specified genera. No source sentence asserts the stronger requirement that the new criteria cover every genus uniformly. In particular, genus 21 and even genera congruent to 2 modulo 3 are outside those stated criteria, but that fact alone is not an identified failure of a quantified requirement in Farb's problem.

Keep these restrictions:

- State that the explicit nilpotent uniqueness example is answered negatively by prior work.
- Do not claim a new discovery, a least counterexample genus, an exact count of all maximizers, or a new full classification.
- Preserve the classification dependency and the distinction between full automorphism groups and subgroups.
- Preserve the positive theorem's exceptional genus 21 and even-genus restriction.
- Keep the broader-source scope visibly separate in any queue row, README, PR title, and summary.

Suggested disposition: a **scope-qualified prior-literature resolution** is credible. An `already_solved` label can be used if its associated text says exactly that the nilpotent example is false by prior work and that known positive canonical-point criteria are supplied. The review does not certify exhaustion of the research programme, but it also finds no definite remaining requested subproblem that forces a `partial` status or continuation for four further turns. Avoid an unqualified novelty or programme-completion claim under any label.

During review, an initial provisional `partial` recommendation treated programme-completion as an additional requirement. On checking the exact requested remainder, that recommendation was withdrawn: it imposed a stronger target than the source states. The final disposition above supersedes it.

The freeze's existing “independent review pending” text should remain intact as historical input. A later reviewed-state supplement can identify this PASS and its scope without rewriting the frozen input. This is an independent model audit with reproducible controls, not human peer review or formal verification.
