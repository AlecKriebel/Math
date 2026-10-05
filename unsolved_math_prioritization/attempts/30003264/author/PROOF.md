# Two different kernels in the S-arithmetic third-homology question

Problem 30003264 / OWR-15173-001, rank 733. Research date: 2026-10-05.

## Disposition

The imported formulation has a substantive domain error. The original question
in Hutchinson's Oberwolfach contribution is not resolved here. The results below
are a statement correction, a credited known small-S case, two reductions, and
an exact explanation of why a tempting passage to the field limit does not solve
the question. There is no novelty or priority claim.

Five substantive approaches are recorded. None proves eventual isomorphism for
the correctly stated question over every global field. In particular, disproving
the malformed formulation is not a counterexample to the original question.

## 1. Governing statement and notation

Put R = Z[1/2]. For a global field F and a finite set S of places containing the
archimedean places S_infinity, write O_S for its S-integers. The primary discussion
also assumes at least two places, at least one nonarchimedean. Write

    A_S = H_3(SL_2(O_S), R),       A_F = H_3(SL_2(F), R),
    j_S: A_S -> A_F,              k_F: A_F -> K_3^ind(F)[1/2],
    N_S = ker(k_F j_S),           L_S = ker(j_S),
    N_F = ker(k_F),               B_S = direct sum_{v in S finite} P(k(v))[1/2].

The primary question asks whether the natural specialization map

    pi_S: N_S -> B_S

is an isomorphism for every sufficiently large finite S. Here sufficiently large
means containment of a fixed finite S_0 (depending on F), not merely one example
of S or an unbounded sequence of choices. The primary states surjectivity for
sufficiently large S. The proof below does not replace that assertion with a new
uniform surjectivity proof.

The source is [OWR], printed pp. 2958-2959, especially the explicit definition
of the subscript-zero kernel on p. 2959. Localizing at 2 is flat, so this agrees
with tensoring the integral kernel in the source with R.

The imported display instead uses L_S in place of N_S. This is not a harmless
change of notation. The natural map under discussion is obtained from field
specializations after j_S; its restriction to L_S is zero.

For q >= 4 the convention for P(F_q) used here is the free abelian group on
[x], x in F_q minus {0,1}, modulo

    [x]-[y]+[y/x]-[(1-x^{-1})/(1-y^{-1})]+[(1-x)/(1-y)] = 0

for distinct x,y outside {0,1}. Only its half-integral version matters. The
known order of P(F_q)[1/2] is the odd part of q+1 [Refined, Corollary 2.7].
The small-field convention is P(F_2) = Z/3; it is explicitly included in
[Rings]. No integral order claim for every q is inferred from the abbreviated
sentence in [OWR].

## Approach 1. The wrong-kernel obstruction, with an explicit residue calculation

### Proposition 1

The restriction to L_S of the primary specialization construction is zero.
For F=Q this restriction cannot be an isomorphism for any S containing the
place 5. Consequently it cannot be an isomorphism for all sufficiently large S.

### Proof

Every component has the form s_v j_S on N_S, where s_v is the appropriate
field-homology specialization. If x belongs to L_S, then j_S(x)=0, hence
s_v j_S(x)=0 for every v. Thus the restriction is the zero homomorphism.

It remains to prove the target is nonzero without relying on an unexplained
finite-field computation. In P(F_5) use generators a=[2], b=[3], c=[4]. The six
ordered pairs (x,y) yield the following relation vectors in that basis:

    (0,0,1), (3,0,-2), (0,0,1), (-1,2,0), (-1,2,0), (1,-2,2).

These relations are equivalent to c=0, a=2b, 6b=0. To check equality rather
than just a quotient, sending (a,b,c) to (2,1,0) in Z/6 annihilates every listed
relation. It is surjective and inverse to the map sending 1 to b. Thus
P(F_5)=Z/6 and P(F_5)[1/2]=Z/3. If 5 belongs to S, this is a nonzero summand
of B_S, so a zero homomorphism cannot be onto. Given any proposed S_0, enlarge
it by {infinity,5}; this disproves the eventual assertion for the restriction
with the erroneous domain. QED.

