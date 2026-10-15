# Independent all-period meromorphic derivation for k404

This derivation was developed after reading the submitted theorem and full proof, before reading any author checker or prior/new reviewer report. The algebra and Laurent coefficients are independently recomputed in fresh_meromorphic_checks.py. Finite numerical controls are supplemental, not the proof.

## Exact claim and admissible domain

The outer ellipse and its strictly nested confocal elliptical caustic are noncircular and nondegenerate. Rescale the caustic major semiaxis to one. Its minor semiaxis is b0=sqrt(1-k²), with 0<k<1. For a primitive periodic billiard, choose the positive turning orientation and let the canonical step be delta=4K tau/N, with gcd(tau,N)=1 and 0<tau<N/2. The target has N=2m with m odd, so N>=6, tau odd, and gcd(tau,m)=1. Set v=delta/2, t=sn(v), C=cn(v), D=dn(v). Then 0<v<K and t,C,D are strictly positive. The outer semiaxes are a=D/C and b=b0/C; its two foci are (+/-k,0).

The original vertices are P(w+j delta)=(-a sn(w+j delta),b cn(w+j delta)). The antipedal vertices are the actual intersections of the lines through consecutive original vertices orthogonal to their respective focal rays. The pedal vertices are the actual feet from the focus to original side lines. The asserted areas are signed shoelace areas in the prescribed order.

The canonical parametrization is credited to Stachel. It is also directly consistent with confocality: a²-b²=k², and a²-1=b²-b0²=b0²t²/C²>0. The addition formulas show each chord through P(u-v),P(u+v) has caustic tangent equation (-sn u,cn u/b0) dot X=1.

## Direct rational construction and real finiteness

Put s=sn u,c=cn u,d=dn u and L=1-k²t²s². Addition gives

    sn(u +/- v)=(sCD +/- tcd)/L,
    cn(u +/- v)=(cC -/+ sdtD)/L.

Solving the two bilinear line equations yields the submitted U(u):

    Ux=-(E s+k(C²-D²s²))/(C²L),
    Uy=c[2b0²-E(1+ks)]/(b0C²L),
    E=1-2k²t²+k²t⁴.

An independent exact polynomial reduction checks both defining line equations, the chord-tangency equations, and the determinant

    det(P(u-v)-F,P(u+v)-F)=2b0Dt d(1+ks)/(CL).

For real u, d>0, 1+ks>=1-k>0, L>=1-k²t²>0, and all constant factors are positive. Hence every real intersection exists uniquely and is finite. This includes star trajectories.

## Correct lattices: a divisor is not itself a function character

