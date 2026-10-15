# Author turn 3: backward feedback transport closes the common-boundary gap

Candidate complete answer for the exact report parameters. Three substantive
author turns have been used. This frozen candidate requires independent audit
before a final disposition. No historical-priority claim is made.

## Theorem and credited inputs

Let I=[−1/2,1/2], D be its probability densities with the relative L1 topology,
G(m)=A tanh(Bm/A), 0<A≤2/5 and 6<B≤16. Let

    f_r(x)=((r+4)x+r+1)/(2rx+2),
    T_r(x)=f_r(x) mod I,     r(u)=G(integral x u(x) dx),
    F(u)=P_{T_{r(u)}}u.

Let B_± be the basins of the two noncentral fixed densities and
W={u in D:F^n u→1 in L1}. Then

    W=partial_D B_+=partial_D B_−.                          (T)

The existence, global convergence and openness assertions for these three
basins, and the fact that 1 is in both noncentral basin boundaries, are
credited to Bardet–Keller–Zweimüller, *Stochastically stable globally coupled
maps with bistable thermodynamic limit*, CMP 292 (2009), 237–270; the full
inspected primary proof is arXiv:0812.4040v1, Theorem 2 and Propositions 3–4.
The exact question and parameter range are Keller's OWR49/2009, pp.2714–2715.

Turn 1 proves on all D that F is continuous and open, and each basin
boundary is completely invariant. It therefore suffices to prove

    W ⊆ closure_D [ union_{n≥0} F^−n({1}) ].                (A)

The reverse inclusion also holds because W is closed and contains every
such preimage, so (A) is an exact density description of the central basin.
The linearized analysis in turn 2 is not a dependency of the proof below.

The essential new use of the source is its dimension-independent inverse
expansion mechanism (§3, Lemma 4). We give its probability-space version
and an exact rational parameter certificate here, rather than relying on
the source's numerical estimate or invoking an L1 stable-manifold theorem.

## 1. A uniformly contracting inverse on random variables

Write b_r=f_r^−1, mapping J=[−1/2,3/2] onto I. Direct calculation gives

    b_r(z)=(2z−r−1)/(r+4−2rz),
    f_r'(x)=(4−r²)/(2(1+rx)²),
    partial_r b_r(z)=−(1−4 b_r(z)²)/(4−r²).                (1)

On any probability space, for any bounded random variable Z valued in J,
there is a unique number r solving

    r=G(E b_r(Z)).                                        (2)

Indeed b_r(z) is nonincreasing in r, and the function r−G(E b_r(Z))
increases by at least the increase in r and has opposite signs at ±A.
Define the inverse feedback operator

    V(Z)=b_r(Z),   with r determined by (2).