This conclusion concerns the recognizable specialization construction. Merely
writing an unspecified different map from L_S does not define that construction.
No assertion about arbitrary homomorphisms out of L_S is needed.

## Approach 2. A fully accounted known positive case

### Proposition 2 (known case, credited)

For F=Q and S={infinity,2}, the correctly defined pi_S is an isomorphism
N_S -> P(F_2)[1/2] = Z/3.

### Inputs from the literature

[Adem-Naffah, p. 8] computes the integral cohomology of SL_2(Z[1/2]); in
particular its fourth cohomology is Z/24 plus Z/3. The corresponding third
homology computation is explicitly recorded as

    H_3(SL_2(Z[1/2]), Z) = Z/8 plus Z/3 plus Z/3

in [Rings, Proposition 8.22]. We use that established homology computation.
The integral homology computation is not reproduced from a full resolution here.

[Rings, Lemma 8.24 and Proposition 8.25] identifies the odd part with a module
having generators D and <2>D of order 3. The map to K_3^ind(Q)[1/2]=Z/3
sends both to the same nonzero class. The residue map sends D to a generator
d of P(F_2)=Z/3, while <2> acts as -1 on the residue group. These particular
map identifications, rather than group orders alone, are important.

### Proof from these inputs

After tensoring with R, identify A_S with F_3^2 in the basis (D,<2>D).
Up to choices of nonzero generators its map to K_3^ind(Q)[1/2] is
(x,y) -> x+y, and its residue map is (x,y) -> x-y. Therefore N_S is the line
{(t,-t): t in F_3}, and its residue map is t -> 2t, an automorphism of F_3.
This proves the stated isomorphism. It also shows L_S=0: the pair of maps to
K_3^ind and the residue group is injective, and both factor through j_S. QED.

This is a known special case, not eventual isomorphism. Enlarging S can create
new kernel classes. Proposition 4 below makes the logical issue precise.

## Approach 3. Reduce the rational-field problem to localization injectivity

### Literature inputs and normalization

[Rational, Theorem 4.3] gives an isomorphism

    s: N_Q -> direct sum_p P(F_p)[1/2]

whose p-component is the valuation-character specialization s_p. A prime p
acts by -1 on its own summand and +1 on the others; -1 acts trivially.

[DVR, Theorem 2.1 and Section 2.7] gives an exact sequence

    H_3(SL_2(Z_(p)),R) -> A_Q --Delta_p--> RP_1(F_p)[1/2] -> 0

when p>=11. For a finite residue field, RP_1(F_p)[1/2] is P(F_p)[1/2].
There is no initial 0 in this sequence; injectivity of the first arrow is not
one of its conclusions.

For clarity, Delta_p and s_p have different normalizations. In the induced
residue module write an element as a + <p>b. The maps called rho_0 and rho_p
in [DVR, Lemma 2.2] are a+b and b, whereas character evaluation <p> -> -1
is a-b. On the augmentation part the first component a+b is zero, since
the finite-field augmentation part vanishes. Thus on N_Q,

    s_p = -2 Delta_p.

All these identifications are over R. In particular the two maps have the same
zero set there. This accounts for the normalization rather than identifying
the two maps without qualification.

### Proposition 3

Let S be finite and contain infinity and {2,3,5,7}. Then

    ker(pi_S: N_S -> B_S) = L_S.

Consequently, whenever pi_S is surjective, there is a short exact sequence

    0 -> L_S -> N_S --pi_S--> B_S -> 0.

For such S, with the primary's sufficiently-large-S surjectivity understood,
the original rational-field question is equivalent to eventual injectivity of
j_S on the whole group A_S.

### Proof

If p is outside S, then p>=11 and the ring map O_S -> Q factors through
Z_(p). The DVR exact sequence therefore gives Delta_p j_S=0. For x in N_S,
j_S(x) lies in N_Q, so s_p j_S(x)=-2 Delta_p j_S(x)=0. Hence
s(j_S(N_S)) is supported only on primes in S.

