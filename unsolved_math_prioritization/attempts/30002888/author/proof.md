# A conditional reduction for mixed-perverse forgetful functors

Problem 30002888; OWR-13682-010. Author investigation dated 2026-10-06.

**Status: partial, conditional, and not a solution of the general problem.**
The propositions below are elementary categorical deductions, with proofs supplied
for checking. No novelty is asserted. In particular, a conditional statement that
starts with a triangle functor does not construct that functor.

## 1. The primary question and its conventions

In Achar's contribution, joint with Riche, Question 3 occurs on printed page 1429
of [OWR]. Its setting is a complex algebraic variety with an algebraic
stratification by affine spaces and a coefficient field F. The ordinary category
is the bounded stratification-constructible category of F-sheaves. Its shift is
written `{1}`. The mixed category is `K^b(Parity_S(X,F))`, with homotopy shift
`[1]` and Tate twist `<1> = {-1}[1]`. Parity objects placed in homotopy degree
zero have weight zero; weight at most n, respectively at least n, means a
representative vanishing below -n, respectively above -n. Recollement defines
the mixed perverse heart. The requested forgetful functor should restrict to an
exact functor between hearts, kill Tate twist coherently, and identify the sum
of graded Yoneda Ext groups with ordinary Yoneda Ext in every nonnegative
degree. The report does not build essential surjectivity into its stated
definition of a grading. It already answers the question affirmatively for
finite flag varieties in the stated good-characteristic setting. [OWR, pp.
1427-1429]

The detailed construction in [AR, Sections 2-3] uses finite affine
stratifications, analytic constructibility, and constant pariversity. Its
coefficient system is `(K,O,F)`, with K a finite extension of Q_l, O its ring of
integers, and F its residue field. Assumption (A1) asks for indecomposable
parity extensions with the normalized constant restriction on each stratum;
the authors say it is automatic for K and F in their setting. Assumption (A2),
imposed later, requires mixed standards and costandards to be perverse. It
supports the highest-weight and derived-realization results; it must not be
silently imposed on the general question. Proposition 5.5 constructs the
finite-flag functor. Thus parity, a perverse t-structure, a realization
equivalence, and a forgetful functor are separate assertions. [AR]

## 2. A generator criterion for the derived Hom comparison

Here is a self-contained conditional reduction. In this section the shift on
the target triangulated category T is denoted `[1]_T`.

Let P be a full additive subcategory of an F-linear triangulated category T,
stable under `[1]_T`. Put D = K^b(P). Denote the termwise shift inherited from
P by `{1}`, the homotopy shift by `[1]`, and set `<1> = {-1}[1]`. Suppose:

1. R: D -> T is a triangle functor.
2. There is an isomorphism of triangle functors eta: R composed with `<1>` -> R.
   Its iterates define eta_n for every integer n, using inverses for negative n.
3. The restriction of R to the stalk complexes P is naturally isomorphic to
   the given inclusion P -> T, on both objects and morphisms.

**Proposition 2.1.** For any M,N in D and any integer k, the natural comparison

    direct_sum_(n in Z) Hom_D(M, N<n>[k])
        -> Hom_T(R(M), R(N)[k]_T)

is an isomorphism. R is conservative and is faithful on each ordinary Hom
space of D. Neither t-exactness nor a grading on an abelian heart is part of
this conclusion.

**Proof.** First let M=P_0 and N=P_1 be stalk complexes from P. We have

    N<n>[k] = P_1{-n}[n+k].

A morphism from a stalk complex in homotopy degree zero to a stalk complex in
a different homotopy degree is zero in K^b(P). Consequently only n=-k can
contribute. The surviving group is

    Hom_P(P_0, P_1{k}).

Because P is full in T and `{k}` on P is `[k]_T`, this group is
Hom_T(P_0,P_1[k]_T). The actual comparison map is the fully faithful inclusion
on this Hom space, followed and preceded by the chosen natural isomorphisms
from hypotheses 2 and 3 and by the shift isomorphism of R. These are
isomorphisms, so the comparison itself is an isomorphism, without needing to
identify those choices with identity maps.