It takes J-valued random variables to I-valued ones. For any two such
variables on the same probability space,

    ||V(Z)−V(Z')||_2 ≤ kappa ||Z−Z'||_2,
    where kappa=24/25<1.                                  (3)

The probability space and any later branch labels are arbitrary.

### Proof of (3)

Interpolate Z_s=(1−s)Z+sZ'. Let X_s=V(Z_s), r_s=G(E X_s),
g_s=G'(E X_s), q_s=1−4X_s², and beta_s=g_s/(4−r_s²). All variables are
bounded. The scalar implicit function theorem applies to (2), whose
r-derivative is at least 1. Differentiation in s is justified by bounded
smooth derivatives of b on the compact parameter/variable rectangle.
This is differentiation along a bounded path, not a claim of Fréchet
smoothness of a Nemytskii map on L2.

With D_s multiplication by f_{r_s}'(X_s), differentiation yields

    (Id+beta_s q_s E) dot X_s=D_s^−1 dot Z_s,
    dot X_s=[Id−beta_s q_s E/(1+beta_s E q_s)]D_s^−1 dot Z_s.  (4)

Here q E denotes the rank-one operator v↦q E(v). Since 0≤q≤1, on any
real probability-space L2 the bracket in (4) satisfies

    ||Id−beta q E/(1+beta E q)||²
       ≤ 1+9 sqrt(beta)/(16 sqrt(3))+beta/4.               (5)

For completeness, write a vector, after rescaling, as q−p with
<p,q>=0. Put v=||q||²≤E q and t=||p||. Its transformed squared norm is

    v[(1+beta E p)/(1+beta E q)]²+t²
       ≤ v(1+beta t)²/(1+beta v)²+t².

The first term after expansion is at most v. The cross term is at most

    [beta sqrt(v)/(1+beta v)²](v+t²),

and the last term is at most (beta/4)t². The maxima over v≥0 are
9 sqrt(beta)/(16 sqrt(3)) and beta/4, respectively. This proves (5).
Vectors perpendicular to q follow by a limit; q=0 and beta=0 are immediate.

Put a=|r_s|. The feedback identity gives

    0≤g_s=B(1−r_s²/A²)≤16−100a²,
    beta_s≤beta(a):=(16−100a²)/(4−a²),    0≤a≤2/5.

Also ||D_s^−1||≤(2+a)/[2(2−a)]. Since 9/(16 sqrt(3))<1/3, (4)–(5) imply

    ||dot X_s||² ≤ U(a)||dot Z_s||²,
    U(a)=(2+a)²/[4(2−a)²] · [1+sqrt(beta(a))/3+beta(a)/4].   (6)

The rational certificate described just below proves U(a)≤91/100,
and 91/100 < (24/25)². Integrating the L2 path derivative proves (3).

### Exact certificate for the whole parameter interval

For j=0,...,39 let l=j/100, h=(j+1)/100, beta_j=beta(l), and let k_j
be the smallest nonnegative integer with k_j²≥10^6 beta_j. The factors
(2+a)²/[4(2−a)²] and beta(a) are increasing and decreasing in a,
respectively. The latter follows by differentiation, giving numerator
−768a/(4−a²)². Thus for a in [l,h],

    U(a) ≤ U_j := (2+h)²/[4(2−h)²]
                   · [1+k_j/3000+beta_j/4].              (7)

TURN_3_CONTRACTION.csv lists the forty rational bounds and root brackets.
All forty satisfy U_j≤91/100, checked by integer arithmetic in
check_turn_3.py. This is a finite rational certificate covering the full
interval, not a sampling argument. The program also checks minimality of
each integer square-root bracket and 91/100<(24/25)².

## 2. Start with a central-basin orbit and correct its terminal law

Fix u in W, and on the probability space (I,u(x)dx) set X_0(x)=x and

    X_{j+1}=T_{r_j}(X_j),  u_j=F^j u,  r_j=G(E X_j).

Let A_j in {0,1} be the branch label, so
f_{r_j}(X_j)=X_{j+1}+A_j. All cuts and endpoints can be assigned
arbitrarily on null sets. For an integer n put

    epsilon=||u_n−1||_1,
    J_n(y)=−1/2+integral_{−1/2}^y u_n(t)dt,
    Y_n=J_n(X_n).

The cumulative-distribution transform sends the nonatomic law u_n(y)dy
to uniform measure on I, even if u_n vanishes on sets of positive measure.
J_n is nondecreasing and absolutely continuous, fixes both endpoints,
J_n'=u_n a.e., and

    ||J_n−id||_infinity≤epsilon.                           (8)

Proceed backward for j=n−1,...,0 by

    Y_j=V(Y_{j+1}+A_j),    rho_j=G(E Y_j).                 (9)

By construction, Y_j lies in branch A_j of T_{rho_j}, and
T_{rho_j}(Y_j)=Y_{j+1}. Each Y_j has an absolutely continuous law:
if Y_{j+1} has one, each sublaw restricted to A_j=0 or 1 is dominated by
that law and hence is absolutely continuous; applying the corresponding
smooth inverse branch preserves absolute continuity. Starting with uniform
Y_n proves this inductively. If v_n denotes the density of Y_0, then the
parameters in (9) are exactly its successive feedback parameters and

    F^n v_n=1.                                            (10)

This is a genuinely self-consistent backward construction. No external
parameter shadow has been substituted for a nonlinear orbit.

Apply (3) to the two inputs Y_{j+1}+A_j and X_{j+1}+A_j. The common branch
label cancels in their difference. Equations (8)–(9) give

    ||Y_j−X_j||_2≤kappa^(n−j) epsilon,
    Delta_j:=|rho_j−r_j|≤16 kappa^(n−j) epsilon,
    sum_{j=0}^{n−1} Delta_j≤384 epsilon.                  (11)

The branch-label coupling is on the fixed original probability space.
No independence assumption on a label and the next variable is used.

## 3. Global monotone transports and accumulated distortion

The random variables just constructed arise from deterministic monotone
maps H_j:I→I, defined by H_n=J_n and, on branch a of T_{r_j},

    H_j(x)=b_{rho_j}( H_{j+1}(T_{r_j}(x))+a ).             (12)

At the original cut, the two branch limits in (12) both equal −rho_j/4,
because H_{j+1} fixes the endpoints. Thus every H_j is continuous,
nondecreasing, onto, and absolutely continuous. The finite piecewise
composition proves the absolute continuity inductively. It fixes the
endpoints and satisfies Y_j=H_j(X_j) almost surely. It may have flat
intervals; none are assumed away.

Uniformly on the relevant rectangles, (1) gives

    |partial_z b_r|≤3/4,      |partial_r b_r|≤25/96.

Let d_j=||H_j−id||_infinity. Comparing (12) with
x=b_{r_j}(T_{r_j}(x)+a) yields

    d_j≤(3/4)d_{j+1}+(25/96)Delta_j,     d_n≤epsilon.

Consequently

    d_0≤101 epsilon,
    sum_{j=0}^{n−1} d_j≤3 epsilon+(25/24)sum Delta_j
                         ≤403 epsilon.                  (13)

Differentiate (12) on the finitely many continuity cylinders. All
compositions of the original branch maps are smooth with derivative
bounded above and below for this fixed n, so inverse images of exceptional
null sets are null. The chain rule gives

    H_0'(x)=u_n(X_n(x)) R_n(x),
    R_n(x)=product_{j=0}^{n−1}
                f_{r_j}'(X_j(x))/f_{rho_j}'(H_j(X_j(x))).  (14)

No division by u_n is involved. The derivative of log f_r'(x) obeys

    |partial_x log f_r'(x)|≤1,
    |partial_r log f_r'(x)|≤35/24.

Using (11) and (13),

    |log R_n(x)|≤sum d_j+(35/24)sum Delta_j≤963 epsilon.

For convenience retain the slightly weaker bound

    exp(−964 epsilon)≤R_n(x)≤exp(964 epsilon).             (15)

All these constants are independent of n and of the roughness of u.

## 4. Why the derivative error is small in unweighted L1

An essential point is to integrate (14) against ordinary Lebesgue measure,
not against u; the latter could introduce an uncontrolled square of u_n.
For any external parameter sequence in [−2/5,2/5], let

    a_n=P_{r_{n−1}} ... P_{r_0} 1.

Then a_n belongs to the Herglotz mixture class D' and satisfies

    1/2≤a_n(y)≤2.                                        (16)

This is the invariant-class calculation in §4.1 of the credited paper.
It can also be checked directly: the normalized density
w_y(x)=(1−y²/4)/(1−xy)², |y|≤2/3, is sent to a convex combination of
w_{sigma_r(y)} and w_{tau_r(y)}, where

    sigma_r(y)=2(y+r)/[(r+1)y+r+4],
    tau_r(y)=2(y+r)/[(r−1)y−r+4].

Both functions increase in r and y on the rectangle. Their corner values
put their ranges inside [−2/3,2/3]. Each w_y takes values between 1/2
and 2. Starting with w_0=1 proves (16). These identities and corner
bounds are included in the exact verifier.

By the defining transfer identity and (16),

    integral |u_n(X_n(x))−1| dx
        =integral |u_n(y)−1| a_n(y)dy≤2 epsilon.           (17)

Together (14)–(17) give

    ||H_0'−1||_1≤2 epsilon exp(964 epsilon)
                         +exp(964 epsilon)−1.            (18)

## 5. From monotone transport to total-variation convergence

We use the following elementary fact, including maps with flat intervals.
If H:I→I is continuous, nondecreasing, onto and absolutely continuous,
then H_*(H' dx)=dx. This follows, for example, by integrating a continuous
test function composed with H and applying the fundamental theorem of
calculus to its antiderivative. Pushforward is a contraction in total
variation on finite signed measures.

For any continuous g on I, writing omega_g for its uniform modulus of
continuity, these facts imply

    ||H_*(g dx)−g dx||_TV
      ≤ integral |g(x)−g(H(x))H'(x)| dx
      ≤ omega_g(||H−id||_infinity)+||g||_infinity||H'−1||_1. (19)

The norm here is the full variation norm, so for densities it equals
L1 distance, without a factor 1/2. Even if the intermediate pushforward
of g dx has atoms on flat intervals, (19) is an inequality of measures
and remains valid.

Since H_0 pushes u dx to the absolutely continuous law v_n dx, contraction,
(13), (18) and (19) give

    ||v_n−u||_1 ≤ 2||u−g||_1+omega_g(101 epsilon)
       +||g||_infinity[2 epsilon exp(964 epsilon)
                                      +exp(964 epsilon)−1]. (20)

For fixed u in W, epsilon=||F^n u−1||_1→0. First fix a continuous g
arbitrarily close to u in L1; then let n→infinity in (20); finally let
the approximation error tend to zero. We obtain

    v_n→u in L1,       F^n v_n=1.

This proves (A) for every density in W, without positivity, boundedness,
variation or a convergence-rate hypothesis on u.

## 6. Finish the original boundary assertion

By credited Proposition 4, 1 belongs to each noncentral basin boundary.
By turn 1's open-map theorem, each boundary is completely invariant, so
it contains every F^−n({1}), and hence its closure. Section 5 therefore
puts W in each boundary. Conversely, the disjointness and openness of
B_± and the credited global convergence theorem imply each boundary is
contained in W. This proves (T).

## Audit focus and scope

The proof uses the exact two-branch Möbius system, tanh feedback and the
report's A,B rectangle. It does not claim the same conclusion for arbitrary
self-consistent transfer operators. Its main analytic checks are:

1. probability-space inverse contraction, with parameters satisfying the
   feedback relation throughout the interpolation;
2. exact branch-label matching and self-consistency of the backward laws;
3. cumulative transport when the terminal density has zeros;
4. uniform accumulated distortion and the unweighted estimate (17);
5. total-variation convergence via (19), rather than mere weak convergence.

The earlier adaptive-cylinder/Brouwer route was not needed and is not
counted as a separate turn or asserted as a theorem in this packet.
The elementary full proof above, the primary prior results and the exact
certificate should be independently audited before a resolution claim.
