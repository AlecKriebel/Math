# A physical proof of the center-pedal/edge-vector reduction

This derivation was completed after the independent mechanism freeze and after the inherited proof was read. It is a separate elementary Cartesian verification of its geometric reduction, not a claim to independent discovery of the theorem or historical priority. It does not use the Jacobi parametrization.

Let E have semiaxes a>b>0 and fix 0<lambda<b². Write T=sqrt(lambda). At a boundary point q=(a c,b s), c²+s²=1, define

    D=b²c²+a²s²,   R=sqrt(D-lambda)>0,   e=(c,s).

The counterclockwise outgoing unit billiard velocity tangent to the caustic is

    v=(-a s R-b c T, b c R-a s T)/D.                  (C1)

Indeed v has unit length and the ellipse normal n_q=(c/a,s/b) satisfies n_q dot v=-T/(ab). For any unit chord velocity u through a boundary point x, its confocal parameter is

    a²u_y²+b²u_x²-det(x,u)² = a²b²(n_x dot u)².       (C2)

Thus (C1) has the required caustic and points into E; its counterclockwise tangential component is positive.

Define two points by

    F_±(q)=[R(-a²s,b²c) ± abT(c,s)]/D.              (C3)

Direct substitution gives F_± in E and

    (-s,c) dot F_±=R,
    F_+-F_-=2abT(c,s)/D.                            (C4)

The line in (C4) is tangent to the *same* confocal caustic: its unit-normal support squared on that caustic is (a²-lambda)s²+(b²-lambda)c²=D-lambda=R². Both endpoints are finite and distinct.

We next verify that the consecutive chords (C3) actually join into a closed billiard. Put r=F_-(q) and n_r=(r_x/a²,r_y/b²). The two exact identities

    diag(a,b)n_r=v,     e dot n_r=-T/(ab)            (C5)

are immediate from (C1) and (C3). Reflect the incoming transformed velocity -e at r. Its reflected velocity is -e_next, where

    e_next=e-2(e dot n_r)n_r/||n_r||².

Consequently, with q_next=diag(a,b)e_next,

    q_next-q=2T v/[ab||n_r||²].                     (C6)

The vector e_next is unit. Thus q_next belongs to E, and (C6) says it is the nontrivial next intersection of E with the original billiard ray q+t v: the coefficient is strictly positive, and ||n_r||²=v_x²/a²+v_y²/b², giving exactly the ordinary quadratic-intersection length.

To fix the sign of the next chord branch, reflection gives e_next dot n_r=T/(ab)>0. Equation (C2) shows that the line through r in direction e_next still has caustic lambda. Its signed support d_next=(-e_next_y,e_next_x) dot r cannot vanish, since d_next²=D_next-lambda>=b²-lambda>0. This support is continuous on the connected strict domain 0<lambda<b² and the full circle of e; as lambda tends to zero, it tends to sqrt(D)>0. It is therefore the positive branch everywhere. The positive normal component e_next dot n_r then identifies r as F_+(q_next), rather than F_-(q_next). We have proved

    F_-(q_i)=F_+(q_(i+1)).                           (C7)

Hence X_i=F_+(q_i) is a billiard orbit on the same ellipse and caustic, with edge X_(i+1)-X_i=F_-(q_i)-F_+(q_i). If q has period N, so does this ordered X sequence (possibly with a smaller least period; no primitivity is needed for the identity).

The center foot on the tangent at q is

    H(q)=(a b² c,a² b s)/D
        =diag(b,a)(F_+(q)-F_-(q))/(2sqrt(lambda)).  (C8)

Therefore the actual center-pedal polygon is a fixed linear image of the *negative ordered edge-vector polygon* of X. Its signed area is

    area(H)=[ab/(4lambda)] area(edges(X)).          (C9)

The minus sign has determinant +1. This is the precise geometric statement used in inherited equations (14)-(15), because its matrix there simplifies to diag(b,a)/(2sqrt(lambda)): canonical relations give cn(K-v)=sqrt(lambda)/a. The separate algebraic identity

    area(edges(X))=2area(X)-(1/2)sum det(X_i,X_(i+2))

holds for arbitrary ordered polygons, including stars, repeated traversals, and split skip-two cycles. No spatial reordering or simplicity premise occurs.

The checker proves 11 generic polynomial identities in (C1)-(C5),(C8), with c²+s²=1 and R²=D-T², by exact symbolic reduction. The branch/positivity and sequence argument above supplies the geometric part not encoded by a polynomial zero. These facts establish the universal Cartesian reduction; they do not by themselves prove the remaining phase-product identity. The inherited odd-order elliptic trace argument supplies that analytic step.
