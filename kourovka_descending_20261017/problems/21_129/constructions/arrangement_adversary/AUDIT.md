# Adversarial audit of the arrangement and lattice probe

Audit timestamp: **2026-10-24T20:05:58Z**. Bounded audit completion: **100%**.
This is an audit of local deductions, not a resolution of Kourovka 21.129;
best-guess progress toward that research goal remains **5%**.

## Verdict and required correction

**Lemma 3.1, the rank-two calculations, Proposition 4.1, the added
Proposition 4.2, and Proposition 5.1 are valid under their stated hypotheses.**
Proposition 5.1 may be promoted from candidate to verified deduction. No
quasi-isometry of the exceptional types has been constructed, and neither
novelty nor a solution of Kourovka 21.129 follows.

The initial CHL source identification was too broad. Theorem 7.1 presents a
quotient of the orbit-complement group for the **Schwarz symmetry group G**.
It identifies that group as the spherical Artin group only when G itself is
the relevant Coxeter group with its full mirror arrangement. The original
real Coxeter group W need not be this G. CHL §3.5 supplies a separate
representation of the original Artin group, and suffices for the claimed
finite-power obstruction. The parent has applied this correction. For full
precision, those maps must be called the **Coxeter-orbit CHL monodromy maps**,
without asserting their image is exactly the group presented by Theorem 7.1.
The parent applied that final wording correction before this audit closed.

The archived preprint places Tables 2–4 in §8, not §7.3. That correction has
also been applied. The independent sub-audit in `chl_source_check/` preserves
the detailed source distinctions.

## 1. Support and parabolic injection

The support argument does not assume the parabolic embedding it proves.
Let M_S be the positive monoid with the Artin presentation. A positive
relation preserves its support. A relation path beginning at a T-word stays
entirely inside T-words; every relation used is consequently a T-relation.
Thus M_T→M_S is injective directly from the presentations.

Every subdiagram T of a spherical Coxeter diagram is again spherical. Apply
the spherical Garside inputs to its *abstract* Artin group A_T. In particular,
every element has the form uv^{-1} with u,v∈M_T. This fraction property also
follows from the lattice order stated in Cumplido–Paris §3: choose a common
upper bound u≥1,g, giving v=g^{-1}u positive and g=uv^{-1}.

If g=uv^{-1} maps to 1 in A_S, monoid injection M_S→A_S gives u=v in M_S,
and the preceding support argument gives u=v in M_T. Therefore A_T injects.
There is no dependence on a previously established embedding A_T→A_S.

Cumplido–Paris §3 gives Z(A_S)=⟨δ⟩, δ=Δ or Δ², with an explicit positive
word involving every generator. For k>0 and u,v∈M_T, an equality
δ^k=uv^{-1} would yield δ^k v=u in M_S, contradicting support. Negative k
reduces to its inverse. The empty subset T causes no exception. For rank 1,
the only proper T is empty; the lemma remains valid.

## 2. Rank-two certificate, including the smallest labels

For m=2k≥4, put y=st. The relation (st)^k=(ts)^k is exactly
y^k=s^{-1}y^k s, yielding ⟨s,y | [s,y^k]=1⟩. The central element is
z=y^k. In the quotient by z, s lies in the infinite cyclic factor of
Z*C_k, while t=s^{-1}y is cyclically reduced of length 2. Both are infinite.
This includes k=2 (m=4); k=1 would make the argument for t fail, but m=2
is a commuting nonedge and is correctly excluded.

For m=2k+1≥3, put y=st and x=y^k s. The Artin relation is equivalent to
s y^k s=y^{k+1}, hence x²=y^{2k+1}. Conversely, x²=y^{2k+1} and
s=y^{-k}x recover that original relation. Thus the change of presentation is
two-sided, with z=x²=y^m, s=y^{-k}x, t=x^{-1}y^{k+1}. In C_m*C_2, the
nonzero exponents −k and k+1 give cyclically reduced words of length 2 for
s and t. This includes k=1 (m=3).

In either parity, the exponent-sum homomorphism sends z to a positive integer,
so z is infinite. A relation s^a z^b=1 first implies a=0 in the central
quotient and then b=0 in the original rank-two group. The same applies to t.
Commutation with z now proves each displayed subgroup is Z². In rank≥3,
Lemma 3.1 embeds the entire two-generator parabolic in Q, so no new central
quotient relation invalidates this independence argument.

## 3. The non-relative-hyperbolicity deduction

