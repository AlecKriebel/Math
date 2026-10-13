# Independent adversarial algebraic/Galois review

Verdict: **PASS_ALGEBRAIC_GALOIS_REMIT** for the frozen original PR 278,
problem 30005468, head deb9d7491a0bf887f7615717a5b484caf212cfd6.
No algebraic correction or proof repair is required within this family's remit.
This is an audit result, not a solved-label, novelty, or priority decision.

The exact accepted claim is that the displayed rational ternary quartic is
a sum of two real polynomial squares and is not a finite sum of rational
polynomial squares, even allowing inhomogeneous summands of arbitrary degrees.
The origin argument also excludes rational SOS membership of this quartic
in the displayed rational unit-ball quadratic module at every finite degree.
DERIVATION.md supplies the universal proof; computations supplement it.

## Mechanisms, evidence, and exact gaps

| Claim or attack | Mechanism and evidence | Finding / remaining gap |
| --- | --- | --- |
| Wrong quartic coefficients or norm sign | Fresh scalar 6-by-6 Sylvester resultants, exact recovery of all 15 homogeneous quartic coefficients on a matrix of determinant 47,775,744 | PASS; every coefficient, including six zeros, matches |
| Hidden real root of h(t)=t^4-t+1 | Elementary interval inequalities and independent exact Sturm sequence | PASS; no real roots, including boundary values 0 and 1 |
| Invalid Frobenius primes or repeated factors | Discriminant 229, mod-2 Frobenius irreducibility criterion, mod-3 irreducible cubic coprime to the linear factor | PASS; primes 2 and 3 are unramified |
| Proper subgroup masquerading as S_4 | Factorization cycles 4 and 3; unique-index-two subgroup argument; finite generation for all eight 3-cycles | PASS; group is S_4 |
| Real-zero descent or projective normalization failure | Explicit coordinates [ab:-(a+b):1]; conjugate pair gives real nonzero vector | PASS; no normalization ambiguity |
| Galois images fail to cover all six intersections | Rational coefficients stay fixed; S_4 acts transitively on six unordered pairs | PASS; one real pair suffices |
| Coincident or insufficient zeros on a line | Nonzero Vandermonde minors; three distinct finite points on each line | PASS; each restricted quadratic is identically zero |
| Rational quadratic survives all six points | Each of the four distinct linear forms divides it; product has degree four | PASS; candidate is zero, contradicting f(1,0,0)=1 |
| Inhomogeneous or higher-degree rational SOS escape | Highest square terms cannot cancel over the reals; constant then linear jets vanish | PASS for arbitrary finite sums, with no search-degree cutoff |
| High-degree ball multipliers cancel the obstruction | Origin weights positive; fourth-order jet rational SOS; ball correction begins in degree six | PASS for displayed generator; separate module family owns broader quantifiers |
| Wrong beta root, denominator, or identity | Direct Q[B]/(B^3-4B-1) arithmetic, B^-1=B^2-4; all 15 residuals zero; exact root counts | PASS; either negative root works; all roots nonzero |

There is no unresolved gap in these algebraic statements. General module
descent, intended source-question interpretation, algorithmic minimal-degree
behavior, and novelty are outside this acceptance.

## Adversarial boundary checks

The quartic vanishes at the origin and both real conjugate-pair projective
points, so its nonnegativity is not strict. Adding one gives minimum exactly
one on the ball. A strict minimum greater than one would be false here.

The coefficient list sigma_0=f, sigma_1=0 is rational when its square factors
may be real. The nonexistence assertion must continue to refer to rational
coefficients of the polynomials being squared. A rational multiplier polynomial
alone is a weaker requirement. A rational positive-semidefinite Gram matrix
is equivalent to rational squares after rational diagonalization and writing
its positive rational diagonal weights as finite sums of rational squares.

The same moment vector has the rational-square separator 1+x^4, so the example
does not establish irrationality for every separator. For 0<c<1, cp-1 is
negative at the origin and cannot belong to either normalized ball module.
At c=1, the origin obstruction holds. For rational c>1, the submission invokes
Powers's strict-positivity theorem. This family does not independently certify
that theorem's body; the separate source/module families handle it.

The beta identity is a real SOS only when beta is negative. There are two
negative roots, not just the one in (-2,-1); both work. The positive root
gives the algebraic identity but not a sum with positive real square weights.
No coefficient verification uses approximate roots.

## Independence and comparison

INDEPENDENCE_SEAL.json was created at **2026-10-06T17:57:47.268339Z**, before
any original independent-review body or another family's report was read.
Its SHA-256 is
9a7db2b6e9bc69e161508880ac0965a2ed0a81b569ab23ba5bd624c17be14fb7.
Exact sealed copies are preserved under sealed/, with SEALED_COPY_BINDING.json.
The sealed derivation and findings remain unchanged; the continuing research
log has its sealed version preserved separately.

After sealing, this family read the original INDEPENDENT_REVIEW.md,
independent_check.py, its receipts, source notes, and review manifest.
Their algebraic sections agree with the independent result. Their finite
checks correctly supplement the Galois and all-degree arguments. No
algebraic overstatement or transfer to an unsupported non-SOS conjecture was
found. The original source-coverage verdict is broader than this family's
verdict and is not adopted without the separate source-family assessment.
The original 2,345-control SymPy checker was source-reviewed but not
re-executed; its historical receipt is not a fresh execution in this audit.

After this seal, the moment/module family reported a sealed symbolic universal
six-intersection determinant equal to minus the Vandermonde product squared.
This agrees with the line restriction proof. It is recorded as reported
corroboration and is not a premise of this family's acceptance.

The relevant primary publisher bodies were also read after the seal:
Theorem 2.1, construction 2.2–2.4, Lemma 2.5, Theorem 2.6, and Example 2.8
identify the same quartic, norm construction, and beta identity.
[Scheiderer, JEMS 18 (2016)](https://ems.press/content/serial-article-files/32129).
This check used publisher PDF text, not a new byte-hashed local PDF capture.
The source family owns immutable source bindings and original-question coverage.

## Reproducibility and disposition

The fresh exact_controls.py uses only the standard library and is independent
of the submitted checker: scalar resultants and interpolation replace the
multiplication-matrix polynomial determinant; direct quotient-field expansion
replaces denominator clearing. It passed **69 exact assertions**, with all
coefficients explicitly recorded. No floating-point arithmetic is used for
mathematical results.

Submitted verify.py was read before execution, copied into replay/, and
passed **2,059 assertions**. Its 504-byte stdout SHA-256
434a1cd7a7174de9dad34eee2b607d171e4cab0f3d631ec04bdb0fb27f4a5752
matches frozen CHECKS.json byte-for-byte. All 18 snapshot file byte counts
and SHA-256 values match the original snapshot MANIFEST.json.

The pinned CPython executable and engine match original runtime pins.
Qualification and both controls ran isolated and unoptimized. Child PIDs
**19681**, **19684**, and **19685** were launched, communicated with, and
reaped by recorder PID **19673**, each with return code 0. Every launch has
prelaunch bindings, request, started and execution records, and complete raw
stdout/stderr. All stderr streams are zero bytes. These qualifications bind
recorded binaries without claiming identical dynamic system dependencies.

Recommended disposition from this family: accept the algebraic obstruction
and displayed-ball jet consequence as verified. Retain the fixed-polynomial
quantifier, rational-square definition, minimum-one normalization, and
classical credit. Leave original-question coverage, priority, claimed-solved
promotion, and public-state decisions to the root after the other families.
No author/source/live files were edited, no Git or provider state was mutated,
and no outside individual was contacted.
