# Independent spectral and concentration derivations

These are deductions checked for the frozen candidate, not assertions that finite code proves an asymptotic theorem. Symbols agree with frozen `PROOF.md`. The target fixes all factor alphabets and density before the length varies.

## 1. Uniform endpoint compression, including unequal lengths

Write `v_t(a,b)` for the number of allowed, non-inverse-fixed blocks with endpoints `(a,b)`. An involutory reduced word has odd length `2s+1`, is determined by its first `s` letters and its self-inverse central letter, and ends in the inverse of its first letter. Uniformly in the finitely many endpoint pairs, deletion is `O(lambda^s)`. The Perron main term of `A^(t-1)` is strictly positive in every entry. Consequently `v_t(a,b) ~ lambda^(t-1) r_a r_b`, including endpoint pairs in the same factor once `t` is sufficiently large. No estimate here requires a uniform constant over different alphabets.

For a link incidence `(x,y)` of lengths `(t,u)`, put endpoints `(a,b)` and `(c,f)`. Holding the corner fixes the boundary condition `A[a,c]`; the last block contributes `T_(ell-t-u)(b,f)`. Reversed incidences and fixed-position cyclic incidences count the same number of completions, because inversion preserves each factor and the remaining-block completion is symmetric. Therefore the unnormalized expected adjacency entry, up to the common `N/Z` factor, is

`c_tu A[a,c] T_(ell-t-u)(b,f)`.

The destination class has `v_u(c,f)` vertices. Its contribution has asymptotic value

`c_tu lambda^(ell-t) A[a,c] r_b r_c r_f^2`.

Summing over `(c,f)` uses two distinct identities:

`sum_f r_f^2=1`, and `sum_c A[a,c]r_c=lambda r_a`.

Thus the degree is asymptotic to `(N/Z) h_t lambda^(ell-t+1) r_a r_b`. Dividing yields exactly the limiting compressed row

`(c_tu/h_t) [A[a,c]r_c/(lambda r_a)] r_f^2`.

In particular the last-coordinate weight is `r_f^2`, rather than a uniform letter weight or `r_f`. The stationary mass of an entire endpoint class is asymptotic to

`(N/Z) lambda^ell h_t r_a^2 r_b^2`.

The factor `lambda^t` from the number of length-`t` vertices cancels the inverse factor in their individual expected degrees. This explains why unequal numbers of vertices in the two length types do not introduce a missing extra Perron factor. For residues one and two, type masses are respectively `(2/3,1/3)` and `(1/3,2/3)`, in increasing-length order.

## 2. Spectral separation

The quadratic form for multipartite `A` is nonpositive on the codimension-one subspace whose total coordinate sum is zero. Its positive index is at most one. Primitivity supplies one simple positive Perron eigenvalue and strict modulus separation of all other eigenvalues. Reversibility makes `P` similar to `A/lambda`, so its remaining spectrum lies in `[-rho,0]`, with `rho<1`.

The exact endpoint compression has bounded dimension, real eigenvalues, and entrywise limit `Q tensor P tensor R`, where `R` has all rows `r_f^2`. Every function in the image of the full expected walk is constant within its endpoint class. Therefore the nonzero full-walk spectrum is exactly the compressed nonzero spectrum; the remaining eigenvalues are zero. The eigenvalue one of the limiting tensor product is simple.

For equal types, all other tensor eigenvalues are nonpositive or zero. For unequal types, `Q` has eigenvalues one and `-1/2`; multiplying the latter by negative eigenvalues of `P` gives additional positive eigenvalues, at most `rho/2`. Thus the limiting Laplacian gap is at least `1-rho/2`, and the chosen

`gamma = 1/2+(1-rho)/4`

has a strict spare margin `(1-rho)/4`. Continuity of fixed-dimensional characteristic polynomials, together with reversibility, suffices for an eventual lower bound `gamma`. A disconnected expected graph would have more than one eigenvalue one and contradict simplicity in a sufficiently small spectral neighborhood of the limit. This argument applies separately to all three residues, then takes the largest of their three starting lengths.

As a check against an unjustified uniform claim, factor part sizes `(1,1,s)` have Perron root `(1+sqrt(1+8s))/2` and a negative root `1-lambda`. Their `rho` tends to one as `s` increases. The gap margin can therefore shrink with the alphabet. This does not affect the stated fixed-parameter theorem.

## 3. The random matrices and exact constants

Every retained sample contributes three undirected edge Laplacians. One edge is `(e_x-e_y)(e_x-e_y)^T`, positive semidefinite with norm two. Summing three gives norm at most six, even when the edges coincide. A block occurrence contributes one endpoint at its formal letter and one at its formal inverse. Because these are distinct after deletion, any fixed vertex receives at most one degree contribution per block position, hence degree contribution at most three. Three equal cyclically reduced blocks attain degree three and Laplacian norm six; replacing these bounds by two and four would be wrong.

