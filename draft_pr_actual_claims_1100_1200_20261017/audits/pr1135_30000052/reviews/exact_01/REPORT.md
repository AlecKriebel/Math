# Independent exact-cell audit of PR #1135

Decision: **MATHEMATICS PASS, FULL NEGATIVE TARGET RESOLUTION.** The exact integrals calculated from the defining model give

\[
 E\operatorname{disc}_4(M_3^{z,\Delta})^4=\frac{19}{1620}
 >\frac4{405}=E\operatorname{disc}_4(M_3^{\rm iid})^4.
\]

The excess is \(1/540\), and the ratio is \(19/16\). I found no mathematical repair needed in the supplied proof. The supplementary four-point value \(139/17280\), the four-point tail lower bound, the second-moment statement, and the equality of the complete one- and two-point laws also pass. This is an internal AI-assisted adversarial mathematical review, not human peer review or a priority determination.

## Frozen scope and independence

Inputs are the ten files in `../../inputs`, authenticated by `INPUT_PINS.json` and copied into both program outputs. The reviewed PR head supplied by the parent is `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`; the parent authenticates its relationship to the GitHub PR. I read the candidate's proof, verification narrative, source review, status, and earlier audit, but imported or reused none of their code or private artifacts. All new work is confined to this review folder; no repository branches, index, references, remotes, PR state, comments, or publication records were modified.

The new implementation integrates directly over affine strips in the full generator/shift square. It uses neither the candidate's triple-inclusion probabilities, the author's floor/permutation polygon clipping, nor the previous audit's shift integration followed by rational interpolation. It uses only Python's standard library and exact `Fraction` arithmetic.

## Original target checked

