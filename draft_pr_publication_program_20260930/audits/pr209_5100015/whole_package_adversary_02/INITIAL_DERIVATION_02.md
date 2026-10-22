# Initial independent derivation and findings 02

UTC: 2026-10-17T01:39:56.433261+00:00
Completion estimate: 25%. Sealed before reading first whole-review report, Root mathematical assessment, or current family reports. Read manuscript and primary-path metadata, and direct Ferudun v1.1 search excerpts only.

## Independent derivation
Let t_j=u+2jv; S=sn,C=cn,D=dn. Direct expansion of det((-a S(z-t),b C(z-t)),(-a S(z+t),b C(z+t))) gives 2ab S(t)C(t)D(z)/(1-k² S(z)² S(t)²). Adding the two dn addition formulas gives 2D(z)D(t)/(1-k² S(z)² S(t)²), proving determinant=ab f(t)(D(z-t)+D(z+t)). This formula is algebraic/meromorphic and valid when cn(2v)=0; it does not divide by f(2v).

An independently expanded edge area is 2 area(P) - (1/2) sum det(P_j,P_{j+2}); the two skipped sums telescope by index reallocation, even if the skipped polygon has multiple cycles. Thus area(edges)=ab(2f(v)-f(2v))T(u).

The two endpoint tangents at P(z-v),P(z+v) intersect at R(z)=(-a² sn(z)/alpha,b² cn(z)/beta): their chord is -sn(z)X/alpha+cn(z)Y/beta=1 and ellipse polarity exchanges that chord with R. Hence area(R)=a²b²/(alpha beta) f(v)T(u+v).

Independently projecting O onto n(z).X=1 gives Q=n/(n.n), with n=(-sn/a,cn/b). Its denominator is a²-(a²-b²)sn²>=(b²)>0 on the real axis. For w=K-v, dn(w)=b/a and cn(w)>0. Since a²-b²=alpha²-beta² and sn(w)=cn(v)/dn(v), the sum P(z+w)+P(z-w) has exactly that denominator/a². Scaling by diag(b/a,1)/(2cn(w)) gives Q. As P(z+K+v)=-P(z-w), this is a backwards edge in the shifted phase, with a fixed positive determinant b/(4a cn(w)²). Reversing every vector has determinant +1 in 2D. Area(Q)=b²(2f(v)-f(2v))T(u+K-v)/(4cn(w)²).

For primitive orbit 2v=4tau K/N. Modulo dn's real period 2K, the shifts give q=N/gcd(N,2) distinct points, each repeated r=gcd(N,2) times because gcd(tau,N)=1. Exactly the admitted parity gives q odd. Reindexing T by 2v equates T(u+K-v) to T(u+K+v). Thus the product is coefficient times r²U_q(u+v)U_q(u+v+K).

Independent global proof: dn has periods 2K,4iK' and changes sign on 2iK'. U_q and V=product of q shifted dn have the same real subgroup period 2K/q and, for odd q, imaginary antiperiod 2iK'. Poles are distinct/simple because shifts in the order-q real subgroup are distinct modulo 2K. At iK' the residue quotient equals (-i)^(q-1) product_{j=1}^{q-1} cs(2Kj/q). Pairing j with q-j gives product of positive cs²(2Kj/q), since both the pair-sign and (-i)^(q-1) contribute (-1)^((q-1)/2). Odd q avoids sn=0 and cn=0 in those factors, so C_q finite/nonzero. Translation covers all poles, including those shifted by 2iK'. V-C_qU_q is entire with 2K and 4iK' periods, hence bounded/constant, and antiperiodicity forces zero. Multiplication by its K translate uses dn(z)dn(z+K)=k'; equality holds meromorphically without illicit multiplication of pointwise pole values. This proves U_q(z)U_q(z+K)=(k')^q/C_q². Restrict to real z only after the identity, where all dn terms are positive.

## Boundary and failure search
No hidden division by either polygon area occurs. 0<k<1 follows strict elliptic caustic and a>b; v in (0,K) makes cn(v),cn(K-v)>0. Real chord intersections are finite because parallel boundary tangents have antipodal contact points; their connecting chord passes through O and intersects a proper centered ellipse rather than touching it. N=1,2 cannot meet strict elliptic-caustic billiard conditions. N divisible by 4 implies q even, and the trace lemma cannot be applied. A listed d-repeat multiplies each signed area by d; if listed dN is not divisible by 4 then N is not either. Opposite orientation negates each area; product unchanged. Stars must keep trajectory order. The coefficient's length degree is 2+4-1-1=4. The circular limit requires separate treatment because k=0 is outside the lemma but rotation symmetry suffices. Focal, collapsed and hyperbolic caustics remain outside scope. Complex denominators may vanish; the proof uses meromorphic identities and pole removal rather than a claim of global nonvanishing.

## Initial findings
No mathematical defect found in this derivation. This is an initial result, not completed package clearance. The attribution hypothesis remains to be checked directly against complete relevant primary passages. Ferudun primary excerpts already explicitly state the exact all-traversal centered theorem, so novelty or firstness cannot be inferred. Need own numerical geometry/reflection/common-caustic checks and explicit four-period obstruction checks; inspect package integrity, source harness, PDF, source dependencies, custody and provider evidence next.
