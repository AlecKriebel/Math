# Closed independent geometry/algebra falsification report — PR1160 / 1900013

Review completed: 2026-10-22 UTC. Overall sweep completion estimate: 79%; this assigned review: 100%.

Immutable head: `6124be0d9baffbfb83d80d7273a2389146b3cf1d`.
Immutable base: `293f0c3d87e07532755d3202e535490ea07e2056`.
All ten files under `unsolved_math_prioritization/attempts/1900013` were read. They are additions relative to the base; exact body copies and blob/SHA-256 pins are in `inputs/` and `PINS.json`. Full PROOF, full AUDIT, corrections, acceptance, README, result and both metadata reports were included. No root verdict was supplied before the independent reasoning. This is an internal mathematical review, not external peer review or a formal certificate.

## Disposition

**No mathematical defect found in the stated theorems.** The strongest verified statement is an exact arithmetic classification of the historical complete eight-sail Klein objects for each fixed totally real cubic field, together with positive SL(3,Z) realization, countable infinitude, finite order strata and finite bounded recovered-order-discriminant strata. Finite exact tests supplement the universal proofs; they do not replace them.

**Material scope caution:** the exact historical question does not expressly require a face/angle/torus description. Its complete arithmetic equivalence and finite conductor quotient must not be rejected as incomplete merely by adding such a requirement. Conversely, this review does not certify all of the generalized sail models in the 2017 survey, nor novelty, priority or present-day global openness. The manuscript's PARTIAL label is conservative scope/editorial language; it does not identify a mathematical gap in its historical arithmetic classification.

## 1. Exact source interface and classification scope

