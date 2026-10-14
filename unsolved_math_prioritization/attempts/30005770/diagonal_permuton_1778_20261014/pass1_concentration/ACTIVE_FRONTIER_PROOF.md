# Minimum-insertion frontiers in principal ends-in-one classes

**Scope:** shared substantive pass 1, target 30005770. This is a restricted concentration theorem, not a proof of the diagonal-permuton conjecture. No novelty claim is made. All randomness below is exactly uniform on the full indicated avoidance class.

## 1. Statement

Fix a nonempty permutation alpha of length m and put tau = alpha skew-sum 1. Let C_n = Av_n(tau), a_n = |C_n|, a_0 = 1. For sigma in C_n, let

L(sigma) = min { j : the first j entries of sigma contain alpha },

with L(sigma) = n+1 if sigma avoids alpha. Thus L is one plus the length of the longest initial segment avoiding alpha. For the empty permutation L = 1.

If m = 1, C_n consists only of the increasing permutation and the full target is immediate. Suppose henceforth that m >= 2. Define

lambda = lim a_n^(1/n),
C(z) = (1 - sqrt(1-4z))/(2z),
gamma = log C(1/lambda).

Here 4 <= lambda < infinity, so gamma > 0; C(1/4) = 2 by continuity. The existence, finiteness and lower bound used here are justified below.

**Theorem A (frontier).** If Pi_n is uniform on C_n, then, for every fixed epsilon in (0,1],

limsup (1/n) log P( L(Pi_n) >= ceil(epsilon n) ) <= -epsilon gamma.       (A)

The convention log 0 = -infinity is used. In particular the initial alpha-free segment is o(n) in probability, with an exponential bound at every positive linear scale.

**Theorem B (small values).** Write M_k(pi) = max { pi^(-1)(v) : 1 <= v <= k }. For every sequence of integers 1 <= k_n <= n with k_n = o(n), and every fixed epsilon in (0,1],

limsup (1/n) log P( M_{k_n}(Pi_n) >= ceil(epsilon n) ) <= -epsilon gamma. (B)

This includes the global minimum and every fixed number of smallest values. There is also a positive-density corner estimate: if k_n/n -> delta in (0,1) and a in (delta,1], then

limsup (1/n) log P( M_{k_n}(Pi_n) >= ceil(a n) )
 <= H(delta) - (a-delta) gamma,                                      (C)

where H(delta) = -delta log delta -(1-delta) log(1-delta). A negative right side gives exponential rarity. These statements do not say that a positive fraction of all points lies near the diagonal.

## 2. Exact minimum insertion

Given sigma of length n, insert a new minimum 1 after its first k entries and increase all old values by 1. There are n+1 possible gaps, k = 0,...,n.

**Lemma 1.** For sigma in C_n, precisely the gaps

k = 0,...,L(sigma)-1

are allowed: the inserted permutation belongs to C_(n+1) exactly when k < L(sigma).

**Proof.** Every forbidden occurrence not using the inserted entry was already present in sigma, which is impossible. Since tau ends in its minimum, every new forbidden occurrence must use the inserted 1 as its last entry. It exists exactly when the first k old entries contain alpha. This is equivalent to k >= L(sigma). If alpha is absent, every gap is allowed, as required. Deleting the minimum is the inverse operation, so these edges form a rooted generating tree with exactly the permutations C_n at level n. No distributional approximation occurs. QED.

The parent is determined uniquely by deleting the minimum and standardizing. More generally, deleting the t smallest values recovers a unique ancestor t levels earlier. In particular the depth-t descendant sets of two distinct same-level parents are disjoint.

**Lemma 2 (Catalan domination of children).** If L(sigma) = L and m >= 2, sort the L child labels as b_1 <= ... <= b_L. Then

b_j >= j+1,  1 <= j <= L.                                         (D)

Every child label is also at most L+1.

**Proof.** Let r be the position of the minimum within alpha. Consider insertion at an allowed gap k. An alpha occurrence not using the new point cannot end earlier than L+1: old earliest occurrences end at L, and the insertion is before that endpoint. If there is no old occurrence, the same assertion follows from the n+1 convention, since the child has length n+1 and label at most n+2 = L+1.

An alpha occurrence using the new minimum requires r-1 entries before it and m-r after it. If k < r-1, none exists, so this child has label L+1. Otherwise its label is at least

min { L+1, k+m-r+1 }.

For an integer q <= L, a child whose actual label is <= q must therefore have

r-1 <= k <= q-m+r-1.

