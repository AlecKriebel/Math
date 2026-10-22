# Independent adversarial audit: finite-width symmetric orbit spectrality

Audit date: 2026-10-11 UTC.
Target: problem 30005476 / OWR-12697711-010.

Review and distribution status: AI-assisted and unrefereed. Acceptance means an
internal AI mathematical audit, not external human peer review or formal
proof-assistant certification. This is a prose edition, not a computational
reproduction package. No claim of first resolution or worldwide novelty is made.

## Verdict

**ACCEPT the mathematical argument in the exact pinned candidate.** No missing
mathematical hypothesis, invalid inference, or counterexample to the stated
claim was found. The proof establishes spectrality in the requested category:
ordinary prime spectra, finite-support row permutations, the topological orbit
quotient, and then its Kolmogorov quotient. It actually permits any algebraically
closed coefficient field, including a countable one.

Reviewed original candidate: 10,565 bytes,
SHA-256 `aa94a980f85ac97357ac0dba1d49ad8e2a799568087d5b405108f7533e907d8d`.
The original candidate and final revision have identical mathematical claims
and proof steps; the final-revision check is recorded below. PROOF.md retains
the complete final mathematical proof. Both original versions were preserved
and reauthenticated by exact byte count and hash for this edition.

Two source/presentation qualifications are required for any subsequent public
version, but neither requires a change to the proof mathematics:

1. Cite Hillar--Sullivant, arXiv:0908.1777v2, Theorem 1.1 / Corollary 3.5, as the
   directly inspected source for equivariant Noetherianity. Cohen (1987,
   Theorem 7) is a historical attribution stated by Kummer--Riener; the original
   Cohen text has not been inspected in this audit.
2. Prominently acknowledge the prior proof announcement. Kummer--Riener's final
   2025 article, printed page 42, credits an announced proof by Nicolà Schnieper
   using the Shift Theorem. Its reference [21] identifies *Orbit closures and
   G-irreducibility*, University of Bern master's thesis, 2024. This audit has
   not obtained or checked that thesis. This work must therefore be described
   as an alternative proof of a previously announced result, not as the first
   resolution of an unqualified current open problem.

### Final editorial revision checked

The final authored revision has SHA-256
`82b63f5602865cbf1a35d9d58bf281d3ccb472206ef2af1cc4450483d4cc5f1a`.
Its exact candidate-to-final diff was read and retained for integrity verification.
The changes add the prior-proof credit, replace the direct source citation,
update local-review status, and supply references. All mathematical lemmas,
proof steps, and the claim are unchanged. The two qualifications above are
therefore satisfied by this final revision, and **the same mathematical
acceptance applies to that exact final pin**. The public edition preserves
all mathematical material, with exact publication-facing editorial changes.
ACCEPTANCE.json binds the distributed proof and audit by hash.

This is an independent mathematical review of a proof, not formal verification,
external peer review, an exhaustive literature search, or a novelty certificate.

## 1. Exact category and primary-source match

Set `S = K[x_ij : i in N, 1 <= j <= n]`, with `n` a positive finite integer,
and `G = union_m Sym(m)`, acting by finite-support permutations of `i`. Let
`X = Spec(S)` contain all ordinary prime ideals and let `Q = KQ(X/G)`.

The final Kummer--Riener PDF was read directly in the following places:

- Printed page 30 / PDF page 3: the standing field is algebraically closed and
  uncountable; `Spec(A)` and its closed/maximal-point subspace are distinguished.
- Printed page 32 / PDF page 5: the ring, finite width, finite-support group,
  and action are exactly those above.
- Printed pages 41--42 / PDF pages 14--15: the orbit quotient, Kolmogorov
  identification, Conjecture 3.24, and the reduction to sobriety.
- Printed pages 45--46 / PDF pages 18--19: bibliographic entries, particularly
  [4], [11], [19], and [21].

Printed page 42 was also rendered and visually inspected. The final-version
proof announcement is unambiguous. The source still uses the label Conjecture
3.24; that label alone is not evidence that no prior proof was announced.

The candidate does not replace `X` by its rational points, use an invariant-ring
quotient, silently switch to the full permutation group, or introduce an action
on the coefficient field. These distinctions are essential.

## 2. Closed-set lattice and the core formula

### 2.1 Quotient closed sets

