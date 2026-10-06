# Geometric quotients of K-sheets: a precise partial answer

## 1. Scope and status

The 2010 Oberwolfach question asks whether symmetric-Lie-algebra K-sheets admit orbit-space geometric quotients, and how nilpotent transverse slices describe them. The surrounding discussion expressly includes gl_n and proposes gluing several slice saturations. The printed report does not explicitly specify whether the target must be separated. That distinction changes the answer.

This note establishes two different assertions:

1. **Positive type-A result, allowing nonseparated schemes.** Every K-sheet for g = gl_n, over an algebraically closed field k of characteristic zero, has a geometric quotient obtained by gluing its nilpotent p-Slodowy slices. The same conclusion holds for sl_n. The proof is an authored deduction from credited published inputs, not a claim that this deduction is new.
2. **Negative separated result.** There is a K-sheet for g = sl_2 with no orbit-separating morphism to any separated k-scheme or separated algebraic space. Its geometric quotient is the affine line with doubled origin. This example is already documented by García-Prada–Peón-Nieto and Hameister–Morrissey.

The arbitrary-type, nonregular case in the category of possibly nonseparated schemes remains outside the result proved here. It must not be marked solved on the strength of either assertion.

## 2. Conventions

Let g be a finite-dimensional reductive Lie algebra over k and let theta be an involution. Write g = kappa + p for its +1 and -1 eigenspaces. Let G be the connected adjoint group and K the connected subgroup corresponding to kappa. K acts on p through the adjoint representation. Passing to a central covering of K does not change its orbits, but its stabilizers can acquire a central kernel; all centralizer assertions below concern G, not such a covering.

A K-sheet S is an irreducible component of p^(m) = {x : dim(K.x) = m}, with its reduced locally closed structure. For a nilpotent e in S, take a normal sl_2-triple (e,h,f), so e,f lie in p and h lies in kappa. Put

    T_e = S intersect (e + p^f),       U_e = K.T_e.

The notation p^f means the centralizer of f in p. Here p is an eigenspace, not a prime characteristic. This note makes no claim in positive characteristic.

By a geometric quotient q:S -> Q we mean a K-invariant surjective morphism whose geometric fibers are single K-orbits, whose topology is the quotient topology, and whose structure sheaf is the sheaf of invariant regular functions. Our construction is universally open and is also categorical for invariant morphisms to schemes. Q is allowed to be nonseparated. We separately discuss what happens if one imposes separatedness.

The affine invariant quotient, a geometric orbit quotient, the quotient stack, and an algebraic-space quotient are different objects. A proof about one is not automatically a proof about the others.

## 3. Credited inputs

We use the following results with their stated characteristic-zero assumptions.

**Input B (Bulois, 2011).** Published Lemma 3.6 and Theorem 3.7 identify the G-orbit quotient of a G-sheet S_G through a nilpotent e with the finite component-group quotient of Q_e = S_G intersect (e + g^f). If G^e is connected, Q_e itself is a section: every G-orbit meets it in exactly one point, and the resulting map psi_e:S_G -> Q_e is a morphism restricting to the identity on Q_e. Lemma 4.1 verifies connectedness in gl_n. Lemma 13.1, Theorem 13.2 and its proof place each type-A K-sheet in a G-sheet. These are published theorem numbers; the older arXiv version uses different numbering.

**Input BH (Bulois–Hivert, 2016).** Propositions 2.4(v), 2.5(ii), and 2.8 give a finite open cover of a K-sheet by U_e and make K x T_e -> U_e smooth and surjective. The nilpotents initially furnished by their degeneration statement lie in the closure of the cone and have the same orbit dimension. For a sheet they therefore lie in the sheet itself, since an irreducible component of p^(m) is closed in p^(m). Their result establishes actual coverage, not merely density of one slice saturation. Numbering here is from the inspected arXiv v2 text corresponding to the published article.