Anderson–Aramayona–Shackleton, Theorem 2, requires: G finitely generated; a
generating set of at least two infinite-order elements; connected
commutativity graph (allowing commuting nonzero powers); and at least one
edge giving a rank-two free abelian subgroup. The proposed U satisfies all
of these, in fact with every subdividing edge giving Z². The source's
conclusion is exactly failure of strong relative hyperbolicity with respect
to every finite family of proper finitely generated subgroups.

Possible duplicate elements among different rank-two centers in U do not
create a gap: identifying vertices in a connected subdivided graph keeps it
connected, and the endpoints of every used edge remain distinct by the Z²
independence check. The original standard generators remain in U and
generate Q. Thus the proof does not need a parabolic-intersection theorem.

An equivalent direct check uses the ingredients of the cited proof. An
embedded Z² lies in one conjugate peripheral H. It contains a standard
generator s. For any Coxeter edge {s,t}, the commuting infinite element z_st
forces z_st∈H by almost malnormality: H∩z_st H z_st^{-1} contains ⟨s⟩.
Then H∩tHt^{-1} contains ⟨z_st⟩, forcing t∈H. Connectedness propagates
this to every standard generator, so H=Q, contrary to properness.

The source boundary is correct: rank-two irreducible central quotients are
Z*C_k or C_2*C_m and virtually nonabelian free; rank 1 gives the trivial
quotient. The proposition asserts nothing for reducible groups. It rules
out isomorphism with the stated rank-one lattices; the note does not infer
quasi-isometry cancellation from Q×R and does not claim to do so.

## 4. CHL maps and the stronger free kernel

CHL §3.5 identifies A_W≅π₁(W\\V°). For |κ_i|<1 the standard-generator
image is semisimple with eigenvalues 1 and −exp(πiκ_i), so rational κ_i
gives finite order. In Tables 2–4, κ_H=1−2/q_H and every q_H is a finite
integer ≥2. The F4 zero-weight q_H=2 boundary is included in |κ_i|<1.
The κ_i=1 boundary is excluded; the source warns semisimplicity may fail
there. Rationality alone would not justify a claim at that boundary.

If ρ(s^q)=1, the exponent-sum map proves s infinite, so the cyclic kernel
is infinite and remains infinite on each finite-index subgroup. Whenever
the projective map factors through the full Q, Lemma 3.1 proves its generator
image remains infinite as required. The word “whenever” is meaningful:
killing a radial Δ² alone would not establish full-center factoring in a
case Z(A)=⟨Δ⟩. Affine parabolic holonomy also needs care because the radial
holonomy can be translation. The note's conditional assertion avoids this
unproved identification.

Crisp–Paris (2001), Theorem 1, applies to arbitrary integers N_s≥2 and says
the subgroup on those generator powers has exactly the commuting relations
for Coxeter labels 2. Taking the two endpoints of any Coxeter edge gives
F₂=⟨s^{N_s},t^{N_t}⟩ inside ker ρ. Its finite-index intersections have
rank at least 2 by Nielsen–Schreier. Its intersection with Z(A) is trivial
because that intersection is central in F₂. Therefore F₂ also embeds in Q,
including rank 2, and lies in the induced projective kernel when defined.

For any homomorphic lift to an extension with abelian kernel, the image of
this F₂ is abelian, so [F₂,F₂] lies in the lifted kernel. This subgroup is
infinite (for example, its nontrivial commutator has infinite order).
Consequently the lifted homomorphism is not a quasi-isometric embedding.
Centrality of the extension kernel is unnecessary; abelianity is enough.
The statement concerns lifts of the given homomorphism and imposes no
obstruction on unrelated nonhomomorphic quasi-isometries.

## Primary source custody

All source inputs were read from the parent's archived primary texts:

- `../sources/CumplidoParis2021.txt`, §3, especially lines 218–244.
- `../sources/AndersonAramayonaShackleton2007.txt`, §2–3, especially
  Definition 1, Theorem 2, Theorem 3, and Lemma 5 (lines 61–185).
- `../sources/CouwenbergHeckmanLooijenga2005.txt`, §3.5 (lines 2120–2160),
  Definition 4.2, Theorem 7.1 (lines 3636–3687), §8 Tables 2–4
  (lines 3924–3956).
- `../sources/CrispParis2001.txt`, Theorem 1 (lines 74–80).

No external individual was contacted. No Git, push, release, or publication
action was taken by this audit.