There are at most max(0,q-m+1) <= q-1 such gaps. Taking q = j excludes b_j <= j, proving (D). Finally an old earliest occurrence shifts from endpoint L to L+1; in the no-occurrence case the child label is at most its length plus one, again L+1. QED.

The stronger lower bound b_j >= min { L+1, j+m-1 } also follows, but is not needed below.

## 3. Descendant amplification

Let D_t(sigma) be the number of depth-t descendants of sigma. Let

B(L,t) = L/(L+2t) * binomial(L+2t,t),  L >= 1, t >= 0.             (E)

**Lemma 3.** D_t(sigma) >= B(L(sigma),t).

**Proof.** The comparison tree with label L has children labelled 2,3,...,L+1. Lemma 2 permits its recursive embedding into the actual tree. More explicitly, if an actual node has label M >= L, its sorted children of indices 1,...,L have respective labels at least 2,...,L+1, and are distinct. Continuing recursively embeds all finite comparison descendants. Distinct insertion paths give distinct permutations because deleting successive minima recovers the path.

For completeness, B(L,0) = 1 and B(L,t+1) = sum_(j=2)^(L+1) B(j,t). Its depth generating function is C(z)^L: indeed C = 1+z C^2 implies

C^L = 1 + z * sum_(j=2)^(L+1) C^j.

This finite geometric-series identity is also valid as a formal series (C-1 = z C^2). The coefficient identity (E) follows by Lagrange inversion applied to C = 1+z C^2; equivalently it is the standard ballot-number formula and can be checked directly in the displayed recurrence with the initial condition. Hence the embedded tree has exactly B(L,t) descendants. QED.

In particular a_t >= B(1,t), the Catalan number. This proves lambda >= 4 once existence is established.

**Exact tail inequality.** Let A_n(ell) = |{sigma in C_n : L(sigma) >= ell}|. For every integer ell >= 1 and t >= 0,

A_n(ell) B(ell,t) <= a_(n+t).                                    (F)

The comparison count is nondecreasing in L, and the descendant sets are disjoint. Dividing (F) by a_n gives a fully finite-n bound, without assuming any ratio asymptotic.

There is a simpler, weaker alternative. The elementary bound that the child at gap k has label at least k+1 gives at least binomial(ell+t-1,t) descendants. It yields the rate -epsilon log(lambda/(lambda-1)). The Catalan domination is responsible for the improvement to (A).

## 4. Growth and proof of Theorem A

The pattern tau ends in 1 and has length at least two, hence is direct-sum indecomposable: an occurrence straddling two direct-sum blocks would split tau as a nontrivial direct sum, which its final minimum rules out. Consequently C is direct-sum closed and

a_(p+q) >= a_p a_q.

Fekete's lemma gives lambda = sup_n a_n^(1/n), allowing initially infinity. The Marcus--Tardos exponential bound makes lambda finite. Thus log a_n = n log lambda + o(n). This uses only the classical exponential bound, not a stronger ratio-limit theorem. The Catalan embedding above gives lambda >= 4.

Fix epsilon > 0 and s > 0. Put ell_n = ceil(epsilon n), t_n = floor(s n). Stirling's formula in (E) gives

(1/n) log B(ell_n,t_n) ->
  (epsilon+2s) log(epsilon+2s) - s log s
  - (epsilon+s) log(epsilon+s).

The prefactor ell_n/(ell_n+2t_n) has logarithm o(n), and rounding changes the limit by zero. From (F),

limsup (1/n) log P(L(Pi_n) >= ell_n)
 <= s log lambda -(epsilon+2s) log(epsilon+2s)
      + s log s +(epsilon+s) log(epsilon+s).                     (G)

To optimize, negate the right side and differentiate with respect to s. When lambda > 4 the maximum occurs at

s = epsilon/2 * (sqrt(lambda/(lambda-4))-1),

obtained from (epsilon+2s)^2 = lambda s(epsilon+s). Substitution gives the maximum epsilon log C(1/lambda).

When lambda = 4, the negated right side increases to epsilon log 2 as s -> infinity. The estimate (G) holds for every fixed finite s; taking the infimum of these valid upper bounds proves the endpoint rate without ever choosing a non-fixed s before n tends to infinity. This proves (A). The same argument works whenever ell_n/n -> epsilon > 0, a form used below. QED.

## 5. Deletion weights and proof of Theorem B

The next argument expressly retains the bias introduced by deleting small values; the resulting ancestor is not asserted to be uniform.

