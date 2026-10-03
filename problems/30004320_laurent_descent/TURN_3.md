# Author turn 3: all torus stabilizers via the full Puiseux union

Status: partial, 3/5 substantive author turns. This turn proves descent for
all torus geometric stabilizers and arbitrary smooth affine acting groups,
without a perfection or tame-splitting assumption. The unrestricted source
question remains unresolved. Standard cohomology and the credited torsor
descent theorem are explicit inputs; no novelty is claimed.

## 1. A different extension field, retaining all constant torsors

For char(k)=p>0 use compatible roots s_n=t^(1/n) for every positive integer
n, including those divisible by p, in an algebraic closure of K=k((t)). Put

    L_all=union_{n≥1} k((s_n)).                            (1)

The union is directed by divisibility. Each stage is k-isomorphic to a
Laurent-series field. For every affine k-group H, the credited
Florence–Gille torsor theorem therefore implies

    H1(k,H) → H1(L_all,H) is injective.                   (2)

For the trivial-kernel assertion, an L_all-point of a k-torsor is defined
at a finite stage. Full injectivity follows by applying the same statement
to the isomorphism torsor between two H-torsors, under an inner form of H.
This is also why the badly ramified extension from turn 2 is not silently
inserted into (1).

Unlike turn 1's field, L_all/K has purely inseparable stages. This causes
no problem here: fppf cohomology is used, and every stage is regular over
k. In particular, k is relatively algebraically closed in L_all, and
L_all is linearly disjoint from any finite separable constant extension.
These facts follow stagewise by the Laurent coefficient argument.

## 2. H1 of every constant torus is unchanged

**Proposition.** For every k-torus T,

    H1(k,T) → H1(L_all,T) is an isomorphism.               (3)

Choose a finite Galois splitting field E/k with group Delta and order d,
with no restriction on divisibility by p. Let M=X_*(T) be the cocharacter
lattice. For a Laurent variable s, split-torus Hilbert90 and Galois descent
give

    H1(k((s)),T)=H1(Delta,T(E((s)))).

Valuation and the chosen uniformizer split the coefficient module:

    T(E((s)))=T(E[[s]]) direct-sum M                      (4)

in multiplicative/additive notation, as Delta-modules. The section sends
a cocharacter lambda to lambda(s). Further,

    H1(Delta,T(E[[s]]))=H1(k[[s]],T)=H1(k,T).              (5)

For the first equality, T is split over E[[s]], whose Picard group is zero,
so torsors there are trivial and descent applies. For the second equality,
a constant torsor lifts any residue-field torsor. Two T-torsors over
k[[s]] with isomorphic special fibers have a smooth affine isomorphism
torsor with a residue point; formal smoothness lifts it successively modulo
s^m, and completeness supplies a k[[s]]-point. This proves injectivity too.
The argument works when p divides d; averaging by 1/d is not being used.

Combining (4)–(5), naturally with respect to constant coefficients and a
specified uniformizer,

    H1(k((s)),T)=H1(k,T) direct-sum H1(Delta,M).            (6)

Under s=u^e the first summand stays fixed and the second is multiplied
by e, because lambda(s)=e lambda(u). The finite-group cohomology
H1(Delta,M) is annihilated by d. Hence every class at a stage of (1)
becomes constant after a further stage of ramification degree d.
A torsor and an isomorphism over a directed union of fields descend to
some finite stage, since all schemes and maps here have finite presentation.
Taking the direct limit proves surjectivity in (3); (2) proves injectivity.

This replaces the preliminary prime-to-p averaging idea by smooth torsor
lifting. It therefore includes wildly split tori, not just tame ones.

## 3. H2 injectivity for every group of multiplicative type

The following lemma will also be useful beyond tori. All cohomology in
this section is fppf.

**Lemma.** For any finite-type k-group D of multiplicative type,

    H2(k,D) → H2(L_all,D) is injective.                    (7)

Choose a finite Galois extension splitting D and a surjection from a
finitely generated permutation lattice onto its character module. The
kernel is a free abelian group of finite rank. Contravariant character
duality gives an exact sequence

    1→D→Q→S→1,                                          (8)

where Q is a quasitrivial torus and S is a torus. This construction works
also when D is finite and non-smooth, for example mu_p: its character
module may have torsion, but the kernel of the permutation-lattice
surjection is still free.

The groups H1(k,Q) and H1(L_all,Q) vanish by Hilbert90 and Weil restriction.
Also H2(k,Q) is a finite product of Brauer groups Br(E_i) for finite
separable constant extensions E_i/k. Its restriction to H2(L_all,Q) is
injective. Indeed a central simple algebra over E_i that splits over
E_i L_all already splits over one E_i((s_n)); its proper Severi–Brauer
variety then has an E_i[[s_n]]-point by the valuative criterion, and hence
an E_i-point. This is the standard elementary Brauer specialization argument.

