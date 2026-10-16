# A Frobenius-norm upper bound for permanents

Research target: OWR 44/2008, problem 9, pp. 2549–2550; corpus ID 30001073.

Status: complete argument, accepted after independent mathematical audit; bounded source checks do not certify novelty. This document does not claim priority. All logarithms are natural. No entrywise O(1/n) assumption is made.

## 1. Main statement

Let A=(a_ij) be an n by n nonnegative **row-stochastic** matrix, and put S=Σ_ij a_ij². Then

    per(A) ≤ exp(−n + e⁴ Σ_ij a_ij² log(e/a_ij))                 (1)
           ≤ exp(−n + e⁴ S(1+log n)).                         (2)

At a=0 the summand a² log(e/a) is defined to be zero. In particular, if A is doubly stochastic and S≤γ, then

    per(A) ≤ exp(e⁴γ) n^(e⁴γ) e^(−n).

For n≥2, the factor exp(e⁴γ) can be absorbed explicitly:

    per(A) ≤ n^(3e⁴γ) e^(−n).                                (3)

This is the upper bound asked for in the source. Together with the source's already-known van der Waerden lower bound n!/n^n, it gives the requested polynomial-factor exponential order. The lower bound is not new. The notation in the original question is asymptotic: a literal bound n^C e^(−n) at n=1 would be false, since per([1])=1. Equations (1) and (2), including their constant prefactor, hold for n=1 too.

## 2. A random-order entropy lemma

Let X=(X_1,...,X_n) be any random permutation of {1,...,n}. Write

    b_ij = P(X_i=j),
    H(X) = −Σ_x P(X=x) log P(X=x),
    g(b) = −b² log b/(1−b)  for 0<b<1,
    g(0)=0,  g(1)=1.

Then

    H(X) ≤ −Σ_ij b_ij log b_ij − n + Σ_ij g(b_ij).           (4)

Proof. Independently of X, assign independent continuous uniform priorities T_1,...,T_n. Reveal the variables X_i in increasing priority order. Ties occur with probability zero. For any fixed order, the chain rule gives H(X) as the sum of the conditional entropies at the successive reveals.

For the reveal of row i, let S_i be the columns not used by earlier revealed rows. Given the order and preceding values, let q_j be the conditional distribution of X_i. It is supported on S_i. If q_j>0 then b_ij>0, since any conditional event under consideration has positive probability and the marginal probability of that value is therefore positive. Set Z_i=Σ_(j∈S_i) b_ij. The conditional law q is supported in the positive support of the probability law b_ij/Z_i on S_i; in particular Z_i>0. Nonnegativity of relative entropy yields

    −Σ_j q_j log q_j + Σ_j q_j log b_ij ≤ log Z_i.

Average this inequality over histories, over the priorities, and sum over i. Independence of priorities and X, and the entropy chain rule for each fixed order, give

    H(X) + Σ_ij b_ij log b_ij ≤ Σ_i E log Z_i.              (5)

Now condition on the full permutation X and on T_i=t. Since X is a permutation, the available columns are exactly X_i and the X_k with T_k>t. Thus

    Z_i = b_i,X_i + Σ_(k≠i) b_i,X_k 1_{T_k>t},
    E[Z_i | X,T_i=t] = b_i,X_i + (1−t)(1−b_i,X_i).

Here the row sums of B are 1. Jensen's inequality applied to log therefore gives

    E[log Z_i | X,T_i=t]
       ≤ log(b_i,X_i + (1−t)(1−b_i,X_i)).

If b=b_i,X_i, then b>0 for every sampled permutation of positive probability. For 0<b<1,

    ∫_0^1 log(b+(1−t)(1−b)) dt = −1 − b log b/(1−b).

For b=1 the integral is 0, equal to the limiting value on the right. Averaging over X yields

    E log Z_i ≤ −1 + Σ_j g(b_ij).

Substitution in (5) proves (4). Terms b=0 are never sampled and are assigned their continuous limits. □

## 3. Applying the lemma to the permanent

If per(A)=0 there is nothing to prove. Otherwise define the Gibbs law on permutations by

    P(X=σ) = (∏_i a_i,σ(i))/per(A).

Let B be its marginal matrix. B is doubly stochastic, and b_ij>0 implies a_ij>0. Direct substitution in the definition of entropy gives

    log per(A) = H(X) + Σ_ij b_ij log a_ij.

Using (4),

    log per(A) ≤ −n + Σ_ij g(b_ij) − D(B||A),              (6)
    D(B||A) = Σ_ij b_ij log(b_ij/a_ij).

