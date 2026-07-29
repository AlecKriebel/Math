# Lemma dependency ledger

This file records logical dependence rather than chronology.

## Primary spectrum theorem

The complete spectrum theorem will require both:

1. **Necessity:** an obstruction for every arbitrary matrix-class solution in
   the excluded dimensions.
2. **Sufficiency:** exact constructions in every claimed allowed dimension.

Known \(d=4\) plus spectator stabilization already proves sufficiency for
\(4\mathbb N\).

## Audited structural chain

The first implications are now proved for every arbitrary solution:

```text
(YB-P) + rank(P)=d²/2
        |
        +--> abstract two-projection block theorem [PROVED]
        |
        +--> scalar partial traces [PROVED via no-opposite-spectrum theorem]
        |
        +--> all-level Markov trace with eta=1/2 [PROVED]
                       |
                       +--> faithful Jones--Wenzl quotient representation [PROVED]
                                      |
                                      +--> exact central multiplicities [PROVED]
                                                     |
                                                     +--> only 2 | d
```

Thus a possible extra factor of two cannot arise from central ranks,
simple-block multiplicities, or Bratteli inclusion recurrences.  It must
arise from strict tensor locality/coherence, or else a \(d\equiv2\pmod4\)
construction exists.

One complete finite-symmetry constructor branch is now closed:

```text
diagonal S4 action on V2 tensor V3 tensor V2
        |
        +--> commutant M2 + M2
        +--> central balanced choices [previously empty]
        +--> all noncentral balanced choices = S2 x S2
                       |
                       +--> 20 sparse cubic coordinates
                       +--> seven exact branch relations
                       +--> three killer coordinates
                                      |
                                      +--> no real solution
```

This exhausts that exact heterogeneous symmetry class but does not force
an arbitrary \(d=6\) solution to be \(S_4\)-equivariant.

The first genuinely local divisibility chain is:

```text
scalar partial traces + spectator-sector restriction
        |
        +--> half ranks and overlap trace D/4 on D = r d²
                       |
                       +--> common-one/common-zero ranks D/8
                                      |
                                      +--> 8 | r d²
                                                     |
                                                     +--> d = 2 mod 4
                                                          forbids odd-rank
                                                          leg projections
```

This proves \(4\mid d\) for every solution controlled on either leg, but
does not yet cover the branch where both one-leg commutants have only
even-rank projections. A global spectrum theorem now requires either:

1. proving that every exceptional solution has an odd-rank leg-commutant
   projection; or
2. obtaining a different invariant that also excludes scalar/even-block
   commutants; or
3. constructing a noncontrolled \(d\equiv2\pmod4\) solution.

The current assumption audit further narrows what can supply item 1:

```text
all minimal leg projections even rank
        |
        +--> C_L = direct sum (M_m tensor I_(2a))
        +--> C_R = direct sum (M_m~ tensor I_(2b))
                       |
                       +--> all central and endpoint transportation
                            equations admit the product solution
                            k_(alpha,beta,lambda,n)
                            = a_alpha b_beta D_lambda s^(n-2)
```

Thus no remaining denominator can come from endpoint multiplicities.
Any obstruction must use the relative position of the right leg algebra of
\(P_{12}\) and the left leg algebra of \(P_{23}\) on the same middle site,
or bypass leg commutants entirely.

One even-block factor is now excluded spatially:

```text
M_m tensor I_2 contained in one leg commutant, d=2m and m odd
        |
        +--> H = I_m tensor K
        +--> automatic standardness removes the scalar Pauli term of K
        +--> K²=I forces the three Hermitian Pauli coefficients to commute
                       |
                       +--> simultaneous diagonalization gives rank-one
                            projections in the opposite leg commutant
                                      |
                                      +--> 8 | d², contradiction
```

At \(d=6\), this removes \(M_3\otimes I_2\) from both endpoints. It does
not remove the scalar algebra or the surviving block types
\[
\mathbb C I_4\oplus\mathbb C I_2,\qquad
(M_2\otimes I_2)\oplus\mathbb C I_2,\qquad
\mathbb C I_2\oplus\mathbb C I_2\oplus\mathbb C I_2.
\]
For the last type, exact enumeration shows that neither the nine two-site
cell ranks nor the nine endpoint common ranks are forced to be uniform.
Any further reduction must retain the actual cell operators and their
relative \(U(6)\) position, not only transportation margins.

