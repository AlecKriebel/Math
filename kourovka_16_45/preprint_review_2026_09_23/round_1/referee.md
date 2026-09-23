# Fresh adversarial preprint review, round 1

Review completed: 2026-09-23 15:07 UTC. Completion estimate for this assigned review: **100%**. Scope is preprint readiness, not journal acceptance. No external individual was contacted. No canonical manuscript, verifier, or git state was edited by this referee.

## Input and independence

The reviewed manuscript is the frozen version 1.0.0 in `input_proof.tex` and `input_proof.pdf`, originally copied from `kourovka_16_45/proof.tex` and `proof.pdf` before the parent began editing them. All manuscript line references below are to this frozen source.

| Input | SHA-256 |
| --- | --- |
| `input_proof.tex` | `4791868796b3236bd6f14386c82185df8b1af5a9aa7e9b957dd427f90d582367` |
| `input_proof.pdf` | `a6c12a2b8bcba3b1ca9d9a07a89052f2e6cad5e97b580d501882c355b9b6184b` |

I read the complete mathematical manuscript first, without reading any prior audit verdict or supplied verification code. I then wrote and ran `independent_finite_check.py` from the manuscript's explicit data. Only afterward did I inspect and replay the supplied Python and C++ programs. I did not read the September 21 audit reports or their checkers. The fresh computation shares the mathematically natural closure/enumeration mechanism described in the manuscript, but imports no project module, certificate, saved group table, or prior checker code.

The parent subsequently disclosed an editorial correction underway involving the projective pairs/products sentence, and a separate package-builder repair. This report remains against the frozen manuscript and does not certify the revised version or the separate upload-kit builder.

## Verdict

**The theorem and its full all-actions proof survive this adversarial review. One minor but actionable mathematical wording correction is required in the frozen text. No other actionable preprint issue was found.**

The verified mathematical conclusion is that the specified matrix action gives a group of order 100920 with

\[
b_{\mathrm f}(G)=b(G)=3<4=\mu'(G).
\]

The finite checks are supporting certificates; the universal bound over all subgroups and all permutation actions is justified by the manuscript's structural proof. I found no circularity, unsupported transfer to an equivalent hard problem, or inappropriate dependence on an optimization result. This conclusion is a referee judgment supported by checkable work, not a claim of formal verification or guaranteed bibliographic priority.

## Actionable finding

### R1-01 — Identify the projective pairs, rather than their products, as the dihedral generators

- **Severity:** minor mathematical wording error (P3).
- **Location:** `input_proof.tex`, lines **266–268**, PDF p. 4.
- **Statement:** Following the displayed pair-subgroup orders, the text says that the corresponding products have orders 4, 3, 10, and that their projective images generate dihedral groups of orders 4, 6, 10.
- **Reasoning:** Grammatically, “their” refers to the products. The individual images of those products have orders 2, 3, and 5, respectively, and generate cyclic groups of those orders. It is the images of each corresponding **pair** of matrices that generate the dihedral groups of orders 4, 6, and 10. The intended argument is readily reconstructed, but the literal assertion is false and should be corrected.
- **Repair:** Write, for example: “The products \(R_2R_3,R_1R_3,R_1R_2\) have orders \(4,3,10\), respectively. In \(H/Z\), the corresponding pairs of involutions generate dihedral groups of orders \(4,6,10\); adjoining the common central involution doubles these orders.”
- **Theorem affected:** **No.** Direct independent computation gives the stated pair-subgroup orders 8, 12, 20, and the intended elementary argument is correct.
- **Status:** Open against this frozen input. The parent reported that this exact repair was already underway. Its repaired version must be evaluated by the next fresh round.

There are no optional style requests or journal-specific conditions in this report.

## Complete mathematical coverage