Under the isomorphism s of [Rational], pi_S is the projection onto these
S-components. Since all other components are already zero, pi_S(x)=0 if and
only if s(j_S(x))=0, if and only if j_S(x)=0. This proves the kernel equality.
Surjectivity then gives the exact sequence. Finally ker(j_S) is automatically
contained in ker(k_Q j_S)=N_S, so injectivity on N_S and on A_S are equivalent.
QED.

### What is still missing

The exact sequence over a DVR does not prove j_S injective. It only identifies
the image at the field term. The field theorem plus this image information
does not settle the finite-S kernel. Likewise, newer Bloch-Wigner sequences
for rings [Rings, Refined2024, Remarks2026] do not by their statements alone
compute every such localization kernel. The number-field extensions in
[Quadratic] are field calculations with an additional unit-coinvariant
qualification for Q(i); they are not uniform finite-S theorems.

## Approach 4. The filtered-limit route and its exact quantifier boundary

### Proposition 4

For every global field F, every element of L_S becomes zero in A_T for some
finite T containing S. Any finitely generated R-submodule of L_S becomes
zero in one common such A_T. This does not imply L_T=0, even eventually.

### Proof of the positive assertions

Every matrix in SL_2(F) has only finitely many denominators, so SL_2(F) is the
filtered union of its SL_2(O_S). The bar chain group in degree n is free on
n-tuples of group elements. Each chain involves finitely many such tuples;
the bar differential involves only the group operations on those elements.
Consequently the bar chain complex of SL_2(F) is the filtered union of the
bar complexes at the finite stages.

If a cycle z at S represents an element of L_S, its image is a boundary in
the field complex. A chain b with boundary z uses finitely many matrices, all
lying in some SL_2(O_T), with T finite and containing S. The same equation
boundary(b)=z holds at T. This proves elementwise eventual killing. For
finitely many module generators, take a common finite union of their witnessing
sets T. Naturality then kills the whole generated submodule at that stage. QED.

### Countermodel to the stronger inference

This is a countermodel in R-modules, not an arithmetic counterexample. For
n>=1 set B_n=(Z/3)^n and A_n=B_n plus Z/3. Map A_n to A_(n+1) by

    (b_1,...,b_n; e) -> (b_1,...,b_n,0; 0).

Let pi_n be projection to B_n and let B_n -> B_(n+1) append zero. All squares
commute; every pi_n is onto; all modules are finite; every kernel is a nonzero
Z/3 but is killed by the very next transition. The colimit of A_n is
direct sum_{n>=1} Z/3, and the induced map to the colimit of B_n is an
isomorphism. Nevertheless no pi_n is injective.

Thus even a correctly computed field limit, finite generation at every stage,
and uniform killing of each fixed old kernel after one step do not imply the
eventual assertion. A proof must prevent new kernel classes at enlarged S.

## Approach 5. Character decomposition identifies every component to control

Restrict again to F=Q and write S_f={p_1,...,p_s}. The units of O_S are
the numbers +/- product p_i^{n_i}. Their square-class group is therefore

    G_S = (Z/2)^(s+1),

with independent generators -1,p_1,...,p_s; independence follows from the sign
and the valuations modulo 2. Conjugation by determinant units gives an action
on A_S which factors through G_S. Indeed a square determinant conjugation can
be represented, up to a scalar matrix, by an SL_2 matrix, hence acts trivially
on homology. The same action preserves N_S and L_S.

For a character chi:G_S->{+1,-1}, set

    e_chi = (1/|G_S|) sum_{g in G_S} chi(g) g  in R[G_S].

This makes sense because |G_S| is a power of 2. Put M_chi=e_chi M.

### Proposition 5

An equivariant map f:M->N of R[G_S]-modules is an isomorphism if and only
if its restriction M_chi->N_chi is an isomorphism for every character chi.

For pi_S the only possibly nonzero target components are the characters

    chi_p(u)=(-1)^{v_p(u)},   p in S_f.

