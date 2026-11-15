# Record 23539734 — completed source/scope continuation

UTC: 2026-11-14T23:46:48.783793+00:00

## Verdict and exact edition

**The full original theorem and all-odd-prime supplementary proposition survive this source/scope review at the level of the explicitly credited classical theorems. No substantive mathematical defect or unresolved mathematical gap was found.** This is a review finding, not publication authority, a human peer-review claim, or a proof of historical priority. No narrowed replacement or repair is being promoted.

The exact native edition is version 1.1, dated 21 October 2026 UTC, DOI https://doi.org/10.5281/zenodo.23539734. The actual standalone 8-page PDF is 106677 bytes, SHA256=e555c20722ca9edb2bc8d164103e748b87c37b56e5eb8bed18c80b33031f737c. The controlling 538-line TeX is 25497 bytes, SHA256=8d93d964cf09e2d895048456aca91d075edb2d2002b85de0dd061f6e2aa9e25f. SOURCE_READY.json is SHA256=1e18c3ce5d1b7556f97ee9c90f4d8ed21fa6a4d19e54cee8b730210a15795eaa. The native assets, ordered original file objects, October 25 transport receipts and all predecessor evidence remain unchanged. Version label 1.1 does not by itself authenticate an earlier deposited edition; the original versions response has one record.

## Independence and exposure

This new continuation agent personally read the complete actual PDF and controlling TeX before reading its own lane's predecessor report, programs, foreign primary bodies or110 sibling findings. Its independent reconstruction is SHA256=9cd48d9eb5cf95c72026c26837eb5941ec8e866ddaaf06eb808f0a8d0b2bb6d3. The predecessor's distinct initial seal remains SHA256=a29453a18dbce66945bfc337334a7c0356305928c4e9f2a2d77f7a3c80987a0d. I do not claim predecessor reading as my own. All 8 target pages were also visually checked. Root's 110 gate was explicitly opened before scientific transfer. No sibling review was read. Own completed 109 scope work concerns a separate paper and is not evidence here.

After the personal initial reconstruction, I read the actual relevant primary bodies from the authenticated own-lane cache: official 58-page OWR actual pages 32–33 / printed 2944–2945 in full, author-hosted 2-page counterpart in full; DH pages 1–3; AS pages 1–4 and 16–17; MP pages 1, 8–9; BCST pages 1–3; OS pages 1–4; and Roberts 2011 actual page 8 / printed 220, reference 9. These are exact read extents, not whole-book or whole-OWR claims. Broader AS pages 1–5 / 16–18 extracts were prepared, but no full 20-page reading is claimed. The official OWR contribution pages were visually checked. Cached-body hashes were independently checked against historical receipts. Fresh primary web opens authenticated the OWR endpoint and AS v2 edition; the DH DOI web-reader attempt was inaccessible, while its previously received exact publisher PDF remains authenticated and was personally read.

## Full original claim and independently reconstructed proof

Let L(u,v)=(u,(u²+1)v), N=p−1, theta_p=phi(N)/N and S={p prime:p≡3mod4}. The map is birational overQ with the displayed rational inverse, infinite order and invariantu. Its generic invariant fiber has genus zero. A nonconstant multiplier(u²+1)^m cannot identically equal 1, proving infinite order. The inverse is not polynomial; no polynomial-automorphism claim is made.

For p∈S, every multiplieru²+1 is nonzero. Fiberwise multiplication is therefore a full-affine permutation, with least period 1 on v=0 and ord(u²+1) on v≠0. All periods divideN. With POINT weighting1/p² and normalizationT/p, every proper divisor ofN is≤N/2<p/2. Hence for every FIXED x∈[1/2,1), once p(1−x)>1, only primitive multiplier fibers are excluded and

    D_p(x)=1−(p−1)P_p/p².

The strict threshold matters: at x=(p−1)/p all points are included. There is no uniform estimate for movingx→1 and no substitution of uniform cycle weights.

The standard cyclic-group primitive indicator is theta times the squarefree-character sum. Every character, including the principal one, is extended by 0 at 0. Root counting and the substitutiont=−s give S_chi=eta(−1)J(eta,chi) for nonprincipal chi. Gauss sums yield modulus sqrt(p) unless chi=eta, where the exact sum is−1 and modulus 1. Thus the principal contribution is exactlyp theta_p in class 3, and the triangle inequality over2^omega(N)−1nontrivial squarefree divisors proves

    |P_p/p−theta_p|≤theta_p(2^omega(N)−1)/sqrt(p).

