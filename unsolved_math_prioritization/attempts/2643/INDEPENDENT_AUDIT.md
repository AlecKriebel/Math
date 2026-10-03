# Independent source and proof-scope audit: KOU-21.134 / 2643

Verdict: **PASS** for an attributed, already-resolved source certificate covering both parts. No mandatory mathematical or source correction found. This is an independent AI audit, not human peer review, proof-assistant verification, or an independent enumeration of either finite group.

Audit date: 2026-10-03 UTC.
Frozen author manifest SHA-256: `e8733976bfb8e9404a2f309eff6a3f465bdd421f51345397f4044f9211c48541`.
All six payload file sizes and SHA-256 hashes match that manifest; together with the manifest this is the specified seven-file author package. No author file was modified. No remote write or new author attempt was made.

## 1. Primary-source checks

- The live [October 2026 announcement](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/) links to the [October Notebook PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf#page=197). The problem and update are on both PDF page 197 and printed page 197; the existing fragment is correct.
- The page explicitly stars 21.134, records negative answers to both questions, credits J. G. Thompson, cites Li–Shi in Ricerche di Matematica 74 (2025), 559–563, and records Vasil'ev's letter of 18 May 2026. The exact finite-group power-equation target was checked against the certificate. It is not 21.137.
- The [versioned Li–Shi preprint](https://arxiv.org/pdf/2303.09460v1) was checked as extracted text and visually on pages 2 and 4. Page 2 attributes the pair to Thompson; Theorem 9 on page 4 identifies the groups and reports MAGMA-derived exact-order counts. The subscript in L_3(4):2_2 is visually unambiguous, and every imported count agrees.
- The [arXiv record](https://arxiv.org/abs/2303.09460) confirms v1 submission on 15 March 2023, at 00:15:31 UTC. Some secondary search results show the announcement date instead; the package's submission date is correct.
- The [Springer publisher record](https://link.springer.com/article/10.1007/s11587-023-00835-4) independently confirms authors Yu Li and Wujie Shi, title, DOI, volume 74, pages 559–563 (2025), online publication 16 December 2023, and issue date February 2025. Full journal text was not accessed. The package accurately identifies the authors' preprint as the detailed theorem source.
- The [ATLAS M23 page](https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/M23/) independently lists L_3(4):2_2 and 2^4:A_7 among the maximal subgroups, each of order 40,320. The [ATLAS L3(4) page](https://brauer.maths.qmul.ac.uk/Atlas/v3/lin/L34/) gives order 20,160 and the outer automorphism group. These corroborate the exact extension notation and order; no unverified mapping between alternate a/b/c and numerical involution labels is needed.

The local source-PDF hashes agree with the certificate:
- Notebook: `31baec1b36ec3a956e787355eccfffa2e89df5b1fe31b22a3123377d8103baab`.
- Li–Shi v1: `a2bb1359b9f184f0faab173fc9a18178191d8b70841f7cd98e9179ecfc7e7068`.

## 2. Exact-order and all-positive-integer checks

The imported vector, indexed by 1, 2, 3, 4, 5, 6, 7, 8, 14, is
`1, 435, 2240, 6300, 8064, 6720, 5760, 5040, 5760`.

Independent arithmetic gives total 40,320 and least common multiple of supported orders 840. The order formulas give |A_7| = 7!/2 = 2,520 and |PSL_3(4)| = 4^3(4^3-1)(4^2-1)/gcd(3,3) = 20,160. Thus both displayed group orders are correct.

The package's checker ran successfully and its stdout was byte-identical to verification.json. Separately, an independently entered vector was processed with SymPy divisor, Möbius, and totient functions:
- Möbius inversion recovers the vector, including all zero entries, on all 96 divisors of 40,320.
- Every exact-order count is divisible by the corresponding Euler totient.
- For all 96 divisors n of the group order, the computed power-equation count is divisible by n (the standard Frobenius necessary condition).
- All 32 exponent-divisor values agree with the reported values. The gcd reduction also passes a redundant numerical sample for n = 1 through 100,000.

The all-n conclusion rests on the proof, not those finite samples. For every positive integer n, x^n = 1 if and only if the exact order of x divides n. Hence t_X(n) = sum_{d|n} a_X(d). Equal exact-order distributions imply equal power-equation counts for every n. Since every supported order divides 840, d|n is equivalent to d|gcd(n,840), yielding the stated finite representation without weakening the quantifier.

All these computations are consistency tests of imported data. They do not establish by independent construction that the two groups have that data. Li–Shi's published computation remains an explicitly credited input.

## 3. Structural deductions and proof scope

For G = V:A_7, V is an elementary abelian normal subgroup of order 16, so V <= R(G). The image of R(G) in the quotient A_7 is solvable and normal. Simplicity and nonsolvability of A_7 force that image to be trivial, and therefore R(G) = V. This deduction needs the stated quotient and normal subgroup, not a separate computation of the A_7 action's faithfulness. In particular, the certificate does not silently infer the radical merely from the colon symbol.

For H, S = PSL_3(4) is nonabelian simple, and the cited ATLAS outer extension is an almost simple group. The specified nontrivial outer involution yields a faithful embedding of S:C_2 into Aut(S): conjugation is faithful on the centerless S, and no element in the nonidentity outer coset can act as an inner automorphism. Thus the asserted inclusion S <= H <= Aut(S) is the relevant structural input, rather than an arbitrary semidirect product with a possibly trivial action.

If N = R(H), then N intersect S is a solvable normal subgroup of S, hence trivial. Since both N and S are normal in H, their commutator is contained in that intersection. Thus N centralizes S. The certificate correctly proves that C_Aut(S)(Inn(S)) is trivial for centerless S, giving N = 1. No circular use of the desired radical conclusion occurs.

These radical orders are distinct isomorphism invariants. The one pair therefore refutes (a), because equal type fails to preserve trivial radical, and (b), because a group sharing the almost simple H's type need not be isomorphic to H. The source certificate does not need the preprint's later Burnside-ring argument, and this audit has not certified that unrelated argument. Neither group is solvable, so this pair makes no solvable-versus-nonsolvable claim about the separate original Thompson question.

## 4. Disposition and repairs

- Recommended disposition: already_solved; both answers negative; credit Thompson, as documented by Li–Shi and the Notebook.
- Substantive proof-attempt charge: 0. No mathematical novelty claimed.
- Mandatory repairs: none.
- Optional precision improvement in a future version: add the publisher-record online/issue dates and the independent ATLAS corroboration, while preserving the distinction between the journal metadata and preprint theorem text. This is not required for PASS.
- The frozen metadata's review-pending field accurately records its preparation state. Record this audit separately rather than silently editing a frozen package.
- The exact unsolvedmath catalogue's live status was not established by this audit. The editor-authored resolution and explicit counterexample are sufficient for the mathematical disposition; do not claim that the external catalogue has been corrected.