For the orbit quotient map `pi: X -> X/G`, a subset downstairs is closed exactly
when its inverse image is closed. The inverse image is necessarily G-stable.
Conversely, a G-stable closed subset `Z` is a union of complete orbits, so
`pi^{-1}(pi(Z)) = Z`; by the quotient topology `pi(Z)` is closed. This is a
bijection, not merely an injection in one direction.

Every closed subset of any space is saturated under topological
indistinguishability: indistinguishable points belong to exactly the same
closed sets. Thus passing from `X/G` to `KQ(X/G)` preserves the entire closed-set
lattice. The composite `q: X -> Q` is surjective.

The ordinary spectrum correspondence identifies closed subsets with radical
ideals. Stability of the closed set is equivalent to stability of its radical
ideal. This uses the ordinary prime-spectrum identity `I(V(J)) = sqrt(J)`,
which does not require finite type or a Nullstellensatz for rational points.

### 2.2 Point closures

For a prime ideal `P`, the ideal of the set of points `{gP : g in G}` is
`intersection_g gP`. This ideal is radical, since an intersection of prime
ideals is radical. Consequently its vanishing set is precisely the Zariski
closure of the orbit. That closure is G-stable: each automorphism preserves
closure and permutes the orbit.

It is the least G-stable closed set containing `P`. By the checked closed-set
bijection, its image is the least closed subset of `Q` containing `q(P)`.
Therefore the candidate's formula

`q^{-1}(closure_Q({q(P)})) = V(intersection_g gP)`

is valid. No assertion that an arbitrary quotient map preserves closures of
arbitrary subsets is being used.

### 2.3 Irreducibility gives radical G-primality

Let `C` be nonempty irreducible closed in `Q`, and write `q^{-1}(C)=V(I)` with
`I` radical and G-stable. Nonemptiness makes `I` proper. If `A,B` are G-stable
ideals and `AB` is contained in `I`, then

`V(I) subset V(AB) = V(A) union V(B)`.

Both latter closed sets descend. Intersecting them with `C`, if necessary,
expresses `C` as a union of two closed subsets of itself. Irreducibility forces
one to equal `C`; pulling back and taking vanishing ideals gives `A subset I`
or `B subset I`. Radicality of `I` is exactly what licenses the last step.

This is G-primality of the radical ideal. Ordinary primality of `I`, or ordinary
irreducibility of `V(I)`, is neither concluded nor needed.

## 3. Countable reduced G-prime ring lemma

The lemma is correct for any group `H`; countability of `H` is not needed.
Rings here are commutative with identity, and the ring is assumed nonzero.

### 3.1 The translate-product selection

For nonzero `a,b`, suppose `a h(b)=0` for every `h`. Then for all `u,v`,

`u(a) v(b) = u(a (u^{-1}v)(b)) = 0`.

The H-stable ideals generated by the two orbits are nonzero. Every product of
their generators is zero, so distributivity and commutativity make their ideal
product zero. This contradicts the G-prime ring hypothesis. Hence some `h`
has `a h(b) != 0`.

Enumerate every nonzero element `a_i`. Given a nonzero finite product `t_m`,
apply this property to `t_m` and the next `a_i`. This is an ordinary countable
recursion, with no problematic transfinite limit stage. It produces the claimed
nonzero products. Finite rings are handled by repeating the finite enumeration.

### 3.2 Repeated powers in the multiplicative set

This is a genuine hazard and the candidate handles it correctly. Let
`b_i=h_i(a_i)` and let `z = product_{i<=m} b_i^{e_i}` be any monomial in the
selected elements, allowing zero exponents. Choose an integer
`d >= max(1,e_1,...,e_m)`. Then

`t_m^d = z * product_{i<=m} b_i^{d-e_i}`.

If `z=0`, then `t_m^d=0`. Reducedness would imply `t_m=0`, contradicting the
construction. Thus zero is absent from the entire multiplicative set, not just
from the squarefree partial products. The empty product is 1 and is nonzero.

### 3.3 Prime and zero core

Localization at this multiplicative set is a nonzero ring, so it has a maximal
ideal by the ordinary maximal-ideal theorem. Its contraction is prime and
avoids the set. In particular `h_i(a_i)` is not in this prime `p`; equivalently
`a_i` is not in `h_i^{-1}p`. Every nonzero element is excluded from at least one
translate of `p`, proving `intersection_h hp = 0`.

