# Independent reconstruction of Certificate 7.1

Public edition dated 2026-10-12. This retains the complete substantive mathematical report, with transparent editorial changes to private references and review-status wording. Independently authored executable checkers, raw interval certificates, full numerical records, detailed diagnostic outputs, and source copies are not included. Hashes identify omitted evidence but do not provide executable public reproducibility. The work is AI-assisted and unrefereed, with no external human peer review or formal proof-assistant certification.

## Scope and outcome

This note reconstructs the scalar and reference-existence gate called Certificate 7.1 in Shouqiao Wang's *A Proposed Complete Solution to Erdős Problem 1038*. It uses an independently written verifier, exact integer interval arithmetic, and explicit finite-series remainder bounds. No author software, Lean project, installer, or externally supplied executable was run.

This is a sufficient independent replacement for Certificate 7.1, not a verification of its original reported slab counts or margin digits. The result is the following conditional calibration theorem. Let L be the global minimum of the admissible zero-platform one-cut width. Assume the previously audited analytic supporting, endpoint-adjoint, and circle block inequalities. Then, for every finite k >= 29/20, the reference choices below satisfy their positivity, simple-main-crossing, positive-adjoint, and strictly positive block-surplus hypotheses. The conditional use of the global-minimum theorem is confined to the terminal effective-platform correction. Establishing that L really is the one-cut global minimum is Certificate 6.1, not a conclusion of this note.

The independent finite-candidate result already accepted in PR 1310 supplies L < T whenever L is the global one-cut minimum, where the following finite decimal is interpreted as an exact rational:

    T = 1.83443047576266171109075363512901884952989750747.

Our strict scalar lower bounds differ from the proposal's bounds, because the interval cover and estimates are different. Agreement with the proposal's reported margins is neither assumed nor required.

| Reference regime | Independently checked cover | Strict normalized surplus |
|---|---:|---:|
| a = 1153/500 - k/4, 36/25 <= k <= 21/10 | 395 parameter slabs | > 0.028229353338717 |
| a = 9/5, 21/10 <= k <= 21/5 | 840 parameter slabs | > 0.036361685512222 |
| Zero platform, 0 < rho <= 1/50 | one nonsingular tail box | > 0.961762019209 |
| Zero platform, 1/50 <= rho <= rho(26631/10^6) | 256 parameter slabs | > 0.000564594536104 |
| Zero platform, rho(26631/10^6) <= rho <= rho(41542/10^6) | 39 parameter slabs | > 0.065630278169259 |

Here rho(q) = -1/log q. Rounded display endpoints in this note are outward bounds; the actual endpoints and margins were checked as integer numerators over 2^160 in the omitted full result records.

## 1. Exact arithmetic and proof-producing checks

Every acceptance calculation uses an interval [l/2^160, u/2^160] with integer endpoints. Addition and subtraction are exact. Multiplication takes the minimum and maximum of the four endpoint products and rounds by integer floor and ceiling. Reciprocal reverses the endpoints and uses integer division; an interval containing zero is rejected. Square root uses integer square root of l*2^160 and u*2^160, rounding the upper root up unless its square is exact. Exact decimal inputs are converted by integer division. The hardened constructor rejects floating-point endpoints.

For log x, monotonicity reduces an interval to its endpoints. Each positive dyadic endpoint is scaled by an exact power of two to y in [1,2]. With t=(y-1)/(y+1), the kernel uses

    log y = 2 sum_{j=0}^{55} t^(2j+1)/(2j+1) + remainder,
    0 <= remainder <= 2 t^113 / (113(1-t^2)).

The remainder is evaluated by directed interval arithmetic. The implemented admissible chart is 0 <= t <= 1/2; this also admits directed rounding around 1/3. The same formula at t=1/3 encloses log 2, and log x = log y + e log 2.

For exp x, monotonicity again reduces to endpoints. Positive arguments are divided by powers of two to t in [0,1]. The sum through degree 60 has a remainder between zero and 2/61!, because the positive terms after degree 60 have successive ratios at most 1/62. Repeated directed squaring reverses the scaling. Negative arguments use reciprocals.

Machin's identity pi = 16 atan(1/5) - 4 atan(1/239), with 120 alternating-series terms and the first omitted term as an error bound, supplies pi. Sine and cosine at points use reduction by a multiple of 2 pi, a checked residual in [-4,4], and Taylor polynomials through degrees 73 and 72. Their absolute error bounds are respectively 4^75/75! and 4^74/74!. Interval sine/cosine enclosures use endpoint values and every possible intervening critical point. The selected integer search range is checked to extend strictly beyond both input endpoints.

