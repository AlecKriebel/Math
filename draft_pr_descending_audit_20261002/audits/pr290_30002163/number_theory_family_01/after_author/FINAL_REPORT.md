# PR290: independent submitted mathematical audit

Verdict: **PASS_COMPLETE_EXACT_FINITE_SOURCE_TARGET**. The exact all- n theorem in the preserved author PROOF.md is proved. I found no mandatory mathematical repair and no remaining mathematical gap for that theorem. My independent argument was frozen before author exposure, and my candidate-specific assessment was frozen before the historical independent review was read. This is a mathematical audit of the submitted original packet, not a later whole-preprint review, priority clearance, publication authorization or a claim of continuing openness.

## Exact reviewed claim

Let F₀=0, F₁=F₂=1 and Fₙ=Fₙ₋₁+Fₙ₋₂. For n≥3 set q=Fₙ≥2 and p=Fₙ₋₁. For the q points

    z_k=(2 sqrt[(k/q)(1-k/q)] cos(2πpk/q),
         2 sqrt[(k/q)(1-k/q)] sin(2πpk/q), 1−2k/q),
         0≤k<q,

the minimum Euclidean chord among every unordered pair is 2/√q, attained by indices 0,1. This includes the finite rational angle, both parity classes, all Fibonacci sizes q≥2 and the north pole. Singleton sizes have no pairwise minimum. Shifted heights, an irrational golden angle, geodesic distance, discrepancy, and optimal packing among arbitrary q-point sets are outside the claim.

The reviewed author proof is 6768 bytes, SHA256 c2cc924751b2f5e6d22d129de6170c3415cca9167c721a0798fc01631cca8c2c; the author verifier is 2913 bytes, SHA256 ceb762bbd6aac9ec626da71de0d7f87245d9071ca35f485be19a10725a72fdc8. Both owned copies remain byte-identical to their supplied original snapshots. All24 original packet bodies, including all7 historical review bodies, were read completely. Raw copying all24 before the first candidate assessment was custody, not exposure to their mathematical conclusions.

## Independent uniform argument, before author exposure

The full independent derivation remains in the preserved parent INDEPENDENT_DERIVATION.md, SHA256 b705881301e016f470724e957d669443765efdb3709ab760b9035192eed018c2. Here is its central arithmetic argument, including its terminal case.

For every integer 1≤m<q and every integer a,

    m |pm−aq| ≥ q/3.                                    (A)

Choose j≥2 such that Fⱼ≤m<Fⱼ₊₁. Then j≤n−1. The vectors u=(Fⱼ,Fⱼ₋₁) and v=(Fⱼ₊₁,Fⱼ) form an integral unimodular basis since their determinant is (−1)ʲ⁻¹. With h=n−j≥1, their errors under (x,y)↦px−qy are

    E(u)=(−1)^(j−1) F_h,
    E(v)=(−1)^j F_(h−1).

These identities follow by the Fibonacci recurrence, with the two initial basis indices or Cassini fixing the sign. They remain valid at h=1: F₀=0 is the actual terminal neighbor error, not a positive quantity.

Write (m,a)=S u+T v with integral S,T, and put A=F_h≥1, B=F_(h−1)≥0. The error magnitude is |SA−TB|. If S=0, the positive integer m is a multiple of Fⱼ₊₁, contradicting its chosen range. If T=0, S≥1 and the magnitude is at least A. Nonzero S,T cannot both be positive, since then m≥Fⱼ+Fⱼ₊₁; they cannot both be negative because m>0. Opposite signs give |SA−TB|=|S|A+|T|B≥A, also when B=0. Finally the Fibonacci addition identity gives

    q=F_j F_(h+1)+F_(j−1)F_h ≤ 3 F_j F_h
      ≤ 3m |pm−aq|.

This proves (A) without an unproved best-approximation assertion. The constant 1/3 is sharp, for example q=3,m=1 and signed nearest residue −1. Nearest-residue ties at q/2 cause no omission: either sign has the same magnitude and cosine. Bound (A) also rules out zero error for 1≤m<q.