The construction gives an ordinary prime, not necessarily a maximal ideal of
the original ring. The latter stronger conclusion is neither justified nor
needed. Maximality is used only after localization.

## 4. The two scalar-extension lemmas

### 4.1 Arbitrary intersections of subspaces

Choose a k-vector-space basis `E` of `L`. Then
`V tensor_k L` is the direct sum over `E` of copies of `V`. For every subspace
`W`, its scalar extension is the direct sum over the same basis of copies of
`W`. A tensor has only finitely many nonzero coordinates in that direct sum.
It lies in every `V_alpha tensor L` exactly when each of its coordinates lies
in every `V_alpha`. This proves the arbitrary-intersection identity exactly as
claimed, even when the family and extension degree are uncountable.

The proof is not an appeal to an invalid general assertion about flat
extensions. For comparison, extension from `Z` to `Q` sends each ideal `(2^m)`
to all of `Q`, while the intersection of the `(2^m)` is zero. The candidate
correctly restricts the statement to scalar extension of vector spaces.

For an ideal `J` of `S_0`, its image `J tensor_k K` inside `S_0 tensor_k K`
is exactly its extended ideal `JS`: products by `s tensor lambda` remain
in the subspace, and all pure tensors `j tensor lambda` are generated by `j`.
Thus applying the vector-space lemma to the ideals `gP_0` is legitimate.

### 4.2 Primeness over an algebraically closed field

The candidate's specialization proof that `A tensor_k L` is a domain is valid
for every k-domain `A`, with no finite-type hypothesis on `A` or `L/k`.

If nonzero tensors `u,v` multiply to zero, each admits a representation in
which the coefficients from `A` are k-linearly independent. At least one scalar
coefficient in each representation is nonzero; reorder so these are the first.
The finitely many scalar coefficients generate a finite-type k-subalgebra
`B` of the field `L`. Tensoring the injection `B -> L` with the k-vector space
`A` is injective. Hence the same product relation already holds in `A tensor B`.

The algebra `B[(lambda_1 mu_1)^{-1}]` is nonzero and finite type over k.
Its residue field at a maximal ideal is a finite extension of k by the weak
Nullstellensatz, and therefore equals k because k is algebraically closed.
The resulting specialization keeps both selected coefficients nonzero.
Linear independence of the `A` coefficients then keeps both specialized
elements nonzero. Their zero product contradicts the domain property of `A`.

Inverting the product is sufficient to keep both coefficients nonzero. No
specialization of the algebra `A` is taken, so its potentially infinite type
causes no problem. The argument is characteristic independent.

## 5. Descent and ascent of the required prime

### 5.1 A countable algebraically closed field of definition

The set of monomials in countably many variables is countable: each monomial
has finite support and finite nonnegative integer exponents. It is a K-basis of
`S`, so every K-linear subspace, in particular `I`, has an at-most-countable
basis. This concerns vector-space dimension, not the cardinality of the set
of K-points or the set of all polynomials over an uncountable field.

Each basis polynomial uses finitely many coefficients. The union of the
coefficient sets is countable. The subfield `F` generated by them and the prime
field is countable, including in positive characteristic. Its relative algebraic
closure `k` in `K` is countable because there are countably many polynomials
over `F`, each with finitely many roots. It is algebraically closed: a polynomial
with coefficients algebraic over `F` has roots in the algebraically closed field
`K`, and each such root is algebraic over `F` by transitivity. Thus all those
roots already belong to `k`.

This field may depend on `I`. There is no assertion of a single countable field
that simultaneously defines all ideals.

### 5.2 Extension, contraction, and the group action

Put `S_0=k[x_ij]` and `I_0=I intersection S_0`. Every chosen K-basis polynomial
lies in `I_0`; hence `I` is contained in the K-span of `I_0`, and therefore in
`I_0 S`. The reverse inclusion holds because `I` is an ideal containing `I_0`.
Thus `I=I_0 S` exactly. Properness and radicality pass to the contraction.

Every row permutation fixes coefficients, so it preserves `S_0`; since it
preserves `I`, it preserves `I_0`. No large field of definition for the group
action is needed. The action is already defined over the prime field.

If G-stable ideals `A_0,B_0` satisfy `A_0 B_0 subset I_0`, their extensions are
G-stable and their product is contained in `I`. G-primality of `I` forces one
extension into `I`, and contracting forces the corresponding original ideal
into `I_0`. Thus `I_0` is G-prime. Only this direction of descent is needed;
no general invariance of G-primality under field extension is asserted.

