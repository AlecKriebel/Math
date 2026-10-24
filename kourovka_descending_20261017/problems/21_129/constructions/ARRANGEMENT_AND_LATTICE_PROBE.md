# Arrangement and lattice construction probe

Status: verified elementary obstructions and an independently audited
central-quotient non-relative-hyperbolicity lemma; **no solution of Kourovka 21.129** and no
novelty claim. Author metadata is in `RESEARCH_LOG.md`.

## 1. Exact target and scope

We seek spherical Artin groups A and B that are quasi-isometric and not
abstractly commensurable. They may be reducible. A common finite cover would
instead prove commensurability; a common proper cocompact geometric model could
produce a quasi-isometry without an algebraic identification.

For irreducible A of rank n, write Q=A/Z(A), and P for the pure Artin subgroup.
Cumplido–Paris Proposition 3.1 gives P ≅ (P/Z(P)) × Z and identifies the latter
central quotient with a finite-index subgroup of Q. Thus the geometric
construction target is Q × R up to quasi-isometry. Cancelling an R-factor from
an arbitrary quasi-isometry is **not** assumed here.

Candidate equal-rank pairs F4/H4 and Dn/En for n=6,7,8 cannot currently be called
noncommensurable on the basis of Cumplido–Paris or Soroko 2021. In contrast,
Soroko proves D4/F4 and D4/H4 noncommensurable. None of these pairs has a
quasi-isometry constructed here.

## 2. Deleting hyperplanes: the natural map fails

**Lemma 2.1.** Let H be a finite set of distinct complex affine hyperplanes in
C^n, let K be a proper subset, and put M_H=C^n minus their union. The inclusion
j:M_H→M_K induces a homomorphism j_* with infinite kernel. If the fundamental
groups are finitely generated, j_* is not a quasi-isometric embedding for word
metrics. The same holds on every finite-index subgroup of π1(M_H).

**Proof.** Choose L∈H\K and a point of L lying on no other member of H. A small
normal disk about that point meets no other hyperplane. Its boundary is a
meridian μ∈π1(M_H); j(μ) bounds the disk in M_K. An affine linear defining
function ℓ_L gives a map M_H→C* whose induced winding-number homomorphism sends
μ to 1. Hence μ has infinite order. Every finite-index subgroup contains μ^d
for some d>0, so its restricted kernel is also infinite.

If a group homomorphism f is a (λ,c)-quasi-isometric embedding, any g∈ker f
satisfies |g|≤λc. A bounded ball of a finitely generated group is finite, so ker
f must be finite. This contradicts the preceding paragraph. ∎

**Consequence.** The standard Dn⊂Bn reflection-arrangement comparison (adding
the coordinate hyperplanes) cannot yield a quasi-isometry by the induced
complement-inclusion homomorphism. This says nothing about arbitrary maps of
the groups. Nor does a nontrivial kernel automatically prevent a map between
the underlying manifolds from having some other useful coarse property.

## 3. A support argument for proper parabolics

The following elementary argument supplies the exact boundary condition needed
when passing to a central quotient.

**Lemma 3.1.** Let A=A_S be an irreducible spherical Artin group and T⊊S. Then
the standard parabolic A_T embeds in A, and A_T∩Z(A)={1}.

**Inputs.** For spherical Artin groups the positive monoid embeds in its group,
and every group element is a fraction uv^{-1} of positive elements. Also,
Z(A)=⟨δ⟩ where δ=Δ or Δ² is positive and has full support S. These standard
Garside facts are stated in Cumplido–Paris §3, with original references to
Brieskorn–Saito and Deligne.

**Proof.** Every positive Artin relation preserves the set of generators that
occur. Consequently two positive T-words can be equal in the full positive
monoid only by applying T-relations: an outside letter can never appear in a
relation path starting at a T-word. This proves injection of positive
parabolic monoids. If uv^{-1}∈A_T maps to 1∈A, then u=v in A, hence in the full
positive monoid by its injection, hence in the T-monoid. This proves A_T↪A.

Suppose δ^k∈A_T with k>0. Write δ^k=uv^{-1} with u,v positive T-words. Then
δ^k v=u is an equality in the positive monoid. Its left side has support S and
its right side has support contained in T, impossible. For k<0 apply the same
argument to the inverse. ∎

Thus every proper standard parabolic injects into Q=A/Z(A).

## 4. Finite powers of meridians in CHL holonomy

