# Independent adversarial review — Zenodo 23430326, version 1.1

Completed 2026-10-24, local review clock 22:58–23:00 PDT. Assigned lane: mathematical falsification and applicability. Completion estimate: 100% of this assigned review; no estimate of worldwide novelty is warranted. The initial independent ledger was sealed before downloaded source-body checks and supplied checker inspection; a prior web search had returned source snippets. Its timestamp correction and this search-result boundary are documented in CUSTODY.md. No sibling report or historical authored review body was read.

**Verdict:** the claimed GL15 example withstands the attacks in this lane. I reconstructed the vanishing and entire-noninduction arguments using the actual published interfaces and independently regenerated the finite data. I found no substantive mathematical defect. One very minor source-locator inaccuracy is recorded below. This is a scoped mathematical verification with established theorems as dependencies, not a formal proof certification or a novelty certification.

## Object and exact claim

Actual PDF: all nine pages read, including status, proofs, consequences, limitations, and all references. SHA256 `1144eb3999212084bef013e7984bfc54bf43a9f931d959b63ba2743d814cf0a9`; 106606 bytes. Its support-kit copy has the same hash. The complete 259-line TeX source was also read. ZIP: 394529 bytes, SHA256 `1f1a66d7e67b1434e4c17af96c9461b1d2f6bd7f4197de4ef88f95aad8105dc1`.

The hypothesis tested is the stated smooth admissible complex representation over F=Q3 and its unramified quadratic extension E. D_K[a,b] is the essentially square-integrable **quotient** of the ascending character induction, not the Zelevinsky segment socle. With A=[0,2], B=[1,4], C=[3,3], D=[2,5], T=[4,6], the Langlands quotient of T,D,C,B,A has degree 15; is Galois invariant; is not an entire normalized induction from any proper parabolic; and has no invariant form for any nonsingular Hermitian stabilizer. No conclusion for all local fields, other coefficient categories, or all possible prior literature was tested or inferred.

## Primary interfaces authenticated

I downloaded primary bodies independently, preserving their hashes in READ_LEDGER.json. The bodies were inspected at the relevant exact statements; they were not read cover to cover or reproved in full.

