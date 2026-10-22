# Turn 5 — A cancellation countermodel to the relaxed constraints

Checkpoint: 2026-10-05 06:49 UTC. Mechanism: build oscillating flat-polynomial blocks that satisfy the signed growth and quadratic-energy estimates, but have excessive absolute coefficient mass. Outcome: rigorous obstruction to the generic-bounds route, **not** a counterexample in S; the associated map has a proved critical point. Five approaches are exhausted. Best-guess progress toward full resolution: 20%; no complete candidate exists.

## 1. Flat polynomials with an elementary certificate

Define P_0=Q_0=1 and, for integers m>=0,

    P_(m+1)(z)=P_m(z)+z^(2^m)Q_m(z),
    Q_(m+1)(z)=P_m(z)-z^(2^m)Q_m(z).

Each polynomial has degree 2^m-1 and all coefficients are +1 or -1: the two summands occupy disjoint degree intervals. For |z|=1 the cross terms cancel, so

    |P_(m+1)(z)|^2+|Q_(m+1)(z)|^2
      =2(|P_m(z)|^2+|Q_m(z)|^2).

Induction gives |P_m|^2+|Q_m|^2=2^(m+1) on the unit circle. Thus, with N=2^m,

    |P_m(z)|<=sqrt(2N),  |z|<=1,                       (1)

by the maximum-modulus principle. These are the standard Rudin–Shapiro polynomials; all needed properties have been proved above.

## 2. Define one infinite coefficient sequence

For j>=3 put m_j=2^j, N_j=2^(m_j), a_j=sqrt(m_j)/4. Since N_(j+1)=N_j^2, the integer blocks [N_j,2N_j-1] are disjoint. Define the real coefficients b_n by

    H(z)=-z+sum_{j>=3} a_j z^(N_j)P_(m_j)(z)=sum b_n z^n.

Thus b_1=-1, every coefficient in block j has modulus a_j, and all other coefficients are zero. The series converges locally uniformly: its coefficient moduli grow slower than any positive power of n, or alternatively (1) gives uniform geometric decay on each compact subdisk. Define gamma_n=b_n/n and G(z)=sum gamma_n z^n.

This is a single fixed infinite construction. No finite run is offered as proof of its limiting behavior.

## 3. Strong partial-energy bounds, including all Milin inequalities

For 1<=K<N_3, sum_{n<=K}|b_n|^2/n=1<=H_K. If N_j<=K<N_(j+1), then

    sum_{n<=K}|b_n|^2/n
      <=1+sum_{i=3}^j a_i^2 sum_{n=N_i}^{2N_i-1}1/n
      <=1+(1/16)sum_{i=3}^j m_i
      <=1+m_j/8 <= m_j/2 <= log N_j <= H_K.             (2)

Here the block harmonic sum is at most 1, sum_{i=3}^j2^i<2m_j, m_j>=8, log 2>=1/2, and H_K>=log(K+1). The case K=0 is trivial.

Because n|gamma_n|^2=|b_n|^2/n, (2) is the individual partial-energy inequality with additive constant zero. Summing (2) for K=1,...,N proves every de Branges–Milin double-sum inequality for this sequence. Thus even this stronger collection of numerical coefficient restrictions does not suffice for the target.

## 4. The signed analytic growth bound also holds

By (1), the modulus of the j-th block is at most

    a_j sqrt(2N_j) r^(N_j)=sqrt(m_j N_j/8) r^(N_j)
                         <=N_j r^(N_j).

For 0<r<1 let t=-log r. The intervals [N_j/2,N_j] are disjoint. Since exp(-tx)>=exp(-tN_j) throughout such an interval,

    sum_{j>=3}N_j exp(-tN_j)
       <=2 sum_j integral_(N_j/2)^(N_j) exp(-tx) dx
       <=2/t <=2/(1-r).

Therefore

    |H(z)|<=3/(1-|z|),  z in D.                       (3)

At z=0 the bound is immediate. This is the same growth order as the signed logarithmic-derivative expression accompanying the original problem.

## 5. Its absolute majorant violates the desired order

Take r_j=1-1/(2N_j). Bernoulli's inequality gives r_j^(N_j)>=1/2, so every power r_j^n in block j is at least r_j^(2N_j)>=(1/2)^2. Consequently

    (1-r_j)sum_{n>=1}|b_n|r_j^n
       >= (1/(2N_j)) a_j N_j /4
       = a_j/8 = sqrt(m_j)/32 -> infinity.             (4)

One can also check the quadratic shape from the historical update: at these radii,

    sum |b_n|^2 r_j^n >= N_j m_j/64,

which is not little-o of (1-r_j)^(-1)log(1/(1-r_j)). Equations (2), (3), and this quadratic lower growth can all coexist with (4) in a relaxed analytic class.

## 6. A bounded holomorphic map realizes the logarithm, but is not univalent

For the j-th block of G, integrate radially and use (1):

    G_j(z)=a_j integral_0^z t^(N_j-1)P_(m_j)(t) dt,
    sup_{|z|<=1}|G_j(z)|<=sqrt(m_j/(8N_j)).

This bound is summable in j. For example 2^j>=2j for j>=3, so sqrt(m_j/N_j)<=2^(-j/2). Thus G=-z+sum G_j is bounded and continuous on the closed disk, as well as analytic inside. The map

    F(z)=z exp(2G(z))

is bounded and holomorphic, has F(0)=0, F'(0)=1, and F(z)/z is nonzero. Its normalized analytic logarithm is exactly 2G, so its logarithmic coefficients really are gamma_n.

Univalence fails, and this failure is certified rather than left as a tacit assumption. Write H(x)=-x+R(x) on the real interval. At q=3/4, the preceding block bound implies

    |R(q)|<=sum_{j>=3}N_j q^(N_j)
           <=sum_{n>=256} n q^n
           =q^256[256/(1-q)+q/(1-q)^2]
           =1036(3/4)^256 < 1/4.                       (5)

The last inequality is an exact rational comparison also replayed by the controls. Hence

    1+2H(0)=1,
    1+2H(3/4)=1-3/2+2R(3/4)<0.

All coefficients are real. The intermediate-value theorem gives an x in (0,3/4) with 1+2H(x)=0. Since

    F'(z)=exp(2G(z))(1+2H(z)),

F has a critical point in D and cannot be holomorphically injective. Thus **F is not in S and does not settle Problem 6.43**.

## 7. Exact conclusion and stopping point

The construction disproves a proposed implication from generic signed-growth plus Milin-energy restrictions to the target majorant. It does not disprove the implication when genuine univalence is added. That missing geometric input is the remaining central difficulty. There is no sixth search turn and no promotion of this relaxed construction as a full counterexample.
