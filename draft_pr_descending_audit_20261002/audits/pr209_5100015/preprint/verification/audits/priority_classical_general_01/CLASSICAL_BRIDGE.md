# Explicit classical bridge to the candidate trace and geometry

Written during the independent classical/general audit of frozen PR209, head fd09a95b479f376234835a4494693bb1316c85ec. This is a derivation connecting prior inputs; it does not assert that an earlier paper states or proves the full k303,b theorem. No prior campaign priority report has been read.

## 1. Exact earlier identity, without a modulus transformation

Use parameter notation m=k², K=K(m), k_c=sqrt(1-m). KLS, *Cyclic Identities Involving Jacobi Elliptic Functions. II*, arXiv:math-ph/0207019v1, 15 July 2002, Appendix A p20 Eq.(86) (v2 p19 Eq.(85)), gives, for odd q,

    product_(j=0)^(q-1) dn(z+2Kj/q|m) = C_q U_q(z),
    U_q(z)=sum_(j=0)^(q-1) dn(z+2Kj/q|m),
    C_q=product_(n=1)^((q-1)/2) cs²(2Kn/q|m).

The base point is arbitrary; this is an identity of meromorphic functions, proved via the paper's master-identity framework, not a finite list of q or phase samples. Eq.(86) is its all-factor special case, with q odd because the preceding identity requires odd l and l=q. C_q is finite and positive for 0<m<1, since 0<2Kn/q<K. Empty product for q=1 gives C_1=1 and needs no general theorem.

Apply the standard quarter-period identity dn(t+K|m)=k_c/dn(t|m) to each factor. Multiplication yields the meromorphic identity

    C_q² U_q(z) U_q(z+K) = k_c^q,
    U_q(z) U_q(z+K) = (1-m)^(q/2) / C_q².                 (B1)

This is exactly the submitted odd-order dn trace lemma, with a classical explicit value. An isolated zero or pole in a factor does not invalidate the meromorphic identity; extend across it by continuation. On the real axis every dn is positive. KS, Pramana63 (2004), p931 Eq.(61), restates the product-to-sum formula. Direct publisher PDF access failed in this audit; that precise published equation was read from a retained publisher-text extraction, while the 2002/2003 primary arXiv PDFs are independently authenticated here.

## 2. Independent generalized Landen normalization

KS, Pramana63 (2004), Eqs.(7)–(9), p923, and (54), p930, uses

    eta = 1/U_q(0),
    m_t = (m-2)eta² + 2eta³ sum_j dn³(2Kj/q|m),
    U_q(z) = eta^(-1) dn(z/eta|m_t),
    K(m_t)=K(m)/(q eta).

The same formulas appear with different numbering in the primary arXiv:math-ph/0312074v1 (31 December 2003); these are not new identities of the candidate. For odd q,

    (z+K)/eta = z/eta + q K(m_t).

The real period of dn is 2K(m_t). An odd multiple of K(m_t) therefore produces its quarter-period reciprocal, giving

    U_q(z)U_q(z+K) = eta^(-2) sqrt(1-m_t).                (B2)

The two explicit constants (B1)/(B2) agree. This route must not omit the argument scale eta: shifting z by K does not simply shift the reduced argument by K(m_t). For even q, K/eta is an even multiple of K(m_t), and it instead gives U_q(z+K)=U_q(z), which does not prove the required product constancy. The product-to-sum route (B1) avoids relying on the explanatory ODE range argument in KS.

## 3. Center tangent feet as differences of unit velocities

Let n_i be the outward unit normal at P_i, h_i=P_i dot n_i>0, and e_i=(P_(i+1)-P_i)/|P_(i+1)-P_i|. Let delta_i be the positive reflection angle with the tangent. Reflection gives

    e_(i-1)-e_i = 2 sin(delta_i) n_i.

The Joachimsthal integral in BT is J=sin(delta_i)/h_i, fixed on the caustic family. The actual perpendicular foot from O to the outer tangent at P_i is Q_i=h_i n_i. Thus

    Q_i = [e_(i-1)-e_i]/(2J).                             (B3)

AST Theorem4 proof, p4, already displays e_(i-1)-e_i=2 cos(angle_i/2)P_i*/|P_i*| and J=|P_i*| cos(angle_i/2), which gives this exact relation by the elementary foot formula Q_i=P_i*/|P_i*|². This is also the center-foot telescope mechanism in Bialy–Tabachnikov, *Dan Reznik's identities and more*, arXiv:2001.08469v2, Theorem4.1 proof pp6–7. AST, *Billiards in ellipses revisited*, arXiv:2001.02934v2, Lemma3.1/Remark3.2 p5, identifies S e_i, S=diag(a,b), as the classical skew-hodograph billiard in the original boundary ellipse. AST credits Veselov; this audit does not independently read the 1988/1991 originals and does not claim their exact earlier formula.

One must still connect this transformed billiard to the SAME caustic family and phase. This is checkable in the candidate's accepted canonical coordinates. Put alpha=1 by scale temporarily, beta=k_c, v=2 tau K/N in (0,K), a=dn(v)/cn(v), b=k_c/cn(v), and P(t)=(-a sn(t),b cn(t)). The chord centered at t has direction

    e(t)=(-cn(t)/dn(t), -k_c sn(t)/dn(t)),

