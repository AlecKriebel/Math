# Reverse challenge of the frozen indirect-priority deduction

**PASS. No required mathematical repair was identified in the frozen adversary DERIVATION.md.** Its argument proves the full contrapositive, including arbitrary compact sets of zero length and positive capacity, under either of the two stated endpoint conventions. It is an audit-composed deduction dated 17 October 2026. Its validity does not authenticate a previously printed resolution, an oldest source, firstness, or current worldwide openness.

This is a new post-freeze addendum. The parent deliberately ended the initial families' input isolation and authorized reading the other family's DERIVATION.md, REPORT.md, VERDICT.json and SOURCES.json. The input hashes are recorded in CROSS_INPUTS.json. The independently frozen initial report, verdict, deduction, ledgers, logs, evidence manifest and outside seal are preserved byte for byte. This review does not repair the submitted proof or rewrite either family's initial verdict.

## Primary-source checks and exact scope

Four relevant primary bodies were freshly retrieved from lawful author/university repositories. Their SHA-256 hashes independently match the comparator's records. CROSS_RETRIEVAL_RECEIPTS.json and CROSS_INSPECTION_RECEIPTS.json record the actual inspected material; none is described as a full-paper audit.

| Source | Body authentication and use |
|---|---|
| Hesse, Arkiv för Matematik 13 (1975), 131–144 | Fresh PDF hash `2e3097cc73232acaeb92a42a7cde3316bee5976b9e8ddf601c8ecfd23cb4f83d`. Definitions 3.1–3.2 on printed132/PDF2 and Theorem5.5 on printed141/PDF11 inspected, with surrounding proof. Visual inspection confirms **closure bars over the curve image**. The theorem applies when both compact plates avoid the boundary of the domain. It provides the required equality with continuous ACL plate potentials. [Primary scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7225-11512_2006_Article_BF02386202.pdf). |
| Diening–Harjulehto–Hästö–Růžička draft | Fresh PDF hash `ccb0c25715fa04be1a70f3589e758d770539c3c487b07eef8d3a4a3009e34069`. Title internally dated 3 December 2010. Definition10.1.1, Lemma10.1.9, Lemmas11.1.2 and11.1.4, Theorem11.1.8 and Corollary11.2.5 checked at the draft's printed309,314,334–337,341. In the application the exponent is constantly2, so exponent bounds and relevant smooth-density requirements hold. The inspected numbering is **draft numbering**. [Author-hosted body](https://www.math.lmu.de/~diening/archive/book.pdf). |
| Hunter half-space notes | Fresh PDF hash `4a6cd9d28833289e4749d570bd1956eeb130b32c485cd779ea71d8019cbb136a`. Printed70/PDF25 contains the first-order trace discussion and Theorem3.42. The theorem has an inconsistent displayed general k; this review uses only the explicitly discussed first-order statement and separately verifies its cutoff proof below. No higher-order conclusion is imported. [Notes](https://www.math.ucdavis.edu/~hunter/m218a_09/ch3.pdf). |
| Björn–Björn–Shanmugalingam 2008 | Fresh PostScript hash `776d335654b93db2f80a1dff678f9c379f93772d022f63066a1bd8cbd8d96a7a`, locally rendered/extracted. Printed1197–1199 checked. Theorem1.1 requires properness and density of continuous Newtonian functions. Printed1198 explicitly corrects the insufficient proof behind the all-representatives claim in Shanmugalingam2000 Remark4.4. The present deduction avoids that dependency. [Author-hosted paper](https://homepages.uc.edu/~shanmun/QContinuity.ps). |

The already authenticated primary Di Nezza–Palatucci–Valdinoci and Brezis bodies were re-extracted independently for the relevant propositions. Proposition3.8 allows input exponent s=1 and gives the continuous flat trace into H^{1/2}; Proposition3.4 at exponent1/2 identifies its Gagliardo seminorm. Brezis Corollary1/Remark3 applies to a measurable integer-valued function at sp=1 on a connected open set. These imports are exact for the uses below. [DPV](https://arxiv.org/abs/1104.4345), [Brezis](https://sites.math.rutgers.edu/~brezis/PUBlications/180.pdf).

Fresh publisher metadata confirms the related Diening et al. book's eBook publication on 29 March 2011 and softcover publication on31 March2011. This establishes the published book's identity and date, **not** a body match of its final theorem numbering with the author draft. The draft's historical public posting date remains unproved. Accordingly, cite the actually inspected draft with its internal date if numbered statements are used; do not silently transfer these page/theorem numbers to the final edition. [Publisher](https://link.springer.com/book/10.1007/978-3-642-18363-8).

## Adversarial mathematical checks

### 1. Finite modulus supplies the actual assumed density

The deduction is correctly contraposed. If the E-to-F modulus is finite, the admissible class contains a Borel density with finite square integral; an infimum of only infinite energies cannot be finite. One such density is sufficient. No minimizing density is assumed, and changing it on a null set is not used. If E is empty the outer family is empty and its modulus is zero. Otherwise F is nonempty because E is contained in[0,1].

### 2. The exhaustion does not apply Hesse to a nonclosed plate

For Q=(-2,3)×(-2,2), the sets

    F_j = { (x,0): -2+1/j ≤ x ≤ 3-1/j, dist(x,E) ≥ 1/j }, j≥2,

are closed bounded sets strictly inside Q, and avoid E. They are nonempty: for example(-1,0) belongs to every F_j. They increase with j. For any x∈(-2,3) outside E, closedness of E gives dist(x,E)>0; for sufficiently large j both the distance condition and endpoint margins hold. Thus their union is exactly F∩Q. E remains fixed throughout. Hesse is applied to each separated pair(E,F_j), never to F itself, and no capacity continuity theorem for a growing nonclosed plate is assumed.

### 3. The image-closure convention genuinely needs the positive background

Hesse's open-interval curve may accumulate on both plates without reaching them at parameter values. The frozen proof explicitly supplies the needed bridge. For ε>0, put ρ_ε=(ρ+ε)1_Q. A Hesse curve contained in Q of infinite Euclidean length has infinite ρ_ε cost. A finite-length continuous curve on an open interval has endpoint limits after compact reparametrization, giving a rectifiable compact extension whose image is the original image closure. If that closure meets both plates, it contains parameter values (possibly endpoints) in E and F_j. Restricting between appropriate values gives a target E-to-F subconnector contained in Q. Its ρ cost is at least1 by the assumed all-curves admissibility. Reversal and any extra intermediate plate contacts do not reduce this bound.

The endpoint points themselves have zero arclength measure, even if ρ takes the value∞ there. This avoids relying on pointwise finite values of ρ. Since Q has finite area and ρ∈L²(Q),

    ∫_Q (ρ+ε)² = ∫_Q ρ² + 2ε∫_Q ρ + ε²|Q| → ∫_Q ρ².

Thus Hesse's larger image-closure family has modulus at most the same fixed finite energy bound. Omitting ε would leave an actual gap for infinite-length image-closure curves; it is already present in the frozen deduction.

### 4. The potential competitors give a uniform Sobolev bound

Hesse's equality allows continuous ACL u_j with the exact values0 on E and1 on F_j and energy at most C+1. Truncation preserves continuity and ACL, and cannot increase the gradient energy. Because Q is a bounded rectangle, the truncated functions belong to L²(Q). Integration by parts on almost every coordinate line identifies their ACL derivatives with weak derivatives; the square-integrability gives W^{1,2}(Q).

For a fixed smooth cutoff η compactly supported in Q and1 near E, w_j=η(1-u_j) has a continuous zero extension to the plane. The product rule yields

    |∇w_j|² ≤ 2|∇η|² + 2η²|∇u_j|²,

so both its L² norm and gradient norm are uniformly bounded. All supports lie in the same compact K⊂Q. The exact values w_j=1 on E and w_j=0 on F_j follow pointwise. There is no limiting representative issue at this stage.

### 5. Strong tail combinations retain the whole first plate

Reflexivity and Mazur's lemma apply in the Hilbert space W^{1,2}(R²). The convex combinations can be chosen from successive tails of a weakly convergent subsequence. Because the original indices in those tails tend to∞, each fixed F_k is eventually a zero set of every constituent and hence of the combination v_n. Every constituent equals1 on all of E, so every v_n does too. Convexity also preserves0≤v_n≤1 and common compact support.

Lemma11.1.2 applies to these continuous, strongly Cauchy v_n. Its uniform convergence outside sets of arbitrarily small capacity produces a quasicontinuous limit; the strong L² limit identifies its almost-everywhere class with w. A further almost-everywhere convergent subsequence, or uniqueness of L² limits, justifies that identification. Consequently the quasicontinuous representative w* equals1 outside a single C₂-null exceptional subset of E. This does not assert that an arbitrary Sobolev representative has any specified values on E.

### 6. The trace really is χ_E

Every real point outside K is zero for all v_n. Every real point inside K and outside E belongs to some F_k and is eventually zero. Every point of E is always1. Thus the entire sequence has pointwise line limit χ_E. The bounds and common compact support imply L² convergence on the line by dominated convergence.

For each continuous compactly supported W^{1,2} function v_n, its trace equals its actual restriction almost everywhere. One can verify this independently by mollifying v_n: the mollifications converge in W^{1,2} and uniformly because v_n is uniformly continuous with compact support; their restrictions converge to the ordinary restriction, while trace continuity identifies the same L² limit. Strong W^{1,2} convergence of v_n therefore gives Tw=χ_E. This is an identification of the ordinary trace class, not restriction of an arbitrary representative of w.

DPV gives Tw∈H^{1/2}(R). Brezis makes this integer-valued function constant almost everywhere on the connected line; its L² integrability, or compact support, forces that constant to be0. This proves both |E|=0 and Tw=0. The argument has not yet proved C₂(E)=0, and the frozen proof correctly continues.

### 7. Both half-planes are needed and both are supplied

The restrictions of a global W^{1,2} function to the upper and lower half-planes have the same trace, with the two standard trace operators agreeing by smooth approximation. Each is zero here. To independently verify the first-order kernel assertion, for almost every vertical line the upper restriction satisfies

    w(x,y)=∫_0^y ∂_y w(x,t)dt.

Let χ_ε(y) remove y≤ε and equal1 for y≥2ε, with |χ'_ε|≤A/ε. Then

    ∫_0^{2ε} |w(x,y)|²/ε² dy
      ≤ 2∫_0^{2ε} |∂_y w(x,t)|²dt.

Integrating in x bounds the derivative-of-cutoff error by a constant times the gradient energy in a shrinking strip, which tends to0. The other L² and derivative errors are likewise integrals over that strip. Common compact support supplies no issue at infinity. Each cutoff is supported a positive distance from the boundary and can be approximated by smooth compactly supported functions inside the half-plane. This proves membership in W^{1,2}_0. Reflection gives the identical conclusion below.

Applying the inspected zero-extension result to each half-plane gives global quasicontinuous representatives w_+,w_- zero quasi-everywhere outside their respective open half-planes. Equivalently, apply Lemma11.1.2 directly to their zero-extended smooth approximations; this gives the same conclusion and avoids any difference between zero-boundary notations. Their sum is quasicontinuous, agrees with w almost everywhere in R², and is0 quasi-everywhere on the whole real line. Quasicontinuous uniqueness from Lemma11.1.4(a), with U=R², identifies the sum with w* quasi-everywhere. Since w*=1 quasi-everywhere on E, E is contained in a finite union of C₂-null sets. Monotonicity and subadditivity imply C₂(E)=0.

This reasoning excludes zero-length positive-capacity compact sets as well as sets containing intervals. It uses neither continuity of a limiting representative on E, a continuum hypothesis, nor logarithmic-capacity equivalence.

### 8. Capacity zero returns to every outer connector

Definition10.1.1 is the inhomogeneous capacity based on the integral of |h|²+|∇h|² and admissibility on an open neighborhood. C₂(E)=0 therefore gives nonnegative h_m≥1 almost everywhere on some open O_m⊃E with W^{1,2} norm tending to0. A fixed cutoff ξ=1 near E and supported in B(0,3/2) preserves this convergence, since multiplication has bounded W^{1,2} operator norm.

Compactness of E gives a positive distance from E to the complement of O_m∩{ξ=1 in a neighborhood}. Choose a nonnegative unit-mass mollifier of smaller radius, also small enough to keep support in B(0,7/4). At every point of E its convolution averages only values at least1 almost everywhere. Hence the smooth φ_m is at least1 on **every** point of E and is0 on the radius2 circle. Convolution does not increase the L² gradient norm, which tends to0.

For every globally rectifiable connector, the smooth chain rule along an arclength parametrization gives ∫|∇φ_m|ds≥1. For a continuous connector only locally rectifiable off its endpoints, apply the inequality on compact interior subintervals tending to the endpoints. Continuity of the curve and φ_m gives limiting endpoint difference at least1; monotone convergence gives the full nonnegative line integral bound. Thus the smooth gradients are admissible for every curve in either stated convention. No exceptional curve family or quasi-everywhere endpoint deletion is used in this last step. Their energy tends to0, proving the outer modulus is0.

## Priority and edition reconciliation

The two initial families obtained different lawful preview surfaces. This family's frozen evidence authenticates a permitted Google Books **partial indexed snippet** at2019 page206 concerning the beginning of a terminology concern. The comparator obtained no readable problem-page text. These observations are compatible. Neither family authenticated the full actual2019 Problem7.58/update page. The truncated snippet must not be completed from a secondary copy, promoted into a withdrawal or alternative theorem, or used to claim the publisher printed a resolution. The preserved receipt is evidence/GOOGLE_BOOKS_PREVIEW_RECEIPT.json. This review did not broaden it into full-page authentication.

The Goldstein–Jackson1982 title remains an unresolved bibliographic lead without its abstract/body. No new evidence here establishes either relevance or irrelevance. Likewise the missing historical public-posting date of the Diening draft and the unmatched final2011 theorem bodies remain source limitations. They do not affect the mathematical implication checked above, but they limit historical publication assertions about that exact retrieved document.

The comparator properly identifies the BBS2008 correction; its proof does not import the insufficient2000 inference. Its conclusion distinguishes an indirect deduction assembled in2026 from an earlier explicit printed resolution. Those distinctions should survive any combined report.

The supported combined statement is: the submitted interpretation admits a complete proof and an independently constructed deduction through compact-condensers, traces and boundary capacity; substantial ingredients are established classical theory. Neither bounded audit establishes firstness or present worldwide openness. Paper framing should acknowledge the classical ingredients and describe the precise problem-specific assembly and all-curves conventions. No required correction to the frozen comparator deduction is requested.

## Preservation and review limits

CROSS_MANIFEST.json seals only the new cross-challenge authored files and receipts; CROSS_FREEZE_SEAL.json is its outside seal. An integrity check compares every initial manifest member and original outside seal against the pre-challenge baseline, and rechecks the five pinned comparator inputs. Ignored _cross_local/ holds retrieved bodies, text and renders; third-party bodies are excluded from the authored cross package. No Git branch, index, commit, push, GitHub/GWS/Zenodo, or external individual communication was changed or initiated.

This is an internal AI adversarial mathematical audit, not external human peer review or a formal proof-assistant certification. Its PASS concerns the specified frozen deduction and source-scoped claims, not a priority guarantee.
