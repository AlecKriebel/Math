# Failed approaches and discovered obstructions

## 1. Symmetry plus presumed uniqueness

The Bell functional has outcome/setting symmetries, and a unique maximizing behavior would inherit them. This cannot be used without first proving uniqueness. The weighted-shift family proves uniqueness is false for every `d>=4` and produces nonuniform designated joint distributions at the exact maximum, even though both local marginals remain uniform.

## 2. Inferring mutual unbiasedness from the scalar equality set

The sharp bound forces the relative unitary `U=A0^dagger A1` to have the correct `d` phases, but this does not determine its eigenvectors relative to `A0`. At `d=4`, the displayed non-Weyl pair has the correct relative spectrum and all polar observables have order four, yet `A0` and `A1` are not mutually unbiased.

## 3. Assuming the canonical maximally entangled realization is representative

The canonical clock/shift realization has uniform target outputs. Maximally entangled states alone do not force this: the exact counterexample also uses `Phi_4`, but its noncanonical Alice basis produces probabilities `1/32` and `3/32`.

## 4. Searching only the Bell objective

Optimizing the Bell value tends to return the familiar symmetric solution and gives little information about other components of the maximizing variety. The successful falsifier instead imposed the exact kernel constraints (`U^4=-I` and fourth-order polar factors) and optimized a non-MUB defect inside that variety.

## 5. Direct-sum and Eve-flag attacks

These were natural possible sources of private-randomness failure. They were unnecessary: a single irreducible-looking `4 x 4` block with trivial Eve already violates observed uniformity. Direct sums remain relevant to a future complete classification.

## 6. Extending the `d=3` pattern naively

Numerical equality-variety searches at `d=3` returned Weyl-oriented blocks and direct sums related by conjugation/orientation, all compatible with target mutual unbiasedness. This does not generalize beyond three outcomes: arbitrary cycle permutations of the equality phases are maximizers, and a single adjacent-order defect creates nonzero Fourier autocorrelation for every `d>=4`.

## 7. Deriving full self-testing from equal multiplicity

The reflection-product argument proves a strong dimension/multiplicity restriction, but equal multiplicities do not determine the relative eigenbases or the polar observables up to a unique representation. The `d=4` witness is the obstruction.

## 8. Robust maximal-randomness theorem

An estimate based only on Bell deficit and converging to `1/d^2` at zero
error is impossible at `d=4`, because an exact maximizer already has guessing
probability `3/32`. Additional full-behavior constraints may yield stronger
bounds. Robustness may also be studied relative to a different baseline: the
worst guessing probability over the entire exact maximizing face.

## 9. Treating the `d=4` obstruction as isolated

The first exact witness looked dimension-specific because its entries lay in `Q(zeta_16)`. Rewriting the equality phases in their own eigenbasis exposed a simple weighted-cycle construction. Every `d`-cycle is a maximizer, and swapping the final two labels makes the second cyclic autocorrelation nonzero for all `d>=4`. Thus the obstruction is an infinite family, not an exceptional four-outcome accident.

## 10. Cancelling a singular polar factor on the state support

An early equality proof said that `|C_y^dagger|^(1/2)` was “invertible on
K=supp(rho_A).” That phrasing is insufficient because the preceding polar
operator can move the state outside `K`. The repaired proof identifies the
final support projection `F_y`, proves both terms of
`(I-V_y tensor B_y)|Psi>` lie in `ran(F_y)`, and then uses the orthogonality
of the kernel and support range. Only after this support-range argument is the
polar stabilizer obtained.

## 11. Using spectral projections before proving support invariance

The scalar gap places `K` inside the equality spectral subspace of
`U=A0^dagger A1`, but it does not by itself show that `K` is invariant under
`U`. The repaired structural appendix first derives every polar stabilizer,
then proves `A0` and `V_y` preserve `K`, and only then obtains
`U=omega^(-y)S_y^2` on `K`. Spectral projections of `U|_K` are introduced
after that step.

## 12. Conflating Bell-value and fixed-behavior certification

Appendix B.1 of the originating paper fixes the full canonical behavior,
whereas Conjecture 2 and its uniqueness argument are naturally phrased as a
consequence of maximal Bell value. The counterexample refutes the latter but
does not challenge the former numerical calculation. Keeping these two
conditioning models separate resolves the apparent `d=4` conflict.