For fixed M, the two sides as functions of N give cohomological functors and
long exact sequences. Direct sums of exact sequences of F-vector spaces are
exact. Naturality of eta as an isomorphism of triangle functors makes the
comparison compatible with the connecting maps. Therefore the property that
the comparisons are isomorphisms in every k is preserved under shifts and
cones in N. Every bounded complex of objects of P is built from its terms by
a finite sequence of these operations, using brutal truncations. This proves
the comparison for M in P and every N in D. Apply the identical argument in
the contravariant variable M to obtain it for all M,N. This is a finite
generation argument; it invokes no convergence statement and no interchange
of an infinite product with cohomology.

For k=0, the n=0 summand maps by the ordinary map on Hom induced by R.
Injectivity of the full comparison implies injectivity on that summand.
If R(M)=0, apply the comparison to M=N. Its n=0 summand contains id_M and is
zero. Hence id_M=0, so M is a zero object. This proves conservativity. QED.

**Application and limitation.** Take P=Parity_S(X,F) and T=D^b_S(X,F).
Proposition 2.1 says that an exact extension of the parity inclusion, equipped
with a coherent Tate-trivialization, would already have the desired derived
Hom comparison. The hypotheses do not follow from the definition of K^b(P).
They isolate an existence-and-coherence problem rather than eliminate it.
Also, the original question does not expressly require that every candidate
forgetful functor extend the parity inclusion; this is a sufficient route, not
a classification of all possible answers.

## 3. Passing to perverse hearts without conflating Ext and derived Hom

Let D and T have t-structures with hearts A and B. Assume `<1>` preserves A.

**Proposition 3.1.** Under the hypotheses of Proposition 2.1, suppose R is
t-exact. Its restriction r:A -> B is exact, and it gives the required grading
isomorphisms on Yoneda Ext in degrees zero and one. The same is true in every
nonnegative degree provided that, for every pair of heart objects, the
canonical maps

    Ext_A^k(M,N) -> Hom_D(M,N[k]),
    Ext_B^k(U,V) -> Hom_T(U,V[k]_T)

are isomorphisms for all k>=0. Canonical realization equivalences
D^b(A)->D and D^b(B)->T are sufficient for this last condition.

**Proof.** A t-exact triangle functor sends the triangle of a short exact
sequence in A to a triangle whose first three terms lie in B. The perverse
cohomology long exact sequence identifies that triangle with a short exact
sequence in B. Thus r is exact. The canonical comparison between Yoneda
Ext and derived Hom is an isomorphism in degrees zero and one for any
t-structure: in degree one, extensions give connecting morphisms, and the
triangle of any morphism M->N[1] gives the inverse extension in the heart.
Those constructions are natural under a t-exact triangle functor. In higher
degrees the canonical map sends a Yoneda extension to the composition of its
degree-one connecting morphisms, so it remains natural. Apply Proposition
2.1 and the stipulated canonical comparison isomorphisms, with each N<n>
still in A. The resulting map is exactly the Yoneda Ext map induced by r and
the restricted Tate-trivialization. QED.

This proof makes no claim that an arbitrary heart realizes its ambient
triangulated category. Checking only degree-zero Hom, or only a dimension
formula, does not establish the grading asked for in [OWR].

**Lemma 3.2 (a sufficient t-exactness test).** Suppose the t-structures are
glued from the perverse t-structures on the strata. Suppose for each stratum s
there is a t-exact functor R_s on the corresponding local mixed category,
together with natural comparisons

    i_s^* R = R_s i_s^*,       i_s^! R = R_s i_s^!.

Then R is t-exact.

**Proof.** The nonpositive part of the glued t-structure is tested by all
i_s^*, and the nonnegative part by all i_s^!. Transport these two tests through
the stated comparisons and use t-exactness of R_s. This proves both required
inclusions. QED.

The comparisons in Lemma 3.2 are additional hypotheses to be constructed.
Separate local functors do not, on their own, provide them. More basically,
an orbit-Hom comparison alone does not imply t-exactness: compose the
one-stratum forgetful functor below with target shift `[1]_T`. It still kills
the grading and satisfies the same Hom comparisons, but carries a nonzero
heart object into B[1], not B.

## 4. The one-stratum case as a complete check

Let X=C^d with its single stratum and a field F. The stratification-constructible
category is generated by the constant sheaf F_X. Indeed, the local systems
are constant, X is contractible, and

    Hom(F_X, F_X{j}) = F if j=0, and 0 otherwise.

