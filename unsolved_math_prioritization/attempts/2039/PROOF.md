# Independent audit of the semiprime unit fraction theorem

This is an AI-assisted, unrefereed authored written-proof audit edition. Acceptance records an independent internal AI audit of the cited prior theorem and its classical analytic inputs. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete authored proof audit, complete analytic supplement and all substantive acceptance qualifications are retained. Executable code, raw datasets and finite-check rows, copied source PDFs or text, source renderings, raw search responses and private coordination material are not distributed. The optional historical finite checks cannot be reproduced from this edition alone.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks are supporting evidence only; the mathematical acceptance rests on the written proof.

## Conclusion

The written argument in Shisheng Li, *Unit fractions with semiprime denominators: an elementary proof of Erdős Problem #306*, arXiv:2609.32140v1, proves the full requested statement: every positive rational whose reduced denominator is squarefree is a finite sum of distinct reciprocals of products of exactly two distinct primes. This audit found no mathematical gap in the written proof. No correction patch is required.

This is a mathematical acceptance of the inspected written argument with its classical inputs, not a claim of journal acceptance or independently reproduced formal verification. The paper's reported Lean theorem retains Ramanujan's inequality as a hypothesis; this audit neither retrieved nor ran the Lean project. That formal boundary does not make the written mathematical theorem conditional on an unproved conjecture: the precise inequality is equation (14) of Ramanujan's 1919 paper and has been checked against the primary scan. The accompanying analytic supplement also supplies a separate elementary derivation.

Audit date: 11 October 2026. Li's complete 13-page PDF was read and every page visually inspected. Its SHA256 is 9983c8340b91610e082bbe3161cea13385745add23e6cb41f3b12be52d91c4d8 and its size is 364,512 bytes. The current official arXiv abstract page lists v1, submitted 26 September 2026 at 01:53:41 UTC, and no journal-reference field. These facts establish the inspected version and stated public status, not refereeing.

## 1. Scope and exact target

Write the target in reduced form as a/b, where a and b are positive integers and b is squarefree. The conclusion requires finitely many pairwise distinct integers n, each equal to pq with p and q different primes, and sum 1/n = a/b. No repeated denominator, prime square, unrestricted semiprime, integer-only conclusion, or three-prime denominator is substituted.

The squarefree condition is necessary: the least common multiple of finitely many squarefree denominators is squarefree, and the reduced denominator of their sum divides that least common multiple. The paper establishes sufficiency.

The main proof is an existence proof with effective but extremely large cutoffs. It does not promise an efficient representation algorithm or a useful bound on the number or sizes of denominators. Its finite Fourier transform is exact; it does not assume a limit theorem, a prime number theorem, unproved independence of residues, or random cancellation.

## 2. The two prime inputs

Let theta(x) = sum_{p <= x} log p and pi(x) count primes at most x.

The required input statements are:

1. The primorial P(x) = product_{p <= x} p is at most 4^x for x >= 2.
2. For all sufficiently large x, pi(x) - pi(x/2) >= x/(7 log x).

The first is a standard elementary primorial bound. A complete short induction appears in the analytic supplement, so the audit does not depend on silently identifying every numerical detail of the 1932 source with the modern formulation. The inspected page 195 of Erdős's cited 1932 paper explicitly proves a closely related bound with the primes at most 10 omitted; it is sufficient up to an immaterial fixed factor, while the supplement proves the precise stronger formulation used by Li.

For the second, Ramanujan's original notation nu(x) is exactly theta(x), not the second Chebyshev function psi(x). The primary scan states

theta(x) - theta(x/2) > x/6 - 3 sqrt(x), for real x > 300.

This is equation (14), followed by the prime-counting consequence in equation (17). Since every term in the theta difference is at most log x, division gives the required pi estimate as soon as sqrt(x) >= 126, hence for x >= 15,876. There is no unjustified replacement of psi by theta, and no missing change of logarithm base.

### The wide interval has enough reciprocal mass

For t = log_2 y, retain the integer dyadic blocks with ceil(8t+1) <= j <= floor(9t). Each lies in (y^8,y^9], and contributes at least 1/(7 j log 2) to the reciprocal prime sum. The sum of 1/j over this range tends to log(9/8), so the reciprocal mass eventually exceeds 1/50. The strict margin is genuine: log(9/8)/(7 log 2) is about 0.02428, greater than 0.02.