Each sheet is stable under K and scalar multiplication: the connected group K x G_m preserves the finitely many irreducible components of p^(m). Thus the cone hypothesis in Input BH applies. There are finitely many nilpotent K-orbits, so the resulting cover can be finite.

**Input HM (Hameister–Morrissey, 2025).** Their regular-quotient theorem constructs a scheme by gluing Kostant–Rallis sections for the entire regular locus p^reg. Theorem 3.16 and Example 3.1 in inspected arXiv v3 supply respectively this gluing description and the rank-one doubled-origin example. Their notation involving multiple sheets of a cover must not be confused with arbitrary nonregular K-sheets. We use the theorem only as a credited regular-case result; the proof in Sections 4–5 below does not depend on HM.

Full bibliographic information and checked locators are in SOURCES.json.

## 4. A gluing criterion

**Theorem A.** Suppose a K-sheet S is contained in a G-sheet S_G. Assume that for every nilpotent e in S the group G^e is connected. Then S has a geometric quotient in finite-type, possibly nonseparated k-schemes. It is obtained by gluing the schemes T_e along the open loci where their points are K-conjugate.

More generally the same proof works whenever Input BH's open cover is available and each covering slice admits the section property in Input B. We do not replace that property by a dimension count.

### 4.1. The local map is a morphism

Choose finitely many representatives e_i and triples, and write T_i, U_i, Q_i, psi_i. Since e_i lies in S_G, Input B applies to that same ambient G-sheet. For x in U_i one can write x = k.t with t in T_i. G-invariance and the section property give

    psi_i(x) = psi_i(t) = t.

Thus psi_i maps U_i into T_i. Its restriction defines a morphism

    q_i:U_i -> T_i

with the inclusion s_i:T_i -> U_i as a section. Factoring through T_i is legitimate: T_i is a reduced locally closed subscheme of Q_i, U_i is reduced, and the image lies in T_i. Equivalently one first restricts to the open set containing T_i and then observes that its defining radical ideal pulls back to zero.

If two points in T_i are K-conjugate, they are G-conjugate and hence equal by Input B. Consequently every K-orbit in U_i meets T_i exactly once. This is the step for which connectedness of G^e matters. A finite G-orbit ambiguity would not suffice.

Let a_i:K x T_i -> U_i be the action map. It is smooth and surjective by Input BH, and

    q_i composed with a_i = pr_2.

This equality holds as a morphism: both sides agree after composing with the locally closed immersion into Q_i, by G-invariance of psi_i and its identity restriction.

### 4.2. Each local map is a geometric quotient

The preceding orbit statement gives the fibers, also after algebraically closed field extension. To check openness, let W be open in U_i. Then

    q_i(W) = pr_2(a_i^(-1)(W)).

The right-hand side is open because projection by a smooth algebraic group is open. The same argument survives every base change on T_i: a_i remains a smooth surjection and its composite with q_i remains the projection. Hence q_i is universally open and surjective, in particular a topological quotient.

For an open V in T_i, pullback embeds O(V) into the K-invariant functions on q_i^(-1)(V), because q_i has the section s_i. Conversely, if F is such an invariant function, let f be its restriction along s_i. On K x V, invariance gives

    a_i^* F = pr_2^* f = a_i^*(q_i^* f).

Smooth surjectivity is faithfully flat, so equality after this pullback implies F = q_i^* f. This proves the invariant-sheaf condition. The argument does not assume that S or U_i is affine.

The same reasoning proves the categorical property. For a K-invariant morphism h:U_i -> Y to any scheme, set h_i = h composed with s_i. The morphisms h and h_i composed with q_i agree after the smooth surjection a_i, by invariance. Morphisms satisfy faithfully flat descent, so they agree on U_i. Uniqueness follows from surjectivity or the section.

### 4.3. Open overlaps and the cocycle

On an overlap U_ij = U_i intersect U_j define

    T_ij = s_i^(-1)(U_j),
    phi_ij:T_ij -> T_ji,       t |-> q_j(t).