The sample matrices are independent, including their zero values on rejected samples. The edges within one sample need not be independent. Let `barD` be the deterministic expected degree matrix, and `delta` its least diagonal entry. With

`X_j=barD^(-1/2)L_j barD^(-1/2)` and `z=barD^(1/2)1`,

each `X_j` is positive semidefinite, has norm at most `6/delta`, and kills the same deterministic vector `z`. Restriction to its orthogonal complement preserves independence, positivity, and the bound. The restricted expectation has minimum eigenvalue `mu>=gamma`. Applying Tropp's lower-tail estimate there gives dimension factor `M-1`, bounded by `M`, and exponent `-epsilon^2 mu/(2*(6/delta))`. For the weaker threshold `(1-epsilon)gamma`, containment in the theorem's failure event and `mu>=gamma` give exactly

`M exp(-epsilon^2 gamma delta/12)`.

On the full space the expectation has minimum eigenvalue zero, so applying a positive-minimum Chernoff bound without this restriction would not be valid. No random subspace is used.

For the degree of one fixed vertex, use the scalar case with summand bound three and mean `bar d_x`. The exact upper-tail exponent is

`-[(1+epsilon)log(1+epsilon)-epsilon]bar d_x/3`.

For `0<epsilon<1`, the bracket is at least `epsilon^2/3`. A union bound over vertices gives exactly `M exp(-epsilon^2 delta/9)`. Independence of degrees at different vertices is unnecessary.

From the endpoint estimate, positivity of the finitely many Perron coordinates, and the integer floor in `N`, one obtains `delta >= c lambda^(d ell-ceil(ell/3))` eventually, while `M<=C lambda^ceil(ell/3)`. For fixed `d>1/3`, `delta` grows exponentially in `ell`; it dominates `log M=O(ell)` in both failure bounds. At `d=1/3` this reasoning does not supply that domination.

## 4. Changing the degree matrix: direct variance proof

Here is an alternative to the correctly used generalized max-min principle in the frozen proof. Define

`Var_W(g) = min_c sum_x W_xx (g_x-c)^2`

for a positive diagonal matrix `W`. On the matrix-concentration event,

`g^T L g >= (1-epsilon)gamma Var_barD(g)`.

This follows by subtracting the `barD`-weighted mean from `g`; the Laplacian quadratic form does not change. The inequality also proves connectivity before any normalization by actual random degrees: a second component-constant kernel vector would have strictly positive `Var_barD`. Since there are many vertices, connectivity forces all actual degrees positive.

On the degree-control event `D <= (1+epsilon)barD`, evaluating the actual variance at the minimizing constant for the expected variance gives

`Var_D(g) <= (1+epsilon) Var_barD(g)`.

Consequently

`g^T Lg >= [(1-epsilon)gamma/(1+epsilon)] Var_D(g)`.

This is exactly the desired lower bound for the actual normalized Laplacian gap. It neither assumes nor requires the expected-mean-zero vector to have zero actual weighted mean. Choosing `epsilon<(2gamma-1)/(2gamma+1)` makes the ratio strictly greater than one half.

## 5. Criterion and torsion

The source criterion used here is the precise presentation criterion as stated in Kotowski--Kotowski v2, Definition 2.12 and Theorem 2.13; its text explicitly allows link multiple edges, excludes loops under cyclic reduction, and uses the normalized, degree-weighted Laplacian. Its random-presentation model explicitly allows repeated relators. Applying global formal inversion to every link vertex changes their edge convention `{u,v^(-1)}` into the candidate's `{u^(-1),v}`. This is a graph isomorphism preserving all edge multiplicities and normalized spectra.

Generators here are formal inverse pairs, even when their images in the eventual quotient acquire torsion, coincide, or become trivial. The deletion of inverse-fixed source blocks makes this formal alphabet well defined without order-two formal generators. An adjacent formal inverse pair would create two adjacent syllables in the same source factor, contrary to the chosen relator space, so every retained triangular relator is cyclically reduced. No torsion-free-group or torsion-free-presentation hypothesis is added by the stated criterion. Repeated samples are repeated triangular cells/relations with their corresponding link weights; the underlying presented group does not change.

The epimorphism to the subgroup generated by source blocks is well defined by the retained original relators. The suffix argument in the candidate supplies every product of two alphabet letters for `L>=4`; the quotient by those products has order at most two. Thus the image subgroup has finite index. The quotient and finite-index property-(T) facts are also stated in the retrieved KK source, Remarks 2.10--2.11. They are used as established results, not independently re-proved in this audit.
