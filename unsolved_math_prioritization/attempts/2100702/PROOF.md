# A bounded spectral criterion for almost-everywhere independence

## Statement and scope

Let `F = (f_1,...,f_n): M^(2n) -> R^n` be smooth. A multiplicity-weighted semiclassical spectral measure that converges to the pushforward of smooth positive volume determines whether `rank(dF) = n` almost everywhere. The test is absolute continuity of the exact limiting measure.

Below is a complete measure-theoretic proof and a derivation of the required joint limit for standard compact Kähler Berezin-Toeplitz quantization. This is a consequence of classical tools, with no novelty claim. It is a bounded answer relevant to Vũ Ngọc's Problem 7.2 in [1], not a claim to settle arbitrary semiclassical operators or to provide a finite-data decision algorithm.

## 1. The pushforward criterion

**Theorem 1.** Suppose that:

- `M` is a Hausdorff, second-countable smooth manifold without boundary of dimension `2n`, where `n >= 1`;
- `nu` is the measure defined by a smooth, everywhere positive density on `M`;
- `F: M -> R^n` is smooth;
- `mu = F_*nu` is locally finite.

Set `C = {x in M: rank(dF_x) < n}` and `R = M \ C`. Then

`mu is absolutely continuous with respect to n-dimensional Lebesgue measure <=> nu(C) = 0`.

In fact, the Lebesgue decomposition of `mu` is

`mu_ac = F_*(nu restricted to R)` and `mu_s = F_*(nu restricted to C)`.

If `nu(M) < infinity`, the total mass of the singular part is exactly `nu(C)`.

**Proof.** The rank condition shows that `C` is closed. The second-countability assumption gives a countable compact exhaustion `K_l` of `M`. Thus

`F(C) = union_l F(C intersect K_l)`

is a countable union of compact sets, hence Borel. Sard's theorem gives Lebesgue measure zero to this set. In particular, the positive measure `F_*(nu restricted to C)` is singular and has total mass `nu(C)`.

We next show that `F_*(nu restricted to R)` is absolutely continuous. Near each point of `R`, the submersion theorem supplies smooth local coordinates `(y,z) in R^n x R^n` in which `F(y,z) = y`. One can obtain these coordinates directly by completing the component functions of `F` to a coordinate system, so no target-coordinate measurability issue is involved. Since `R` is second-countable, countably many such charts cover it.

Let `A` be a Borel Lebesgue-null subset of `R^n`. In any of these charts, the preimage of `A` is contained in `A x R^n`, which is `2n`-dimensional Lebesgue-null by Fubini, first on bounded boxes and then by a countable union. The smooth coordinate density of `nu` is absolutely continuous with respect to `2n`-dimensional Lebesgue measure. Consequently every chart contributes zero measure to `F^(-1)(A) intersect R`. The countable chart cover gives

`nu(F^(-1)(A) intersect R) = 0`.

This proves absolute continuity of the regular-set pushforward. Since both pushforwards are positive and dominated by the locally finite measure `mu`, they are locally finite. Their sum is `mu`, and the two parts just exhibited are respectively absolutely continuous and singular. Uniqueness of Lebesgue decomposition proves the claimed formulas. Finally, a positive pushforward has zero total measure exactly when its source measure does. Therefore `mu_s = 0` if and only if `nu(C) = 0`. This proves the equivalence. QED.

**Comments on hypotheses.** Compactness of `M` is unnecessary for this proof. Local finiteness makes the target measure a Radon measure and makes the local spectral formulation below unambiguous. Smoothness supplies the differentiability required by Sard. Strict positivity ensures that `nu` has the same null sets as any other smooth positive volume, including Liouville volume on a symplectic manifold. No properness, integrability, regular-fiber hypothesis, or action-angle coordinates are used.

For a smooth manifold with boundary and an ordinary smooth volume density, the boundary has zero ambient-dimensional volume. Applying the proof on the interior proves the same almost-everywhere criterion. This observation does not cover a measure that places additional positive mass on the boundary.

## 2. The conditional spectral consequence

Suppose locally finite multiplicity-weighted joint eigenvalue measures have the form

`rho_h = a_h sum_lambda m_h(lambda) delta_lambda`,

where `a_h > 0` is the given normalization and `m_h(lambda)` is the dimension of the common eigenspace. Assume the joint Weyl law

`lim_(h -> 0) integral phi d rho_h = integral_M phi(F(x)) d nu(x)`

for every continuous compactly supported function `phi` on `R^n`. This is vague convergence to the locally finite measure `F_*nu`; on a common compact support it is ordinary weak convergence.

