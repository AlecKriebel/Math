# Exponential permuton concentration under adjoining a minimum

## Theorem and scope

Fix a permutation q of length at least two whose first entry is 1. Suppose that for every epsilon>0, a uniformly random Sigma_n in Av_n(q) satisfies

P(d_BL(mu_{Sigma_n}, mu_J)>epsilon) <= C_epsilon exp(−c_epsilon n)

for all sufficiently large n, with c_epsilon>0, where mu_J=Law(U,1−U) and mu_sigma is the square-spread permuton. Then the same assertion holds for the exact uniform law on Av_n(1 direct-sum q).

Consequently, the anti-diagonal limit with exponential fixed-deviation tails holds for every fixed pattern

beta_d=I_d direct-sum 231,  d>=1,

using the established beta_1=1342 case as the seed. Position reversal and inversion give diagonal limits with exponential fixed-deviation tails for

Av_n(132 skew-sum J_d) and Av_n(213 skew-sum J_d), d>=1.

In the original target notation tau=alpha skew-sum 1, these are

alpha=132 skew-sum J_(d−1), or alpha=213 skew-sum J_(d−1).

An empty J_0 is allowed. The d=1 cases are the previously established seed results; d>=2 supplies the extension. No claim for arbitrary alpha, or for alpha=312, follows from this theorem.

More generally, in the target convention, exponential diagonal concentration for any fixed tau=alpha skew-sum 1 implies it for tau skew-sum 1. Repetition appends any fixed decreasing block of new minima.

## 1. Credited growth-rate input

For a fixed pattern q, put a_n=|Av_n(q)|, a_0=1, and write L(q) for its Stanley–Wilf growth rate. The existence and finiteness of that rate are standard consequences of Arratia and Marcus–Tardos. For a pattern starting with 1, Bóna proved

L(1 direct-sum q)=(1+sqrt(L(q)))^2.                         (1)

We use this precise result with its starts-with-1 hypothesis. Primary source: Miklós Bóna, *The limit of a Stanley–Wilf sequence is not always rational, and layered patterns beat monotone patterns*, arXiv:math/0403502v2, Theorem 5.4, p.7; published J. Combin. Theory Ser. A 110 (2005), 223–235, DOI 10.1016/j.jcta.2004.07.014. The same preprint's Theorem 5.2 identifies the particular family growth L(beta_d)=(d−1+sqrt(8))^2. Those are credited counting results, not permuton assertions.

A starts-with-1 pattern of length at least two is skew-indecomposable. Therefore its avoidance class is closed under skew sums: an occurrence crossing two skew blocks would itself be skew-decomposable. Hence a_(m+n)>=a_m a_n. Writing lambda=L(q), this implies

a_n<=lambda^n for every n>=0.                            (2)

Indeed a_(rn)>=a_n^r, and taking rn-th roots and then r→infinity gives (2).

Set q'=1 direct-sum q, b_n=|Av_n(q')|, and

Lambda=(1+sqrt(lambda))^2.

By (1), for every gamma>0 and all sufficiently large n,

b_n >= Lambda^n exp(−gamma n).                           (3)

Only this exponential-scale lower bound is needed; no ratio limit or precise coefficient asymptotic is assumed.

## 2. Canonical deletion and an ambient merge count

A left-to-right minimum of a permutation is an entry smaller than all earlier entries. Delete every such entry from pi and standardize the remaining sequence to obtain sigma. Since q starts with its minimum,

pi avoids q' if and only if sigma avoids q.              (4)

Proof: if the remaining entries contain q, the first entry of that occurrence is the smallest within it. Since this entry was not a left-to-right minimum of pi, some earlier entry is smaller, so adjoining that earlier entry creates q'. Conversely, in an occurrence of q', every entry belonging to its q part has the occurrence's first entry smaller and earlier; none is a left-to-right minimum. Thus that q occurrence survives deletion. This is also the starts-with-1 case of Bóna's Proposition 5.1.

Let k be the number of remaining entries. Record their position set P, their value set V, and their standardization sigma. Both P and V are k-element subsets of [n]. The other n−k entries are left-to-right minima and so appear in decreasing order. The triple (P,V,sigma) uniquely recovers pi.

We enlarge this injective encoding to the ambient set of ALL triples

P,V in binom([n],k), independently, and sigma in Av_k(q),