Delete the k smallest values of pi in C_n and standardize, obtaining sigma in C_(n-k). Rebuild pi by successive insertions of new minima. By Lemma 2 each insertion increases the label by at most one. A point inserted at step j has current position at most L(sigma)+j-1, and later insertions can move it right at most k-j times. Hence

M_k(pi) <= L(sigma)+k-1.                                        (H)

For fixed sigma there are at most binomial(n,k) a_k possible descendants: choose the positions occupied by the k small entries and choose their standardized subpermutation, which belongs to C_k. Those choices and sigma determine pi uniquely; not every pair need be valid, so this is an upper bound. In fact (H) gives the sharper sigma-dependent bound binomial(L(sigma)+k-1,k) a_k, but it is not needed.

Therefore, for integer q,

P_n(M_k >= q)
 <= binomial(n,k) * (a_k a_(n-k)/a_n)
       * P_(n-k)( L >= q-k+1 )
 <= binomial(n,k) * P_(n-k)( L >= q-k+1 ).                       (I)

The last inequality is direct-sum supermultiplicativity. Equation (I), including its completion factor, is the exact bridge between the two uniform laws.

If k = k_n = o(n), log binomial(n,k) = o(n), (n-k)/n -> 1, and (ceil(epsilon n)-k+1)/(n-k) -> epsilon. The variable-threshold version of (A) applied to (I) proves (B). If k_n/n -> delta and q_n/n -> a > delta, the same argument gives log binomial(n,k_n)/n -> H(delta) and frontier exponent -(a-delta) gamma. This proves (C). QED.

## 6. Why this does not prove the target

The target asks that inversion density tend to zero, or equivalently that the entire uniform permutation have weak diagonal limit. The statements proved here localize an insertion frontier and the smallest o(n) values, which themselves have vanishing permuton mass. The positive-density estimate (C) only gives a corner constraint, with an entropy cost H(delta); it does not give M_(delta n)/n -> delta.

The completion factor in (I) cannot be omitted. Deleting k minima from uniform C_n gives a parent sigma with probability D_k(sigma)/a_n, not probability 1/a_(n-k). Replacing this weighted law by a uniform law would be the precise unjustified step in a purported bulk proof.

Even the deterministic conclusions of the proved concentration statements need not force diagonal geometry. For the illustrative target alpha = 132, fix 0 < d < 1. Take r_n = floor(d n/3), let sigma_n be the direct sum of r_n copies of 132, and append a decreasing block of length n-3r_n by direct sum. These permutations avoid 2431 because each block does and 2431 is direct-sum indecomposable. Their frontier L is 3 for all sufficiently large n, and for every k_n=o(n) their first k_n values have positions at most k_n+2. Nevertheless their decreasing final block contributes asymptotic inversion density (1-d)^2/2 when inversions are divided by n^2. This is only a deterministic nonimplication example, not a counterexample under the required uniform law.

No bound on maximum displacement is asserted; it would be false in important target cases. No new alpha beyond established sources is declared solved. The full universal diagonal-permuton conjecture remains unresolved by this argument.

## 7. Attribution and verification boundaries

- Target and exact uniform weak-limit contract: Bevan/Troyka, Oberwolfach report 6/2024, printed pp.281--282 and 298--299, https://ems.press/content/serial-article-files/48646?nt=1 .
- Exponential avoidance bound: Adam Marcus and Gabor Tardos, *Excluded permutation matrices and the Stanley--Wilf conjecture*, JCTA 107 (2004), 153--160, DOI https://doi.org/10.1016/j.jcta.2004.04.002 ; author manuscript https://web.math.princeton.edu/~amarcus/papers/permmat/MarcusTardos_permmat.pdf . Only the finite exponential bound is invoked; Fekete and the lower bound were proved above.
- Independently recovered primary context: Neal Madras and Gokhan Yildirim, *Longest monotone subsequences and rare regions of pattern-avoiding permutations*, EJC 24(4), P4.13 (2017), p.2 states the finite growth limit with attribution. https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i4p13/pdf/ . Their rare-region results are not used as a limiting-support theorem.
- Hohmeier--Slivken v3, https://arxiv.org/abs/2502.19541v3 , gives credited restricted families; no generalization of its theorem is assumed here.

The companion finite checker tests the stated combinatorial identities on bounded exact inputs. It does not certify the all-n theorem; the arguments above supply that proof. It supplies no evidence that uniform permutons beyond known families converge. No source text, dataset contents, or private coordination materials are included in this authored report.
