# Large positive surgery on arbitrary knots

## Result and scope

Problem KP-3.41, unsolvedmath ID 2839, remains unresolved by this investigation. Five bounded approaches yield an exact-gap audit and elementary consequences of published results, not a general proof or counterexample. No novelty claim is made for the consequences below. The Li–Wan–Zhou-dependent consequence is expressly conditional on the theorem in their current preprint.

Write M_r(K) = S^3_r(K), with the smooth rational coefficient measured against the meridian and Seifert longitude and the orientation inherited from surgery on oriented S^3. The target is

    for every knot K, there exists an integer N_K such that,
    for every rational r >= N_K, M_r(K) has a positive cooriented tight contact structure.

Infinity, when included as a surgery slope, returns S^3 and causes no issue. The threshold may depend on K; the contact structure may depend on r. An integer-slope theorem alone does not establish the rational statement. Neither universal tightness nor any kind of symplectic fillability is required. K3, Section 3.5 and Problem 3.41, fixes the orientation convention and distinguishes the fillable variant [K3].

## 1 The standard Legendrian route has fixed hypotheses

For an oriented Legendrian representative L in standard tight S^3, put t = tb(L), rho = rot(L). Golla's Theorem 1.1 tests his specified contact n-surgery structure xi_n^-(L), for positive integer n, by the simultaneous conditions

    t - rho = 2 tau(K) - 1;  n + t >= 2 tau(K);  tau(K) = nu(K).

The smooth slope is n+t, not n. Increasing n resolves only the inequality. His Proposition 6.18 gives rational slopes q > 2 tau(K)-1 when epsilon(K)=1 and the first equality holds; for epsilon(K)=0 it gives q>=0 under that equality [G]. This is a construction-specific criterion, not a classification of all tight structures on M_q(K).

Here is the elementary stabilization obstruction. After a positive and b negative stabilizations, the classical invariants become t'=t-a-b and rho'=rho+a-b. Thus t'-rho'=t-rho-2a. If delta=(2 tau(K)-1)-(t-rho)>0, the new defect is delta+2a>0. Stabilizing that representative cannot repair the equality. Nor does it change tau or nu of the smooth knot. If orientation reversal is allowed, apply this argument separately to the two initial orientations. This does not exclude a different, non-stabilization-related representative or another surgery construction.

There is a stronger obstruction to the proposed universal standard-contact construction: Conway proves all positive contact surgeries on every Legendrian figure-eight representative in standard S^3 are overtwisted [C]. Failure of that construction is not nonexistence of tight contact structures on the resulting smooth manifolds.

## 2 Mirroring the negative-surgery theorem loses positivity

Li–Wan–Zhou Theorem 1.1 supplies positive tight contact structures on M_-r(K) for every knot and rational r>0 [LWZ]. Applying it to the mirror gives a structure on M_-r(mirror K), identified orientation-preservingly with -M_r(K).

Under the underlying orientation-reversing diffeomorphism from M_r(K), the pullback beta satisfies beta wedge d beta < 0 with respect to the prescribed orientation of M_r(K). Tightness survives diffeomorphism, but positivity does not. Replacing beta by -beta cannot repair this: (-beta) wedge d(-beta) = beta wedge d beta. More generally, for any nowhere-zero real f, (f beta) wedge d(f beta) = f^2 beta wedge d beta. The sign remains negative. Therefore the negative-surgery theorem yields a tight negative structure on the positive-surgery manifold, not the requested positive structure. This is an exact sign obstruction, not an absence-of-search-hits argument.

## 3 Extending the non-loose construction has a concrete barrier

In [LWZ], admissibility means tb != 1 and tb-rot=2g(K)-1. Theorem 1.7 constructs nonzero LOSS representatives with tb=-k for k>=0. Legendrian surgery consequently has smooth slope -k-1. Theorem 1.6(2) transfers nonvanishing LOSS to nonvanishing contact invariant; Theorem 3.3 preserves LOSS under negative stabilization. These statements are used as preprint inputs, not reproved here.

**Conditional barrier.** Assume those two transfer/stabilization results. If M_s(K) admits no positive tight contact structure for a positive integer s, there cannot be an admissible nonzero-LOSS representative L of K with tb(L)>=s+1 in any positive contact structure on S^3.

**Proof.** Set k=tb(L)-s-1>=0 and negatively stabilize k times. The resulting L' has tb(L')=s+1>=2. Its rotation falls by the same k, so tb(L')-rot(L')=2g(K)-1. Every intermediate tb is at least 2, avoiding the exceptional value 1. LOSS remains nonzero. The transfer theorem now makes Legendrian surgery on L' have nonzero contact invariant, hence be tight. Its smooth coefficient is tb(L')-1=s, contradicting the assumption. This proves the conditional barrier.

For K=T(2,2m+1), m>=1, the known forbidden slope s=2m-1 [LS] bounds such representatives by tb<=2m-1. Thus an attempted all-knot extension to arbitrarily large tb is actually false under the cited transfer theorem. It is not merely missing from the cited construction. This does not refute high surgery: positive contact surgery from other representatives may work.

