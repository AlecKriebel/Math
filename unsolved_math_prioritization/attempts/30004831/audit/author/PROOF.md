# A checked order two counterexample

## Attribution and conclusion

The unrestricted question has a negative answer, already given by Ruipeng Zhu, Example 4.11 of [Z]. The construction below is its order-two specialization. We give direct checks, including consistent left coproduct conventions, rather than relying on every intermediate display in [Z]. This is a reconstruction of existing mathematics, not a new-resolution claim.

Work over k = C. Define

H = k<g,g^{-1},x> / (gg^{-1}=g^{-1}g=1, xg=-gx, x^2=1-g^2),

L = k<h,h^{-1},y> / (hh^{-1}=h^{-1}h=1, yh=-hy, y^2=0).

Use the Hopf structures

Delta(g)=g tensor g, Delta(x)=x tensor 1 + g tensor x,

Delta(h)=h tensor h, Delta(y)=y tensor 1 + h tensor y,

epsilon(g)=epsilon(h)=1, epsilon(x)=epsilon(y)=0,

S(g)=g^{-1}, S(x)=-g^{-1}x; S(h)=h^{-1}, S(y)=-h^{-1}y.

We prove that their categories of right comodules are k-linear tensor equivalent, while

cd(H)=gldim(H)=1 and cd(L)=gldim(L)=infinity.

Here cd(A)=pd over A tensor A^op of the regular bimodule A. For Hopf algebras this also equals left and right global dimension and the projective dimensions of the trivial left and right modules; see [B22, introduction] and [B26, before Theorem 3.2]. It is not Gerstenhaber-Schack dimension.

## Normal forms and Hopf identities

Each algebra has basis g^i x^j, respectively h^i y^j, for i in Z and j in {0,1}. One construction starts with the skew polynomial extension of the Laurent polynomial ring, using the automorphism that negates the Laurent generator, and then imposes the monic quadratic relation. Its constant polynomial is invariant under that automorphism. Division by the monic relation therefore gives exactly the stated basis and an associative multiplication. Explicitly,

(g^i x^j)(g^r x^s)=(-1)^{jr} g^{i+r} x^{j+s},

with x^2 replaced by 1-g^2; for L replace y^2 by zero. The formula also applies when i or r is negative.

The coproduct of x squares to

x^2 tensor 1 + (xg+gx) tensor x + g^2 tensor x^2
= (1-g^2) tensor 1 + g^2 tensor (1-g^2)
= 1 tensor 1 - g^2 tensor g^2.

The mixed relation is preserved because xg+gx=0 in each relevant factor. For L the same computation gives Delta(y)^2=0. Coassociativity and the counit identities follow on the generators from their displayed skew-primitive forms. The proposed antipodes preserve the opposite-algebra relations and satisfy both antipode identities on the generators; these identities then extend to the generated bialgebras. In each case S^2 fixes the Laurent generator and negates x or y, so S^4=id. Both antipodes are bijective.

## The bi-Galois object

Set

B = k<u,u^{-1},t> / (uu^{-1}=u^{-1}u=1, tu=-ut, t^2=-u^2).

Its basis is u^i t^j, i in Z, j in {0,1}, by the same normal-form construction. Define a right H-coaction rho and a left L-coaction delta by

rho(u)=u tensor g, rho(t)=t tensor 1 + u tensor x,

delta(u)=h tensor u, delta(t)=h tensor t + y tensor 1.

For rho, the mixed terms in rho(t)^2 vanish and

rho(t)^2=-u^2 tensor 1 + u^2 tensor (1-g^2)
=-u^2 tensor g^2=-rho(u)^2.

For delta, the mixed terms likewise vanish and

delta(t)^2=h^2 tensor (-u^2)=-delta(u)^2.

The skew-commutation relations and inverse relations are preserved. Thus these are algebra maps. Coassociativity and counit identities hold on u,t; notably delta requires the coproduct Delta(y)=y tensor 1+h tensor y used here. The two coactions commute: on t either composition is

h tensor t tensor 1 + y tensor 1 tensor 1 + h tensor u tensor x,

and on u either is h tensor u tensor g.

Define the canonical maps

can_R(a tensor b)=(a tensor 1)rho(b),

can_L(a tensor b)=delta(a)(1 tensor b).

They are bijective, as can be seen without any cleft-map inference. For can_R use the left B-module bases indexed by the second tensor factor:

can_R(a tensor u^i)=a u^i tensor g^i,

can_R(a tensor u^i t)=a u^i t tensor g^i + a u^{i+1} tensor g^i x.

The diagonal coefficients u^i and u^{i+1} are invertible. Explicit inverse formulas, for b in B, are

can_R^{-1}(b tensor g^i)=b u^{-i} tensor u^i,

can_R^{-1}(b tensor g^i x)
=b u^{-(i+1)} tensor u^i t - b u^{-1}t u^{-i} tensor u^i.

For can_L use the right B-module bases indexed by the first factor:

can_L(u^i tensor b)=h^i tensor u^i b,

can_L(u^i t tensor b)=h^{i+1} tensor u^i t b + h^i y tensor u^i b.

Its inverse is

can_L^{-1}(h^i tensor b)=u^i tensor u^{-i}b,

can_L^{-1}(h^i y tensor b)
=u^i t tensor u^{-i}b - u^{i+1} tensor u^{-1}t u^{-i}b.

