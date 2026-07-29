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
