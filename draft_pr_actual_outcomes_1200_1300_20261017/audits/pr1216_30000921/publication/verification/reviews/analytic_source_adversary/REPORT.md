# Fresh analytic and source-scope adversarial report

**Verdict: PASS. No mathematical repair is required for the submitted claim or its stronger stated extensions.** This is a fresh, candidate-aware internal AI review. It does not establish novelty, firstness, current openness, external peer review, or formal certification. The strongest verified conclusion is the analytic negative answer: there is an entire differentiation-hypercyclic F for which the pointwise product zF is not hypercyclic. For each fixed nonconstant complex polynomial p, such failures are dense in H(C); one F also defeats all positive monomials; precisely the nonzero constant polynomials preserve every hypercyclic entire function.

## Reviewed identity and independence

The submitted eight-file inventory and its seven non-self hashes pass a fresh closed-set check. The distributed bindings in ACCEPTANCE.json match the actual submitted bytes. In particular:

| Item | Bytes | SHA256 |
|---|---:|---|
| PROOF.md | 13407 | `3479117bbe24e0829a31a9ac616c305028ad571aa41647d28b3e7016311f8fe6` |
| AUDIT.md | 16032 | `c4b060d33bb10e3cb19f0c7d53afe6a5c788d918954733ecec544734bfdc78b6` |
| MANIFEST.json | 1341 | `924c78d491b208b29ebcbc1e1308b7b4d3a2f5f90255ccf62af481a10eadfc10` |

The assigned current head `3ee95e0e22a7bb21d7d08e3c4dcd40f60dfd47c3` is parent-supplied context, not an independently checked Git fact in this family. No Git command, index/checkout mutation, candidate edit, other family's work, or candidate/source program was used. All output is confined to this review folder. Source bodies and modest page renders are under its ignored `sources/` directory. No outreach occurred.

The original-document hashes, omitted historical packets, receipt counts, and old acceptance in the submitted metadata are historical claims. This review verifies the current distributed documents, supplies fresh independent computations and fresh source retrievals, and does not authenticate or replay the omitted historical evidence. The difference between `accepted_original_documents` and `distributed_document_bindings` is explicit metadata, not a failed current binding. Mathematical text is assessed directly without relying on the previous audit's acceptance.

## Source gate

