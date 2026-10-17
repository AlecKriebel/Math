# Independent finite reconstruction certificate

Problem 30003185 / row 1763. 13 October 2026.

## Decision and evidentiary role

**PASS.** Reader-owned reconstructions of the accepted arguments agree with direct finite enumeration and exact rational arithmetic. All three execution modes, normal, `-O`, and `-OO`, pass 991,546 explicit checks apiece and produce byte-identical mathematical evidence. Fifteen deliberately false statements are rejected in all three modes, for 45 explicit rejections. No assertion statement is used to enforce a check.

This is a finite acceptance certificate for the integrated reader, not another research pass, a new proof of the published inputs, or an experimental proof of the asymptotic theorem. The accepted mathematical proofs remain the basis for uniformity in dimension and field size. The constructions described here were implemented independently from the formulas and mathematical arguments; no preceding audit program or result file supplies their computed observations.

The public evidence is [finite reconstruction](FINITE_RECONSTRUCTION.json), [optimization parity](OPTIMIZATION_RESULTS.json), [false-statement witnesses](FALSE_CONTROL_RESULTS.json), and the [evidence-file manifest](RECONSTRUCTION_MANIFEST.json). These files contain mathematical observations and verification metadata, not third-party source text or executable programs. Their hashes identify bytes, not mathematical truth.

## 1. Unconditional graph masses and actual stabilizers

### Symplectic reconstruction

All two-dimensional subspaces of the four-dimensional symplectic space over F₃ are generated once, using reduced row-echelon bases. Ninety are nondegenerate. Independently, all 81 maps F between two symplectic planes are examined. Exactly 24 satisfy F*F=I. Their graphs are therefore legitimate conjugate negative spaces and contribute unconditional mass

\[
24/90=4/15.
\]

This matches the accepted orbit–embedding quotient

\[
\frac{|\operatorname{Sp}(2,3)|^4}
 {|\operatorname{Sp}(4,3)|\,|\operatorname{Sp}(2,3)|}.
\]

Using the 24 successful graph maps as the denominator would falsely produce probability one. The corresponding false control is rejected. The test therefore measures the entire conjugacy-class denominator, rather than merely normalizing a successful chart.

A separate enumeration constructs all 729 self-adjoint operators on the four-dimensional symplectic space. An operator is represented as K=J⁻¹S with S alternating; the minimal-polynomial equation is tested directly. Each of the three irreducible quadratic minimal polynomials occurs for exactly 72 operators. This agrees with

\[
|\operatorname{Sp}(4,3)|/|\operatorname{Sp}(2,9)|=72.
\]

Replacing the extension-field symplectic centralizer by a linear torus of order eight predicts 6,480 and is rejected. The check is not based only on a characteristic-polynomial label.

### Orthogonal reconstruction

Over F₃ and F₅, both determinant classes of two-dimensional A and B are used. All linear maps F:A→B and all self-adjoint K on A are enumerated. Conjugacy-class denominators are counted independently from actual nondegenerate subspaces of A⊥B of A's discriminant. Thus both equal-dimensional discriminant possibilities are retained.

For every eligible squarefree characteristic polynomial, the operator count is exactly |O(A)|/2. The reconstruction also verifies that every polynomial satisfying the two determinant-character constraints occurs in the graph enumeration; it does not inspect only nonempty observed fibers. Each admissible fiber has exact mass

\[
\frac{|O(A)|^2|O(B)|^2}{2|O(A\perp B)|}
\]

in these codimension-zero examples. Changing |O(A)|/2 to |O(A)| is rejected. These finite cases do not independently reconstruct the positive-codimension embedding theorem; that is an accepted mathematical argument, while positive-dimensional orbit and complement formulas receive the separate subspace checks below.

Exact dimension arithmetic checks the exponent −a in both graph-weight formulas over 2,144 pairs 1≤a≤64, a≤b≤2a. Exact rational checks retain the conservative constants

\[
(7/8)^4>1/2,\qquad 2401/18432>1/8.
\]

## 2. Fourier inversion and the distinguished Cayley factors

Every monic polynomial over F₃ through degree eight, F₅ through degree five, and F₇ through degree four is inspected: 16,548 polynomials in total. Squarefreeness is determined by the polynomial gcd with the formal derivative, and the two forbidden roots are evaluated directly.

Let Tᵣ be the number surviving these tests. Coefficient extraction from

\[
\frac{1-qu^2}{(1-qu)(1+u)^2}
\]

agrees with every direct principal count. The three nontrivial evaluation-character sums independently agree with coefficients of

\[
\frac{(1+su)(1-qu^2)}{(1-u^2)^2},\qquad s=-1,-\chi(-1),-1.
\]

