# Proof roadmap for expert review

## 1. From a behavior-set counterexample to one global maximizer

For fixed finite outputs, the fixed-qubit strategy sets and their convex hulls
are compact. If a POVM behavior lies outside the PVM convex hull, its nearest
PVM point gives a strict separating Bell functional. Maximizing this
functional over the full POVM set supplies a global maximizer above the PVM
support value.

This globality matters later: every local measurement at the selected
strategy is genuinely optimal with the state and other measurements fixed, so
finite POVM duality applies.

## 2. Eliminate every architecture with one binary party

Every binary qubit POVM is an exact convex mixture of PVMs. Fix two binary
PVMs on Bob and compress each Alice-steered positive operator to

\[
\Phi_B(\sigma)=
(\operatorname{Tr}\sigma,\operatorname{Tr}\sigma B_0,
\operatorname{Tr}\sigma B_1).
\]

The image cone is a three-dimensional Lorentz cone or a simplicial
degeneration. The two Alice inputs give a positive relation between two
finite lists of extreme rays. Support-minimal relations use at most four rays;
cone extremality leaves only two-versus-two circuits. Every circuit lifts to
two rank-one decompositions of one positive qubit operator. A canonical
purification realizes those two decompositions by two PVMs.

The circuit weights form one shared-randomness variable for the complete
behavior. This is stronger than separately decomposing each measurement.

## 3. Reduce all remaining counterexamples to `(2,3)-by-(2,3)`

Choose an extreme point in the maximizing face. State and measurement
decompositions allow a pure entangled state and extremal local POVMs.

If the two local measurement spans share a nonscalar Hermitian operator,
an exact two-branch filtering perturbation decomposes the full behavior.
Extremality and full-rank marginals force the intersection to be exactly
`\(\mathbb R I\)`.

Because `Herm(2)` has real dimension four, one span has dimension at most two
and can be replaced by a binary PVM. The other has dimension at most three.
For an extremal qubit POVM,

\[
\sum_a\operatorname{rank}(M_a)^2\le4.
\]

Linear independence then leaves exactly three rank-one effects. Apply the
argument on both parties.

## 4. Lorentz incidence coordinates

Represent a Hermitian qubit operator by a Lorentz vector:

\[
X=x_0I+x_1\sigma_x+x_2\sigma_y+x_3\sigma_z,\qquad
\det X=x^T\eta x.
\]

Positive rank-one effects are future-null rays. The two binary and three
ternary effects satisfy one circuit

\[
r_1+r_2=r_3+r_4+r_5=u.
\]

The first four effects form a basis. Their Lorentz Gram matrix is a
four-parameter metric `g`. The first four joint probabilities form a matrix
`P`, and every declared probability is `\(r_i^T P r_j\)`.

Pure-state steering is conformally Lorentz and gives

\[
F_j(P,g)=(Pr_j)^Tg^{-1}(Pr_j)=0,\qquad j=1,\ldots,5.
\]

Together with normalization, these equations define a smooth 14-dimensional
incidence manifold.

## 5. Why incidence tangents are physical

Given a nearby incidence point, Lorentz Gram--Schmidt reconstructs Alice's
future-null effects. The vectors

\[
s_j=\tfrac12\mathsf E^{-T}Pr_j
\]

are future-null steered operators. Their circuit sums define a positive
full-rank reduced state. Inverting its square root reconstructs Bob's POVMs
and a normalized pure state. The Born probabilities are exactly
`\(r_i^TPr_j\)` and are automatically nonnegative.

The regular level-set theorem then integrates every tangent. Signature, time
orientation, positive marginals, and full rank are open, so the curve is
physical on both sides even if an individual joint event has zero
probability.

## 6. Positive multipliers

At stationarity,

\[
c-\alpha uu^T=-2g^{-1}P\Lambda,\qquad
\Lambda=\sum_j\lambda_jr_jr_j^T.
\]

Apply finite POVM duality separately to the binary and ternary input. Each
dual slack is a nonnegative multiple of the adjugate of the corresponding
rank-one effect. Pullback through full-rank steering identifies

\[
4|\det C|^2\lambda_j=s_j\ge0.
\]

If `\(s_j=0\)`, replacing that complete input by a deterministic PVM
preserves the Bell score and leaves only one nontrivial input on that party,
which is local/PVM-simulable. A strict separator therefore has
`\(\lambda_j>0\)` for all five effects, so `\(\Lambda>0\)`.

## 7. Second variation and the rank trichotomy

After the tangent substitution `\(\delta P=PW+Hg^{-1}P\)`, exact square
completion gives

\[
q(W)=\operatorname{Tr}(S W\Lambda W^T),\qquad
S=P^Tg^{-1}P.
\]

Because `S` has signature `(1,3)` and `\(\Lambda>0\)`, `q` has inertia
`(4,12)`.

Let `\(\mathcal D\)` be the four-parameter metric differential.

- **Rank at least two.** The compatible `W`-space has dimension at least 13,
  while a nonpositive subspace of `q` has dimension at most 12. Hence there is
  a positive physical second-order direction.
- **Rank one.** An exact quadratic map is projectively injective away from
  five base rays, including four exceptional divisors. At most one
  differential row is nonzero, so the multiplier kernel contains no strictly
  positive vector.
- **Rank zero.** All transformed rays permute the base rays. The unique
  circuit forces equal scale and a special Gram probability table. A bounded
  transportation flow decomposes all four setting blocks simultaneously into
  deterministic local strategies.

Every rank contradicts a strict non-PVM global maximizer. Nearest-point
separation therefore proves equality of the convex behavior sets.

## 8. Add the exact `3 x 2` witness

The separate exact witness uses a weighted CHSH locking term and a ternary
state-discrimination advantage. The projective upper bound controls Schmidt
imbalance and Bob-axis nonorthogonality by the CHSH deficit, exhausts all
ternary-PVM supports, and completes a square. This supplies the achieved
`3 x 2` side of the minimum-setting classification.