The exact asymptotic spectral data determines the integrals against every such `phi`, hence determines the Radon measure `mu`. Theorem 1 then determines a.e. functional independence from that measure. If only one spectral window is known, this conclusion is restricted to its preimage; global independence requires data covering all spectral values.

The Weyl law is an assumption in this general statement. It must not be obtained from a theorem whose hypotheses already include a.e. functional independence. The following compact application establishes it directly from scalar quantization calculus.

## 3. Compact Kähler application with explicit quantization assumptions

Let `(M,omega)` be a nonempty compact Kähler manifold of complex dimension `n` with positive prequantum holomorphic Hermitian line bundle `L`. Write

`d nu_L = omega^n/n!` and `V = nu_L(M) > 0`.

Fix `H_k = H^0(M,L^k)` with the standard `L^2` inner product, `N_k = dim H_k`, and the orthogonal projector `Pi_k`. For smooth scalar `g`, write `Q_k(g) = Pi_k M_g Pi_k`, restricted to `H_k`. Work with sufficiently large `k` so that `N_k > 0`.

Let `T_{1,k},...,T_{n,k}` be exactly pairwise commuting self-adjoint operators on `H_k` such that, for fixed real smooth functions `f_j`,

`T_{j,k} = Q_k(f_j) + E_{j,k}`, with `||E_{j,k}|| <= C_j/k`.

These are the leading-order estimates for the standard scalar order-zero Toeplitz families with principal symbols `f_j`. The following argument only needs these estimates, the scalar product estimate, and the scalar trace formula. It does not claim that arbitrary families called semiclassical satisfy these hypotheses, nor that every Poisson-commuting classical tuple admits exactly commuting quantizations.

By simultaneous diagonalization, choose an orthonormal common eigenbasis with joint eigenvalues `lambda_(a,k) in R^n`, `1 <= a <= N_k`, repeated according to common-eigenspace dimension. Define

`mu_k = (1/N_k) sum_(a=1)^(N_k) delta_(lambda_(a,k))`.

**Theorem 2.** Under these hypotheses,

`mu_k -> F_*(nu_L/V)` weakly as probability measures.

Consequently, `rank(dF) = n` almost everywhere if and only if this limiting measure is absolutely continuous. Moreover, the singular mass of the limit equals `nu_L(C)/V`.

**Proof.** The needed scalar estimates are

1. `||Q_k(g)|| <= ||g||_infinity`;
2. `||Q_k(g)Q_k(h) - Q_k(gh)|| = O(k^(-1))` for fixed smooth `g,h`;
3. `Tr Q_k(g) = c k^n integral_M g d nu_L + O(k^(n-1))`, where `c > 0` is a fixed normalization constant independent of `g`.

The first follows immediately from compression by an orthogonal projector. The second and third are standard compact Berezin-Toeplitz estimates. In the convention of [4], the leading constant in the third is `c = 1`; different prequantum curvature conventions change `c` but not the normalized limit. Exact source locations are supplied below.

Since `Q_k(1) = I`, the trace estimate at `g = 1` gives

`N_k = c k^n V + O(k^(n-1))`.

Dividing the scalar trace estimate by this expression yields

`(1/N_k) Tr Q_k(g) = (1/V) integral_M g d nu_L + O(k^(-1))`.

The operator norms of `T_{j,k}` are uniformly bounded by the assumed approximation and estimate 1. For any fixed ordered word of length `r` in the operators `T_{j,k}`, a telescoping replacement of each factor by `Q_k(f_j)` changes the word by `O(k^(-1))` in operator norm: there are finitely many replacements, one factor in each summand has norm `O(k^(-1))`, and every other factor is uniformly bounded. Repeated use of estimate 2 changes the resulting product into `Q_k` of the product of its symbols, again with error `O(k^(-1))`.

Therefore, for every fixed real polynomial `q` in `n` variables,

`q(T_(1,k),...,T_(n,k)) = Q_k(q composed with F) + R_(q,k)`,

where `||R_(q,k)|| = O_q(k^(-1))`. This also covers the constant term, since `Q_k(1)=I`. Exact commutation makes polynomial evaluation independent of monomial ordering.

For any operator `R` on the finite-dimensional space `H_k`,

`|Tr R| <= N_k ||R||`.

Thus its normalized trace is bounded by its operator norm, and in particular the contribution of `R_(q,k)` is `O_q(k^(-1))`. Simultaneous diagonalization and the scalar normalized trace formula now give

`integral q d mu_k = (1/N_k) Tr q(T_k) -> (1/V) integral_M q(F) d nu_L`.

Choose a fixed compact cube `B = [-R,R]^n` containing every joint spectrum for all sufficiently large `k` and also `F(M)`. Such a cube exists by uniform operator-norm bounds and compactness of `M`. Polynomials are uniformly dense in `C(B)` by Stone-Weierstrass. Given `phi in C(B)` and `epsilon > 0`, choose `q` with `||phi-q||_B < epsilon`. Both `mu_k` and `F_*(nu_L/V)` are probability measures, so

