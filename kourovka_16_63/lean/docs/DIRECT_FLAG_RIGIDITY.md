# A classification-free proof of full flag rigidity

**Status:** a new mathematical argument developed in this session. Its finite
identities and two-generator recipes were checked exactly by
`scripts/direct_flag.py`. This document is not a Lean proof, and the external
checks do not establish that Lean accepts the argument. No novelty claim is made.

The argument uses the paper's exact, raw-transvectant normalization. It proves
both stabilizer assertions needed for the lifting lemma without classifying the
whole automorphism group, proving cohomology vanishing, or identifying every
derivation as inner. These other results may remain useful elsewhere, but they
are unnecessary for this particular route to the lifting step.

## 1. Setting

Let k = F_1009 and let B be the paper's 31-dimensional k-vector space with its
specified bracket. Write

    x = h,
    y = e + f + U_1 + V_0 + R_2,
    t = U_0,
    z = U_1 + V_0,
    r = R_2.

The original ordered basis is

    h,e,f,U_0,...,U_6,V_0,...,V_4,W_0,...,W_6,T_0,T_1,T_2,R_0,...,R_4,Z_0.

The flags are F2 = span(x,y) and F3 = span(x,y,t). All integers divided by below
are nonzero modulo 1009. No assumption about disconnected components of the
automorphism group is made.

The following exact identities are immediate from the bracket table, and were
independently recomputed over the integers:

    [x,t] = 6t,
    [y,t] = 6U_1,
    [x,y] = 2e - 2f + 4U_1 + 4V_0,
    [e,f] = x,
    [e,z] = t,
    [r,t] = 0,
    [U_2,U_6] = 2880W_5,
    [U_0,W_5] = 86400T_0,
    [U_0,V_4] = 8640T_0.

In particular [x,y] has zero h-coordinate and zero R_2-coordinate.

## 2. Explicit two-generator reconstruction

Put H(v) = [x,v]. The h-weights present in y are 2,-2,4,0, and H(x)=0.
The following integer identities hold:

    16e = -H^3(y) + 2H^2(y) + 8H(y),
    48f = -H^3(y) + 6H^2(y) - 8H(y),
    48z =  H^3(y) - 4H(y),
    16r =  H^3(y) - 4H^2(y) - 4H(y) + 16y.

Their denominators are units in k and Z_1009. Starting with x,y, form e,f,z,r
using these formulas, and then use:

    U_0 = [e,z],
    U_j = [f,U_(j-1)]/(7-j)                   (1 <= j <= 6),
    V_0 = z-U_1,
    V_j = [f,V_(j-1)]/(5-j)                   (1 <= j <= 4),
    R_0 = [e,[e,r]]/2,
    R_j = [f,R_(j-1)]/(5-j)                   (1 <= j <= 4),
    W_0 = [U_0,U_3]/720,
    W_j = [f,W_(j-1)]/(7-j)                   (1 <= j <= 6),
    T_0 = [U_0,V_4]/8640,
    T_1 = [f,T_0]/2,
    T_2 = [f,T_1],
    Z_0 = [V_0,R_4]/576.

Together with x=h, these are all 31 basis vectors. The generated 88-node DAG
records the recipes with shared subexpressions. Every node was evaluated using
exact rational arithmetic; all 31 targets are exactly the intended standard
basis vectors. All denominators are coprime to 1009, so the same equalities
specialize to F_1009 and to Z_1009. This is a mathematical specialization
argument, not a claim that a Z_1009 scalar map is already formalized.

Thus x,y generate B as a Lie algebra over k and as a Lie lattice over Z_1009.
A linear bracket-preserving map fixing x,y fixes every expression in these
recipes and is the identity. A derivation killing x,y kills every such
expression by the Leibniz rule and is zero.

## 3. Every flag-preserving automorphism fixes x

Let Q be any k-linear bracket-preserving bijection with Q(F2)=F2 and
Q(F3)=F3. In fact the inclusions Q(F2) subset F2 and Q(F3) subset F3,
together with injectivity, are enough below.