Substitution verifies both compositions. Comparing coefficients in rho(b)=b tensor 1 first kills every t term and then all u^i terms except i=0; hence the right coinvariants are k. The analogous comparison for delta gives the left coinvariants k. B is nonzero and faithfully flat over k because it is a nonzero vector space. Thus B is an L-H-bi-Galois object.

The standard bi-Galois equivalence theorem gives a k-linear strong monoidal equivalence from right L-comodules to right H-comodules by cotensoring with B. This is the external categorical theorem used here, stated in [B22, Section 2.2, page 565], originally due to Schauenburg [S]. Equivalence of comodule categories is exactly the equivalence in the question; an equivalence of algebra-module categories is neither asserted nor needed.

## Why H has global dimension one

Let D=k[x,(1-x^2)^{-1}]. This is a localization of the PID k[x], and is a PID itself. H is the crossed product D direct-sum Dg, with

g d=sigma(d)g, sigma(x)=-x, and g^2=1-x^2 in D^times.

These relations give an algebra with the same presentation as H: the inverse of g is (1-x^2)^{-1}g, and conversely (1-x^2)^{-1}=g^{-2}. They establish the claimed identification and show H is free as both a left and a right D-module.

For every left H-module M, its restriction to D has a projective resolution of length at most one. Applying H tensor_D - produces a projective H-resolution of H tensor_D M of length at most one. The natural multiplication map H tensor_D M -> M has the H-linear splitting

m |-> (1/2)(1 tensor m + g tensor g^{-1}m).

D-linearity follows from g^{-1}d=sigma(d)g^{-1}. For g-linearity, use g^2 in D and move it across the balanced tensor product. Multiplication composed with this map is the identity. Hence M is a direct summand of a module of projective dimension at most one, so pd_H(M)<=1. This establishes left global dimension at most one.

It is not zero. The central element x^2 is a nonzero non-zero-divisor: multiplication by it is injective on D direct-sum Dg. Its ideal is proper because the counit kills x^2. If H/Hx^2 were projective, the sequence 0 -> Hx^2 -> H -> H/Hx^2 -> 0 would split, giving H=Hx^2 direct-sum J as left modules. Then x^2 J lies in both summands and must vanish. Regularity forces J=0, contradicting the nonzero quotient. Consequently this quotient has projective dimension one.

The bijective antipode identifies H with its opposite algebra, giving the same right global dimension. Thus gldim(H)=1.

## Why L has infinite global dimension

The subalgebra E=k[y]/(y^2) embeds in L by the normal forms. L is free as a left E-module, with basis {h^i : i in Z}; moving y through powers of h only changes a sign. Therefore restriction from L-modules to E-modules takes projectives to projectives.

The trivial E-module k has the exact infinite free resolution

... -> E --y--> E --y--> E -> k -> 0.

At every positive degree, image and kernel are both ky. Applying Hom_E(-,k) gives zero differentials and a copy of k in every degree. Thus Ext_E^n(k,k)=k for every n>=0, and pd_E(k)=infinity.

If the trivial L-module had finite projective dimension, a finite L-projective resolution would restrict to a finite E-projective resolution of k, which is impossible. Hence pd_L(k)=infinity and gldim(L)=infinity. The same argument on the other side, or the antipode, gives the right-handed conclusion.

## Hypotheses and boundaries

This is a counterexample over an algebraically closed field of characteristic zero, with bijective antipodes satisfying S^4=id. Both Hopf algebras are infinite-dimensional. They are finite free of rank four over the central Laurent ring generated by g^2, respectively h^2, so are noetherian affine PI algebras; the faithful regular representation over that ring also exhibits a matrix polynomial identity.

Neither is cosemisimple. For H, the right subcomodule spanned by g,x is an extension of the trivial comodule by kg. A splitting would require x+c g to be coinvariant, but its coproduct differs from (x+c g) tensor 1 by g tensor (x+c g-c), which is nonzero by the normal forms. Replace g,x by h,y to obtain the same obstruction for L. Therefore positive cosemisimple results are not contradicted.

L is not homologically smooth, because smoothness would imply finite Hochschild dimension. Thus the theorem requiring both algebras to be smooth does not apply. The theorem requiring both global dimensions to be finite likewise does not apply. In particular, finiteness on only one side cannot replace finiteness on both sides.

The proof establishes the exact unrestricted negative answer. No attempt is made to classify the remaining positive subclasses.

## References

- [Z] R. Zhu, Artin-Schelter Gorenstein property of Hopf Galois extensions, Example 4.11. Inspected manuscript: https://arxiv.org/abs/2501.02828v2 . Journal metadata: J. Pure Appl. Algebra 229 (2025), issue 12, article 108123, https://doi.org/10.1016/j.jpaa.2025.108123 .
- [B22] J. Bichon, On the monoidal invariance of the cohomological dimension of Hopf algebras, C. R. Math. 360 (2022), 561-582, https://doi.org/10.5802/crmath.329 .
- [B26] J. Bichon, Monoidal invariance of the cohomological dimension of Hopf algebras: the finite case, https://arxiv.org/abs/2602.12731v1 .
- [S] P. Schauenburg, Hopf bi-Galois extensions, Comm. Algebra 24 (1996), 3797-3825, Corollary 5.7. The theorem is invoked through the inspected statement [B22, Section 2.2, page 565], not represented as a fresh full inspection of [S].
