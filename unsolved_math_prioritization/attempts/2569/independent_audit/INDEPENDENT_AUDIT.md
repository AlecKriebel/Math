# Fresh adversarial audit: KOU-21.60 / 2569

## Verdict: PASS

The frozen candidate gives a valid counterexample to the stated positive Grothendieck-group criterion: `G = SL(2,5)`, `p = 2`. I found no missing mathematical implication and no required repair. All three projective indecomposable types over **F₂**, including the nonsplit type, satisfy the positive condition. The eight-dimensional projective cannot lift to a projective Z_(2)G-lattice because its forced characteristic-zero character contains a quaternionic irreducible once.

This is a fresh mathematical/computational audit, not specialist human verification, formal proof-assistant certification, a publication, or a priority claim. The former contributor is not counted as the final reviewer. No frozen file was edited and no remote write was made.

## Audited scope and reproducibility

The fresh audit checked the complete author package and reran all author and contributor scripts. Their result JSON files matched the reviewed outputs. The main proof, preserved unchanged in this publication, has SHA-256 `3ceab2f387baa3d61c15805cdde7d8154c8350e2b3b4bf2ce187ec53b99ec299`.

The independent verifier was written separately and imports none of the author or contributor verification code. The publication copy replaces a local source-text parser with the same explicit mathematical idempotent coefficients in `a5_idempotents.json`, and replaces local snapshot bookkeeping with the proof-integrity check above. These are input/packaging adaptations; the mathematical algorithms and assertions are unchanged. All mathematical result fields are compared with the original independent run.

## 1. Exact problem and source gate

I visually inspected the stored image of printed page 186 and independently extracted that page from the locally available October Notebook PDF. Problem 21.60 concerns finite G, the localization Z_(p), and the ordinary Grothendieck group of F_pG. Its positive condition uses reductions of **simple rational** modules and nonnegative integral combinations. It does not require a chosen rational witness to reduce isomorphically to a projective module. The proposed example addresses exactly this statement.