| Source lines | Claim examined | Adversarial check and result |
| --- | --- | --- |
| 27–86 | Claimed invariants, scope, original problem, action conventions | Checked against the primary notebook and Cameron sources. The definition of bases for the permutation image and permission for nonfaithful actions agree. The priority statement is suitably limited. |
| 65–73 | Empty sets, infinite action domains | For a finite image, choosing a moved point for each nonidentity image element gives a finite subbase. Inclusion-minimal bases are therefore finite. Trivial-group values are consistent. |
| 89–118 | Subgroup formulation and quotient maximum | Checked both directions. Normality of the intersection is exactly what equates the chosen-coset stabilizer with the action kernel. Core intersection identity is valid. Empty-family and trivial-action conventions work. |
| 120–138 | Meet breadth equals independence number | Witnesses chosen outside one member and inside all others are independent. Omission-generated subgroups provide the converse. Neither direction assumes normality. |
| 140–165 | Restriction lemma and Boolean meet embedding | Every witness for a remaining member lies in the restricted subgroup. The empty restricted family for a one-member family is consistent. The displayed index complement converts intersections of sets to intersections of subgroups correctly. No join-preserving claim is used. |
| 168–198 | Complement, triangle relations, SL2(5), A5 quotient | Fresh exact arithmetic verifies the triangle relations, order 120, the asserted SL2(5) generator mapping as a bijective homomorphism, and the A5 quotient with kernel exactly Z. This also removes dependence on trusting the standard triangle presentation. |
| 200–224 | Proper subgroups of A5, simplicity, mu'(A5)=3 | Rechecked transitive and intransitive cases, Sylow normalizer orders, exclusion of orders 15, 20, 30, the A4 and dihedral independence bounds, the degree-five minimal base, and the conjugacy-class argument for simplicity. No classification assumption is hidden. |
| 226–251 | mu'(H)<=3 and faithful base bound 2 | Unique-involution argument is valid in odd characteristic with determinant one. Odd-order subgroups inject into A5 and have orders 1, 3, or 5. For an indexed dependent image family, s in KZ but not K forces Z not contained in K, hence the required smaller bound. A trivial-intersection family must contain an odd member, which bounds its minimal size by 2. |
| 253–275 | Complement witnesses and b(H)=3 | Words for R2 and R3, squares, product orders, pair subgroup orders, generation, independence, and exact intersections all checked independently. The first two pair groups intersect in a group of order 4 since that intersection contains <R3> and its order divides gcd(8,12). Removing R3 from the third pair group leaves precisely Z in the triple intersection. Only R1-01 requires repair. |
| 278–299 | One-dimensional affine lemma | The cyclic 2-group has a unique maximal subgroup, so some generator projects to a generator. For nontrivial D, its scalar is not 1, making the geometric sum vanish. An element outside the resulting complement forces the entire prime-order translation subgroup. The cases C=1, D=1, and subgroups disjoint from translations are covered. |
| 301–315 | Line stabilizers and irreducibility | The scalar kernel is unipotent of order 29 unless identity, impossible in H. Thus the stabilizer embeds into F29*, has order dividing 4, and is cyclic. All 30 line stabilizers were also checked directly and are C4. |
| 330–347 | Every subgroup avoiding V has faithful invariant at most 2 | Additive subgroups are F29-subspaces because the field is prime. The zero-intersection case embeds into H. In the line case, Sylow 2-subgroups have precisely the order of the cyclic image, complement the line, and act faithfully. There is no omitted subgroup case or unproved complement-conjugacy assumption. |
| 349–360 | Faithful all-subgroups upper bound | A trivial-intersection family cannot have all members contain V. Restriction to a member avoiding V gives t-1<=2. No maximality, transitivity, or enumerative cutoff is used. |
| 362–375 | Nonfaithful upper bound | Irreducibility makes N intersect V either trivially or in V. In the first case the commutator calculation forces N into C_G(V)=V, hence N=1. Thus every nontrivial kernel contains V and the action factors through H. This covers every nonfaithful action. |
| 377–419 | Independent four-set, generation, exact mu'(G) | Projection proves the linear members essential; the translation is outside the complement. Irreducibility generates V. All omission orders and full order checked directly. The unrestricted meet-family argument covers both intersections 0 and a line, giving rank at most 4. |
| 421–455 | Faithful minimal base of size 3 and theorem | Independently generated all three groups, checked order 58, each exact pair intersection, total identity, minimality, faithfulness through cores, and degree 5220. Combining the independently checked upper and lower arguments yields exactly the stated theorem. |
| 458–485 | Nonnormal bottom and failed core repair | Checked Z0 as the fourfold intersection, the explicit translation conjugation, the preimage cores V semidirect Z, and the trivial core of H. No quotient by a nonnormal subgroup is taken. |
| 487–510 | Enumeration coverage and computational scope | The subgroup search has a complete generating-sequence reachability argument. An ambient whole-group member or repeated member cannot occur in an irredundant nonempty family. The checks over the 75 proper subgroups therefore cover all relevant triples and quadruples. Irredundancy passes to subfamilies, so absence of quadruples excludes larger families. |
| 512–532 | Characteristic-11 counterexample to overgeneralization | Verified the stated, fixed matrix C belongs to the order-120 complement and has order 10; generated the four stated subgroups; checked orders 110, 110, 242, 605, total intersection 1, and deletion orders 11, 11, 5, 2. |
| 534–559 | Reproducibility and AI disclosure | Supplied checkers inspected and freshly replayed successfully; their complete actual-matrix subgroup sets agree. They use exact integer arithmetic, independent reconstruction, and no optimization prerequisite. The paper clearly labels itself unrefereed and the checks as AI assisted. Prior audit reports were not used for this review. |
| 561–589 | References | Checked the original problem, 2010 exposition, 2014 preprint, 2024 article metadata and relevant definitions. The notebook September update does not add a solution to 16.45. No definitive novelty guarantee is asserted or supplied. |

