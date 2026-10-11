# Acceptance and continuing normalization boundary

Problem 30001876 / OWR-11135-003. Prose edition dated 11 October 2026.

**SCOPED SPECTRAL RECONSTRUCTION ACCEPTED; TWO CONDITIONAL CONVENTION-RELATIVE LOCAL IDENTITIES ACCEPTED; BLANKET LITERAL PRINTED CONSISTENCY REMAINS HELD.**

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made.

## Chronology matters

PROOF.md retains the complete initial authored reconstruction and mathematical audit. At that stage the exact closed gamma factor was held pending an independent match of the underlying normalization conventions. AUDIT.md is the subsequent complete independent challenge. It confirms the algebraic contradiction and stabilizer multiplicity, supplies a corrected-import Bessel–Mellin–Barnes calculation, and exposes the previously untracked interchange of power-function parameters. This later calculation narrows the earlier hold; it does not erase the history or pretend the original report had already established the later identities.

The combined acceptance is the precise scope below. The full source theorem, its sharp bound, and all original displays together are not adjudicated.

## Accepted claims

- In the level-one spherical Hecke–Maass cuspidal setting, the upper block-diagonal restriction with scale has the integral-defined GL2 cusp-plus-Eisenstein spectral reconstruction, with the stated standard analytic imports.
- The global constant eigenfunction component and all odd cusp coefficients vanish at each scale; this does not assert that the restricted function is a GL2 cusp form.
- The Mellin frequency is 2t; inversion has factor 1/pi and the integrated norm identity has factors 1/pi and 1/(4 pi^2). L2, regularized pointwise, and smooth pointwise assertions retain their distinct hypotheses.
- The printed equations (3.13), (3.18), (3.19), (3.20) are algebraically inconsistent as simultaneous literal assertions, and the stated U2 with ordinary hyperbolic measure has a stabilizer factor 2.
- Conditional on the corrected imported Takhtadzhyan–Vinogradov Bessel formula, the fully matched local Mellin/Barnes calculation gives I_lambda=P(lambda)/8.
- For literal Li–Young (2.3), eta1=nu2-1/3 and eta2=nu1-1/3 give lambda=(-A,-B,-C), hence 8J=P_plus/D.
- For the explicitly interchanged Bump power exponents, eta1=nu1-1/3 and eta2=nu2-1/3 give lambda=(C,B,A), hence 8J_Bump=P_minus/D. The printed final expression (3.19) survives in this convention through compensating intermediate errors.

## Both conventions, fully specified

Write A=1-nu1-2nu2, B=-nu1+nu2, C=2nu1+nu2-1, so A+B+C=0. Let

D=pi^(1/2-3nu1-3nu2) Gamma(3nu1/2) Gamma(3nu2/2) Gamma((3nu1+3nu2-1)/2),

P_plus/minus(s,tau)=pi^(-3s) product over q in {A,B,C} and epsilon in {+1,-1} of Gamma((s+epsilon i tau +/- q)/2).

In each convention, W_J is the raw Jacquet function for that convention, W*=D W_J, and

J_tau(s)=integral W_J(diag(ab,a,1)) K_(i tau)(2 pi b) (a^2 b)^s da db/(a^2 b^2).

The lower diagonal ratio remains a and the GL2 K function remains at b. No a/b switch, contragredient substitution or Fourier-index exchange is implicit.

1. Literal convention: I_nu(diag(ab,a,1))=a^(nu1+2nu2)b^(2nu1+nu2). It matches Blomer with eta1=nu2-1/3, eta2=nu1-1/3, lambda=(-A,-B,-C). The conditional conclusion is 8J=P_plus/D.
2. Explicit Bump convention: I_nu^Bump=a^(2nu1+nu2)b^(nu1+2nu2). It matches eta1=nu1-1/3, eta2=nu2-1/3, lambda=(C,B,A). The conditional conclusion is 8J_Bump=P_minus/D, exactly the expression printed in (3.19).

For either fully specified Fourier expansion, the ordinary-measure even period is Lambda_j=8 conjugate(rho_j(1)) L_j J_tj, with the analogous Eisenstein formula. Its three factors 2 come respectively from the U2 stabilizer, the GL2 K normalization, and signed-index pairing. Changing the Whittaker convention requires interpreting the Fourier expansion and its coefficients in that same convention; no unproved coefficient identification across conventions is asserted.

The corrected completed Bessel identity has leading constant 8. Its double Mellin transform has constant 8*(1/4)*(1/4)*(1/2)=1/4. The last K inversion contributes 1/4, and z=2w contributes 2, giving I_lambda=P(lambda)/8 after Barnes second lemma. The full derivation, convergence region, meromorphic continuation, mapping and import limits are in AUDIT.md, sections 5–6.

In the Bump reading a coherent repair uses 8 rather than 4 in the defining local period integral, I(W*)=P_minus/8 without a D denominator, and the restored stabilizer factor in unfolding. The earlier Stade comparison constant becomes 2 rather than 4, with its parameter swap explicitly tracked. The final expression survives because intermediate factor errors compensate. Merely publishing a factor-two correction, or merely removing a D denominator, would not capture this reconciliation.

## What remains held and outside scope

- Blanket literal consistency of all original definitions and gamma displays remains held.
- No single convention is silently selected; the change to the power function is material, and generic opposite spectral triples are not permutations.
- The factor-two unfolding finding alone is not a certified factor-two correction of the final printed period formula.
- No conclusion that the final restriction theorem is false and no paper-wide theorem acceptance; sections 5–10 and the sharp eigenvalue-aspect bound were not proof-audited.
- The corrected Bessel formula, Barnes second lemma, spectral theory, cuspidal derivative decay and reduction theory remain identified imports; the original Takhtadzhyan–Vinogradov and Stade proofs were not inspected.
- No extension to arbitrary automorphic representations, levels, K-types, noncuspidal forms, regularized periods or embeddings; no unjustified exchange of the full j,t,tau inverse family.
- The OWR introductory motivation is contextualized as existing joint work. No new unsolved conjecture, new restriction theorem, novelty, priority or exhaustive literature certification is claimed.
- Whole-file retrieval and byte authentication do not mean whole-paper reading, full dependency-proof audit or formal mathematical certification.

## Evidence, provenance and distribution

The creator’s closed 60-member evidence package and the independent challenge’s closed 36-member package were reauthenticated against independently supplied manifest digests. Complete original authored reports remain unchanged; only public editorial framing and removal of private coordination references distinguish the distributed reports. All mathematical sections, arguments, formulas, import qualifications, inspection limits and the original hold are retained.

Historically, the creator recorded 12 arithmetic/transcription diagnostics and 11 inventory cases (one valid fixture and ten corruptions) under normal, -O and -OO Python. The independent challenge recorded 20 exact mapping/prefactor checks and four 45-digit Barnes contour evaluations using two nonsymmetric opposite triples and two contour cutoffs, plus a zero-triple integral and a sign-sensitive comparison. Its recorded numerical result is normal Python; no all-mode numerical claim is inferred. Independent inventory controls used one valid fixture and seven corruptions under normal, -O and -OO. These finite checks are diagnostics, not substitutes for the imported Whittaker identity or automorphic proof.

Edition preparation adds no new mathematical experiments or scholarly-source inspection. It rechecks exact bytes, editorial retention, public-file membership and a prospective additions-only patch. Only eight authored prose/metadata files are distributed, excluding copied sources, source images/extracts, dataset contents, code, raw outputs and private coordination material. Source hashes and acceptance labels do not establish a mathematical theorem or publication permission by themselves.
