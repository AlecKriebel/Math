# Density series, arithmetic obstruction, and candidate cocycle

## Status and scope

This is a newly authored reconstruction from the problem definitions and freshly verified finite certificates. It does not authenticate an earlier artifact or settle the density's arithmetic nature.

The density series, the stated global bounds and unboundedness of B, the ordinary-truncation denominator obstruction, the integral identity with constant 101/126, and the explicit candidate's binary rotation cocycle are proved below. Unboundedness is recovered through the fully re-established Abel/Bessel argument in Section 3.1. Binary output for the actual optimum, equality of the explicit candidate with the actual optimum, and an arithmetic conclusion about alpha remain **unproved**.

The numerical cutoff X=192 means the first 25 smooth numbers. It does not mean prefix index 192.

## 1. Definitions

Let D={2^a 3^b : a,b are nonnegative integers}, listed increasingly as d_1=1<d_2<... . Let Psi(X)=#{d in D : d<=X}, with Psi(X)=0 for X<1. Write V_X={(a,b):2^a 3^b<=X}.

A forbidden triple in V_X is {(a,b),(a+1,b),(a,b+1)} whenever all three vertices lie in V_X. Equivalently, in D it is {d,2d,3d}. Let f(k) be the maximum size of a subset of {d_1,...,d_k} containing no full forbidden triple, with f(0)=0. Set

- A(X)=f(Psi(X));
- tau(X)=Psi(X)-A(X), the minimum number of deleted vertices hitting every forbidden triple;
- delta_f(d_k)=f(k)-f(k-1), which is either zero or one;
- B(X)=3A(X)-2Psi(X)=Psi(X)-3tau(X).

The original finite-interval function F(N) is the maximum size of a subset of {1,...,N} avoiding every triple {n,2n,3n}. Its limiting density is alpha=lim F(N)/N, whose existence follows in the next section.

## 2. Exact density series and existence of the limit

Every positive integer has a unique expression r d with gcd(r,6)=1 and d in D. Each forbidden triple stays in one such r-component. Therefore

F(N) = sum_{r<=N, gcd(r,6)=1} A(N/r)
     = sum_{d<=N, d in D} delta_f(d) C_6(N/d),

where C_6(y)=#{r<=y:gcd(r,6)=1}. We have C_6(y)/y -> 1/3, and C_6(y)<=y for y>=1. Since

sum_{d in D} 1/d = (1-1/2)^(-1)(1-1/3)^(-1) = 3,

dominated convergence, using 0<=delta_f<=1, gives

alpha = (1/3) sum_{d in D} delta_f(d)/d.                         (2.1)

The integral of a step-function cumulative count gives, by Tonelli,

alpha = (1/3) integral_1^infinity A(X)/X^2 dX
      = 1 - (1/3) integral_1^infinity tau(X)/X^2 dX.             (2.2)

All integrals converge absolutely. For example, Psi(X) is at most (floor(log_2 X)+1)(floor(log_3 X)+1), and 0<=tau<=Psi.

## 3. Global bounds on B

Color (a,b) by a+2b modulo 3. Each forbidden triple has one vertex of each color. Deleting a smallest color class hits every triple, so tau(X)<=Psi(X)/3 and B(X)>=0.

The number of forbidden triples is exactly Psi(X/3). Each vertex is in at most three triples: as the anchor, its eastern neighbor, or its northern neighbor. Consequently 3tau(X)>=Psi(X/3). Shifting b by one shows

Psi(X)-Psi(X/3)=floor(log_2 X)+1.

Combining these facts gives, for every X>=1,

0 <= B(X) <= floor(log_2 X)+1.                                (3.1)

At X=d_k this is 0<=B_k=3f(k)-2k<=floor(log_2 d_k)+1.

### 3.1 Unboundedness: Abel coefficients and Bessel inequality

Write ell_2=log 2, ell_3=log 3, theta=ell_3/ell_2, and omega=exp(2*pi*i/3). The number theta is irrational, since a rational value would imply 3^q=2^p for positive integers p,q. Define, for u>=0,

Z(u)=sum_{a*ell_2+b*ell_3<=u} omega^(a+2b).

Suppose for contradiction that B(X)<=M for all X>=1. Let N_r(X) be the raw count of color r. The color-cover argument gives

B(X)>=Psi(X)-3 min_r N_r(X).

Therefore every N_r is at least Psi/3-M/3 and, because their sum is Psi, at most Psi/3+2M/3. Since 1+omega+omega^2=0, this implies |Z(u)|<=2M. Thus it suffices to show Z is not bounded.

