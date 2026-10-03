# Independent adversarial audit: Rubel's Problem 6.52

Audit date: 2026-10-03 UTC. Problem ID: 2306052 / AMR-022-6052. Rank: 528.

## Verdict

**PASS for the stated partial results and the proposed `unsolved`, `5/5` disposition. No mathematical blocker found.** The general question is not resolved. Neither a novelty claim nor a claim of certified present-day openness is justified or made. This audit is an independent mathematical review of the supplied note, not formal verification or human peer review.

The exact affine classification, the strict bounded-perturbation estimate, and the omitted-value selection obstruction survive the adversarial checks below. All seven frozen artifacts remain unchanged. No external publication or repository modification was performed.

## Reviewed material and integrity

The complete contents of `PROOF.md`, `README.md`, `SOURCE_GATE.md`, `STATUS.json`, `RESEARCH_LOG.md`, `verify.py`, and `verification.json` were reviewed. The SHA-256 of the supplied `FROZEN.sha256` is:

`87d64058e57661b2be187931acb3b0886a9d7ea1974aabbdb68cb9fb01dd6201`

Every entry in that manifest passed before and after the audit. The additional files in this audit directory are separately covered by `AUDIT.sha256`.

The primary statement and full accompanying update were checked in the supplied PDF text and rendered page: Hayman–Lingham, *Research Problems in Function Theory*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed p. 137, PDF leaf 138. The source asks whether each holomorphic disk surjection admits at least one bounded univalent perturbation preserving surjectivity, and attributes the question to L. A. Rubel. Its 2018 update reports no progress to the authors. This is historical evidence, not a current-status certificate.