The subset T_ij is open in T_i. Every orbit in U_ij meets it exactly once, and q_i(U_ij) = T_ij. Since U_i is K-stable, the K-conjugate representative q_j(t) also belongs to U_i, so phi_ij indeed maps into T_ji. The map is a morphism, as a restriction of q_j.

The local quotient's categorical property, or pullback along the smooth action maps, gives

    phi_ji composed with phi_ij = id,
    phi_jl composed with phi_ij = phi_il

where defined. These identities say that successive choices of the unique orbit representative agree. They hold as morphisms, not just as identities between sets of complex points: on a smooth cover one writes the representatives as group translates and applies invariance of each q_i.

The schemes T_i therefore glue along these open isomorphisms to a scheme Q. Since the cover is finite and its members are finite type, Q is finite type over k. The maps U_i -> T_i -> Q agree on overlaps, giving q:S -> Q.

The preimage of the chart T_i in Q is exactly U_i. Indeed, the transition identifications identify precisely representatives of the same K-orbit, and every U_i is K-stable. Thus all local quotient properties just established apply on an open cover of Q. The fibers of q are exactly the K-orbits, q is universally open and surjective, and O_Q = (q_* O_S)^K. Invariant morphisms factor locally and their factorizations glue uniquely. This proves Theorem A.

Nothing in this argument asserts that the diagonal of Q is closed. Gluing separated charts along open sets need not yield a separated scheme.

## 5. Application to type A

**Corollary B.** For g = gl_n and any involution theta, each K-sheet S has the quotient in Theorem A. Its charts are its p-Slodowy slices.

By Input B, S is contained in a G-sheet S_G and nilpotent centralizers in the adjoint group of gl_n are connected. Input BH supplies the open cover. These verify every hypothesis of Theorem A; applying it proves the corollary.

One can independently check the centralizer assertion. The GL_n-centralizer of a nilpotent matrix is the group of units of its finite-dimensional commutant algebra. It is the principal open locus where the determinant is nonzero in that vector space, and is therefore irreducible. Its image in PGL_n is connected. This proof also explains why one must use the adjoint group: an SL_n-centralizer can have a different component group.

For g = sl_n, extend theta to gl_n by making it act trivially on the scalar center. Then p is unchanged, as are the adjoint group and the K-action on p. A K-sheet is consequently the identical subset with the identical quotient problem. A normal triple lies in sl_n, and the extra scalar direction in g^f does not enter p^f. Corollary B therefore gives exactly the asserted p-slice construction for sl_n as well.

For n = 1 the adjoint action is trivial; sheets are the eigenspaces on which that action is trivial, and the quotient is the identity. The zero nilpotent can be treated with the allowed triple (0,0,0). This degenerate case causes no exception to the construction.

This is a proof of the type-A subcase with a nonseparated target convention. It is an assembled consequence of established results, not a claim of a newly discovered resolution of the full 2010 problem.

## 6. The rank-one obstruction and explicit quotient

Work over k as above. In g = sl_2 take theta to be conjugation by diag(1,-1). Its -1 eigenspace consists of matrices

    x(a,b) = [[0,a],[b,0]].

In the adjoint group PGL_2 the connected fixed subgroup is the diagonal torus, parameterized effectively so that

    t.x(a,b) = x(ta,t^(-1)b).

Using diag(t,t^(-1)) in SL_2 instead would give weights +2 and -2; over an algebraically closed field this has exactly the same orbits. Confusing these parameterizations would give incorrect stabilizer claims.

Every nonzero vector has a one-dimensional orbit and the origin has a zero-dimensional orbit. Therefore

    S = A^2 minus {(0,0)}

is a K-sheet: it is the irreducible open set p^(1). Its orbits are the hyperbolas ab = c for c != 0 and the two punctured axes for c = 0. The two axes are distinct K-orbits. They are not closed in p, but they are closed in S; the omitted origin is their only added limit. In fact any orbit in a constant-orbit-dimension sheet is closed relative to that sheet, since boundary orbits have lower dimension. Relative closedness alone does not force a separated quotient.

