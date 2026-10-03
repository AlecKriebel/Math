# Independent adversarial audit: fractional coefficient savings

**Entry:** rank 495, problem 30005832, OWR-14298166-010  
**Reviewed:** 2026-10-03 UTC  
**Verdict:** **PASS, qualified as to the qualitative problem interpretation and historical priority.**

The frozen quantitative theorem is correct. No mathematical HOLD was identified. The construction gives a bounded-width, linear-size CNF family with rational normalized Nullstellensatz mass at most `72d - 102 + 106/2^d`, while every arbitrary-real refutation has at least `2^(d-1) + 1` literal-weakening terms. Consequently the integer mass is at least that large. The claimed `Omega(N/log N)` separation follows.

This is more than the previously published constant-gap example. It is also a defensible affirmative example for the original question under the ordinary reading of “natural” as a familiar cardinality-circuit encoding and “greatly” as an unbounded, nearly linear factor. The original question does not demand a superpolynomial lower bound. On the other hand, neither naturalness nor historical closure has a formal criterion in the source. An unconditional declaration that the historical open problem is fully settled would outrun this audit. The packet's conservative partial-result designation is acceptable, but should be understood as a scope/publication judgment, not a missing proof step or an established failure to meet a superpolynomial requirement.

## 1. Frozen target and integrity

Reviewed proof SHA-256:

`58378769695d585a53ba5e342305e344be8dd64e0ea765cc9e467ad93d8cf184`

Reviewed manifest SHA-256:

`477bda86fe9e79f2067a3d271146babb60272a690edf54207b727864542604ba`

All six manifest-listed files match their recorded byte counts and hashes. The independent checker verifies the manifest and every listed file both before and after its checks. The frozen public packet was not edited. The audit files are separate from that packet. No remote repository state was changed, and no source PDF, extracted source text, catalogue record, or private research material is included in the audit deliverables.

## 2. Original question and proof-system match

The original source was checked in the supplied official MFO PDF, printed p. 927, including visual inspection of PDF page 57. Its question is:

> Are there natural examples where having fractional coefficients greatly reduces the total coefficient size needed for Nullstellensatz and/or Sherali-Adams proofs?

The following discussion contrasts proof size with coefficient mass; it imposes no quantitative definition of naturalness, no minimum gap exponent, and no explicit superpolynomial requirement. The ICALP article's introductory discussion supplies proof-complexity motivation, including exponential examples, but does not turn that motivation into an additional formal hypothesis of this question.

The supplied ICALP PDF was checked at Definitions 5–9 and Remark 10, with visual inspection of printed p. 117:5. These specify Boolean twin literals, compatible literal monomials, a minimum coefficient-mass representation, and the equivalent weakening formulation when axioms are monomials. In that setting, Boolean and twin-relation correction terms are not charged. This matches the candidate's principal convention.

Important consequences of that match:

- Every clause is represented by its coefficient-one violation indicator. No constraint is secretly multiplied by a parameter-dependent scalar.
- The integer restriction concerns coefficients of the displayed literal weakenings. It does not mean integer coefficients after an arbitrary change of polynomial basis while still permitting fractional decompositions for free.
- A weakening that could originate from several clauses remains one function after aggregation. Choosing any one eligible source for it is legitimate in the lower-bound proof.
- Arbitrary multipliers reduce, after expansion and Boolean/twin normalization, to the literal-weakening setting. Terms killed by incompatible literals do not help.
- Free Boolean/twin corrections vanish on every Boolean witness. They cannot evade the lower bound.
- The candidate's principal certificate is actually an ordinary polynomial identity after substituting each twin by `1-v`; it does not need Boolean correction terms at all.

The assertion that rational and real mass optima agree is also correct: after splitting signs, the problem is a feasible finite rational linear program with an attained finite optimum and hence a rational optimal solution. The proof only needs the explicit rational feasible solution.

## 3. Circuit semantics, variable counts, and clauses

For `d >= 1`, `m = 2^d`, `r = m/2`, the balanced tree adds two `s`-bit words at each level-`s` node. A node contains one half-adder and `s-1` full-adders. Each gate introduces exactly two new variables. The carry entering position zero is the constant zero, not a missing variable or uncharged constraint.