There are only 6 primes below 16, while 2≤ell^(1/4) at every prime ell≥17, so2^omega(N)≤64N^(1/4). Combining the exact CDF identity with this bound gives the claimed 1/p+64p^(−1/4)error. This is a proof for all asserted primes and fixed thresholds, not an empirical extrapolation or a new primitive-value theorem.

CRT and Dirichlet produce an increasing subsequence in S that is 1 modulo each expanding product of odd primes. Euler's vanishing prime product forces theta_p→0, so the CDF tends1. For the incompatible subsequence, Möbius inversion followed by Siegel–Walfisz gives the unconditional shifted-prime mean

    average theta_p→A=product_ell(1−1/[ell(ell−1)]).

The cutoffK=(logX)^6has tailO(X/K), and the initial-range error weighted by1/d isO(XlogK/log^4X)=o(pi(X)); phi(d)≥sqrt(d/2)ensures absolute convergence of the coefficient series. The elementary Euler-product lower bound isA≥7/24. If only finitely many class 3primes had theta_p≥1/24, residue-class PNT and theta_p≤1/2for every odd prime would force the whole-prime mean≤13/48, a strict contradiction. Therefore limsup D=1 and liminf D≤23/24, with subsequences independent of x and the threshold eventual separately for each fixed x.

This alone does not establish the strongest quantifier. For EVERY further subset of S of positive UPPER relative density, the required additional input is the atomless limiting empirical WHOLE-prime law oftheta_p. Its unconditional continuity is stated directly by DH's Proposition 2.1 / application m=2 and by AS Theorem 1.3(i), n=1. AS's proof first treats primes and then removes proper prime powers, whose count is negligible relative topi(X). No conditional residue-class law, absolute continuity, GRH or fixed-base Artin conjecture is required.

Independently, suppose b_p→c on a subset A of upper prime density delta>0. For any epsilon>0, all but finitely many members of A lie in[c−epsilon,c+epsilon]. Along endpoints realizing delta, the limiting empirical law gives that interval mass ≥ delta. Atomlessness makes the endpoints continuity points. Letting epsilon↓0forces an atom of mass ≥ delta at c, impossible. Since S has prime density1/2, its positive upper relative density is enough. Applying this argument to the uniform o(1) CDF bridge proves all of Theorem 1(iii)'s CDF claim.

A CDF can fail to converge at a limiting atom while measures converge weakly, so the weak claim requires a continuous test. Here the globally bounded continuous ramp

    h(t)=max(0,min(1,2t−1)), t≥0,

kills every proper-divisor normalized period and gives value 1−2/p at the maximal period. Therefore

    integral h dmu_p=(1−2/p)(p−1)P_p/p²=theta_p+o(1).

Weak convergence along any asserted positive-upper-density set would force convergence of this moment, contradicting the same atomless-law argument. This proves the entire weak nonconvergence claim without assuming a CDF continuity point.

For every ODD prime, r_p=#roots(u²+1)∈{0,2}. On Omega_p={u²+1≠0}, the map is a permutation; its size isR=p(p−r_p). The primitive indicator's principal term becomes(p−r_p)theta_p and all nonprincipal bounds persist. Thus P_p/p=theta_p+o(1) uniformly over odd primes, and exact regular-domain formulas are

    Dreg_p(x)=1−(p−1)P_p/R,
    integral h dmureg_p=(1−2/p)(p−1)P_p/R.

Both have the asserted theta bridges because(p−1)/(p−r_p)=1+O(1/p). This does not turn class 1maps into full-plane permutations.

If all regular points remain and e≤r_p p exceptional points are retained, the completed/deleted measure is(1−epsilon)mureg_p+epsilon sigma_p, where epsilon=e/(R+e)≤r_p/p≤2/p and sigma_p is any probability measure recording the assigned FINITE NONNEGATIVE periods divided byp. For every[0,1]statistic, the change is≤epsilon; for any bounded real statistic it is≤2||f||infinity epsilon. This proves the complete arbitrary-subset/arbitrary-period/uniform-point-weight robustness. Assigned periods may exceed p; the ramp remains a valid bounded continuous test on[0,infinity). The whole-prime scalar law consequently excludes every positive-UPPER-prime-density selection under every stated convention. Deleting regular points, altering point weights, permitting negative periods or claiming actual least periods on nonperiodic points is outside the proposition.

## Primary credit and historical boundary

