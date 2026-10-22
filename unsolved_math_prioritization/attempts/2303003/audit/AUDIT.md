# Independent adversarial audit: Function Theory Problem 3.3

## Decision

**Mathematics and exact original scope: PASS.** The construction proves a negative answer to the entire catalogue question, with all radii and every positive-axis point covered. The historical attribution is supported by the primary material actually inspected. The recommended disposition is **already_solved, 1/5**; this is a verified reconstruction of a known counterexample, not a new resolution or a solution of the later optimal-constant problem.

**Publication candidate: PASS after one editorial correction.** In the last section of the frozen proof, change “The stronger bound −K/3” to “The weaker bound −K/3”. The adjective reverses the ordering of the two negative upper bounds, but does not occur in or affect the proof. `PROOF.corrected.md` supplies exactly that one-word edit, and `correction.patch` records it. This corrected proof receives a full PASS from this audit. No further mathematical correction is needed.

The author-frozen files were preserved. No remote writes, commits, branch operations, comments or queue changes were made in this audit. No additional auditors were used. This is an independent assistant audit, not human peer review or formal proof-assistant verification.

## 1. Frozen input and replay

The supplied `FROZEN_MANIFEST.json` has SHA-256

`d1c7d42a977dc92d007026d39c05887cb821b13c704542d34e9206c56146cfde`.

Its digest was verified during the initial audit and rechecked on completion. All ten listed files match both their listed byte counts and their SHA-256 digests. The public directory contains exactly those ten files and the manifest. All nine checks in `SHA256SUMS` pass.

`python3 verify.py` was rerun under Python 3.12.14 without modifying the program or installing dependencies. It passed 16 exact rational/symbolic controls, nine floating-point axis diagnostics, and six floating-point gap diagnostics. Its output is byte-for-byte identical to the frozen `verification.json`. The replay is saved separately as `replayed_verification.json`; `integrity_and_replay.json` records the checks.

These checks establish reproducibility of the program and integrity of the reviewed inputs. They do not establish any continuum quantifier, harmonicity, subharmonicity or boundary theorem. Those matters were independently checked below.

## 2. Exact scope and source inspection

The numerical catalogue record, code AMR-022-3003, agrees with the original Problem 3.3 in Hayman–Lingham's [2018 problem list](https://arxiv.org/pdf/1809.07200v2), printed p.60 (PDF p.61). I read both the original statement and the immediately following update, visually inspecting a fresh rendering from the retained source PDF. The question assumes a strictly negative subharmonic function on the open right half-plane and a semicircular infimum at most −K at every positive radius; it asks for the universal positive-axis upper bound −K/2. It does not require the infimum to be attained in the open half-plane. It does not incorporate the distinct optimal-constant question posed in the update.

The update explicitly records the negative answer and describes a counterexample violating the half bound on the whole positive axis. Thus the retained catalogue summary and keyed prior report, which call that same question unknown as of this edition, are inconsistent with the actual source. The retained prior report offers no mathematical construction to audit or continue.