If alpha in H2(k,D) restricts to zero, its image in H2(k,Q) is therefore
zero. By the long exact sequence of (8), alpha is the connecting image
of beta in H1(k,S). Since H1(L_all,Q)=0, vanishing of alpha over L_all
forces beta to vanish there. Injectivity (2) for S forces beta=0 over k.
Thus alpha=0, proving (7).

## 4. Full gerbe objects for torus bands descend

For a gerbe with commutative automorphisms, the local automorphism groups
descend canonically to an abelian band: the identification induced by an
isomorphism is independent of its choice, because conjugation is trivial.
For the quotient gerbe C=[X/G] of a smooth homogeneous variety with torus
geometric stabilizer, this band is a k-torus T. No k-point of X is presumed.
The standard abelian-gerbe description identifies its class with
alpha in H2(k,T); alpha=0 exactly when C has a k-object. Once one object
eta is fixed, all other objects up to isomorphism are obtained by twisting
eta by T-torsors, that is by H1(k,T). These are standard gerbe facts, not
new cohomological definitions; see the source note below.

If C has a K-point, its class vanishes over K and hence over L_all.
By (7) it is neutral over k. Choose a k-object eta. For a prescribed
K-object xi, the difference between eta_L_all and xi_L_all is a
T_L_all-torsor. By (3) it comes from a T-torsor over k. Twisting eta by
that torsor, with the appropriate orientation, gives an object eta' with

    eta'_L_all isomorphic to xi_L_all.                    (9)

The orientation can be specified by requiring that the twist's Isom torsor
with eta is the chosen difference torsor; either convention gives (9).

## 5. Homogeneous-space conclusion, including orbit control

**Theorem.** Let G be a smooth affine group over an arbitrary field k of
positive characteristic, and let X be a smooth homogeneous G-variety with
torus geometric stabilizer. Then X(K) nonempty implies X(k) nonempty.
In fact, for every x in X(K), there are x_0 in X(k) and g in G(L_all)
such that x and x_0 lie in the same G(L_all)-orbit.

The point x defines xi in [X/G](K) whose underlying G-torsor is trivial.
Choose eta' from (9), and let E→X be its underlying G-torsor and equivariant
map. The isomorphism (9) makes E trivial over L_all. By (2), E has a
k-point e. Its image x_0 is in X(k). After extension to L_all, the
isomorphism with the trivial torsor sends e to an element of G(L_all),
which gives the asserted orbit relation. No orbit equality over K or k
is asserted.

The characteristic-zero case was already covered by the credited perfect-
field theorem. Thus the substantive new scope of this argument is the
imperfect-field torus-stabilizer class, with all predecessor inputs credited.

## 6. What this does not prove

The injectivity (7) is also available for infinitesimal multiplicative-type
bands, but (3) was proved only for tori. For example, if a is not a p-th
power in k, the mu_p-torsor represented by 1+a t over L_all does not in
general come from k. To see this, suppose (1+a t)/c=b^p with c in k^*
and b in a finite stage k((s)), t=s^n. Coefficient comparison forces both
1/c and a/c to be p-th powers in k (and if p does not divide n, the term
at exponent n already obstructs a p-th power). The ratio would make a a
p-th power, a contradiction. Thus (7) alone is insufficient for full object
descent, and no statement about all multiplicative-type stabilizers follows
merely by reusing (9).

Likewise the Artin–Schreier class z^p−z=t^(−1) remains nonconstant after
adjoining all roots of t. In k((s)) write n=p^e m with p not dividing m.
Modulo Artin–Schreier differences, s^(−n) reduces to s^(−m), whose pole
order is not divisible by p, so it cannot differ from a constant by an
Artin–Schreier difference. This is still an auxiliary object-descent
obstruction, not a counterexample to the original homogeneous question.

A next mechanism must use a stabilizer's embedding in the ambient group,
rather than claim full object descent for arbitrary wild bands.

## Sources for standard inputs

- Florence–Gille, arXiv:1910.14509v3, Proposition5.2(3)/Theorem5.4:
  constant affine-group torsor descent, already bound in SOURCE_MANIFEST.
- Florence's primary compactification paper, especially §§3–4: the
  homogeneous-space gerbe/cohomology framework. Its perfect-field theorem
  is not invoked to infer an imperfect-field result.
- Stacks Project, Section8.11, https://stacks.math.columbia.edu/tag/06NY
  (canonical abelian automorphism sheaf), and Section21.11,
  https://stacks.math.columbia.edu/tag/0CJZ (second cohomology and gerbes).
- Brosnan–Reichstein–Vistoli, §4, explanation of twisting and the difference
  of objects of a commutative-band gerbe, with its cited Giraud references.

The cohomological decomposition, character-module resolution and application
are proved above rather than inferred from the source report's short summary.