The gate variable tuples are pairwise distinct within each gate. Previously generated carry variables enter later gates correctly; the final carry becomes the top output bit of its word. The output word from each nonroot node is consumed as an input at its parent. Thus there are no unexplained extension rules inside the proof: every circuit variable and gate constraint belongs to the input formula.

The audited counts are:

- Gates: `sum_s (m/2^s)s = 2m-d-2`.
- Half-adders: `m-1`.
- Full-adders: `m-d-1`.
- Boolean variables: `m + 2(2m-d-2) = 5m-2d-4`.
- Clauses: `12(m-1) + 24(m-d-1) + m + d+1 = 37m-23d-35`.

A half-adder has 16 Boolean tuples and four valid tuples, hence 12 forbidden-tuple clauses. A full-adder has 32 tuples and eight valid tuples, hence 24 such clauses. Their maximum widths are four and five. The input units and root units do not duplicate gate axioms or each other.

For every input assignment there is exactly one gate-consistent extension. The root represents the integer Hamming weight of the inputs, including both endpoint weights zero and `m`. The root units select precisely weight `r`. Therefore the gate/root subsystem is consistent with every weight-`r` input, and adjoining all input-zero units is inconsistent.

## 4. Local identities, global signs, and mass

For a gate with incoming bits `a,b` or `a,b,c`, sum bit `z`, and carry bit `t`, the residual is the incoming-bit sum minus `z+2t`. Its zero set is exactly the correct XOR/AND or XOR/majority truth table. Multilinear interpolation expands this affine residual using only the forbidden full-tuple indicators.

The local residual distributions and their absolute sums were independently reconstructed:

- Half-adder, residuals `-3,-2,-1,0,1,2`: multiplicities `1,3,4,4,3,1`; mass 18.
- Full-adder, residuals `-3,-2,-1,0,1,2,3`: multiplicities `1,4,7,8,7,4,1`; mass 36.

Position weights are `2^j`. Inside each addition, an intermediate carry has coefficient `-2^(j+1)` at its producer and `+2^(j+1)` at its consumer. Across the tree, every nonroot output bit similarly cancels against its parent input occurrence. The residual sum is therefore `sum_i x_i - Z`.

For a zero target bit, the root unit is `y_j`, with positive sign in `Z-r`. For the unique one target bit `j=d-1`, the unit is `1-y_j`, with negative sign there. Subtracting both the residual sum and `Z-r` from `sum_i x_i` gives `r`, so division by `r` gives the claimed identity with exactly the signs in equation (13).

One level-`s` node costs `18 + 36(2^s-2) = 36*2^s-54` before division. Total gate mass is `36md-54m+54`. Adding input mass `m` and root mass `2m-1`, then dividing by `m/2`, gives exactly `72d-102+106/m`. No root carry, input term, or gate cost is omitted.

The proof has degree at most five, constant axiom multipliers, and a linear number of literal-weakening terms. Each residual magnitude is at most three and each positional weight is at most `r`; root coefficients have magnitude at most two. All reduced coefficient denominators divide `r`. The stated magnitude and bit-length upper bounds follow. Logarithmic coefficient mass must not be confused with logarithmic written proof length or bit complexity.

## 5. Lower bound: full strength and limitations

The all-degree support argument is valid for arbitrary real coefficients, not only nonnegative coefficients or constant multipliers.

Take any putative refutation and assign each nonzero weakening term one original source axiom. Let `I` be the input indices whose zero units were selected as sources. If `|I| <= m-r`, choose an `r`-element set outside `I` and extend its indicator input through the circuit. Every gate and root source vanishes. Each selected input source also vanishes. Any multiple of a vanishing source vanishes, independently of its coefficient and degree. Thus all terms vanish while the left side remains one, a contradiction.

Consequently `|I| >= m-r+1`. There must be at least that many distinct nonzero terms, because each chosen term contributes at most one index to `I`. This reasoning remains valid when a term is eligible for multiple input or noninput sources: one source per term suffices. It also survives cancellation and aggregation into distinct weakening functions.

