# Independent geometric reconstruction

This document was completed and hashed before reading any selected author mathematical text or historical audit. Only the parent assignment's target, the scope/receipt metadata, the Morgan–Pansu question, and primary Lauret–Will paper were available. The proof below was reconstructed from the connection and invariant planes, not from author or peer proofs.

## Exact claim and target

Fix 0<u<1/2. Let g_u have orthonormal basis e0,e1,e2,e3,e4 with abelian n=span(e1,...,e4) and [e0,x]=A_u x, where A_u=J direct_sum uN, J=[[0,-1],[1,0]], N=[[0,1],[0,0]]. Let G_u be its simply connected group. The standard metric is a non-strict local maximum of F=Scal^2/|Ric|^2 among all left-invariant metrics on this fixed group, with F=1/3. Nevertheless Ric cannot equal cI+D with D a derivation of this specified Lie algebra.

The target is Question 14, section 11, printed page 12, in the [Morgan–Pansu problem list](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf). It concerns local maxima on the left-invariant metrics of a given solvable group and defines solvsolitons through its Lie algebra. No strictness or complete-solvability condition appears there.

## 1. Curvature from the connection

For an arbitrary real A and the corresponding orthonormal almost-abelian metric, put S=(A+A^t)/2 and K=(A-A^t)/2. Koszul gives, for X,Y in n,

    nabla_0 0=0, nabla_0 X=KX,
    nabla_X 0=-SX, nabla_X Y=<SX,Y> e0.

With R(U,V)W=nabla_U nabla_V W-nabla_V nabla_U W-nabla_[U,V] W, direct substitution gives

    R(X,0)0=([K,S]-S^2)X,
    R(Z,X)Y=-<SX,Y>SZ+<SZ,Y>SX.

Contraction yields

    Ric_00=-tr(S^2), Ric_0n=0,
    Ric_nn=[K,S]-(tr A)S.

For tr A=0, [K,S]=[A,A^t]/2. Hence T=tr(S^2), C=[A,A^t] satisfy

    Scal=-T, |Ric|^2=T^2+|C|^2/4,
    F=T^2/(T^2+|C|^2/4).

When T>0, F<=1/3 is exactly P(A):=|C|^2-8T^2>=0. At A_u,

    T=u^2/2,
    Ric=diag(-u^2/2,0,0,u^2/2,-u^2/2),
    |Ric|^2=3u^4/4, F=1/3.

The independent script recomputes Ric from generic 5-dimensional structure constants and Koszul coefficients; it verifies the formula for a generic 4x4 A, even before imposing trace zero.

## 2. Every nearby metric is covered, including complement shifts

Keep the original algebra and its fixed abelian ideal n. For any nearby positive inner product, choose an orthonormal basis of n whose columns in the original basis are h; h may be chosen continuously near I by Cholesky or the positive square root. The unit vector in n-perp with positive e0 component is a(e0+w), a>0 and w in n. Since n is abelian, ad(w)|n=0. Thus the bracket matrix in this orthonormal frame is

    a h^-1 A_u h.

Both a and h depend continuously on the metric. The complement shift has no effect on this matrix. Curvature scales quadratically with a; F is unchanged. It therefore suffices to show local maximality on the whole similarity orbit of A_u, a superset of the matrices produced by nearby metric restrictions. Conversely each nearby similarity matrix can be realized by an inner product that declares the corresponding basis of n orthonormal and e0 orthogonal unit; no group variation is needed.

The simply connected group can be explicitly fixed as R semidirect R^4, with multiplication (t,z)(s,w)=(t+s,z+exp(tA_u)w). All metric variations above are inner products on this same algebra, hence left-invariant metrics on this same group.

## 3. Complete local orthogonal normal form

Let A be similar to A_u and close to it, after removing scale. Its eigenvalues are i,-i,0,0, with one rank-one zero Jordan block. The projection -A^2 has range U, the invariant real plane for i,-i; its kernel is the generalized zero plane. This projection and U vary continuously. Choose an orthonormal basis of U and extend by an orthonormal basis of U-perp. In that basis,

    A=[[B,X],[0,D]],

where tr B=0, det B=1, and D is a nonzero rank-one nilpotent 2x2 quotient operator. Write B=S_B+K_B. Its symmetric part is traceless, and an oriented orthogonal change within U diagonalizes it to diag(r,-r), r>=0. The skew part is kJ with k>0 near the standard metric, and det B=1 forces k=sqrt(1+r^2). An orthogonal basis of U-perp adapted to ker D and im D makes D=vN with v>0. Thus every nearby orbit point is orthogonally represented by

    B(r)=[[r,-sqrt(1+r^2)],[sqrt(1+r^2),-r]],
    D(v)=[[0,v],[0,0]], X arbitrary real 2x2,
    r near 0, v near u, |X| near 0.

