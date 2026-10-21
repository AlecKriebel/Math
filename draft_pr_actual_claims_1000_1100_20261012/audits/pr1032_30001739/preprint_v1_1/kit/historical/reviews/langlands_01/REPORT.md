# Independent adversarial review: Langlands, noninduction, and original scope

**Assigned-family verdict: CLEAN.** The submitted candidate satisfies the original problem's `k=1` representation hypotheses. The proof's universal noninduction reduction, quotient/order conventions, ladder hypothesis, two-direction LC criterion, and Zelevinsky ring-involution transfer survive this fresh review. There are no actionable mathematical defects in this assigned family. This is **not** a verdict on the analytic period-vanishing argument or on the complete counterexample.

## Review identity and independence

- PR: 1032; problem: 30001739.
- Immutable head: `810d52306312623ecfe01ecbc5f5f0dd360972c3`.
- Submitted proof SHA-256: `bdc8ad8dc7156a8962f2932755a24e5b4507d2d214f6087d72e63605926cc125`.
- All 44 snapshot file hashes and sizes match `SUBMITTED_PINS.json`; independent verification is in `INPUT_PINS.json`.
- Assigned mechanism: classification plus finite matching, with source authentication of the original question.
- Reads before independent reconstruction: submitted `current/PROOF.md`, `current/MODEL.json`, and fresh primary sources. Embedded acceptance statements in PROOF were treated as claims, not evidence. No historical audit, old certificate verdict, analytic-family artifact, or other new review family was consulted.
- A new checker was written from the source definitions and executed before reading the submitted Hall code. Only after the fresh derivation/graphs had been reconstructed was submitted `check_hall_certificates.py` read and its witnesses compared. Submitted `independent_checks.py` was read then but was not executed; its analytic calculations were not adopted as evidence.
- All review writes are under this `reviews/langlands_01` folder. No external individuals were contacted, no subagent was spawned, and no candidate, shared Git/index, queue, PR, service, or publication mutation was made.

## Claim, assumptions, and success criteria

The representation under review is the irreducible Langlands quotient of

\[
 D_E[4,6]\times D_E[2,5]\times D_E[3,3]\times D_E[1,4]\times D_E[0,2],
 \qquad D_E[a,b]=\operatorname{St}_{b-a+1}(E)|\det|_E^{(a+b)/2},
\]

where `F=Q_3` and `E/F` is the unramified quadratic field extension. Its five Langlands segments are `A=[0,2], B=[1,4], C=[3,3], D=[2,5], E_0=[4,6]`; `E_0` is denoted `E` in the finite certificates.

This family succeeds if it establishes, using correctly instantiated primary theorem interfaces rather than bare checker outputs, that this is a smooth admissible irreducible complex representation of `GL_15(E)`, that it is `tau` invariant, and that it is not itself a whole induction from any proper parabolic. It must also identify the exact original conjecture and distinguish the unrelated reducible standard module used to define the factor from the entire product assumed irreducible in the conjecture.

The full claim additionally asserts zero period multiplicity for every Hermitian form. That is a separate family; it is not a success criterion silently supplied by this finite review.

## Fresh primary-source authentication

Full PDFs were retrieved into `sources/raw` from primary repositories, with URLs, final HTTP URLs, retrieval timestamps, byte lengths, hashes, and version/locator information recorded in `sources/SOURCE_RECEIPTS.json`. Relevant pages were read in full extracted text and critical notation pages were rendered and visually inspected; see `sources/INSPECTION_RECEIPT.json`. This authenticates the used theorem interfaces, not every proof of the cited source papers.