Truncation triangles therefore split, giving the usual equivalence with
D^b(F-vector spaces). Finite-dimensionality is understood throughout. The
parity category is the semisimple additive category generated by all F_X{r},
r in Z, with no maps between different r. Its bounded homotopy category
accordingly splits into finite sums of F_X{r}[i].

Write L=F_X{d}, the perverse-normalized constant object. The local mixed
heart is semisimple with simple objects L<n>, n in Z; this is the defining
local mixed perverse t-structure. Its derived category is D, since every
F_X{r}[i] is a shift of exactly one of those simples:

    F_X{r}[i] = L<d-r>[i+r-d].

Thus identify the mixed heart with finite-dimensional graded vector spaces
by L<n> corresponding to a one-dimensional vector space in degree n.
Identify the ordinary heart with finite-dimensional vector spaces by L
corresponding to F. The ordinary forgetful functor from graded to ungraded
vector spaces is exact. Derive it, and conjugate by these two realization
equivalences, to obtain R:D->D^b_S(X,F). It kills `<1>`, and the displayed
formula gives

    R(F_X{r}[i]) = F_X{r+i}.

In particular it extends the parity inclusion and is t-exact. This construction
uses actual functors between semisimple categories and their derived
categories; it does not make an unspecified choice of convolutions.

For completeness, if V,W are finite-dimensional graded vector spaces, every
linear map U(V)->U(W) decomposes uniquely into its finitely many homogeneous
components. This proves the degree-zero grading identity. Positive Yoneda
Ext groups vanish on both sides because every short exact sequence of vector
spaces, graded or ungraded, splits. Hence the full grading identity holds in
every degree. The same argument applies componentwise to a finite disjoint
union of affine spaces when every stratum is open and closed.

This is a basic special case, not new progress on nontrivial gluing and not
an answer for a general affine stratification.

## 5. Why a naive totalization is not a general construction

A complex in K^b(P) has differentials in the homotopy/derived category of
sheaves. Choosing chain-level representatives need not turn it into a strict
bicomplex. The equation d_(i+1)d_i=0 in a homotopy category only asserts that
the represented composite is null-homotopic.

Here is the first coherence calculation, independent of any claim that its
obstruction occurs on a particular variety. Work in a differential graded
category with cochain differential delta. Let f_1:A_0->A_1,
f_2:A_1->A_2, f_3:A_2->A_3 be closed degree-zero morphisms. If their adjacent
composites vanish in H^0, choose degree -1 morphisms h_21 and h_32 such that

    delta(h_21)=f_2 f_1,        delta(h_32)=f_3 f_2.

The degree -1 morphism z=f_3 h_21-h_32 f_1 from A_0 to A_3 is closed:

    delta(z)=f_3 f_2 f_1-f_3 f_2 f_1=0.

A next-stage coherent filler for these particular choices requires a
degree -2 morphism h_321 with delta(h_321)=z, up to the uniform sign
convention of the chosen twisted-complex model. Thus it requires [z]=0.
Changing either null-homotopy can change [z]; failure for one choice is not
a choice-independent obstruction. Even success at this stage is not a proof
that all higher choices can be made compatibly or functorially.

The ordinary parity condition must not be substituted for a proved
dg-formality or coherent-lifting theorem. No nonzero obstruction class for
an admissible X has been exhibited here. This calculation explains a gap in
a proposed universal construction; it is not a counterexample to the
existence of the requested functor.

## References

[OWR] Pramod N. Achar, joint work with Simon Riche, "Modular perverse sheaves
on flag varieties," in *Enveloping Algebras and Geometric Representation
Theory*, Oberwolfach Reports 12 (2015), report 25; contribution pp. 1427-1430.
https://ems.press/journals/owr/articles/13682 ; DOI
https://doi.org/10.4171/OWR/2015/25 .

[AR] Pramod N. Achar and Simon Riche, *Modular perverse sheaves on flag
varieties II: Koszul duality and formality*, Duke Mathematical Journal 165
(2016), 161-215. Inspected author preprint, version 2 dated 2014-12-20:
https://arxiv.org/abs/1401.7256 ; https://arxiv.org/pdf/1401.7256 .