The official Vivaldi 2004 contribution, joint work with John A. G. Roberts, uses precisely the point-weighted T/p scale and states Conjecture 1 for arbitrary birational maps. Its genus-one discussion is a subsequent heuristic, not an explicit genus-one hypothesis of the broad existence sentence. The forward-polynomial, rationally invertible map is within that broad wording and is a full-affine permutation onS. The target avoids narrower elliptic-fiber or polynomial-automorphism claims and the distinct prime-averagedT/p² Conjecture 2. The official 58-pagePDF's relevant contribution is actual32–33; SHA256=7c4c7d0a8e2eb49b82abc1d6d5eb1875e73cacae73dfe2709534498b1d04508d. [Official OWR source](https://ems.press/content/serial-article-files/45972).

All established ingredients must remain credited: Alina Ostafe / Igor E. Shparlinski's triangular family, arXiv:0902.3884v3 (14 March 2009), which contains this map after exchanging coordinates; Andrew R. Booker / Stephen D. Cohen / Nicole Sutherland / Tim Trudgian's quadratic primitive-value character framework, arXiv:1803.01435v2 (header 22 March 2018 / internal 23 March 2018); Lorenzo Menici / Cihan Pehlivan's published shifted-prime mean, Acta Arithmetica 174(3) (2016), 255–276, Lemma 2 with r=m=1; Stefanos Aivazidis / Efthymios Sofos's arXiv:1308.5701v2 (19 April 2014), Theorems 1.1(i) / 1.3(i), n=1; Jean-Marc Deshouillers / Mehdi Hassani's J. Aust. Math. Soc. 93 (2012), 77–83, published online 16 January 2013, Proposition 2.1 and m=2 application. Kátai's original 1968 law is acknowledged through the actual inspected DH/AS interfaces. Their original Kátai/standard Siegel–Walfisz bodies were not retrieved, and I claim the declared classical theorem level, not a new foundational proof. AS itself credits the older n=1 mean to Stephens/Pillai; this paper makes no arithmetic priority claim.

The genuine Roberts 2011 reference 9 lists N. Neumärker, J. A. G. Roberts, C.-M. Viallet and F. Vivaldi, *The dynamics of reversible birational maps over finite fields*, UNSW Preprint (2011). Its body and version relationships remain unrecovered. I personally verified that reference in the actual primary body, not the unseen preprint. The manuscript explicitly preserves this lead. Neither an exact historical firstness claim nor worldwide current-open status follows from the predecessor's bounded search, which was read as a search-scope record rather than reproduced as a fresh discovery. No new omission or exact prior statement was authenticated. No external contact or individual outreach was prepared.

## Meaningful reproducibility and limits

After personally reading both supplied standard-library programs, I reran `check_math.py` and `check_all_odd_primes.py` with `python -B -O`. They have explicit runtime guards, no source/file/network writes, and print-only mains. Complete current output objects match the complete deposited expected JSON objects, reproducing 147619 and 46298 checks respectively. Current receipts retain exact interpreter commands, start/end times, source hashes, output hashes and exit codes. Previous receipts were independently checked against actual source/output hashes and whole expected objects. Historical manuscript counts 8347742 / 230780 remain historical; no such replay is attributed to this continuation.

I also wrote a materially distinct read-only verifier using direct iterate fixed-point TRACES and Möbius inversion, without target imports, order-factor code, complex approximations or a cyclotomic-ring dependency. On 25 odd primes through 101 it recovers all period-point masses from#Fix(L^d), validates divisibility by the period, primitive mass, exact CDF/ramp identities and the character-bound squared inequality. It checks every retained exceptional count 0 through r_p p with heterogeneous normalized periods including 0 and p² and the universal mixture inequality. Its 16716 positive checks and four negative/boundary mechanisms are recorded separately from native and predecessor totals. These reject full-affine permutation at 5, the excluded-maximal-fiber formula at 3, x=3/4, unbounded-moment robustness, and the inference from a mean/two subsequences alone to every positive-density selection.

These finite checks validate identities, boundary handling and implementation consistency. Infinite subsequences, the mean, atomlessness and universal positive-upper-density nonconvergence are justified by the written arguments and authenticated theorem interfaces. No source builder, finalizer, installer, historical audit program, Git operation, site/Sheet/native edit, release or outreach was performed. The inspected old `prepare_final_records.py` writes source-final receipts and was deliberately NOT executed.

The read-only verifier also checks original source identities, predecessor initial seal and all final continuation/source bindings. This bounded source/scope contribution is 100% complete. The website catalogue and any publication decision remain root responsibilities.