| Source | Fresh SHA-256 | Critical locators |
|---|---|---|
| [LM arXiv v3](https://arxiv.org/pdf/1411.6310v3) | `ac54929c76878b080e09ebec149d38130842439aab4c6080620c2bbae6259438` | Definition 2.2 pp.8–9; Proposition 2.5 and Theorem 2.6 pp.10–11; Definition 5.13 p.34; LC definitions pp.35–36; Proposition 5.20 p.38 and proof p.39; A.5 pp.52–53 |
| [EMS OWR 14/2011](https://ems.press/content/serial-article-files/46327) | `7f06bd2004dd3280376d9725131715774fb51478e9d42216439f64d2d9994c44` | Two p-adic orbits: PDF p.11/printed p.729; summed-period identification: PDF p.13/printed p.731; Conjecture 4 and imprimitive definition: PDF p.16/printed p.734 |
| [MFO OWR 14/2011](https://publications.mfo.de/bitstream/handle/mfo/3229/OWR_2011_14.pdf?isAllowed=y&sequence=1) | `4321a11e3517e09592f45ee9782c697d4a6f5e37203140fc2ad4c3dd805cd41c` | Same interfaces, PDF pp.11,13,16; printed pp.731,733,736 respectively |
| [Published FLO](https://numdam.org/item/10.1007/s10240-012-0040-z.pdf) | `b4b0eb8c749d1244836610bbc56ff8fba0046ce0532f0c87ea179581783da453` | Characteristic-zero local-field setup p.191; representation category and dual p.196; segment quotient convention p.203 |

The LM PDF is specifically v3, revised 14 December 2015, with heading 15 December 2015; its hash matches the submitted proof's cited version. The published FLO hash also matches. The MFO and EMS PDFs have different hashes and printed pagination. `MODEL.json`'s p.734 locator is correct for the EMS version; p.736 is correct for the MFO version. This is not evidence of two different conjectures.

## Original-question scope

The source's section 5.3 explicitly defines its “imprimitive” factors by absence of a whole proper parabolic induced realization. Its Conjecture 4 then requires those factors to be individually Galois invariant and their entire product to be irreducible, and predicts multiplicity `2^k`. The source identifies the multiplicity with the direct sum of stabilizer-period spaces over Hermitian orbits. Its p-adic setting has exactly two such orbits.

The original conjecture does not repeat a detailed coefficient/category restriction in its own sentence. The submitted MODEL makes the smooth complex characteristic-zero p-adic interpretation explicit, consistent with FLO's local setup. The actual field `Q_3` lies within the original local-field context, so a valid counterexample there would refute the asserted universal conclusion without needing an assertion about other fields or categories. No genericity, unitarizability, pairwise distinctness of factors, or `k>=2` restriction appears in this conjecture's stated hypotheses.

The original text's “unitary periods” refers to invariance under a unitary **group**. It does not require the representation itself to be unitary. Restricting to unitarizable representations would change the question and would exclude this proof's route, but that restriction is not present in Conjecture 4.

The construction with `k=1` is legitimate: set the one target factor equal to the candidate quotient. Its irreducibility is supplied by classification and its noninduction is checked separately. The reducibility of the standard module defining that quotient is unrelated to the conjecture's one-factor product.

## Classification, quotient, and noninduction findings

The full independent equations and proof are in `DERIVATION.md`.

1. **Langlands segment convention is correct.** LM defines `L([a,b])` as the cosocle of the ascending character product, and identifies it as essentially square integrable. This agrees with the submitted Steinberg twist. Using the Zelevinsky socle convention at this point would change the representation; the submitted proof does not make that substitution.
2. **The candidate order is correct.** The degree is 15 and the exponents in `O1=(E,D,C,B,A)` are `5,7/2,3,5/2,1`. Every earlier/later pair in each of `O1`, `O2=(E,C,D,B,A)`, and `O3=(E,D,B,C,A)` avoids the LM precedence relation. Consequently these are permitted ordered forms of the same multisegment, and the classification gives the same irreducible cosocle. The simple cosocle establishes a unique maximal proper kernel; it does not establish generation by any designated rank-one submodules.
3. **The universal reduction is valid.** Exactness and preservation of nonzero objects force any whole proper induced realization of this irreducible representation to have irreducible inducing data. Grouping the blocks yields an entire irreducible two-factor product `L(m1) × L(m2)`. The additive multiplicity-one constituent property and injectivity of Langlands classification force `m1+m2=m`, as multisets of segments. Equality of cuspidal supports alone would not justify this reduction, but the stronger classification statement does.
4. **No factorization is missed.** A proper Levi has at least two positive-degree blocks. If any grouped factor were reducible, its nonzero proper subobject and quotient would remain nonzero after induction with the other factor, contradicting simplicity. Nonempty partitions of the five distinct segment occurrences thus cover every possibility, including arbitrary block counts and arbitrary irreducible inducing representations.
5. **The Z/L transfer is valid.** The required involution is a ring involution that permutes irreducible classes. It sends `L(n)` to `Z(n)` using the same multisegment `n`. Positivity and finite length imply equality of irreducibility status of the two products. This neither asserts a functorial isomorphism nor replaces the parameters by their combinatorial duals.
6. **The ladder hypothesis holds in every partition.** Every singleton is a ladder. The only nonladder pairs are `BC` and `CD`; their complements `ADE` and `ABE` are ladders. The weaker LM ladder definition needs strictly monotone endpoints, not adjacent linkage. It is used only to invoke the LC criterion, not to infer that every such ladder is noninduced.
7. **Both LC directions are needed and correctly used.** The theorem tests `LC(m,n)` and `LC(n,m)` when one side is ladder. A failed condition with the nonladder side first is still within the explicit second condition of the theorem. For example `LC(E,ABCD)` is vacuous and true, while the reverse condition fails. Testing the first direction alone would miss this partition.
8. **The neighbor orientations match the primary notation.** The shifted segment in `Y` is the first coordinate shifted left. The second coordinate of a neighbor precedes the second coordinate of `X`; the first coordinate of `X` precedes the first coordinate of its neighbor. The source's injective map covers `X`, not `Y`. The submitted formulas and reviewed code implement exactly these definitions.
9. **Galois invariance is valid.** The trivial cuspidal line and every normalized absolute-value twist are fixed by `tau`. Induction and the unique cosocle commute with the Galois twist. The candidate is therefore individually invariant as required for `k=1`.

These findings validate submitted PROOF lines 54–58, 152–167, and the representation-hypothesis portion of line 171. They do not validate its analytic conclusions merely because a unique quotient or a Hall obstruction exists.

## Independent finite certification and hostile checks

`checks/independent_lc.py` was created from the primary definitions, without importing submitted code or certificates. Its complete output is `receipts/independent_lc.normal.stdout`. Each direction records the full `X`, shifted `Y`, and neighbor graph. Every Hall subset is exhaustively checked, and an independent exhaustive injection search reaches the same result. All 15 unordered partitions have a singleton empty neighborhood in at least one direction; the independent table is in `DERIVATION.md`.

Controls include equality, strict containment, either shared endpoint, overlap, juxtaposition, gaps, reversed precedence, all 1,936 ordered pairs on a 44-interval grid, duplicate segment occurrences, every internal list permutation for each candidate partition, common translation, and contragredient reversal. A nonempty **successful** matching control prevents a vacuous “all products reducible” checker. Explicit calibrations test each neighbor arrow and the left shift. The distinct-occurrence representation avoids accidentally replacing multisegments by sets when duplicates arise.

`checks/mutation_controls.py` tests six hostile definition mutations. Every mutation is detected. A useful adversarial observation is that all five graph mutations—reversing either neighbor arrow, reversing both arrows, shifting right, and omitting the shift—still leave all 15 candidate partitions failing. Thus the bare “all 15 fail” result cannot verify the matching convention. The positive calibrated edges and shift test supply the missing discrimination. The sixth mutation, omitting the reverse LC condition, is detected by the `E/ABCD` asymmetry. This confirms why theorem interfaces and hostile controls were necessary.

After this reconstruction, the submitted Hall checker was read before execution. Its 15 explicit witnesses were verified against the fresh complete graphs; all directed `Y` lists and empty neighborhoods agree. The comparison is in `receipts/SUBMITTED_CERTIFICATE_COMPARISON.json`.

All three scripts—the independent graph checker, hostile controls, and reviewed submitted Hall checker—were executed under normal Python, `-O`, and `-OO`. All nine executions exit zero with empty stderr; each script's output is byte identical across modes. Exact commands, interpreter version, code hashes, timestamps, and stdout/stderr hashes are in `receipts/CHECK_RUNS.json`. Optimization flags are semantic execution controls and are not a security sandbox. No historical UID1000 or permission harness was run. No historical finite PASS was adopted as evidence for a theorem application or multiplicity.

## Exact remaining analytic obligations

The strongest verified result of this family is:

\[
 \pi=L(A+B+C+D+E_0)\in\operatorname{Irr}(GL_{15}(E)),\qquad
 \pi^\tau\simeq\pi,\qquad
 \pi\ \text{is not a whole proper parabolic induction}.
\]

For the complete counterexample the separate analytic family still must verify all of the following interfaces at the specific singular parameters and for every Hermitian form:

- Completeness and specialization of the entire period basis on all three induced orders.
- Exact normalization and orientation of the reverse intertwiner and its image's containment in the unique maximal quotient kernel.
- Holomorphic gamma-ratio specialization and the claimed zero/nonzero alternative for each linked pair.
- Invertible, label-diagonal, nonzero transport across both strict-containment swaps.
- Independence of the restricted open periods after the linked swaps, sufficient to force every coefficient to vanish along the odd cycle.

If that analytic chain is correct, the source-authenticated `k=1` instance predicts total multiplicity 2 whereas the claimed period result supplies 0. Without that chain, the work here supplies a verified imprimitive invariant representation and validated finite obstruction data, not a verified counterexample.

## Disposition and repairs

**Assigned family CLEAN; actionable mathematical findings: none.** No repair to the representation, noninduction argument, or original-scope interpretation is required by this review. For citation reproducibility, retain the EMS URL with the p.734 locator or explicitly use the MFO p.736 locator; the source receipts already distinguish them. The final combined verdict must be supplied by the parent after its independent analytic review. No external publication or acceptance-state change is authorized by this family report.