There are scalars a,b,c,d,u,v,s with

    Qx = ax+by,
    Qy = cx+dy,
    Qt = ux+vy+st.

Apply Q to [x,t]=6t. Bilinearity and the identities above give

    (av-bu)[x,y] + 6as t + 6bs U_1 = 6u x + 6v y + 6s t.          (1)

Taking the h-coordinate gives u=0. Taking the R_2-coordinate gives v=0.
Since Q is injective and t is nonzero, Qt=st is nonzero, so s is nonzero.
The U_0-coordinate of (1) now gives a=1, and its U_1-coordinate gives b=0.
Therefore Qx=x. This step does not invoke the radical or any group
classification theorem.

## 4. The remaining sign is excluded by the raw brackets

Because Qx=x, Q commutes with H. Apply Q to the four projector identities
in Section 2, using Qy=cx+dy and Hx=0. It follows that

    Qe=de,   Qf=df,   Qz=dz,   Qr=cx+dr.

From [e,f]=x and Qx=x, we obtain d^2=1. From [e,z]=t we obtain Qt=d^2t=t.
Applying Q to [r,t]=0 now gives 6ct=0, hence c=0. Thus Qy=dy.

Using [f,U_j]=(6-j)U_(j+1), starting from QU_0=U_0, we get

    QU_j=d^j U_j.

Since V_0=z-U_1, QV_0=dV_0, and similarly

    QV_j=d^(j+1)V_j.

As d^2=1, QU_2=U_2, QU_6=U_6, and QV_4=dV_4. Applying Q successively to

    [U_2,U_6]=2880W_5,
    [U_0,W_5]=86400T_0

shows QW_5=W_5 and QT_0=T_0. But applying Q to

    [U_0,V_4]=8640T_0

shows QT_0=dT_0. Since T_0 is a nonzero basis vector, d=1. Consequently
Qx=x and Qy=y. Section 2 gives Q=id.

**Conclusion:** the stabilizer of F2 subset F3 in the full Aut_k-Lie(B) is
trivial. No finite-field automorphism component is excluded by assumption.

## 5. Every flag-preserving derivation is zero

Let D be a k-linear derivation with D(F2) subset F2 and D(F3) subset F3.
Write

    Dx=ax+by,   Dy=cx+dy,   Dt=ux+vy+st.

Apply the Leibniz rule to [x,t]=6t:

    6a t + 6b U_1 + v[x,y] + 6s t = 6u x + 6v y + 6s t.           (2)

The h- and R_2-coordinates again give u=v=0. The U_0- and U_1-coordinates
then give a=b=0. Hence Dx=0, so D commutes with H.

The projector identities give

    De=de,   Df=df,   Dz=dz,   Dr=cx+dr.

Applying D to [e,f]=x gives 2dx=0, hence d=0. Applying D to [e,z]=t gives
Dt=0. Applying D to [r,t]=0 now gives 6ct=0, hence c=0. Thus Dx=Dy=0,
and Section 2 gives D=0.

**Conclusion:** the infinitesimal flag stabilizer is zero without an inner-
derivation classification.

## 6. Verification scope and next formal steps

The executable reconstructs the original coefficient table from the raw
transvectant formula, compares it with the bundled table, checks all 4495
increasing-index Jacobi triples, checks the displayed special identities and
projector formulas, and validates every DAG target. A deliberately wrong W_0
normalization is rejected. These are exact mathematical computations but they
remain outside Lean's trust boundary.

To use this route in the final formal proof, Lean must still check:

1. The coefficient table's equality with the raw-transvectant definition, and
   its Lie identities on arbitrary vectors.
2. The finite identities, DAG soundness and acceptance, and specialization to
   the relevant coefficient rings.
3. The coordinate argument above for arbitrary bracket-preserving linear
   equivalences and derivations.
4. The separate lifting, logarithm/exponential, Smith/kernel and BCH/Lazard
   arguments. None follows merely from flag rigidity.
