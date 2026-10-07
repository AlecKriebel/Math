# Four-site, small-time negative association for step ASEP

Problem: 9600004 / AMR-095-0004, queue rank 933.

Status: rigorous local partial result; the full infinite-lattice, all-time question is not settled here. No novelty claim is made.

## Exact target and theorem

Let eta_t be nearest-neighbor exclusion on the integers. Each occupied site attempts a jump right at rate p and left at rate q; attempts into occupied sites are suppressed. Initially eta_0(x)=1 exactly when x<=0. The rates are spatially constant.

Liggett's October 15, 2012 Problem 4 asks for negative association of the entire time-t law, for every time, when p>q. His introductory convention is an irreducible transition-probability kernel; for this nearest-neighbor model that convention gives 0<q<p and p+q=1. General positive rates are equivalent by deterministic time rescaling. The theorem below also includes q=0 and q=p, as extensions.

**Local theorem.** For p>0 and 0<=q<=p, put delta=1/10837981440. If 0<=p*t<=delta, the marginal of eta_t on C={-1,0,1,2} is negatively associated. Thus Cov(f,g)<=0 for every two increasing real-valued functions with disjoint coordinate supports contained in C. When both functions are nonconstant and t>0 in this interval, the covariance is strictly negative.

This is a theorem about the actual infinite system, not just a reflecting finite chain. It does not establish negative association on larger sets or at later times, and does not establish the strong Rayleigh property.

## 1. Reduction to 174 increasing-event tests

A function on a finite Boolean cube is increasing precisely when all its upper level sets are increasing events. Decomposing a real-valued function into a constant plus positive multiples of indicators of those upper level sets shows that it is enough to test increasing-event indicators on disjoint supports.

For a nonempty support A of size 1, 2, or 3, the numbers of nonempty, nonfull increasing events are respectively 1, 4, and 18. Enumerate all nonempty disjoint supports A,B within C, counting each unordered pair once. There are:

- 6 singleton/singleton tests;
- 12*4=48 singleton/two-site tests;
- 4*18=72 singleton/three-site tests;
- 3*4*4=48 two-site/two-site tests.

The total is 174. Redundant coordinates in an event are allowed; this only repeats some inequalities and omits none. Constant functions have zero covariance.

## 2. Exact generator calculation

Normalize time to tau=p*t and write r=q/p. Let G_r be the generator with right rate 1 and left rate r. For a configuration s and each adjacent unequal pair, the generator swaps the pair at rate 1 for 10 and r for 01, and subtracts the same rate on the diagonal.

The supplied checker works in Q[r], using exact rational coefficients. Starting at the step configuration, let v_0 be its unit mass and recursively put v_(j+1)=v_j Q, with Q the finite-chain generator on the sites {-7,...,8}. For a cylinder indicator h, the coefficient of tau^j in its expectation is v_j h/j!.

For j<=6 these are exactly the infinite-volume derivatives. Initially the only active bond is (0,1). After at most j actual swaps, all deviations from the step, and all active bonds, remain within a distance at most j+1 from this interface. A length-j generator product also allows diagonal factors, which do not enlarge that region. Consequently no boundary bond of {-7,...,8} can contribute to any generator product of length at most 6. Thus the finite calculation computes G_r^j h at the infinite step exactly, with no numerical truncation or limiting approximation. The checker additionally reproduces the full certificate on {-8,...,9}.

For each indicator pair (a,b), compute

c_j(r) = E_j[ab] - sum_(i=0)^j E_i[a] E_(j-i)[b],

where E_j[h] denotes the exact Taylor coefficient above. The certificate includes c_0,...,c_6 as rational polynomials in r. In every one of the 174 cases, all coefficients before a first index k vanish identically in r, and c_k is a negative constant, independent of r. The complete histogram (order, coefficient, multiplicity) is:

