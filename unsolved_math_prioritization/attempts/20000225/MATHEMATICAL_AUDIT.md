# Independent audit: graph tangencies and the irreducible Harbourne threshold

Date: 2026-10-10 UTC.

## Verdict and frozen acceptance scope

**ACCEPT the mathematical construction-route obstruction, with the one nonblocking editorial correction below now applied in the accompanying proof.** No fatal mathematical gap was found. This is a proof conditional only on the explicitly credited standard complex-dynamical theorem, whose applicable statement and conventions were checked in the primary source. It is not a new proof of that theorem.

The distributed manuscript is [PROOF.md](PROOF.md), 13,388 bytes, SHA-256 `c9667c8f65d9ad6a7c4691209f8070b4cbf8775819e88c64d31700f040d16cc9`. The original independent audit checked the frozen original proof and its closed input inventory before and after its review. That input was not edited. This edition applies the exact one-sentence clarification described in §6 and makes only distribution-scope, historical-computation and reference edits; all mathematical arguments and substantive audit findings remain. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof and audit bytes.

The accepted statements are exactly:

1. For rational maps f:P1_y→P1_x and g:P1_x→P1_y over C of positive degrees a,b with ab>1, their graph curves satisfy
   sum_p (I_p−1) ≤ 2a+2b−4.
2. Their number of distinct intersections is at least (a−2)(b−2)+1, and the number with I_p≥q≥2 is at most floor((2a+2b−4)/(q−1)).
3. In particular, an irreducible pair of bidegrees (1,n),(n,1) cannot have n distinct contacts of intersection multiplicity n for n≥5. No symmetry hypothesis is needed.
4. Therefore the graph-pair route proposed in Orevkov §1.3 cannot produce the proposed degree n²+1, n²+n ordinary n-fold-point family in precisely its n≥5 range where the hypothetical proper-point Harbourne constant is below −2.

This audit does **not** accept any claim of a full solution to the irreducible proper-point problem, impossibility of all plane curves with the same degree and singularity counts, impossibility of the asymmetric n=4 graph pair, realization or elimination of the prior degree-21 patterns, or global novelty. The outcome remains partial progress.

## 1. Exact dynamical input

Epstein's *Infinitesimal Thurston Rigidity and the Fatou–Shishikura Inequality*, arXiv:math/9902158v1, p.1, states γ(T)≤δ(T) for every rational map of degree D>1. Both the text and the actual PDF page were inspected. His γ is a weighted cycle count; δ counts independent infinite forward critical-orbit tails.

For a parabolic cycle whose multiplier has order q, the normal form has first resonant term of degree qν+1. The assigned weight is ν in the parabolic-repelling case and ν+1 in the parabolic-attracting or parabolic-indifferent cases. Thus the proof correctly uses a lower bound, not an equality valid in all parabolic cases. For a fixed point of multiplier one and order k of T(w)−w, q=1 and ν=k−1. This order is invariant under a nonsingular local coordinate change. Distinct fixed points are distinct cycles, so their lower weights can be summed.

The remaining weights are nonnegative: zero for repelling and superattracting cycles, one for nonzero attracting and irrationally indifferent cycles. Ignoring these cycles can only weaken the bound. In particular, the argument does not incorrectly require an infinite critical tail for each superattracting cycle.

Epstein p.2 explains the classical parabolic critical-point-per-petal-cycle input. For multiplier one the petals are individual petal cycles, so a contact of multiplicity k consumes k−1 units, not one unit and not k units. The general root-of-unity normalization would require dividing by q; the authored application never uses q>1.

Theorem 1 has no Lattès exclusion. Its proof on pp.4–5 explicitly disposes of Lattès maps because all their periodic points are repelling. The exclusion in an intermediate rigidity proposition is therefore not a missing hypothesis of the graph theorem. Page 4 was also visually inspected. No complete reproof of Epstein's analytic rigidity argument is claimed.

Source: https://arxiv.org/abs/math/9902158 ; pinned PDF SHA-256 `183fe1d8a889ec536aae458786abace55474fd6b4cc362a1c8213044092a890e`, 215,210 bytes.

## 2. Critical values and orbit relations

For T=g∘f, the local degree identity is valid at every point of the sphere, including poles and infinity. It implies

Crit(T)=Crit(f) ∪ f⁻¹(Crit(g)),

and consequently CV(T)⊆g(CV(f))∪CV(g). Equality at the critical-point level is available, although only inclusion is needed. Distinctness and possible collisions only decrease the cardinality on the right.

Riemann–Hurwitz gives total ramification 2a−2 and 2b−2. The numbers of distinct critical values of f and g are bounded by those totals; critical multiplicities must not be used to increase the count. Hence #CV(T)≤2a+2b−4.

