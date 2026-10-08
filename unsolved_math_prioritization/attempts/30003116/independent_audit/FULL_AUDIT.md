# Independent audit of rational multiplicative orbit entropy

## Verdict and frozen scope

The authored mathematics in the frozen packet is accepted as a collection of restricted results and reductions. The intended sufficiently-large-denominator problem remains unresolved after five approaches. One minor domain clarification is required in the abstract collision lemma: its covering quotient assumes U is nonempty. All orbit applications already satisfy this, so no headline theorem or proof strategy changes. The finite fixed-point example is valid only as a defect in an unqualified all-denominators reading; it is not an asymptotic counterexample.

The audited target is problem 30003116, source code OWR-14603-015, queue rank 993. The exact original manifest SHA-256 is:

`f0e11096444ac0a676a9e4a8cd267e51bb4600512574eebf961ce5789a03c115`

All five mathematical files, the README, source metadata, chronology, original checker, original verifier, original negative controls and recorded results were inspected. The original 12-entry inventory plus manifest was preserved. This audit is a separate AI-assisted mathematical and computational review, not human peer review or formal verification. Neither research novelty nor exhaustive literature coverage is certified.

An optional validator hardening patch is supplied separately. It addresses malformed-input diagnostics and validates the manifest's redundant target field. It changes no mathematical claims, test expectations, or accepted original results. The frozen original is accepted for its stated integrity and finite-control purpose, with the limitations detailed below.

## Problem and source interpretation

The controlling source is Lindenstrauss's Question 2 in the [OWR 21/2016 report](https://ems.press/content/serial-article-files/46625?nt=1), printed pages 1127–1128, DOI [10.4171/OWR/2016/21](https://doi.org/10.4171/OWR/2016/21). Its target is a positive multiple of log log s as a lower bound on logarithmic covering number, at a fixed negative power of log s and with each exponent O(log s). The packet correctly treats a,b as fixed multiplicatively independent integers greater than one, r as a unit modulo positive s, and gcd(s,ab)=1. Constants and a sufficiently-large threshold may depend on a,b. The source's reciprocal positive constant is equivalent to a positive multiplicative constant.

The local PDF identity and page image were checked independently. The source really prints the Baker-case condition |s|<r^(1−theta). For 0<theta<1 and fixed positive s, adding a sufficiently large multiple of s to r preserves every orbit point and the unit condition while making that inequality hold. The condition is therefore not a meaningful restriction on the rational point without an additional choice or correction. The audit does not guess the author's intended correction. The packet's explicit power-small-residue hypothesis is separately proved and properly distinguished.

The source does not explicitly exclude small denominators. The packet discloses this and does not use a boundary flaw to claim the intended quantitative question solved. Negative bases, the base 1, nonpositive denominators and nonpositive constants are not part of the repaired meaningful target. These conventions are stated rather than silently used.

## Approach 1 audit

The singleton classification is correct for L>=1: comparisons with the a and b images give s|(a−1)r and s|(b−1)r. Cancelling the unit r gives s|a−1 and s|b−1. Those conditions also suffice for every product to fix r/s.

For a=4, b=7, s=3, r=1, multiplicative independence follows from prime valuations, all unit assumptions hold, and the orbit is {1/3}. Since log log 3>0, a positive logarithmic entropy lower bound fails. For the same fixed bases a singleton can only have denominator dividing gcd(3,6)=3. This witness does not form an unbounded-denominator obstruction. If the cutoff is below one, the orbit is still a singleton; the example does not rely on rounding the cutoff upward.

The injectivity proof is valid whenever (ab)^L<s. Multiplicative independence makes the positive integers a^n b^k distinct, and their range below s makes their residues distinct. Unit dilation by r preserves this. All rational orbit points lie on the s-grid, so distinct points have circle separation at least 1/s. The claimed fine-scale cardinality and occupancy bound follow. Closed intervals explain the additional one in floor(s delta)+1. The particular choice floor(log(s−1)/log(ab)) is safe even at equality because the maximum product is at most s−1.

At delta=(log s)^−N, the lower bound from this occupancy argument tends to zero. The packet does not upgrade cardinality into coarse-scale nonconcentration.

## Approach 2 audit

