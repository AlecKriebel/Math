# Independent audit: a D4 counterexample in canonical potential coordinates

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete analytical proof and its explicit numerical proof tables are retained. The two documents use separately stated row orders and sign conventions for their separating vectors. The displayed formulas, exponent rows, and integer vectors make every certificate directly checkable. This is not a computational reproduction package: executable code, raw exploratory datasets, copied sources and images, and private coordination records are omitted. Historical program checks are supporting verification history and are not claimed to have been rerun for this edition.

The later pullback-varsigma converse and coefficient conjecture remain unresolved by this work. The published sufficient theorem is not refuted; no general replacement proof is supplied for its affected proof step. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

## Scope and status

The independently reconstructed data give a negative answer to the original OWR canonical-potential converse for target 30004665. The submitted candidate is accepted by an independent internal AI audit within this scope. The result concerns the complete, combined-monomial inequality presentation of the canonical potential in its specified cluster torus. It does not concern arbitrary presentations of a cone.

Choose the simply connected group G = Spin_8(C), of type D4. Number the Dynkin diagram with central node 2 joined to leaves 1, 3, 4. The word is

i = (1,2,3,2,4,2,1,2,3,2,4,2).

The canonical potential has 22 distinct monomials, all with coefficient 1. Two have exponent -2 at X_6. Nevertheless, every one of its 22 inequalities is essential, as proved below by explicit integer points. No assertion of novelty or exhaustive current literature coverage is made.

## 1. Original target and coordinate boundary

The source OWR report, printed pages 1123–1125 (PDF pages 37–39), defines the cluster-torus cone and gives a unimodular identification with the string cone. Its final conjecture on page 1125 expressly places the exponent test on W restricted to the dual cluster torus. That is also the coordinate choice in the imported target.

The later Koshevoy–Schumann paper additionally discusses the chamber-ansatz pullback varsigma. For this word, varsigma has only exponents -1, 0, 1, while W has exponent -2. Nonredundancy is invariant under an invertible monomial coordinate map; coordinatewise exponent bounds are not. Consequently this example does not refute the later varsigma formulation, its stated sufficient theorem, or the coefficient-based Conjecture 4. Their relevant conclusions are satisfied by this example.

## 2. Reduced longest word

Use the Cartan matrix with diagonal 2 and off-diagonal -1 exactly on edges 1–2, 2–3, 2–4. In the simple-root basis, the successive inversion roots s_{i_1}...s_{i_{k-1}}(alpha_{i_k}) are:

1. (1, 0, 0, 0)
2. (1, 1, 0, 0)
3. (1, 1, 1, 0)
4. (0, 0, 1, 0)
5. (1, 1, 1, 1)
6. (1, 1, 0, 1)
7. (1, 2, 1, 1)
8. (0, 1, 1, 0)
9. (0, 1, 1, 1)
10. (0, 0, 0, 1)
11. (0, 1, 0, 1)
12. (0, 1, 0, 0)

They are pairwise distinct, nonnegative, and are all 12 positive roots of D4. The final Weyl matrix is -I_4. Thus the word is reduced and represents the longest element. The historical verifier independently enumerated the root system by simple-reflection closure and checked equality with this list.

## 3. Canonical potential reconstruction

Write y_k = X_k^{-1}. For positions k < l, draw a horizontal arrow k → k^+ when l = k^+; draw an inclined arrow l → k when l < k^+ < l^+ and the letters i_k, i_l are Dynkin-adjacent. There are no arrows between frozen vertices. The frozen positions of this word are 7, 9, 11, 12, carrying simple-root labels 1, 3, 4, 2.

For B_{ab} equal to the number of arrows a → b minus b → a, the reciprocal-X mutation rule at mutable k is

y_k′ = 1/y_k;  y_a′ = y_a (1 + y_k^{sgn(B_{ak})})^{B_{ak}} for a ≠ k.

The term with B_{ak}=0 is unchanged. An optimized frozen vertex f has no outgoing arrows to mutable vertices, and its canonical potential summand in that seed is y_f. This fixes the potential independently of exponent or nonredundancy conjectures.

The independent program constructs braid paths to words ending in each simple-root label. A commuting move swaps its two coordinates. A three-term move at starting position p mutates at p and then swaps positions p+1 and p+2. At each step it checks that the mutated/relabelled quiver equals a fresh quiver from the resulting word. It pulls back the last-coordinate monomial using exact rational arithmetic and combines like monomials. The paths have 16, 0, 7, 1 moves for labels 1, 2, 3, 4. The historical reconstruction record retained every path and final coefficient. This edition retains the complete combined support below and the full fixed-label routes, mutation rules, and analytical potential derivation in PROOF.md; the machine reconstruction record and executable program are not distributed.

The final support is as follows. The index in this table is used by the separating certificates. Every coefficient is 1.