The rotation diagonalizing S_B need not tend to I as r tends to zero. This causes no gap: it commutes with J, leaves |X| unchanged, and keeps the transformed B near J. This is a covering normal form, not an assertion of a smooth quotient chart at the isotropy-singular standard point. The scalar r measures both components of the traceless symmetric B-direction.

No upper-right coupling is excluded. In fact every such block matrix is similar to A_u: B is similar to J, D(v) is similar to uN, and the Sylvester map Z -> BZ-ZD is invertible because their spectra are disjoint; a block shear removes X.

## 4. Uniform control of all transverse directions

Write the columns of X as x,y in R^2. Then

    T=2r^2+v^2/2+|X|^2/2,
    C=[[C_B+XX^t, XD^t-B^tX],
       [DX^t-X^tB, C_D-X^tX]],
    C_B=[[0,4rk],[4rk,0]], C_D=diag(v^2,-v^2).

Let P(r,X,v)=|C|^2-8T^2, with k=sqrt(1+r^2). This is smooth near r=0, including signed r as an auxiliary coordinate. For every v>0,

    P(0,0,v)=0, d_(r,X)P(0,0,v)=0.

Its quadratic term in z=(r,X) is

    Q_v(z)=16(2-v^2)r^2
          +2|y+vJx|^2+2(1-4v^2)|x|^2.

This identity was verified exactly by the independent script. It is positive definite whenever 0<v<1/2. For the fixed 0<u<1/2 choose a closed interval I around u contained in (0,1/2). By compactness, Q_v(z)>=m|z|^2 for all v in I and some m>0. Continuity of the z-Hessian gives a single delta>0 such that its change from z=0 has norm at most m, uniformly on v in I and |z|<delta. Taylor's integral formula then gives P(z,v)>=m|z|^2/2 (after harmless adjustment of the constants). Therefore P>=0 in a full neighborhood in this covering normal form, with equality exactly when r=X=0. Since T remains positive, F<=1/3 there.

This controls the flat v-direction uniformly. A semidefinite Hessian at only v=u would not suffice; the interval argument closes that gap. Complement shifts, scale, orthogonal basis changes, and every similarity transverse direction have all been included.

## 5. Derivation obstruction

Assume Ric=cI+D. Then D is forced to be the displayed diagonal matrix minus cI, regardless of what general derivations might preserve. In particular D e0=d0 e0 with d0=-u^2/2-c, and D_n is block diagonal. Applying the derivation identity to [e0,x]=A_u x gives

    [D_n,A_u]=d0 A_u.

On U, D_U=-cI commutes with J, so d0=0, forcing c=-u^2/2. On the nilpotent block, [D_V,uN]=u^3N, whereas d0uN=0. Since u>0 this is impossible. This argument does not assume that every derivation preserves n; only the uniquely forced candidate Ric-cI does.

## 6. Boundary and semantic falsifiers

At u=0 the standard metric is flat, Ric=0, and F is undefined. It is excluded.

At u=1/2 set r=0 and X=[[a,0],[0,-a/2]], keeping v=1/2. The exact P is -a^4. These triangular matrices remain in the same similarity orbit by the Sylvester argument, and tend to the standard one as a tends to zero. Hence the endpoint is not a local maximum, despite its semidefinite transverse quadratic form. For u>1/2, y=-uJx gives a negative quadratic direction. These are independent, checkable boundary falsifiers.

The metric is nevertheless a Ricci soliton as a Riemannian manifold. Indeed write group coordinates as t, q in R^2 (rotation block), z in R^2 (nilpotent block). Its standard line element is

    dt^2+|dq|^2+|exp(-tuN)dz|^2.

It is the product of Euclidean R^2 and the standard three-dimensional Heisenberg metric [e0,e4]=u e3. On the product nilpotent algebra, Ric=(-3u^2/2)I+D with D eigenvalues u^2 on e0,e4, 2u^2 on e3, and 3u^2/2 on the Euclidean directions; this is a derivation. That distinct transitive nilpotent presentation explains the Ricci-soliton status. It does not turn Ric-cI into a derivation of g_u. Thus the example addresses the exact printed solvsoliton statement while remaining compatible with a claim that local maxima are Ricci solitons.

## Independent conclusion before author-source inspection

The proposed all-metrics local-maximum and non-solvsoliton claims have a complete independent geometric proof for 0<u<1/2. No remaining mathematical gap has been identified in this route. This does not yet certify the selected author proof or publication package; those are next to inspect. Completion estimate: 60% of this geometric audit. Author proof-search turns: zero.
