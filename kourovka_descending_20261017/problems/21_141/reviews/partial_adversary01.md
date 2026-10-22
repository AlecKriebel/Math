# Fresh adversarial review of the partial results for Kourovka 21.141

Checkpoint: **2026-10-17 21:21 UTC**. Review completion estimate: **100% for
the claims and computations enumerated here**. Best-guess progress toward the
unrestricted discovery goal remains **10%**: this is a judgment of the current
partial package, not a fractional proof. No originality certification, complete
solution, outside communication, Git operation, queue update, or release was
performed by this reviewer.

Reviewed: `approach_homology.md`, `approach_tree.md`, `tree_rank2_review.md`,
and `counterexample_raag/FIBER_OBSTRUCTION.md`. The review attempted to falsify
the proofs, rather than treating either earlier verification or the target
conclusion as evidence. It used the local primary-source texts and reopened
the primary publications for the exact cited theorem scopes.

## Verdict

**No fatal gap was found in the stated partial conclusions under the explicit
proper pro-p amalgam convention.** In particular, the elementary normal-kernel
arguments, the elementwise-commensurated edge result, the finite-edge-orbit
criterion, the abelian-fiber obstruction, and the rank-two path diagnostic
with its faithful modification withstand this review.

The unrestricted coherence assertion remains unproved. None of the checked
arguments establishes a finite decomposition, or the required finite homology,
for every finitely generated subgroup with an infinite profinite orbit space.
The varying rank-two family does not establish inaccessibility of a fixed group.

Two presentation/provenance improvements are advisable and do not change a
mathematical conclusion:

1. State Lemma 6 with **profinite A** explicitly. The surrounding pro-p
   conventions already impose that interpretation; the proof uses an open
   subgroup inside a neighborhood, so the isolated phrase “compact group”
   should not suggest a theorem about arbitrary compact topological groups.
2. The last line of `FIBER_OBSTRUCTION.md` refers to `sources/manifest.json`.
   The actual source inventory at review time contains
   `sources/download_manifest.json`; the referenced name should be corrected
   or the promised manifest supplied.

## 1. Extension, quotient, and normal-kernel closure

The finite-presentation extension proof is valid in the pro-p category.
Every element of a finitely generated pro-p group is represented by a free
pro-p word, so choosing the words for conjugates and lifted quotient relators
does not require finite abstract-word representations. The subgroup generated
by the kernel generators in the presented group is closed by definition.
Imposing both conjugation directions makes every quotient generator normalize
it. The normalizer is closed, hence all of the presented group normalizes it.

There are two separate kernel checks, both present and necessary. The
restriction of the natural map to the kernel presentation composes to the
given embedding into the original extension; this identifies the kernel copy
without assuming the presentation is proper. The quotient presentation is
exactly the chosen presentation of Q, so every remaining kernel element lies
in that already identified copy. This proves injectivity of the full map.
Finite kernels and torsion cause no exception.

Root caught a nonessential false explanatory sentence in the earlier draft:
for a **closed** subgroup of a profinite group, a one-sided inclusion of a
conjugate already forces equality. A finite quotient separating an element
from the smaller closed subgroup would otherwise contain conjugate finite
subgroups in a strict inclusion, contradicting their equal orders. I checked
the corrected text after Lemma 1. Both conjugation directions remain valid
redundant relators; they are sufficient but are not necessary for normality.

For the quotient-coherence lemma, the full preimage of a finitely generated
closed subgroup of A/N is finitely generated: append generators of N to
lifts of quotient generators. Its compact image in the quotient is closed.
Adding the finitely many kernel generators as relators kills exactly N,
because they generate N as a closed subgroup and N is normal. This does not
assert arbitrary quotient closure of coherence.

Intersections with a finite closed subnormal procyclic series give a series
whose factors are closed subgroups of procyclic groups. Thus every closed
subgroup of a polyprocyclic kernel is finitely generated and finitely presented.
The extension argument consequently proves the strongest useful kernel rule:

> If every closed subgroup of N is finitely generated and finitely presented,
> N is normal in E, and E/N is coherent, then E is coherent.

