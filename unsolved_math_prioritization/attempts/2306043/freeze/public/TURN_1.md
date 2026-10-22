# Turn 1 — Abelian reformulation and global quadratic energy

Checkpoint: 2026-10-05 06:42 UTC. Mechanism: convert the radial majorant to coefficient partial sums, then apply the de Branges–Milin quadratic inequalities. Outcome: rigorous weaker bound; full target not proved. Best-guess progress toward a full resolution: 10% (a planning estimate, not a probability or a claim that a fraction of the theorem is proved).

## 1. An exact reformulation

Let a_n>=0 with A(r)=sum a_n r^n finite for every r<1, and S_N=sum_{n<=N}a_n. Then

    A(r)=(1-r) sum_{N>=1} S_N r^N.                         (1)

Tonelli proves (1) by interchanging nonnegative sums. If S_N<=C N, then A(r)<=C r/(1-r). Conversely, assume A(r)<=C/(1-r) for all r sufficiently close to 1. For N>=1 choose r_N=1-1/(2N). Bernoulli's inequality gives r_N^N>=1/2. Hence

    S_N/2 <= sum_{n<=N} a_n r_N^n <= A(r_N) <= 2CN,

so S_N<=4CN for all sufficiently large N; enlarge the constant for the remaining finite set. Thus the O statements are equivalent, with no monotonicity of a_n needed. Similarly S_N=o(N) implies A(r)=o((1-r)^(-1)): split (1) at a fixed cutoff and bound its tail by epsilon times sum N r^N. The converse follows from the same r_N argument.

Apply this with a_n=n|gamma_n|. This does not solve the problem: it identifies the exact missing Cesaro bound.

## 2. The strongest immediate generating-function deduction

The published de Branges–Milin inequalities state that, for every f in S and integer N>=1,

    M_N := sum_{n=1}^N (N+1-n)(n|gamma_n|^2-1/n) <= 0.    (2)

For 0<r<1 all relevant series converge absolutely, because the logarithm is analytic in D. Multiplying (2) by r^N and summing gives

    sum_{N>=1} M_N r^N
       = (1-r)^(-2) sum_{n>=1} (n|gamma_n|^2-1/n) r^n.

Consequently

    E(r):=sum_{n>=1} n|gamma_n|^2 r^n <= log(1/(1-r)).    (3)

Cauchy–Schwarz now gives

    A(r) = sum (sqrt(n)|gamma_n|r^(n/2))
                   (sqrt(n)r^(n/2))
         <= sqrt(E(r)) sqrt(r/(1-r)^2)
         <= sqrt(r log(1/(1-r)))/(1-r).                  (4)

The normalization factor 2 in log(f/z) is essential to the constants in (2)–(4). In b_n notation, E(r)=sum |b_n|^2 r^n/n, not sum |b_n|^2 r^n.

## 3. Gap

The factor sqrt(log(1/(1-r))) is unbounded. It cannot be discarded as an implicit constant. Individual energy bounds or a finite list of checked coefficients do not supply the missing linear average bound. TURN_2 tests a dyadic strengthening; TURN_5 supplies a countermodel to the combined generic bounds.

The proof of (2) is an external classical theorem input. Everything from (2) to (4) is derived here; none of these consequences is presented as a novel result.
