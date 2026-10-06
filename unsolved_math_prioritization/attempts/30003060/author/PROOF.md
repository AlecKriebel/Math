# A characteristic obstruction for higher Koszul homology

## Scope and attribution

This note concerns problem 30003060 / OWR-14218-004, attributed to Andrea Solotar's contribution, joint with Roland Berger and Thierry Lambre, in the 2016 Oberwolfach report *Hochschild Cohomology in Algebra, Geometry, and Topology*, printed pp. 479-481, DOI [10.4171/owr/2016/10](https://doi.org/10.4171/owr/2016/10).

The unrestricted-field equivalence in that question is false. We exhibit a Koszul quadratic algebra with nonzero positive-degree higher Koszul homology in every positive characteristic. This is a complete counterexample to the literal unrestricted-field formulation, not to the characteristic-zero equivalence. In particular, the implication from vanishing to Koszulness in characteristic zero remains unresolved here. The characteristic-zero question is mathematically distinct. The report does not explicitly restrict the field, and the sources do not establish a uniquely characteristic-zero historical intention. No novelty or first-priority claim is made.

The invariant is higher Koszul homology with coefficients in the algebra itself and the fundamental degree-one Koszul cocycle, as in Berger-Lambre-Solotar, [*Koszul calculus*, arXiv:1512.00183v3](https://arxiv.org/abs/1512.00183v3), Sections 2 and 5.2. It is not ordinary Koszul homology, and it is not computed with coefficients in the trivial module.

## 1. Definitions in the case needed

Let k be a field, let V have basis x,y, and let A=T_k(V)=k<x,y>, with generators in internal degree one. This is a quadratic algebra with relation space R=0; zero relations are allowed by the definition A=T(V)/(R).

For a quadratic algebra, put W_0=k, W_1=V, and

W_j = intersection over i+2+l=j of V^(tensor i) tensor R tensor V^(tensor l), for j>=2.

Here W_j=0 for j>=2. The Koszul homology complex with coefficients A is therefore exactly

0 -> A tensor V --b--> A -> 0,

where b(a tensor v)=av-va. Write C for the vector subspace spanned by all commutators av-va with a in A and v in V. Commutators of longer words are sums of these generator commutators, by successive cyclic rotations of the concatenated word. Thus C is also the full commutator subspace. Then

HK_1(A)=ker b, HK_0(A)=A/C, and HK_j(A)=0 for j>=2.

The fundamental-cocycle cap differential on a Koszul cycle is

delta([a tensor v])=[av] in A/C.

Linearity is understood for sums of simple tensors. This is the degree-one specialization of the defining higher differential. It exists in every characteristic. Thus

HK^hi_1(A)=ker(delta:ker b -> A/C),

because there is no incoming map from HK_2(A). Nonzero cycles in this kernel are genuine nonzero higher classes, with no further quotient or higher boundary to check.

## 2. Koszulness

The augmentation epsilon:A->k sends nonempty words to zero. Multiplication mu:A tensor V->A, mu(a tensor v)=av, is a graded left A-module map. Every nonempty word has a unique last letter. Consequently, mu maps the word/letter basis bijectively to the nonempty-word basis of the augmentation ideal. It is injective and its image is ker epsilon. Hence

0 -> A tensor V --mu--> A --epsilon--> k -> 0

is an exact graded free resolution, generated in degrees one and zero in homological degrees one and zero. This is a linear resolution of k, so A is Koszul over every field.

The map mu is not the commutator differential b. Confusing these maps would erase the example.

## 3. The smallest counterexample

Take k=F_2. The chain z=x tensor y + y tensor x is nonzero, because its two summands are distinct basis vectors of A tensor V. Its Koszul differential is

b(z)=(xy-yx)+(yx-xy)=0.

The higher differential is

delta([z])=[xy+yx]=[2xy]=0 in A/C,

since xy-yx is a commutator and 2=0 in k. Because W_2=0, z cannot be an ordinary Koszul boundary, and because HK_2(A)=0 its nonzero class cannot be a higher boundary either. Therefore

HK^hi_1(F_2<x,y>) != 0,

although F_2<x,y> is Koszul. This disproves the unrestricted-field forward implication, and hence the unrestricted equivalence. The class has homological degree one, coefficient weight one, and total internal weight two.

## 4. Every positive characteristic

Let char(k)=p>0, and let w=x^(p-1)y be the length-p word. Let rho move the last letter of a word to its beginning. Its p cyclic rotations w_i=rho^i(w), 0<=i<p, are distinct: the unique y occurs in different positions.

Write w_i=a_i v_i, where v_i is the last letter, and set

z_p = sum_{i=0}^{p-1} a_i tensor v_i.

These are distinct basis tensors, so z_p is nonzero. The commutator differential telescopes:

b(z_p)=sum_i (w_i-rho(w_i))=0.

Successive rotations are equal modulo C because w_i-rho(w_i)=a_i v_i-v_i a_i lies in C. Thus

delta([z_p])=sum_i [w_i]=p[w]=0.

As before, W_2=HK_2(A)=0, so this gives a nonzero HK^hi_1 class. Its coefficient weight is p-1 and its total weight is p. This uniform argument covers p=2 and all odd primes, avoiding any possible restriction to characteristic unequal to two for unrelated derivations.

## 5. Full cyclic-orbit calculation for free algebras

More generally, let V have a finite basis of r letters. Fix a positive total weight n. Concatenation identifies A_(n-1) tensor V and A_n with the same vector space E_n on length-n words. Under this identification, b=1-rho. The cyclic permutation partitions the word basis into disjoint orbits O.

On an orbit of size d, ker(1-rho) is one-dimensional, generated by s_O=sum_{w in O}w. To see this in any characteristic, the coefficient of each word in (1-rho)c is the difference of two neighboring coefficients, so all coefficients of c must agree. The quotient E_O/(1-rho)E_O is also one-dimensional: all words become equal, and the coefficient-sum functional witnesses that their common class is nonzero. No division by d is used in either assertion.

The higher differential is induced by the identity from the invariant space to the coinvariant space. It sends s_O to d[w]. It is consequently an isomorphism on this one-dimensional block when d is nonzero in k, and the zero map otherwise.

It follows that the total-weight-n components of both HK^hi_1(A) and HK^hi_0(A) have one basis class for every cyclic word orbit whose cardinality is divisible by char(k), with none in characteristic zero. Also HK^hi_j(A)=0 for every j>=2, and the weight-zero component of HK^hi_0(A) is k.

Thus the extra condition HK^hi_0(A)=k in BLS Conjecture 6.5 does not rescue the unrestricted-field formulation: this free algebra violates both that condition and positive-degree vanishing. In characteristic zero, these free algebras do have the expected vanishing, so the example gives no characteristic-zero counterexample.

## Verification and limits

The infinite statements above have algebraic proofs independent of computation. The accompanying standard-library verifier compares exact matrix/nullspace calculations with a separately implemented orbit computation in 114 bounded cases and checks explicit telescoping witnesses for 11 primes through 31. These are controls, not a proof by finite sampling. Both implementations were prepared in this author investigation; they do not constitute external independent review.

This authored note and its controls are AI-assisted and unrefereed. The corrected derivative has a separately recorded independent mathematical and source-scope audit. No characteristic-zero resolution, new theorem priority, formal proof-assistant verification, or human peer review is claimed.