`|integral phi d mu_k - integral phi d F_*(nu_L/V)|`

`<= 2 epsilon + |integral q d mu_k - integral q d F_*(nu_L/V)|`.

Taking the upper limit in `k` and then letting `epsilon` tend to zero proves weak convergence. Theorem 1 gives the criterion and the singular-mass identity. QED.

**Why this is noncircular.** The scalar product and trace estimates hold for arbitrary fixed smooth scalar symbols. Their proofs do not require the tuple `F` to have full rank. Commutation is used to obtain an exact joint eigenbasis and the trace identity, not as a substitute for the missing rank condition.

**Why the volume must be specified.** In Theorem 2 the weak limit uses normalized Liouville volume `nu_L/V`, not an arbitrary previously chosen density. Any other everywhere-positive smooth density has the same null sets, so the independence criterion is unchanged, but the limiting measure itself need not be equal for the two densities.

## 4. What is, and is not, detected

- The input is the infinite asymptotic family with joint multiplicities. An unweighted set of distinct eigenvalue locations does not by itself give the normalized trace measure.
- The argument does not prove that multiplicities are indispensable for every possible spectral criterion in the compact Toeplitz class. It proves their role in this criterion.
- The individual measures `mu_k` are atomic; their being singular does not predict whether their weak limit is absolutely continuous. The test concerns the exact limit.
- The rank-deficient locus may be nonempty and have zero volume. That case passes the criterion, consistently with the original a.e. independence axiom.
- Detecting atoms in the limit alone is not the theorem: a singular measure need not be atomic.
- No finite-data algorithm, rate for approximating the singular mass, or stable decision procedure is established.
- No joint counting law for arbitrary noncompact operators, continuous or essential spectrum, or merely formal commutation of unbounded operators is asserted. Their spectral theory and local finiteness require separate hypotheses.
- No claim about current full-problem literature status or mathematical novelty follows from this observation.

For a simple demonstration of the multiplicity issue, take distinct scalar eigenvalues `{0,1/k,...,1}` and dimension `N_k = k(k+1)`. Repeating every value `k` times gives empirical measures converging to uniform measure on `[0,1]`. Instead, repeat each nonzero value once and repeat zero `k^2` times. The distinct spectrum and dimension are unchanged, but the empirical measures converge to `delta_0`. This is an abstract matrix example about data loss, not a counterexample within a fixed geometric Toeplitz quantization class.

## 5. Source locations

[1] A. Bolsinov, V. S. Matveev, E. Miranda, and S. Tabachnikov, *Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems*, arXiv:1804.03737v2. Section 7.1, pp. 35-36, gives the self-adjointness, commutation, and a.e. independence axioms; Problem 7.2 is on p. 36. In v1 the same item is Problem 6.2, p. 46. The statement does not explicitly specify a multiplicity convention. https://arxiv.org/pdf/1804.03737v2

[2] M. Schlichenmaier, *Berezin-Toeplitz quantization for compact Kähler manifolds: A review of results*, arXiv:1003.2523v1; published in *Advances in Mathematical Physics* (2010), Article 927280. Section 3.1 fixes the volume and quantization setup. Theorem 3.3(a,c), pp. 8-9, Proposition 3.4, p. 9, and Proposition 3.9, p. 10, are the norm, product, and trace inputs. The review uses a very ample line-bundle convention. https://arxiv.org/pdf/1003.2523v1 ; https://doi.org/10.1155/2010/927280

[3] M. Bordemann, E. Meinrenken, and M. Schlichenmaier, *Toeplitz Quantization of Kähler Manifolds and gl(N), N -> infinity Limits*, arXiv:hep-th/9309134v3; *Communications in Mathematical Physics* 165 (1994), 281-296. Section 5, p. 12, Remark (2)-(3), directly records the iterated-product estimate and normalized trace-product asymptotic in its compact setup. https://arxiv.org/pdf/hep-th/9309134v3

[4] X. Ma and G. Marinescu, *Berezin-Toeplitz quantization on Kähler manifolds*, arXiv:1009.4405v1. The setup on pp. 1-2 uses a positive prequantum line bundle, without assuming that it is itself very ample. Theorem 0.1 and equations (0.11)-(0.13), p. 3, give the diagonal-kernel leading coefficient and uniform remainder; integration gives the scalar trace law. Theorem 0.3 and equations (0.19)-(0.20), p. 4, give the product remainder in operator norm. Take the auxiliary bundle to be trivial. https://arxiv.org/pdf/1009.4405v1