The only non-elementary input is a fixed-base polynomial lower bound for a nonzero two-logarithm form. [BLMV's 2009 author version](https://math.huji.ac.il/~elon/Publications/Effective_Furst.pdf), Theorem 4.3, attributes this input to Baker and Wüstholz. Multiplying the rational-approximation statement by the nonzero denominator and log b yields the stated linear-form version. Cases with one coefficient zero are handled by decreasing the positive constant. Multiplicative independence ensures the form is nonzero for every nonzero integer pair. No explicit small effective numerical exponent is claimed.

For x in [1/s,s^−theta], Y=log(1/(2x)) obeys theta log s−log 2<=Y<=log s. The selected k satisfy k log b<=Y/2, so the selected n are nonnegative. Their products lie strictly above 1/(2a) and at most 1/2, with no reduction modulo one needed. Distinct k yield distinct exponent pairs; multiplicative independence gives distinct products. Coefficient differences are O(log s), uniformly in x. The external logarithmic-form bound and the derivative lower bound for the exponential then give separation at least a positive constant times (log s)^−D.

For sufficiently large s, the number of points is at least theta log s/(4 log b). Choosing an integer N>D makes their separation exceed (log s)^−N. It can equally be made to exceed 2(log s)^−N, or any fixed multiple, by increasing the threshold. This observation justifies the length-two-delta difference arcs used later. All exponent bounds and constants depend only on the stated fixed bases and theta, not on x or the numerator.

Reflection handles the seed near one. A forward residue obtained at exponents at most C log s has distance at least 1/s from the nearest integer by the unit assumptions. Composing its orbit with the constructed exponents increases the cutoff by another fixed multiple of log s. This proves the forward-small-residue criterion without assuming any unproved recurrence.

For the rational-neighborhood extension, h=lcm(ord_q(a),ord_q(b)) is defined because gcd(q,ab)=1; q=1 is treated separately. The two h-th powers fix u/q modulo one and remain multiplicatively independent. A nonzero rational difference has magnitude at least 1/(qs), hence at least 1/(Qs). Replacing s by S=Qs and theta by theta/2 is valid for large s. Only finitely many q<=Q occur, so their constants and exponent inflation h can be bounded uniformly. The conversion from log S to log s is harmless: one may increase the final scale exponent by one, or apply the same separation proof directly using log S comparable to log s. A translated or reflected band has length below one half, so its circle separation is preserved even when its interval representation wraps across zero.

The missing universal hypothesis is correctly retained. Pigeonholing O((log s)^2) orbit points gives inverse-polylogarithmic closeness, not closeness bounded by s^−theta for a fixed theta>0. No argument in the packet bridges those scales.

## Approach 3 audit and constants

The unconditional estimate is valid uniformly for every admissible numerator and denominator:

C(A_floor(M log s), (log s)^−4) >= c sqrt(log log s).

To make the constant accounting explicit, write A=log(ab) and B=log a. For all sufficiently large s, the initial L0=floor(log(s−1)/(2A)) has T=(L0+1)^2 with T−1 >= (log s)^2/(32 A^2). Thus the minimum consecutive gap d satisfies

1/s <= d <= C0/(log s)^2, with C0=32 A^2.

Set C1=max(C0,4a). The first expanded point at least 4 delta is at most C1/(log s)^2, for delta=(log s)^−4 and log s>=1. Eventually it lies below one quarter, so j1 exists. Maximality gives a^j1 d>1/(4a), and hence the packet's displayed lower bound on J holds, with slack of one in the integer count. For a sufficiently large threshold this implies J >= log log s/B. In particular c=1/sqrt(B) is an allowable eventual lower-bound constant after selecting that threshold.

All selected t_j lie in [0,1/4]. Consecutive gaps are at least 4 delta because a>=2. Consequently any two have circle distance greater than 2 delta. Both original orbit points can be multiplied by a^j despite individual wraparound: their difference is still a^j d modulo one. Since d>=1/s and a^j d<=1/4, j<log_a s. All differences therefore come from A_H−A_H with H=L0+ceil(log_a s).

For example, M=1/(2A)+1/B+2 works for sufficiently large s, including floor/ceiling slack. If K closed intervals of length delta cover A_H, their ordered differences project to K^2 circle arcs of length 2 delta. Each can contain at most one selected t_j. Thus K^2>=J, proving the claim. This argument needs neither a small actual orbit residue nor Baker's theorem.

The conditional power-close-pair argument also holds. Use the oriented smaller circle difference, whose size is in [1/s,s^−theta]. The two-base small-seed construction yields at least c_theta log s difference points with separation greater than 2 delta once the threshold is large. The same square-cover argument yields c'_theta sqrt(log s) covering points. Exponent shifts remain O(log s). This is sufficient for the target entropy if its hypothesis is supplied, but the hypothesis is not established uniformly.

The unconditional estimate gives only one half log log log s plus a bounded constant after taking logarithms. It is not the requested positive multiple of log log s.

## Approach 4 audit and constants

The finite collision identity is exact. The introductory U should be explicitly nonempty before the later division by E_r. If U is empty, T=E_r=0 and that quotient is undefined, although the mean identity itself remains true. The separate one-line mathematical clarification patch adds this domain restriction; every orbit application has T>=1. For each ordered off-diagonal pair, multiplication of its nonzero difference by r runs through every nonzero residue modulo the prime p. Precisely 2 floor(p delta) residues are within circle distance delta of zero for 0<delta<1/2. Every diagonal pair is counted for every r. The odd-prime hypothesis prevents endpoint overlap and all applications use sufficiently large primes.

Assigning each of the T support points to one of K covering intervals counts at least the sum of squared assignment sizes among the collisions. Cauchy–Schwarz gives E_r>=T^2/K. The same reasoning holds for circle arcs, including arcs crossing zero. This is a lower bound for the covering number, with the inequality oriented correctly.

Markov's inequality with threshold mean(E)/eta leaves at most eta(p−1) exceptions. No integrality assumption about that real upper bound is needed. Equality at the energy threshold can be included among the good numerators, so the endpoint does not weaken the stated bound.

For the multiplicative rectangle, with A=log(ab), one has for sufficiently large p

(log p)^2/(16 A^2) <= T <= (log p)^2/A^2.

With delta=(log p)^−6, the extra factor in the denominator of the Markov bound is at most 4 A^−2 (log p)^−4 and is eventually at most one. With eta=(log p)^−1/2 this gives the explicit allowable constant

C(A_L(r,p),delta) >= (log p)^(3/2)/(32 A^2)

outside at most (p−1)/sqrt(log p) numerators. The exponent cutoff is at most log p/(2A). Constants and thresholds are independent of the good numerator. The logarithmic conclusion follows after absorbing log of the constant.

The argument does not remove the exceptional set. It does not prove the formula for arbitrary composite moduli, where a nonzero difference need not be a unit. Those limitations are stated correctly; averaging does not imply a worst-case bound.

## Approach 5 audit

The row-cancellation formula retains multiplicities and is exact, even when orbit points coincide. With the packet's convention for total variation norm, the bound is 2/(L+1). The alternative convention using a supremum over measurable sets would differ by two; the packet has fixed the relevant convention explicitly. The b identity is identical after interchanging the two indices. On the circle the multiplication maps are continuous, so weak limits along L tending to infinity are jointly invariant. No conclusion about entropy follows from that fact alone.

A closed interval of length 1/q meets at most two half-open q-partition atoms on [0,1), including exact boundary configurations. A K-interval cover therefore gives at most 2K occupied atoms and Shannon entropy at most log(2K). Thus a lower bound on this empirical measure's coarse partition entropy would imply a support covering lower bound. The converse need not hold because nonuniform weights may concentrate almost all mass at one support point.

For the short injective rectangle, the s-partition has exactly T equally weighted occupied cells. Its entropy is 2 log(L+1). The joint-refinement comparison is correctly directed: each q-cell meets at most ceil(s/q)+1 s-cells, so the loss in passing to the coarser scale is bounded by the logarithm of that number. At polylogarithmic q this bound is vacuous.

For the single-base model with s_m=a^m−1, multiplication by a permutes the m displayed points cyclically. They occupy distinct s_m-cells. At resolution a^ell, the exact cell counts are one count m−ell and ell distinct counts one. The entropy formula and the ell+1 cover follow. If ell=O(log m), both the small-mass contribution and the main-atom contribution tend to zero. Choosing ell to fit any fixed polylogarithmic scale yields O(log log s_m) covering. Only O(1) points can lie above a fixed positive epsilon, so the uniform measures converge weakly to the point mass at zero.

This example has one generator. It proves failure of a proposed general entropy-transfer step; it is not a counterexample to the required interaction of two multiplicatively independent generators. The packet makes this distinction and does not invoke measure rigidity without supplying its entropy hypothesis.

## Prior work and nonconflation

BLMV's [2008 author version](https://math.stanford.edu/~akshay/research/blmv.pdf) and [2009 author version](https://math.huji.ac.il/~elon/Publications/Effective_Furst.pdf), Theorem 1.10, already give rational-orbit density at a triple-log scale with exponents below 3 log of the denominator. This is correctly credited as prior work, and does not supply the much finer polylogarithmic covering target for free. The relevant statements and adjacent context were inspected; their full proofs were not independently reproved.

The fixed-base logarithmic-form input is correctly attributed to Baker–Wüstholz through BLMV Theorem 4.3 and its bibliography. The original 1993 paper was not separately retrieved. [Fan–Queffélec–Queffélec](https://ems.press/content/serial-article-files/47663?nt=1) studies the multiplicative semigroup, gaps and distribution and is not used as a solution of this finite rational-orbit estimate. The [Burton–Panangaden v1 abstract](https://arxiv.org/abs/2410.22701v1) concerns formulations of invariant-measure and periodic-equidistribution questions, rather than a proof of the present covering bound.

No argument imports results about invariant-measure classification, intersection dimensions, random matrix Furstenberg theory, or two-dimensional orbit density as though they established this one-dimensional quantitative rational question. Supplementary bounded web queries did not verify a later resolution. That is not a certificate of current global openness.

The four recorded source PDF byte counts and SHA-256 values agree with the inspected local PDFs. The recorded saved-copy sizes and hashes for the four main repository records also agree with their saved copies. This audit did not re-download either corpus dataset or repeat every remote branch/PR query. It therefore accepts those entries only as bounded investigation metadata, not as independent exhaustive provenance or a global nonduplication proof. No source PDFs, extracted text, screenshots, corpus records, private coordination data or private personal information are included in the audit deliverables.

## Executed controls and their limits

The original test harness was rerun independently. Its three clean full replays passed, each reproducing 86,778 checks; all 21 mathematical negative invocations and 30 packet mutations were rejected. The independent mathematical checker imports none of the original checker and performs 38,715 controls per run. Normal Python, -O and -OO outputs agree byte for byte. It tests all subsets of tiny prime grids at exact collision thresholds, a dynamic-programming interval-cover oracle, rational-neighborhood identities, difference membership and strict packing, cancellation coefficients, symbolic distributions, endpoint occupancy, and eight intentionally wrong inferences.

The independent packet suite tests original and hardened candidate verifiers in all three Python modes. Its 29 cases per verifier/mode include clean replays, invalid pins, malformed JSON and schemas, duplicate keys, unsafe paths, target/status drift, syntax and assert mutations, false recorded results, extra paths, symlinks, file-mode drift, an intentionally false re-pinned proof, and a genuinely read-only copy. Copies use non-writable files and directory; an attempted write is confirmed to fail, full replay succeeds, and pre/post byte/mode identities agree. Because the original manifest binds modes, these copies explicitly rebind modes from 0644 to 0444 and use the resulting new external pin. They are not misrepresented as the unchanged original pin.

Three malformed original cases terminate nonzero via an uncaught exception: top-level manifest array, top-level null, and a re-pinned Python syntax error. This is fail-closed behavior, but inconsistent diagnostic handling. The original also ignores the manifest's redundant top-level problem_id if an independently changed external pin is supplied; its full replay still checks the source-scope target. The optional patch validates these fields and produces clean REJECTED exits for these malformed cases. These are robustness improvements, not evidence of corruption in the actual frozen packet.

A deliberately false theorem sentence passes either verifier after explicitly re-pinning its file and manifest. This is expected and recorded as a scope control: an integrity checker and a finite computation suite cannot validate an arbitrary mathematical proof or an externally redefined trust root. Neither suite is a security proof against a maliciously replaced checker. Every universal conclusion accepted in this audit rests on the written mathematical reasoning, with the named external theorem where applicable.

## Acceptance conditions

With the stated nonempty-U clarification, the packet may be described as independently AI-audited restricted progress on an unresolved asymptotic problem. Apply or explicitly accompany it with `MATHEMATICAL_CLARIFICATION.patch`; the headline bounds require no correction. Preserve the five-approach unresolved disposition, the finite-versus-asymptotic qualification, the external Baker–Wüstholz credit, the BLMV prior-work credit and the stated verification/search limits. Do not turn these controls into a formal-verification or human-review claim. The optional hardening patch can be applied only as a separately identified revision with a new manifest and external pin; it must not replace or silently change the audited frozen original.
