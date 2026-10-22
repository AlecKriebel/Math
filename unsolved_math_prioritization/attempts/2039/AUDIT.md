# Elementary verification of the analytic inputs

This is an AI-assisted, unrefereed authored written-proof audit edition. Acceptance records an independent internal AI audit of the cited prior theorem and its classical analytic inputs. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored proof audit, complete analytic supplement and all substantive acceptance qualifications are retained. Executable code, raw datasets and finite-check rows, copied source PDFs or text, source renderings, raw search responses and private coordination material are not distributed. The optional historical finite checks cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks are supporting evidence only; the mathematical acceptance rests on the written proof.

This supplement independently supplies the exact prime bounds used in the written-proof audit of Erdős Problem 306. It follows elementary factorial and Chebyshev identities, and does not use author code, formal-verification claims, the prime number theorem, or unproved hypotheses. Ramanujan's exact inequality was also verified in equation (14) of the original primary scan.

## 1. The primorial bound

For an integer n >= 1 let P(n) be the product of primes at most n. We prove P(n) <= 4^n by strong induction. The cases n = 1,2 are immediate. If n = 2m >= 4, n is composite and P(n) = P(n-1) < 4^n.

If n = 2m+1 >= 3, every prime p in (m+1,2m+1] divides the integer binomial(2m+1,m): it appears in the numerator and not in either denominator factorial. Their product is therefore at most this binomial coefficient. The two middle coefficients in row 2m+1 are equal and their sum is at most 2^(2m+1), giving binomial(2m+1,m) <= 2^(2m) = 4^m. By induction,

P(2m+1) <= P(m+1) binomial(2m+1,m)
          <= 4^(m+1) 4^m = 4^(2m+1).

For real x >= 2, P(x) = P(floor x) <= 4^(floor x) <= 4^x. This is the precise form used in Li's estimate for the number of row residue patterns.

## 2. Two factorial bounds with all ranges justified

For real x > 0 put

F(x) = log(floor(x)!) - 2 log(floor(x/2)!).

With n = floor(x), floor(x/2) = floor(n/2), so F(x) is the logarithm of n!/(floor(n/2)!)^2. We prove

F(x) < 3x/4 for x > 0,
F(x) > 2x/3 for x > 300.

### Upper bound

For n = 2k, the factorial ratio is binomial(2k,k) <= 2^(2k). Since log 2 < 3/4, this gives F(x) < 3n/4 <= 3x/4 when n > 0. For n = 0, F(x) = 0 < 3x/4.

For odd n = 2k+1 define R_k = (2k+1)!/(k!)^2. The values for n = 1,3,5,7,9 are 1,6,30,140,630. They are each smaller than (21/10)^n. The exponential series gives

exp(3/4) > sum_{j=0}^4 (3/4)^j/j! > 21/10.

Thus these five cases satisfy R_k < exp(3n/4). For k >= 4,

R_{k+1}/R_k = (2k+3)(2k+2)/(k+1)^2
              = 4 + 2/(k+1) <= 22/5
              < (21/10)^2 < exp(3/2).

Induction advances n by 2 and proves the upper bound for every odd n. This argument also verifies log 2 < 3/4, since exp(3/4) > 21/10 > 2.

### Lower bound

For even n, the middle binomial coefficient is a maximum of the n+1 coefficients summing to 2^n, so the factorial ratio is at least 2^n/(n+1). For odd n = 2k+1, it equals (k+1) binomial(n,k), which is at least binomial(n,k) and therefore also at least 2^n/(n+1). Consequently

F(x) >= n log 2 - log(n+1).

Two elementary bounds suffice: log 2 > 69/100 and log 301 < 6. For the first, the positive expansion

log((1+t)/(1-t)) = 2(t + t^3/3 + t^5/5 + ...)

at t = 1/3 gives log 2 > 56/81 > 69/100. For the second, the preceding exponential lower bound gives exp(6) > (21/10)^8 > 301.

At n = 300,

n log 2 - log(n+1) > 300(69/100) - 6 = 201 > (2/3)301.

The difference g(n) = n log 2 - log(n+1) - 2(n+1)/3 strictly increases for n >= 300, because

g(n+1)-g(n) = log 2 - 2/3 - log(1+1/(n+1))
             > 69/100 - 2/3 - 1/301 > 0.

Hence F(x) > 2(n+1)/3 > 2x/3 for every x > 300, since n <= x < n+1. The stated threshold is justified without an unquantified use of Stirling's formula.

## 3. Recovering the exact Ramanujan inequality

Define theta(x) = sum_{p <= x} log p and psi(x) = sum_{p^k <= x} log p, with both zero below 2. The sums are finite for each x. Prime factorization gives

psi(x) = sum_{k >= 1} theta(x^(1/k)),
log(floor(x)!) = sum_{j >= 1} psi(x/j).

Separating the even indices in these identities gives two finite alternating sums:

psi(x) - 2psi(sqrt(x)) = theta(x) - theta(sqrt(x)) + theta(x^(1/3)) - ...,
F(x) = psi(x) - psi(x/2) + psi(x/3) - psi(x/4) + ... .

Monotonicity of theta and psi implies the alternating-sum bounds

psi(x) - 2psi(sqrt(x)) <= theta(x) <= psi(x),
psi(x)-psi(x/2) <= F(x) <= psi(x)-psi(x/2)+psi(x/3).

Using F(x) < 3x/4 in the second inequality and telescoping over x, x/2, x/4, ... gives psi(x) < 3x/2 for x > 0. For x > 300 the lower factorial estimate gives

2x/3 < psi(x)-psi(x/2)+psi(x/3).

On the other hand, the first alternating-sum bound and theta(x/2) <= psi(x/2) show

psi(x)-psi(x/2)+psi(x/3)
<= theta(x)-theta(x/2)+2psi(sqrt(x))+psi(x/3)
< theta(x)-theta(x/2)+3sqrt(x)+x/2.

Subtracting the error terms proves

theta(x)-theta(x/2) > x/6 - 3sqrt(x), for every real x > 300.

The prime-counting consequence is obtained by bounding each log p in the left-hand sum by log x. For x >= 126^2 = 15,876, the right side is at least x/7, so

pi(x)-pi(x/2) >= x/(7 log x).

This independently verifies the analytic input used by Li. It closes the mathematical dependency at the written-proof level; it does not import or discharge any hypothesis inside an uninspected Lean project.

## Source and verification notes

Ramanujan's original paper uses nu for the function denoted theta here. The primary collected-paper scan reproduces *A proof of Bertrand's postulate*, J. Indian Math. Soc. 11 (1919), 181-182, at collected-paper pages 208-209. Equation (14) is exactly the final inequality above. Both scan pages were visually inspected.

- Original scan: https://www.imsc.res.in/~rao/ramanujan/CamUnivCpapers/Cpaper24/page1.htm
- Second page: https://www.imsc.res.in/~rao/ramanujan/CamUnivCpapers/Cpaper24/page2.htm
- Searchable retypeset primary text: https://ramanujan.sirinudi.org/Volumes/published/ram24.pdf

The finite rational comparisons appearing above were additionally checked by an auditor-authored exact-arithmetic script. The proof itself is the symbolic argument, not the script's successful exit status.
