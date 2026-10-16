# Independent Goh1992 collision and support-realization adversary

Author: Codex independent adversary `priority12_goh1992_adversary`.
Scope: supplied complete Goh1992 article versus the original PR563 proof and frozen pre-Goh publication manuscript. No final changed-package acceptance.

## Finding

**No verified mathematical or priority collision with Goh1992 was found.** The complete source does not state or construct an actual support slit with nonmonotone continuous polar argument or radial angle. Its theorems restrict a function satisfying TWO independent extremal/critical coefficient equations. The candidate uses ONE functional, for which compactness supplies genuine global maximizers. Neither decomposition of this functional nor normalization of S supplies a second independent equation. The source's restrictions therefore do not force the candidate extremizers to be Koebe.

I independently derived a stronger compatibility test: **no rotation of Koebe can support the candidate functional for any nonzero real epsilon**. This rules out an unnoticed reduction to a joint-support case of Goh. It is an audit lemma, not a claim of historical novelty. The exact proof is below.

The actual-slit identification and the uniform sign bounds survive this focused challenge. The pre-Goh manuscript needs its obsolete statement that Goh1992 is uninspected replaced with the completed bounded comparison. The separate absence of the Duren commentary and Hibschweiler1995 is an explicitly accepted limitation; it does not by itself block publication, and this review does not clear global priority.

## Independence, exact inputs, and full coverage

`SOURCE_FIRST_CHECKPOINT.md` was saved and sealed BEFORE accessing candidate or old reports. Its seal time is 2026-10-15T03:09:03.143967+00:00 and SHA256 is recorded in `SOURCE_FIRST_SEAL.json`. Complete Goh OCR, wrapper through references, was read, and every body page, printed 197–206/PDF 2–11, was visually inspected. This includes every proof, intermediate identity (1)–(16), remark, conclusion, acknowledgment, and reference. The exact supplied PDF is 511209 bytes, SHA256 `94af0c114ce2ced1cb7f2337568c4ce0b8e0615c1ec32542f226d9bf177a0503`.

Only afterward I read the complete original `PROOF.md` (SHA256 `f01dd412bf207967018faa7e1b5a599630ed64830daa5874a0d6c1ce4e54e1c8`) and complete publication `support_slit.tex` (pre-Goh SHA256 `c46d521e893a46466cf26b50c54294d1923e93dad4076e4b5dfa16c52d42830a`). I read the original finite checker to understand its claimed scope, but wrote a separate portable checker. I did not read any other review's substantive conclusions. `INPUT_SEAL.json` freezes content identities of all six input files, including HL PDF/OCR.

HL Problem 6.72 was read in OCR and visually checked on complete printed p.143/PDF144. It asks whether the actual arc omitted by a support point has monotone argument, and whether its radius–tangent angle is monotone. The questions concern global behavior. The 2018 editorial update is not evidence of 2026 status. The candidate explicitly covers both signed and ordinary unsigned radius–tangent angle conventions, and either direction of monotonicity.

## Goh's exact constraints and why they do not collide

Goh assumes coefficient functionals `L=Σ(j=2..n)lambda_j a_j` and `M=Σ(j=2..m)mu_j a_j`, with nonzero top coefficients, not positive real multiples. Each support yields its generalized Schiffer equation. TWO equations yield an algebraic continuation, and comparison of local branches `F=b1 z+b2 z²+…` forces roots-of-unity restrictions on `b1`. Rationality, then Koebe, follows when all branches have `b1=1`. The source does not obtain algebraicity from a single coefficient support equation.

The exact sufficient condition in Theorem 1 is `|alpha|<=2sqrt(2)` or `|alpha|>=4`, with `alpha=((m-3)lambda_(n-1)/lambda_n-(n-3)mu_(m-1)/mu_m)/(n-m)`. OCR corrupted `sqrt(2)`; visual verification is decisive. One global maximum and one independent critical equation suffice. Degree three versus any degree is settled by Theorem 2. In the equal-degree case the leading ratio must be real, and normalized coefficient subtraction produces the last differing index `ell`. Theorem 3 applies when `gcd(n-1,ell-1)=1`; Theorem 4 treats `ell=3` by additional algebra.

For `n=m=4`, `ell=2,3` both satisfy Theorem 3. For `n=m=5`, `ell=2,4` satisfy Theorem 3, and `ell=3` satisfies Theorem 4. These are restrictions on a PAIR of independent equations. The candidate has exact degree four because `lambda4=i epsilon` is nonzero. Padding `lambda5=0` violates the source's top-coefficient hypothesis and cannot turn it into degree five. Adding a genuine degree-five term creates a different functional and does not establish that the same function is critical for it.

The conclusion's sum argument runs from common maxima of L and M to a common maximum of L and L+M. It does not infer separate maxima from maximizing a sum. The strengthened critical-point remarks likewise assume a second Schiffer equation; a single scalar stationarity condition under rotations does not supply that equation. The Schiffer identity is real linear in functional coefficients and their conjugates, so the equation for a sum also cannot be separated into equations for its summands.