The elementary periods/characters are:

    sn(u+2K)=-sn u,       sn(u+2iK')=sn u,
    cn(u+2K)=-cn u,       cn(u+2iK')=-cn u,
    dn(u+2K)=dn u,        dn(u+2iK')=-dn u.

These follow from NIST DLMF §22.4, Tables 22.4.1–3. In particular dn does NOT change sign under 2K. A printed conflicting line in Stachel is not used.

The scalar L is elliptic on the lattice <2K,2iK'>. U itself need not descend to that lattice. Pole counting L there is nonetheless valid. sn² has one double pole there, so L has exactly two zeros counted with multiplicity. The imaginary-shift chart sn(iK'+x)=1/(k sn x) places those zeros at iK'+/-v. They are distinct because 0<v<K, and simple because sn'(+/-v)=CD!=0 and t!=0. They have no hidden zeros at Jacobi poles; L has poles there. The common simple poles of sn,cn,dn in U are removable since both numerators and L have order at most/exactly two. Thus U has only the stated at-most-simple poles.

For the full antipedal area B(w), U_j(w)=U(w+v+j delta), so all potential poles occur at iK'-j delta modulo <2K,2iK'>. The two endpoint lists coincide by cyclic index shift.

Every cyclic area is invariant under w->w+delta. Because m delta=2K tau with tau odd, the original vertex list at w+2K is exactly the cyclic shift by m. It follows that the area also has period 2K. Bezout for gcd(tau,m)=1 gives h=2K/m as a period. This reasoning concerns complete cyclic sums, and does not incorrectly give U or an individual pedal vertex that period.

The correct full torus for the area is Gamma=<h,4iK'>. On Gamma the possible antipedal area poles are only p=iK' and p+2iK'. The vertical anti-period is a nontrivial character, not a period until doubled.

## Independent local cancellation of the antipedal double poles

Use X=sn x,Z=dn x in the chart u=iK'+x. Then

    Ux=-(E X/k+kC²X²-D²/k)/(C²(X²-t²)),
    Uy=-i Z[(2b0²-E)X-E]/(k b0 C²(X²-t²)).

This rationalization is independently certified. Let R+ and R- be the residue vectors at x=+v and x=-v, respectively. At the corresponding +2K translates, X and X' negate while Z is unchanged. Direct substitution gives

    Res(U at iK'+v+2K)=-R-,
    Res(U at iK'-v+2K)=-R+.

At w=p the singular U vertices for the requested N>=6 are j=0,N-1,m,m-1. The only edges containing two singular vertices are (N-1,0) and (m-1,m); their double Laurent coefficients, including the common half-area factor, sum to

    [det(R-,R+)+det(-R+,-R-)]/2=0.

The other edges have at most one simple-pole vertex. No unexamined central factor is needed for this cancellation. The exact certificate verifies the residues and determinant cancellation as rational identities. This independently establishes the at-most-simple area poles for the required parity, without merely invoking the manuscript's oddness argument.

The manuscript's global oddness argument is also correct: y-reflection together with reversal gives B(-w)=B(w), after equality of the two focus areas by central relabeling. The 2iK' shift reflects in the x-axis with order unchanged, so B(w+2iK')=-B(w). Consequently B(p+z)=-B(p-z), eliminating all even Laurent powers. It handles all admissible even primitive periods and any possible extra adjacent coincidences in the period-four specialization.

## The comparison trace and a fully justified uniqueness step

Define S(w)=sum(j=0..N-1) dn(w+j delta). It has real periods delta and 2K, hence h, and imaginary anti-period 2iK'. The only poles on Gamma are p and p+2iK', both simple. Near p, dn(p+z)=-i cn z/sn z=-i/z+O(z). Exactly j=0 and j=m of the original sum have poles at p: the necessary congruence j tau=0 mod m has those two solutions in 0<=j<N. dn's real 2K period makes their residues equal. Therefore

    Res_p S=-2i != 0.

The residue at the vertical translate is +2i. Matching B's first residue with b times S automatically matches the other by the shared anti-period. B-bS is holomorphic on the compact torus, hence constant. Its anti-period forces the constant to be zero. Thus B(w)=bS(w), without assuming b!=0. Reality at real w makes b real. The cyclic central symmetry makes the same b apply to both original foci.

This argument uses both the pole divisor and the character. Merely having at most two poles would not by itself remove an additive constant.

## Independent pedal Laurent chart and explicit trace coefficient

The actual foot from F+=(k,0) to the caustic tangent is

    q(u)=((k-sn u)/(1-k sn u), b0 cn u/(1-k sn u)).

The exact checker independently verifies both the line equation and that q-F is parallel to the tangent normal. On a full real period 4K, the F+ denominator has its double zero at r=K+iK'; its 2K translate has sn=-1/k and is regular. The common sn/cn poles are removable. Quarter-period identities give the exact chart

    qx(r+x)=(k²cn x-dn x)/(k(cn x-dn x)),
    qy(r+x)=-i b0²/(k(cn x-dn x)).

This chart is even in x. Its leading Laurent term, recomputed from the Jacobi ODE, is

    q(r+x)=(2/k)(1,i)x^(-2)+O(1),

with no x^(-1) term. Since 0<delta<2K, both neighbors are regular. Their difference q(r+x+delta)-q(r+x-delta) is odd in x and starts with 2q'(r+delta)x. The two incident area terms therefore have at most a simple pole. On the full real 4K period only one vertex in the primitive cyclic sum is singular at r; this prevents hidden products between nonadjacent singular vertices.

The pedal cyclic sum T(u) has period h and imaginary anti-period 2iK'. Its possible pole divisor on Gamma is exactly that of S(u+K): r and r+2iK'. At r, S(u+K) has residue -2i. Thus the same compact-torus argument gives T(u)=p0 S(u+K).

A further independent check computes p0 explicitly. Write s_delta=sn delta,c_delta=cn delta,d_delta=dn delta. Differentiating the quarter-period chart gives

    qx'(r+delta)=-b0^4 s_delta/[k(c_delta-d_delta)^2],
    qy'(r+delta)=-i b0² s_delta(d_delta-k²c_delta)/
                 [k(c_delta-d_delta)^2].

The residue of the incident half-area is (2/k)det((1,i),q'(r+delta)). Dividing by -2i yields

    p0 = b0² s_delta(d_delta-k²c_delta-b0²)/
         [k²(c_delta-d_delta)^2].                 (A)

All these derivative/residue equalities are independently exact-certified. Formula (A) is an audit certificate, not a novelty claim.

In fact p0>0 for every strict allowed step: s_delta>0 and c_delta<1. The identity

    d_delta²-(k²c_delta+b0²)²
        = k²b0²(1-c_delta)²>0

implies d_delta>|k²c_delta+b0²|, hence d_delta-k²c_delta-b0²>0. Also d_delta>c_delta, so the denominator in (A) is nonzero. This provides an analytic denominator proof independent of the manuscript's lifted-normal geometric proof. The latter is separately correct because det(n,n')=dn/b0>0, the half-turn takes exactly 2K, and 0<delta<2K makes every relative pedal determinant positive.

## Exact parity, completed ratio, and limits

The original side pedal parameter is u=w+v. For N=2m with m,tau odd,

    K+v=((m+tau)/2)h

is an integer multiple of the actual area period. Therefore A_F(w)=T(w+v)=p0S(w). Since S(w)>0 on the real axis, A_F(w)>0, and

    A_F*(w)/A_F(w)=b/p0

is defined and constant throughout the real family. Neither numerator positivity nor b!=0 is required. Both foci give the same constant. Reversal negates both signed areas; repeated admissible primitive orbits scale both equally.

If m is even (primitive N divisible by four), K+v is a half-integer multiple of h instead. The phase alignment above then fails; it cannot be extended by deleting the requested parity or padding a different primitive orbit with repetitions. The proof has no circular or degenerate-caustic limiting claim. The boundaries k=0,k=1,v=0,v=K are excluded precisely where one or more chart hypotheses change.

## Primary identity references

- [NIST DLMF §22.4](https://dlmf.nist.gov/22.4), Tables 22.4.1–3: periods, pole/zero locations, and quarter-period charts.
- [NIST DLMF §22.8](https://dlmf.nist.gov/22.8), equations 22.8.1–3: Jacobi addition formulas.
- [Stachel, arXiv:2105.03624](https://arxiv.org/abs/2105.03624), canonical parametrization and rational rotation step; the final journal edition is the version cited by the submitted proof. The real 2K period of dn is checked independently against DLMF.