Every infinite orbit started at a critical point of T has the same eventual tail as its first image, a critical value. Two critical points with the same first critical value give the same tail. More generally, intersecting infinite forward orbits eventually agree, and are counted only once. Removing finite critical orbits can only reduce δ(T). Thus δ(T)≤#CV(T) is valid without an assumption that every critical value has an infinite orbit.

This establishes the full accepted chain:

sum_p(I_p−1) ≤ γ(T) ≤ δ(T) ≤ #CV(T) ≤ 2a+2b−4.

There is no substitution of the much weaker 2ab−2 critical-point budget. At n=5 that weaker bound is 48 and cannot rule out the demanded 20 units. The actual factorwise budget is 16.

## 3. Graph conventions and local intersection multiplicity

With bidegree defined as degree in x followed by degree in y, x=f(y) is (1,a), while y=g(x) is (b,1). This agrees with the displayed equations in Orevkov's construction. Swapping the names of the two factors changes no conclusion.

A reduced irreducible divisor of bidegree (1,a) has equation linear in the x-homogeneous coordinates, with coefficient forms of degree a in y. A common zero of those coefficient forms on P1 gives a common homogeneous linear factor and hence a fiber component. Irreducibility excludes this. The coefficients define a basepoint-free degree-a morphism, and the divisor is its smooth graph. This proves the converse used in the application. A smooth divisor of this positive bidegree is necessarily irreducible as well: any extra fiber component would meet the component carrying x-degree one and destroy smoothness.

The graph equations in local parameters u,v at an intersection are u−f(v) and v−g(u). Elimination produces C[[v]]/(v−g(f(v))). Its length is exactly ord(T(v)−v), with no immersion or unramifiedness assumption on f required. If either factor is ramified at the relevant point, T has multiplier zero and this local intersection is simple. A common graph component would force T=id, ruled out by deg(T)=ab>1.

The same local ring argument works in reciprocal coordinates at poles and infinity. If T'(p)≠1, including multiplier zero and nontrivial roots of unity, then I_p=1. Only multiplier-one fixed points contribute tangency excess. Other periodic points of T do not correspond to intersections and are not spuriously counted.

The global intersection product is (1,a)·(b,1)=ab+1. The graphs have no common component; hence subtracting one per distinct intersection from the total multiplicity gives exactly the excess in the theorem. This proves both corollaries without a hidden affine-chart hypothesis.

## 4. Orevkov's source and exact positive control

The complete arXiv primary PDF was present and its relevant pp.2–4 were read. Pages 3–4 were visually inspected. Section 1.3 explicitly proposes the n order-n tangencies and distinguishes the symmetric n=4 search from the unresolved asymmetric case; it says n≥5 was not tried. The author-hosted current version was also read in the packet and agrees on this passage. A fresh arXiv metadata check still listed v3, 9 February 2026. These checks do not establish novelty of the obstruction.

The contact convention is unambiguous in §1.2: its cubic contact has local intersection number three. Using exactly p=z³−3z²+1, q=z³−z²+z, f=−q/p, the independent audit recalculated f∘f by direct rational substitution and separately eliminated x from the two graph equations by a resultant. Both give the complete fixed divisor 3[−1]+3[0]+3[1]+[2]. The published denominator, scalar, coprimality, all four local orders, f multipliers −1,−1,−1,3, and composition multipliers 1,1,1,9 agree. Infinity maps to −1 under the composition and supplies no missing intersection. Exact critical-value elimination finds eight distinct critical values for this composition. The excess is six, consistent with the upper bound eight.

The known degree-ten curve remains credited to Orevkov. Its Harbourne value is −2/3. The full plane construction and its singularities are accepted from that source, not independently reconstructed in this audit.

Source: https://arxiv.org/abs/2601.07809 ; pinned PDF SHA-256 `6cedc659d9cb1bb52380a761f51d7380dcf0a41d5aaef9844c2ee3a5cda56d22`, 173,930 bytes. Author-hosted copy: https://www.math.univ-toulouse.fr/~orevkov/12tp.pdf ; SHA-256 `8164897f03e7a8bacb1d09e6f4d780c964681252576dee7a1b85c64cb82be54b`, 161,655 bytes.

## 5. Arithmetic, hypotheses, and scope controls

All displayed numerical formulas were independently recalculated symbolically. The hypothetical family has

h_n=(−n³+2n²+1)/(n²+n),

and its ordinary-singularity genus budget is exactly the arithmetic genus. Its excess demand minus the available budget is (n−1)(n−4). The strict Harbourne threshold starts at n=5, because after n=5+t the negative of the numerator of h_n+2 is t³+11t²+33t+14. This is positive for every integer t≥0, independently of the finite tests. The values 1/6, −2/3, −31/20, −37/15 for n=2,3,4,5 agree. The first excluded route would demand five order-five contacts for degree 26 and 30 ordinary quintuple points, consuming 20 units against 16.

