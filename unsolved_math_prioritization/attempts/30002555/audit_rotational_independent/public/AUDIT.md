# Independent full audit: the three-ended rotational obstruction

Problem 30002555 / OWR-12875-003, rank 987. Audit date: 7 October 2026 UTC.

## Disposition

**ACCEPT the frozen candidate as a complete negative answer to the stated
universal exact-matrix-group realization question. No mathematical correction
patch is required.**

The accepted author manifest is
`f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59`.
Its `PROOF.md` has SHA-256
`78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464`.
This disposition applies to those exact bytes, including the cone-model
clarification in Section 6. It is an independent mathematical audit, not a
claim of journal peer review, originality, or a complete classification.

The proof's substantive foundations are classical uniformization and
orientable-surface classification. The modern finite-isometry obstruction is
properly credited. These are legitimate declared dependencies; the candidate
does not claim to reprove uniformization or surface classification.

## 1. Exact target and source alignment

I inspected the complete Valdez contribution, printed pp. 885–888, in the
primary [Oberwolfach report](https://ems.press/content/serial-article-files/46504)
and visually checked Question 4 on printed p. 887. Its quantifiers range over
closed Cantor subsets and countable subgroups of GL+(2,R) without contracting
elements. The requested surface must be tame, infinite genus, have no planar
ends, and have the specified end-space homeomorphism type. This is an actual
matrix subgroup specification, not merely a request for an abstract group
isomorphic to it. Neither a marked action on the end set nor finite flat area
is imposed. The adjacent Jacob's-ladder and finite-area questions are separate.
The contraction inequality in the preceding summary theorem is visibly
inconsistent with its prose; it does not override Question 4's explicit
noncontracting requirement.

I checked the [2017 journal paper](https://msp.org/agt/2017/17-1/agt-v17-n1-p15-s.pdf):
its introductory results do not establish arbitrary-end realization; Theorem
1.2 provides the needed genus-and-nested-end-space classification, and Section
1.4 defines tameness through conical completion neighborhoods and defines the
Veech group as the full derivative image. No discreteness assumption on the
prescribed countable matrix group is present. Thus density of an infinite
rotation subgroup in SO(2) is not a failure of admissibility.

I independently retrieved [ARSVW v2](https://arxiv.org/pdf/2311.00158v2), verified
the 23 February 2026 version stamp, and inspected its relevant definitions,
theorems, and proofs. Theorem 1.8 states the finite-isometry obstruction;
Lemma 2.17(2), Theorem 2.18, Corollary 2.19, and the proof of Theorem 1.8 give
its mechanism. Definition 3.1 and Section 3.1 were additionally checked in
rendered pages 13–14: the isometry subgroup is the rotational derivative
preimage, and the flat metric need not be complete. The author's
[publication page](https://m-artigiani.github.io/research/papers/) describes the
paper as to appear in Algebraic & Geometric Topology. I did not inspect a final
journal version. Its other realization theorems cannot be used without their
topological hypotheses.

## 2. Independent reconstruction of the mathematical implication

### 2.1 The underlying surface, not its possibly nonmanifold completion

A translation atlas is a complex atlas because its transition maps are
holomorphic translations. If a convention includes a finite cone point of
angle 2πk, its punctured neighborhood has a coordinate model with developing
map proportional to w^k. The coordinate w extends the complex structure
over the point. An orientation-preserving affine automorphism with rotational
derivative is holomorphic off those points; its continuity at each included
point makes its coordinate expression bounded near the puncture. Removable
singularities applied to the map and inverse give a biholomorphic extension.

If the surface convention instead excludes cone points, the original
underlying surface already has its complex atlas. There is no need to fill
punctures or alter its ends. Infinite-angle completion points are not ordinary
manifold points and are never added to the Riemann surface in this argument.
Consequently no inference from flat completeness, or from the completion
being a topological surface, is made. The proof works on precisely the
surface to which the end condition applies. This settles the main convention
risk in applying a conformal argument to tame but incomplete flat metrics.

Let I be the full preimage of SO(2) under the derivative homomorphism D. Then
I consists of holomorphic automorphisms of that Riemann surface, and
D(I)=Γ(S)∩SO(2). The latter equality holds simply by taking any affine lift
of a derivative in the intersection. It does not require a section of D,
injectivity of D, or an action of Γ(S) itself on S.

### 2.2 Uniformization and a discrete normalizer

Infinite genus gives a nonabelian fundamental group. By uniformization its
simply connected conformal cover is the sphere, plane, or disk. The sphere
case is impossible: every nonidentity holomorphic sphere automorphism has a
fixed point, so a free deck group is trivial. For the plane, a fixed-point-free
nonidentity map z↦az+b must have a=1; hence a free holomorphic deck group
consists of translations and is abelian. The only possible cover is therefore
the disk, equivalently the upper half-plane H. Write S=H/Λ, with Λ a
nonabelian discrete subgroup of PSL(2,R).

All holomorphic automorphisms lift to H. A lift normalizes Λ, and every
normalizer element descends, so Aut(S)=N(Λ)/Λ. Here quotienting by Λ is
essential: infinitely many lifts of one automorphism do not constitute
infinitely many automorphisms.

To verify discreteness of N(Λ), choose noncommuting a,b∈Λ. A nontrivial
sequence n_j∈N(Λ) tending to the identity would eventually satisfy
n_j a n_j^(-1)=a and n_j b n_j^(-1)=b, because both conjugate sequences
belong to the discrete group Λ. For a nonidentity element of PSL(2,R), its
centralizer is abelian, as is seen in each elliptic, hyperbolic, and parabolic
normal form. Thus a and b cannot both centralize such an n_j. This proves
identity isolation and hence discreteness. No finite-generation assumption
on Λ is used: two noncommuting elements suffice.

For clarity, the compact-transporter step is also valid. The action of
PSL(2,R) on H is proper, with compact rotation stabilizer. Compact sets of
source and target positions restrict the transporter to a compact subset of
the group. A discrete subgroup is closed and meets such a compact set in
finitely many points.

Finally, compact K⊂S can be covered by finitely many smaller coordinate
neighborhoods whose closures lie inside evenly covered neighborhoods. Pick
one lift of each closure. Their finite union L is compact and maps onto K.
If a coset [n] sends some x∈K to y∈K, choose u,v∈L over x,y. For a deck
transformation λ, n(u)=λ(v); hence λ^(-1)n sends L to meet L. Finitely many
normalizer elements have this property, so only finitely many cosets do.
This proves compact-set proper discontinuity of Aut(S). It uses the complete
uniformizing hyperbolic geometry upstairs, not completeness of the original
flat metric.

### 2.3 The core really is nondisplaceable

For three ends, all accumulated by genus, surface classification identifies
S with a compact pair of pants K whose three boundary circles are attached
to one-ended infinite-genus surfaces with one boundary circle. The complement
S\K has three components, each carrying exactly one end of S.

Suppose a homeomorphism h satisfies h(K)∩K=∅. Since h(K) is connected, it
lies entirely in one component U_i of S\K. The union of K with the other
two components is connected and disjoint from h(K). It therefore lies in
one component of S\h(K), carrying at least two distinct ends of S. But h
induces a permutation of the three ends, and its image of each original
complementary component carries exactly one end of S. This is impossible.

The phrase “carries one end” is correctly relative to ends of the ambient
surface S. An open complementary component may additionally have a boundary
end if regarded as a separate abstract surface; that does not affect this
argument. Likewise, permuting the three ends cannot evade the contradiction.
The same reasoning holds for any finite n≥3. For n=2 its numerical step is
false, so it gives no obstruction for Jacob's ladder.

All automorphisms in I must move K to meet K. Compact-set proper
discontinuity therefore makes I finite, and so its image Γ(S)∩SO(2) is
finite. Even an infinite translation kernel could not evade this conclusion:
it would itself lie inside the now-finite group I.

### 2.4 The exact witness and its infinite-order proof

Let B=[[3,-4],[4,3]] and A=B/5. Exact multiplication gives AᵀA=I and
det(A)=1. Thus every integer power is a Euclidean rotation and no power
strictly shortens every nonzero vector. The determinant-one condition also
rules out a strict operator-norm contraction after an arbitrary linear
conjugacy, although only the displayed orthogonal matrices are needed.

The author's recurrence proof of infinite order is correct for all n≥1:
u_n=tr(B^n) satisfies u_0=2, u_1=6, and
u_(n+1)=6u_n−25u_(n−1), whence u_n≡1 mod 5 for n≥1. The value forced by
A^n=I would instead be u_n=2·5^n≡0 mod 5.

As a distinct algebraic check, directly reducing the matrix identity gives
B²≡B mod 5 with B nonzero mod 5. By induction B^n≡B mod 5 for every
positive n. If A^n=I, then B^n=5^nI reduces to zero, another contradiction.
This is an all-n proof; the independent finite Gaussian-integer computations
are only supplementary controls.

The points 0, 2/3, and 1 belong to the middle-thirds Cantor set using ternary
expansions 0.000…, 0.200…, and 0.222…. The finite set is nonempty and
closed and has three distinct elements. The map n↦A^n identifies Z with G,
so G is countably infinite. A surface realizing the specified pair would
have an infinite subgroup G⊂Γ(S)∩SO(2), contradicting the finite-image
conclusion. In fact even A∈Γ(S) is impossible.

## 3. Conjugacy and cone-model check

The optional conjugacy statement in Section 6 is sound. Postcomposing all
translation charts by L∈GL+(2,R) preserves translations as transition maps,
keeps the underlying topology, and changes the derivative group to
LΓ(S)L^(-1). The least and greatest singular values of L bound the new
length metric above and below by positive constant multiples of the old
one, giving corresponding metric completions.

Bilipschitz equivalence alone would not justify an exact conical local
model. The additional argument in the frozen text supplies what is needed:
a finite or infinite cyclic cover of a punctured round disk becomes the
same cover of a punctured ellipse. A smaller round disk about the origin
contained in that ellipse has the same punctured fundamental group, so its
preimage remains the requisite connected cyclic cover. In the changed
translation coordinates the pulled-back metric is exactly Euclidean, not
merely comparable to Euclidean. Completing that neighborhood gives the
required finite or infinite cone model. Ordinary regular points remain
regular. Thus tameness is preserved, and the matrix-conjugacy extension
introduces no extra gap. It is not needed for the main counterexample.

## 4. Adversarial controls and reproducibility

Every author-manifest member was independently size- and hash-checked. The
author verifier succeeded under ordinary and optimized Python, replaying
1,996 exact checks in each mode. The independent script additionally passed
4,160 controls, including 1,024 Gaussian-integer powers, inverse powers,
norm identities, the mod-five idempotent matrix check, and source-packet
preservation. A finite quarter-turn is a negative control against the false
inference “rational orthogonal implies infinite order.” A nonorthogonal
determinant-one matrix is a control against “determinant one implies
isometry.” The two-end inequality is tested as a negative control.

Nine verifier fault classes were each rejected in ordinary and optimized
Python: wrong anchor, modified proof byte, missing member, extra member,
symlink member, duplicate JSON key, duplicate inventory entry, unsafe path,
and Boolean byte count. All mutations were confined to disposable copies.
The original packet was verified unchanged afterward. These tests establish
the stated controls, not security against arbitrary hostile executable
verifiers; reproducibility relies on the externally anchored reviewed bytes.

Run the independent controls with Python 3.10+:

    python -B INDEPENDENT_CHECKS.py PATH_TO_FROZEN_AUTHOR_PACKET

The output must match `INDEPENDENT_RESULTS.json`. This audit does not count
finite computations as proofs of infinite-order induction, uniformization,
proper discontinuity, or the surface classification/core argument.

## 5. Limits, credit, and acceptance scope

- The conclusion refutes the universal statement using one admissible pair;
  a full realization classification is neither needed nor provided.
- It does not forbid abstract infinite cyclic Veech groups generated by
  other matrices, and it does not settle the Jacob's-ladder lattice question.
- It does not require finite area, flat completeness, finitely many cones,
  a trivial derivative kernel, or a splitting of the derivative map.
- The finiteness mechanism is already present in the credited literature.
  No claim of priority for the explicit rational witness is justified or
  necessary.
- This audit reviewed the complete frozen candidate, its computational
  controls, and the relevant primary-source passages and proofs. Unrelated
  contributions in the 74-page workshop report and unrelated construction
  proofs in the cited papers were not subjects of this audit.
- The author packet was preserved. This audit contains original analysis,
  scripts, receipts, and public bibliographic/verification metadata; source
  PDFs, extracted source text, and rendered source pages are not included.

Within this scope the proof is complete, and no actual gap or necessary
correction was found.
