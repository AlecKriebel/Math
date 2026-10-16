# Author approach 2: exact lower-cell model by Plücker elimination

## Result and limitation

For the loopless lift f=(3,6,5,7,9), with ordinary permutation (3,1,5,2,4), the critical closure is homeomorphic to the product of two triangles. This is an authored topological result. The source-defined stratification has not been identified with the product face stratification, so this result does not settle even this example's full stratified version of the campaign target.

## Angular domain

The f-crossings are 12,13,23,24,25,45. Normalize θ₂=0. Every admissible tuple is uniquely

    (θ₁,θ₂,θ₃,θ₄,θ₅)=(-a,0,b,c,d),
    a>0, b>0, a+b<π, 0<c<d<π.

Set

    A=sin a, B=sin b, C=sin(a+b),
    D=sin c, E=sin(d-c), F=sin d.

The projective triples (A:B:C) and (D:E:F) independently range over positive triangle side-length triples. This follows from the elementary sine law and uniqueness of a Euclidean triangle from its three side ratios. Normalize each triple to sum 2. Its closure is

    T = {(x,y,z) : x,y,z>=0, x+y+z=2, x,y,z<=1} = Δ₂,₃.

Strict triangle inequalities give the relative interior of T.

## Exact measurement formula

For the five indices the Grassmann-necklace complements and signs in Galashin's boundary measurement formula (arXiv:2102.13339, Theorem 1.17) are

    J₁={2,4}, J₂={3,4}, J₃={1,4}, J₄={1,5}, J₅={1,2},
    (ε₁,...,ε₅)=(1,1,-1,-1,1).

Write l_i(t)=sin(t−θ_i), and X=sin(a+c), Y=sin(a+d). In the basis (l₁²,l₁l₂,l₂²), multiplying all five columns by A² gives the coefficient matrix

    [ 0,    BD,          AD,   AF,    0  ]
    [ -AD, -(BX+CD),    -AX,  -AY,   A²  ]
    [ AX,   CX,           0,    0,    0  ].

The trigonometric identity DY−FX=−AE is immediate by expanding the sines. Divide every 3×3 minor of this matrix by the common scalar A³X. The result, in lexicographic order 123,124,125,134,135,145,234,235,245,345, is

    (0, BE, BD, AE, AD, AF, CE, CD, CF, 0).             (1)

The accompanying SymPy check computes every minor symbolically and verifies this exact identity. The displayed matrix argument initially uses X≠0 and generic θ. The polynomial vector (1) is nonzero for every admissible θ, so continuity of the original boundary measurement map extends (1) to every admissible θ, including the interior locus X=0 at which the naive coefficient matrix loses rank. No claim is made that the generic span formula itself remains full rank on that locus.

## Compactness and injectivity

Define H:T×T→RP⁹ by (1). Let L=A+C=2−B and R=D+E=2−F. Both satisfy L,R>=1. Consequently

    Q=AD+AE+CD+CE=LR>0.

The following quantities are recovered continuously from the projective coordinates:

    B/L=(BD+BE)/Q,      F/R=(AF+CF)/Q,
    A/L=(AD+AE)/Q,      C/L=(CD+CE)/Q,
    D/R=(AD+CD)/Q,      E/R=(AE+CE)/Q.

Normalization then recovers L=2/(1+B/L), R=2/(1+F/R), hence both triples. Thus H is injective, and compactness of T×T makes it a homeomorphism onto its image. The image of relint(T)×relint(T) is exactly the critical cell. Since that set is dense in T×T, the image of all of T×T is exactly the critical closure. This proves the stated topological result.

## Why the full target is still open here

Galashin's Definition 4.9 uses the common refinement of images of open faces of the affine poset cyclohedron C(P̃_f). A homeomorphism H from a convex polytope does not by itself identify those strata with relative interiors of faces. In particular, the cyclohedron can retain relative rates at collisions involving both triangles, while formula (1) discards some of that information. One must show that its face images give precisely the product-face partition, or construct a different convex realization of the resulting refinement. Neither is asserted here.