The input's 522 exact checks reproduce byte-for-byte under ordinary and optimized Python. Their output SHA-256 is `b94090a49ca6308161fe935e44b04c996a84b4936aa8b1de3dd82ed4e5ca2e4d` in both modes. Many are repeated finite samples; they are supplementary algebraic verification, not 522 proofs or a replacement for the analytic theorem.

A separately written historical checker, importing none of the author's checker, passed 2,222 checks in both modes. It includes all-n symbolic identities, exact n=2,…,500 arithmetic, general (a,b) algebra, direct graph resultants, seven varied exact asymmetric/symmetric compositions, and eleven negative controls. Its projective ramification calculation includes finite critical poles and infinity as either a critical point or a critical value.

Decisive hypothesis and interpretation controls:

- For a=b=1, f=id and g=z+1 have excess one at infinity but a proposed budget zero. Thus ab>1 cannot be removed.
- The identity composition has a nonisolated fixed locus and is explicitly rejected.
- A degree-one factor is permitted when the other factor has degree above one; f=id, g=z+1/z saturates excess two.
- Power maps have superattracting fixed points at zero and infinity, both simple as intersections. Their critical orbits are finite, so a rule assigning a positive infinite-tail weight to superattracting points would be false.
- For −z+z², the fixed point at zero has multiplier −1 and a simple fixed-point intersection. Only its square produces a multiplier-one order-three germ. This prevents confusing fixed points with iterated cycles or omitting the multiplier-order divisor.
- The exact n=4 equality case and the known n=3 example are not ruled out by the accepted bound.

## 6. Applied editorial clarification

The frozen proof's example T(z)=z+1/z is mathematically correct: infinity is a triple fixed point, since its reciprocal germ is w/(1+w²). However, its critical points are ±1 and its critical values are ±2, both finite. It therefore demonstrates the need for projective fixed-point coordinates, not an omitted critical value at infinity.

The audit explicitly accepts the following one-sentence replacement in a corrected edition, while retaining the rest of the paragraph and all calculations:

“Projective coordinates are essential when checking fixed-point multiplicities: T(z)=z+1/z is degree two and has at infinity a parabolic fixed point of multiplicity three.”

This is the sole required edit and changes no theorem. The quoted sentence is applied exactly in the accompanying proof before the edition’s distribution-scope edits. The original frozen input remains unchanged. This correction changes no mathematical statement, local calculation or hypothesis.

As an additional audit control only, conjugating z+1/z by M(z)=1/(z−2) gives S(z)=z(2z+1)/(z+1)². Now S(z)−z=−z³/(z+1)², its finite critical value is −1/4, and its other critical value is infinity, coming from the double pole at −1. The contact excess two would exceed an affine-only critical-value count one. This confirms the general warning by a genuine example without requiring it to be added to the proof.

## 7. Literature status, prior work, and remaining gaps

The AIM proper-point definition and Problem 5.3 were checked in text and PDF pixels on p.3. Dimca–Harbourne–Sticlaru's infinitely-near default and Remark 1.8 were read separately; that convention is not substituted for the target's proper-point convention. The original existence question remains unresolved by this packet. Bounded current searches and the inspected sources did not supply a general resolution; this is not an exhaustive nonexistence-of-literature claim.

The earlier report’s byte identity was historically verified. Its proper-point local slack formula and global degree-21 constant were rechecked algebraically. The present audit does not promote those necessary patterns into existence statements, does not equate zero delta defect with ordinary singularities, and does not claim those earlier results again as new work.

No converse identifies all degree-26 curves with 30 ordinary quintuple points with Orevkov's graph construction. No such converse may be inferred from this route obstruction. Likewise, the generic intersection-count bound and the finite symbolic cases do not decide the asymmetric n=4 case.

The analytic theorem is a credited dependency. Its full proof was not independently reconstructed. The original plane-curve existence problem, low-degree realizability questions, sharpness in all bidegrees, and global novelty remain outside acceptance. No source or dataset contents are distributed in this proof-only edition. The manuscript and audit are AI-assisted and unrefereed; acceptance is not external human peer review, journal acceptance or proof-assistant certification.

## Reproduction and integrity

The historical independent exact checker supplied the supplementary algebraic checks described above. A separate pinned, closed-inventory verifier checked the original input against an external manifest digest rather than trusting a resealable local digest alone. Nine distinct tampering cases plus a valid control were run in normal, -O, and -OO modes, all with the expected outcomes. The author’s own 22 manifest controls were also reproduced. The audit’s closed manifest was independently sealed and tested, with external receipts outside that manifest to avoid self-reference.

These are historical verification facts. Programs, raw outputs, generated certificates, datasets, copied primary-source extracts, source documents or screenshots and private coordination material are excluded. The complete proof and every substantive mathematical audit finding are included; the mathematical verdict does not depend on omitted code. [SOURCE_METADATA.json](SOURCE_METADATA.json) preserves public source identities, inspection boundaries and historical verification metadata. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-program reruns.