- [FLO, published paper](https://numdam.org/item/10.1007/s10240-012-0040-z.pdf): pp.201–203 give N=C_M M, inverse identities, chamber holomorphy, the correct rank-one image/kernel direction, quotient-segment convention, and the relation a≤c≤b≤d. Equations (4.5), (12.5), (13.3) fix the gamma-ratio orientation. Corollary 13.6 explicitly gives a basis for each fixed x, of size 2^(t−1). Equations (12.1), (6.6) and the pp.293–294 argument justify independent entire open-orbit restrictions after a linked swap.
- [LM, arXiv 1411.6310v3](https://arxiv.org/pdf/1411.6310v3): Proposition 2.5(5) and Theorem 2.6 provide additive constituent parameters for L. Definition 5.13 and Proposition 5.20 apply when either side is a ladder. The two directed matching obligations use precisely the displayed arrows and a left shift of both endpoints. Appendix A.5 identifies the ring involution taking Z(m) to L(m) at the same multisegment.
- [JPSS published scan](https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf): visually inspected pp.444–445, including the hypotheses preceding (5), and pp.395–396, §2.9. The quasi-square-integrable segment formula specializes as claimed; invertible Laurent-monomial epsilon factors cannot change valuations near the specialization.
- [OWR 14/2011, EMS body](https://ems.press/content/serial-article-files/46327): Conjecture 1, the orbit-sum interpretation, and §5.3's definition of imprimitive and Conjecture 4 were inspected directly. The context includes arbitrary irreducible Langlands quotients, not an implicit restriction to unitarizable representations.

These imports have compatible hypotheses: characteristic-zero p-adic fields, complex coefficients, essentially square-integrable and therefore generic individual inducing factors, and positive center differences at every required rank-one step. The nongeneric quotient is never substituted for a generic inducing factor in Theorem 12.4.

## Independent reconstruction and attempted falsification

### 1. Conventions, fields, models, and orbit counting

The lengths 3,4,1,4,3 sum to 15. The centers 5,7/2,3,5/2,1 strictly decrease in the initial standard module. Each factor is fixed by the field involution, so the unique quotient is fixed as well. Nothing here replaces Galois invariance by contragredient invariance.

The norm convention creates no factor-of-two error: |Nm(z)|_F=|z|_E. Thus the F-side gamma factors use q=3 and the E-side normalizers q=9 with the same real exponents. Eta(3)=−1 on the F side, while its base-change pullback is trivial. A conductor-zero nontrivial additive character exists; changing it changes units only at this point.

I tested the tempting center objection. The central character on a scalar z is |z|_E^45, since the sum of all character exponents is 45. On the norm-one center of any U(V), |z|_E=1, so this is trivial. The claimed vanishing is therefore not a mistaken central-character obstruction. This also shows that π itself is not unitarizable, which removes an apparent conflict with positive unitarizable results. Its standard module is reducible at the linked pairs; the generic-quotient criterion excludes the generic positive class. The presence of Steinberg factors of length greater than one rules out spherical vectors in the standard module and hence its quotient, using exact compact invariants. Unramified cuspidal-line parameters do not make π spherical.

There are two Hermitian G-orbits even in odd dimension, when stabilizer groups may be isomorphic. The argument fixes arbitrary x throughout. The size-sixteen basis is genuinely for this fixed stabilizer; the paper does not divide a total over two orbits incorrectly. A simultaneous eta twist multiplies the relevant Levi forms by a fixed nonzero character value, so choosing epsilon_T=0 loses no coordinate.

### 2. Rational germs from a different finite mechanism

Before reading the supplied math programs, I wrote independent_falsification.py without importing them. It constructs the graded kernel of N_m tensor 1 + 1 tensor N_n for each pair of Steinberg lengths. Exact integer-matrix ranks recover the unramified L-exponents. With centers restored, the kernel exponents are b−c−j, j=0,…,min(m,n)−1. This is a finite linear-algebra cross-check of the JPSS specialization, not a substitute for the published local-factor theorem.

Starting with gamma=epsilon L(1−u,dual)/L(u), I obtain the same direction as the paper: numerator from Q and denominator from P in equation (4). Inverting that ratio would invalidate the proof; the actual FLO (13.3) rules out that attempted objection.

All ten unordered pairs, both directional exponent lists, and forty exact q/sign germs were computed. For the five used linked pairs TD,BA,TC,DB,CA the orders for opposite labels are 2,2,1,2,1. Equal-label germs are units. For DC and CB, P={2}, Q={1}; both label parities have order zero. Their q=3 values are 9/13 and 9/7, and their q=9 values are 81/91 and 81/73, agreeing with the actual PDF. These are epsilon-free values only; no unsupported normalization constant was promoted to an exact operator value.

### 3. The nested swaps are actual isomorphisms

Both swaps have positive forward center difference 1/2. Upon using unitary Steinberg factors and putting their centers into the parameters, FLO's chamber statement supplies forward M and reverse N holomorphy. The forward E-side scalar has L-exponents 2 and dual exponent 1; its L(0) and dual L(1) are finite nonzero. Thus forward N is also holomorphic. The meromorphic inverse identities can consequently be specialized to inverse operators.

All three orders TDCBA, TCDBA, TDBCA satisfy both the actual FLO forbidden-relation test and LM's ordered-form test. The period bases in these orders are complete and holomorphic. The F-side scalar for either nested swap is a unit for every label, so the specialized functional equation transports each segment-labelled basis vector by a nonzero scalar. This excludes hidden mixing or loss of support. The nonmonotone center order in the latter two presentations is harmless because these modules are proven isomorphic to the initial standard module.

### 4. Rank-one kernels and specialization

For each needed linked adjacency, the positive center condition and the source rank-one identity put the reverse N image in a proper forward-M kernel. Exact, nonzero-preserving parabolic induction preserves the nonzero rank-one submodule and quotient. Therefore the induced kernel is proper and lies in the unique maximal proper submodule of the standard module. This is the correct quotient orientation; it would fail for an unsupported use of a segment socle.

A quotient period annihilates each such submodule at zero. Its constant-coefficient expansion in a holomorphic source basis need not annihilate it away from zero, and the paper does not assert that. Restricting the meromorphic identity to open-orbit sections makes every target restriction entire and independent at zero. This supports coefficientwise exclusion without claiming full-period holomorphy or completeness in the linked-swapped order. The same restricted-space device is explicit in FLO's ladder proof; its application here does not require the quotient to be a ladder.

The five exposed conditions form T—D—B—A—C—T. Each nonzero coordinate would require unequal endpoints on all five edges. The independent exhaustive enumeration of the sixteen labels with epsilon_T=0 gives no survivor. Equivalently, summing the five binary equations gives 0=1. No equality generating the entire maximal kernel from transported rank-one kernels is used. The vanishing deduction is complete with the authenticated source interfaces.

### 5. Entire induction rather than equality of cuspidal supports

If an entire proper induction were this irreducible π, exactness and preservation of nonzero objects force irreducible inducing data. Grouping Levi factors gives two irreducible positive-degree factors. The additive constituent theorem forces the **multisegment** sum to be A+B+C+D+T. This is stronger than the insufficient assertion of matching cuspidal supports.

I independently enumerated all fifteen unordered partitions and both directed graphs. Every partition has a ladder side: singleton sides always do; only BC and CD among two-element sides fail, and their complements ADT and ABT are ladders. The arrow directions and the two-endpoint left shift agree with the actual source definition. Applying the ring involution preserves the positive irreducible expansion and hence the length-one condition; no erroneous multisegment dualization occurs.

Every partition has an isolated X vertex in at least one direction. I then compared the **actual TeX manuscript's** fifteen displayed rows with my independently generated named graphs: all fifteen witnesses are isolated, all fifteen entire Y lists are exact, and no partition is missing. independent_results.json retains the full thirty graphs and exact witnesses. This proves the claimed entire-noninduction under the LM interface.

## Findings and exact gaps

No substantive mathematical defect was found. The strongest verified result is the complete stated example and its three historical conjecture consequences, conditional on the standard published theorem imports. FLO's τ-Witt definition assigns index zero to these individually invariant Steinberg data; the historical k=1 imprimitive conjecture predicts total two, while the verified two orbit contributions are each zero.

One editorial locator is slightly inaccurate: paper p.2 calls FLO's N “defined in (1.10)”. The definition N=C_M M is the unnumbered display immediately before (1.10); (1.10) is its Whittaker compatibility identity. Pages201–202 identify the material unambiguously. Severity: minor citation localization only. No source change was made or repair developed.

The exact remaining research limitation is priority and overlap with the uninspected Luo–Zha body, including transformed parameters, mechanism, and period consequences. This lane did not retrieve that body or certify novelty. The manuscript discloses this limitation prominently. It is not an omitted step of the displayed proof and cannot be converted to a firstness claim.

I did not independently reproduce every external theorem's deep proof, inspect all fourteen cited papers in full, audit all website/catalogue metadata, or perform a fresh general literature search. Those are limits of this lane. Claims about BP/Lu–Matringe/Matringe–Offen/Matringe–Offen–Yang and the exact older GMM/MOS/Sharma antecedent examples are not newly certified here; their bounded narrative was read in the actual paper and the source-credit ledger. Nothing from those works is required as a proof dependency of the main theorem.

## Checkable artifacts and custody

- SEALED_EARLY_LEDGER.md and CUSTODY.md: independence seal and corrected chronology.
- READ_LEDGER.json: exact actual-read coverage, file identities, primary URLs, and exclusions.
- independent_falsification.py and independent_results.json: independent nilpotent-kernel computation, forty germs, thirty LC graphs, actual-table comparison, chamber/order tests, and parity enumeration.
- run_bounded_checks.py and bounded_check_runs.json: retained run deadlines, process-group cleanup, return status, and output hashes. Both final runs completed below two seconds with empty stderr. The supplied verifier's fifteen optimization-mode runs are retained only as supplementary reproducibility evidence; its PASS status is not a mathematical proof or promotion criterion.

Only this lane's directory was written. Main remained checked out; no sources, shared scripts/configs, website, native spreadsheet, earlier review, commit, release, or outreach was changed or initiated. Primary body working copies and rendered pages are private and ignored from version control by this lane's .gitignore.

Root must read the actual paper and all completed independent reports before any promotion. This report does not substitute for that adoption step.
