# A reader for the {n,2n,3n} density problem

## 1. The question and the answer this checkpoint gives

Let F(N) be the largest size of a subset of {1,…,N} containing no entire triple {n,2n,3n}. The finite-interval extremal density alpha=lim F(N)/N exists. The original question asks for its value and, in particular, a proof of irrationality. This checkpoint does not decide that arithmetic question.

It supplies exact finite optimization, an all-scale exact-one hitting-set formula, an all-scale one-defect formula, analytic identities for alpha, and an obstruction to one ordinary truncation argument. It also separates an explicit binary rotation cocycle from an unproved binary assertion about the unrestricted optimum. The distinction is essential: the tractable constrained formula has not been shown to compute the unrestricted optimum at every cutoff.

The [source guide](SOURCES.md) records that existence and the exact series were already established in Graham–Witsenhausen–Spencer (1977). Reproving them here fixes conventions; it is not a new resolution of the classical question.

## 2. Decompose the integer interval into smooth components

Every positive integer is uniquely r·2^a3^b with gcd(r,6)=1. Multiplication by 2 or 3 preserves r, so forbidden triples do not join different components. Let d_1=1<d_2<⋯ list the 3-smooth numbers and let f(k) be the maximum triple-avoiding size in {d_1,…,d_k}, with f(0)=0. Then Delta f(k)∈{0,1}, and

    alpha = (1/3) sum_{k≥1} Delta f(k)/d_k.

If Psi(X)=#{d_k≤X}, A(X)=f(Psi(X)), and tau(X)=Psi(X)−A(X), then

    alpha = 1 − (1/3) integral_1^infinity tau(X)/X² dX.

The factor 1/3 is the density of positive integers coprime to 6. The exact component identity and dominated-convergence argument are proved in [the arithmetic supplement](proofs/03_ARITHMETIC_RESULTS.md), including convergence and the initial index.

## 3. Why three colors help, and why they do not finish the problem

Write a smooth number as the lattice vertex (a,b). The triples are right-angle stencils {(a,b),(a+1,b),(a,b+1)} inside 2^a3^b≤X. The color a+2b modulo three gives one vertex of each color in every triple.

Let C_r(X) count nonisolated vertices of color r. A single color is an exact-one hitting set. Conversely, when every triple has exactly one hit, the recurrence

    x_(a,b+1)=1−x_(a,b)−x_(a+1,b)

forces a three-periodic phase except near a short terminal boundary. Four finite terminal profiles exhaust that boundary. This proves

    q0(X)=min_r C_r(X)    for every X≥1.

The complete rigidity argument, four-profile table, base cases, and recurrence are in [the structural supplement](proofs/02_EXACT_ONE_STRUCTURE.md).

For X∈[24·2^m,27·2^m), one particular color class can be improved by deleting three vertices and adding two. The modified hitting set has exactly one double-hit triple. Define epsilon_r(X)=1 for this interval and r=m+2 modulo three, and zero otherwise. The explicit candidate is

    tau_hat(X)=min_r(C_r(X)−epsilon_r(X)).

The patch proves tau≤q1≤tau_hat. The [single-defect theorem](proofs/04_SINGLE_DEFECT_THEOREM.md) proves q1=tau_hat by classifying the sole double-hit corner: high-row defects cost at least zero, left-axis defects reduce to six patterns, deep interior defects are impossible, and the remaining suffix has eight shapes with three phases each. All 280 cutoffs below 3^18 are independently optimized as finite base cases. None of this proves tau=tau_hat. The one-saving patch and its five affected anchors are written out in the structural supplement.

## 4. Exact finite evidence, with index labels

The integer transfer dynamic program was recomputed through d_200=15,116,544. At these 200 cutoffs, tau=q1 and both constrained formulas agree with their color candidates. This is exact finite evidence, not an all-scale unrestricted theorem.

Three useful checkpoints are:

- d_24=162: tau=7 and the minimum hitting set is unique.
- d_45=1536: tau=14, but all three adjusted color classes have size 15. The unrestricted minimum is unique. It hits {192,384,576} twice and all other complete triples once.
- d_77=3^9=19,683: tau(d_76)=tau(d_77)=25, so the maximum avoiding size increases from 51 to 52. There are 12 minimum hitting sets at d_77.

At d_45 the unique minimum is

    {3,4,18,24,32,81,108,144,192,384,486,512,648,864}.