| k | c_k | multiplicity |
|---|---|---|
| 1 | -1 | 33 |
| 2 | -1/2 | 50 |
| 3 | -1/2 | 34 |
| 3 | -1/3 | 18 |
| 4 | -1/12 | 15 |
| 4 | -1/3 | 8 |
| 4 | -1/4 | 8 |
| 5 | -1/12 | 2 |
| 5 | -1/24 | 2 |
| 5 | -1/8 | 2 |
| 6 | -1/144 | 2 |

For example, Cov(eta_t(-1), eta_t(0)*eta_t(1)*eta_t(2)) = -tau^6/144 + O(tau^7). This singleton/three-site test goes beyond pairwise occupation correlations.

The event enumeration and all coefficients are recomputed by check_certificate.py; they are not trusted inputs. The polynomial indeterminate r is never numerically sampled in this proof.

## 3. Uniform remainder bound

Suppose 0<=r<=1. If h is supported in an interval of length m, only its m+1 touching bonds contribute to G_r h, and each effective swap has rate at most 1. Hence

||G_r h||_infinity <= 2(m+1)||h||_infinity.

The support interval grows by at most two sites at each application. For any of our indicators a,b,ab, whose supports lie in the four-site interval C, define

D_j = 2^j product_(ell=0)^(j-1) (5+2*ell), with D_0=1.

Then ||G_r^j h||_infinity<=D_j. The Markov semigroup is a sup-norm contraction, so derivatives of E[h(eta_tau)] of order j have absolute value at most D_j.

One can justify these derivative and Taylor bounds without an infinite-volume domain assumption: first work with reflecting finite intervals, where the semigroup is a matrix exponential. The bounds above are uniform in the finite interval; the initial derivatives through order 6 stabilize as shown in Section 2. Pass the Taylor inequalities to the infinite system using the usual nearest-neighbor Poisson graphical construction. For a fixed finite cylinder and fixed time, a discrepancy from a receding boundary requires a chronological chain of increasingly many neighboring clock rings. Its probability tends to zero by the factorial bound on such ordered chains. Therefore the cylinder expectations converge, and the uniform Taylor remainder bound passes to the limit.

For H(tau)=Cov(a(eta_tau),b(eta_tau)), the product rule gives

|H^(j)(tau)| <= D_j + sum_(ell=0)^j binom(j,ell) D_ell D_(j-ell)
                 <= (1+2^j)D_j,

since D_ell D_(j-ell)<=D_j. This applies uniformly to 0<=r<=1. If the first nonzero coefficient is c_k=-a with a>0, Taylor's theorem therefore gives

H(tau) <= -a*tau^k + [(1+2^(k+1))*D_(k+1)/(k+1)!]*tau^(k+1).

For 0<tau<=a*(k+1)!/[2*(1+2^(k+1))*D_(k+1)], this is at most -a*tau^k/2<0. Taking the minimum over all certificate cases gives exactly delta=1/10837981440. At tau=0 the law is deterministic, so all covariances vanish. Section 1 now proves the stated theorem.

## 4. What remains

The bound concerns one specified four-site marginal and a very short uniform time interval. It cannot be restarted at delta, because the evolved law is not the original deterministic step and no appropriate asymmetric preservation theorem has been proved here. It also gives no common time interval over arbitrary finite coordinate sets. Either a global structure theorem or an actual positive covariance witness for disjoint increasing cylinder functions would be needed to resolve the original question. Mere pairwise covariance checks, an equilibrium argument, or a determinantal formula lacking the necessary kernel hypotheses would not suffice.

## References

1. Thomas M. Liggett, Some Open Problems, October 15, 2012, Problem 4, PDF page 2: https://web.archive.org/web/20150919235903id_/http://www.math.ucla.edu/~tml/open.pdf
2. Julius Borcea, Petter Branden, Thomas M. Liggett, Negative dependence and the geometry of polynomials, J. Amer. Math. Soc. 22 (2009), 521-567; https://arxiv.org/abs/0707.2340 . Theorem 5.2 concerns symmetric dynamics and strongly Rayleigh initial laws; Remark 5.3 gives a different asymmetric counterexample with a random initial law.