At those characters the target is P(F_p)[1/2]. At every other character it
is zero. In particular, surjectivity is insufficient: every extra source
character component, as well as every kernel in a single-prime component,
must be ruled out.

### Proof

For any nontrivial character theta, choose h with theta(h)=-1. Multiplication
by h permutes the group, so sum_g theta(g)=-sum_g theta(g), which gives zero
over R. The corresponding sum is |G_S| for the trivial character. Character
orthogonality now gives e_chi e_psi=0 for chi != psi, e_chi^2=e_chi, and
sum_chi e_chi=1. These identities can also be obtained by multiplying the
commuting factors (1+chi(g_i)g_i)/2 over the generators. Thus
M=direct sum_chi M_chi and likewise for N, with no finite-generation
assumption. An equivariant f preserves these summands, which proves the
criterion. The description of the target follows from its valuation-character
action. QED.

### Adversarial example for a target-only character test

For two prime generators take B=F_3 with character (-,+), plus F_3 with
character (+,-), and take A=B plus F_3 with character (-,-). Let pi:A->B
be projection. It is an isomorphism on both target-supported characters and
is surjective, but its mixed-character kernel is F_3. This is an abstract
module control, not an arithmetic counterexample.

This character route does not establish that the unwanted components of the
actual N_S vanish. It pinpoints the missing arithmetic input. Nor may these
half-integral idempotents be used integrally: 1/2 is essential.

## Overall conclusion

The primary problem remains unresolved by this investigation, after five
distinct approaches. The imported statement needs repair from L_S to N_S.
The small case S={infinity,2} is known, with an explicit nonzero correct
kernel and zero field-localization kernel. For Q, after adjoining 2,3,5,7,
the remaining eventual-injectivity problem is precisely the finite-stage
localization kernel once the primary's eventual surjectivity is applied.
Neither the field limit nor target-supported character calculations remove it.

All displayed elementary deductions are proved above. The imported arithmetic
theorems are explicitly credited; their entire proofs and foundations have not
been independently re-proved. The exact-arithmetic program verifies the finite
relation and module controls only. This is unrefereed AI-assisted research, not
proof-assistant certification or human peer review.

## References

- [OWR] K. Hutchinson, On the low-dimensional homology of SL2 of S-integers,
  Oberwolfach Report 52/2016, pp. 2958-2959.
  https://doi.org/10.4171/OWR/2016/52
- [Refined] K. Hutchinson, A refined Bloch group and the third homology of
  SL_2 of a field. https://arxiv.org/abs/1101.3279
- [Adem-Naffah] A. Adem and N. Naffah, On the cohomology of SL(2,Z[1/p]),
  arXiv v1 (1995); published in LMS Lecture Note Series 252 (1998), pp. 1-9.
  https://arxiv.org/abs/math/9503230
- [Rational] K. Hutchinson, The third homology of SL_2(Q), arXiv v4 (2020);
  Journal of Algebra (2021). https://arxiv.org/abs/1906.11650v4
- [DVR] K. Hutchinson, B. Mirzaii and F. Y. Mokari, The homology of SL_2 of
  discrete valuation rings, inspected arXiv v2 (2020); published in Advances
  in Mathematics 402 (2022), 108313. https://arxiv.org/abs/2007.11159v2
- [Rings] R. Cuitun Coronado and K. Hutchinson, Bloch Groups of Rings,
  arXiv v3, 10 February 2026. https://arxiv.org/abs/2201.04996
- [Quadratic] R. Cuitun Coronado, Third homology of SL_2 over Number fields:
  The norm-Euclidean quadratic imaginary case, inspected arXiv v1 (2022).
  https://arxiv.org/abs/2212.07819
- [Refined2024] B. Mirzaii and E. Torres Perez, A refined scissors congruence
  group and the third homology of SL_2, arXiv v2 (2024).
  https://arxiv.org/abs/2307.08872v2
- [Remarks2026] E. Torres Perez, Remarks on refined scissors congruence group
  and the third homology of SL_2, arXiv v2, 7 September 2026.
  https://arxiv.org/abs/2608.08890v2