The primary [2004 paper](https://arxiv.org/pdf/math/0411054), Definition 1.1 on PDF page 3, defines a sail as the boundary of the convex hull of nonzero integer points in a closed orthant. The continued fraction is the union of all sails, and equivalence is an integer-lattice-preserving linear transformation. Definition 1.2 on page 4 uses irreducible integral unimodular operators with distinct real eigenvalues. The discussion on pages 15–16 associates the cubic field and gives inequivalent same-field examples. Problem 3 asks for classification at a fixed cubic extension, and separately mentions uncertainty about finiteness. It does not stipulate classification by face data. The present totally real scope follows from the specified real-root operator class.

The primary [2017 survey](https://arxiv.org/pdf/1712.01450), pages 3–6, treats several geometric constructions and defines algebraic arrangements through irreducible totally real GL(n,Z) operators. Pages 7–9 stress informative geometric/combinatorial invariants and include separately stated fundamental-domain and torus problems. Problem 13 on page 8 gives the fixed-cubic-extension classification request without an express face-data or algorithmic requirement. This context makes geometric descriptions desirable, but does not logically make them an extra condition in the literal historical question. Applying a historical eight-sail theorem to every generalized construction would require additional argument, not provided here.

I read the exact primary PDF text at the decisive definitions and problem statements. The web screenshot interface did not deliver image pixels to this reviewer; no visual-inspection or fresh-source-hash claim is made. The current Conrad PDF retrieval timed out twice. That is not a mathematical gap: the order-unit existence needed below follows from the usual maximal-order Dirichlet theorem through a finite residue group. The inherited source-verification claims in the candidate were read, not silently reclassified as fresh retrievals by this reviewer.

## 2. Attempts to falsify missing-ray recovery

Let I be an arbitrary full lattice in K, not assumed to be an invertible ideal. Since it has a finite rational basis, some positive integer d satisfies dI⊂O_K. Every nonzero x∈I therefore satisfies

    |σ1(x)σ2(x)σ3(x)| ≥ d^(-3) = δ > 0.

No nonzero element of K has a zero embedding. Thus the lattice has no nonzero point on a bounding plane, and closed-orthant and open-orthant lattice generators coincide.

In one orthant, change signs to make the coordinates positive. For a finite convex combination y=Σλ_j x_j, concavity of log gives

    log(y1 y2 y3) ≥ Σλ_j log(x_j1 x_j2 x_j3) ≥ log δ.

Every point of the finite convex hull has product at least δ. Its closure lies in the closed orthant, and product continuity preserves the inequality at every finite limit. Hence every point of that closed hull still has all three coordinates strictly positive. Sequences escaping to infinity do not create finite points on a coordinate plane. In particular, a sail from another cone cannot introduce a point on a missing-plane ray.

For v in an open orthant, write tv in a lattice basis and round its coordinates down. The eight corners of the enclosing basis parallelepiped differ from tv by vectors with a bound independent of t. In embedding coordinate i, |tσ_i(v)| grows linearly; all corners are therefore in the same open orthant for sufficiently large t. The parallelepiped contains tv and is full-dimensional. Thus both membership of the ray tail and full-dimensionality of the convex hull follow without a polyhedrality or periodicity assumption.

The parameter set {t≥0:tv∈P_C(I)} is nonempty and closed. Its members satisfy

    t^3 |σ1(v)σ2(v)σ3(v)| ≥ δ,

so its positive infimum t0 is attained and bounded away from zero. Smaller ray parameters are outside P_C and approach t0v. Hence t0v lies on its boundary. This proves that every interior ray meets a sail and every plane ray misses the entire union. Recovering the planes as maximal real planes in their union is justified because a real plane is not the union of finitely many proper linear subspaces.

The candidate's replacement of a convex hull by its closure is valid: for a full-dimensional convex set C, int(cl C)=int C and cl C is unchanged, so ∂C=∂cl C. The supplied parallelepiped verifies the essential full-dimensional hypothesis. Neither the origin, a boundary ray, nor a noninvertible lattice furnishes a counterexample. The origin is already part of the source's ambient linear setting.

**Status:** recovery holds for the actual geometric union. No operator has been smuggled in as additional geometric data.

## 3. Rational stabilizer, order and semilinear equivalence

A real matrix preserving each coordinate hyperplane individually has all off-diagonal entries zero. For a Q-linear map T on K of this form, a=T(1) belongs to K and its embeddings are precisely those three diagonal entries. Consequently σ_i(Tx)=σ_i(ax) for every x, so T=m_a. Conversely m_a preserves the planes. This uses preservation individually, not just an arbitrary permutation; zero and singular maps are allowed in the algebra.

Intersecting with integral endomorphisms of I gives R=(I:I). Clearing denominators in the finitely many multiplication matrices of an O_K basis places mO_K inside R for some m>0. For a∈R, the integral multiplication matrix on I has a monic integral characteristic polynomial; Cayley–Hamilton and evaluation at 1 show that a is integral. Thus R is a full unital subring of O_K: an order, even when I is not invertible over it.

An actual lattice-linear sail equivalence T permutes the recovered planes. It therefore conjugates the rational multiplication algebra to itself and induces a Q-field automorphism τ. Evaluating Tm_xT⁻¹=m_τ(x) at T(1)=a gives

    T(x)=aτ(x),        J=aτ(I).

Conversely this map permutes hyperplanes and cones, takes lattice generators to lattice generators, and takes the hulls and boundaries to their counterparts. This proves both directions of the equivalence criterion. No arbitrary permutation of embeddings can be substituted for a genuine field automorphism. A non-Galois totally real cubic, for example t³−4t+1 of discriminant 229, has trivial field automorphism group; all its rational plane-arrangement normalizers are scalar multiplications. In the cyclic test field, the verifier instead constructs the actual order-three automorphism θ↦θ²−2 and checks its conjugation identity exactly.

The integral ring is transported by conjugation. Its trace Gram determinant is therefore invariant and equals disc(R), because Tr_Q(m_am_b)=Tr_K/Q(ab). The trace pairing is positive definite in a totally real field. This invariant belongs to the actual sail union with its integer lattice, not to an arbitrarily selected operator polynomial. The central symmetry of the complete union also validates the stated GL/SL orbit equivalence in dimension three: compose a negative-determinant equivalence with −Id. No assertion for a single sail or even dimension follows.

**Status:** exact arithmetic equivalence and recovered multiplier-order discriminant are verified.

## 4. Full-lattice realization and infinitude

For arbitrary full I, choose R=(I:I). Independently of the order-specific citation, let mO_K⊂R. An infinite-order maximal-order unit u has a finite-order image in (O_K/mO_K)×. A positive power v of u is 1 modulo mO_K, so v and v⁻¹ lie in R. Squaring v gives an infinite-order totally positive unit ε∈R with norm one. Its multiplication matrix on I is integral with integral inverse and determinant one.

A rational algebraic-integer unit is ±1. Thus ε is nonrational. Prime degree three implies Q(ε)=K; separability then gives distinct eigenvalues, and its multiplication characteristic polynomial is an irreducible cubic. In embedding coordinates the eigen-hyperplanes are precisely the three required ones. This is an actual positive SL(3,Z) realization for every I.

Conversely, for an irreducible cubic operator A and 0≠v∈Q³, the field-module map x↦x(A)v is injective, since nonzero field elements act invertibly. Dimension makes it an isomorphism. Pulling back Z³ produces the required full lattice. Hence no historical operators are omitted.

For R_f=Z+fO_K, the multiplier ring equals R_f by applying a multiplier to 1. Since 1 is primitive in O_K, it extends to an integral basis 1,ω2,ω3. The basis 1,fω2,fω3 has index f² and discriminant f⁴ disc(K). Different positive f are separated by the recovered geometric invariant. This distinguishes actual sail unions, not just presentations of a common union. Countability follows from countability of K and finite generation of each lattice.

**Status:** every-field countable infinitude and the positive realization theorem are verified; f=1 and arbitrary nonmaximal orders cause no exception.

## 5. Conductor sandwich, including noninvertible lattices

Fix R⊂O=O_K, conductor c, and representatives J_i of the finite O ideal class group. For I with multiplier R, J=OI is a nonzero fractional O ideal. Normalize by a scalar so that J=J_i. Then

    cJ_i=cOI⊂RI⊂I⊂J_i.

The conductor contains mO for some m>0, since R has finite index. Therefore J_i/cJ_i is finite. Every intermediate additive subgroup gives a full lattice; R-stability, O-saturation J_i, and exact multiplier R select exactly those in the stratum. No invertibility assumption on I is used.

The selection is genuinely finite. If aI⊂I and OI=J_i, then aJ_i⊂J_i. Invertibility of the maximal-order ideal J_i forces a∈O. Also c⊂(I:I). Thus the exact multiplier test is the stabilizer of I/cJ_i under the finite ring O/c. Saturation and R-stability are finite module tests. If I′=aI and both saturate to J_i, then aJ_i=J_i, hence a∈O×. The unit action has finite image on J_i/cJ_i. Automorphisms transport R, c and ideal classes; a compensating scalar renormalizes τ(J_i) to the chosen representative. Different choices differ by an O-unit and produce the same orbit after the unit quotient.

This is not a hidden appeal to invertibility at the nonmaximal order. The independent example I=<1,θ,2θ²> in Z[θ], with θ³−3θ+1=0, has multiplier R=<1,2θ,2θ²>, saturation Z[θ], and conductor c=2Z[θ] relative to that overorder. Direct multiplication requires the θ and θ² coefficients of a multiplier to be even. The quotient I/cI=I/2Z[θ] has four elements, whereas R/c has two. An invertible R-ideal would reduce to a rank-one module over R/c=F₂ and have two elements, so I is noninvertible. It remains fully included in the sandwich. This auxiliary calculation needs no assertion that Z[θ] is the maximal order.

The finite quotient construction plus standard maximal-order class/unit data leaves no equivalent-or-stronger unsupported classification conjecture. It provides an exhaustive arithmetic parameterization. A general implementation, complexity claim, or direct reconstruction of face geometry is not supplied or needed for the finiteness theorem. Finally, disc(R)=[O:R]²disc(K) bounds the order index, and finitely many subgroups of bounded index give finitely many orders. The fixed-order argument then gives bounded-discriminant finiteness and the stated lower bound on N_K(X).

**Status:** finite strata and arithmetic classification verified; no mathematical route is marked blocked.

## 6. Independent computations and limits

`verify.py` is a new standard-library-only implementation; it imports no candidate code. It checks all ten immutable pins and the candidate manifest, rebuilds multiplication from θ³=3θ−1, and verifies the displayed A/B pair, common polynomial, determinant one, exact positive-root intervals, irreducibility, Gram/discriminant values 81 and 6561, linear multiplier formula, and cubic norm identity on a degree-three unisolvent grid. It verifies an actual order-three automorphism, twelve conductor-unit residue realizations, and every finite subspace modulo 2 and 3. Counts are respectively 16/28 total subspaces and 14/18 full-span subspaces with exact scalar multiplier. The explicit noninvertible witness is included. Four false arithmetic claims are rejected. Normal, −O and −OO execution must give the same JSON output.

The universal geometric argument is a written proof, not a finite approximation of a sail. This review makes no current-literature or novelty claim. It also makes no claim that literal face/torus classification or all other survey models has been proved. No external human communication, source edits, Git/index/ref mutation, PR mutation, release, Zenodo or spreadsheet action was performed.