Fourier inversion on {±1}² reconstructs all four actual sector counts. For example, at q=3, r=8 the total is 2,457, the three nontrivial sums are all −7, and the four raw-evaluation sectors have sizes 609, 616, 616, 616. The r≥8 lower bound qʳ/16 holds in the tested applicable case. Low-degree empty sectors are retained, rather than being presented as evidence for an all-degree density theorem. A false series obtained by suppressing the excluded-prime denominator is rejected by its incorrect coefficients.

The fields F₈₁ and F₆₂₅ are constructed explicitly from quartic polynomials that are first checked to have no factors of degrees one or two. Full Frobenius degree, maximal multiplicative-order two-part, and the map

\[
\kappa=-\frac{(\lambda-1)^2}{(\lambda+1)^2}
\]

are evaluated within those fields. The respective results are 40 and 312 selected λ, 20 and 156 κ, and five and 39 irreducible κ-orbits. Each κ has full degree four and exactly two inverse-related preimages. The norms of κ and 1+κ lie in the base field and have characters (+1,−1). Reversing the latter character to +1 is rejected. This independently tests the orthogonal determinant correction, not merely the number of distinguished roots.

## 3. Subspace counts and exponent inequalities

The reconstruction generates 15,147 ambient subspaces using unique reduced row-echelon bases. Cases include symplectic dimensions four and six over F₃; both orthogonal signs in dimension four over F₃ and F₅; and an odd orthogonal five-space over F₃. Dimensions k=0,1,2 are used. Restricted eigenspace inventories are also generated independently.

For each actual basis, its Gram matrix determines singularity and nondegeneracy. Invariance under the chosen diagonal involution is decided by comparing the sum of the two projection ranks with k. The observed invariant counts agree with the decomposition convolution over i+j=k, including the products of discriminant characters for nondegenerate summands.

The singular counts agree with

\[
T(e,k)=\prod_{j=0}^{k-1}\frac{N_{e-2j}}{q^{k-j}-1},
\]

using the symplectic, odd-orthogonal, or signed even-orthogonal singular-vector count. In particular, both families of maximal singular planes in split four-space are counted. Dropping half that count is rejected. Nondegenerate counts agree with the order quotient for every occurring type, including the complement discriminant. The finite cases also satisfy the accepted rational product bounds.

A separate integer sweep checks 560,201 dimension instances through e=84. It verifies

\[
ib+ja-2ij\ge ek/12
\]

when k≤e/2 and a,b≥e/3, and

\[
ib+ja-3ij\ge ek/12
\]

when the additional singular-space restrictions 2i≤a and 2j≤b hold. The erroneous strengthening of the second lower bound to ek/3 is rejected by the feasible instance (e,a,b,k,i,j)=(12,6,6,6,3,3), whose loss is nine, not at least 24.

The auxiliary constant calculations use exact fractions: 256≤3⁸, the geometric-tail constant is below 13, and the error fits below half the target q⁻ᵉ budget. The non-subspace arithmetic separately checks 1/e+1/(e−2)≤1/6 for e=16,…,128, the projective class constant at the limiting e=16, and the exponent subtractions 192/15−1=59/5 and 59/5−1=54/5. These calculations do not verify Burness's theorem or the Liebeck–Pyber–Shalev maximal-subgroup theorem; those remain explicitly credited inspected inputs.

## 4. Quotient anti-concentration and the product obstruction

All 120 matrices of SL₂(5) are constructed. Group multiplication, inverses, commutators, and subgroup closures are computed from matrix operations. The derived subgroup has order 120 and the quotient by ±I has order 60. Every fiber of the induced conjugation action on this quotient has exactly two matrices.

The subgroup

\[
\{(x,x),(x,-x):x\in\operatorname{SL}_2(5)\}
\]

has order 240 and both projections have order 120. It is a proper subgroup of the 14,400-element product and becomes a single graph only after passing to the simple quotients. Thus the false assertion that surjective projections alone imply product containment is detected concretely. Adding the independent component element (I,u), for a standard noncentral unipotent u, generates the whole product in this model.

An order-four class has 30 elements, and a specified quotient conjugation action has two representatives in it. The resulting conditional upper bound is 2/30=1/15. A one-lift bound is rejected. Conversely, taking the two coordinates to be the same uniform class element leaves them on the diagonal with probability one. Removing the independence hypothesis and retaining 1/15 is rejected. This order-four toy class tests the algebraic fiber bound and dependence hazard; it is not a claimed instance of the large-dimensional natural-involution generation theorem.

## 5. Determinant transfer is a class-law equality

This reconstruction enumerates GL₃(3) and its determinant-one subgroup and conjugates t=diag(−1,−1,1). The 11,232-element full group and 5,616-element special group produce exactly the same 117 conjugates. Their constant conjugation-fiber sizes are respectively 96 and 48. The full centralizer has 48 elements of each nonzero determinant.

