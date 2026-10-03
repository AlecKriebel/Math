# Source, scope, and prior-work audit

Problem 10900004 / AMR-108-0004. Checked 2026-10-03 UTC.

## Original target

The requested entry was attempted at https://www.unsolvedmath.com/problems/10900004; retrieval was unavailable. The selected record and prior report were recovered from the campaign's pinned dataset, then checked against the original source rather than treated as authoritative.

The source is Delp--Hoffoss--Manning (eds.), *Problems In Groups, Geometry, and Three-Manifolds*, https://arxiv.org/abs/1512.04620, **Question 1.4 on PDF page 1**. The rendered page and extracted text agree. It asks about gluing two figure-eight exteriors by an unspecified homeomorphism, and explicitly distinguishes the known identity-double case. The intended residual is arbitrary gluing, not existence for some gluing. The adjacent Question 1.5 asks the broader hyperbolic-JSJ question.

## Corrections to the prior imported report

- The source location is **1.4**, not 1.1.
- The Ballas--Danciger--Lee preprint is **arXiv:1508.04794**, https://arxiv.org/abs/1508.04794. The previously given 1510.07739 is an unrelated paper on Kapustin--Witten and Vafa--Witten equations, as verified at https://arxiv.org/abs/1510.07739.
- The unknown matching condition is not an established necessary-and-sufficient criterion for *all meanings of convexity* without additional geometric hypotheses. Its proved use here is a sufficient construction theorem for properly convex pieces with principal boundary. Failure of a selected model is not nonexistence of all structures.

## Primary literature checked

1. **Ballas--Danciger--Lee (2018)**, Geometry & Topology 22, 1593--1646, https://doi.org/10.2140/gt.2018.22.1593; publisher PDF https://msp.org/gt/2018/22-3/gt-v22-n3-p08-p.pdf. Read Theorems 1.1, 1.3--1.5, Remark 3.3, Sections 5--6, and Section 7's hypotheses and peripheral formulas. Visual check of printed p. 1598 confirms equation (1-1) and Theorem 1.4. Relevant locations: pp. 1594--1599, 1609, 1622--1633, 1635--1642. Theorem 7.5 is conditional, not an arbitrary-gluing assertion.

2. **Benoist, A survey on divisible convex sets**, Theorem 4.1, author's PDF https://www.imo.universite-paris-saclay.fr/~yves.benoist/prepubli/06beijing.pdf. Verified the equivalence between strict convexity and word hyperbolicity for a discrete group dividing a properly convex domain. The closed-quotient assumption matters.

3. **Ballas (2015), Finite Volume Properly Convex Deformations of the Figure-eight Knot**, https://arxiv.org/abs/1403.3314, DOI https://doi.org/10.1007/s10711-015-0043-2. Abstract checked. This supplies finite-volume deformations of the open knot complement, not a statement that every prescribed torus gluing works. No stronger inference from the unread full paper is used.

4. **Ballas--Casella (2021), Gluing equations for real projective structures on 3-manifolds**, https://arxiv.org/abs/1912.12508; DOI https://doi.org/10.1007/s10711-021-00641-y. Abstract and paper introduction checked. Their equation/inequality framework is a candidate computational tool; no calculation in this package solves those global equations for an arbitrary `A`. Their figure-eight-*sister* example is not the exact figure-eight gluing target.

5. **Islam--Zimmer (2024), Convex co-compact representations of 3-manifold groups**, https://arxiv.org/abs/2009.05191, https://doi.org/10.1112/topo.12332. Read Theorem 1.3 and the introduction in the primary full text. This is a necessary topological restriction on manifolds already admitting such representations. Reversing its implication would be invalid. The glued figure-eight family has the permitted hyperbolic-piece topology, which does not establish existence.

6. **Button (2014), A 3-manifold group which is not four dimensional linear**, https://arxiv.org/abs/1210.3068. Primary abstract checked. Its counterexamples are graph manifolds. They are not counterexamples in the present family of hyperbolic pieces, so no claim is transferred from them.

7. **García--Porti (2025), Projective deformations of hyperbolic 3-orbifolds with turnover ends**, https://arxiv.org/abs/2503.20395, and **Monroe (2026), Branched Bending in Finite-Volume Hyperbolic Manifolds**, https://arxiv.org/abs/2604.22004. Primary abstract-level checks were included in the current-literature scan. Monroe studies a deformation mechanism and a Borromean-rings infinitesimal example. Neither checked abstract states the required all-gluing result. We do not claim exhaustive review of their full proofs.

The author's current research pages and searches for the exact problem, glued figure-eight exteriors, arbitrary gluing, and convex projective hyperbolic-JSJ manifolds were also checked. No complete resolution was located. This is a bounded literature audit, not a certification that no later or obscure result exists.

## Duplicate and repository checks

- The live `main` queue was checked and records this target at rank 508, queued 0/5 at the time of inspection.
- Repository file and all-state PR searches used the numeric ID, AMR code, `figure-eight`, and `Danciger`; no mathematically identical attempted target was returned. A looser `figure`/`eight` query returned an unrelated graph-theory PR, which was rejected as a false match.
- The ID branch search was empty. The exact attempt-directory request returned 404, and the complete main attempt-directory listing had 47 entries with no 10900004 entry.
- The available `state.json` and `review_v2/related_target_groups.json` contained no entry under this ID or the relevant name searches. Recursive-tree retrieval failed with a transport error; this limits repository-wide negative conclusions.
- A selective search of the pinned source records found **10900005 / AMR-108-0005**, the strictly more general hyperbolic-JSJ problem. It shares the geometric mechanism but is not an already attempted duplicate or a separate result settled here. Other text matches concerned geometric triangulations, projective configurations, or tropical geometry and were not mathematically equivalent.

No same-target prior attempt was located by these checks. The work proceeds as a new bounded attempt, without treating the literature's known double as a new result.

## Scope and provenance

The mathematical output consists of original exposition, elementary reductions, and explicit finite matrix examples. Imported geometric theorems are attributed in RESULT.md. The diagonal examples are peripheral models only; they are not certified holonomies of the figure-eight group. No priority claim is made.

Original PDFs, complete extracted sources, source-corpus records, screenshots, private working material, and complete connector responses are excluded from the public package. Only authored summaries, proofs, exact verifier code, and its compact output are eligible for publication after fresh audit.