All terms with b=0 are interpreted as zero; an a=0 entry necessarily has b=0. Since both A and B have total entry sum n, D(B||A) also equals

    Σ_ij d(b_ij,a_ij),
    d(b,a) = b log(b/a) − b + a.

For a>0 and b≥0, d(b,a)≥0 by x log x−x+1≥0. Define d(0,0)=0, which is the only case involving a=0 that can occur. No column-stochastic hypothesis on A was used.

## 4. Scalar absorption inequality

For 0≤a,b≤1, with a=0 allowed only when b=0,

    g(b) − d(b,a) ≤ e⁴ a² log(e/a).                       (7)

Proof. The endpoint (a,b)=(0,0) is immediate. For b=0 the left side is −a≤0. Assume a,b>0. The elementary inequality log x≤x−1 implies

    b log(1/b) ≤ 1−b,

and hence g(b)≤b, including b=1 by continuity. The same elementary inequality gives

    log(1/b)/(1−b) ≤ 1+log(1/b),

because this is equivalent to b log(1/b)≤1−b. Consequently

    g(b) ≤ h(b) := b² log(e/b).

If b≥e²a, then log(b/a)≥2, so

    d(b,a) ≥ b+a ≥ b ≥ g(b).

If b<e²a, use d≥0. The function h is increasing on (0,1], because h'(b)=b(1+2log(1/b))>0. If b≤a, then h(b)≤h(a). If a<b<e²a, then b²<e⁴a² and log(e/b)≤log(e/a), whence h(b)≤e⁴h(a). Both cases establish (7). The endpoints b=1 follow by continuity. □

Summing (7) in (6) proves (1).

## 5. Converting the entry sum to a Frobenius bound

Row stochasticity and Cauchy–Schwarz give S≥1. Let p_ij=a_ij²/S, a probability distribution on at most n² points. Then

    Σ_ij a_ij² log(1/a_ij)
       = (S/2)(H(p)−log S)
       ≤ (S/2)(2log n−log S)
       ≤ S log n.

This proves (2). If S≤γ, replace S by γ. For n≥2, 1+log n≤3log n, giving (3). □

## 6. Necessary polynomial losses

The polynomial prefactor cannot in general be replaced by a constant depending only on γ. For an integer k≥1 and n=km, take A to be block diagonal with k blocks J_m/m. Then A is doubly stochastic,

    Σ a_ij² = k,
    per(A) = (m!/m^m)^k
           ~ (2πm)^(k/2) e^(−n)
           = (2π/k)^(k/2) n^(k/2)e^(−n).

Thus any exponent valid at γ=k must be at least k/2 asymptotically. The explicit constant in (3) is deliberately not optimized.

## 7. Prior-work boundary

The random-order entropy method is classical, especially Radhakrishnan's entropy proof of Brégman's theorem (1997). More specifically, Anari and Rezaei, *A Tight Analysis of Bethe Approximation for Permanent*, arXiv:1811.02933v2, §4, equation (6), p. 12, already establish the Gibbs-marginal/random-order upper bound from which (6) follows by the conditional Jensen calculation in §2 above. Their use of the Gibbs marginal matrix instead of the input matrix must be credited. Sections 2–3 provide a self-contained derivation, including zero entries, rather than claiming that idea as new.

The input Frobenius hypothesis is exactly the source hypothesis. The stronger entrywise condition a_ij≤γ/n is not substituted. The candidate contribution for this target is the explicit scalar KL absorption estimate (7) and its Frobenius-norm consequence (1)–(3). Bounded searches did not locate this consequence already stated. This is not proof of novelty or priority; it may be an unstated or previously published consequence of known entropy techniques. Anari's 2026 preprint, arXiv:2608.28031v2, also retains sequential relative entropy for improved exponential-factor approximation but the inspected statements and full-text Frobenius occurrences do not state the target norm bound.

Public primary sources:

- Original problem: [Oberwolfach Reports 44/2008, problem 9, pp. 2549–2550](https://doi.org/10.4171/owr/2008/44).
- Classical method: [Radhakrishnan, An Entropy Proof of Bregman's Theorem (1997)](https://doi.org/10.1006/jcta.1996.2727).
- Direct prior entropy comparison: [Anari–Rezaei, arXiv:1811.02933v2](https://arxiv.org/abs/1811.02933v2), §4, equation (6), p. 12.
- Recent related work: [Anari, arXiv:2608.28031v2](https://arxiv.org/abs/2608.28031v2), §4, Lemma 7, pp. 9–10.