Fresh retrieval from the [2008 publisher PDF](https://ems.press/content/serial-article-files/46147) confirms the target at printed 330/PDF 34. I read PDF pages 32-35 and visually inspected page 34. Definition 4 uses density of all derivatives in H(C), including order zero. Question 5 concerns the pointwise product pf for arbitrary hypercyclic f and nonconstant p. Theorem 6 has a residual positive class with all nonzero polynomial multipliers. It does not assert the universal claim posed in the question. The manuscript addresses the correct operation and quantifiers; neither polynomial composition nor p(D) is substituted. The surrounding universal-Taylor-series questions concern a different function class. DOI: [10.4171/OWR/2008/06](https://doi.org/10.4171/OWR/2008/06).

Freshly retrieved PDFs match every submitted historical whole-PDF hash:

| Source | Bytes | SHA256 | Fresh inspection |
|---|---:|---|---|
| Costakis 2008 | 420658 | `9bd27d84931841479eaf5e0915e4a99e720c4c135a7d57c97dff43e4687d03a5` | Text 32-35; visual 34 |
| Costakis 2010 | 283107 | `ee55f0f14a36216e03533bf568976f9bc83c6d7ef68f3ac8dcecfdc8371d96ae` | Text 5,21,22; visual 5 |
| Bernal-Gonzalez et al. 2018 | 171692 | `7093a8989e3f5da15db5ff82cb0d158fb67c74c72bbd9cc1b5e8687dc8a01e43` | Text 1-3 |

The [2010 publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/90964) states in Theorem 1.7, printed 207/PDF 5, residual common hypercyclicity for the sequences n^b D^n over all real b. The inspected Section 6 splits positive/negative b. This generic assertion does not concern every hypercyclic function. Its proof is not needed for the candidate and was not fully audited here.

The [2018 publisher PDF](https://jot.theta.ro/jot/archive/2018-080-001/2018-080-001-011.pdf), introduction pages 1-3, distinguishes P composed with f, convolution operators Phi(D), selected multiplicative groups, and composition-operator hypercyclicity. Those statements do not supply universal preservation by an independent-variable multiplier p(z). The submitted description stays within this scope. No exhaustive literature or priority search was attempted.

## Infinite analytic audit

**Baire existence and density.** A standard metric from the integer-radius disk seminorms makes H(C) complete: limits on successive disks agree, and locally uniform limits are entire. Taylor truncations and rational-complex coefficient approximation give a countable dense polynomial set. A Cauchy estimate on a larger disk proves continuity of each derivative. Thus all U(j,r,s) in the candidate are open. Their density is correctly witnessed by Q+I_n P: the normalized primitive has derivative P, tends to zero on each fixed disk by factorial domination, and n can simultaneously exceed deg Q and meet any neighborhood constraint. Baire's theorem yields a dense intersection; a two-step target approximation shows each member's orbit dense on every compact set. There is no appeal to an unverified explicit starting function.

**Dense tails and perturbation.** A nonempty open subset contains infinitely many distinct small constant translates. Removing finitely many orbit values leaves a nonempty open set, since finite subsets of this Hausdorff space are closed. Therefore every derivative tail is dense, even if values repeat. Tail density produces strictly increasing n_j with approximation on radius-j disks to error 1/j. If D^n h tends locally uniformly to zero, addition along the same subsequence preserves every target limit. The proof uses this special null orbit condition, not openness of HC(D).

**Coefficient lemma, arbitrary compact sets.** For bounded c_k tending to zero, the series with derivative-normalized coefficients c_k is normally convergent, and its n-th derivative has coefficients c_(n+k). On a disk centered at alpha its norm is bounded by exp(R) times the tail supremum. For any compact K choose R with K contained in that disk; the same bound proves uniform convergence on K. This also justifies termwise differentiation at every order. There is no growth assumption on the starting coefficients a_k beyond f being entire.

**The z construction.** The replacement works for complex a_k and at threshold equality. The actual bound is 2/(k+1), which is sufficient and tends to zero; an unjustified factor-one bound is not used. Every positive-order derivative of zF evaluated at zero has modulus at least one. Its zeroth derivative evaluates to zero. Both kinds of values have distance at least 1/2 from 1/2, so the open evaluation disk of radius 1/4 is missed by the whole orbit. This is a continuous-functional obstruction to density. It proves the negative answer for an admissible p, rather than merely an eventual or finite obstruction.

**Simultaneous positive monomials.** For fixed m>=1, derivatives of order n<m vanish at zero. At n>=m, direct multiplication of ordinary Taylor coefficients gives n!/(n-m)! times b_(n-m). The lower bound is n!/((n-m)!(n-m+1)); after writing n=k+m, it becomes the product of k+2 through k+m, with empty product one for m=1. Hence the same F and the same missed open set work for every positive integer m. No simultaneous claim for arbitrary nonconstant polynomials follows or is asserted.

**Arbitrary fixed polynomial, root multiplicities, and complex recursion.** Fix p first. A root alpha has multiplicity 1<=m<=d, and its shifted expansion has q_m nonzero. At stage k the only newly available normalized coefficient in derivative order k+m is c_k, with nonzero coefficient A_k=q_m (k+m)!/k!. All higher polynomial-degree terms use correction indices between zero and k-1. This proves well-founded triangular recursion, including k=0, m=d, missing q_j terms, nonreal roots and coefficients, and large cross terms. The exact Taylor-product identity uses n!/(n-j)! because the function coefficients are normalized by (n-j)!, whereas q_j are ordinary polynomial coefficients.

If |S_k|>=eta, zero correction preserves the barrier. If |S_k|<eta, complex division by A_k sends the entire derivative value exactly to the positive real eta. The triangle inequality bounds |c_k| by 2eta/|A_k| regardless of the size of earlier corrections or of the other q_j. Later corrections have indices greater than k and cannot alter the locked derivative. At equality zero correction works. All orders below m vanish, and every later order has modulus at least eta; the evaluation disk centered at eta/2 with radius eta/4 is therefore missed, including order zero.

**Null orbit and eta uniformity.** Set r_k=k!/(k+m)!. For m>=1 this decreases to zero and r_k<=1/m!. Consequently

    sup_K |h^(n)| <= (2 eta exp(R)/|q_m|) r_n,
    sup_K |h| <= 2 eta exp(R)/(|q_m| m!),

whenever K is in the alpha-centered radius-R disk. These bounds are uniform over the recursion's branches and its dependence on eta. For every fixed positive eta they prove the null orbit and hypercyclicity of F=f+h. For an arbitrary neighborhood of f, put its finitely many compact constraints in one such disk and select eta small enough before running the recursion. No continuity of the coefficients in eta is assumed, no exchange of limits is used, and eta=0 is never needed. Uniformity over varying p, q_m, alpha or neighborhoods is neither claimed nor required.

**Density and constants.** Every neighborhood of every f in HC(D) contains the asserted F. Since HC(D) is dense, each fixed-p failure set is dense in all H(C). The order is forall fixed p, forall f, forall neighborhoods, exists F. The proof does not exchange this with existence of one F for all p, nor claim every f fails. A nonzero constant multiplier is a homeomorphism commuting with differentiation; zero fails since HC(D) is nonempty. This completes the exact classification. A dense exceptional set is compatible with a residual positive class; no category contradiction exists.

## Fresh exact diagnostics and controls

`exact_checks.py` is independently written with only standard-library imports and exact Gaussian-rational arithmetic. Product checks convolve ordinary Taylor coefficients; additional checks translate to the global variable, multiply, differentiate, and evaluate at a nonreal root. These finite calculations are subordinate to the preceding infinite analytic proof. The finite test inputs are not claimed to be hypercyclic functions.

All three interpreter modes, normal/-O/-OO, produced byte-identical PASS receipts. The program uses explicit exceptions, not removable assertions. Each mode covered 6,048 z replacements including 432 equality cases; 135 fixed-polynomial cases with 1,620 recursive steps, 675 corrections and 945 retained values; 8,910 checks that locked derivative values stay unchanged; 2,025 translated-global product checks; low orders and multiplicities 1-5; q_m imaginary or complex and some higher q_j zero; eta as small as 10^-6; monomials m=1-7; and 4,800 factorial-tail monotonicity checks. All detailed counts are in the receipt.

Five invalid variants were rejected on explicit fixtures in every mode: omit clipping, drop the z-product factor n, drop a higher-degree polynomial cross term, reverse the factorial-tail inequality, and center an excluded orbit neighborhood at zero while ignoring order zero. A separate m=0 control records the absence of factorial decay, confirming why nonconstancy/root multiplicity is essential to this route.

Final `exact_checks.py` SHA256: `f1b9faee5fa6dbd27fa0abe7b5c9d5a6a5d1373c9f28718b372dbcb6d3a5cbd1`.
Each 1,671-byte exact receipt SHA256: `6784d07d8a101b67172134cd11725f2f082af733635a70f32e188b463b0e9e35`.

Reproduce the finite diagnostics with `python3 exact_checks.py`, `python3 -O exact_checks.py`, and `python3 -OO exact_checks.py`. Recheck current submitted bindings with `python3 integrity_check.py`. `retrieve_sources.py` retrieves the three publisher PDFs, records their hashes, extracts only stated relevant pages, and renders only two pages into ignored `sources/`. `source_receipt.json` records fresh retrieval details. `EVIDENCE.json` binds this family's current non-source artifacts.

## Remaining gap and repairs

No analytical gap or required mathematical repair was found. The counterexample and each stated extension pass this review. The exact remaining boundary is historical: neither novelty nor present-day openness is established, and historical omitted computational/integrity receipts remain historical metadata. No claim about all polynomials failing for one common F is promoted. No candidate file was changed.