filling the complement positions with complement values in decreasing order. Many such triples are not canonical and may not yield q'-avoiders. They are used only for an UPPER bound. We never assert independent uniform subsets after conditioning on a valid encoding.

The total ambient count is

T_n=sum_(k=0)^n binom(n,k)^2 a_k
   <=sum_(k=0)^n [binom(n,k)lambda^(k/2)]^2
   <=[sum_(k=0)^n binom(n,k)lambda^(k/2)]^2
   =Lambda^n.                                          (5)

Thus ambient overcount costs no exponential factor relative to (3). This matching growth rate is essential to the proof.

## 3. Transport cost and deterministic merge geometry

Define, for a permutation pi of length n>=1,

ell_n(pi)=n^(−2) sum_(i=1)^n |i+pi(i)−n−1|,

and set ell_0=0. Always 0<=ell_n<=1, and ell_n=0 for the decreasing permutation. Let

D(mu)=integral |x+y−1| dmu(x,y).

The centers of pi's occupied squares have coordinates ((i−1/2)/n,(pi(i)−1/2)/n). Within a square the value of x+y changes by at most 1/n from its center. Consequently

|D(mu_pi)−ell_n(pi)|<=1/n.                              (6)

Uniform marginals and the coupling (X,Y) with (X,1−X) give d_BL(mu,mu_J)<=D(mu). The function |x+y−1|/sqrt(2) is bounded by 1 and is 1-Lipschitz on the Euclidean square, so D(mu)<=sqrt(2)d_BL(mu,mu_J). Therefore

d_BL(mu_pi,mu_J)<=ell_n(pi)+1/n,
ell_n(pi)<=sqrt(2)d_BL(mu_pi,mu_J)+1/n.                  (7)

The hypothesis of the theorem is thus equivalent to exponential fixed-positive-deviation tails for ell_n; finite exceptional n can be absorbed into the multiplicative constants.

For a k-subset P of [n] define its prefix discrepancy

E(P)=max_(0<=j<=n) | |P intersect [j]|−kj/n |.

If P={p_1<...<p_k}, then evaluating the discrepancy at p_r yields

|p_r/n−r/k|<=E(P)/k.                                   (8)

The complement of P has the same discrepancy. Let pi be the ambient merge of sigma of size k and the decreasing permutation of size m=n−k, with position and value subsets P,V for sigma. For 0<k<n, compare the center (p_r−1/2)/n to its local center (r−1/2)/k. Equation (8) implies the coordinate error is at most

E(P)/k+(1/2)(1/k−1/n).

The analogous bound holds for values. After averaging over the k sigma points with their full-permutation mass 1/n, their transport cost is at most

(k/n)ell_k(sigma)+(E(P)+E(V))/n+(1−k/n)/n.

For the decreasing complementary sequence, its local cost is zero. Applying the same argument with m and the complements gives cost at most

(E(P)+E(V))/n+(1−m/n)/n.

Adding these inequalities proves

ell_n(pi) <= (k/n)ell_k(sigma)
             +2(E(P)+E(V))/n+1/n.                      (9)

For k=0 or k=n, the conclusion remains valid directly: the merge is respectively decreasing or just sigma. In particular, if E(P),E(V)<=delta n, then

ell_n(pi) <= (k/n)ell_k(sigma)+4delta+1/n.               (10)

This is an explicit geometric statement about the merge, not an inference from its counting sequence.

## 4. Uniform exponential bound for subset discrepancies

For a uniformly random k-subset P, each X_j=|P intersect [j]| is hypergeometric with mean kj/n. Uniformly in 0<=k,j<=n,

P(|X_j−kj/n|>t)<=2 exp(−t^2/(2n)),                     (11)

with deterministic endpoint cases understood separately. Here is a direct martingale justification. For 0<k<n, expose k distinct samples from a population of n entries with j ones. The Doob martingale for the eventual sum has increments

[(n−k)/(n−r)] (Y_r−p_(r−1)),  1<=r<=k,

where p_(r−1) is the proportion of ones still unseen. Each increment has absolute value at most one. Azuma–Hoeffding therefore bounds the two-sided tail by 2 exp(−t^2/(2k)), which implies (11). For k=0,n the sum is deterministic.

A union bound over j, then over independently chosen P and V, gives