### 5.3 The quotient ring and the prime upstairs

`S_0` is a countable ring since both its field and monomial set are countable,
and each polynomial has finite support. Its quotient `R_0=S_0/I_0` is nonzero,
countable, and reduced. G-stable ideals in the quotient lift to G-stable ideals
containing `I_0`. Thus its nonzero G-stable ideals cannot have zero product.
All hypotheses of the countable-ring lemma have now been supplied.

The resulting prime in `R_0` lifts to a prime `P_0` of `S_0`. Intersections
commute with inverse image under the quotient map, giving
`intersection_g gP_0 = I_0`.

Let `P=P_0 S`. The standard scalar-extension quotient isomorphism gives
`S/P = (S_0/P_0) tensor_k K`. Its right side is a domain by the checked
specialization lemma; in particular it is nonzero. Hence `P` is an ordinary
proper prime ideal of `S`.

For each `g`, extension commutes with the action: `g(P_0S)=(gP_0)S`. The
checked vector-space intersection lemma then yields

`intersection_g gP = (intersection_g gP_0) tensor_k K = I_0 tensor_k K = I`.

Every equality is in the same ambient space `S=S_0 tensor_k K`. There is no
interchange of a localization with an infinite intersection.

## 6. Sobriety, Noetherianity, and the spectral conclusion

The core realization just proved applies to the radical G-prime ideal
associated to each nonempty irreducible closed `C` in `Q`. The core formula
and surjectivity of `q` show `closure({q(P)})=C`. This proves existence of a
generic point. The Kolmogorov quotient is T0, so two points cannot have the
same closure unless they agree. Generic points are therefore unique: `Q` is
sober. No extra closed-point condition is inserted.

For the remaining hypotheses, Hillar--Sullivant proves Noetherianity of
`K[X_[r]xP]` as a module for the skew action of its polynomial ring and the
symmetric group. Its submodules are exactly stable ideals. Transpose the two
indices and take `r=n` to obtain the current polynomial ring.

The paper's notation initially allows all permutations of `P`, but its
Corollary 3.5 proof chooses permutations that are the identity above a finite
bound. Specifically, an increasing injection restricted to the finite set of
indices of a polynomial extends to such a finite permutation. Thus every
finite-support-stable ideal is stable under the increasing-map monoid, and
the finite equivariant generation theorem applies to it. Alternatively, every
full permutation agrees with some finite-support permutation on each finite
polynomial support, so the two notions of stable ideal coincide. This does
not assert that the two groups have the same individual point orbits.

Finite generation of each stable ideal implies stabilization of every ascending
chain: the union is stable and its finite orbit-generator set lies in one
chain member. In particular chains of stable radical ideals stabilize. Under
the closed-set correspondence this is the descending-chain condition for
closed subsets of `Q`, so `Q` is Noetherian.

Every open subset of a Noetherian space is quasi-compact. To see the precise
argument, its relative-open cover is also a family of opens of `Q`, since the
subset itself is open. The finite unions from the cover form an ascending
family. If no finite union covered the subset, successively adjoining an
uncovered cover member would give an infinite strictly increasing chain of
opens, contradicting Noetherianity. Therefore all opens, including `Q`, are
quasi-compact. They form a basis, and pairwise intersections are open and
quasi-compact. These properties plus sobriety are exactly the spectral-space
axioms in Stacks Project Definition 5.23.1.

The finite-orbit-closure corollary also follows. An invariant closed subset
descends to a closed subset of the Noetherian sober `Q`. Its finitely many
irreducible components have generic points; lift those points to `X` and use
the core formula. Pulling back the finite union recovers the original closed
subset. No finiteness of the ordinary irreducible-component set of `X` is used.

## 7. Adversarial boundary checks

These are logical stress tests, not computational evidence for the theorem.

- **Reducedness is real.** In the countable ring
  `F_2[z_i : i in N]/(z_i^2 : i in N)`, with finite-support permutations,
  two nonzero polynomials can be moved onto disjoint variable supports, making
  their product nonzero. Hence zero is G-prime in the ideal-product sense.
  Yet every prime contains the nonzero nilradical, so no prime can have zero
  G-core. This would defeat the lemma without reducedness. The candidate
  explicitly has reducedness and uses it at the necessary step.