For Re(s)>0, absolute convergence allows summing the Laplace integrals of its steps:

F(s)=integral_0^infinity Z(u) exp(-su) du
    = 1 / [s(1-omega exp(-ell_2 s))(1-omega^2 exp(-ell_3 s))].  (3.2)

For n=0,1,2,... put t_n=2*pi*(n+1/3)/ell_2. These are distinct positive nonzero frequencies. At s=i*t_n, the first geometric denominator vanishes, and the second cannot vanish: simultaneous vanishing would give theta=(3m+2)/(3n+1) for some integer m. Expanding the first denominator at s=sigma+i*t_n gives 1-exp(-ell_2*sigma)~ell_2*sigma. Hence the Abel coefficient exists and is

a_n=lim_{sigma down to 0} sigma F(sigma+i*t_n)
   = 1 / [ell_2*i*t_n*(1-omega^2 exp(-i*t_n*ell_3))].         (3.3)

We now show infinitely many |a_n| are at least 1/(8*pi^2). Set beta=(2-theta)/3. Choose arbitrarily large denominators q of reduced rational approximations p/q to theta satisfying |theta-p/q|<1/q^2; continued-fraction convergents provide these. Since p is coprime to q, the q points np/q modulo one, 0<=n<q, are exactly the q-point grid. Choose n in this range with

||np/q-beta||<=1/(2q),

where || || is distance to the nearest integer. It follows that

||n theta-beta|| < 3/(2q).                                   (3.4)

The selected indices n are unbounded. Otherwise a single n would recur along an infinite subsequence q tending to infinity, forcing n theta-beta to be an integer, and thus theta=(3m+2)/(3n+1), a contradiction. We may therefore choose infinitely many distinct n>=1. Since n<q, (3.4) gives ||n theta-beta||<=3/(2n). The elementary inequality |1-exp(2*pi*i*y)|<=2*pi*||y|| yields

|1-omega^2 exp(-i*t_n*ell_3)|
 = |1-exp(2*pi*i*(beta-n theta))|
 <= 3*pi/n.

For these n, the denominator magnitude in (3.3) is at most

2*pi*(n+1/3) * 3*pi/n <= 8*pi^2.

Consequently |a_n|>=1/(8*pi^2) for infinitely many distinct frequencies.

Finally, a bounded function cannot have this property. Here is the needed Bessel argument, including the limiting justification. If |Z|<=K, equip [0,infinity) with probability measure dmu_sigma=sigma exp(-sigma u)du. For any finite collection of distinct frequencies t_j,

integral exp(i*(t_j-t_k)*u) dmu_sigma -> 1 if j=k, and 0 otherwise.

If their Abel coefficients a_j=lim integral Z(u) exp(-i*t_j*u) dmu_sigma exist, take P(u)=sum_j a_j exp(i*t_j*u). Expanding the nonnegative integral of |Z-P|^2 and taking limits gives

sum_j |a_j|^2 <= K^2.                                       (3.5)

Indeed, the P norm tends to sum |a_j|^2, the mixed term tends to that same sum, and the Z norm is bounded above by K^2 for every sigma. The infinitely many lower bounds |a_n|>=1/(8*pi^2) contradict (3.5) by taking a sufficiently large finite subset. Thus Z is unbounded, and so B(X) cannot be bounded. Because B is constant between consecutive smooth cutoffs, B_k is unbounded as claimed.

## 4. Ordinary-truncation denominator obstruction

Define the ordinary truncation

L_X=(1/3) sum_{d<=X} delta_f(d)/d,

and let q_X be its denominator in lowest terms. Put m=floor(log_2 X), for X>=1.

### 4.1 Exact 2-adic denominator valuation

At d=2^m, the newly added vertex (m,0) is isolated in its smooth-prefix triple hypergraph. It cannot be the northern vertex of a triple, and the triple anchored at 2^(m-1) would also require 3*2^(m-1)>2^m. No old triple changes. Thus delta_f(2^m)=1, also for m=0 from the empty prefix.

Among all d=2^a3^b<=X, the only d with a=m is 2^m, because 3*2^m>X. Every other summand in 3L_X has denominator with 2-adic valuation at most m-1. Putting the summands over a common denominator 2^m times an odd power of 3, the numerator is odd: the 2^m summand contributes an odd integer and all others contribute even integers. Multiplication of the denominator by 3 does not change its 2-adic valuation. Hence

v_2(q_X)=m.                                                   (4.1)