For integer coefficients, every nonzero coefficient has absolute value at least one, so integer mass is at least support. Integer certificates exist by the full-assignment-indicator construction given in the packet; the integer minimum is not being compared to an empty feasible set.

This establishes a linear support lower bound. It does not establish a degree lower bound, a superlinear support lower bound, or a superpolynomial bit-complexity separation. Those are limitations of the proved conclusion, not flaws in it.

For the explicitly stated alternative system `-1 = sum c_W W + sum b_M M`, with `b_M >= 0`, the same witness makes the axiom terms zero and the remainder nonnegative. That is a contradiction. Negating the upper-bound certificate supplies its upper bound. The optional extension is therefore sound for exactly the stated syntax and cost. The terminology qualification concerning the older arXiv Definition 16 is warranted; no universal identification of all Sherali–Adams variants is needed.

## 6. Small parameters and asymptotics

The family is well-defined already at `d=1`: four variables, sixteen clauses, and certificate mass 23. Its support lower bound is only two. Bounds of this kind do not certify a strict separation for every small parameter.

The first strict separation certified by these particular upper/lower bounds occurs at `d=11`:

- `m=2,048`, `N=10,214`, `M=75,488`.
- Rational mass at most `706613/1024`, approximately 690.052.
- Integer mass and arbitrary-real support at least 1,025.

The formula denominator is positive for all `d>=1`. For large `d`, the gap is at least `(m/2+1)/(72d-102+106/m) = Omega(m/d)`. Since `N=Theta(m)` and `d=Theta(log N)`, this is `Omega(N/log N)`. The fact that the small-parameter upper bound is loose does not invalidate that asymptotic claim. The checker verifies the strict-gap threshold through `d=100`; the general asymptotic conclusion follows symbolically from the formulas.

## 7. Independent computational controls

The separate dependency-free `independent_checks.py` does not import the author's code. It reconstructs the circuit recursively in postorder rather than level by level. It uses scaled integer coefficients and ordinary monomial tuples retaining repeated powers, rather than Boolean-idempotent multiplication. Thus its ordinary-polynomial identity checks cannot silently hide a missing Boolean correction.

It also reruns the author's checker as a separately labelled reproduction test. Its output exactly matches the frozen `exact_results.json`, including all 5,757 reported assertions.

Independent controls include:

1. Local truth tables generated using parity and carry predicates, checked against residuals and exact polynomial expansions.
2. Full certificate construction and ordinary-polynomial cancellation for every `d=1,...,11`, through 2,048 inputs.
3. Rejection of separately corrupted input, gate, and target-root signs for every generated family.
4. All 4,112 full Boolean assignments for `d=1,2`, including invalid circuit assignments, checking both the identity and unsatisfiability.
5. Every input assignment through eight inputs and every critical avoiding witness through sixteen inputs: 12,948 maximal forbidden-set witnesses.
6. Exhaustive enumeration of all literal monomials for `d=1,2`. For `d=2`, this checks all `3^12=531,441` monomials and all 508,878 distinct eligible weakenings against the six weight-two witnesses. Their projections have minimum covering number three, consistent with the arbitrary-real support obstruction.
7. Independent real dual and primal controls for the published gadget replication with one through four selector bits, including the credited mass 14 versus integer mass 17 instance.
8. Exact mass summations and formulas through `d=100`.
9. Exact truth-table verification of conventional XOR plus AND/majority gate encodings, supporting the robustness observation below.

Finite controls are regression and adversarial checks, not substitutes for the all-parameter algebraic and combinatorial proofs. Assertion totals include repeated local checks and must not be interpreted as independent mathematical theorems.

Reproduce from the audit directory with:

`python independent_checks.py > independent_results.json`

An optional `--public` argument selects a relocated frozen public directory. The supplied result is deterministic and uses only Python standard-library exact arithmetic.

## 8. A useful robustness observation