### 6.1. Nonexistence of a separated geometric quotient

Consider the two morphisms

    alpha(z) = (1,z),          beta(z) = (z,1)

from A^1 into S. On G_m, beta(z) = z.alpha(z), so any K-invariant morphism q satisfies q composed with alpha = q composed with beta there. If its target is separated, the equalizer is closed in A^1. Since it contains the dense open G_m, it is all of A^1. At zero this forces

    q(1,0) = q(0,1).

An orbit-separating map cannot do that. The same diagonal argument works for a separated algebraic-space target. Hence there is no separated geometric quotient. This is a rigorous counterexample to a separated interpretation, not to all quotient conventions.

### 6.2. The nonseparated geometric quotient

Cover S by U_+ = {a != 0} and U_- = {b != 0}. Set c = ab and use sections (1,c) and (c,1), respectively. The charts are explicitly trivial:

    G_m x A^1 -> U_+,       (t,c) |-> (t,c/t),
    G_m x A^1 -> U_-,       (t,c) |-> (ct,t^(-1)).

Their inverse torus coordinates are t = a and t = b^(-1). The local quotient maps are c = ab. On U_+ intersect U_- the common parameter c is nonzero. Thus the two copies A^1_+ and A^1_- glue by c -> c on G_m, producing the affine line D with two origins.

The map q:S -> D has a single orbit in every fiber. It is a geometric quotient by either the local product description or Section 4. It is nonseparated by the two maps alpha and beta above.

For e = x(1,0), f = x(0,1), and h = diag(1,-1), the triple is normal and p^f = k.f. Therefore T_e = {(1,c)}. The opposite normal triple (f,-h,e) gives T_f = {(c,1)}. This identifies the two charts precisely as p-Slodowy slices. A single slice misses the other nilpotent orbit, so replacing the open cover by one saturation would be wrong.

For comparison, the invariant ring of the affine plane is k[ab]. The map S -> A^1 given by ab merges the two axial orbits and is not geometric. The global regular-function calculation on S gives the same ring: inside k(a,b),

    k[a,a^(-1),b] intersect k[a,b,b^(-1)] = k[a,b].

Hence taking global invariants cannot recover the two origins. This demonstrates concretely the difference between an affine invariant quotient and an orbit-space quotient.

## 7. What remains

The connected-centralizer criterion is sufficient, not necessary. For a general G-sheet the finite group A(e) = G^e/(G^e)^0 can be nontrivial. Then a G-orbit can meet Q_e in several points. The restriction of the G-quotient to a K-slice need not distinguish K-orbits, and the map q_i in Section 4 no longer exists by the same argument.

To extend this proof one must construct a genuine local K-quotient of each T_e, identify its overlap relation, and prove effective scheme gluing. It is not enough to know a finite G-orbit relation, smoothness of the sheet, constant stabilizer dimension, or existence of a quotient stack. In particular a nontrivial finite G-component-group action need not preserve the chosen p-slice or encode exactly K-conjugacy.

Another possible route is rigidification of the quotient stack. It requires appropriate flatness/smoothness of the full stabilizer group scheme and a proof that the resulting algebraic space is a scheme. Constant fiber dimension by itself is not such a proof. No unsupported extension of the regular-locus theorem is used here.

The source inspections established published regular-locus results and the elementary obstruction, not a published theorem resolving all nonregular K-sheets in all types. A targeted literature search through 2026-10-06 did not establish such a theorem. This is a bounded search conclusion, not a claim that no such result exists.

## 8. Verification boundary

The accompanying program checks exact Laurent-polynomial identities for the rank-one action, normal triple, slice parameterizations, inverse coordinates, and generic orbit witness. No finite list of examples is used as a proof of Theorem A or Corollary B. Those rely on the mathematical proof and on the named published inputs. Hash and inventory checks establish reproducibility and file identity, not theorem truth.