For an explicit check, when t >= 16 the harmonic sum is at least log(9t/(8t+2)), hence at least log(72/65). The exact integer inequality 72^50 > 2^7 * 65^50 shows log(72/65)/(7 log 2) > 1/50. Every dyadic endpoint in this argument is already above 15,876. Thus y >= 2^16 is sufficient for this particular mass estimate. The endpoints in the inclusion of dyadic blocks have the correct direction.

## 3. Reduction to a small target without repeated denominators

It is enough to prove the following stronger small-target statement: for a fixed rational tau in (0,1/400] with squarefree reduced denominator, every sufficiently large integer y admits a representation using primes v <= 2y^2 and y^8 < u <= y^9.

Given arbitrary a/b, choose a prime q not dividing ab with a/(bq) <= 1/400. Its reduced denominator remains squarefree. Apply the small-target statement q times to x = a/(bq), choosing the scales successively so that y_{i+1}^8 > y_i^9 and all scales exceed its threshold. This is possible because the small-target theorem works for every sufficiently large y, not merely for one unspecified y.

In each resulting denominator vu, the factor u is the unique larger prime factor. The intervals containing these larger factors are disjoint across the q representations. Unique prime factorization therefore rules out any denominator collision, even if a large prime from an earlier scale later occurs as a small-side prime. The q finite representations add to qx = a/b. The auxiliary prime q itself may recur as a small-side factor; this does not repeat a product when the larger factors differ. This proves the rational-target reduction and global distinctness, including integer targets with b = 1.

## 4. Construction and tuning

Fix a reduced tau = a/b in (0,1/400], and let B be the primes dividing b. Then b > 1. Choose integer y larger than every prime in B and define

- W = primes in (y^2,2y^2];
- V = {2} union B union W;
- U(Y) = primes in (y^8,Y], with y^8 < Y <= y^9;
- H = sum_{v in V} 1/v;
- H_0 = 3/2 + sum_{p in B} 1/p.

These are sets, so if 2 divides b it is counted only once in V. For sufficiently large y,

|W| >= y^2/(8 log y),
product_{v in V} v <= 2b * 16^(y^2),
1/2 <= H <= H_0.

The first follows from the pi bound at x = 2y^2; the logarithmic comparison is valid for y >= 2^(7/2). The second deliberately overcounts any overlap between {2} and B, so the inequality remains valid. For the third, W contains at most y^2 integers and every member exceeds y^2, giving sum_W 1/w <= 1. The upper bound H_0 is independent of y, a necessary point in the later exponential comparison.

Let A = {vu : v in V, u in U(Y)}. The two sides are disjoint because v <= 2y^2 < y^8 < u. Each ordered pair (v,u) yields a unique product, and each product has two distinct prime factors. Define half the total reciprocal load by

mu(Y) = (H/2) sum_{u in U(Y)} 1/u.

The full interval has mu >= (1/4)(1/50) = 1/200 >= 2tau. Adding one column changes mu by H/(2u) < H/(2y^8), which is less than tau/2 for sufficiently large y. The first column therefore has mu < tau, while the full interval exceeds tau. Stop at the last prime endpoint with mu <= tau. There is a next prime, and its addition crosses tau. Consequently

0 <= tau - mu < H/(2y^8),
mu >= tau/2,
|U| >= tau y^8/H.

The last inequality follows from sum_U 1/u = 2mu/H >= tau/H and 1/u < 1/y^8. Equality of mu and tau causes no difficulty; then the gap is zero.

Every subset S of A has reciprocal sum sigma(S) between 0 and 2mu <= 2tau <= 1/2. If sigma(S) is congruent to tau modulo 1, their difference is an integer strictly between -1 and 1. It is therefore zero. This is exact equality of rational numbers, not an approximation.

All thresholds may depend on b alone: tau >= 1/b, and H <= H_0 depends on B alone. There is no uniform-in-tau claim left unsupported.

## 5. Exact finite Fourier encoding

Let L be the product of the distinct primes in V union U. Squarefreeness of b and inclusion B subset V give b dividing L. Every vu divides L as well. Therefore L(sigma(S)-tau) is an integer, allowing exact root-of-unity orthogonality.

Let N count subsets with sigma(S) congruent to tau modulo 1, let e(z) = exp(2 pi i z), and let h run over -L/2 < h <= L/2. Expanding over all subsets gives