I fetched the [official EMS report](https://ems.press/content/serial-article-files/45858) afresh, extracted context on printed pp. 696–699, and visually inspected printed pp. 697–698 with the PDF skill. The PDF has 445,532 bytes and SHA-256 `2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e`.

Novak's contribution, reporting joint work with Hinrichs, defines anchored normalized indexed counting, discusses even exponents, and asks the comparison of expected p-th powers. Its generalized lattice uses all indices from zero to n minus one, and product Lebesgue averaging over the entire generator/shift cube. Thus the present one-dimensional fourth-moment example satisfies the displayed question. No rational-generator, primality, or well-distribution restriction is present. The later existence question for good lattices is separate and is not resolved by this counterexample.

## A complete cell partition

Fix an integer \(n\ge1\), and let

\[
 \mathcal F_n=\{0,1\}\cup
 \{k/m:1\le m\le n-1,\ 1\le k<m\}.
\]

Arrange these finitely many rational values in increasing order. On an open consecutive generator interval \(I=(a,b)\), no \(jz\), \(1\le j<n\), is integral. Put \(K_j=\lfloor jz_*\rfloor\) at any interior witness \(z_*\). The only interior shift at which point \(j\) wraps is the affine line

\[
 \Delta=h_j(z)=K_j+1-jz.
\]

The functions \(h_j\), together with zero and one, have a fixed strict ordering on \(I\). Indeed, crossing zero or one requires \(jz\) integral. A crossing of \(h_i\) with \(h_j\) requires \((j-i)z\) integral. All such interior crossings are in \(\mathcal F_n\), which is impossible inside \(I\). There are exactly \(n\) open strips between the ordered boundaries.

Each strip is

\[
 C=\{(z,\Delta):a<z<b,\ \ell(z)<\Delta<u(z)\},
\]

where \(\ell,u\) are affine with rational coefficients. Its closure is a triangle or a quadrilateral, possibly with repeated endpoint vertices. On this strip every floor
\(f_j=\lfloor jz+\Delta\rfloor\) is constant, hence
\(t_j=jz+\Delta-f_j\) is affine. The order of the points is constant: a tie of two such affine expressions would again require \((j-i)z\) integral. A single strict interior sample therefore identifies both all modular floors and the sorting permutation on the whole strip.

These cells cover the entire unit square except their finitely many line-segment boundaries. There is no conditioning or deletion of a positive-measure set. On every generator interval the shift strips telescope from zero to one; their interiors are disjoint. Their combined area is exactly one. Endpoint generators, point collisions, and wrap events on the omitted boundaries are null under product Lebesgue measure, so including them by any consistent convention does not change the expectation.

The program verifies each cell at all four endpoint vertices. Because each floor range and order inequality is affine, validity at those vertices implies validity throughout the convex closed cell. It also tests 2,702 exact rational interior witnesses across point counts one through seven, requiring unique cell membership and the independently computed floors and point order. The coverage proof, rather than those finite witnesses, establishes exhaustiveness.

## Direct exact integration, with no fitted degree

Let \(s_1\le\cdots\le s_n\) be the sorted points on a cell, and set \(s_0=0\), \(s_{n+1}=1\). For even \(p\ge2\), integration over the anchored-box endpoint first gives the exact deterministic identity

\[
 \operatorname{disc}_p^p
 =\frac1{p+1}\sum_{k=0}^n
 \left[(s_{k+1}-k/n)^{p+1}-(s_k-k/n)^{p+1}\right].
\]

This follows by integrating \((x-k/n)^p\) over each interval \((s_k,s_{k+1})\); for even p this equals the required absolute p-th power. Zero-length intervals and tied endpoints make zero contributions, so the deterministic identity still holds for coincident indexed points. For odd exponents this removal of the absolute value would be invalid, and the program explicitly rejects that input.

Every term on a cell is a power \(L^m\) of an affine form
\(L=A z+B\Delta+C\), with \(m=p+1\). If \(B\ne0\), direct integration in the shift gives

\[
 \int_{\ell(z)}^{u(z)} L^m\,d\Delta
 =\frac{[Az+Bu(z)+C]^{m+1}-[Az+B\ell(z)+C]^{m+1}}
 {B(m+1)}.
\]

If \(B=0\), it gives \((Az+C)^m[u(z)-\ell(z)]\). In either case the result is an explicit rational polynomial in z. The code expands by exact polynomial multiplication and integrates each coefficient by
\(\int_a^b z^r dz=(b^{r+1}-a^{r+1})/(r+1)\).
For \(B\ne0\) its degree is at most \(p+2\), and for \(B=0\) it is at most \(p+2\) as well. This bound is descriptive: no interpolation, reconstruction assumption, numerical quadrature, or degree truncation is used.

For n = 3 the resulting complete cell table is as follows. Pairs in the boundary columns are the coefficients (slope, constant) of the shift boundary.

| Generator interval | Lower shift | Upper shift | Floors (0,1,2) | Point order | Area | Fourth-moment integral |
|---|---|---|---|---|---|---|
| (0,1/2) | (0,0) | (-2,1) | (0,0,0) | (0,1,2) | 1/4 | 79/15552 |
| (0,1/2) | (-2,1) | (-1,1) | (0,0,1) | (2,0,1) | 1/8 | 61/155520 |
| (0,1/2) | (-1,1) | (0,1) | (0,1,1) | (1,2,0) | 1/8 | 61/155520 |
| (1/2,1) | (0,0) | (-1,1) | (0,0,1) | (0,2,1) | 1/8 | 61/155520 |
| (1/2,1) | (-1,1) | (-2,2) | (0,1,1) | (1,0,2) | 1/8 | 61/155520 |
| (1/2,1) | (-2,2) | (0,1) | (0,1,2) | (2,1,0) | 1/4 | 79/15552 |

Their areas sum to one, and their integrals sum to
\(2(79/15552)+4(61/155520)=19/1620\).

For n = 4 the generator intervals have endpoints
\(0,1/3,1/2,2/3,1\), producing 16 strips. The full individual records are in both result files. Grouping equal contributions yields

\[
 2\frac{3199}{933120}
 +4\frac{811}{5598720}
 +2\frac{79}{1399680}
 +4\frac{301}{11197440}
 +2\frac{1447}{11197440}
 +2\frac{241}{3732480}
 =\frac{139}{17280}.
\]

The advertised n = 3 and n = 4 lattice fractions are outputs of this integration. Neither is a constant in the implementation.

## Independent iid calculation and controls

For iid points the count at x is binomial. Expanding the entire binomial law gives a second direct exact calculation:

\[
 E\operatorname{disc}_p(M_n^{\rm iid})^p
 =\sum_{k=0}^n\sum_{a=0}^p
 \binom nk\binom pa(k/n)^{p-a}(-1)^a
 \frac{(k+a)!(n-k)!}{(n+a+1)!}.
\]

The factorial fraction is the elementary integer beta integral of
\(x^{k+a}(1-x)^{n-k}\). The program evaluates this whole sum; it does not use the candidate's closed fourth-moment formula to generate the comparator. For p = 4 its independently calculated values agree with \((3n-1)/(30n^3)\) for n = 1 through 7. In particular the iid values are \(4/405\) at n = 3 and \(11/1920\) at n = 4.

The direct-cell calculations cover all n from one through seven and p in {2,4,6,8}, making 28 exact lattice/iid moment pairs. The numbers of cells are respectively 1, 2, 6, 16, 30, 60, 84. All second moments equal \(1/(6n)\), and every tested exponent has identical lattice/iid values at n = 1,2. The additional values are controls, not a claim to have classified every parameter or established any monotonicity beyond the stated counterexamples.

The general control statements have short proofs independent of finite computation. For distinct j,k, the point \(t_j\) is uniform and independent of z, since conditional on z the independent uniform shift is translated. Multiplication of a uniform circle variable by the nonzero integer k-j preserves its uniform law. Thus, conditional on \(t_j\), the point \(t_k=\{t_j+(k-j)z\}\) is uniform. Coordinatewise independence proves the same statement for vectors in every dimension.

An anchored box of volume \(v=\prod_r x_r\) therefore has count variance \(nv(1-v)\). Its squared normalized discrepancy expectation is \(v(1-v)/n\). Integrating v and its square gives

\[
 E\operatorname{disc}_2^2=\frac{2^{-d}-3^{-d}}n
\]

for both ensembles and every n,d. The 49 dimensional formula evaluations in the result files are evaluations of this proved expression, not independent numerical evidence for the infinite statement.

For n = 1 there is one uniform point. For n = 2 the map
\((z,\Delta)\mapsto(\Delta,\{z+\Delta\})\) preserves the product uniform law: condition on the first coordinate and the second remains uniform. Consequently the complete ordered two-point laws agree with iid in every dimension, and all measurable discrepancy functionals agree whenever their expectations are defined. This proves the asserted minimal point count, without relying only on the four checked exponents.

## Whole-proof adversarial checks

The main analytic proof's lower-half triple-event calculation is also correct. In independent uniform coordinates u = t0 and v = t1, t2 = {2v-u}. For 0 <= x <= 1/2, the negative branch wraps outside [0,x), and the positive branch does not wrap. For each u in [0,x), v has admissible interval [u/2,(u+x)/2), of length x/2. This gives q = x squared divided by two. Pairwise independence then supplies the remaining count probabilities. The fourth-moment polynomial and simultaneous-reflection argument integrate to the same value as the direct cells. Crucially, the lower-half formula is not extended to x = 1 and pairwise independence is not substituted for joint independence.

The independent tail argument is valid. On the ascending no-wrap triangle the two empty tails contribute
\([\Delta^5+(1-\Delta-(n-1)z)^5]/5\). Integrating the shift and then the generator gives \(1/[105(n-1)]\). The reflected descending triangle gives the same amount. Their interiors are disjoint for n >= 3, including the borderline n = 3 case where generator intervals share only an endpoint. All omitted contributions are nonnegative. Thus the lower bound is \(2/[105(n-1)]\). At n = 4 it exceeds iid by \(5/8064\), while the complete direct-cell value exceeds iid by \(1/432\). At n = 3 that lower bound alone is insufficient, as explicitly checked.

No collisions are removed or conditioned away. Boundary counts at fixed configurations change the integrand only at finitely many x endpoints; parameter boundaries have zero area. Absolute values, the coefficient 1/n, continuous averaging, and the distinction between a norm expectation and a p-th-power expectation are all essential and retained.

## Reproduction, adverse controls, and limitations

`python3 check_cells.py` and `python3 -O check_cells.py` produce byte-identical JSON. The finalized run makes 11,120 explicit requirements in each mode. All use exceptions rather than assertions, so optimization leaves them active. The eleven recorded adverse controls catch: invalid point count; an odd exponent without absolute-value splitting; a missing generator breakpoint; a corrupted modular floor; a reversed interior order; a duplicated index; a deleted positive cell; lost 1/n normalization; a joint-iid substitution; a zero generator substituted for generator averaging; and misuse of the three-point tail bound.

Both modes also reject the explicit `--negative-guard` invocation after running the full calculation. Input integrity is checked against the frozen ten-file inventory before calculation. The separate replay receipt records normal/optimized outputs and negative-guard status, and additional integrity mutation receipts identify altered frozen-input copies rejected in both modes. All mutations are confined to ignored temporary mirrors.

The code is corroboration of the standalone direct-cell derivation. It is neither formal proof-assistant certification nor an exhaustive software-correctness proof. This task did not perform a new global priority search. No claim of historical novelty or continued openness follows from the mathematical acceptance.

**Final assessment:** no unresolved mathematical concerns in the complete negative answer or its stated supplementary/control claims. Completion toward this assigned mathematical reproduction/audit: **100%**. The parent's subsequent priority and publication decisions remain separate.
