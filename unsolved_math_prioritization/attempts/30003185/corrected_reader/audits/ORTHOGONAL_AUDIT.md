**Integrated reader status.** The marginal theorem is accepted. Its original remaining-generation boundaries are closed by the later accepted stages. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Independent audit: natural orthogonal Bray marginal bound

## Verdict

**Accepted within the exact stated scope.** The audited proof establishes the following mathematical proposition, rather than merely a numerical conjecture:

For every odd prime power q, every nondegenerate quadratic space V of natural dimension n at least 98,304, every G equal to O(V), SO(V), or Ω(V), and every strong involution t actually belonging to G, a uniform g in G satisfies, for either fixed eigenspace E of t,

P(inv(t t^g)|_E is strong) > 1/(5,000,000 log n).

The logarithm is natural, and the two eigenspaces have separate marginal guarantees. Both even-dimensional Witt types, both discriminant classes in odd dimension, unequal eigenspace dimensions, and equal-dimensional eigenspaces of different discriminants are covered. No substantive gap was found in this proposition.

The audited artifact is *A uniform marginal bound for natural orthogonal groups*, filename `ORTHOGONAL_MARGINAL_PROOF.md`, 19,061 bytes, SHA-256 `18111968da08d3aa61677d07628dbf5092af60526ed9213ccb772079cba7cf2b`. This acceptance applies to those bytes. It does not assert a completed centralizer-generation algorithm, projective versions, or the result in small dimensions.

## 1. Discriminant, Witt type, and spinor conventions

The proof consistently uses the determinant square class of the symmetric bilinear form β, with Q(v)=β(v,v)/2. This avoids the occasionally different signed-discriminant convention. In dimension 2m the split condition is χ(det β)=χ((-1)^m). In a fixed dimension over an odd finite field, dimension and this determinant square class classify nondegenerate forms. Thus equal-dimensional spaces must retain their actual determinant classes even when their abstract odd-dimensional orthogonal groups are isomorphic.

The spinor norm is normalized using Q(v) on a reflection. Replacing Q(v) by β(v,v) multiplies each reflection norm by 2; every determinant-one isometry is a product of an even number of reflections. Hence its spinor norm, and therefore Ω, is unaffected. The proof does not conflate the determinant of a quadratic-form matrix with an unadjusted reflection convention.

The conjugacy-orbit reduction is valid. Each strong t-eigenspace has dimension at least three, contains a hyperbolic plane, and represents both nonzero square classes. Its reflections, extended by the identity on the other eigenspace, lie in C_O(t) and realize both (-1,+1) and (-1,-1) under (det,χθ). They generate the quotient O/Ω. Consequently O=Ω C_O(t), and the O-class of this particular t is one Ω-class and one SO-class. Uniform conjugation in each of these three groups therefore induces the same class measure.

Replacement of t by -t is used only after this reduction to uniform O-conjugation. The identity (-t)(-t)^g=t t^g holds regardless of whether -t belongs to the initially specified SO or Ω. The original labels of the target eigenspaces are simply exchanged when necessary. There is no hidden assumption that -I belongs to the sampling subgroup.

For example, genuine membership of an involution in SO requires an even-dimensional negative eigenspace. In Ω it additionally requires trivial spinor norm; in that even dimension this is equivalent to the negative space's bilinear determinant being square. The theorem starts with t in G and does not silently assert the existence of an involution of every arbitrary type in G.

## 2. Orthogonal graph constraints and fibers

Write V=A perpendicular-direct-sum B with dim A=a≤b=dim B, and t negative on A. For F:A→B, K=F*F is self-adjoint. Invertibility of K makes F injective with nondegenerate image. The graph W has form β_A(I+K), so its isometry type agrees with A exactly when det(I+K) is square. This constraint cannot be discarded in an orthogonal count.

The equation F*F=K is exactly an isometric-embedding problem from A_K, whose determinant is disc(A)det K, to B. In positive codimension c=b-a, the complement has the uniquely determined dimension and determinant disc(B)/(disc(A)det K). Both determinant classes exist in every positive dimension. In codimension zero the embedding exists exactly when det K has character χ(disc(B)/disc(A)); the complement group then has order one. These cases are treated correctly.

For fixed K, O(B) is transitive on the embeddings, with pointwise stabilizer O(C). Thus the fiber size is |O(B)|/|O(C)|. Fixing the character of det K makes the complement type fixed, so a single denominator may legitimately be used in the subsequent sum.

No graph multiplicity is lost: a subspace in this chart determines F uniquely by its projection onto A. The class size remains |O(V)|/(|O(A)||O(B)|), including a=b; the centralizer of t preserves its two labeled eigenspaces and cannot exchange them.

## 3. Squarefree self-adjoint class weights