Ordinary floating-point calculations only propose root brackets or trigonometric reduction integers. No proposed sign, root, endpoint padding, or special-function value is accepted without the exact interval tests. A poor proposal can cause rejection or further subdivision but cannot make an invalid box pass. In particular, there is no mpmath/Arb conversion, undocumented print precision, or fixed decimal padding assumption in the acceptance path.

All proof gates are ordinary conditional checks which raise an exception on failure. None uses a Python assertion. Optimization flags therefore do not remove proof conditions.

## 2. Reference formulas and block surplus

For k >= 1 and 1 <= a < 2 let

    c=(a+2)/2, r=(2-a)/2, H=r/2,
    eta=(k+1)e_[a,2] - k omega_[a,2].

In the coordinate d=c-r cos theta, its angular density is

    A(theta)=k+1-k sqrt(2a)/d.

It has total mass one and is increasing. Positivity is equivalent to A(0)>0. Let rho0=(sqrt(2)-sqrt(a))/(sqrt(2)+sqrt(a)). For x<a, x != 0, put

    Kx=sqrt((a-x)(2-x)), rhox=r/(c-x+Kx),
    W(x)=k log|x| + log((c-x+Kx)/2) - 2k log(1-rho0 rhox),
    Wx(x)=k/x - 1/Kx + 2k rho0 rhox/[Kx(1-rho0 rhox)].

The verifier explicitly checks the physical domain x<a, the side of zero, the appropriate opposing endpoint signs, and a strict sign of Wx throughout each root box. The intermediate value theorem and strict derivative sign therefore isolate one root in each box uniformly over the entire parameter slab. Three interval Newton intersections tighten the boxes: if m is the exact midpoint and X contains the root, the mean-value theorem gives

    root in m - W(m)/Wx(X).

Intersecting this enclosure with X cannot discard a true root. The negative root is the unique negative crossing. Since eta is positive, W is strictly concave between zero and a; a positive crossing with Wx>0 is the first positive crossing and thus the right endpoint of the main negative component. The positive slope also gives a strictly positive point immediately to its right, establishing strict separation.

At the roots x_minus and x_plus set sigma_minus=-1/Wx(x_minus)>0 and sigma_plus=1/Wx(x_plus)>0, and write rho_minus,rho_plus for their Poisson parameters. Then

    a_pi = 1+2k rho0/(1+rho0),
    b_pi = 4 sigma_minus rho_minus/(1-rho_minus^2)
           +4 sigma_plus rho_plus/(1-rho_plus^2),
    R0 = 2 sigma_minus rho_minus/(1-rho_minus)
         +2 sigma_plus rho_plus/(1-rho_plus),
    Qmax=pi/a_pi, Rmax=pi R0/b_pi,
    C=log H+k log((a+2+2 sqrt(2a))/4), M0=x_plus-x_minus,
    Ceff(T)=C+(T-M0)/R0.

All denominators, Poisson ranges, density positivity, root slopes, and positive adjoint masses are checked. Positivity of the adjoint on every nonempty interval follows from its numerator vanishing at a and having derivative

    sigma_minus K_minus/(d-x_minus)^2
    + sigma_plus K_plus/(d-x_plus)^2 > 0.

For positive normalized block masses Q,R, the audited circle inequality gives the normalized block surplus at least

    log(2H/(a_pi b_pi)) + h(Q)+h(R)
    + sum_{n>=1} (sinc(nQ)-sinc(nR))^2/n
    - pi Ceff/(a_pi Q).

Here

    h(X)=-sum_{n>=1} sin(nX)^2/(n^3 X^2)-log(X/pi).

The function h is nonnegative and decreasing on (0,pi]. Indeed,

    h(X)=log(2pi)-3/2+2 int_0^1 (1-t)log(sin(Xt)/(Xt)) dt.

The function sin u/u decreases on (0,pi), since sin u-u cos u has derivative u sin u>0 and vanishes at zero. Thus h decreases, and the series gives h(pi)=0.

To bound h at a positive argument, we retain n=1,...,80. The omitted nonnegative sine-square sum is at most sum_{n>80} n^-3 <= 1/(2*80^2). Consequently the directed interval

    -sum_{n=1}^{80} sin(nX)^2/(n^3 X^2)-log(X/pi)
    + [-1/(2*80^2 X^2),0]