This is a concrete obstruction to identifying the unrestricted optimum with the minimum adjusted single color class. It is not an obstruction to every possible simple formula.

The [finite supplement](proofs/01_FINITE_CERTIFICATES.md) proves the transfer recurrence, its exact counting extension, and the separate excess-cap recurrence. Independent tests include exhaustive subsets through index 20, edge branching through index 25, a transposed row dynamic program through index 77, a further vertex include/exclude algorithm through index 45, and direct full-interval optimization for N≤80. Every stored witness is checked directly against the actual triples.

## 5. An ordinary truncation route is blocked

For L_X=(1/3)sum_(d≤X) Delta f(d)/d, write q_X for its reduced denominator and m=floor(log_2 X). A newly added pure power of two is isolated, so its avoiding increment is one. It is the only included denominator having 2-adic valuation m. Therefore

    v_2(q_X)=m.

An optimal avoiding set below X can be combined with all smooth numbers in (3X,9X]. There are at least m+1 of those. This yields

    alpha−L_X≥(m+1)/(27X),
    q_X(alpha−L_X)>(m+1)/54.

Thus the denominator-scaled errors of these ordinary truncations grow without bound. This blocks the usual vanishing scaled-error irrationality proof for this sequence of approximants. It does not prove that alpha is rational, exclude other approximants, or rule out a different irrationality argument.

The same supplement proves 0≤B(X)≤floor(log_2 X)+1 for B=Psi−3tau. Its Abel-coefficient argument establishes unboundedness of B: assuming bounded color discrepancy would give infinitely many uniformly nonzero Abel Fourier coefficients, contradicting a finite-set Bessel inequality for a bounded function. The argument and all limiting steps are included, rather than inferred from a plot.

## 6. The renormalized integral and the candidate cocycle

The first 25 exact smooth cutoffs determine

    integral_1^24 tau(X)/X² dX = 3/8,
    integral_1^192 tau(X)/X² dX = 2803/5184.

For the actual optimum set

    E(X)=tau(8X)−tau(X)−floor(log_3(8X)).

A change of variables and exact endpoint bookkeeping give

    alpha = 101/126 − (1/21) integral_24^infinity E(X)/X² dX.

This identity holds for the actual tau. The integral converges absolutely because E(X)=O(log X). It does not require E to be binary.

For the explicit candidate, the color increments under X→8X have the form h(1,1,1)+v(X), where h=floor(log_3(8X)) and every coordinate of v is 0 or 1. Consequently the candidate output

    e_hat(X)=tau_hat(8X)−tau_hat(X)−h

is always 0 or 1 for X≥24. Writing X=27^q t with 1≤t<27, the vector v has nine cyclic breakpoints, and multiplication of X by eight acts by t→8t reduced multiplicatively into [1,27). In logarithmic coordinates this is rotation by the irrational number log_3(2).

For delta_r=C_r−epsilon_r−tau_hat, the exact state update is

    e_hat=min_r(delta_r+v_r),
    delta'_r=delta_r+v_r−e_hat.

The full breakpoint table and boundary conventions appear in the arithmetic supplement. This explicit skew product does not supply a finite-state description of the unrestricted optimum. Candidate binary output cannot be substituted into the actual integral without establishing the missing identification.

## 7. A narrow source correction

The [reciprocal-tail supplement](proofs/05_RECIPROCAL_TAIL_CORRECTION.md) proves that, for S={2,3}, the O(1/X) remainder claimed in Proposition 4.3 of Veselinov v1 is false: X·T(X)−log X/(log 2·log 3) is unbounded in absolute value. The proof uses nondecaying Abel coefficients and a finite-set Bessel inequality, not a numerical trend. The exact reciprocal-tail identity, its O(log X/X) bound, the density series, and exact nested density bounds remain valid. This is a correction to that particular remainder assertion, not a rejection of the paper as a whole or an answer to EP168.

## 8. What is still needed

The principal open questions in this checkpoint are:

1. Does the unrestricted minimum equal the one-defect candidate at every cutoff? Finite agreement alone is insufficient.
2. Is actual E(X) binary for every X≥24? The proved candidate statement does not answer this.
3. Can the exact density or a suitable representation be shown rational or irrational? Neither the color formulas nor the ordinary-truncation obstruction settles this.

This is an interim preservation of partial results, with the original arithmetic question unchanged.