## Direct obstruction to Koebe support

Write `k_u(z)=z/(1-u z)^2`, `|u|=1`. Its coefficients are `a_j=j u^(j-1)` and its omitted ray is `w=-u^(-1) r`, `r>=1/4`, since `k_u(z)=u^(-1)k(uz)`. For the candidate,

`Q(w)=-a/w^3-b/w^4-c/w^5`,

where `b=i epsilon(6u-3)` and `c=i epsilon`. Along the ray, trajectory positivity requires

`Q(-u^(-1)r) u^(-2) = a u/r^3-b u^2/r^4+c u^3/r^5`

to be real for every r in an interval. Multiplication by `r^5` gives a polynomial whose three coefficients must be real. In particular,

`Im(c u^3)=epsilon cos(3 theta)=0`,

`Im(b u^2)=3epsilon(2cos(3theta)-cos(2theta))=0`,

where `u=e^(i theta)`. For real nonzero epsilon, setting `x=cos(theta)` forces

`h(x)=4x^3-3x=0` and `g(x)=2x^2-1=0`.

But exact multiplication gives

`(4x^2-1)g(x)-2x h(x)=1`.

No simultaneous root exists, even complex. Thus no Koebe rotation is a support point for this L. This is consistent with Goh: candidate global maximizers exist, are non-Koebe, and cannot satisfy a second independent degree-four critical equation of the source's kind. A weaker independent cross-check uses the candidate's near-Koebe estimate: a hypothetical Koebe maximizer obeys `|u-1|<4eta`, so `|u^3-1|<12eta<1`, already incompatible with `Re(u^3)=0`. An initial parent message used the incorrect ray direction `-u`; it was corrected to `-u^(-1)` before final sealing. The corrected derivation above is the operative one.

## Sum and normalization attacks

Normalization fixes `a0=0,a1=1`; it does not fix `a2`. Identity and Koebe have `a2=0,2`. Consequently the candidate's degree-two term is not an irrelevant constant.

An actual-S countercheck shows the summands cannot be separately maximized. `Re a2` has unique maximizer k. At k the perturbation `Re i epsilon(a4-3a3)` is zero, whereas at `k_i` it is `4epsilon>0`. Hence no function jointly maximizes these two summands, although their sum has a maximum by compactness. This specifically blocks an illicit application of Goh with `M=a2` or `M=i epsilon(a4-3a3)`.

Complex functionals must also be compared modulo their real restrictions on normalized S. The introductory general conjecture's literal wording requires the usual interpretation of 'essentially different' modulo normalization constants: adding `a1` gives a different functional on H(D) but the same restriction up to a constant on S. Goh's actual coefficient statements begin at `a2`, eliminating that ambiguity. For finite functionals beginning at `a2`, equality of real restrictions up to a constant forces equality of coefficients: evaluate the difference on all Koebe rotations and use uniqueness of positive Fourier modes. Thus the candidate cannot be represented as a lower-degree functional with the same real restriction. Conjugating its coefficients also gives a genuinely different real restriction; at `k_i` its perturbation changes from `+4epsilon` to `-4epsilon`.

## Why the pure-square argument is inapplicable

Goh's Theorem 4 first subtracts TWO normalized equations and reaches `ell=3`. With `A=d3`, `B=d2`, `beta=B+2a2 A`, the derived equation is

`(z f'/f)^2 [A/f^2+beta/f]=A z^-2+beta z^-1+c0+conj(beta)z+conj(A)z^2`.

