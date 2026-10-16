# Turn1 mathematical checkpoint, before the separate k203,a review

2026-10-01 05:11 UTC. This is an author derivation awaiting exact-source/Jacobi verification and complete candidate packaging. It was derived before reading either the parallel k303,a candidate or the k203,a candidate/shared pole lemma. No result from those packets is an input. This checkpoint is not a review request or final disposition.

Use Stachel's parametrization with caustic axes alpha,beta, modulus k=sqrt(alpha²−beta²)/alpha, quarter period K, and v=2tauK/N in(0,K). The outer axes satisfy a=alpha dn(v)/cn(v), b=beta/cn(v). Let P(u)=(-a sn u,b cn u), with orbit vertices P(u+2iv). Write

    f(t)=sn(t)cn(t)/dn(t),  T(u)=sum_i dn(u+2iv).

Jacobi addition appears to give the exact cross-product identity

    det(P(z−t),P(z+t))
      =2ab sn(t)cn(t) dn(z)/(1−k²sn²(z)sn²(t))
      =ab f(t)[dn(z−t)+dn(z+t)].

Consequently original area is ab f(v)T(u), and the area of its ordered edge-vector polygon is ab[2f(v)−f(2v)]T(u), since area(Delta P)=2area(P)−(1/2)sum det(P_i,P_(i+2)). No approximation or area division enters.

The outer tangent vertex is diag(a/alpha,b/beta) P(u_i+v), because its caustic contact is (-alpha sn(u_i+v),beta cn(u_i+v)) and conic polarity gives outer/contact coordinates. Thus

    A'(u) = (a²b²/(alpha beta)) f(v) T(u+v).

The foot of O on the outer tangent at P(u) is

    Q(u)=(-a b² sn(u),a² b cn(u))/(a²−(a²−b²)sn²(u)).

Set w=K−v. Jacobi quarter-shift formulas give sn(w)=cn(v)/dn(v), dn(w)=b/a. Adding P(u+w) and P(u−w), then using P(z−2K)=−P(z), gives

    Q(u)=L[P(u+K−v)−P(u+K+v)],
    L=diag(b/a,1)/(2cn(w)), det L=b/(4a cn²(w)).

Therefore

    A'_O(u)= [b²/(4cn²(w))][2f(v)−f(2v)] T(u+K−v).

Cyclic invariance gives T(u+2v)=T(u), so the requested area product is a fixed real coefficient times

    T(u+v) T(u+v+K).                                      (*)

## Proposed complete pole argument for (*)

Let q=N/gcd(N,2), r=N/q. Because gcd(tau,N)=1, the real shifts modulo2K form the subgroup H={2Kj/q}, and T(u)=r sum_(h in H)dn(u+h). Our exact parity condition is q odd.

For0<k<1, dn has periods2K,4iK', anti-period2iK', and only simple poles at iK'+2mK+2n iK'. Thus T has only simple poles, at those points shifted by H (r duplicates give multiplicity in the coefficient, not higher pole order).

Put c=K+iK'. The period/evenness identities imply dn(c+t)=−dn(c−t). For odd q, no h in H is congruent toK modulo2K, so every summand dn(c+h) is finite. The subgroup is invariant under h↦−h, hence T(c)=0 by pairing. At every pole p of T, periodicity and anti-periodicity therefore give T(p+K)=0. Conversely, at a pole of T(u+K), T(u)=0 because2K is a period. All putative poles of the elliptic product T(u)T(u+K) are removable, so the product is constant by compactness of the torus. For real u all summands dn are positive, ruling out an accidental identically-zero trace.

Still to verify before full freeze: exact primary pole/period table, every coefficient in the addition and projection formulas, source-scope/primitive/star details, and independent exact or high-precision diagnostics. Circle k=0 is a separate rigid-rotation limit, outside the source's strict a>b assumption. No use of the other ongoing candidate is planned.

## Research clock

Author turn1 began05:06 UTC and pauses05:11 UTC for the parent-assigned independent5100011 review. Approximately5 active minutes used. No new author turn is charged for that separate review, and no publication/PR is requested for this unfinished checkpoint.
