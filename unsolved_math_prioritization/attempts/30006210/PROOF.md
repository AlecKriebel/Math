# An inverse-polynomial influence threshold for two Boolean-cube polynomials

## Status and scope

This proof of the exact two-polynomial question posed by Per Austrin in the 2025 Oberwolfach report, contributed section “Zeros of Low-Degree, Low-Influence Polynomials on the Boolean Hypercube,” p. 445, has been accepted by an independent internal mathematical audit. The AI-assisted proof and audit are unrefereed; no external human peer review is claimed. This is not a novelty claim or a claim about every formulation called polynomial compatibility.

The essential structural input is the polynomial-support separator of Longcheng Li, Qian Li, Xingjian Li, and Qipeng Liu, *Impossibility of Perfectly Complete Many-Round Key Agreement in the QROM*, arXiv:2608.03824v1 (4 August 2026), Lemma 3.5. We give its argument, with explicit constants, below. Its Markov-inequality ingredient is also presented explicitly; the Bernoulli symmetrization appears in Kothari, Kovacs-Deak, Wang, and Yang, *Rational degree is polynomially related to degree*, arXiv:2601.08727v3, Fact 5 and Corollary 1. The conversion from a separator to relative influences is proved here using an elementary adaptive resampling argument. No priority claim is made for that conversion.

## Theorem

Let n,d be positive integers. Let f,g be nonzero real multilinear polynomials on {-1,1}^n, each of degree at most d. Write

    f(x) = sum_{S subset [n]} f_hat(S) product_{i in S} x_i,
    ||f||_2^2 = E f(X)^2 = sum_S f_hat(S)^2,
    RelInf_i(f) = sum_{S containing i} f_hat(S)^2 / ||f||_2^2,

where X is uniform and the denominator includes S = empty set. Define RelInf_i(g) in the same way.

If all these relative influences are at most

    1 / (4096 d^8),

then there exists x in {-1,1}^n such that f(x)g(x) is nonzero.

Thus the exact requested absolute constants can be taken to be c = 1/4096 and C = 8. They are deliberately not optimized.

We prove the contrapositive. A useful stronger quantitative conclusion of the proof is that, whenever nonzero f,g of degree at most d have disjoint supports,

    max_i max(RelInf_i(f), RelInf_i(g)) >= 1 / (1024 d^8).

The smaller constant in the theorem avoids any boundary-equality question.

## 1. A bounded polynomial cannot switch sign on too many disjoint blocks

We use the classical univariate Markov inequality in the following normalization. If P is a real polynomial of degree at most m with |P(t)| <= 1 for 0 <= t <= 1, then |P'(t)| <= 2m^2 throughout that interval. This is the usual inequality ||Q'||_[−1,1] <= m^2 ||Q||_[−1,1], after an affine change of variable. A primary mathematical source recording this normalization is Kothari et al., arXiv:2601.08727v3, Theorem 1; the classical inequality is the only approximation-theory theorem used below.

Lemma 1. Suppose R is a real function on {0,1}^b with a multilinear representation of degree at most m, satisfying

    |R(y)| <= 1 for all y,
    R(0) = 1,
    R(e_j) <= 0 for j = 1,...,b.

Then b <= 2m^2.

Proof. Let Y_1,...,Y_b be independent Bernoulli(t) bits, and put P(t) = E R(Y). In the multilinear expansion, replace each monomial of size k by t^k. Therefore P is a polynomial of degree at most m. Since it is an average of values in [-1,1], |P(t)| <= 1 for every real t in [0,1]. Its constant coefficient is R(0) = 1 and its linear coefficient is

    P'(0) = sum_j (R(e_j) - R(0)) <= -b.

Markov's inequality yields b <= |P'(0)| <= 2m^2. This proves the lemma. Changing R to -R gives the identical conclusion when R(0) = -1 and every R(e_j) >= 0. [End of proof.]

## 2. A depth-16d^4 separator for disjoint polynomial supports

The following is an explicit-constant version of Li–Li–Li–Liu, Lemma 3.5. It applies to arbitrary real values, and permits inputs on which both polynomials vanish.

Lemma 2. If p,q are real multilinear polynomials of degree at most d on {0,1}^n and p(x)q(x) = 0 at every vertex, there is a deterministic decision tree of depth at most 16d^4 whose output h belongs to {0,1} and satisfies

    h(x) = 1 whenever p(x) != 0,
    h(x) = 0 whenever q(x) != 0.

The tree is defined on every vertex, including their common zero set, where either output is allowed. It never queries an already queried coordinate.

Proof. Construct the tree recursively on restricted subcubes. If p is identically zero, output 0; if q is identically zero and p is not, output 1. These rules assign an arbitrary valid value when both are zero.