- **Algebraic closedness is real for the ascent lemma.** For example,
  `Q(sqrt(2)) tensor_Q Q(sqrt(2))` is not a domain, though both factors are.
  The candidate never assumes general field extension preserves primality;
  it first constructs an algebraically closed `k`.
- **Scalar extension is narrower than flat base change.** The `Z -> Q`
  example above shows why arbitrary-flat-intersection arguments would fail.
  The candidate's basis-coordinate proof avoids this failure.
- **Ordinary prime points are indispensable.** The invariant diagonal defined
  by `x_i1-x_l1` and all `x_ij` for `j>1` is a fixed copy of `Spec(K[t])`.
  Its generic point is available in the specified category. With rational
  points alone this becomes the infinite cofinite space `A^1(K)`, whose
  whole irreducible closed set has no generic point. The latter is not the
  conjecture's space.
- **No ordinary Noetherianity is smuggled in.** The ordinary ideal generated
  by every `x_i1` is not finitely generated: any proposed finite list uses
  only finitely many row variables, and setting those variables to zero
  leaves an omitted `x_i1` nonzero. This also rules out importing a
  locally-ideal-finite orbit theorem without checking its hypothesis.
- **Finite width is used for Noetherianity.** The prime-core construction only
  needs countably many monomials and a descended action. It does not by
  itself establish spectrality for infinitely many columns or an arbitrary
  group action. No such enlargement of the claim is accepted here.
- **Uncountability is unused, legitimately.** The target's uncountable field
  lies inside the proved scope. The proof needs no rational generic point,
  so it does not invoke a countable-type rational-point Nullstellensatz.
- **All characteristics are covered.** No averaging, division by a group
  order, characteristic-zero theorem, or separability assertion is used.

## 8. Import and limitation register

Specialized mathematical import:

- Hillar--Sullivant, *Finite Gröbner bases in infinite dimensional polynomial
  rings and applications*, arXiv:0908.1777v2, Theorem 1.1 and Corollary 3.5;
  proof of Corollary 3.5 checked, with Theorem 3.1 and surrounding finite-width
  setup read. A whole audit of the underlying Gröbner/Higman proof is not
  claimed. Primary source: https://arxiv.org/abs/0908.1777v2.

Standard imports:

- Existence of maximal ideals in nonzero commutative rings, localization and
  contraction of primes, ordinary prime-spectrum closed-set correspondence,
  and vector-space basis/exactness facts. For the maximal-ideal assertion,
  Stacks Project Lemma 10.17.2: https://stacks.math.columbia.edu/tag/00E0.
- Weak Hilbert Nullstellensatz for finite-type algebras over an algebraically
  closed field. Exact finite-type field statement checked at Stacks Project
  Theorem 10.34.1: https://stacks.math.columbia.edu/tag/00FV.
- The spectral axioms, Stacks Project Definition 5.23.1:
  https://stacks.math.columbia.edu/tag/08YF. Its opening paragraph also records
  Hochster's equivalence with spaces homeomorphic to ring spectra. The
  original Hochster theorem was not independently audited here.
- Standard Noetherian-space finite irreducible decomposition for the stated
  corollary. This can also be proved by Noetherian induction on closed sets.

Scope/status primary source:

- Kummer--Riener, *Equivariant algebraic and semi-algebraic geometry of
  infinite affine space*, Journal of Algebra 666 (2025), 28--46,
  https://doi.org/10.1016/j.jalgebra.2024.11.016.
  Public institutional record:
  https://nva.sikt.no/registration/0198cc8923dc-5250cc93-79cf-4ebe-ae76-31630d0455d9.
  This supplies the exact target and the prior-proof announcement, not the
  new candidate's generic-prime argument.

Comparison sources, not hidden imports:

- Cohen's historical theorem is credited by Kummer--Riener; original text
  uninspected here.
- Schnieper's thesis is identified by the final article; its actual proof,
  statement, and hypotheses are uninspected here.
- The n=1 Nagpal--Snowden result is credited by the primary final article;
  the present proof does not import it.
- No Shift Theorem or Lorenz core-surjectivity theorem is used in the candidate
  or this acceptance. Their applicability is therefore not a missing premise.

The public edition contains the complete authored mathematical proof and audit,
with source-identification and inspection metadata. It distributes no copied
source documents, raw datasets, code, or private coordination material. Hashes
authenticate retained bytes; they do not certify a theorem, novelty, or priority.