The orthogonal calculation is materially different from the symplectic one. For a squarefree characteristic polynomial f of degree a with s irreducible factors, each primary space is one-dimensional over its extension field L_i. The balanced symmetric forms on that primary space are precisely Tr(c_i uv). There are two classes modulo changes of extension-field basis, and each has isometry centralizer {+1,-1}.

The primary projections are polynomials in K and are self-adjoint, so distinct primary spaces are perpendicular. Multiplying one c_i by a nonsquare multiplies its F_q-determinant by Norm(c_i), which is nonsquare because χ_q(Norm x)=χ_L(x). Exactly half of the 2^s form-class choices therefore have the prescribed determinant of A. The sum over all admissible K-classes is

2^(s-1) |O(A)|/2^s = |O(A)|/2.

This is a sum of genuine orthogonal conjugacy-class weights. It is not a copied linear torus count, a symplectic centralizer count, or a claim of uniform K under uniform conjugation.

The two determinant characters are χ((-1)^a f(0)) and χ((-1)^a f(-1)). Both signs, including the degree parity, are retained.

## 4. Unconditional probability mass

Combining the class denominator, the embedding fiber, and the sum of self-adjoint K-classes gives, for each admissible f,

P_f = |O(A)|² |O(B)|² / (2 |O(V)| |O(C)|).

This is unconditional probability mass in the full conjugacy class. There is no uncounted conditioning on the chart.

The exponent of q in this expression is exactly -a:

a(a-1)+b(b-1)-((a+b)(a+b-1)+(b-a)(b-a-1))/2 = -a.

The standard order formulas give normalized orders between 7/6 and 8/3 in every positive dimension and for both form types; the zero-dimensional normalized order is one. Thus

P_f ≥ q^(-a) (7/6)^4 / (2(8/3)^2)
    = q^(-a) 2401/18432
    > q^(-a)/8.

The strict final inequality is correct, and the argument also covers c=0. A separately checked public source for the order formulas is Peter J. Cameron's *Classical Groups*, Chapter 6, printed pp.65–66: https://maths.qmul.ac.uk/~pjc/class_gps/ch6.pdf . The proof additionally cites D. E. Taylor's corrected *The Geometry of the Classical Groups*: https://www.maths.usyd.edu.au/u/don/papers/gcg.pdf .

## 5. Spectrum, determinant sectors, and negative dimensions

Direct multiplication reproduces the displayed 2-by-2 block matrix for t s_W. Its scalar relation is

κ=-(λ-1)²/(λ+1)².

For κ different from 0 and -1, the reciprocal eigenvalues are distinct and neither equals +1 or -1. Squarefreeness of f gives semisimplicity. All eigenvalues in a primary block have the same order 2-part, since Frobenius and inversion preserve order.

A uniquely maximal order 2-part greater than one makes inv(t s_W) negative on the whole corresponding 2k-dimensional block and positive elsewhere. Its negative dimensions in A and B are each k. The complement C in B is fixed and remains part of the positive eigenspace. The proof's B-balance interval accounts for it.

For k divisible by a power of two d≥4 but not by 2d, selecting maximal-2-part λ in F_(q^k) gives at least q^k/(8k) irreducible κ-polynomials of degree k. The proper-subfield bound is sufficient even at q=3,k=4. A κ of degree k/2 would force λ into the norm-one group of order q^(k/2)+1, whose 2-part is two because k/2 is even, contradicting the selected order 2-part. The two-to-one λ-to-κ map and division by the k-element Frobenius orbit are correct.

This factor has det K character +1 and det(I+K) character -1: κ is square in the even-degree extension, while 1+κ=4λ/(λ+1)² is nonsquare. Norms preserve the quadratic character. A remainder of sector (α,-1) therefore produces total sector (α,+1), as needed.

The 2-adic order comparison is valid for both split and norm-one eigenvalues. Excluding remainder factor degrees divisible by d makes all their order 2-parts strictly smaller than the distinguished one.

## 6. Character-series calculation and small-q protection

The three raw-evaluation characters on polynomials coprime to X(X+1) have degree-one sums respectively

-1, -χ(-1), -1,

and zero sums in every degree at least two. The product-character identity is the elementary sum of χ(c(c-1)), equal to -1. Hence their Dirichlet polynomials are 1-u, 1-χ(-1)u, and 1-u.

Their squarefree series are exactly

(1+s u)(1-q u²)/(1-u²)², with s equal to +1 or -1.

The denominator uses the principal character excluding both linear factors. Forgetting those factors would give an incorrect series; the audited proof includes them. The nontrivial coefficients have absolute value at most qr/2 for r≥1. Replacing raw evaluations by determinant characters only changes the prescribed signs by χ(-1)^r.