Otherwise both are nonzero. Neither can be a nonzero constant, since it would force the other to vanish identically. Let D = max(deg p, deg q), so 1 <= D <= d. Multilinearize s = p^2 - q^2 as a function on the remaining cube; its degree is at most 2D. Choose z maximizing |s(z)|. This maximum is positive: at some vertex one of p,q is nonzero, and disjointness forbids cancellation of their squares. At z exactly one of p,q is nonzero.

Assume first that p(z) != 0. Then s(z) > 0 and q(z) = 0. Let M_1,...,M_b be an inclusion-maximal family of pairwise disjoint supports of maximum-degree monomials of q. Here “maximum-degree” means degree exactly deg q, and inclusion-maximality refers to the family, not to the individual monomials. This finite family is nonempty.

For each j, fix all coordinates outside M_j to their values in z. The coefficient of the monomial indexed by M_j is unchanged: a contribution from a different monomial would require a strict superset of M_j, which cannot occur at maximum degree. The restricted q is consequently nonzero. Since q(z) = 0, there is a nonempty E_j subset M_j such that q(z flipped on E_j) != 0. The E_j are pairwise disjoint. At this changed vertex p vanishes, and therefore s is strictly negative.

Encode simultaneous choices of these disjoint flips by b bits y and set

    R(y) = s(z flipped on the union of E_j with y_j = 1) / |s(z)|.

Every original coordinate is fixed or is an affine function of one y_j. Substitution followed by multilinearization cannot increase degree, so deg R <= 2D. The choice of z gives |R(y)| <= 1. Also R(0) = 1 and R(e_j) < 0. Lemma 1 gives b <= 2(2D)^2 = 8D^2.

The set H = union_j M_j has at most 8D^2 deg(q) <= 8d^3 coordinates. By maximality of the disjoint family, H intersects every maximum-degree monomial of q. Query all still-free coordinates in H. For every assignment of their answers, all former maximum-degree monomials lose at least one variable; lower-degree monomials cannot gain degree. Thus the restriction of q is either zero or has strictly smaller degree. The restricted p cannot gain degree.

If q(z) != 0 instead, interchange p and q, or equivalently use -s. The same construction decreases deg p.

At every nonterminal stage deg p + deg q decreases by at least one. It begins at most 2d and is a nonnegative integer while both functions remain nonzero. Hence there are at most 2d such stages on a branch. Each stage queries at most 8d^3 coordinates. The depth is therefore at most 16d^4. Branches off the promised support are explicitly handled by the termination rules, so this is a total decision tree. [End of proof.]

An affine change x_i = 2z_i - 1 transfers this lemma to {-1,1}^n without changing polynomial degrees or tree depth.

## 3. A covariance inequality for an adaptive decision tree

For uniform X on {-1,1}^n, write X^(i) for X with coordinate i independently resampled from a uniform sign. Resampling includes a probability 1/2 of leaving that coordinate unchanged. For any real function u on the finite cube, define

    A_i(u) = E |u(X) - u(X^(i))|.

Lemma 3. Let a deterministic decision tree compute h:{-1,1}^n -> {0,1}. Assume it queries each coordinate at most once on a branch. Let r_i be the probability, under uniform input, that it queries i. Then, for every real u on the cube,

    |Cov(h(X),u(X))| <= (1/2) sum_i r_i A_i(u).

No boundedness, sign condition, low-degree condition, or tree-computability condition on u is needed.

Proof. Let X,Y be independent uniform cube points. Run the tree only on X. Write the queried coordinates, in their order, as I_1,...,I_L, where the random length L is the depth of the reached leaf. Define Z_0 = X and obtain Z_t by replacing coordinates I_1,...,I_t of X by the corresponding coordinates of Y. The replacement sequence does not change which queries are made: those queries always come from the original run on X.

First consider a complete transcript tau, meaning the sequence of queried coordinates, all their observed X-values, and the final leaf. Its event is exactly a cylinder fixing those queried coordinates. Conditional on tau, the unqueried coordinates of X are still mutually independent uniform signs. The queried coordinates of Y are independent uniform signs as well, independent of X and tau. Consequently Z_L, conditional on tau, is uniform on the whole cube. In particular, since h(X) is determined by tau,

    E[(h(X)-1/2) u(Z_L)] = E[h(X)-1/2] E[u(X)].

Subtracting this identity from E[(h(X)-1/2)u(X)] and telescoping gives

    Cov(h,u) = E[(h(X)-1/2) sum_{t=1}^L (u(Z_{t-1})-u(Z_t))].

Since |h(X)-1/2| = 1/2,

    |Cov(h,u)| <= (1/2) sum_t E[1_{L>=t} |u(Z_{t-1})-u(Z_t)|].