Any shared endpoint atom is also excluded:

```text
one left and one right C³ rank-two atom span the same 2-space
        |
        +--> shared-cell restriction is a base-dimension-two cubic
                       |
                       +--> ranks 1,3: determinant gap
                       +--> rank 2: known d=2 emptiness
                       +--> ranks 0,4: scalar
                                      |
                                      +--> mixed colors propagate the scalar
                                                   |
                                                   +--> partial-trace contradiction
```

Thus only genuinely transverse relative positions, with no shared
two-dimensional atom, remain in the three-atom/three-atom branch.

The shared-atom argument in fact upgrades to the entire pair of leg
commutants at \(d=6\):

```text
non-scalar C_L(P) intersection C_R(P)
        |
        +--> C17 gives only even-rank projections
        +--> rank 4 replaced by its rank-2 complement
                       |
                       +--> common 2-space W
                              |
                              +--> H restricted to W tensor W is a d=2 cubic
                                      |
                                      +--> determinant gap + d=2 emptiness
                                           force a scalar cell
                                                  |
                                                  +--> cubic propagates scalar
                                                       to W tensor V
                                                              |
                                                              +--> partial-trace
                                                                   contradiction
```

Therefore
\[
\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb C I_6.
\]
This excludes aligned and flip-symmetric even-block branches, but exact
relative-position models show it does not exclude two transverse
non-scalar leg algebras or scalar leg commutants.

The same mechanism gives a descent theorem in every unresolved dimension:

```text
common projection z of ranks r and s=d-r
        |
        +--> diagonal restrictions are non-scalar local cubic involutions
        +--> positive Hecke traces give eta in {1/3,1/2,2/3}
        +--> ambient standardness gives
             a-r²/2 = e-s²/2
                       |
                       +--> either both eta=1/2
                       +--> or r=s and both eta=1/3 or both eta=2/3
                                      |
                         d=2 mod 4 + C17 forces r even
                                      |
                                      +--> r=s=d/2 odd is impossible
                                                   |
                                                   +--> two smaller balanced
                                                        exceptional cells
```

Thus a minimal \(d\equiv2\pmod4\) counterexample must have scalar common
leg algebra.  This is a structural induction principle, not yet a global
nonexistence theorem, because it does not exclude a common-leg-irreducible
minimal solution.

Scalar contraction closures do not strengthen this branch:

```text
three-site cubic residual
        |
        +--> close against C[S_3]
        |       |
        |       +--> four tautologies
        |       +--> two shadows of outer channel contractions
        |
        +--> trace the middle site
        |       |
        |       +--> positive M with fixed scalar marginals and bounds
        |       +--> exact scalar d=6 limitation model
        |
        +--> partially transpose all six permutations
                |
                +--> 48 scalar Brauer tests
                +--> exact standard d=6 fake passes all 48
                     while failing the cubic
```

Therefore any remaining parity mechanism must retain operator-valued
spatial overlap data; scalar permutation, reshuffling, or cup-cap closures
are insufficient.

Two broad construction branches are now also closed:

```text
diagonal U(m) color equivariance, m odd
        |
        +--> A tensor P_sym + B tensor P_asym
        +--> restriction to Sym^3(color) gives a d=2 cubic
                       |
                       +--> trace-zero case: known d=2 emptiness
                       +--> trace +/-2 case: determinant 1/16 < 1/9

crossed factorization d=3*2 or 2*3
        |
        +--> rank-three projection in one leg commutant
                       |
                       +--> controlled-leg theorem excludes d=6
```

The first new shifted-intersection relation is also now exact:

```text
three-site common projection e + Markov trace
        |
        +--> zero variance of e P_shift e
                       |
                       +--> e_123 e_234 e_123 = e_123 / 4
                                      |
                                      +--> d^4/8 generic blocks
                                      +--> still only 2 | d
```

The accompanying \(d=6\) limitation countermodel proves that this
marginal/angle package alone is insufficient. Any use of it in a spectrum
proof must retain the fact that \(e\) is the entire common intersection of
the original projections and must couple back to the generic
squared-angle-\(1/3\) sector.

