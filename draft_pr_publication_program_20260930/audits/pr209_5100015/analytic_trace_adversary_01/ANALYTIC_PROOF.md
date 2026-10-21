# Analytic derivation and adversarial trace audit

## Scope and independent route

The sealed plan and initial derivation predate source inspection. The initial parametrization used x=+a sn(u); the following uses x=-a sn(u), matching the manuscript. This reflection reverses both signed areas and preserves their product. Nothing here identifies an unsigned lobe area or reorders vertices.

The derivation below supplies a universal mathematical argument. CHECK_RESULTS.json supplies finite exact and arbitrary-precision diagnostics, not a substitute for that argument. The special-function inputs are the ordinary Jacobi addition, real/imaginary period, pole, and quarter-period formulas. No numerical pole cancellation is assumed.

## 1. Geometric reduction without assuming the invariant

For the fixed strict confocal pair set

k²=(a²-b²)/(a²-lambda), k'²=(b²-lambda)/(a²-lambda),
K=K(k), K'=K(k'), and choose the unique v in (0,K) with sn²(v)=lambda/b².

Then a/b=dn(v)/k', alpha=a cn(v)/dn(v), and beta=b cn(v). Put

P(z)=(-a sn(z),b cn(z)), B(z)=(-alpha sn(z),beta cn(z)).

Direct addition shows that P(z-v) and P(z+v) lie on the line

-sn(z) X/alpha + cn(z) Y/beta =1,

which is tangent to C at B(z). The same calculation with z=u+v and z=u-v gives the two tangents from any P(u). Thus successive caustic-tangent chords are exactly the fixed shifts +/-2v. For a consistent billiard orientation use +2v. The difference of endpoints and the identity a/b=dn(v)/k' give the forward unit chord velocity at midpoint phase z as