The complete forbidden-tuple CNF is not essential to the separation. Replace each local gate's clauses by any exact CNF on those same four or five variables. Every forbidden full tuple violates at least one replacement clause. Its full-tuple indicator is therefore a literal weakening of that clause. The original certificate terms remain available with the same coefficients and mass. The gate/root witness assignments are unchanged, so the lower bound also survives.

For example, encode a half-adder by the usual four XOR clauses for its sum output and three AND clauses for its carry output. Encode a full-adder by eight three-input-XOR clauses and six majority clauses. These exact gate encodings have seven and fourteen clauses, respectively, and maximum width four. They were independently truth-table checked. The same certificate and lower-bound argument then apply to a formula with the same variables and `22m-13d-20` clauses.

This observation is an audit-side consequence, not an alteration to the frozen theorem or its stated clause count. It shows that the gap does not depend on retaining redundant full-tuple clauses. Substantial changes such as replacing the entire cardinality circuit with a single unnormalized arithmetic equation still require a different measure analysis.

## 9. Five approaches and attribution

The five recorded approaches are substantive and their outcomes are appropriately separated:

- The six-variable example is existing Potechin–Zhang work, correctly credited. Its finite 14-versus-17 gap is not claimed as a discovery.
- Selector replication has the stated exact real and integer optima. Its ratio tends to `4/3`, so it does not establish the desired growing gap.
- Real-mass tensorization follows from primal products and tensor products of feasible optimal duals. No unjustified integer-optimum or support tensorization is asserted.
- The padded Hamming-slice construction has the stated certificate and hitting-set lower bound, but its exponential input expansion is correctly disclosed.
- The adder family removes that padding and supplies the central unbounded separation with linear input size.

The adder method is an established encoding technique, independently supported by the supplied Eén–Sörensson source, Section 5.4. This supports its naturalness as an encoding, not priority for this mass estimate. The audit establishes neither novelty nor the absence of a prior equivalent construction. The packet correctly avoids a first-discovery claim.

## 10. Disposition and recommended wording

**Mathematical disposition:** PASS for the exact frozen theorem, normalization, lower-bound scope, mass formulas, all five approach assessments, and the explicitly limited optional proof-system extension.

**Original-target disposition:** qualified affirmative evidence, with no formal defect preventing the family from answering the literal qualitative question under a reasonable natural-encoding/unbounded-savings interpretation. A requirement of superpolynomial hardness must not be invented and then used to declare failure. Conversely, subjective naturalness and historical closure cannot be certified by exact-arithmetic checks.

A defensible concise statement is:

“An explicit linear-size cardinality-adder CNF family exhibits an unbounded `Omega(N/log N)` fractional-coefficient advantage in the normalized Boolean Nullstellensatz mass convention. The proof and quantitative gap are verified; interpretation of the original qualitative naturalness question and historical priority remain qualified.”

Keeping the campaign's conservative partial/unsolved designation is permissible while those external judgments remain open. There is no proof-repair requirement before publishing the frozen quantitative result with its existing qualifications. Any revised stronger full-resolution or novelty claim would need its own justification.

### Primary references checked

1. Aaron Potechin, joint work with Aaron Zhang, contribution in *Proof Complexity and Beyond*, OWR 15/2024, printed pp. 926–927. [Official report](https://publications.mfo.de/bitstream/handle/mfo/4161/OWR_2024_15.pdf?sequence=4), [DOI](https://doi.org/10.4171/OWR/2024/15).
2. Aaron Potechin and Aaron Zhang, *Bounds on the Total Coefficient Size of Nullstellensatz Proofs of the Pigeonhole Principle*, ICALP 2024, article 117, Definitions 5–9, Remark 10, introductory discussion, and Appendix A. [DOI](https://doi.org/10.4230/LIPIcs.ICALP.2024.117).
3. Aaron Potechin and Aaron Zhang, earlier full version, arXiv:2205.03577v1, Definition 16. [Versioned record](https://arxiv.org/abs/2205.03577v1).
4. Niklas Eén and Niklas Sörensson, *Translating Pseudo-Boolean Constraints into SAT*, Section 5.4. [DOI](https://doi.org/10.3233/SAT190014).