because its line is tangent to the caustic at B(t)=(-alpha sn(t),beta cn(t)), and the positive direction follows from v>0. Quarter-period formulas then give

    S e(t)=P(t+K).

Consequently for P_i=P(u+2iv),

    S e_i=P(u+(2i+1)v+K).                                (B4)

This is the same original ellipse and same caustic; no appeal to an unspecified new invariant is needed. Equations (B3)/(B4), cyclic reindexing and J b=cn(K-v) recover exactly submitted Eq.(14), including its fixed diagonal map and sign. They are valid for actual tangent feet, not original-chord feet. Reflection and (B3) also hold after reversing traversal.

## 4. Ordered signed areas and the exact central missing historical step

For any indexed vector polygon X_i,

    area(X_(i+1)-X_i)=2area(X_i)-(1/2)sum_i det(X_i,X_(i+2)).

This is determinant expansion; it never requires a convex/simple polygon. Jacobi addition gives, with f(t)=sn(t)cn(t)/dn(t),

    area(P(u+2iv))=ab f(v) T(u),
    area(P_(i+1)-P_i)=ab[2f(v)-f(2v)]T(u),
    T(u)=sum_(i=0)^(N-1)dn(u+2iv).

Combining with (B3)/(B4) gives the equivalent simpler center-pedal trace

    area(Q)= [2f(v)-f(2v)]/(4J²) T(u+v+K).                (B5)

Polarity with respect to the outer ellipse maps the caustic contact B_i to the intersection R_i of the two endpoint tangents. Hence

    area(R)= a²b²/(alpha beta) f(v) T(u+v).               (B6)

For a primitive winding tau, gcd(tau,N)=1, q=N/gcd(N,2), r=N/q, the shifts modulo 2K exhaust the q-subgroup r times, so T=r U_q. When N is odd or 2 mod4, q is odd; (B1), (B5) and (B6) prove the candidate's all-phase area product with explicit value

    a²b² f(v)[2f(v)-f(2v)] r² k_c^q
    -------------------------------------------------- . (B7)
                  4 alpha beta J² C_q²

This is a checkable route composed from old identities and standard geometry. It does not by itself establish historical anticipation of the target: no earlier source located/read here explicitly assembles (B3)–(B7), states its center outer-pedal product, and handles its exact parity/domain. The substantive historical missing bridge is identification of a prior explicit full target reduction/proof, not the classical status of (B1). The derivation also shows that calling the candidate's pointwise bridge wholly new without discussing BT's telescope and AST's hodograph would be too strong.

Primitive stars work because only gcd and traversal order enter. A repeated admissible primitive orbit repeats each area summand and multiplies the product by the square of repetition count. A listed N not divisible by4 has primitive divisor not divisible by4. The circular case follows independently by rigid rotation; hyperbolic/focal/degenerate caustics are not asserted. J has units length^(-1), making (B7) have area-squared units length^4.

## 5. Independent verification of the cited old product-to-sum identity

For completeness one can verify KLS's exact coefficient without its Fourier derivation. Let V(z)=product_(h in H)dn(z+h), H={2Kj/q}, q odd. V and U are 2K-periodic and 2iK'-antiperiodic. At p=iK', dn has residue -i and dn(p+t)=-i cs(t). All possible poles of either V or U are simple because distinct H shifts have distinct poles modulo 2K. The residue ratio at p is

    Res_p(V)/Res_p(U)
      = (-i)^(q-1) product_(j=1)^(q-1)cs(2Kj/q)
      = product_(j=1)^((q-1)/2)cs²(2Kj/q) = C_q,

using cs(2K-t)=-cs(t). Subgroup periodicity and imaginary antiperiodicity give the same ratio at every possible pole. Hence V-C_q U is entire and elliptic, so constant; its imaginary antiperiod forces that constant to vanish. This validates the exact old identity and its all-phase character independently. It is a reproof of prior mathematics, not a candidate novelty claim.

## 6. The old even original/outer area theorem also implies the lemma

Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*, Theorem6, published pp104–105, proves phase constancy of the ORIGINAL polygon area times its tangent polygon area for even n and concentric ellipses in general position. This is a different pair of polygons from the target R,Q.

Nevertheless, it yields (B1)'s constancy, without its explicit value. For any fixed 0<m<1 and odd q>=3, take a caustic of axes alpha,beta=alpha sqrt(1-m) and construct the AUXILIARY confocal outer ellipse with w=K/q,

    a_aux=alpha dn(w)/cn(w), b_aux=beta/cn(w).

Stachel's canonical theorem gives a primitive 2q-periodic family, tau=1. This is a strict nondegenerate confocal pair. Its complex intersections are four distinct points, so the usual general-position restriction causes no special confocal exception. By the determinant area formula its original area and tangent area are positive nonzero fixed coefficients times

    U_q(z), U_q(z+K/q),

respectively: each full 2q sum is twice the q sum. Since K-K/q=((q-1)/2)*(2K/q), subgroup periodicity gives U_q(z+K/q)=U_q(z+K). The old even area-product theorem therefore proves the candidate lemma for ALL phases, not only an auxiliary finite sample. q=1 follows from the elementary quarter shift. This route is another explicit synthesis of a prior general theorem; it is not a claim that Chavez-Caliz already states the outer-center-pedal theorem.