## Candidate construction chain

```text
structured numerical or finite search at d=6
        |
        +--> exact algebraic recognition
        |
        +--> independent exact verifier
        |
        +--> extension mechanism
        |
        +--> spectrum sufficiency theorem
```

No numerical candidate enters a theorem until exact recognition and exact
verification are complete.

The broadest retained Weyl-frame search currently separates into two
near-miss mechanisms:

```text
all 361 real coefficients in retained Hermitian Weyl frame
        |
        +--> desired cubic exactly
        |       |
        |       +--> Weyl stratum
        |               |
        |               +--> wrong quadratic / signature 9+27
        |
        +--> balanced involution exactly
                |
                +--> adjacent anticommutation
                        |
                        +--> cubic coefficient 1, not 1/3
```

The second implication is exact; the observed separation of all forty
search endpoints into these strata is numerical evidence only.

The fusion-anomaly route now has a precise conditional endpoint:

```text
neutral SU(3)_3 fusion component
        |
        +--> R(A4)
        +--> nontrivial degree-one projective class
                |
                +--> C^alpha[A4] = M2 + M2 + M2
                        |
                        +--> action on C^s would force 2 | s
                        |
                        +--> natural action is only on C^2 tensor C^s
                                |
                                +--> forces only 2 | d
```

A successful use of this mechanism requires a new spatial
projective-descent theorem producing an invariant \(s\)-dimensional
multiplicity factor. The diagonal tower, determinant channels, grading,
FS data, and bare reversal do not construct it.

The square-restriction branch now closes exactly at four strands:

```text
ambient balanced exceptional solution
        |
        +--> H4 q-symmetrizer = H4 q-antisymmetrizer = 0
                |
                +--> inherited by every W^tensor n restriction
                        |
                        +--> scalar / eta=1/3 / eta=2/3 excluded
                                |
                                +--> restriction has eta=1/2
                                        |
                                        +--> dim W is even
```

Thus every restrictable \(d=2\bmod4\) solution descends to a smaller
balanced solution in the same congruence class. A minimal unresolved
solution, if one exists, must have no proper local decomposition whose
two diagonal tensor squares are invariant.

The determinant-boundary route has an all-level stopping theorem:

```text
three-site invertible endpoint a
        |
        +--> simple-current path-count bijection
                |
                +--> dim(a A_(m+3) a) = dim(A_m)
                        |
                        +--> disjoint A_m copy fills the corner
                                |
                                +--> a A_(m+3) a = a tensor A_m
                                        |
                                        +--> no action on ran(a)
```

Accordingly, any future parity mechanism must use data outside closed
Hecke boundary words—for example a genuinely spatial identification not
contained in the diagonal tower.

The identity-amplification cut-down branch is now closed uniformly:

```text
published H4 boxtimes I_m and corank-two local Q
        |
        +--> leakage sum over three Schmidt coefficients
                |
                +--> if compressed B-span <= 1:
                |       kernel contains a real plane
                |       and m rank(B_tilde) <= 4
                |               |
                |               +--> m=2: six-line rank<=2 cone has no plane
                |               +--> m>=3: no nonzero rank<=1 pencil element
                |
                +--> compressed B-span >= 2
                        |
                        +--> Q commutes with two Pauli directions
                                |
                                +--> Q commutes with full active M4
                                        |
                                        +--> rank Q divisible by 4
                                                |
                                                +--> rank 4m-2 impossible
```

This prevents \(4m\to4m-2\) by square restriction of the known identity
amplification.  It does not constrain a genuinely new
\((4m-2)\)-dimensional solution.

One-sided square invariance has been reduced to one scalar target:

```text
balanced W tensor W restriction, U=W^perp
        |
        +--> K = compression of P to U tensor U
        +--> Tr K = u^2/2
        +--> K-K^2 = C* C
                |
                +--> delta = u^2/2-Tr(K^2)
                          = ||C||_HS^2
                          = (1/2)||[P,P_UU]||_HS^2
                                |
                                +--> delta=0 iff U tensor U invariant
```

An exact \(d=6\) two-site model has \(\delta=1/2\) while preserving all
two-site data and the full \(d=4\) restricted solution.  Hence the only
remaining route to \(\delta=0\) is a genuinely mixed-sector consequence of
the ambient three-site cubic.