The supplied Eremenko paper, [arXiv:math/0503750](https://arxiv.org/abs/math/0503750), was checked for the full hypotheses and proof of Theorem 2, including its meromorphic-extension discussion. This audit does not independently reproduce the packet's repository-search or literature-search history. Those bounded-search reports are not mathematical premises of the positive results.

## 1. Exact affine range classification

Write H = {Re t > 0}, T(z) = (1+z)/(1-z), and P(t) = t²-t. The identities and domain claims are correct. In particular, T is a bijection from the open disk to H and the roots of P(t)-w have sum 1. Thus at least one has real part at least 1/2, proving surjectivity of f₀ = P∘T for every complex target w.

For a = α+iβ, clearing the denominator in H yields

Q(t) = t³ + (a-w-1)t - (a+w).

Because t+1 never vanishes in H, this equation is equivalent to the original equation there. The cubic is monic for every finite a and w, and its three roots, with multiplicity, sum to zero. If there is no root in H, all three real parts are nonpositive and have sum zero; therefore all are zero. The converse is immediate. Roots on the imaginary axis correctly count as outside the open domain.

If the roots are i y₁, i y₂, i y₃ with real yⱼ, their constant coefficient is purely imaginary and their coefficient of t is real. The former forces Re w = -α and the latter forces Im w = β. Thus w = -conj(a) is the only possible omitted target. No uniqueness of omitted values for general disk functions is being assumed.

At that candidate target,

Q(iy) = -i(y³ - (2α-1)y + 2β).

The real cubic y³-py+2β, p = 2α-1, has three real roots with multiplicity exactly when p³ ≥ 27β². For p < 0 its derivative is strictly positive and only one root is real. For p = 0, three real roots occur only at β = 0. For p > 0 the local maximum and minimum give precisely |β| ≤ (p/3)^(3/2). Consequently the claimed two alternatives, including the entire range in the good case and exactly one missing value in the bad case, follow for every a and every target.

### Repeated roots, cusp, and possible degree escape

- The equality case is included. At a = (1+3s²)/2 + i s³, the real cubic is (y-s)²(y+2s). All roots remain on the boundary of H. At s = 0 this becomes a triple root and the target -1/2 is indeed omitted.
- The independent factorization f₀(z)+z/2+1/2 = (1+z)³/[2(1-z)²] verifies the cusp tip without root-count conventions.
- At a = 0 the cleared cubic has the extra factor t+1. Its root t=-1 is outside H, so it cannot create or remove an admissible solution. More generally Q(-1)=-2a; cancellation occurs only at a=0.
- The original numerator N(z)=2z(1+z)+az(1-z)²-w(1-z)² satisfies N(1)=4. No solution at the excluded pole z=1 was counted. Its degree drop at a=0 is compatible with the harmless t=-1 factor, rather than a lost solution inside the disk.
- In the half-plane coordinate the polynomial is always monic of degree three. No finite parameter is being crossed by a drop of that degree. No continuity-of-roots argument is needed.
- Since |a|<1/2 implies α<1/2, every such a is good. The bad point a=1/2 proves the stated centered-disk radius is maximal. Nonzero affine perturbations are bounded and injective, as required by Rubel's question.

No sign error, missing conjugation, boundary exclusion error, or unaccounted multiplicity was found.

## 2. Uniform bounded-perturbation stability

Theorem 7 supplies one common positive margin for all target values, not merely a target-dependent continuity statement. The transfer of h to H preserves its supremum norm exactly because the Cayley inverse is a bijection.

Fix any finite w and choose either square root s of w+1/4. This is a choice at a single target; no global square-root branch is required.

- If |s|≤1/4, the circle centered at 1/2 with radius 3/8 lies strictly in H, contains both zeros including a possible double zero, and gives the boundary lower bound 9/64-4/64=5/64.
- If |s|>1/4, select a quadratic root r with Re r≥1/2. Its radius-1/8 circle lies strictly in H. The other root is at distance 2|s|>1/2, so precisely the selected root is enclosed, and the boundary lower bound exceeds (1/8)(1/2-1/8)=3/64.

The first case includes the threshold |s|=1/4. The second case gives a strict inequality. Therefore ||h||∞<3/64 is strictly below the relevant boundary modulus in both cases, and Rouché applies on each closed disk. The disks are compactly contained in H for every fixed target, even when their location varies without bound as w varies. Their Cayley images are correspondingly compact subsets of the original disk. This validates the all-target quantifier without requiring a common compact source set.

The stated constant need not be sharp; the note does not claim sharpness. The critical value -1/4 is correctly handled by the clustered-root case. Its unique preimage z=-1/3 is critical, so the example genuinely violates the proposed uniform inverse-branch condition. Also f₀(-r) tends to zero, so it genuinely fails the strong-annularity condition. These observations are compatible with its positive bounded-norm stability margin.

## 3. Omitted-value selection obstruction

Proposition 5 is correct under its explicit hypothesis that a finite-valued holomorphic selection b exists on a whole punctured parameter disk. Lemma 1 makes |b(a)| tend to infinity uniformly as a tends to zero: for any fixed target disk, every sufficiently small bounded perturbation still covers it. This excludes both removable and essential singularities. The reciprocal extends with a zero of finite positive order m, so b has exactly a pole of order m at zero. No other poles can occur in that smaller punctured disk because b was assumed holomorphic there.

For a sufficiently small radius ρ, B=max|b| on the parameter circle is finite. Boundedness of u allows a fixed source point z₀ with |f(z₀)|>B+ρ||u||∞. The resulting boundary homotopy to -f(z₀) never meets zero. The meromorphic argument principle then counts exactly m zeros against the pole of order m. A zero cannot be at zero, because the pole is not canceled by subtracting a linear term and a constant. Thus at least one nonzero parameter contradicts the omission assumption.

A separate holomorphic reformulation confirms the pole bookkeeping. Write b(a)=c(a)/a^m with c holomorphic and c(0)≠0. On |a|=ρ compare

c(a)-a^(m+1)u(z₀)-a^m f(z₀)

with -a^m f(z₀). The strict boundary inequality gives m zeros by ordinary Rouché, while the value at zero is c(0)≠0. Each zero is a prohibited equality b(a)=f(z₀)+a u(z₀). This avoids any ambiguity about exceptional poles or the winding-number sign.

This does not establish that omitted values of a general disk-source family admit such a selection. Eremenko's Theorem 2 concerns functions entire in the source variable and uses Picard uniqueness to make the exceptional set a graph. Its meromorphic extension can differ from the assigned finite exceptional value at isolated exceptional parameters. None of those conclusions supplies the missing disk-source selection. The note correctly declines to import the theorem. No general selection theorem or resolution is claimed.

## 4. Remaining analytic and logical checks

- Lemma 1 correctly uses a finite target cover and a common positive minimum. Each local Rouché contour has at least one enclosed zero, with multiplicity allowed. The double strict inequality on its boundary is valid.
- Proposition 2 is a genuine sufficient condition with a single global margin. It is not asserted to follow from surjectivity.
- Corollary 2.1 correctly uses the common interior point and a first Rouché comparison to establish a zero of f. Its second comparison then preserves a zero for f+h-w. No nesting or exhaustion of the source domains is needed.
- Proposition 3 operates on a smaller target disk compactly inside the inverse branch's domain. The composed bounded perturbation is holomorphic there and strictly dominated on the boundary. It is a sufficient hypothesis, not a necessary one.
- Proposition 4 correctly verifies that f+a₀z cannot be constant when f is onto. Lemma 1 then makes each compact-target parameter set open. The countable intersection description alone does not imply a nonzero member; the note explicitly identifies this gap.
- The omitted-target escape statement follows from compact-target stability and does not require choosing a convergent subsequence of the coefficients beyond aₙ→0.
- The rational example supplies both good and bad bounded univalent perturbations, which refutes an unrestricted “every perturbation” strengthening but does not refute the original existential claim.
- The five recorded approaches are substantive mathematical routes: compact-target stability, uniform contours, inverse branches, affine topology/selection, and the exact rational family. Their results support the proposed unsuccessful-investigation disposition. This audit does not certify recorded work times or reinterpret `5/5` as five independent solutions.

## 5. Independent exact controls

The submitted standard-library verifier was rerun. Its output is byte-for-byte identical to the supplied `verification.json` and records 1,021 successful assertions.

`independent_verify.py` separately reproduces all 1,021 exact controls without importing or executing the submitted verifier. It uses SymPy 1.14.0 for formal identities instead of the submitted sparse-polynomial implementation. The categories are:

- 6 formal polynomial identities;
- 8 exact rational constants;
- 205 cusp, root-sum, root-product, inside, and outside controls;
- 9 named parameter examples;
- 793 strict half-radius-disk controls.

It adds 615 adversarial controls:

- 8 extra algebraic checks for denominator cancellation, homogeneous coordinate change, monicity, the discriminant, and the critical point;
- 525 exact real-root isolations on a rational (p,β) grid, counting multiplicity and comparing three-real-root status with the claimed inequality;
- 41 additional exact cusp root isolations, including the triple-root tip;
- 41 exact checks that the corresponding Cayley preimages lie on the unit circle.

Total: **1,636 passing exact controls**, of which **566 use independent exact real-root isolation with multiplicity**. These checks are finite and supplementary. They are not substitutes for the analytic proofs or for the universal quantifiers in Rubel's question.

To reproduce from the packet directory:

    python3 artifacts/verify.py
    python3 audit/independent_verify.py
    sha256sum -c FROZEN.sha256
    sha256sum -c audit/AUDIT.sha256

The independent verifier requires SymPy. Its saved result is `independent_verification.json`; the separately saved submitted-verifier result is `submitted_verifier_reproduction.json`.

## Final disposition

Accept the frozen packet as a carefully scoped, unrefereed partial-results note. No correction is required to the stated mathematical claims. Preserve `general_question_resolved: false`, the absence of novelty/current-open-status certification, and the distinction between exact algebraic checks and analytic proof review. The universal Rubel problem remains unresolved by this work.