The matching condition is Conjecture 9 in the [Johnston–Rumynin public preprint](https://arxiv.org/html/2507.21316v2). The [October editorial update](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/) also explicitly distinguishes AI-proposed arguments from mathematically confirmed solutions. The public PDF endpoint failed in this audit's web tool; the stored PDF and page image were successfully inspected. The release does not claim that the inaccessible catalogue body was inspected.

A small fresh search found no identified earlier resolution, but this is not an exhaustive novelty determination. Retain the package's no-priority-claim and no-human-verification qualifications.

## 2. Independent group and ordinary representation constructions

I generated a quaternion subgroup using

- `a = i`;
- `b = (1 − φ i + (φ−1) j)/2`, where `φ² = φ+1`.

Both are unit quaternions. A simultaneous Cayley-graph traversal maps them to the matrices

- `A = [[0,1],[4,0]]`;
- `B = [[0,1],[4,1]]`

over F₅. It gives a bijection onto all 120 determinant-one matrices. Every one of the 14,400 products was checked to respect this bijection. Thus the computed quaternion representation is an actual representation of the stated group, not merely a class function inferred from orthogonality.

For a quaternion q, the natural SU(2) trace is twice its real coordinate. Symmetric-power characters were evaluated by the recurrence `f_(n+1)(t) = t f_n(t) − f_(n−1)(t)`. I constructed the nine ordinary representations from Sym⁰ through Sym⁵, the second real-field embeddings of the degree-two and degree-three representations, and the quotient's five-point augmentation representation.

For the last representation, I independently found the five Sylow Q₈ subgroups of SL₂(F₅). Conjugation on these five subgroups has kernel `{I,−I}` and image A₅. Its augmentation character gives exactly the candidate's χ₊. This also explicitly verifies the quotient identification.

The full nine-by-nine ordinary orthogonality check passed, the sum of squared degrees was 120, and the FS indicators in order

`1, 2a, 2b, 3a, 3b, 4+, 4−, 5, 6`

were

`1, −1, −1, 1, 1, 1, −1, 1, −1`.

In particular, Sym³ is a genuine irreducible χ₋, of degree four, with FS indicator −1. The two degree-four characters are orthogonal. These independently constructed results agree with [Chung–Kostant–Sternberg, Sections 2 and 4](https://fanchung.ucsd.edu/wp/groupb.pdf) and the [GroupNames character table](https://people.maths.bris.ac.uk/~matyd/GroupNames/97/SL(2,5).html).

## 3. All modular simple types and the nonsplit F₂ case

I separately enumerated SL₂(F₄), using F₄ = F₂[a]/(a²+a+1), and constructed its action on P¹(F₄). The resulting 60 permutations are exactly A₅. For its natural module N and Frobenius twist N^(2), the matrix spans over F₄ have dimension four. The tensor product `N ⊗ N^(2)` has matrix span dimension sixteen. Thus these representations are absolutely irreducible; the natural pair is distinguished by the traces on the two order-five classes.

There are four 2-regular conjugacy classes, so `1, N, N^(2), S` exhaust the absolutely simple modules. Frobenius interchanges N and N^(2). Restriction of scalars of N gives a four-dimensional F₂-module U whose acting algebra is all M₂(F₄): its F₂ matrix span has dimension eight. Hence U is F₂-simple with endomorphism field F₄. The five-point augmentation module S has full matrix span M₄(F₂), hence is absolutely simple. These give exactly the three F₂ simple types `1,U,S`.

The split Brauer character rows on classes `1,3,5A,5B` are

`(1,1,1,1)`, `(2,−1,φ−1,−φ)`, `(2,−1,−φ,φ−1)`, `(4,1,−1,−1)`.

They follow from lifting the eigenvalues of the explicitly constructed finite-field matrices. Inverting their 2-regular weighted Gram matrix gives the A₅ split Cartan matrix

```
4 2 2 0
2 2 1 0
2 1 2 0
0 0 0 1
```

This is an independent derivation, rather than substitution of the candidate's Cartan data.

### Additional direct idempotent check

To verify even the A₅ lifting claims used only in the supplemental filtration discussion, I parsed the three published Table 5 elements and multiplied them in Q[A₅]. All are actual idempotents and all their denominators are odd. Their reductions have left-ideal dimensions 12,16,4. Their ranks on the split simple modules identify the respective tops as `1`, the pair `N,N^(2)`, and `S`.

The ordinary characters of these actual rational projectives, at orders `1,2,3,5`, were computed as traces of `L_g R_e`, giving

- `(12,0,0,2)`;
- `(16,0,−2,1)`;
- `(4,0,1,−1)`.

Expansion in the F₂ Brauer basis produces exactly

`[P_H(1)] = 4[1]+2[U]`,
`[P_H(U)] = 4[1]+3[U]`,
`[P_H(S)] = [S]`.

This checks the credited input without using Proposition 3.3 or trusting the claimed idempotents without multiplication.

## 4. Central filtration and the positive witnesses

For `t=z−1` in F₂G, the equalities `t²=0` and `ker(t on F₂G)=tF₂G` are immediate on each pair `g,zg`. The kernel/image equality passes to direct summands of free modules. Consequently every projective P has an actual exact sequence with both outer modules isomorphic to `P/tP`.

The quotient of a projective remains projective because a split free-module decomposition survives tensoring. Nilpotence of tF₂G gives the correspondence of primitive idempotents and simple tops. One can also see indecomposability directly: the endomorphism ring of P maps onto that of P/tP, with square-zero kernel, and a quotient of a local ring is local. Hence the corresponding PIM class doubles. There is no misuse of coinvariants on an arbitrary Grothendieck equality.

As another independent control I explicitly lifted all three modular A₅ idempotents into F₂G. Given a set-theoretic lifted element a, `a²−a` lies in the central square-zero ideal, so `a²` is an idempotent. Direct left-ideal computations gave dimensions 24,32,8 and ranks of z−1 equal to 12,16,4. In particular, the eight-dimensional PIM has nontrivial central nilpotent action.

The rational degree-four witness is the augmentation representation on five points. The rational degree-five witness is the augmentation representation of the six-point action on P¹(F₅). Their complex character norms are one, so they are rationally irreducible. Their reductions are respectively S and `1+U`. Therefore the three allowed positive witnesses really are

- `4V₁ ⊕ 4V₅` for class `(8,4,0)`, dimension 24;
- `2V₁ ⊕ 6V₅` for class `(8,6,0)`, dimension 32;
- `2V₄` for class `(0,0,2)`, dimension 8.

The regular multiplicities are 1,2,4, giving `24 + 2·32 + 4·8 = 120`. Using multiplicity four for U would be wrong; the package correctly uses its F₄ endomorphism field.

## 5. Necessary projective descent and the obstruction

Let E be the eight-dimensional PIM. Its Brauer character on odd-order elements is twice χ₊. If it were the reduction of a projective Z_(2)G-lattice, its generic-fibre character Ψ would agree on these elements and vanish on every even-order element.

The vanishing argument in the package is valid. Restrict the projective lattice to the cyclic subgroup generated by g, complete, and adjoin the odd roots of unity by an unramified extension. Splitting the odd cyclic factor leaves projectives over the local group algebra of the cyclic 2-part. These are free, and a nonidentity 2-part element has regular trace zero. This is a property of projective lattices, not a claim that arbitrary positive witnesses are projective.

The forced Ψ is precisely `χ₊+χ₋` on every element. The independent finite computations give its inner product with χ₋ as one. An irreducible of FS indicator −1 must occur with even multiplicity in a complexified real representation. A rational representation would supply such a real representation, producing a contradiction.

For completeness, the implication from semiperfectness can be proved independently of the paper's extension argument. Put A=Z_(2)G. Because A is finite over the local base ring, `2A ⊂ J(A)` and `J(A)/2A = J(A/2A)`. If A were semiperfect, take a finitely generated projective cover L of the simple top S. Then L/2L is projective over F₂G and has simple top S; therefore it is the PIM E. This would be the impossible projective lattice lift. No unproved converse, extension lift, or rational-form sufficiency lemma is needed.

## 6. Global versus 2-adic Schur index

There is no conflict with the existence of an eight-dimensional projective lift over Z₂. Its character contains χ₋ once, which in fact forces the χ₋ local Schur index at 2 to be one. The global index is two.

The independent arithmetic source [Eisele–Kiefer–Van Gelder, Section 5.2](https://openaccess.city.ac.uk/id/eprint/13180/1/commens.pdf) identifies the relevant rational component as `M₂((-1,−3)/Q)`. The quaternion algebra is ramified at 3 and infinity and split at 2: for odd units −1,−3 the 2-adic Hilbert-symbol exponent is even. This matches the contributor's distinction. The degree-six Hamilton component is different and has local index two at 2. The core proof only requires the real parity obstruction and is not contingent on this classification.

## 7. The C₂ source warning and supplementary attempts

The stated C₂ control is correct. With trivial coefficients R=Z_(2), a 1-cocycle is a homomorphism C₂→(R,+), hence zero. With trivial F₂ coefficients the group of such cocycles is F₂. Thus the claimed unrestricted Ext¹ comparison is not an isomorphism. Equivalently an integral extension of two trivial rank-one lattices would have a unipotent involution; its off-diagonal entry a satisfies `2a=0`, so it splits. The corresponding modular extension can be nonzero.

The qualification in `turn_05.md` is essential and is already present: **C₂ itself is not a counterexample to semiperfectness or to the conclusion of Proposition 3.3.** Its regular integral lattice lifts the modular regular module with rational constituents trivial plus sign. The small example invalidates the selected recursive extension-lifting step, not every possible lift.

The stronger filtration discussion for SL₂(F₅) also checks out. The verified A₅ projective lifts admit filtrations obtained by intersecting saturated rational submodules with their lattices; the quotients are torsion-free over the DVR, so reduction remains exact. Doubling and splicing gives the claimed filtrations for all three G-PIMs. This supplemental observation does not enter the main counterexample proof.

The other recorded attempts were also checked: the C_p comparison correctly separates composition classes from module isomorphisms; the rational-form descent construction by dense rational bases is valid; and restriction to Q₈ supplies the parity obstruction for every odd p-group padding. The controls for the last family only implement its parity arithmetic, not an independent classification of rational modules. The written uniform argument supplies that part, as the package says.

## Repairs and release recommendation

**Required mathematical repairs: none.**

Optional exposition improvements, not release blockers:

1. The main proof could spell out the short projective-cover argument in Section 5 of this audit instead of referring generically to the standard lifting criterion.
2. Exact theorem/page locators for the standard FS-parity and projective-character facts would help a specialist reader, though the current proof gives the relevant vanishing argument and uses these facts correctly.
3. Keep all final wording at the level of an audited candidate awaiting human specialist verification. Do not relabel it an established literature solution or assert priority from bounded searches.

The frozen package can pass this fresh final audit without another author attempt. The audit report, independent verifier, and its JSON output are separate from the author and contributor material.