### 4.2 Lower bound on the truncation error

Take an optimal avoiding subset of D intersect [1,X], and adjoin every smooth number in (3X,9X]. Their union is avoiding. A triple anchored at n<=X stays at or below 3X; a triple anchored at n>3X has 3n>9X; no anchor in the omitted interval (X,3X] is present.

For every a=0,...,m, there is a b>=0 with 3X<2^a3^b<=9X: choose the first power of 3 above 3X/2^a. These m+1 vertices are distinct. Therefore

A(9X)-A(X) >= Psi(9X)-Psi(3X) >= m+1.

Using (2.1), all weights of terms with X<d<=9X are at least 1/(9X), giving

alpha-L_X >= (m+1)/(27X).

By (4.1), q_X>=2^m>X/2, so

q_X (alpha-L_X) > (m+1)/54.                                  (4.2)

In particular, these denominator-scaled ordinary-truncation errors grow without bound. This blocks the usual small-error argument based on these particular partial sums; it neither proves rationality nor excludes another route to irrationality.

## 5. Exact finite data and rational constants

The input file fixtures/exact/tau_through_X192.json contains these exact values:

| d | tau(d) | d | tau(d) | d | tau(d) | d | tau(d) | d | tau(d) |
|---|---:|---|---:|---|---:|---|---:|---|---:|
|1|0|2|0|3|1|4|1|6|1|
|8|1|9|2|12|2|16|2|18|3|
|24|3|27|4|32|4|36|4|48|4|
|54|5|64|5|72|5|81|6|96|6|
|108|7|128|7|144|7|162|7|192|8|

The finite certificate records agreement between integer column-transfer dynamic programming and independent exhaustive subset search through prefix index 20, and between that dynamic program and an independent edge-deletion recurrence through prefix index 25. The separate fixtures/exact/ verification artifacts carry the finite optimization certificates. The arithmetic checker does not claim to establish their optimality itself.

For T_Y=integral_1^Y tau(X)/X^2 dX, integration on the half-open smooth-number intervals gives

T_24 = 3/8,
T_192 = 2803/5184.                                            (5.1)

Endpoint values do not affect these integrals. In particular, the jump at 192 is not inserted into the integral up to 192.

For X>=24, floor(log_3(8X)) starts at 4 and then increases by one at X=3^j/8, j>=5. Thus

J = integral_24^infinity floor(log_3(8X))/X^2 dX
  = 4/24 + sum_{j>=5} 8/3^j
  = 1/6 + 4/81
  = 35/162.                                                   (5.2)

Exact rational arithmetic yields

8T_192 - T_24 + J = 25/6.                                    (5.3)

## 6. Renormalized integral identity

Define the actual optimum output

E(X)=tau(8X)-tau(X)-floor(log_3(8X)).

Let T=integral_1^infinity tau(X)/X^2 dX and I=integral_24^infinity E(X)/X^2 dX. Substituting u=8X into the first term gives

I = 8(T-T_192) - (T-T_24) - J
  = 7T - 25/6.

Equation (2.2) now gives the fully reconstructed identity

alpha = 101/126 - (1/21) integral_24^infinity E(X)/X^2 dX.      (6.1)

### 6.1 What is known about the actual output

E(X) is integer-valued. It is O(log X), without any candidate-optimality assumption. Indeed, putting h=floor(log_3(8X)), shifting the old vertex set by three in a adds just columns a=0,1,2. Their total size is 3h+s for an s in {0,1,2}; equivalently Psi(8X)-Psi(X)=3h+s. Monotonicity and extending a cover by all new vertices give

0<=tau(8X)-tau(X)<=3h+s,

and hence -h<=E(X)<=2h+2. This also directly proves absolute convergence of the integral in (6.1).

The global assertion E(X) in {0,1} is **UNPROVED**. A binary statement for the explicit candidate below does not establish it for E.

## 7. Explicit candidate and binary cocycle

This section concerns an explicitly defined function, denoted tau_hat, rather than the actual optimum tau. It does not require identifying tau_hat with the minimum cover with at most one defect (often denoted q_1), or with unrestricted tau.

For X>=24, let N_r(X) count all vertices (a,b) of V_X with a+2b=r modulo 3. Put m=floor(log_2 X). The only possible isolated vertex is (m,0), present as an isolated vertex exactly when 3*2^(m-1)>X. Let i_r(X) be its indicator in color r, or zero if there is no isolated vertex. Set C_r(X)=N_r(X)-i_r(X).

Let epsilon_r(X)=1 exactly when, for some integer j>=0,

