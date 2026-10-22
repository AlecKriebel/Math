# Independent analytic reconstruction, before candidate intake

Recorded 2026-10-16, after frozen plan; candidate PROOF.md and all previous reports remain unread at this checkpoint. This is a mathematical derivation, not a novelty claim.

## 1. Source scope and notation

RGK arXiv:2004.12497v11, page 3 equation (1), explicitly uses signed shoelace areas. Section 3.3 page 4 defines feet from M to sides of the trajectory. Table 3 page 6, row k203,a, gives A Am, N congruent 0 modulo 4, all M, unknown value and unknown proof. The distinct journal article (Arnold Math. J. 7 (2021), 341-355, DOI 10.1007/s40598-021-00174-y), pages 343, 344, 346, has the same convention, definition and row. Neither row literally says least period. For this audit N means least period, as required in the frozen hypothesis. Repeated lists are treated separately below.

Set alpha=sqrt(a^2-lambda), beta=sqrt(b^2-lambda), 0<lambda<b^2, and c^2=a^2-b^2=alpha^2-beta^2. Write k=c/alpha in (0,1), k'=beta/alpha, m=k^2. K=K(k), K'=K(k'). Jacobi functions below use modulus k (software parameter m). Put s=sn, c0=cn, d=dn. All complex dot products are bilinear, not Hermitian.

The Stachel journal PDF, Theorem 4.3 pp1614-1615, gives P(u)=(-a sn u,b cn u) and half-step h satisfying cn h=beta/b, with h=2K tau/N. Page1613 incorrectly prints dn(u+2jK)=(-1)^j dn(u). The correct identity is dn(u+2jK)=dn(u). This error is not adopted here. Chavez-Caliz Theorems3/6 concern the polygon formed by tangents to the OUTER ellipse at vertices, not the requested pedal. No Chavez area theorem is used below.

## 2. Derivation of the Jacobi mechanism and billiard map

The ODE s'=c0 d, c0'=-s d, d'=-m s c0 with initial values (0,1,1) implies c0^2+s^2=1 and d^2+m s^2=1. Integration along the real axis gives K=integral_0^1 [(1-t^2)(1-mt^2)]^(-1/2)dt; s(K)=1,c0(K)=0,d(K)=k'. Analytic uniqueness applied to the ODE gives the addition formulas:

sn(u+v)=(s_u c_v d_v+s_v c_u d_u)/D,
cn(u+v)=(c_u c_v-s_u d_u s_v d_v)/D,
dn(u+v)=(d_u d_v-m s_u c_u s_v c_v)/D,
where D=1-m s_u^2 s_v^2.

Indeed differentiating the three displayed rational expressions in u gives the same ODE and their u=0 values are (s_v,c_v,d_v); hence uniqueness proves the formulas wherever defined and meromorphic continuation proves them globally. In particular the K shift is (c0/d,-k' s/d,k'/d), and its square is (-s,-c0,d). There is no real sign change of dn at 2K.

Imaginary transformation follows by the same ODE check:
sn(iz,k)=i sn(z,k')/cn(z,k'), cn(iz,k)=1/cn(z,k'), dn(iz,k)=dn(z,k')/cn(z,k').
As z approaches K', cn(z,k') has a simple zero, yielding the common simple pole at iK'. Applying the addition formulas there gives

sn(iK'+z)=1/(k sn z),
cn(iK'+z)=-i dn z/(k sn z),
dn(iK'+z)=-i cn z/sn z.

Thus a 2iK' shift acts as (s,-c0,-d), and 4iK' is a common period. Their common pole set is 2rK+(2l+1)iK'. The zeros of dn are (2r+1)K+(2l+1)iK', all simple. These exhaust the divisors on the standard Jacobi torus; alternatively this is the standard meromorphic continuation of the inverse integral. The divisor/period inventory is independently cross-checked against NIST DLMF22.4 Tables1-3, https://dlmf.nist.gov/22.4 . No quarter-period branch is inferred from a real square root in the complex plane.

Define h in (0,K) uniquely by cn h=beta/b. Then
sn^2 h=lambda/b^2,
dn h=a beta/(b alpha),
alpha=a cn h/dn h, beta=b cn h.
The identity for dn follows from 1-m lambda/b^2=a^2 beta^2/(b^2 alpha^2). Hence no negative axis or branch is used.

For any v, the line through P(v-h) and P(v+h) is

n(v).X=1, n(v)=(-sn v/alpha,cn v/beta).

To check, substitute addition formulas and alpha=a q/r,beta=b q, where p=sn h,q=cn h,r=dn h. For P(v+h), the dot product is [r s_v sn(v+h)+c_v cn(v+h)]/q. The cross terms cancel and the remaining numerator is q(s_v^2 r^2+c_v^2)=q(1-mp^2s_v^2), equal to the addition denominator times q. The minus sign case is identical. The contact point (-alpha sn v,beta cn v) lies on this line and its caustic normal is n(v), so it is a genuine caustic tangent.

These are billiard chords for the confocal ellipses. For an elementary reflection check, let W=diag(a^-2,b^-2)P and let e be a unit vector along either caustic tangent through P. Its distance/tangency equation, or the discriminant of X=P+t e in the caustic, gives (W.e)^2=lambda/(a^2 b^2). Thus the two inward/outward directions have equal normal components in absolute value and opposite signs at reflection, which is the specular law. A fuller direct discriminant calculation can use adj(diag(alpha^-2,beta^-2)) and P on the outer ellipse. Consequently the caustic-preserving billiard step is u -> u+delta, delta=2h, or its inverse. The real parametrization is one-to-one modulo4K, so least-period closure is delta=4K tau/N, gcd(tau,N)=1. Take 0<tau<N/2 for one orientation; reversal supplies the other. All such stars are covered by exactly the same formulas.

## 3. Exact arbitrary-point pedal expansion

Let n_i=n(u+h+i delta). Set D_i=n_i.n_i=dn^2(u+h+i delta)/beta^2 and R_i=n_i/D_i. The actual foot from fixed M to the full side line is

Q_i=M+(1-n_i.M)R_i.

This follows by solving n_i.Q_i=1 with Q_i-M parallel to n_i. In particular
R(v)=(-beta^2 sn v/(alpha dn^2 v), beta cn v/dn^2 v).
All real denominators are positive. Translation invariance of signed area gives

B_M=1/2 sum_i (1-n_i.M)(1-n_{i+1}.M) det(R_i,R_{i+1}).

For even primitive N, tau is odd and the i+N/2 normals and R vectors are their negatives. Opposite terms cancel every linear coefficient in M. The quadratic term of any real polygon of unit side normals e_i=(cos phi_i,sin phi_i) has coefficient

1/2 sum det(e_i,e_{i+1})(M.e_i)(M.e_{i+1})
= |M|^2/4 sum det(e_i,e_{i+1})(e_i.e_{i+1}).

Proof: write M=r(cos psi,sin psi), expand the product of cosines. The anisotropic term sums to zero since sin(phi_{i+1}-phi_i) cos(phi_i+phi_{i+1}-2psi)
=[sin(2phi_{i+1}-2psi)-sin(2phi_i-2psi)]/2. This also proves the rational bilinear identity by analytic continuation; no complex square-root normals are required. Therefore

B_M=B_0+|M|^2 C,
C=1/4 sum_i det(n_i,n_{i+1})(n_i.n_{i+1})/(D_i D_{i+1}).

In real angular notation C=(1/8)sum sin(2(phi_{i+1}-phi_i)). This is an identity including self-intersections and signed negative or zero areas.

## 4. Complete pole cancellation

Now N=4n and tau is odd. Define T=4K/N=K/n, delta=tau T. The cyclic traces A,B_0,C are invariant under delta and 2K. Bezout, gcd(tau,2n)=1, makes T a period. They share the nonzero imaginary period4iK'. It suffices to work on the compact quotient C/(T Z+4iK' Z).

### Original area

A(u)=1/2 sum det(P(u+i delta),P(u+(i+1)delta)). Its only possible poles are u=iK',3iK' modulo the quotient lattice. They have order at most one, because no adjacent vertices have simultaneous poles: that would require delta=0 or2K modulo4K, excluded by a nondegenerate elliptical caustic and primitive N>=4. Nonadjacent antipodal poles add finitely many simple principal parts, never increase the order.

Moreover P(2iK'-z)=-P(z), so changing u to 2iK'-u reverses the vertex list up to central inversion and cyclic relabeling. Thus A(2iK'-u)=-A(u). The points T/2+iK' and T/2+3iK' are fixed under this involution on the quotient and are not poles. A vanishes there to order at least one.

For the stronger exact divisor assertion, at u=iK'+z, P(u)=(-a/k,-ib/k)/z+O(z). The immediate neighbors tend to P_+=(-a/(k sn delta),-ib dn delta/(k sn delta)) and P_-=-P_+. The two antipodal singular vertices give total residue
2 i ab(dn delta-1)/(k^2 sn delta), nonzero for 0<delta<2K, 0<k<1. Hence A has two simple poles and consequently precisely the two simple zeros just found. Exact residues are not needed for the invariant itself.

### Pedal area and radial coefficient

At each common Jacobi pole, R=O(z), so it is holomorphic there. Its only poles occur at zeros v0=K+iK' (mod2K,2iK') of dn. Around v0, sn and cn are even analytic functions and dn is odd with simple zero. This follows explicitly from
sn(K+iK'+z)=dn z/(k cn z),
cn(K+iK'+z)=-i k'/(k cn z),
dn(K+iK'+z)=i k' sn z/cn z.
Thus R(v0+z)=R_-2 z^-2+R_0+O(z^2), with NO z^-1 term, and R(v0+delta)=R(v0-delta).

In B_0, the two terms using a singular R_j combine into
1/2 det(R_j,R_{j+1}-R_{j-1}). The difference is O(z), so this has at most a simple pole. There are no adjacent simultaneous R poles, by the same delta exclusion. If several nonadjacent poles occur, this argument applies to each and no product creates a higher pole.

For C, the terms involving n_j with D_j=O(z^2) combine into

1/(4D_j) {det(n_j,n_{j+1})(n_j.n_{j+1})/D_{j+1}
          -det(n_j,n_{j-1})(n_j.n_{j-1})/D_{j-1}}.

At z=0 the adjacent normals agree and their denominators are nonzero, so the braces are O(z). Hence C also has at most simple poles. At common Jacobi poles each rational term has removable singularities: both det(n_j,n_l) and n_j.n_l grow at most as z^-1 while D_j grows as z^-2, with adjacent l regular. All possible poles have now been exhausted.

The location of such pedal poles in u is K+iK'-h-i delta. Because K=nT and h=tau T/2 with tau odd, these are T/2+iK' and T/2+3iK' on the quotient. They are disjoint from the possible poles of A.

The identity n(2iK'-v)=-n(v) likewise holds for R. Under u ->2iK'-u, the side arguments satisfy v_i(2iK'-u)=2iK'-v_{-i-1}(u). Consequently B_0 and C are odd under this involution: orientation is reversed and central inversion preserves each determinant. At u=iK' and3iK' they are holomorphic, since the side half-step is an odd half-integer multiple of T; hence they vanish there.

It follows that A B_0 and A C have no poles anywhere on the compact quotient torus. Each is constant. Therefore, for every finite fixed real M,

A(u) B_M(u) = A B_0 + |M|^2 A C

is independent of phase. The argument never divides by A or B_M and does not posit positive areas. Reversing the actual vertex order negates A and B_M, preserving their product. In the chosen forward orientation, every consecutive real eccentric-angle increment lies in (0,pi) because its chord supports a proper centered caustic; each det(P_i,P_{i+1}) is positive, so A>0 on the real family even for stars.

## 5. Boundary and interpretation checks

The proof applies uniformly for all coprime tau and N=4n in the elliptical-caustic range, including N=4. No generic-parameter assumption is needed. The circle k=0 and degenerate caustic k=1 are excluded by the exact hypothesis; finite nondegenerate limits of the invariant follow from continuity of the real foot/area formulas, but no claim about singular limits is needed. D_i>0 for every real phase, so M may lie on a side, on any zero-pedal-area locus, or arbitrarily far away without invalidating the proof.

If a primitive admissible orbit of length N is repeated r times, both signed shoelace areas multiply by r, so their product multiplies by r^2 and stays invariant. However the printed condition on a displayed list length alone cannot bring an arbitrary primitive 2 mod4 family into the theorem merely by duplicating its list. That stronger reading would need a separate assertion and is not what this frozen audit proves. A numerical nonprimitive stress check is planned.

## 6. Status before candidate intake

The exact frozen hypothesis has an independently reconstructed proof mechanism, subject to writing and running direct checks of formulas, divisors and sign cases. The reconstruction does not rely on the submitted proof, prior verdicts, another PR, or an unpublished sibling checkpoint. It also bypasses the Chavez theorem completely. Next: record numerical checks and then audit every candidate line/dependency.
