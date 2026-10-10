# Rational and integral completely positive factorizations

## Result and scope

UnsolvedMath 30003649, OWR-15957-002, rank 737. Checked 5 October 2026.

Both questions in the primary 2017 formulation have prior resolutions. The rational question has a negative answer in Sidney Holden's public 13 September 2026 manuscript. Its finite certificate was independently checked here, including a newly written exhaustive facet enumerator. The integral question asks specifically about order two, and has an affirmative published answer by Thomas Laffey and Helena Šmigoc (2018).

This package is a verification and scope report. It claims no new solution, priority, external human peer review, or newly run formal proof-assistant verification. The rational source is a public repository manuscript, not a verified journal publication. A fresh uninvolved audit of this package is still required before publication.

## Exact primary target

Abraham Berman's contribution to *Copositivity and Complete Positivity*, Oberwolfach Report 52/2017, printed page 3082 (PDF page 12), gives two questions:

1. For every positive integer n and rational symmetric A admitting A = BBᵀ with a finite entrywise nonnegative real n-by-m matrix B, must there be some finite-width entrywise nonnegative rational factor?
2. For n = 2 and integral A admitting such a real factor, must there be a finite-width entrywise nonnegative integral factor?

No bound on m, nonsingularity requirement, denominator limit, scaling permission, or interior assumption is part of either question. The second question does not quantify over all matrix orders. The original page explicitly lists the rational interior case among known affirmative cases.

Source: [official OWR PDF](https://ems.press/content/serial-article-files/46715), DOI [10.4171/OWR/2017/52](https://doi.org/10.4171/OWR/2017/52). The relevant page was inspected as both extracted text and an image. The UnsolvedMath page itself returned HTTP 403 in direct retrieval; that route was not bypassed. The source mapping was recovered through the supplied catalog descriptor and independently checked against the official primary report.

## Rational question

The counterexample has order 444, integral strictly positive entries, ordinary rank seven, and real cp-rank seven. It has no rational nonnegative Gram factor of any finite width. Singularity puts it on the boundary of the completely positive cone in the full symmetric-matrix space; entrywise positivity does not put it in the cone's interior.

The exact witness is A = RRᵀ, where R is the signed integer 444-by-7 array in the pinned public source. The nonnegative real factor is RO, where O is an orthogonal matrix over the real cubic field Q(∛2). The signed factor R itself is not a nonnegative rational factor.

[Holden's proof and certificate record](https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/412489c6c52f49653bf069ac2f85e92034cdbfa5/references/holden-pf03-2026-09-13) supplies the complete witness. The present package supplies an independently written verifier and the mathematical interface proof in PROOFS.md. The pinned source files were re-retrieved at the immutable commit and matched the initially inspected bytes.

Actual new checks:

- Exact cubic-field orthogonality, symmetry, trace zero and the Cayley identity
- Seven rational coefficient matrices of rank three
- Seven local positive-semidefinite restrictions with precisely the required one-dimensional kernels
- Positive exact barycentric coordinates and a positive rational pointing functional
- All 189 strict cross-block generator pairings
- All 54,264 six-generator candidate supports, with 444 supporting facets and no rank-deficient subsets
- Exact equality of the regenerated complete facet array to the public R and incidence data
- Rank R = 7; 2,966 positive entries and 142 zero entries in RO
- Every one of the 98,790 stored lower-triangular integer Gram entries; all are positive
- Five corruptions rejected: orthogonal factor, trace, generator, missing facet and expanded Gram entry

The computations used only Python integers and fractions. Downloaded source programs and old success logs were not executed or used as proof inputs. Finite data checks are combined with the all-width mathematical argument; a finite search over possible factor widths would not suffice.

The public repository separately records a Lean formalization by George Stepaniants with a narrower witness scope but the same universal negation. This run did not compile or audit that Lean project, and does not rely on its status claim.

## Integral question and countercontrols

Laffey and Šmigoc prove the order-two assertion in *Integer completely positive matrices of order two*, Pure and Applied Functional Analysis 3 (2018), 633–638; [primary preprint](https://arxiv.org/abs/1802.04129). The paper explicitly cites the OWR question. The 2021 paper *A simplex algorithm for rational cp-factorization* gives another proof: [primary preprint](https://arxiv.org/abs/1807.01382).

PROOFS.md gives a short all-input descent proof, accompanied by an exact implementation. Its 100,161 integral positive-semidefinite triples with all entries between 0 and 60 passed; these finite controls corroborate, rather than replace, the proof.

The distinction from higher order is necessary. The matrix with rows (2,3,1), (3,5,3), (1,3,5) has a four-column nonnegative rational Gram factor and no integral Gram factor of any width. Its explicit factor and unrestricted-width obstruction are proved in PROOFS.md. This is a known example, recorded in Berman and Shaked-Monderer's [2025 survey](https://cot.mathres.org/issues/COT202523.pdf), Example 3.2; it is not a new counterexample.

That survey still presents the general rational boundary problem as open, while confirming the order-two integral theorem. The 2017 interior result ([primary preprint](https://arxiv.org/abs/1701.03148)) and the later generalized-perfect-matrix framework ([2026 paper](https://arxiv.org/abs/2602.05841)) do not turn rational approximation into exact factorization of every boundary point.

## Scaling and width

The rational question permits arbitrarily many columns. For example, the scalar matrix [2] lacks a one-column rational factor but has the rational two-column factor [1,1]. This rules out using a nonsquare scalar or failure at minimal real cp-rank as a counterexample.

A rational nonnegative weighted sum of rational rank-one generators is equivalent to an unweighted rational Gram factor when width is unrestricted. Rational factorability is also invariant under multiplication by a positive rational scalar. Thus Holden's counterexample cannot acquire a rational nonnegative factor, or an integral nonnegative factor, after multiplying by any positive rational scalar. These equivalences are proved in PROOFS.md. They do not imply that an integral A with a rational factor already has an unscaled integral factor.

## Prior-attempt search and stopping decision

The exact problem ID was searched in the actual AlecKriebel/Math indexed files, all-state pull requests and branches. No exact-ID match was returned. A direct read of the standard attempt README returned 404. Searches for the subject found no matching prior attempt; broader matches were unrelated. This is a bounded repository search, not a claim to have exhausted all private histories or proved novelty.

One substantive approach was used: recover the primary target, check later primary literature, then independently verify the located prior resolution. The early stopping condition is met. No additional attempted original solution is warranted. Neither minimum counterexample order nor the classification of each smaller order is asserted.

## Reproduction and release scope

Use README.md for commands and pinned input URLs. Source PDFs, their extracted text, the downloaded matrix/certificate datasets, and private coordination material are deliberately absent from this safe package. Public source hashes, byte counts, match results and inspection metadata are present. No remote repository write, branch update, commit, push or PR was performed for this task.