N / 2^|A| = (1/L) sum_h e(-h tau) Phi(h),
Phi(h) = product_{v in V,u in U} (1 + e(h/(vu)))/2.

This counts each subset once and includes the empty subset. Since tau is positive and below 1, the empty subset cannot be a solution. The use of the even modulus L is harmless; the half-open frequency interval contains exactly L residues, with one representative of the endpoint class.

Chinese remaindering identifies a frequency with independent residues xi_v modulo v and zeta_u modulo u. The phase h/(vu) modulo 1 depends exactly on the pair (xi_v,zeta_u). Set

F_u(xi,zeta_u) = product_{v in V} |cos(pi h/(vu))|,
S_u(xi) = sum_{zeta_u mod u} F_u(xi,zeta_u).

The product is well-defined because the absolute cosine has period 1 in its argument h/(vu). Holding the row residues xi fixed, the column residues vary independently under CRT. Therefore

sum_h |Phi(h)| = sum_xi product_{u in U} S_u(xi).

This is a finite algebraic identity. It is the reason column estimates can be multiplied without multiplying by the entire enormous number of frequencies.

## 6. Classification and the major contribution

Call xi coherent if xi_v is the residue of one integer M with |M| <= y^7 for every v. Such M is unique: the product of the W primes exceeds (y^2)^|W| >= exp(y^2/4), which eventually exceeds 2y^7+1. Two possible M would differ by a multiple of this product and have absolute difference at most 2y^7.

There are precisely three disjoint cases:

1. Coherent rows and every column equal to M modulo u.
2. Coherent rows and at least one different column label.
3. Incoherent rows.

In case 1, CRT gives h congruent to M modulo L, and |M| < L/2 gives h = M in the selected frequency interval. Conversely every |h| <= y^7 belongs to case 1. Thus these are exactly the small integer frequencies, with no duplicated coherent pattern.

For these frequencies the elementary identity (1+e(z))/2 = e(z/2) cos(pi z) gives

e(-M tau) Phi(M) = e(M beta) P(M),
beta = mu - tau,
P(M) = product_{v,u} cos(pi M/(vu)).

Since |M|/(vu) <= 1/(2y) < 1/2, all cosine factors of P(M) are positive. Also P(-M) = P(M), and P(0) = 1. Pairing M and -M yields the real term 2 cos(2 pi M beta) P(M). The tuning estimate gives |2 pi M beta| <= pi H/y < pi/2 once y > 2H_0. Hence every pair is nonnegative and the major contribution is at least 1/L, furnished by M = 0 alone. There is no unsupported claim that arbitrary Fourier coefficients are positive.

## 7. Separation of two labels in one column

The elementary bound |cos(pi z)| <= exp(-2 ||z||^2), with ||z|| the distance to the nearest integer, follows from sin(pi t) >= 2t for 0 <= t <= 1/2. Its constant and endpoints are correct.

If two labels in a column u differ by nonzero s modulo u while the row residues stay fixed, their phase difference in row v is s times v^{-1}/u modulo 1. Indeed, h-h' = vk and vk is congruent to s modulo u. No multiplier from L or omitted CRT factor is needed.

Set delta = 1/(400 log y) and epsilon = exp(-|W| delta^2/8). The lower bound on |W| gives

epsilon <= exp(-y^2/(10,240,000 log^3 y))
        <= exp(-y^2/(20,000,000 log^3 y)) = E(y).

The paper's rounded constant is weaker than the one obtained directly, in the safe direction.

Take the balanced representative |s| <= u/2. If ||s w^{-1}/u|| <= delta for w in W, choose its balanced numerator t with |t| <= delta u. The relation tw = s + u ell gives

|ell| <= 2 delta y^2 + 1/2.

There are at most 4 delta y^2 + 2 integers in that interval, including its endpoints. Each s + u ell is nonzero since s is not divisible by u, and for large y its absolute value is at most y^11. Six different primes greater than y^2 would have product greater than y^12, so each such integer has at most five possible prime divisors from W. Negative integers and repeated prime powers do not change this argument. Thus the number of these nearly invisible rows is at most

5(4 delta y^2 + 2) = y^2/(20 log y) + 10
                      <= y^2/(16 log y) <= |W|/2.

