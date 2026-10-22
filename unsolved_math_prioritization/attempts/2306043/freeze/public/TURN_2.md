# Turn 2 — Dyadic localization and the quadratic-example trap

Checkpoint: 2026-10-05 06:43 UTC. Mechanism: seek uniformly bounded dyadic weighted energy to remove the logarithmic loss; test compatibility with the primary update and an exact sparse model. Outcome: this intermediate route is blocked, and the historical quadratic lower growth does not disprove the actual target. Best-guess progress toward full resolution: 5%.

## 1. What the tempting block estimate would prove

For f in S define

    E_j = sum_{2^j<=n<2^(j+1)} n|gamma_n|^2,   j>=0.

If E_j<=K_f for every j, Cauchy–Schwarz on one block gives

    sum_{2^j<=n<2^(j+1)} n|gamma_n|
       <= sqrt(E_j) sqrt(sum_{2^j<=n<2^(j+1)} n)
       <= sqrt(2K_f) 2^j.

Summing complete blocks and bounding the final partial block by its full block would give S_N=O_f(N), hence the desired conclusion by TURN_1.

## 2. That stronger premise is false in the full class

Under the same premise set D_N=sum_{n<=N} n^2|gamma_n|^2. If 2^J<=N<2^(J+1), then

    D_N <= sum_{j=0}^J 2^(j+1) E_j
        <= 2K_f(2^(J+1)-1) <= 4K_f N.

Abel summation yields

    Q(r)=sum n^2|gamma_n|^2 r^n <= 4K_f r/(1-r).

It follows that Q(r)=o((1-r)^(-1)log(1/(1-r))). This contradicts the existence assertion for a particular f in S in Hayman–Lingham Update 6.43. Thus, at the theorem-input level of that inspected update, there is a fixed f for which sup_j E_j=infinity. The shortcut requires a genuinely false stronger statement, even allowing its constant to depend on f.

This conclusion uses the update's attributed Hayman example. The original 1980 construction was not independently inspected; see the source scope. We do not substitute an unverified reconstruction of that example.

## 3. Why the quadratic lower growth is not a disproof of the problem

Here is a self-contained sequence control, not a univalent-function construction. For integers j>=3 define

    m_j=2^j,  N_j=2^(m_j),
    c_(N_j)=sqrt(N_j m_j)/4,
    c_n=0 otherwise.

For K with N_j<=K<N_(j+1),

    sum_{n<=K} c_n^2/n = (1/16)sum_{i=3}^j m_i
                       < m_j/8 <= H_K,

where H_K=sum_{n<=K}1/n, and H_K>=log(K+1)>=m_j log 2>=m_j/2. Thus it satisfies even the stronger zero-additive-constant Milin partial-energy inequality.

Set r_j=1-1/(2N_j). Bernoulli gives r_j^(N_j)>=1/2, so

    sum c_n^2 r_j^n >= N_j m_j/32.

Since (1-r_j)^(-1)log(1/(1-r_j))=2N_j log(2N_j)
=2N_j(m_j+1)log 2, the ratio is bounded below by

    m_j/[64(m_j+1)log 2].

It does not tend to zero. Nevertheless sum_{n<=K}c_n=o(K). Indeed c_(N_(i-1))/c_(N_i)<1/2, so sum_{i=3}^j c_(N_i)<=2c_(N_j). Consequently for N_j<=K<N_(j+1),

    (sum_{n<=K}c_n)/K <= sqrt(m_j/N_j)/2 -> 0.

TURN_1 then proves sum c_n r^n=o((1-r)^(-1)). Quadratic growth of the form in the update is therefore compatible with an absolute-linear sum even smaller than required. Cauchy–Schwarz cannot be reversed to bridge this gap.

For completeness the signed series with these positive c_n also has O((1-r)^(-1)) growth: c_(N_j)<=N_j and, with t=-log r, the intervals [N_j/2,N_j] are disjoint and

    sum N_j r^(N_j) <= 2 integral_0^infinity exp(-tx) dx
                    = 2/t <= 2/(1-r).

## 4. Exact remaining gap

One needs a direct linear coefficient-average mechanism that permits unbounded dyadic quadratic energies, or a single genuinely univalent counterexample. This turn supplies neither. A dyadic Cauchy–Schwarz estimate alone cannot settle the original conjecture.