For the unitary case, F₉=F₃[i] with i²=−1 is constructed explicitly. Enumeration of orthonormal column triples gives 24,192 matrices in GU₃(3), and 6,048 in SU₃(3). The same involution has 63 conjugates in either group, with fibers 384 and 96. The centralizer has 96 matrices at each of the four norm-one determinant values. Falsely restricting that image to determinant one is rejected.

These observations reconstruct the mechanism D=J C_D(t), and consequently equality of the uniform conjugacy-class laws. They do not identify uniform special-group sampling with a pointwise nearly-uniform distribution on the full group. The latter laws have different supports and are not the inference used by the reader.

## 6. Conditioning, half-mass retention, and confidence

An exact finite probability model has one failure outcome of weight four and four successful outcomes of weight one, normalized by eight. Enumeration of four trials gives failure weight 256 and first-success weights 960 for each of the four labels. Thus the selected label is exactly uniform conditional on success. Treating the trials as two disjoint two-trial blocks gives equal joint weights 144 for all 16 pairs of successful labels, verifying preservation of independence after successful-block conditioning in this model.

For two through eight orthogonal primary factors, all sign assignments with each prescribed total discriminant are counted. Requiring the distinguished discriminant to be square retains exactly half. The false claim that the extra Ω condition costs no mass is rejected.

Logarithms used in the illustrative sample budgets are enclosed by rational bounds. After reducing x to [1,2), the identity

\[
\log x=2\sum_{j\ge0}\frac{z^{2j+1}}{2j+1},\qquad z=(x-1)/(x+1)
\]

is truncated at 48 terms with a geometric bound on the positive tail; log 2 is enclosed in the same way. No floating-point logarithm decides a check. The log n enclosures have width below 10⁻⁴⁰. The resulting values of L satisfy Lκ/log n≥log(385/η), which is the exponent budget for the block union bound.

For η=1/20, the finite calculations give:

| Marginal-family illustration | n | κ⁻¹ | L | 385L |
| --- | ---: | ---: | ---: | ---: |
| Symplectic | 49,152 | 40,000 | 3,866,915 | 1,488,762,275 |
| Orthogonal Ω-retained | 98,304 | 10,000,000 | 1,028,758,128 | 396,071,879,280 |

These deliberately conservative numbers illustrate arithmetic only. They are not practical performance estimates or an assertion that the overall generation cutoff is known numerically: the theorem still also requires n≥3d₀.

Repetition counts are checked by exact rational powers of ten. For δ=1/20, two repetitions are required; rounding down to one is rejected. A separate finite counterexample records that ten trials of success probability 1/10 still miss with probability (9/10)¹⁰=0.3486784401. A fixed-error guarantee cannot be advertised as an automatically vanishing-error guarantee. The accepted analytic quantifier discussion, rather than this one finite example, explains the asymptotic boundary.

## 7. Scope guards and what is not certified

Enumeration of SL₂(3)=Sp₂(3) finds only I and −I with square one, neither strong on a plane. This detects the false all-dimensions marginal statement. In the symplectic boundary example with t-eigenspace dimensions 16,384 and 32,768, equal negative dimensions would have to be 32,768/3 for simultaneous strength; there is no such integer dimension. The false promotion of the two marginal events to a simultaneous guarantee is rejected.

At the respective smaller-factor thresholds 8,192 and 32,768, every integer b between a and 2a and both balance intervals are checked with exact rational endpoints. The powers of two are 128 and 512, and the minimum number of permitted odd multiples is six, above the certified lower bound 8/3.

This certificate does not extend the reader to characteristic two, arbitrary projective involutions with order-four lifts, similitudes, non-natural representations, small-dimensional generation exceptions, dependent or merely unspecified random samples, or total computational running time. It does not numerically specify the published absolute maximal-subgroup constant or the resulting overall dimension cutoff. It does not use the historically unverified Praeger–Seress 2011 article to certify the current conclusion: the accepted 192-class replacement remains the active generation input.

## 8. False-control coverage and reproducibility boundary

The fifteen rejected modifications are: omitting the Fourier denominator; normalizing only by the successful graph chart; substituting a linear torus for the symplectic centralizer; removing the orthogonal operator half-count; reversing the distinguished determinant character; dropping one split maximal-singular family; strengthening the subspace exponent falsely; suppressing the second central lift; inferring a product from its projections; removing component independence; restricting the unitary determinant image; making Ω retention free; rounding amplification down; extending the positive marginal to every dimension; and replacing separate marginal guarantees by simultaneous balance.

Every rejection is an ordinary explicit exception with exit status two, and its mathematical witness is recorded. A crash, timeout, surviving mutation, changed optimization-mode output, or missing observation is not accepted as a successful negative control. The replay contract bounds each process by 90 seconds and the complete reconstruction by 360 seconds; enumeration domains are fixed. Output contains no clock-dependent measurements or random seed effects. The executable replay materials are kept outside this public mathematical packet.