At least |W|/2 rows consequently see phase differences greater than delta. In each, at least one of the two phases is greater than delta/2 in distance from an integer. Multiplying the cosine bound over these rows proves

F_u(xi,zeta) F_u(xi,zeta') <= exp(-|W| delta^2/4) = epsilon^2.

Hence at most one label has weight greater than epsilon. If one specified label has every W-phase at most delta/2, every other label alone has weight at most epsilon^2, hence at most epsilon. The latter assertion uses the same visible rows but forces the larger phase to belong to the other label. Both versions of Li's separation lemma are valid.

## 8. The single-column rigidity argument

Set delta_a = 1/(8y^2). Suppose one column label makes every row phase have distance at most delta_a. For each v take the balanced integer J_v modulo vu realizing the row and column residues. Then

|J_v| <= delta_a vu <= u/4,
J_v congruent to zeta_u modulo u.

Every difference J_v-J_{v'} is a multiple of u and has absolute value at most u/2 < u. All J_v therefore equal one integer M. In the row v = 2,

|M| <= 2 delta_a u <= y^7/4.

The row labels are thus coherent. This uses the actual inclusion of the prime 2, even if 2 was already in B. It uses small ordinary integers, rather than an unjustified modular division or an assumption that residues are close globally. The inclusive balanced-residue endpoint causes no ambiguity here, because the proved bounds are much smaller than half the modulus.

Taking the contrapositive, if rows are incoherent, every possible column label has at least one phase greater than delta_a. Therefore its weight is at most exp(-2 delta_a^2).

## 9. Summing the minor frequencies

### Incoherent rows

Let d = delta_a^2 = 1/(64y^4). For a fixed incoherent xi, separation permits at most one heavy label in a column, and rigidity bounds that label by e^(-2d). The others, at most u <= y^9 labels, each have weight at most epsilon. Hence

S_u(xi) <= e^(-2d) + y^9 epsilon <= e^(-d)

for large y. The last absorption is justified by e^(-d)-e^(-2d) >= d/2 and the superpolynomial decay of epsilon. For example, d <= 1/64 gives e^(-d)(1-e^(-d)) >= (1-d)(d-d^2/2) >= d/2. It is also valid when no label is heavy: the extra e^(-2d) is simply a harmless upper-bound term.

After multiplication over columns and summation over all row patterns, this case contributes at most

2b * 16^(y^2) * exp(-tau y^4/(64H))
<= 2b * exp(y^2 log 16 - y^4/(64b H_0)),

which tends to zero and is eventually at most 1/4. Replacing H by the constant H_0 and tau by 1/b explicitly validates the comparison of the y^2 and y^4 exponents. The large number of column labels is absorbed locally before row-pattern counting; it is not omitted.

### Coherent rows with a mismatch

Fix the unique coherent M. The matching label has W-phases at most |M|/(uw) <= y^(-3), eventually at most delta/2. Separation therefore bounds each mismatching label by epsilon. Their total weight R_u is at most y^9 epsilon.

Expanding the product over columns by its nonempty mismatch set D gives an upper bound

(1 + y^9 epsilon)^|U| - 1
<= |U| y^9 epsilon exp(|U| y^9 epsilon)
<= y^18 epsilon exp(y^18 epsilon)

for this fixed M. There are at most 2y^7+1 <= 3y^7 coherent M, yielding

3y^25 epsilon exp(y^18 epsilon).

This tends to zero and is eventually at most 1/4. The empty mismatch set is exactly the single major frequency h = M and was correctly removed. Weighted expansion avoids the invalid shortcut of multiplying one small-column estimate by all frequencies.

Together the two minor cases contribute at most 1/2 to the unnormalized sum of |Phi(h)|. The factor 1/L in Fourier inversion then makes their absolute contribution at most 1/(2L). The major sum is real and at least 1/L. Taking real parts therefore gives

N / 2^|A| >= 1/L - 1/(2L) > 0.

Thus N > 0. Tuning converts the congruence to equality, and the reduction in Section 3 handles every positive rational with squarefree denominator.

## 10. Simultaneous size conditions

There is no circular choice of y, Y, H, or U. The following finite list of sufficient conditions can be imposed before choosing Y. Use H_0 as above, E(y) = exp(-y^2/(20,000,000 log^3 y)), and take y integral:

1. y >= 2^16 and y > every prime dividing b.
2. y > 2H_0, H_0/y^8 < 1/b, and 2y^2 < y^8.
3. exp(y^2/4) > 2y^7+1.
4. y^2/log y >= 800 and 2delta y^2+1 <= y^2.
5. y^3 >= 800 log y.
6. E(y) <= 1/(128 y^25).
7. log(8b) + y^2 log 16 <= y^4/(64b H_0).

Conditions 1-5 give all interval, tuning, coherence and separation requirements. Condition 6 implies y^9 epsilon <= 1/(128y^4), so it absorbs the light labels in the incoherent case. It also bounds the coherent mismatch contribution by (3/128) exp(1/128), which is less than 1/4. Condition 7 gives the required 1/4 bound for incoherent rows. Each condition holds for every sufficiently large y, because H_0 and b are fixed, y^2/log^3 y dominates every fixed multiple of log y, and y^4 dominates y^2. Their finite intersection is therefore cofinal in the integers. No numerical experiment or assumed formal asymptotics is needed to establish this fact.

## 11. Provenance and the formal-verification boundary

The full theorem is a prior-result claim, not a new result of this audit. Li's September paper credits Yuren Tang's development as the earlier full proof and describes adopting its finite-Fourier framework. The official Tang Zenodo record 20767390 dates v0.0.3 to 19 June 2026, describes the exact full rational statement, and explicitly retains two Rosser-Schoenfeld inputs. This audit inspected metadata only, not the source archive, the exact Lean statements of those two inputs, or their application. It cannot certify Tang's build, dependencies, theorem translation, or a fully unconditional machine proof.

Li's earlier arXiv:2606.15159v2, dated 17 June 2026 on its PDF, asserts all natural-number targets and rational targets above a denominator-dependent positive threshold, with additional claims about three or more prime factors. The inspected abstract expressly leaves the remaining two-prime small-target regime open. It is not evidence by itself for the exact full theorem audited here. Its formal-verification descriptions are likewise author statements rather than checks performed by this audit.

The 2015 Butler-Erdős-Graham paper supplies the integer theorem with three distinct prime factors. It is contextual provenance, not a replacement for the two-distinct-prime rational theorem.

Li's September Lean declaration is reported to prove an implication from Ramanujan's precise inequality. No Lean code or source archive was retrieved or executed, and no claim about absence of sorry or exact kernel axioms was independently tested. The present mathematical acceptance instead rests on checking the written proof, checking the analytic citation against its primary source, and independently deriving the required analytic bounds. One may accurately call the written result unconditional while continuing to call the reported formal endpoint conditional on its explicit analytic hypothesis.

## 12. Disposition and limitations

Accept the exact theorem at the level of this independent written-proof audit. No genuine gap, false constant, collision in the rational reduction, missing denominator-divisibility condition, or unproved analytic hypothesis was found. The audit does not establish worldwide consensus, journal acceptance, priority beyond the recorded public provenance, or an independently replayed formal proof. No modification to the theorem is needed, and there is no correction patch to publish.

The optional auditor-authored exact-arithmetic checks verify only selected constants and a small finite CRT/subset identity. They do not replace the proof or test its enormous eventual construction. The acceptance is the mathematical argument above.

## Public sources

- Li, September full theorem, versioned official abstract: https://arxiv.org/abs/2609.32140v1
- Li, June partial theorem: https://arxiv.org/abs/2606.15159v2
- Tang, v0.0.3 metadata: https://doi.org/10.5281/zenodo.20767390
- Ramanujan, *A proof of Bertrand's postulate*, original collected-paper scan, pages 208-209, reproducing J. Indian Math. Soc. 11 (1919), 181-182: https://www.imsc.res.in/~rao/ramanujan/CamUnivCpapers/Cpaper24/page1.htm and https://www.imsc.res.in/~rao/ramanujan/CamUnivCpapers/Cpaper24/page2.htm
- Ramanujan, searchable retypeset primary paper: https://ramanujan.sirinudi.org/Volumes/published/ram24.pdf
- Erdős, *Beweis eines Satzes von Tschebyschef*, Acta Litt. Sci. Szeged 5 (1932), 194-198: https://users.renyi.hu/~p_erdos/1932-01.pdf
- Butler, Erdős and Graham, *Egyptian fractions with each denominator having three distinct prime divisors*, Integers 15 (2015), A51: https://mathweb.ucsd.edu/~ronspubs/15_04_egyptian.pdf