Only in the special case `beta=0` does the numerator become an even quartic in the DISK INPUT coordinate z. The actual slit tip's disk preimage `z0` makes `f'` vanish simply, hence gives a double root. Evenness then supplies the double root at `-z0`, forcing a square and rationality. This depends on the cancellation mechanism and the location of `z0` in the input plane.

The candidate's even quartic is instead `P(v)=a-bv²+cv⁴` in the OUTPUT double-cover coordinate `w=-v^-2`. The finite target slit tip need not be a zero of P. A double zero of the pullback in the input z coordinate does not become a double zero of P. The candidate does not assert this quartic is square; it explicitly uses its nonzero analytic square root on a bounded disk.

Indeed it cannot be a polynomial square for the candidate's global maximizers. Their bounds give `|A|<3`, `|B|<4`, hence `|a|>=1-3epsilon`, `|b|<4epsilon`, `|c|=epsilon`. Therefore

`|b²-4ac| >= 4epsilon(1-3epsilon)-16epsilon² = 4epsilon-28epsilon² > 3epsilon > 0`.

An even quartic with nonzero leading and constant coefficients is a quadratic polynomial square only if this discriminant vanishes. The exact checker verifies this obstruction and a simple negative control `1+v²+v⁴` showing that evenness alone never suffices.

## Actual global support and angle-failure audit

I challenged the candidate's central distinction between a formal trajectory and an actual omitted slit. It survives in the frozen publication manuscript:

1. `Re L(k)=2`, `Re L(identity)=0`, so the continuous complex-linear functional has nonconstant real restriction. Compactness supplies actual global maximizers in normalized S. Coefficient bounds put EVERY such maximizer near k, without assuming a differentiable or unique maximizing selection.
2. The odd-root area theorem controls the full weighted tail of `sqrt(z/f(z))`. At `z=-2/3` it bounds both f and f'. Schwarz's lemma for an inverse on an inscribed disk gives `dist(f(z),boundary)<= (1-|z|²)|f'(z)|`, with the required direction. Thus the ACTUAL finite tip radius is `<7/25+7eta<3/10`; no continuity of tips under perturbation is assumed.
3. The output natural coordinate has no singularities or zeros of P on `|v|<=3`. Rouché gives a holomorphic inverse V for `|t|<2`. `W=-V^-2` is a regular positive trajectory and satisfies `|W|>25/81>3/10` for `0<t<=7/4`.
4. A tail of the genuine support slit lifts to v tending to zero; the constant imaginary part of its square-root primitive must be zero. Both real natural-coordinate rays project to the same W by oddness. Local trajectory uniqueness therefore identifies W with the genuine slit near infinity. The closed/open membership argument extends through the whole segment: the radius gap `7/810` excludes the actual tip, and the differential is regular and nonzero. This is an application of a necessary extremal equation plus actual slit geometry, not a converse extremality criterion.
5. The uniform bound `|Z-1|<223epsilon`, `Z=tV'/V`, gives positive real part and the correct inward orientation. The finer bound `|Z-1-i epsilon q|<2000epsilon eta`, with `q=t²-2t⁴/5`, survives exact rational checking. `q(1)=3/5`, `q(7/4)=-441/640` have wide margin over the error. They produce opposite signs of the derivative of the continuous argument on ACTUAL regular slit points.
6. The signed outward angle is `arg Z`, tending to zero at infinity and having both signs. This rules out monotonicity in either direction. The ordinary unsigned angle is positive at both tested points and zero between them; it too fails monotonicity. Thus both questions, including their angle convention ambiguity, are covered.

The original PROOF has an abbreviated reciprocal-square estimate that uses `|H+H0|<7/2` after only stating `|H|<2`; that coarse displayed bound alone would not imply the sharper sum bound. The preceding `|H-H0|<5eta`, `H0=5/3` immediately supplies `|H+H0|<=10/3+5eta<7/2`. The frozen publication manuscript already states this refinement explicitly. This is a repaired exposition point, not a surviving blocker.

Goh supports rather than contradicts the classical increasing-modulus and positive-trajectory premises. Its cited classical results are not independently proved by Goh's exposition or by these finite controls. The original proof's simple-pole uniqueness statement is replaced in the manuscript with a direct local square-root-coordinate derivation; this removes dependence on an unproved uniqueness slogan.

## Could Goh's examples already supply the target failure?

The complete Brown theorem quoted on p.201 supplies coefficient functionals having no Koebe maximizer. Goh combines it with his degree-three theorem to show that certain pairs have no common extremizer. It does not provide their maps, slit constructions, or a sign reversal of argument/radial angle. Non-Koebe is not equivalent to the target failure.

As a limited independent check, for perturbations `a2+i epsilon(alpha a3+beta a4)`, the near-Koebe first-order calculation gives

`q(t)=((alpha+6beta)/3)t²-(2beta/5)t⁴`.

Pure `a3` has `q=t²/3`; pure `a4` has `q=2t²-2t⁴/5`, with its nonzero root beyond the Koebe tip coordinate t=2. The candidate's mixed `alpha=-3,beta=1` places the reversal at `t²=5/2` inside the controlled actual slit segment. These are first-order comparison controls only; they do not classify every global degree-three support or establish absence of an unknown older construction. The complete Goh article supplies no verified actual support example with the two target failures.

## Reproducibility, limitations, and disposition

`exact_controls.py` is a standalone Python standard-library program with no PDF, TeX, canonical-repository, absolute-path, or network dependency. It emits FULL JSON on stdout. `EXACT_CONTROLS.json` preserves the complete 32-check result, including exact phase/Bézout, discriminant, sum, coefficient-family, tip-radius, uniform-error and positive/negative controls. Its code does not prove compactness, classical support geometry, area/coefficient theorems, complex analytic uniqueness, or historical novelty; these limits are explicit in its JSON.

No external person was contacted; no outreach was drafted. No other shard or source agent was contacted. Work and generated artifacts remain inside this dedicated shard, on main, with no index, branch, remote, or canonical-content writes. Source and input identities are sealed separately from the pure mathematical checker. Raw images and caches are ignored.

Disposition: **no Goh1992-derived mathematical blocker; no verified source collision; bounded source comparison complete**. Parent should add accurate Goh1992 attribution and replace the obsolete pending-source paragraph in the changed package, preserving the accepted limitations for the two unavailable texts. No historical-firstness or still-open-in-2026 statement is authorized. A fresh comprehensive adversary must evaluate the parent's final changed package; this source-specific assignment issues no final package acceptance.