I independently rendered and visually read the complete retained publisher first-page preview of [W. K. Hayman, “On a theorem of Tord Hall”](https://doi.org/10.1215/S0012-7094-74-04103-9), p.25. It contains the counterexample assertion, c=90, a=1/100, eta=c epsilon, zeta=i exp(−i eta), and the exact two-arctangent plus logarithm formula used in the reconstruction. Dividing the original function by −M produces precisely V in the packet before truncation. The epsilon=10^-6 choice and the bounded truncation are explicit additions to that source construction. The author does not misattribute those additions or claim novelty.

The retained first-page PDF has one page. The two retained source PDF digests and sizes agree with `SOURCE_MANIFEST.json`:

- 2018 source: SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`, 1,706,228 bytes.
- 1974 first-page preview: SHA-256 `7c7292e2a921fa0d062f51e6ccaad24e7c5f37e0e33404b3dc5adadcf6637482`, 60,661 bytes.

The 2018 source was also opened through the research web reader. That reader could not reopen the publisher's article record or first-page endpoint, so the independently examined local preview is the evidence for its mathematical contents; I do not represent those failed web calls as fresh publisher retrievals. Page 26 was not read. Neither was the Chapter 7 book proof. The proof's disclosure of this access boundary is correct, and the reconstruction below does not depend on the unseen page.

The cited 2018 bibliography entry [412] does identify Volume I (1976). The source's Chapter 7 reference is therefore mismatched: Volume I has five chapters, whereas [the publisher's Volume II contents](https://www.sciencedirect.com/book/9780123348029/subharmonic-functions) list Chapter 7. This bibliographic issue is not used to infer any unseen theorem. The exact original question is already negatively settled independently of the book-reference mismatch. This audit makes no claim about the present-day optimal constant or the present-day openness of that different problem.

The packet reports bounded repository-duplicate checks and acknowledges their limitations. This mathematical audit inspected the retained exact queue row and prior-report evidence, but did not repeat the author's remote repository searches or re-download the full large catalogue/report corpora. Consequently it does not convert those bounded author searches into an exhaustive independent novelty search. No novelty claim is needed or made.

## 3. Definition, normalization, and Poisson signs

It suffices to take K=1. Multiplication by any K>0 preserves continuity, subharmonicity, strict negativity and every required inequality.

With epsilon=10^-6 and eta=90 epsilon=9/100000, one has 0<eta<1/2. Therefore zeta=sin eta+i cos eta has modulus one and lies strictly inside the right half-plane. Both components of E=(0,1−epsilon) union (1+epsilon,infinity) have positive measure. Its complement also has positive measure.

For z=x+iy with x>0, the kernel x/(x²+(y−t)²) is positive. Its integral over the entire real line is pi, so 0<h(z)<1. The integral converges at infinity and its derivatives on any compact subset of the half-plane have integrable majorants. Hence h is harmonic. The two-arctangent antiderivative in the packet also independently checks this and fixes the signs.

In more detail, integration over t>0 gives pi/2+atan(y/x), and atan(y/x)=arg z on the right half-plane. Integration over the removed interval gives

atan((1+epsilon−y)/x)−atan((1−epsilon−y)/x)

which equals the sum of the two arctangents subtracted in the packet. Thus its displayed identity for pi h is correct over the whole half-plane without choosing branches in an off-axis addition formula. Endpoint membership in E does not change the integral.

## 4. Green sign, singularity, and bounded subharmonic truncation

Write zeta=s+it with s>0. Direct expansion gives

|z+conjugate(zeta)|²−|z−zeta|²=4xs>0.

The reflected zero −conjugate(zeta) is outside the right half-plane. Consequently G is positive and harmonic off zeta, while −G equals log|z−zeta| minus a harmonic function. With value −infinity at zeta, −G is subharmonic. The sign agrees with the positive logarithmic singularity of G and, equivalently, with the nonnegative Riesz mass of −G.

Thus −V is subharmonic. Its maximum with the constant −1 is subharmonic: the maximum is upper semicontinuous, and at the center of each admissible disk a maximizing constituent supplies the submean inequality. The constant ensures finite values throughout. Since G tends to +infinity at zeta while h is bounded, u is identically −1 in a sufficiently small neighborhood of the pole. It is therefore continuous there; elsewhere continuity follows directly from the maximum formula.

As V>0 away from zeta, all values satisfy −1≤u<0. The pole is not silently excluded from the domain and does not leave a −infinity value in the final function. There is no incorrect use of the generally invalid operation of taking an arbitrary minimum of subharmonic functions: the operation applied to −V is a maximum.

## 5. Every semicircle, including the two gap endpoints

For r>0 outside the closed gap, the positive boundary coordinate r lies in the interior of E. Let d>0 be its distance from the complement of E. When y is sufficiently close to r, every complementary t satisfies |t−y|≥d/2. The complementary kernel integral is then bounded by the full tail integral over |t−y|≥d/2, which is at most 4x/d. It tends to zero as x tends to zero. This explicitly justifies h(z)→1 for arbitrary approaches to ir from inside the half-plane, including along the semicircle.

At ir the two Green moduli agree, and neither vanishes because the Green pole and its reflection have nonzero real parts. Hence G(z)→0. Thus u(z)→−1 along the semicircle. The global lower bound u≥−1 proves the required infimum is exactly −1. Boundary attainment is unnecessary and not assumed.

For |r−1|≤epsilon, the point r zeta lies on the required semicircle and remains in the open half-plane. Radius r=1 is handled exactly by the assigned pole value. For r≠1, the denominator in the Green function is the positive number |r−1|≤epsilon.

The elementary estimate sin eta≥eta−eta³/6≥(9/10)eta is valid at this eta; its stated integral derivation is correct. The lower bounds r>9/10 and sqrt(r)≥9/10 follow immediately from r≥1−epsilon>9/10>(9/10)². Therefore

x=r sin eta≥(81/100)eta>(4/5)eta.

The independent expansion

|r zeta+conjugate(zeta)|²=(r+1)² sin² eta+(r−1)² cos² eta=(r−1)²+4r sin² eta

proves the claimed numerator bound. Its square root is at least 2 sqrt(r) sin eta≥1.62 eta>eta. Dividing by |r−1|≤epsilon yields G(r zeta)>log 90.

Since arg(r zeta)=pi/2−eta, the full positive-boundary Poisson mass before deleting the interval is pi−eta. The deleted integral is at most its interval length divided by x, namely 2 epsilon/x<5/(2c). Hence pi V(r zeta)>pi−eta−5/(2c)+a log c.

The factorial comparison used to show e<3 is strict and correct. It gives e^4<81<90 and therefore log 90>4. Finally,

4a−eta−5/(2c)=10919/900000>0.

Thus V(r zeta)>1 throughout the entire punctured closed gap, and u(r zeta)=−1. Together with r=1, this covers both endpoints r=1−epsilon and r=1+epsilon, which were intentionally excluded from the boundary-limit case. There is no gap in the partition of all positive radii.

## 6. Strict positive-axis violation, uniformly over every x>0

For any real x>0, q=2x/(x²+1) is strictly positive and at most one, by (x−1)²≥0. Integrating the deleted interval at y=0 gives a difference of two angles in (0,pi/2), whose difference is also in (0,pi/2). Its tangent is 2 epsilon x/(x²+1−epsilon²). Since 0<epsilon<1, the denominator is positive. This proves the stated arctangent formula with no branch ambiguity.

At such x, direct expansion of the two squared Green moduli gives G(x)=artanh(q sin eta). Its argument is strictly between zero and one. The elementary integral bounds for artanh and atan in the packet have the correct directions: their integrands are respectively bounded above by the value at the right endpoint and below by the value at the right endpoint.

Applying them gives

aG(x)≤a q eta/(1−eta²),

while the deleted angular mass is at least q epsilon/(1+epsilon²). In the latter step, the denominator initially obtained is 1+q² epsilon², which is at most 1+epsilon², so the further lower bound has the correct direction.

The strictly positive rational coefficient margin is

1/(1+epsilon²)−ac/(1−eta²)>0.

Equivalently, ac(1+epsilon²)<1−eta²; with ac=9/10 and eta²=81·10^-10 this is exactly the rational inequality printed in the proof. Multiplication by q epsilon>0 preserves strictness for every x>0. The loss from deleting the boundary interval therefore strictly exceeds the Green contribution. It follows that V(x)<1/2, while the earlier sign argument supplies V(x)>0.

Since V(x)<1/2<1, truncation is inactive on the entire positive axis, so u(x)=−V(x)>−1/2 for all x>0. Values approaching the bound as x tends to zero or infinity do not cause failure: these are boundary or limiting points, not finite positive x, and q remains strictly positive at every point under consideration. No finite-sampling argument is used here.

## 7. What the 16 controls actually establish

The exact program controls comprise fifteen rational comparisons and one sparse polynomial identity. They correctly check:

1. The exact eta value.
2. Positivity of epsilon.
3. Epsilon below one.
4. Positivity of eta.
5. Eta below one half.
6. The gap-radius lower bound.
7. The coefficient used in the sine lower estimate.
8. The auxiliary comparison (9/10)²<9/10 used to lower-bound sqrt(r).
9. The horizontal-coordinate coefficient exceeding 4/5.
10. The Green-numerator coefficient exceeding one.
11. The integer inequality 3^4<90.
12. The positive gap surplus after replacing log 90 by 4.
13. The strict axis coefficient inequality.
14. Its equivalent cross-multiplied form.
15. Positivity of the relevant denominators.
16. The exact polynomial expansion for the gap Green numerator.

The program does not prove e<3, the sine estimate, the integral bounds, any theorem about subharmonic functions, the boundary limits, or the real-axis arctangent identity. The analytic proof supplies these correctly. The axis comparison uses the direct formula and a stable axis formula at nine points; the gap comparison checks six radii, including both endpoints but excluding the pole. All are explicitly labeled noncertifying. That division of responsibility is appropriate and accurate.

## 8. Correction, disposition, and publication boundary

Only the adjective in the first paragraph of §5 needs correction. For K>0, −K/2<−K/3, so the latter is a weaker universal upper bound. The existence or proof of Hall's weaker theorem is not a dependency of this counterexample. The correction changes neither a formula nor the scope, and no analytic reworking is required.

The corrected proof completely meets the original hypotheses and negates the original conclusion. It demonstrates a previously published negative resolution; hence already_solved is the appropriate exact-question disposition. The single documented substantive reconstruction supports 1/5. Additional proof-search turns are not required merely to address a different optimal-constant problem. The original frozen `STATUS.json` truthfully records that independent review was pending at author freeze; the separate audit supplies the later review outcome without rewriting that historical record.

Before publication, integrate the one-word correction and regenerate whichever release hashes describe the corrected public packet. Do not retain a manifest claiming the old proof digest for the new bytes. The authored audit and corrected proof can be published; source PDFs, page renderings, extracted text, catalogue records, prior-report records and operational evidence should remain excluded, as in the frozen input. No public access to scholarly downloads is required for the correctness of the self-contained reconstruction.