## Independent computational evidence

Run the fresh checker with:

```sh
python3 kourovka_16_45/preprint_review_2026_09_23/round_1/independent_finite_check.py
```

It completed successfully on Python 3.14.6, macOS 26.6.2 arm64 in approximately 1.37 seconds. The output is `independent_finite_results.json`; checker SHA-256 is `37fce76f970e0781d45285983d79769d844724a68e80564c7af81be7227dc789`.

Distinct checked data include:

- H has 120 matrices. Its element-order distribution is 1:1, 2:1, 3:20, 4:30, 5:24, 6:20, 10:24.
- Its 76 subgroup orders have distribution 1:1, 2:1, 3:10, 4:15, 5:6, 6:10, 8:5, 10:6, 12:10, 20:6, 24:5, 120:1.
- All 1,215,450 four-member families of proper subgroups fail meet-irredundancy, and all 67,525 triples fail faithful minimality.
- The pair subgroups have orders 8, 12, 20, all their pairwise intersections have order 4, and their triple intersection is Z.
- The affine group generated by S has 100920 elements; omission orders are 120, 6728, 10092, 16820; S is independent; the omission intersection is exactly Z0 and is nonnormal.
- The faithful three-family has the exact three intersections printed in the paper and trivial total intersection.
- All 30 line stabilizers have order 4 and contain an element of order 4.
- The fixed characteristic-11 example has the claimed subgroup and deletion-intersection orders.

The supplied Python program was then run with its output directory redirected into this review folder. The C++ program was compiled with `-O2 -std=c++17 -Wall -Wextra -pedantic` using Apple clang 21.0.0 and run successfully. The comparison program reported agreement of all 76 actual matrix subgroups despite the different indexings. See `replay_python.log`, `replay_cpp.log`, and `replay_comparison.log`. Reviewed program hashes:

| Program | SHA-256 |
| --- | --- |
| `src/verify_counterexample.py` | `0d31f0018645500df60ac4f6cbfd5c2cdac077afad1ddaa59f60565aa4dd178e` |
| `src/verify_counterexample.cpp` | `b315b718ed33e9d7a98c7ce16a8b9555b310aa916524ebf120875dcd81bf0fd7` |
| `src/compare_certificates.py` | `e069950883743c1c8bb248f583a7e1a74cc6c3e37feb865df79e15c9d576ab1e` |

## Primary-source and PDF checks

All nine pages of the frozen manuscript PDF were rendered and inspected. There are no missing formulas, clipped passages, broken symbols, or other presentation defects that interfere with reviewing this preprint. The displayed data agree with the source. The relevant notebook page and 2024 article pages were likewise rendered and read.

Primary sources accessed on 2026-09-23:

- [September 2026 notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf), printed p. 100: the problem and its equivalent normal-bottom formulation agree with this paper. PDF SHA-256: `2fcce9b98a4df10267fe120229217bfe556c70510704e311540da0cef438f911`.
- [September update](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf): no entry for 16.45 was found. PDF SHA-256: `6dd201b3ae6673b0a053bf8b7d4e3aa8ab54025f19ebf1d8e5e33ca0b838dc0b`.
- [Cameron 2010](https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/): explicitly allows nonfaithful and intransitive representations, uses b2 and mu*, and states the normal-bottom obstruction.
- [Cameron 2014](https://arxiv.org/html/1408.0968v1), Sections 2–3: explicitly allows nonfaithful representations; Propositions 3.1–3.2 and Corollary 3.3 support the cited formulations and notation.
- [Cameron 2024](https://msp.org/mt/2024/3-2/mt-v3-n2-p08-s.pdf), printed pp. 428–429: explicitly allows nonfaithful representations, uses b2 and mu-up-arrow, and poses the equality as unresolved. DOI and bibliographic metadata agree. PDF SHA-256: `94ba37fc539f64f83481b255373c115f078cea0d6accaabeb0f4a4138662f12f`.

Third-party downloads, extracted text, and rendered inspection images are kept only in ignored `kourovka_16_45/tmp/preprint_review_2026_09_23/round_1/`; they are not publication artifacts.

## Exact remaining gaps and stopping condition

1. Correct R1-01 in the frozen version. No new construction, theorem change, or additional computation is needed.
2. This review is not a proof-assistant formalization, and cannot guarantee that no further defect exists. No unresolved mathematical proof gap was identified.
3. The current source search is enough to support the paper's bounded bibliographic statement, not universal priority.
4. The revised version and upload-kit builder are outside this frozen-input verdict. A fresh review of the revised manuscript can establish the requested clean-round stopping criterion.

After R1-01 is repaired, this referee has identified no additional obstacle to posting the result as an explicitly unrefereed preprint.