Couwenberg–Heckman–Looijenga (CHL), §3.5, starts with a real Coxeter group W
and W-invariant Dunkl weights. The monodromy representation has domain
π1(W\V°)≅A_W by Brieskorn's identification. For |κ_i|<1 the image of the
standard generator σ_i is a semisimple complex reflection of angle
π(1+κ_i). Rational κ_i therefore makes this image finite order. The weights
in the relevant CHL Tables 2–4 (archived preprint §8) satisfy
κ_H=1−2/q_H with finite integers q_H≥2, hence 0≤κ_H<1. These include
E6,E7,E8,F4,H3,H4 examples; F4 permits two mirror-orbit parameters. Thus the
corresponding representations of the original spherical Artin groups kill a
positive power of every standard generator. No assertion about the exact
order of each image is needed.

CHL Theorem 7.1 describes the analogous complete holonomy quotient by
finite-power stratum-loop relations. Its domain is π1(G\V°), where G is the
**Schwarz symmetry group**, which need not be the original Coxeter W. We do
not identify those two domains without proof. The finite-power assertion for
A_W above uses §3.5 directly, so this distinction does not affect it. The
boundary κ_i=1 is excluded: CHL explicitly warns that monodromy may fail to
be semisimple there.

**Proposition 4.1.** For a spherical irreducible Artin group A of rank≥2, a
homomorphism ρ that kills a positive power of a standard generator has infinite
kernel on every finite-index subgroup. The same assertion holds for the
induced projective holonomy homomorphism from Q whenever it is defined.

**Proof.** A standard generator s has infinite order by the exponent-sum map
A→Z, s↦1. Thus ⟨s^q⟩ is an infinite subgroup of ker ρ. Every finite-index
subgroup meets it in an infinite subgroup. For Q, Lemma 3.1 embeds the
rank-one proper parabolic ⟨s⟩, so its image is still infinite. ∎

Hence the Coxeter-orbit CHL monodromy maps just constructed, including their finite-index
restrictions and their projectivizations, are not quasi-isometric embeddings.
Passing to a torsion-free finite-index subgroup of the **image** does not fix
this: its inverse image still contains the same infinite kernel. Shared CHL
orbifolds or holonomy lattices therefore do not by themselves give a common
finite cover or quasi-isometry of the original spherical Artin groups.

This is a statement about the given quotient maps. It does not prove that the
groups cannot be quasi-isometric by some unrelated map.

There is a stronger obstruction to repairing such a construction just by
restoring a central direction.

**Proposition 4.2.** Suppose A is an irreducible spherical Artin group of
rank≥2 and ρ:A→L kills a positive power of **every** standard generator (as
the Coxeter-orbit CHL monodromy maps above do). Then ker ρ contains a nonabelian free group,
and so does its intersection with every finite-index subgroup of A. The same
holds for the induced projective map on Q whenever it is defined. Any lift of
ρ to an extension of L with abelian kernel still has infinite kernel and
cannot be a quasi-isometric embedding.

**Proof.** Choose a Coxeter edge {s,t}, so m_st≥3. If s^q_s and t^q_t lie in
ker ρ, choose multiples N_s,N_t≥2 of q_s,q_t. Crisp–Paris, Theorem 1, says
that ⟨s^{N_s},t^{N_t}⟩ is the free group F_2: the only relations between powers
of standard generators are the original commuting relations, and s,t do not
commute. This subgroup lies in ker ρ. Its intersection with a finite-index
subgroup has finite index in F_2 and is again nonabelian free.

Moreover F_2∩Z(A) is trivial, since any such intersection element lies in the
center of F_2, which is trivial. Thus this F_2 also injects into Q (including
the rank-two case). For a lift \tildeρ:A→E with E→L having abelian kernel,
the image of F_2 lies in that abelian kernel. Hence [F_2,F_2] is an infinite
subgroup of ker \tildeρ. The finite-kernel necessity in Lemma 2.1 applies. ∎

Thus an abelian central-extension repair of the same CHL quotient map cannot
give the sought geometric equivalence. This remains a statement about lifts
of that map; arbitrary nonhomomorphic quasi-isometries are not ruled out.

## 5. A central-quotient obstruction to rank-one lattice models

**Proposition 5.1 (independently audited).** If A is an
irreducible spherical Artin group of rank at least 3, then Q=A/Z(A) is not
strongly hyperbolic relative to a finite collection of proper finitely
generated subgroups.

**Proof.** For every Coxeter-diagram edge {s,t}, with label m≥3, let z_st be the
standard central generator of its rank-two Artin parabolic. The parabolic
injects in Q by Lemma 3.1 since rank(A)≥3. We check that each of ⟨s,z_st⟩ and
⟨t,z_st⟩ is Z² within this parabolic.

For m=2k even (k≥2), set y=st. The rank-two presentation becomes

    ⟨s,y | [s,y^k]=1⟩,

with z_st=y^k. Quotienting by z_st gives Z*C_k, in which s and t=s^{-1}y both
have infinite order. As z_st has nonzero exponent sum, it is infinite; a
relation s^a z_st^b=1 forces a=0 in that free product and then b=0. The same
holds with t.

