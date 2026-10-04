# Author turn 1: an open-map factorization and exact boundary pullback

Status: partial; original common-boundary question remains unresolved. This is
one substantive turn, not a source-resolution claim. Use SOURCE_SCOPE.md for
the exact system and credited earlier results. The proof here is on all of D.

## 1. Isolating the invertible nonlinear feedback step

For |r|≤A≤0.4 put

    h_r(x)=(x+r/4)/(1+rx),   Q_r=P_{h_r}.

These are increasing smooth bijections of I, with inverse h_−r, fixed
endpoints, and

    d h_r/dx=(1−r²/4)/(1+rx)²>0,
    d h_r/dr=(1/4−x²)/(1+rx)²≥0.

Direct substitution gives T_r=T_0 composed with h_r away from the cut.
Consequently, with K(u)=Q_{r(u)}u,

    F=P_0 composed with K.                                      (1)

Each Q_r is a positive L1 isometry, including on signed integrable functions.
The map (r,u)↦Q_r u is jointly continuous: for a fixed continuous density
this follows from the uniform convergence of the inverse diffeomorphisms
and their derivatives; approximation by continuous functions and the
isometry property give the assertion for arbitrary L1 functions.

**Proposition 1.** K is a homeomorphism from D onto D.

For v in D define

    M_v(r)=integral h_−r(x) v(x) dx,
    H_v(r)=r−G(M_v(r)),        −A≤r≤A.

M_v is continuous and nonincreasing. Since G is increasing,
H_v(s)−H_v(r)≥s−r for s>r. Moreover H_v(−A)<0<H_v(A), since |G|<A.
There is a unique root rho(v). The bound |h_−r|≤1/2 and Lip(G)≤B give

    |rho(v)−rho(w)|≤(B/2)||v−w||_1.                            (2)

Indeed |H_v(r)−H_w(r)|≤(B/2)||v−w||_1 uniformly in r, and the previous
strict increase transfers this bound to the roots. Set

    J(v)=Q_−rho(v) v.

The pushforward identity gives phi(J(v))=M_v(rho(v)), so r(J(v))=rho(v)
and K(J(v))=v. Conversely, if v=K(u), its defining root is r(u), so
J(v)=u. Joint strong continuity and (2) imply that J is continuous;
K is continuous by the same joint continuity and continuity of phi and G.
Thus J=K^−1, proving the proposition. No differentiability of K in the
L1 norm has been used or asserted.

## 2. Positive exact sections of the doubling operator

For w in D write v=P_0 w. Up to null sets the inverse branches of T_0 are

    a(y)=(y−1/2)/2,       b(y)=(y+1/2)/2,
    v(y)=[w(a(y))+w(b(y))]/2.

Define q(x)=w(x)/v(T_0 x) when the denominator is positive, and q(x)=1
otherwise. Then 0≤q≤2 a.e. Where v(y)=0 both inverse-branch values of w
vanish, so the second clause gives P_0 q(y)=1 there also. Hence P_0 q=1
almost everywhere. Define a bounded positive linear map on L1 by

    R_w(z)(x)=q(x) z(T_0 x).

It satisfies

    P_0 R_w(z)=z,    R_w(v)=w,    ||R_w(z)||_1=||z||_1.         (3)

For the norm identity use P_0 q=1 and integrate |z|; this also proves
that R_w maps D into D. In particular,

    ||R_w(z)−w||_1=||z−v||_1.                                (4)

Thus P_0 is surjective and open in the relative L1 topology on D: the
image of every relative radius-epsilon ball around w contains the
relative radius-epsilon ball around v.

Combining (1)–(4),

    S_u(z)=K^−1 R_{K(u)}(z)

is a global continuous right inverse of F through u:

    F S_u(z)=z,      S_u(Fu)=u.                              (5)

**Theorem 2.** F:D→D is a continuous open surjection. Every iterate F^n
has a continuous right inverse through each prescribed point of D.
The latter follows by composing the sections along its finite orbit.

## 3. Pulling common boundaries backward

Let B be either stable noncentral basin. It is open, and
F^−1(B)=B, since convergence is unchanged by omitting the first term.
Then

    F^−1(partial_D B)=partial_D B.                            (6)

For one direction, if u is on the boundary then continuity maps points of
B approaching u to B approaching Fu, and complete invariance excludes
Fu in B. For the other, let Fu be on the boundary. Every neighborhood U
of u has F(U) open around Fu, hence meets B. Complete invariance implies
U meets B, whereas u is outside B. This proves (6).

Let C=partial_D B_+ intersect partial_D B_−. It is closed and completely
invariant. Since B_± are disjoint and open, C is contained in W. Credited
Proposition 4 of Bardet–Keller–Zweimüller yields W intersect D' contained
in C. We have therefore proved the full-space partial inclusion

    closure_D [ union_{n≥0} F^−n(W intersect D') ] ⊆ C ⊆ W.   (7)

In particular, every finite preimage of 1 is a common-boundary point.
Every symmetric density is also in C: average it on the symmetric dyadic
partition into 2^n intervals. The averages u_n are symmetric densities,
u_n→u in L1, and P_0^n u_n=1. All preceding iterates remain symmetric,
so their feedback is zero and F^n u_n=P_0^n u_n. Closedness of C proves
the claim. Every density with an eventually symmetric orbit is in C too.
This symmetry corollary is also obtainable from the already credited
density of B_+ union B_− and reflection; no novelty is claimed for it.

## 4. Exact obstruction to finishing by this route

For u in W, F^n u→1. Formula (5) lifts the endpoint 1 backward to a
finite preimage of 1, through n continuous sections depending on the orbit.
It does NOT establish that these n-step lifts tend to u: no uniform modulus
of continuity of the growing section composition has been proved. The
mere convergence of F^n u gives no comparison with that modulus. Likewise,
external linear PFO shadows are not automatically self-consistent orbits.
Neither (7) nor openness proves that its left-hand closure equals W.

Next mechanism: analyze the actual stable functional of the linearized
operator, including its full-L1 behavior, rather than invoking a nonexistent
L1 differentiable stable-manifold theorem. A later argument must still
control nonlinear feedback and arbitrary rough densities.