| j | Summand | Monomial in y |
|---|---|---|
| 1 | W_1 | y_7 |
| 2 | W_1 | y_6 y_7 |
| 3 | W_1 | y_6 y_7 y_8 |
| 4 | W_1 | y_6 y_7 y_8 y_10 |
| 5 | W_1 | y_5 y_6 y_7 y_8 y_10 |
| 6 | W_1 | y_3 y_6 y_7 y_8 |
| 7 | W_1 | y_3 y_6 y_7 y_8 y_10 |
| 8 | W_1 | y_3 y_5 y_6 y_7 y_8 y_10 |
| 9 | W_1 | y_2 y_3 y_6 y_7 y_8 |
| 10 | W_1 | y_2 y_3 y_6 y_7 y_8 y_10 |
| 11 | W_1 | y_2 y_3 y_5 y_6 y_7 y_8 y_10 |
| 12 | W_1 | y_2 y_3 y_4 y_5 y_6 y_7 y_8 y_10 |
| 13 | W_1 | y_2 y_3 y_4 y_5 y_6^2 y_7 y_8 y_10 |
| 14 | W_1 | y_1 y_2 y_3 y_4 y_5 y_6^2 y_7 y_8 y_10 |
| 15 | W_2 | y_12 |
| 16 | W_3 | y_9 |
| 17 | W_3 | y_8 y_9 |
| 18 | W_3 | y_8 y_9 y_10 |
| 19 | W_3 | y_5 y_8 y_9 y_10 |
| 20 | W_3 | y_4 y_5 y_8 y_9 y_10 |
| 21 | W_4 | y_11 |
| 22 | W_4 | y_10 y_11 |

In particular, rows 13 and 14 contain y_6^2. Thus the canonical exponent bound fails. The support has no repetitions; no inequalities are hidden by collecting equal monomials.

## 4. Exact proof of nonredundancy

Let a_j be the exponent row of X in monomial j, so the canonical cone is C = {t in R^12 : a_j·t ≥ 0 for all j}. The following v_j are integral. For every row j, exact integer arithmetic gives a_j·v_j = -1 and a_k·v_j ≥ 0 for all k ≠ j.

| j | v_j, in coordinate order 1,…,12 |
|---|---|
| 1 | (-1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 0, 0) |
| 2 | (-1, -1, -1, -1, -1, 1, 0, -1, -1, -1, 0, 0) |
| 3 | (-1, -1, -1, -1, -1, 0, 0, 1, -1, -1, 0, 0) |
| 4 | (-1, -1, -1, -1, -1, 0, 0, 0, -1, 1, -1, 0) |
| 5 | (-1, -1, -1, -1, 1, 0, 0, 0, -1, 0, -1, 0) |
| 6 | (-1, -1, 1, -1, -1, -1, 0, 1, -1, -1, 0, 0) |
| 7 | (-1, -1, 1, -1, -1, -1, 0, 0, -1, 1, -1, 0) |
| 8 | (-1, -1, 1, -1, 1, -1, 0, -1, -1, 1, -1, 0) |
| 9 | (-1, 1, 1, -1, -1, 0, 0, -1, -1, -1, 0, 0) |
| 10 | (-1, 1, 0, -1, -1, 1, -1, -1, -1, 1, -1, 0) |
| 11 | (-1, 1, 0, -1, 1, -1, 0, -1, -1, 1, -1, 0) |
| 12 | (-1, 1, 0, 1, 0, -1, 0, 0, -1, 0, -1, 0) |
| 13 | (-1, -1, 0, 1, 1, 1, -1, 0, -1, -1, -1, 0) |
| 14 | (1, -1, 0, 1, 1, 0, 0, 0, -1, -1, -1, 0) |
| 15 | (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1) |
| 16 | (-1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 0, 0) |
| 17 | (-1, -1, -1, -1, -1, -1, -1, 1, 0, -1, 0, 0) |
| 18 | (-1, -1, -1, -1, -1, -1, -1, 0, 0, 1, -1, 0) |
| 19 | (-1, -1, -1, -1, 1, -1, -1, 0, 0, 0, -1, 0) |
| 20 | (-1, -1, -1, 1, 1, -1, -1, 0, 0, -1, -1, 0) |
| 21 | (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 0) |
| 22 | (-1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 0, 0) |

The historical exact certificate record retained all 484 dot products, which the historical verifier recomputed. They are directly checkable from the complete monomial table and separating-vector table above. Each v_j belongs to the cone obtained after deleting inequality j and does not belong to C. Deleting any single inequality therefore enlarges the cone. This is the definition of nonredundancy and is a proof over the reals, not a numerical feasibility claim.

The point (-1,…,-1) gives a strictly positive value for every a_j. Hence the cone is full-dimensional as well. The unimodular chamber map transports the presentation, and these separation statements, to the corresponding string cone.

## 5. Chamber ansatz and the exact published assertion affected

For the present word the standard chamber map X = CA(x) is:

- X_1 = x_1^-1 x_2 x_4 x_6 x_7^-1
- X_2 = x_2^-1 x_3 x_4^-1
- X_3 = x_3^-1 x_4 x_6 x_8 x_9^-1
- X_4 = x_4^-1 x_5 x_6^-1
- X_5 = x_5^-1 x_6 x_8 x_10 x_11^-1
- X_6 = x_6^-1 x_7 x_8^-1
- X_7 = x_7^-1 x_8 x_10 x_12
- X_8 = x_8^-1 x_9 x_10^-1
- X_9 = x_9^-1 x_10 x_12
- X_10 = x_10^-1 x_11 x_12^-1
- X_11 = x_11^-1 x_12
- X_12 = x_12^-1