For a pair with t=i/q<s=j/q<1, d=s−t=m/q, v=t+s−2ts and c=cos(2πpm/q), the exact quarter squared chord is

    H=|z_i−z_j|^2/4=v−c sqrt(v^2−d^2),
    v−d=2t(1−s)≥0.

When c≤0, H≥v≥d≥1/q. When 0<c<1, put w=√(v²−d²). Both H and d√(1−c²) are nonnegative, and

    H^2−d^2(1−c^2)=(w−cv)^2≥0.

Choose the signed nearest residue r=pm−aq. Coprimality excludes r=0. In the positive-cosine branch 0<|r|<q/4, so sine concavity in the first quadrant gives sin(2π|r|/q)≥4|r|/q. Thus (A) yields

    H ≥ d sin(2π|r|/q) ≥ 4m|r|/q^2
      ≥ 4/(3q)>1/q.

The pole calculation is |z₀−z₁|²=4/q. In fact my proof also establishes uniqueness of the unordered minimizing pair in the displayed index range: equality can only occur in the nonpositive-cosine branch, requires m=1 and v=d, and s<1 then forces t=0. This extra equality conclusion is an independently checked mathematical consequence, not a priority claim. The author's stated attainment needs only the explicit pole calculation.

## Author proof: the different nonzero quadratic form is valid

The author uses a restricted approximation lemma rather than (A). Its hypotheses q≥8, 0<p<q, m≥1, m²<q, s=mp−ℓq and r=|s|<q/4 are exactly what the dangerous pair branch needs. Cassini gives ε=p²+pq−q²=(−1)ⁿ. The integer

    B=ℓ²+ℓm−m²

is nonzero for m>0, because B=0 would give a rational root ℓ/m of x²+x−1. Direct expansion gives

    q²B=εm²−(2p+q)ms+s².

Hence q²≤m²+(2p+q)mr+r². Supposing mr≤q/4 makes the latter strictly less than q+13q²/16, which is strictly less than q² for q≥8, since 1/q≤1/8<3/16. All absolute values, strict endpoints and signs are correct. No asymptotic approximation is being substituted for a finite inequality.

My initial attempted residue-squared form r²−(−1)ⁿm² can vanish. That is not the author's B. Independent exact witnesses q=3,m=1; q=8,m=2; and q=21,m=3 have the residue-squared form zero but author B=1,−1,1 respectively. The owned new negative control really exits1 when the wrong form is substituted into the author's identity; its full traceback is preserved. This falsifies the attempted substitution, not the candidate proof.

The author's geometric formula uses U=2v and D²=2[U−c√(U²−4d²)]. Its bounds D²≥4d for c≤0, D²≥4d√(1−c²) for 0<c<1, and D²≥4d² from the vertical coordinate are exact and pole-safe. The first positive-cosine square-root comparison explicitly has nonnegative sides. For q≥8, m²≥q uses the vertical bound; m²<q splits by the cosine sign. The nearest residue is nonzero, the positive branch is exactly first quadrant, and the restricted lemma yields a strict lower bound there. There is no missing range.

The only smaller nontrivial sizes are q=2,3,5. Their branches are correct: q=2 has only m=1 with negative cosine; q=3,m≥2 is vertical and m=1 has cosine −1/2; q=5,m≥3 is vertical, m=1 has negative cosine, and m=2 has |r|=1 with sine≥4/5, yielding D²≥32/25>4/5. These exact arguments require no decimal trigonometric evaluation.

## Primary target and conventions

I copied only permitted raw primary bodies into private custody, not any source-family narrative. I read the whole Brauchart contribution on printed2436–2439, OWR40/2012 PDF8–11, and visually inspected all4 original rendered pages. Its printed2438 displays precisely the rational-angle zero-based construction and the finite conjecture used here. The subsequent set label {z₁,…,z_q} conflicts with the displayed 0≤k<q and its explicit pair z₀,z₁. Extending the formula to k=q and changing to 1≤k≤q is congruent under (x,y,z)↦(x,−y,−z), k↦q−k. It maps the north pair to the corresponding south pair. Using both poles and q+1 points would change the claim.

