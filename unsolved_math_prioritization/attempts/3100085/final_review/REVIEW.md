# Independent review: biased binomial probability collisions (3100085)

## Verdict and scope

**PASS for the stated probability-domain partial results, unchanged. The original problem remains unsolved after five substantive author turns.** No mandatory correction was found. This is a technical audit of a frozen research packet, not a claim of historical novelty or a substitute for human peer review.

The reviewed author checkpoint is `b1bf2b1cb02bc8db4635f7f1bfe092c26cc215fd` on `math/3100085-binomial-collisions-wip`. The exact 40-file author packet is bound by `FINAL_FROZEN_MANIFEST.json`, SHA-256 `e2ee0cd9986c128b7699ee8dd13001e3d156bda1f3116a2182b00308db5b309c`; the manifest itself is the 41st retained file. All final and four historical manifests match. The five authored verification programs reproduce their retained output byte for byte: 760,234 assertions in total.

The strongest retained result is an **all-row exclusion of outer spans at most 12**, based on a finite reduction proved analytically and exact root certificates. It implies outer span at least 13 for any example and, for rational odds, row index at least 8192. The exact scan through row 80 is a separate finite check. The unresolved issue is existence of an integer right-tail root for some unbounded outer span; the packet does not decide it.

## Source scope

The complete Galvin entry and its surrounding Probability section on [Joshua Cooper's problem page](https://people.math.sc.edu/cooper/combprob.html) were read, along with the imported problem and upstream research records. It asks for two equal pairs on four distinct indices for the weighted binomial expression, excluding the unbiased and endpoint parameters. The tree-independence-polynomial discussion is motivation rather than a second requested classification. The prose does not expressly restate every probability-domain convention: the packet explicitly interprets the question as integer n >= 0, 0 < p < 1 with p != 1/2, and indices in 0,...,n. This review accepts that contextual interpretation, without claiming a result about negative or complex p or out-of-support zero terms. The packet already discloses this scope; no correction is required.

The classical row-LCM identity is credited to [Farhi's paper](https://arxiv.org/abs/0906.2295), whose full five-page text and proof were checked. The squarefree-row classification is treated as known, consistent with the relevant discussion and page 9 of [Conrad's note](https://kconrad.math.uconn.edu/blurbs/proofs/binomcoeffintegral.pdf). Fresh source copies match the retained source hashes. No literature-completeness or novelty certification is inferred.

## Turn 1: exact collision reformulation and necessary conditions

For positive odds q = p/(1-p), equality at a < b is exactly q^(b-a) = binom(n,a)/binom(n,b). Taking rational prime-exponent vectors divides each coefficient valuation difference by the interval length. Equality of those vectors is equivalent to equality of the positive real odds, by unique factorization after clearing the two lengths. The zero vector is precisely the excluded q=1 case. The common denominator divides each width and hence their gcd; coprime widths force rational q. These statements use positivity to select a unique real root.

Successive weighted-term ratios q(n-k)/(k+1) strictly decrease. Consequently a level can appear at most once on each side of the mode, no level contains three terms, and four distinct equal-pair indices must be nested a < c < d < b. The treatment includes an adjacent two-term modal plateau. Equal-width intervals cannot tie at the same odds because their coefficient ratios vary strictly with the starting point.

The equal-midpoint exclusion was checked separately. Pairing reflected factors R_j=(j+1)/(n-j) gives a product depending monotonically on x(S+1-x), with S the common index sum. For S<n the outer geometric mean is smaller than the inner mean; for S>n the direction reverses; S=n gives only q=1. The central singleton is handled by squaring, so parity does not leave a gap. Since width difference two would mean both offsets equal one, the surviving outer and inner widths differ by at least three.

Legendre's formula bounds each binomial prime valuation by floor(log_l n), since each floor-function bracket is zero or one. A nonzero valuation therefore bounds the width divided by the rational-exponent denominator by floor(log_2 n). The rational-odds width bound and the prime-row endpoint obstruction are valid necessary conditions, without any converse claim.

The authored scan checks all pairs through n=80 exactly. An independent implementation here instead reduces numerator and denominator by their maximal common perfect-power exponent, avoiding the author's prime-vector method. It independently checks all 88,556 pairs and finds no four-distinct-index collision. This does not extend the scan past n=80 or establish an all-n result.

## Turn 2: formal short-span certificates

After reflection, take q<1 and write the outer indices as A and A+r, with B=n-A-r. The outer relation is q^r=P_r(A)/P_r(B), so A<B. The nested inner interval has offsets u,v>=1 and length s=r-u-v>=1. Its simultaneous equality is the zero condition

    D(B)=P_r(A)^s P_s(B+v)^r - P_r(B)^s P_s(A+u)^r.

For the 20 offset patterns with 3<=r<=6, substituting B=A+1+T produces formal factor identities. Nineteen use A=x; the exceptional (r,u,v)=(6,2,3) uses A=x+1. Every recorded factor has nonnegative integer coefficients and positive constant term, with a nonzero prefactor, so the resulting polynomial cannot vanish for the covered nonnegative integers. The independent checker reconstructs all 20 complete identities in an exact integer polynomial implementation, checks monomial uniqueness and exponent domains, and does not rely on sample evaluations.

The omitted exceptional boundary A=0 is addressed explicitly: D(B)=-9(B+4)(B+7)Q(B), where Q=B^4-230B^3-2523B^2-8672B-9620. On B>0, Q(B)/B^4 has strictly positive derivative, tends from negative infinity to 1, and changes sign strictly between 240 and 241. Thus its sole positive zero is not an integer. This closes the shifted-certificate boundary and proves the initial all-n span-six exclusion.

## Turn 3: credited LCM obstruction and its limitations

Let L_n be the LCM of the nth binomial row. Farhi's identity gives v_l(L_n)=floor(log_l(n+1))-v_l(n+1). For the two nested widths r>s, put g=gcd(r,s), R=r/g and S=s/g. Bezout gives q^g=a/b in lowest terms. The outer equality forces a^R and b^R to divide the appropriate two binomial coefficients, hence a and b divide K_R=product_l l^floor(v_l(L_n)/R). This is a divisibility root, not an ordinary rounded real root. R>=2 is correctly retained.

The resulting large-prime equality restrictions, squarefree-LCM exclusions, rational-odds restrictions and stated Mersenne-row corollaries follow. The elementary squarefree-row classification includes boundary n=0 and agrees with the credited known set 0,1,2,3,5,7,11,23. The n=8 example correctly shows that passing the LCM restriction does not imply a collision. There is no unsupported sufficiency step. The later rational-odds threshold strengthens, rather than contradicts, the earlier interim threshold.

## Turn 4: the infinite-to-finite reduction

This is the critical analytic argument. Define H_w(x)=s log P_r(x)-r log P_s(x+w) for x>=0. Its derivative is rs times the difference between the average reciprocal on the full interval and the average on the shifted inner interval. If w is at least the opposite offset, first delete equal numbers at both ends, then delete the remaining left endpoints. Strict convexity of the reciprocal makes the full mean larger than the symmetrically trimmed mean: the chord bound places the interior mean strictly below the endpoint mean. Removing additional left, largest reciprocals lowers the mean again. All intervals stay nonempty, and u,v>=1 supplies strictness. Thus H_w is strictly increasing in this orientation, with limit zero at infinity.

If u>=v, H_u(A)<H_u(B)<=H_v(B), excluding a root. Therefore any surviving oriented collision has u<v. Then H_v is strictly increasing to zero and H_v(A)<H_u(A). If H_u(A)>=0, there is no finite root; if H_u(A)<0, there is exactly one real B>A. The exact existence gate is P_r(A)^s<P_s(A+u)^r. This supplies both existence and uniqueness, not just monotonicity of a sampled expression.

The finite bound on A is valid with its strict integer endpoint. Put delta=v-u>0, t=A+1, mu=(r+1)/2 and nu=mu-delta/2. Taylor's lower bound for the full logarithmic mean uses log''>=-1/t^2 and variance (r^2-1)/12; Jensen bounds the inner mean above. The mean difference is at least

    delta/[2(A+mu)] - (r^2-1)/(24t^2).

For t>=r-1, A+mu<=A+r<=2t. Hence positivity is forced by 6 delta t>r^2-1. With M=max(r-1,floor((r^2-1)/(6 delta))+1), the gate can only hold for 0<=A<=M-2. The strict inequality and the subtraction by two are correctly aligned. No asymptotic estimate has been used as an exact cutoff without proof.

Finally, the sign of D(B) agrees with H_u(A)-H_v(B). It is positive at B=A and eventually negative when the gate holds, with a unique zero. Exact integer doubling followed by bisection therefore terminates and either finds an integer root or brackets it between adjacent integers. For fixed r there are finitely many offsets and bounded A values, so this is genuinely an all-n finite decision procedure for that fixed span. It gives no uniform conclusion for unbounded r.

## Turn 5: complete span-twelve certificate and corollaries

The independently reconstructed domain has 938 bounded left-tail cases for r=3,...,12 and u<v. Exactly 879 fail the strict gate; 59 pass. The independent enumeration uses pairs of interior support positions and an inequality-based cutoff loop rather than copying the author's offset-loop/floor expression. Each surviving case has adjacent integers L,U with A<=L, U=L+1 and strict signs D(L)>0>D(U). All cases and certificate integers match.

As an additional normalization check, both endpoints of all 59 brackets were tested directly using the original binomial coefficients at n=A+B+r, not only the rising-factorial formula. The four support indices are distinct and valid, q<1 is consistent, and all 118 signs agree. The maximal bracket endpoint 2240 is an output of root isolation, not a bound on n imposed by the theorem.

Thus no probability-domain collision has outer span at most 12. Combined with the rational-odds width bound this forces n>=2^13=8192 for rational odds. The claimed Mersenne rows with exponent at most 20 follow from the zero 2-adic exponent and 2^20<3^13; the corollary is correctly restricted to rational odds. No argument excludes irrational odds in all those rows or all larger spans.

## Reproducibility, boundaries and remaining gap

`independent_check.py` imports no author verification program. It uses Python integer/rational arithmetic and SymPy's exact integer polynomials, with no floating-point comparisons. Invoke it with the author packet directory as its sole argument; when installed in `final_review/`, omitting the argument selects its parent author directory. Its retained output records 107,320 successful assertions, including all formal identities and final certificates. These controls supplement the analytic review; finite tests alone do not prove the convexity, Taylor or unbounded-parameter statements.

No author file was edited by this review. Raw source downloads and review working files are excluded from the portable review. The finite-n scan, all-n bounded-span theorem, rational-only corollaries and unresolved unbounded problem remain explicitly distinct. A complete answer would still require either a valid integer root at some larger span or an argument excluding every larger span. No such result is present, and the disposition **unsolved, 5/5** is appropriate.