24*2^j <= X < 27*2^j, and r=j+2 modulo 3;

otherwise epsilon_r(X)=0. The intervals are disjoint. Define

w_r(X)=C_r(X)-epsilon_r(X),
tau_hat(X)=min_r w_r(X).                                     (7.1)

The structural reconstruction supplies feasible color covers and the exceptional one-saving patch, so tau_hat is an upper-bound candidate for the unrestricted minimum. No lower-bound identification is used here.

### 7.1 Scale-eight increment of each candidate color count

Translation (a,b)->(a+3,b) identifies V_X with all columns a>=3 in V_(8X), preserving color. The three new columns a=0,1,2 have respective maximum b values

h_0=h,
h_1=floor(log_3(4X)),
h_2=floor(log_3(2X)),

where h=floor(log_3(8X)). Put z=8X/3^h in [1,3). The height triples are

- (h,h-1,h-2) for 1<=z<4/3;
- (h,h-1,h-1) for 4/3<=z<2;
- (h,h,h-1) for 2<=z<3.

In the first case, the color counts are (h,h,h). The extra vertex in the second case has color 2h modulo 3, and the additional vertex in the third case has color 2h+1 modulo 3. Consequently the new color-count vector is

h(1,1,1)+v(X),

where

v=0                                  if 1<=z<4/3;
v=e_(2h mod3)                        if 4/3<=z<2;
v=e_(2h mod3)+e_((2h+1) mod3)        if 2<=z<3.                (7.2)

Every coordinate of v is zero or one. Both corrections in (7.1) are invariant under scale eight, color by color: the isolated vertex shifts a by three; the exceptional-interval index j shifts by three. The converse for the exceptional interval uses X>=24, so an exceptional interval of 8X must have j>=3. Therefore

w_r(8X)=w_r(X)+h+v_r(X).

Taking minima proves, for every X>=24,

tau_hat(8X)-tau_hat(X)-h is either 0 or 1.                    (7.3)

This conclusion is entirely about tau_hat.

### 7.2 Nine breakpoints and multiplicative rotation

Write X=27^q t uniquely with 1<=t<27. The vector v depends only on t. Its nine cyclic breakpoints are

9/8, 3/2, 9/4, 27/8, 9/2, 27/4, 81/8, 27/2, 81/4.

Using coordinate order (r=0,1,2), the half-open interval values are:

| t interval | v |
|---|---|
|[1,9/8)| (1,0,1) |
|[9/8,3/2)| (0,0,0) |
|[3/2,9/4)| (0,1,0) |
|[9/4,27/8)| (0,1,1) |
|[27/8,9/2)| (0,0,0) |
|[9/2,27/4)| (1,0,0) |
|[27/4,81/8)| (1,1,0) |
|[81/8,27/2)| (0,0,0) |
|[27/2,81/4)| (0,0,1) |
|[81/4,27)| (1,0,1) |

The first and last intervals form one interval on the multiplicative circle, so there are nine breakpoints, not ten.

Scaling X by eight drives

t -> 8t                 if 8t<27,
t -> 8t/27              if 8t>=27.

This is multiplicative reduction modulo 27, not additive remainder modulo 27. In logarithmic coordinates it is rotation by log_27(8)=log_3(2), which is irrational since a rational value would imply a positive power of 2 equals a positive power of 3.

For the normalized nonnegative integer color state delta_r=w_r-min_s w_s, the candidate's output and next state are exactly

e_hat=min_r(delta_r+v_r) in {0,1},
delta'_r=delta_r+v_r-e_hat.                                   (7.4)

This gives an explicit skew product with binary candidate output. It does not establish a finite-state reduction for the unrestricted optimizer, nor does it identify the candidate state with the exact optimum's transfer-DP state.

## 8. Reproduction and limits

Run `python3 -I -B checks/check_arithmetic.py`. The checker uses exact rational arithmetic, validates all 25 finite input values, checks the constants and the nine-breakpoint partition at endpoints and interior points, and checks correction discontinuities. The output agrees under normal, `-O`, and `-OO` execution. The all-scale claims rely on the written proofs above.

The finite input's optimization certificate is separate; the arithmetic checker alone does not prove those minima. Global equality of the explicit candidate with unrestricted tau, global binary output for actual E, and either rationality or irrationality of alpha remain unproved. The [single-defect supplement](04_SINGLE_DEFECT_THEOREM.md) supplies a separate proof identifying the candidate with q1; the arithmetic derivations above do not require that identification.
