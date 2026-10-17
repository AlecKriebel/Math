# Parent reconstruction: PR1135 / 30000052 / OWR-723-005

Frozen head: e809a9c40f4ccdaced6f45f10b1dc8b7725a2119. Ten body-pinned input identities match. The root read the entire proof, substantive prior audit, status/acceptance, supplementary verification description and source review. This reconstruction takes neither earlier acceptance nor desired conclusion as a premise.

## Exact target from the primary source

The root freshly retrieved the official 50-page OWR13/2004 PDF, matching445532 bytes and SHA2562f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e. The full contribution printed696–699 was read, and printed697–698 independently rendered and visually inspected. The discrepancy definition is an Lp norm of normalized anchored-box counting error. The displayed question on698 explicitly compares expectations of its pth power, integrates generator and shift over the full product cube, and uses indexed points j=0,...,n−1. Discussion fixes even p, so4 is allowed. There is no generator restriction, conditioning, prime-n assumption or fixed-generator average. The separate final existence/upper-bound question on699 is not this target. Attribution is Erich Novak, reporting joint work with Aicke Hinrichs. Source receipt: `sources/ROOT_FETCH_RECEIPT.json`; third-party bodies/text/renders remain ignored.

## Direct analytic reconstruction

Let T_j={jZ+Delta} with independent continuous uniforms. Conditional on Z, T_j is uniform, hence T_j is independent of Z. For distinct j,k, multiplication of the independent Z by k−j preserves circle Haar measure. Thus (T_j,T_k) is an independent uniform pair. This is not a claim of triple independence. The reasoning is coordinatewise valid for all dimensions and indices.

At n=3 set U=T_0,V=T_1; this pair is iid uniform and T_2={2V−U}. For0≤x≤1/2, on U,V<x the quantity2V−U lies between−x and2x. The negative part cannot wrap into[0,x), and the positive part does not wrap. The remaining inclusion condition is U/2≤V<(U+x)/2. The entire interval lies in[0,x], and its length is x/2 for every U∈[0,x]. Its area is q(x)=x²/2. Boundary choices change no expectation.

For N_x the indexed count, the first two factorial moments are3x and3x². Together with P(N_x=3)=q and total probability1 they force

P_0=1−3x+3x²−q, P_1=3x−6x²+3q, P_2=3x²−3q, P_3=q.

Their normalized fourth-moment polynomial on the lower half is

F(x)=x⁴−(10/9)x³+(8/27)x²+x/27.

Simultaneously replacing Z,Delta by their negatives modulo1 preserves product measure; the centered count at x maps in law to the negative centered count at1−x, outside null events. Hence F(1−x)=F(x). Tonelli applies to the bounded nonnegative integrand. Integration gives2∫_0^(1/2)F=19/1620.

Independently, the iid count is binomial(n,x). Expansion of its centered fourth power retains the all-equal and two-pair index patterns. Its integral is(3n−1)/(30n³). At n3 this is4/405. A sharper sign check compares triple-inclusion probabilities: replacing q(x)=x²/2 by x³ changes the fourth moment by(4/9)(1−2x)(x²/2−x³)=(2/9)x²(1−2x)² on the lower half. Its reflected integral is1/540>0; the ratio is19/16. This proves the full universal negative answer without a numerical estimate or an omitted program.

For the second mechanism, on0≤Z≤1/(n−1),0≤Delta≤1−(n−1)Z there is no wrap, so the empty tails alone contribute[Delta⁵+(1−Delta−(n−1)Z)⁵]/5. Their integral over the triangle is1/[105(n−1)]. The reflected descending triangle with Z=1−W, (n−1)W≤Delta≤1 contributes the same. Interiors are disjoint for n≥3; all omitted contributions are nonnegative. The bound2/[105(n−1)] gives2/315 at n4, exceeding11/1920 by5/8064. It does not alone prove n3; the direct calculation does.

The same bound in fact exceeds iid for every integer n≥4. Cross-multiplication gives4n³−21n²+28n−7; at n=4+t this is25+52t+27t²+4t³>0. This is an additional elementary consequence checked by the root, not an attribution to prior literature or an essential part of the three-point solution.

## Boundary and scope checks

Any anchored box volume v has pairwise-independent Bernoulli indicators, so the normalized count variance is v(1−v)/n. Integrating gives(2^(-d)−3^(-d))/n exactly. At n1 the complete ensemble is one uniform point; at n2 it is a uniform independent pair coordinatewise. Their entire laws agree with iid, hence no counterexample of any defined measurable discrepancy functional exists with fewer than three points. Collisions and coordinate endpoints are null parameter sets, but indexed counting and weight1/n remain defined there; the proof does not condition them away.

The root's independent standard-library exact polynomial reconstruction `root_reproduction/check_root_moments.py` passes76 checks, with all ordinary/-O results identical. It derives the count identities, integrand, pointwise difference, exact integral and ratio, recomputes iid binomial polynomials for n1–16, checks tail integration/scaling, the all-n≥4 comparison polynomial, and explicit adverse controls. It neither imports reviewers' programs nor claims formal certification. Receipt: `root_reproduction/ROOT_MOMENT_REPLAY.json`.

Final mathematical assessment: PASS. Three distinct new independent families completed full reviews. The exact-integration reviewer proves complete affine-strip coverage and derives the supplementary full n4 value139/17280 from the defining integral; it is no longer imported from the historical audit. The root read all three full reports and programs, verified29 authored artifact pins, and reproduced all72816 requirements per successful ordinary/-O mode with every result field identical and explicit failure guards active. One ineffective finite tail diagnostic used the wrong coordinate; the reviewer corrected it and refreshed the log/report/code/manifest, and the root reproduced the corrected program. No mathematical claim or analytic proof required repair. Root reproduction receipts identify the exact final programs. The subsequent complete priority assessment, including the later overlapping preprint, is recorded separately in ROOT_PRIORITY_DECISION.md. This mathematical acceptance is not publication clearance or a human-refereed verdict.