Its exponent matrix H is triangular with all diagonal entries -1, so det(H)=1. Pulling back monomial j changes its exponent row from a_j to a_j H. All entries of every a_j H belong to {-1,0,1}; the historical certificate record retained the complete rows. The explicit chamber map and monomial table above determine every transformed row. For the two squared monomials, the pullbacks are particularly transparent:

- Row 13 pulls back to x_2 x_4 x_6 / x_7
- Row 14 pulls back to x_1

Thus the exponent-bound equivalence asserted at the beginning of the published proof of Theorem 2, printed page 1046 (PDF page 16), fails. Proposition 5 supplies a monomial torus isomorphism and hence preserves redundancy, but that fact alone cannot preserve the coordinatewise exponent bound. Removing the false equivalence leaves that proof’s invocation of Proposition 6 unsupported for general multiplicity-free pullbacks. This audit supplies no general replacement proof of the published sufficient theorem and does not establish that its conclusion is false. In this example its conclusion is true by the exact certificates above.

## 6. Source conventions and controls

- The primary target is Schumann, “Optimality of string cone inequalities and potential functions,” joint work with Koshevoy, OWR 20/2021, pages 1123–1125: https://ems.press/content/serial-article-files/46898
- Koshevoy–Schumann, “Redundancy in string cone inequalities and multiplicities in potential functions on cluster varieties,” Journal of Algebraic Combinatorics 56 (2022), 1031–1053: https://doi.org/10.1007/s10801-022-01144-z . The published PDF fixes the example word to (2,1,3,4)^3. The older arXiv-v1 word discrepancy is already corrected there and is not claimed as a new error.
- Genz–Koshevoy–Schumann, “Polyhedral parametrizations of canonical bases & cluster duality,” arXiv:1711.07176v1, page 15, supplies the Dynkin-adjacency condition on inclined edges. It is required for the canonical BFZ seed and agrees with the published D4 quiver. KS Definition 8 omits that condition in its terse text. This audit uses the primary canonical seed rule, not the omission: https://arxiv.org/abs/1711.07176

The X-mutation and optimized-seed conventions were visually checked in the published PDF page 9 (printed 1039), and the chamber formula in page 13 (printed 1043). The canonical seed of the published example and its corrected word were visually checked at page 20 (printed 1050). Independent reconstruction recovers 27 central terms, exactly one coefficient 2, and the stated midpoint redundancy. This is a consistency control, not a claim that every typeset term of that displayed expansion is error-free.

The retained OWR source was byte-authenticated against its earlier retrieved copy. Public source byte hashes, exact historical inspection scope, and retrieval history are recorded in SOURCES.json. Full retrieval is not full inspection.

## 7. Candidate acceptance

The submitted manifest SHA256 is dbe8a47ee8f6cf208ba3bd64ad8e3ee0640caf76212f56effc1c141d0e7465ce. All 32 members match their sealed byte counts and hashes. The independent polynomial matches every submitted coefficient and exponent. All 22 submitted separating vectors pass 484 exact dot-product tests. Their human-readable proof table matches the integer data. The submitted closed formula is identical to the independent polynomial. The four submitted fixed-label mutation routes, every intermediate exchange matrix, optimized endpoints, Weyl-root data, and chamber-ansatz data also agree. The historical independent verifier and candidate-data comparison passed ordinary Python, -O, and -OO runs. No mathematical correction to the submitted canonical-W proof is required.

## 8. Independence, reproducibility and test limits

No submitted candidate program was imported or executed. Reconstruction was written directly from the primary rules and completed, with independently found separating points, before reading the sealed candidate. A historical pre-candidate content pin recorded that state. Candidate data were subsequently compared as inert JSON only.

A numerical optimizer was used only to propose the audit’s separating points. These were converted to exact integers and all inequalities were checked again using integer arithmetic. The historical acceptance verification and replay used no LP solver or floating arithmetic. An earlier exact-simplex-library probe returned a point that failed exact constraints; it was rejected immediately and is not part of the proof. The failed exploratory probe is disclosed here as historical context; its log is not distributed.

The historical independent verifier recomputed the potential from the word, verified the root and chamber data, checked all 22 separators and the interior point, and reproduced the historical example’s consistency properties. It used explicit exceptions rather than assert statements. All 25 negative controls were rejected: dropped term, changed coefficient, changed exponent, and a zeroed witness for each of the 22 rows. It passed in ordinary Python, -O and -OO modes. These are records of the completed audit, not new mathematical executions during editorial preparation.

Mathematical boundary: this settles the stated canonical-W exponent converse negatively. It does not settle the later pullback-varsigma converse, disprove the later sufficient theorem, disprove the coefficient-based conjecture, claim an exhaustive classification, or establish novelty.