For m=2k+1 odd (k≥1), set x=(st)^k s and y=st. Then the presentation is

    ⟨x,y | x²=y^m⟩,

with z_st=x²=y^m, s=y^{-k}x, and t=x^{-1}y^{k+1}. Quotienting by z_st gives
C_2*C_m. The displayed expressions for s,t are nontrivial cyclically reduced
words of free-product length two, so both have infinite order there. Again
z_st has nonzero exponent sum and independence follows.

Let U be the images in Q of all standard generators and all z_st for Coxeter
edges. It is a finite generating set consisting of infinite-order elements.
Its commutativity graph contains, for each edge {s,t}, the path s—z_st—t, with
each adjacent pair generating Z². Since the Coxeter diagram is connected,
this commutativity graph is connected. Anderson–Aramayona–Shackleton,
Theorem 2, now gives the assertion. ∎

**Scope of the conclusion.** In particular Q contains Z² and is not word
hyperbolic. It cannot itself be a cocompact lattice in a strictly negatively
curved rank-one symmetric space. Proposition 5.1 also prevents Q from being
isomorphic to a nonuniform finite-volume rank-one lattice, since those are
strongly relatively hyperbolic with finitely generated cusp groups. No
quasi-isometry-cancellation assertion for Q×R is used or established. A claim
about arbitrary quasi-isometries to truncated rank-one lattice models would
additionally require the appropriate quasi-isometry invariance theorem; we
do not need that stronger claim for the obstruction above.

Rank 2 is a necessary exclusion: dihedral central quotients are virtually
nonabelian free groups. Rank 1 gives the trivial central quotient. Reducible
groups are not covered by Proposition 5.1 as stated.

## 6. Status and remaining gap

| Mechanism | Checkable outcome | Exact remaining gap |
| --- | --- | --- |
| Delete or add reflecting hyperplanes | Infinite-kernel obstruction to the natural group map | Construct an unrelated coarse equivalence, if any |
| CHL ball quotients | Explicit finite meridian-power relations, hence infinite kernel | A lattice quotient does not identify the coarse geometry of its source |
| Direct rank-one lattice model for Q | Audited Proposition 5.1 excludes it in rank≥3 | No substitute common model produced |
| Common finite covers of reflection complements | Would establish commensurability | No such correspondence built for unresolved pairs |
| General all-type positive proof | None | Recover irreducible types/products from arbitrary quasi-isometries |

Routes that simply identify an Artin group with its CHL monodromy image are
**blocked**. Reopening requires a materially new mechanism controlling the
infinite kernel, not just a common target lattice. The same applies to the
natural arrangement-deletion map. No full quasi-isometry or certified
counterexample has been found.

## Primary sources

1. M. Cumplido and L. Paris, *Commensurability in Artin groups of spherical
   type*, Rev. Mat. Iberoam. 38 (2022), 503–526, DOI
   <https://doi.org/10.4171/RMI/1282>. Open author/publisher PDF archived under
   `sources/CumplidoParis2021.pdf`; source URL
   <https://ems.press/content/serial-article-files/38999>. Used: Theorem 2.2,
   Proposition 3.1, and §3 Garside inputs.
2. J. W. Anderson, J. Aramayona, and K. J. Shackleton, *An obstruction to the
   strong relative hyperbolicity of a group*, J. Group Theory 10 (2007),
   749–756, DOI <https://doi.org/10.1515/JGT.2007.054>. Author original
   <https://eprints.soton.ac.uk/50546/1/relhyp.pdf>, Theorem 2, archived locally.
3. W. Couwenberg, G. Heckman, and E. Looijenga, *Geometric structures on the
   complement of a projective arrangement*, Publ. Math. IHÉS 101 (2005),
   69–161, DOI <https://doi.org/10.1007/s10240-005-0032-3>. Author preprint
   <https://www.staff.science.uu.nl/~looij101/dunklrev2a.pdf>, §3.5, Theorem 7.1,
   and §8 Tables 2–4, archived locally. Preprint page numbers differ from the
   journal pagination.
4. I. Soroko, *Artin groups of types F4 and H4 are not commensurable with that
   of type D4*, Topology Appl. 300 (2021), 107770, DOI
   <https://doi.org/10.1016/j.topol.2021.107770>; primary author PDF
   <https://www.math.fsu.edu/e-prints/archive/paper575.pdf>. Used only for the
   certified noncommensurability pairs in §1.
5. J. Crisp and L. Paris, *The solution to a conjecture of Tits on the subgroup
   generated by the squares of the generators of an Artin group*, Invent.
   Math. 145 (2001), DOI <https://doi.org/10.1007/s002220100138>.
   Primary preprint <https://arxiv.org/abs/math/0003133>, Theorem 1, archived
   as `sources/CrispParis2001.pdf`.