contains h(X). This bound is also used in the terminal refined range; no trilogarithm evaluation is needed.

## 3. Finite-parameter regimes

The initial k partition has exact rational mesh 1/400. Unresolved slabs are bisected, never accepted heuristically. The accepted union covers [36/25,21/10] and [21/10,21/5], including their common endpoint. The first range starts strictly below 29/20.

For each slab, Ceff(T)<0, 0<Rmax<Qmax<pi, and positivity of the density and adjoint are checked. Define

    B=log(2H/(a_pi b_pi))+h(Qmax)+h(Rmax),
    P=-pi Ceff(T)/a_pi >0.

Monotonicity of h lets us use the outward upper caps in its lower bounds. In the constant-edge regime, dropping all nonnegative squares leaves B+P/Q, whose minimum over Q<=Qmax is at Qmax. The verifier checks B+P/Qmax>0.

In the affine regime, retain the n=1 square. For Q<=Rmax, B+P/Q+(sinc Q-sinc R)^2 >= B+P/Rmax. For Q>=Rmax and R<=Rmax, monotonicity of sinc gives a lower bound

    f(Q)=B+P/Q+(sinc Q-sinc Rmax)^2.

The exact interval checks cover all Q=Rmax+u(Qmax-Rmax), using 32 closed rational u-subintervals covering [0,1], and prove

    f'(Q)=-P/Q^2+2(sinc Q-sinc Rmax)sinc'(Q)<0.

Thus it suffices to check B+P/Rmax>0 and f(Qmax)>0. Both checks pass on every accepted affine slab. The reported margins are the directed minimum of these lower bounds.

The target linkage is one-sided. For fixed reference and block, increasing the target from L to T adds (T-L)/R0 to Ceff and decreases the surplus. Therefore the checks at exact T establish at least the same surplus for every L<=T. No lower bound on L is used in these finite regimes.

## 4. Terminal zero-platform regime

Let q be the one-cut parameter, rho=-1/log q, d=log 2-2 log(1+q), A=1-rho d, and

    k=(1-rho d)/(rho d), a=2((1-q)/(1+q))^2.

This gives C=0 exactly. In the stable variables z_plus=q u_plus and z_minus=q u_minus, the crossing equations are

    G_plus=A log((z-q^2)/(1-z))-log z-d=0,
    G_minus=A log((z-q^2)/(z-1))-log z-d=0.

The verifier proves q<z_plus<1<z_minus, opposing parameter-uniform endpoint signs, and respectively positive and negative z-derivatives. Four interval Newton intersections tighten the roots. These are the simple physical exterior branches: the map from u to the spatial coordinate is decreasing for u>1, the known derivative factorization has exactly one nontrivial positive-side root, and the negative-side branch is strictly monotone.

Set

    P0=rho d+2q(1-rho d)/(1+q),
    raw(z)=1-A(1-q^2)z/[(1-z)(z-q^2)],
    wp=-1/raw(z_plus), wm=1/raw(z_minus),
    D=2 P0(wp+wm),
    Qmax=pi rho d/P0,
    Rmax=pi [(1+q/z_plus)wp+(1+q/z_minus)wm]/[2(wp+wm)].

The signs raw(z_plus)<0<raw(z_minus) and eta(0)=1-2kq/(1-q)>0 are checked. Algebraic cancellation of the original positive factors gives

    D=a_pi b_pi/(2H).

For completeness, put t=rho d=1-A and F(u)=A log((u-q)/|1-qu|)-log u. Then raw=-u F_u. The spatial derivative is x_u=-H(1-u^-2), while W=-(1+k)F. Therefore each positive slope-reciprocal magnitude is sigma=t K w, with K=H(u-u^-1) and w=wp or wm. It follows that a_pi=P0/t and b_pi=4tH(wp+wm), proving the displayed identity. Similarly, R0=2tH sum((1+q/z)w), which gives the formula for Rmax. This derivation uses no small-q limiting substitution. For every finite rho>0, D>0. The scalar with all squares and self-gaps discarded is -log D. On the simple boxes, that scalar is strictly positive directly; no monotonicity-of-D certificate is needed. On the refined boxes we instead check -log D+h(Qmax)+h(Rmax)>0.