Its use for an edge normal in both vertices is correct. Properness ensures
that the common edge and the proposed normal subgroup really are embedded
subgroups of G. Quotienting by a subgroup C normal in both vertices preserves
properness: the quotient vertex embeddings have kernel exactly C. The
malnormal-quotient conclusion is therefore valid with the stated analytic
hypothesis on H/C. No claim that an arbitrary edge admits such a C is proved.

## 2. Commensuration and the common open normal kernel

The Baire argument was checked at its potentially fragile transitions.
Finite generation of H supplies a countable list of its open subgroups.
The sets F_n are closed. Elementwise commensuration ensures that each a
belongs to one of them, so Baire supplies a coset a_0 V inside one F_n.
The resulting intersection N_0 contains K_n and lies in H^(a_0).
Since K_n is open in H and H is commensurable with H^(a_0), K_n is also
open in H^(a_0). Hence N_0 is commensurable with H.

The open subgroup V normalizes N_0, so N_0 has only finitely many conjugates
under the ambient profinite group. Every conjugate remains commensurable
with H, using actual elementwise commensuration. Their intersection N is
normal and commensurable with H. Since N lies in H^(a_0), normality gives
N=N^(a_0^-1) <= H. Thus N is open in H, as required. No unproved uniform
intersection-index bound enters the argument.

The subsequent common-kernel step is especially important and is sound.
Separate the closed subset H outside C_1 intersect C_2 from the identity in
the ambient proper amalgam, obtaining an open normal U with
U intersect H <= C_1 intersect C_2. Then, for both i,

```
U intersect H = U intersect C_i.
```

Each right-hand side is normal in G_i. Consequently U intersect H is normal
in G and open in H. Intersecting the two vertex cores alone would not give
this conclusion; the ambient open-normal cut supplies the missing invariance.

The finite-edge reduction also checks. An open normal subgroup disjoint from
the finite edge has a finite quotient graph with trivial edge stabilizers.
The vertex factors are closed subgroups of coherent vertices. Coherence of
their finite free pro-p product, followed by finite-extension closure, gives
coherence of the original amalgam. Finite generation of the original
vertices or of the entire amalgam is not needed for that argument.