For the cited Aistleitner–Brauchart–Dick PDF, I read its title page, Lambert map Eq.(7) on PDF5, the operative whole §5.2 on PDF14–16 including its stated planar Lemma17 proof and following corollary, and its whole bibliography on PDF28–30. I visually inspected PDF1,5,14. This is not full-work reading or an independent validation of the discrepancy theorems or Lemma17's unread antecedent references.

The companion defines f_k=(k/q,{kp/q}), z_k=Φ(f_k), 0≤k<q, where Φ takes longitude in its first coordinate and height in its second. Put j≡kp modq. This is a permutation, and p²≡ε modq gives k≡εpj modq. At the new height j/q the longitude is therefore 2πεpj/q: the OWR set for even n, its longitude reflection for odd n. Reflections preserve chords. The author's §5 claim is thus verified from the primary definitions; a planar separation lemma alone would not prove the spherical minimum.

The supplied companion raw body has an arXiv v1 stamp15Sep2011 and an internal title-page date October14,2018. I retain both observations and do not identify this raw body's creation date or byte identity with the Springer final. Its supplied metadata links the final DOI10.1007/s00454-012-9451-3; no final-journal body collation was undertaken. EMS metadata distinguishes report year2012 from publication date2013/05/29. These edition/date qualifications do not affect the checked formulas or the all- n proof. A carryover odd-index label in the companion's even-case planar unit-cell paragraph is not used in this proof or the definition/reindexing check.

The private source pins agree with the submitted source_manifest.json, but copied bytes and hashes do not authenticate an acquisition session, certify literature coverage or establish priority. No sibling or ROOT mathematical/priority report was read. No new priority search was undertaken. The old SOURCE_GATE's limited searches, imported Git-history assertions and outside later abstract references are historical assertions, outside this audit's independently verified scope; they cannot establish worldwide novelty or continuing openness.

## Finite controls, historical metadata and exact gap

The preserved independent initial packet contains a uniform proof, genuine exact arithmetic controls through q=121393 and a separate rational interval check of all16588 pairs through q=144. Its four negative runs test zero-norm misuse, wrong parity, unsigned-residue substitution and changing the angle to a general coprime numerator. All were actually captured and reaped before author exposure. The latter negative example q=13,p=1 is outside the Fibonacci numerator hypothesis and checks that the hypothesis is essential. These finite tests corroborate the argument and do not prove all n.

The original author's exact CHECKS claims421647 assertions and300237 pair certificates through q=610; its diagnostics claims2061234 floating-point pair checks through q=1597. The historical reviewer claims242425 assertions and114492 direct pair certificates through q=377. I read all those code bodies, their complete stored outputs and their scopes. The author exact code uses integer/Fraction identities and proof-derived bounds, while the diagnostics use binary64 and are correctly labeled numerical. The historical independent code uses rational Machin/Taylor cosine bounds and direct positive-side squared comparisons; no defect was found in its stated finite certificate mechanism. I did not freshly rerun these3 legacy controls. ROOT reports separate genuine reproduction; that report is not substituted for my own native receipts or for the uniform deduction.

The historical AUTHOR_REPLAY.json gives command/result records but not the native PID/time custody used here. It is preserved as a historical claim, not promoted to my own execution evidence. The v2 metadata qualifies author/review completion percentages as informal, uncalibrated estimates rather than probabilities, while preserving original mathematical bodies. The original packet's pending-review states describe its historical stage; my verdict does not rewrite them or cause a Git/publication action.

My first candidate assessment,4532 bytes SHA25632b5fa1b692f991173ee17e5d63c5f749ecb459e529302cd52528f50ba13b5c6, was actually frozen inside native PID11071's interval2026-10-05T20:53:22.449438–20:53:22.479948 UTC, before the remaining22 bodies or old reviewer conclusion were read. Subsequent agreement with that old review is corroboration, not the basis of my finding.

Remaining mathematical gap: **none for the displayed finite theorem**. Remaining excluded questions: priority, present openness, publication readiness of a later paper, and external proposer acceptance. No optional proof-style strengthening is a blocker. ROOT must adjudicate and bind the final external manifest; I do not self-seal or approve publication. The authored reports and final read-only verifier distinguish mathematical reasoning, finite evidence, source reading, and body integrity. Private primary PDFs, full extracts, renders and raw prelaunch copies must stay private.