Together with T_r≥q^r/3, four-sector Fourier inversion gives each prescribed determinant sector at least q^r/12-3qr/8. The sufficient inequality 18r≤q^(r-1) holds for all odd q≥3 and r≥8, yielding q^r/16. No all-degree sector-density claim is made: the exact controls exhibit empty sectors at q=3, r=1 and r=2.

The exclusion of factor degrees divisible by d removes at most q^r(1+log a)/d globally. Taking d≥32(1+log a) leaves q^r/32 in every desired sector. This is subtraction of an unconditional union bound, not an independence assumption about factor degrees and determinant signs.

## 7. Thresholds, intervals, and final constant

At n≥98,304, the smaller eigenspace dimension a is at least 32,768. The least power of two d at least 32(1+log a) satisfies d<64(1+log a) and a>24d. The latter follows from a≥1536(1+log a); the left-to-right ratio is increasing beyond the threshold.

For A the interval is [a/3,2a/3]; for B it is [b/3,min(2b/3,5a/6)]. For every a≤b≤2a these intervals have length at least a/6, lie above a/3, and end no later than 5a/6. Therefore they contain at least a/(24d) integers of the form d times an odd integer. The remainder degree is at least a/6, so the sector lemma's r≥8 restriction is amply satisfied.

The distinguished factor is the only irreducible factor whose degree is divisible by d. This makes the counting representation unique and prevents overcounting across k. The polynomial count is at least q^a/(6144d); combining it with the graph mass gives a probability strictly greater than 1/(49152d), hence greater than 1/(3145728(1+log a)).

The logarithm conversion correctly uses 1+log a<(4/3)log n. In the orthogonal problem only n≥2a is available, so the stronger symplectic inequality 1+log a<log n would not be justified. The actual proof uses the valid conversion, yielding 1/(4194304 log n) and then the advertised relaxed constant 1/5,000,000.

## 8. Independent exact controls

The finite reconstruction uses exact finite-field arithmetic and rational numbers. Its controls are supplementary evidence, not the basis of the analytic acceptance.

- Exhaustive squarefree character-sector counts cover 272,267 monic polynomials: F_3 through degree 10, F_5 through degree 7, F_7 through degree 5, and F_9 through degree 5. All principal counts, all three nontrivial character sums, degree-parity conversions, and the applicable sector bounds agree exactly.
- Exhaustive self-adjoint counts cover 33,698 matrices, including both determinant classes in dimensions two and three. Every eligible characteristic polynomial contributes exactly |O(A)|/2 operators.
- Exhaustive graph counts cover 146,972 maps over F_3 and F_5, including equal dimensions, unequal dimensions, and all tested input discriminant pairs. Every nonempty admissible polynomial fiber matches the exact formula. Empty low-dimensional sectors also match the predicted constraints.
- Separate positive-codimension controls count embeddings of both nondegenerate two-dimensional source types into both four-dimensional target types over F_3, F_5, and F_7. These test the complement determinant and O(C) stabilizer in nonvacuous codimension-two cases.
- Reflection controls verify representation of every nonzero value by both three-dimensional determinant classes over F_3, F_5, F_7, and F_9, realizing both determinant/spinor reflection cosets.
- Four extension-field controls use (q,k)=(3,4),(5,4),(7,4),(3,8). Their numbers of distinguished irreducible factors are respectively 5, 39, 150, and 205. Every selected factor has degree k, the asserted two-to-one λ fiber, and determinant characters (+1,-1).
- Seventy-two threshold/balance controls include the minimum a, dimensions immediately above it, larger dimensions, equal eigenspace dimensions, and b=2a boundary cases. All interval counts and constant comparisons pass.

The [stage certificate](../certificates/ORTHOGONAL_STAGE.json) contains the exact outcomes. No Monte Carlo sampling or floating-point group arithmetic is used; floating-point logarithms are confined to supplementary checks of already-proved analytic threshold inequalities.

## 9. Remaining boundaries

The accepted theorem is restricted to natural linear involutions in the three named isometry groups and to uniform sampling. It does not itself cover projective involutions with order-four lifts, arbitrary similitude groups, other sampling subgroups, characteristic two, or dimensions below the threshold. A nearly-uniform version would require stating and applying the pointwise density comparison; none is silently substituted here.

The full Bray centralizer-generation claim remains outside this acceptance. One must still supply a correctly scoped class-random generation result and a direct-product/subdirect-product argument that reaches the specified derived subgroup. Obtaining a strong involution in each fixed eigenspace with the proved marginal probability is not, by itself, that generation theorem. In particular C_G(t), C_G(t)'', and its last derived subgroup are not interchangeable without an additional argument.

The original source target is Cheryl E. Praeger's *Finding strong involutions in finite classical groups in odd characteristic*, OWR 37/2016, printed pp.2160–2161, DOI https://doi.org/10.4171/OWR/2016/37 . The linear and unitary results are prior literature, and this audit makes no worldwide novelty or openness certification.