The primary publication explicitly defines its profinite commensurator by
closing the actual commensurating set; Proposition 3.2 uses a finite list of
actual commensurating generators. The local proofs retain this distinction.
The dense-proper-commensurator example in `approach_tree.md` is consistent:
finite-support elements centralize an open subgroup of H, whereas the
coordinatewise shift moves every nontrivial coordinate support away from H.
Its ambient product is not finitely generated. These facts prevent an
unsupported substitution of the closed commensurator into the Baire proof.
[Berdugo–Zalesskii, Definition 3.1 and Proposition 3.2](https://link.springer.com/article/10.1007/s40863-025-00523-1).

## 3. Finite-orbit homology and the abelian-fiber obstruction

For a finitely generated subgroup L with finitely many edge orbits, there
are also finitely many vertex orbits: each vertex of each standard-tree type
is an endpoint of an edge. Each orbit is compact, and a finite partition into
compact orbits is a partition into clopen sets. Thus the compact permutation
modules really are finite sums of induced compact modules.

The displayed Tor sequence has the correct order. Continuous Shapiro
identifies the individual finite-sum terms with stabilizer homology.
There is no assumption of finite generation of a vertex stabilizer before
it is established: finite edge H_1 and finite H_1(L) force finite vertex
H_1 by exactness. Coherence then gives finite vertex H_2, which together
with finite edge H_1 forces finite H_2(L). For finitely generated pro-p L
this is precisely the finite-presentation criterion. The dual cohomological
argument in the fiber note gives the same dimension inequalities.

These are compact-module homology statements and discrete-coefficient
cohomology statements in their respective standard categories. They do not
replace a completed module by an algebraic direct sum over infinitely many
orbits. Wilkes' absolute Shapiro lemma is Proposition 1.21; his proper-amalgam
Mayer–Vietoris theorem allows empty relative families and also states the
homological version. These scopes match the uses here.
[Wilkes, Proposition 1.21 and Theorem 4.6](https://arxiv.org/html/1710.00730v1).

The fiber theorem requires only that every closed subgroup of H be finitely
generated, not finitely presented. Its zero-character part checks as follows.

* If both vertex images in Z_p are nonzero, their free pro-p product is a
  free pro-p group of rank two mapping onto Z_p. The fiber maps onto its
  kernel. The Schreier ranks 1+p^n of the inverse images of p^n Z_p are
  incompatible with a finitely generated kernel, because such a kernel
  plus one lift would give a uniform generator bound.
* If exactly one vertex image is zero, properness of H in that vertex
  supplies an index-p quotient killing H: separate H in a finite p-group
  quotient and put its image in a maximal subgroup. No finite generation
  of that vertex is required. The resulting C_p free-product Z_p quotient
  maps onto F_p[[Z_p]] semidirect Z_p. Translates of the unit basis vector
  span every finite module quotient, so the map is onto. Its fiber maps
  onto the additive module F_p[[Z_p]], whose elementary abelian quotients
  have dimensions p^n. Hence the original fiber cannot be finitely generated.
* If an edge inclusion is onto, the amalgam is the other coherent vertex;
  this handles the degeneracy instead of invoking the zero-character claim
  where it would fail.

For a finitely generated abelian quotient Q, a nonopen closed edge image S
has smaller Z_p-rank, so Q/S maps onto Z_p. The inverse image of the kernel
of that character is finitely generated if the original fiber is, because
closed subgroups of finitely generated abelian pro-p groups are finitely
generated. This contradicts the zero-character case. Therefore S is open,
and the finite-orbit argument applies. Finite torsion in Q creates no
exception. This rules out **all finitely generated abelian-quotient fibers**
as non-finitely-presented witnesses under the stated hypotheses. It makes
no assertion about arbitrary finitely generated nonnormal subgroups.

## 4. Tree lemmas, properness, and the rank-two family

The finite-graph presentation lemma uses edge generators correctly:
equality of continuous homomorphisms on a finite topological generating
set implies equality on the whole compact edge group. The vertex-generation
lemma also checks. Its constructed subgroup W normally generates V; if W
were proper, a finite p-group quotient would give a proper maximal subgroup,
whose index-p normal preimage contradicts that normal generation.

The action-kernel lifting lemma does not require a splitting of the extension.
Full preimages of edge groups contain the entire kernel, so all kernel
copies are identified along the maximal tree. Remaining edge relations
specify conjugation on the kernel by the chosen stable-letter lifts. This
makes the kernel copy normal and identifies the quotient presentation with
Q. The map to K then proves injectivity on the kernel, quotient, and whole
group. The preimage vertices remain embedded in the original stabilizers.

The procyclic affirmative case uses exactly the current Theorem 6.8 after
removing the finitely generated action kernel. The source imposes faithful
actions as a standing convention and supplies finite graphs with groups
conjugate into the relevant stabilizers. These hypotheses are respected.
[Chatzidakis–Zalesskii, v2, §2.2 and Theorem 6.8](https://arxiv.org/html/2007.06867v2).

For the path construction, the compatible maps A_i -> Z_p^2 have matrices
diag(p^i,p^(n-i)). They are injective, proving properness before any use of
a standard tree. Eliminating generators gives the displayed two-generator
presentation and its abelianization Z_p^2. The intersection of the vertex
coordinate lattices is p^n Z_p by p^n Z_p. Injectivity on A_0 then proves
that the common vertex intersection equals C, rather than merely mapping
onto its coordinate image. Centrality proves that C is exactly the action
kernel. The finite quotient vertex and edge orders have logarithms n and
n-1, so both boundary indices remain p, including the n=1 trivial-edge case.

The faithful modification is sound. The embedding of A_0 free-product Z_p
uses the finite connected-subgraph embedding theorem, applied to the enlarged
proper graph. Its action kernel lies in P_n and a distinct free-factor
conjugate. Those two vertices have an explicit finite two-edge path with
trivial edge stabilizers, which makes their intersection trivial. No finite
path between arbitrary vertices of a pro-p tree is assumed.
The cited finite-subgraph lemma and collapse are precisely Lemma 2.15 and
Remark 2.19; Corollary 3.14 has the stated analytic/malnormal scope.
[Castellano–Zalesskii](https://ems.press/content/serial-article-files/48579?nt=1).

The H^1 restriction matrix has row coordinates
(-alpha_(i+1), beta_i) modulo p, so it is onto in every characteristic.
Both H^2 restrictions are zero, since their exterior-square determinants
are p. Continuous Mayer–Vietoris consequently gives dim H^2(P_n)=n+1.
This checks also at p=2: continuous cohomology of Z_2^2 is exterior, with
degree-one squares zero. The same H^2 dimension persists after freely
adjoining the additional generator.

The independently written exact-arithmetic script
`reviews/partial_adversary01_checks.py` reproduced the H^1 ranks and the
coordinate/quotient formulas for **96 cases**, p in {2,3,5,7} and 1<=n<=24.
Every assertion passed. These finite checks supplement the preceding
uniform algebraic proof; they do not independently prove the group-theoretic
Mayer–Vietoris theorem or any assertion about infinite profinite orbit spaces.

## 5. Strongest verified conclusions and the exact remaining gap

The package supports all of the following partial conclusions, without a
novelty claim:

1. Coherence for the stated normal-polyprocyclic-kernel cases, including
   normal edges, finite edges, elementwise-commensurated polyprocyclic edges,
   and analytic malnormal quotient edges after removing a common normal
   polyprocyclic subgroup.
2. Finite presentation of a finitely generated subgroup whose restricted
   standard-tree action has finitely many edge orbits and finitely generated
   edge stabilizers.
3. Finite presentation of every finitely generated kernel of an epimorphism
   onto a finitely generated abelian pro-p group, under coherent vertices
   and the weaker edge-subgroup finite-generation assumption.
4. A faithful, reduced family with fixed edge type Z_p^2, uniformly bounded
   vertex generator number three, d(Q_n)=3, and unbounded finite graph size.

The last item excludes a universal bound depending only on those generator
numbers and the fixed edge isomorphism type. It involves varying ambient
groups, each finitely presented and freely decomposable after the faithful
modification. It supplies neither an infinite refining sequence for one fixed
group nor a finitely generated infinitely related subgroup of one fixed
amalgam. No acylindricity hypothesis has been checked for this family.

For a general finitely generated L in the target amalgam, the orbit spaces
can be infinite profinite spaces. Individual edge stabilizers being finitely
generated does not give finite-dimensional completed family homology, and
vertex coherence cannot be applied until finite generation of the relevant
vertex stabilizers is established. No proof controls both of these issues
or provides another finite-presentation mechanism for every L. That is the
exact all-subgroup gap. A proposed “finite core” or rank induction that merely
assumes the missing control remains blocked, as the research policy requires.

## 6. Follow-up audit: relation ranks, inverse limit, and free indecomposability

Checkpoint: **2026-10-17 21:23 UTC**. Follow-up review completion estimate:
**100% for these three added claims**. Overall discovery estimate remains
**10%**. No complete answer or originality claim is being promoted.

The new homological calculation in `approach_homology.md` is the dual of
the previously checked cohomological calculation. Its H_1 edge-to-vertex
map is injective: for each i, the u_i coordinate survives only as a nonzero
multiple of a_(i+1), and v_i only as a nonzero multiple of b_i. These are
2n different vertex coordinates. The H_2 edge-to-vertex map is zero because
each boundary map on the exterior square has determinant p=0 in F_p.
The relevant exact sequence therefore has the form

```
k^n --0--> k^(n+1) --> H_2(P_n,k) --> k^(2n) --injective--> k^(2n+2).
```

It identifies H_2(P_n,k) with k^(n+1), with neither an omitted extra summand
nor a quotient ambiguity. Together with d(P_n)=2 this proves minimal
pro-p relation rank n+1. The lack of a uniform bound concerns a varying
finite graph and varying ambient groups; it does not concern the relation
rank of subgroups of one fixed amalgam. The finite computation already
recorded above checks this matrix and its transpose at p=2 as well.

The inverse-system claim is also correct with the specified generator-fixing
bonding maps. Write F=F_pro-p(x,y) and let N_n be the **closed normal**
relator subgroup for P_n. Given n>=m and 0<=i<=n, the stated interval
for j is nonempty: its lower endpoint is at most m and at most i, since
m<=n. It ensures i>=j and n-i>=m-j. Thus the n-th relator is a commutator
of powers of two commuting elements in P_m. This proves N_n<=N_m and gives
compatible continuous epimorphisms P_n -> P_m; it is not a choice of
unrelated epimorphisms between abstractly isomorphic presentations.

The filtration bound has the right direction and indices. In the mod-p
Magnus algebra, x^(p^i)-1 has degree p^i and y^(p^(n-i))-1 has degree
p^(n-i). The commutator has degree at least their sum. A Zassenhaus term
is closed and normal, so it contains the whole closed normal relator
subgroup, not just the displayed relators. The minimum of the sums is
p^floor(n/2)+p^ceil(n/2), which tends to infinity for every fixed prime.
Separatedness therefore gives intersection_n N_n=1.

There is a simpler independent proof of this separation, avoiding any
Magnus input. For every open normal subgroup U of F, the finite p-group
F/U has exponent dividing p^e for some finite e. If n>=2e-1, then for
every i between 0 and n at least one of i or n-i is at least e. One of
the two commutator entries is therefore trivial in F/U. All defining
relators die, giving N_n<=U. Thus (N_n) is eventually contained in every
open normal subgroup of F, and its intersection is trivial. This also
shows that the convergence is topological, rather than only a formal
intersection calculation.

Finally F maps **onto** the inverse limit: for a compatible sequence of
cosets, its inverse images in F are nonempty nested compact sets. Every
finite subfamily is realized in its largest-index quotient, so their
intersection is nonempty. The map is injective by the intersection claim,
and is a topological isomorphism by compactness and the Hausdorff property.
Consequently this particular inverse limit is free pro-p of rank two.
Unbounded relation ranks of the finite-stage groups do not furnish an
infinitely related limit group. No assertion that arbitrary inverse systems
have this behavior has been made.

The expanded exact-arithmetic script checked all **343,400** interval
choices 1<=m<=n<=100, 0<=i<=n, the balanced minimum formula in the earlier
96 prime/length cases, and the finite-exponent threshold for 1<=e<=64.
All assertions passed. These finite checks are supplementary to the uniform
inequalities above.

For R_n=P_n/C, the added conclusion of **free indecomposability for n>=2**
is correct. Here is a proof requiring only the finite p-group fixed-point
theorem already cited in `approach_tree.md`, with no uniqueness assertion
about fixed vertices on an arbitrary infinite pro-p geodesic. Suppose
R_n=U free-product V with both factors nontrivial. Since d(R_n)=2 and
generator numbers add in a free pro-p product, both factors have generator
number one and hence are procyclic. But R_n contains the embedded finite
vertex group

```
A_1/C = C_(p^(n-1)) x C_p.
```

For n>=2 this is nonprocyclic. On the standard tree of the free splitting
it fixes a vertex by the finite p-group fixed-point theorem, putting it
inside a conjugate of a procyclic factor, a contradiction. The n>=2 bound
is necessary: R_1=C_p free-product C_p is freely decomposable.

The original adjacent-fixed-vertex proof uses the additional familiar fact
that a nontrivial finite subgroup has at most one fixed vertex in the
standard tree of a free pro-p product. It should either cite that fact
explicitly or use the preceding rank-two proof; the conclusion needs no
stronger fixed-subtree assertion.

R_n retains faithful reduced actions, d=2, bounded vertex and edge generator
numbers two, and unbounded finite graph size. Its finite edge isomorphism
types/orders vary with n. The different family Q_n retains the fixed edge
isomorphism type Z_p^2 and d=3, and is freely decomposable. These two sets
of advantages must not be combined into an unproved family having both
fixed edge type and free indecomposability. Neither family supplies a fixed
inaccessible group or answers the original coherence question.