The first full-cubic color compression now has a sharp stopping point:

```text
genuine one-sided W tensor W restriction
        |
        +--> WWU and UWW boundary compressions of the cubic
        |       |
        |       +--> exact norms r^2 u / 4
        |       +--> weighted leakage L* A_perp L
        |               |
        |               +--> does not determine L*L or delta
        |
        +--> abstract balanced H3 model with all eight color sectors
                |
                +--> exact tensor-sector dimensions and scalar traces
                +--> spectator-color and WW-pair commutators vanish
                +--> complementary UU-pair leakage remains 16/9
                        |
                        +--> full matrix-algebra spectator locality absent
```

Therefore an implication \(\delta=0\), if true, must use the common
two-site factorization
\[
P_{12}=P\otimes I_d,\qquad P_{23}=I_d\otimes P
\]
beyond its restriction to the commutative color algebra.  The abstract
model is not a Yang--Baxter witness and does not disprove the genuine-local
implication.

The balanced standard quantum-supergroup candidate is also closed:

```text
standard Manin GL(s|s) Hecke symmetry, q=t^2
        |
        +--> ordinary braid relation and roots {q,-1}
        +--> multiplicities d^2/2 and d^2/2
        |
        +--> suppose T is unitary for G tensor G
                |
                +--> even |ii> and odd |aa> have different eigenvalues
                |       |
                |       +--> G_ia^2=0, so even and odd spaces are G-orthogonal
                |
                +--> mixed q-vector t|ia>+|ai>
                +--> mixed -1-vector |ia>-t|ai>
                        |
                        +--> inner product = (conj(t)-t)G_ii G_aa != 0
                                |
                                +--> contradiction
```

This obstruction is uniform in \(s>0\), but it excludes only the standard
one-parameter super-Hecke family and its local conjugates.  It is not an
obstruction to arbitrary exceptional matrices or to unaudited
multiparameter twists.

The obvious positive-metric replacement also fails exactly:

```text
balanced GL(3|3) Manin (-1)-eigenspace
        |
        +--> orthogonal rank-18 projection P_orth
                |
                +--> H_orth = I - 2P_orth is Hermitian, H_orth^2 = I
                        |
                        +--> cubic residual squared norm = 140/3
                        +--> each marginal deviation squared norm = 6
                                |
                                +--> not an exceptional solution
```

Nearby unrestricted Grassmann searches return numerically to this point,
but that optimizer behavior supplies no nonexistence theorem.

The binary-tetrahedral heterogeneous branch has a complete finite
reduction:

```text
diagonal 2T invariance on A tensor B tensor A
        |
        +--> exact module decomposition 1+1'+1''+3+3+3
                |
                +--> balanced signatures only (3,1) and complement (0,2)
                        |
                        +--> K -> -K reduces all cases to CP^2
                                |
                                +--> F[2,2]=F[5,5]=0
                                |       |
                                |       +--> a^2=1/3 and Re(conj(z1)z2)=0
                                |
                                +--> |F[57,20]|^2=16/729
                                        |
                                        +--> contradiction
```

Thus this full symmetry branch supplies no \(d=6\) witness. The dependency
chain uses diagonal \(2T\)-equivariance essentially and cannot be promoted
to an unrestricted obstruction.

The finite-image fixed-point route separates as follows:

```text
exceptional R
        |
        +--> factors through H_n(3,6)
        |       |
        |       +--> Rowell: every fixed-strand braid image is finite
        |
        +--> normalized partial trace = (q-1)I/2
                |
                +--> Conti--Lechner: nonergodic for d>2
                        |
                        +-X finite image + this trace alone do not force
                            an algebraic fixed point or leg commutant
```

The exact countermodel
\[
(q-1)(I_m\boxplus I_m)
\]
has every property below the crossed arrow but scalar leg commutants.  It
has an opposite eigenvalue pair.  Therefore the only surviving version of
this route must use the exceptional no-opposite-spectrum consequence
\[
\varphi(\mathcal L_R)'\cap\mathcal L_R=\mathbb C
\]
to control the different, vertical algebra
\(\mathcal L_R'\cap\mathcal N\). No such horizontal-to-vertical theorem is
currently available.