In the simple regime it is unnecessary to interval-check Qmax<pi near the singular endpoint: a_pi=1+2kq/(1+q)>1 proves it exactly, while Rmax/pi is a positive weighted average of (1+q/z_plus)/2 and (1+q/z_minus)/2, both less than one. The refined regime explicitly checks both cap upper bounds below pi before evaluating h.

### Nonsingular tail

For 0<rho<=1/50, q=exp(-1/rho)<2^-72, because log 2<25/36 implies 72 log 2<50. Use the closed independent box

    0<=rho<=1/50, 0<=q<=2^-72,
    499/1000<=z_plus<=501/1000,
    149/100<=z_minus<=15001/10000.

Direct rational-interval evaluation proves the opposing G endpoint signs, the root derivative signs, and raw(z_plus)<0<raw(z_minus). Since q(rho)/rho increases on (0,1),

    kq <= q/(rho d) <= 50*2^-72/d_lower,

which proves eta(0)>0 without division by a rho interval containing zero. The cancelled D expression is defined on the entire closed tail box and is at most 0.038237980791. For each actual rho>0 it is positive, so -log D>=1-D>0.961762019209. No claim about a finite reference at rho=0 is made or needed.

### Parameter coverage

Write g(q)=(1+q)d(q)+2q log q. Its derivative is log(2q^2/(1+q)^2), negative on this range. Exact endpoint checks give

    g(41542/10^6) > 0.372861191115,
    k(41542/10^6) in [4.199981974345,4.199981974346] < 21/5,
    k(26631/10^6) in [4.659976505491,4.659976505492] < 233/50.

Thus g>0 on (0,41542/10^6], which proves strict density positivity and k'(q)<0. Also k(q)->infinity as q->0. Therefore the terminal family covers every k>=21/5 with strict overlap at the finite endpoint.

The rho split and cap are calculated as outward intervals from their exact rational q values. The simple cover runs through the split's upper endpoint and the refined cover starts at its lower endpoint. This intentionally overlaps the split. The refined cover runs through the cap's upper endpoint. Consequently conversion to rho cannot create a gap. The final dyadic endpoints, rather than rounded display decimals, define the checked cover.

## 5. Effective-platform dependency and strictness

For a terminal reference, C=0. If Certificate 6.1 establishes that L is the global one-cut minimum, then M0>=L and hence Ceff=(L-M0)/R0<=0. Its contribution -pi Ceff/(a_pi Q) is nonnegative and may be discarded. This is the only global-minimum input not proved within this reconstruction note itself; it is discharged by the accompanying accepted one-cut proof and end-to-end audit. Merely knowing a small fixed-candidate upper bound would not justify discarding it.

For any nonempty target block, its physical probability mass q_block and adjoint mass r_block are positive. A strictly positive normalized surplus therefore gives a strictly positive unnormalized surplus after multiplication by q_block*r_block. There are finitely many blocks. Summing, and applying the audited block-reduction proposition, yields strict total width greater than L for the atomized finite configuration. The independently audited elementary range handles 1<=k<=29/20. The original finite polynomial has at least the width of its atomization.

This completes the numerical/reference Certificate 7.1 gate conditional on the stated analytic inputs and Certificate 6.1. It does not independently re-prove the circle rearrangement theorem, the full supporting/adjoint argument, or Certificate 6.1. It does not treat a reported author run or a proposed manuscript status as a proof receipt.

## Sources and attribution

- [Wang's proposed manuscript](https://multiscalar.ai/results/erdos-1038/paper.pdf), retained SHA-256 3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad. Mathematical definitions and the target Certificate 7.1 are attributed to this proposal.
- [Companion author verifier](https://multiscalar.ai/results/erdos-1038/numerical_verifier.py), retained SHA-256 e84b94b40a27d2f3e254d4d14393a49c79ac4db57e4b55010441d4e04eff9616. Static inspection only; no author code was imported or executed.
- [Tao's one-cut construction](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf), retained SHA-256 7ef1d231d1689873bafba3bbe5e70710bc605eee245d71614f3abd0917824d41.
- [Accepted fixed-candidate packet, draft PR 1310](https://github.com/AlecKriebel/Math/pull/1310), commit 845701107993994ce9d56a93164535bcb9b33874. Its acceptance does not itself include the global lower bound.

The underlying reconstruction was performed without publication or queue mutation. This public edition includes its authored proof note and aggregate verification metadata, but excludes the executable programs and full raw interval records.