## 4 Foliation alternatives do not supply the required quantifiers

K3 summarizes Roberts' fibered-hyperbolic result with a knot-or-mirror alternative, for slopes in (-1,infinity) [K3, R1, R2]. The original papers' public publisher abstracts were checked; no independent full-proof audit of Roberts is claimed. Keeping the K3 interpretation, its logical shape is a disjunction about K and its mirror within a restricted knot class. Even a statement P(K,r) or P(mirror K,r) for every r would permit the first alternative to fail at every large r. It neither selects the required knot nor removes the fibered-hyperbolic hypothesis. An orientation-preserving identification or a separate argument providing the missing branch would be needed. None is supplied here.

## 5 Fillability and known bad slopes do not decide the target

Ding–Li–Wu Theorems 1.13–1.16 prove eventual Stein fillability for specified knot families: closed three-braid L-space knots and sums, the two-bridge family in their Figure 3, torus knots and sums, and P(-2l-1,2m+1,2n+1) with l,m,n positive. Their Question 1.17 and Conjecture 1.18 retain the all-knot questions [DLW]. No arbitrary-knot Kirby-calculus reduction preserving the needed Stein presentation was obtained. Also, an obstruction to fillability alone does not obstruct tightness.

The known bad slopes give a sharp elementary calibration. Let K_m=T(2,2m+1), m>=1, with positive torus-knot convention. Its genus is m. The L-space-knot case summarized in K3 gives tight positive structures for every rational r>=2m. Lisca–Stipsicz's exceptional family has no positive tight structure at r=2m-1 [LS]. Therefore the smallest integer threshold N such that all rational r>=N work is exactly 2m: 2m works; any smaller integer includes the forbidden slope. In particular, there is no finite knot-independent integer threshold. This is a consequence of known results, not new progress on the arbitrary-knot assertion.

Indeed, the negation of the target requires one fixed K for which bad rational slopes are unbounded above. Varying K_m with the bad slope 2m-1 proves failure only of a uniform threshold. It does not refute a separate threshold for each knot.

## Exact remaining gap

For an arbitrary fixed knot outside the established constructions, one still needs positive tight structures on every rational slope in one full positive tail, or a fixed-knot sequence of arbitrarily large slopes for which all positive contact structures are overtwisted. None of the five routes supplies either outcome. The useful deliverable is the distinction between the global problem and the demonstrated limitations of particular constructions, including the conditional stabilization barrier. Stop classification: stalled partial after five approaches.

## Sources and inspection limits

- [K3] Baykur, Kirby, Ruberman, editors, K3 A New Problem List in Low-Dimensional Topology, author preliminary version, AMS volume 295 (2026), Section 3.5, pp. 160–162, especially Problem 3.41. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [G] Marco Golla, Ozsvath–Szabo invariants of contact surgeries, Geometry & Topology 19 (2015), 171–235, Theorem 1.1 and Proposition 6.18. https://msp.org/gt/2015/19-1/gt-v19-n1-p04-p.pdf
- [LWZ] Zhenkun Li, Shunyu Wan, Hugo Zhou, Surgeries on knots and tight contact structures, arXiv:2510.05294v1, 6 October 2025, Theorems 1.1, 1.6, 1.7, 3.3 and Section 6. Current public record inspected 6 October 2026; only v1 listed and no journal reference shown. https://arxiv.org/abs/2510.05294
- [LS] Paolo Lisca, Andras I. Stipsicz, On the existence of tight contact structures on Seifert fibered 3-manifolds, Duke Mathematical Journal 148 (2009), 175–209. The arXiv author version's introductory exceptional family and Theorem 1.1 were inspected; these cite their earlier nonexistence result. https://arxiv.org/abs/0709.0737
- [C] James Conway, Contact surgeries on Legendrian figure-eight knots, Journal of Symplectic Geometry 17 (2019), 1061–1078, Theorem 1.1; author PDF inspected. https://www.jiconway.com/Papers/Figure-Eight_Surgeries.pdf
- [DLW] Fan Ding, Youlin Li, Zhongtao Wu, Nonexistence and existence of fillable contact structures on 3-manifolds, Asian Journal of Mathematics 28 (2024), 617–652; arXiv v3, 25 February 2025, marked accepted version. https://arxiv.org/abs/2111.02151
- [R1] Rachel Roberts, Taut foliations in punctured surface bundles I, Proceedings of the London Mathematical Society 82 (2001), 747–768. https://doi.org/10.1112/plms/82.3.747
- [R2] Rachel Roberts, Taut foliations in punctured surface bundles II, Proceedings of the London Mathematical Society 83 (2001), 443–471. https://doi.org/10.1112/plms/83.2.443

The exact problem's website did not return usable content through the web tool on two attempts. Identity and statement were instead checked against the complete inherited record and the actual K3 PDF. Bounded current primary-literature searches found no verified all-knot solution; that does not prove absence of later or unindexed work. The verification metadata records hashes, inspection locators, and retrieval limitations. No primary paper's full proof has been independently certified by this report.