To evaluate a summand, condition on a pre-query transcript sigma of length t-1 at which the algorithm has not stopped. It fixes exactly the already queried X-coordinates and determines the next coordinate i. The other X-coordinates are still independent uniform signs. All previously queried coordinates appearing in Z_{t-1} have instead been supplied from Y; those signs are independent of sigma. Therefore, conditional on sigma, Z_{t-1} is uniform on the entire cube. Moreover Y_i is an independent uniform sign because i has not previously been queried. It follows that the conditional pair (Z_{t-1},Z_t) has exactly the law of (X,X^(i)).

Thus the last sum equals

    (1/2) sum_{t,i} Pr[L>=t and I_t=i] A_i(u)
      = (1/2) sum_i r_i A_i(u).

This also covers variable stopping times, since the finite sum runs over all possible pre-query transcripts. It proves the lemma. [End of proof.]

If the tree has depth at most T, then sum_i r_i = E L <= T.

## 4. Relating the resampling quantities to Fourier influences

Lemma 4. If a is a nonzero real function on the cube, and u = a^2/||a||_2^2, then

    A_i(u) <= 2 sqrt(RelInf_i(a)(1-RelInf_i(a)))
           <= 2 sqrt(RelInf_i(a)).

Here relative influence is defined by the full Fourier expansion, whether or not a has low degree.

Proof. Normalize ||a||_2 = 1 and let X^flip_i denote the point with sign i flipped. Put rho = RelInf_i(a). Parseval gives

    E (a(X)-a(X^flip_i))^2 = 4rho,
    E (a(X)+a(X^flip_i))^2 = 4(1-rho).

An independent resampling flips a sign with probability 1/2. Factoring the difference of squares and applying Cauchy–Schwarz yields

    A_i(a^2)
      = (1/2) E |a(X)^2-a(X^flip_i)^2|
      <= (1/2) sqrt(4rho) sqrt(4(1-rho))
      = 2 sqrt(rho(1-rho)).

Normalization recovers the statement. [End of proof.]

## 5. Completing the theorem

Suppose, to the contrary, that f(x)g(x) = 0 everywhere. Set

    u = f^2/||f||_2^2,   v = g^2/||g||_2^2,
    delta = max_i max(RelInf_i(f), RelInf_i(g)).

Both u and v have expectation 1. Lemma 2 supplies a separator h computed by a tree of depth T <= 16d^4. Pointwise, hu = u and hv = 0. Writing mu = E h, we obtain

    Cov(h,u) = 1-mu,     Cov(h,v) = -mu.

Their absolute values sum to exactly 1, even when the supports do not cover the cube. Lemmas 3 and 4 imply

    1-mu <= sum_i r_i sqrt(RelInf_i(f)) <= T sqrt(delta),
    mu   <= sum_i r_i sqrt(RelInf_i(g)) <= T sqrt(delta).

Adding gives

    1 <= 2T sqrt(delta) <= 32d^4 sqrt(delta).

Therefore delta >= 1/(1024d^8). Under the theorem's assumption delta <= 1/(4096d^8), the displayed upper bound is at most 1/2, a contradiction. The supports must intersect. [End of proof.]

## Source credit and boundaries of the conclusion

- Per Austrin's exact two-polynomial question and the relative-influence convention are in the 2025 Oberwolfach report, p. 445: https://doi.org/10.4171/owr/2025/9 .
- The decisive disjoint-support separator is credited to Li, Li, Li, and Liu, Lemma 3.5: https://arxiv.org/abs/2608.03824v1 . This note verifies that argument and exposes a numerical depth bound rather than merely invoking the cryptographic conclusion.
- The Markov/Bernoulli-symmetrization input is in Kothari, Kovacs-Deak, Wang, and Yang, Theorem 1, Fact 5, and Corollary 1: https://arxiv.org/abs/2601.08727v3 .
- The earlier distribution formulation appears in Austrin, Chung, Chung, Fu, Lin, and Mahmoody, *On the Impossibility of Key Agreements from Quantum Random Oracles*, CRYPTO 2022, Conjecture 1.2 and Section 5.2: https://doi.org/10.1007/978-3-031-15979-4_6 . This proof's stated target remains the exact two-polynomial Boolean-cube formulation.

The 2022 exponential argument uses the strict hypothesis delta < 2^(-d)/d. The non-strict endpoint printed in the 2025 report cannot hold uniformly starting at d=1: f=1+x_1 and g=1-x_1 have disjoint supports and both relative influences equal to 1/2. This endpoint issue does not affect the theorem proved here. Likewise, the source's inverse-quadratic obstruction is a necessary restriction, not a previously proved sufficient threshold.

Supplementary finite computations used during verification tested the implementation of the separator, the hybrid identity, and the constants; executable checks are not included in this prose edition. They are not the proof of any universal mathematical statement. The universal argument is the sequence of four lemmas and the contradiction above.