P(E(P)>delta n or E(V)>delta n)
 <=4(n+1)exp(−delta^2 n/2).                             (12)

Independence of P and V is true in the ambient triple model. The union bound itself does not require it.

## 5. Counting bad encodings under the exact uniform target law

Fix epsilon in (0,1). Set delta=epsilon/16, and take n>=4/epsilon. If ell_n(pi)>epsilon and the discrepancy event in (12) does not occur, then (10) gives

(k/n)ell_k(sigma)>epsilon/2.

Since ell_k<=1, this implies both

k>epsilon n/2 and ell_k(sigma)>epsilon/2.                (13)

Thus components with sublinear size, or even with size <=epsilon n/2, cannot cause this bad event on a good allocation. No uniform concentration claim for small components is needed.

By the theorem's hypothesis and (7), there are constants C,c>0, depending only on epsilon and q, such that under the exact uniform law on Av_k(q),

P(ell_k(sigma)>epsilon/2)<=C exp(−c k)                   (14)

for all k>=1 after enlarging C if necessary. For example, for k>=4/epsilon the event implies d_BL>epsilon/(4sqrt(2)); the finitely many smaller k are absorbed into C.

For a fixed k, take the uniform AMBIENT triple. Combining (12)–(14), its probability of producing a merge with ell_n>epsilon is at most

4(n+1)exp(−delta^2 n/2)+C exp(−c epsilon n/2).

Multiply by binom(n,k)^2 a_k and sum over k. Every bad q'-avoider has one canonical encoding among those counted triples. Therefore, with

r=min(delta^2/2,c epsilon/2)>0,

#{pi in Av_n(q'): ell_n(pi)>epsilon}
 <=[4(n+1)+C]exp(−r n) T_n
 <=[4(n+1)+C]exp(−r n) Lambda^n.                        (15)

Now divide by the actual avoidance count b_n. Use (3) with gamma=r/2. The exact UNIFORM q'-avoiding law then satisfies

P(ell_n(Pi_n)>epsilon)
 <=[4(n+1)+C]exp(−r n/2)
 <=C' exp(−r n/4)                                      (16)

for all sufficiently large n. The final polynomial absorption changes only C' and the onset. Equation (7), with epsilon adjusted by a factor of two, proves the stated exponential d_BL concentration.

The proof never replaces the actual uniform law by independently random interleavings. It bounds bad ambient triples, uses a canonical injection for actual avoiders, and divides by their exact class size. The credited growth equality is the step controlling the possible bias of the conditioning.

## 6. Iteration and geometric symmetries

Let beta_1=1342 and beta_d=1 direct-sum beta_(d−1) for d>=2. Each starts with 1. The established exact labeled-tree proof for uniform 1342-avoiders supplies the exponential hypothesis at d=1. Inducting with the theorem gives the conclusion for every fixed d. Constants may depend on d; no uniform-in-d rate or growing d_n is claimed.

Position reversal maps beta_d to

reverse(beta_d)=132 skew-sum J_d.

Inversion first maps beta_d=I_d direct-sum 231 to I_d direct-sum 312; reversing positions then gives 213 skew-sum J_d. These are exact finite-class bijections, and their transformations of square-spread permutons are the corresponding reflections/transposition of the unit square. Inversion preserves the anti-diagonal; position reversal sends it to the diagonal. The rates and exact uniform laws therefore transfer.

For the general target closure, q=reverse(tau) starts with 1 whenever tau ends with 1. Reversing 1 direct-sum q gives tau skew-sum 1. Thus the theorem preserves exponential diagonal concentration when another final minimum is adjoined. It does not supply a seed for an arbitrary tau, and it leaves the previously uncovered alpha=312 / tau=4231 case untouched.

## 7. Role of the protected-tail source

Úlfarsson, *Protected tails and polynomial-time enumeration of permutations avoiding a direct sum of an increasing pattern and 231*, arXiv:2609.15642v2 (1 October 2026), provides exact counting and uniform generation for this family. Its introductory discussion identifies Bóna's recursive minima deletion and exact growth theorem, which led to the argument above. The proof here does not require a marked-state analysis of the protected-tail recurrence, and does not infer a limit from a sampler, heatmap, or finite numerical table. Prior enumeration, prior seed results, and the concentration-transfer argument remain separate inputs.