e(z)=(-cn(z)/dn(z),-k' sn(z)/dn(z)).

Equivalently diag(a,b)e(z)=P(z+K). The difference of incoming and outgoing velocities is normal to E (also follows from the foot identity below), and their norms are one. This verifies reflection rather than merely constructing a Poncelet polygon. Since (sn,cn) is one-to-one modulo its real period 4K, primitive closure means 2Nv=4K tau with gcd(tau,N)=1. Reversal chooses 0<tau<N/2. This also explains why the torsion model covers the geometric hypothesis.

Put f(t)=sn(t)cn(t)/dn(t) and T(u)=sum_(j=0)^(N-1)dn(u+2jv). Jacobi addition gives for H(z)=(-A sn(z),B cn(z)):

det(H(z-t),H(z+t))
 =2AB sn(t)cn(t)dn(z)/(1-k²sn²(z)sn²(t))
 =AB f(t)[dn(z-t)+dn(z+t)].

Consequently signed shoelace area of P is ab f(v)T(u). Expanding the determinant for E_j=P_(j+1)-P_j gives

Area(E)=2 Area(P)-1/2 sum_j det(P_j,P_(j+2))
       =ab[2f(v)-f(2v)]T(u).

The second equality is a sum identity. It never assumes that stepping by two makes one primitive cycle.

The intersection of boundary tangents at P(z-v),P(z+v) is

R(z)=(-a dn(v)sn(z)/cn(v), b cn(z)/cn(v)).

Solving the two tangent equations directly proves this, independently of conic-polarity terminology. Hence

A_R(u)=a²b² f(v)T(u+v)/(alpha beta).                         (R)

The actual orthogonal center foot on the tangent at P(z) is

Q(z)=(-a b² sn(z),a² b cn(z))/[a²-(a²-b²)sn²(z)].

Write w=K-v. Then cn(w)=k' sn(v)/dn(v)>0 and dn(w)=b/a. Addition plus P(z-2K)=-P(z) gives the pointwise identity

Q(z)=L[P(z+K-v)-P(z+K+v)],
L=diag(b/a,1)/(2cn(w)), det L=b/[4a cn²(w)].

This is the actual foot, not a caustic contact or a chord foot. Taking signed areas of this edge-vector polygon yields

A_Q(u)=b²[2f(v)-f(2v)]T(u+K-v)/[4cn²(K-v)].                (Q)

It also verifies reflection explicitly: e(u-v)-e(u+v)=2J Q(u), where J=sn(v)/a=sqrt(lambda)/(ab). Since Q is parallel to the ellipse normal, the two unit chord velocities obey the specular law.

All real denominators are safe: dn(t)>0 for real t, cn(v)>0, cn(K-v)>0, and a²-(a²-b²)sn²(z)>=b²>0. Distinct endpoint tangents cannot be parallel because antipodal endpoints would give a center-crossing chord, which cannot touch the proper inner ellipse. No polygon area has been divided out. Real orientation also shows each consecutive determinant of the center-foot polygon is positive: the normal direction is a continuous strictly turning antipodal map and 0<2v<2K. Thus its phase coefficient cannot vanish. Stars retain their original index order.

Complex phases require real scrutiny. Individual feet have genuine poles where 1-k²sn²(z)sn²(w)=0, namely translates of iK'+/-w; the original sn/cn poles cancel in the rational foot expression. Adjacent-foot determinants can initially display apparent higher-order terms. The exact pointwise edge identity and determinant expansion above remove those terms algebraically, reducing the complete areas to the two dn traces (R),(Q). They do not assert that the individual coordinates are everywhere holomorphic. The trace proof below checks every remaining complex pole and supplies the complementary zeros.

## 2. Universal odd trace argument and its exact constant

Let q be odd, H={2Kj/q mod 2K}, and U(z)=sum_(h in H)dn(z+h). The poles of dn are simple at iK'+2mK+2n iK', with residue -i at iK'. It has real period 2K, imaginary period 4iK', and imaginary antiperiod 2iK'. Distinct h give distinct poles modulo this lattice, so the residues of U do not secretly cancel.

Let c=K+iK'. Evenness and the real/imaginary half-period relations imply

dn(c+t)=-dn(c-t).

Because q is odd, K is not in H, so none of the terms U(c) is a pole. Pairing h with -h proves U(c)=0, including the self-paired term h=0. Subgroup periodicity and imaginary antiperiodicity therefore give U(p+K)=0 at every possible pole p of U.

At such p, the simple pole of U is multiplied by a holomorphic zero of U(z+K); the singularity is removable. At a possible pole p-K of the second factor, U(p-K)=U(p+K)=0 by real 2K periodicity. These exhaust all potential singularities. Thus U(z)U(z+K) is entire elliptic and is constant. U is positive on the real axis, so the constant is nonzero. This is a complete pole audit, not just a check at one phase. In a reduced real period 2K/q the trace has exactly two simple poles and complementary zeros; the two factors have disjoint pole sets.

For the manuscript's explicit normalization define

C_q=product_(j=1)^((q-1)/2) cs²(2Kj/q), V(z)=product_(h in H)dn(z+h).

All factors in C_q are finite and positive. At iK',

Res(V)/Res(U)=(-i)^(q-1) product_(j=1)^(q-1)cs(2Kj/q)=C_q,

where dn(iK'+t)=-i cs(t) and cs(2K-t)=-cs(t). Pairing the q-1 terms supplies the two cancelling signs. Odd q also ensures all other factors of V are finite and nonzero at that pole. Subgroup translation gives the same residue ratio at every pole. Therefore V-C_q U is entire elliptic and constant. Both V and U are antiperiodic under 2iK', forcing that constant to zero. Finally dn(t+K)=k'/dn(t) yields

U(z)U(z+K)=(k')^q/C_q².                                  (T)

This validates the exact factor rather than merely proving an unspecified constant. The argument agrees with the manuscript's classical product-to-sum reproof; no claim of a new identity is made.

## 3. Parity, stars, and the area product

For primitive N and winding tau, the shifts 2jv modulo the dn period 2K exhaust H exactly r times, where q=N/gcd(N,2), r=N/q. Thus T=r U. The condition N not divisible by 4 is exactly q odd. Cyclic reindexing gives T(u+K-v)=T(u+K+v). Multiplication of (R),(Q),(T) now proves

A_R A_Q = [a² b⁴ f(v)(2f(v)-f(2v))/(4alpha beta cn²(K-v))]
          * r²(k')^q/C_q²,

independent of phase. All factors have the manuscript's units: the bracket has dimension length^4 and the trace constant is dimensionless. Coprime stars only permute H and do not change any sum argument. Reversal changes both area signs. A fixed d-fold displayed traversal repeats each shoelace sum d times and multiplies the product by d².

For even q, K belongs to H, so U(z+K)=U(z). Since every trace pole has a nonzero residue, U(z)² has a genuine double pole and is nonconstant. Thus the odd-order pole mechanism cannot be continued through the excluded parity. The manuscript's exact N=4 boundary example has E:x²/4+y²=1 and common lambda=4/5: the axis diamond has (A_R,A_Q)=(8,4), while the indicated billiard rectangle has (10,5), yielding 32 versus 50. The independent checker proves exact incidence, reflection, common-caustic tangency, and these areas.

## 4. Limits and residual scope

In the circular limit k->0 with radius rho and v->pi tau/N, direct regular-star geometry gives A_R=N rho² tan(v), A_Q=N rho² sin(v)cos(v), product N²rho⁴sin²(v). The manuscript coefficient tends to rho⁴sin²(v), while T tends to N, agreeing exactly. This checks scale and factors independently. Approaching v=K causes loss of a proper nonantipodal chord; approaching lambda=b² collapses the caustic minor axis. The proof does not take either boundary as an admissible member or divide through a vanishing boundary quantity.

No internal mathematical gap was found in this approach family for the exact stated strict-ellipse claim. Standard Jacobi-function theory is used as stated; no formal verification or interval enclosure of the numerical controls is claimed. This audit does not certify literature completeness, historical independence, novelty, human review, whole-package integrity, or publication readiness.
