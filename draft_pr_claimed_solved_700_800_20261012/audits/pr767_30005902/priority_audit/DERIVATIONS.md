# Checkable implications, independent of broad source assertions

## A complete old-family counterexample to the original unrestricted question

This is our explicit specialization of the coordinate-group family discussed in FS final Ex2.4. It is not represented as an algebra named verbatim in that example.

Over Q set A=Q[x,y,z]. The matrices

    U(x,y,z) = [[1,x,z],[0,1,y],[0,0,1]]

multiply by U(x,y,z)U(x',y',z')=U(x+x',y+y',z+z'+xy'). Thus U3 is a connected smooth affine nonabelian algebraic group (underlying affine 3-space), and A is its coordinate Hopf algebra. Its coproduct has x,y primitive and Delta z=z tensor 1+1 tensor z+x tensor y; epsilon evaluates at the origin; S(x)=-x, S(y)=-y, S(z)=-z+xy. Coassociativity is the associative displayed group law; S^2=id by substitution. The distinct tensor monomials x tensor y and y tensor x prove noncocommutativity. Since A tensor A is commutative, conjugation by any putative R is trivial, contradicting Delta^op z != Delta z. Hence A is non-quasitriangular.

Let f_x,f_y,f_z be the linear-coefficient maps at the origin. For I=(x,y,z), each vanishes on 1 and I^2, and therefore f(ab)=epsilon(a)f(b)+f(a)epsilon(b). These are scalar bar 1-cocycles. Every scalar 0-coboundary is epsilon(a)c-c epsilon(a)=0. Thus [f_z] is nonzero in Ext_A^1(Q,Q), witnessed by f_z(z)=1. This argument uses neither a generic exterior-cohomology theorem nor the questionable cotangent notation in FS Ex2.4.

## The two embeddings and why a sign cannot rescue universal vanishing

Put f*g=(f tensor g)Delta. FS uses L_f=(id tensor f)Delta. Coassociativity gives L_f L_g=L_(f*g). Their degree-one bracket is f*g-g*f. The tensor-induced bar comparison in Karadag section 5 instead gives R_f=(f tensor id)Delta; coassociativity gives R_f R_g=R_(g*f). The Hochschild degree-one bracket is the ordinary commutator, so its scalar preimage is g*f-f*g. Both maps split under epsilon, and applying epsilon to an inner derivation gives zero. Thus they inject degree-one scalar classes into HH^1. The underlying Hochschild operation is the same commutator, evaluated on different embedded images; we do not identify the two embeddings as equal.

For the coproduct above their generator tables are:

| map | x | y | z |
|---|---:|---:|---:|
| L_fx | 1 | 0 | 0 |
| L_fy | 0 | 1 | x |
| L_fz | 0 | 0 | 1 |
| R_fx | 1 | 0 | y |
| R_fy | 0 | 1 | 0 |
| R_fz | 0 | 0 | 1 |

These are derivations because the augmentation derivation identity and multiplicativity of Delta give the Leibniz rule. A derivation is determined by its generator values. Consequently [L_fx,L_fy]=L_fz, while [R_fx,R_fy]=-R_fz. Applying epsilon gives respectively f_z and -f_z, both nonzero. The degree of the result is 1+1-1=1. KW Thm4.1 identifies the latter induced operation with the monoidal bracket in OWR, since S is bijective. Hence this is a complete negative instance of the literal original question in characteristic zero and infinite dimension, already within the old coordinate-group family. It is not a solution of a finite-dimensional characteristic-zero restriction.

This derivation establishes all missing yes/no conditions rather than treating the bare existence of invariant derivations as a prior answer. Source Ex2.4 does not use the later problem's wording or separately prove non-quasitriangularity; those are transparent implications checked here. Ex2.3 independently supplies precisely the needed degree-one rule. We date the added explicit examples conservatively to the final publication, 2 June 2004, not to the 2002 arXiv submission.

## The finite27 example as a standard dual construction

In characteristic 3, the Frobenius map on U3 cubes coordinates. Its kernel has coordinate algebra H=F3[x,y,z]/(x^3,y^3,z^3) with the same coproduct. This identification follows immediately from the matrix group law and the scheme-theoretic kernel equations x^3=y^3=z^3=0; it does not identify H-modules with rational U3 modules.

Under convolution in H*, the primitive coefficient functionals X=f_x,Y=f_y,Z=f_z satisfy [X,Y]=Z, [X,Z]=[Y,Z]=0 and X^3=Y^3=Z^3=0. These equalities can be checked from the coproduct. The 27 ordered monomials X^aY^bZ^c, 0<=a,b,c<3, span H*: their pairing with the polynomial basis is invertible. verify_implications.py checks its rank is 27 over F3 by exact elimination. Thus H* is the restricted enveloping algebra of the three-dimensional Heisenberg Lie algebra with zero restricted powers, and H is its finite coordinate dual. Primitives are exactly the three augmentation derivations because I/I^2 has basis x,y,z.

This checks applicability of FS final Ex2.3 to the finite example. It does not establish that the precise quotient presentation and bracket were printed earlier. General restricted-Lie/Frobenius-kernel sources often calculate Ext over u(g) or kG; that is Ext over H*, whose tensor category is symmetric. It must not be substituted for Ext over H. The current packet's finite presentation and computational exposition are useful even though the original universal problem already has an older counterexample family.

## Scope of verification

verify_implications.py supplements these proofs with exact finite arithmetic: coproduct-derived dual multiplication, convolution relations and PBW-pairing rank. The rational coordinate calculation is checked through generator derivations; determination by generators supplies the proof for all polynomials. Numeric tests do not replace source theorem comparison or prove global firstness. No higher-degree claim is required here; separately restricted problems are not promoted by this audit.
