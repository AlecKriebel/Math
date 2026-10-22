# Independent adversarial audit: Function Theory Problem 2.4

## Verdict

**PASS for the scoped conclusion `already_solved`, with one substantive
investigation (`1/5`).** The supplied error-function proof correctly establishes
the concrete two-ray existence assertion. The historical affirmative answer is
explicitly recorded in the primary problem-list update and corroborated in the
original Hwang follow-up. There is no mathematical correction required in the
frozen packet.

This verdict does not certify a classification of all possible exceptional
values or Julia directions, the stronger historical statement about arbitrarily
many directions, or the unretrieved historical constructions. It is an
independent AI-assisted mathematical review, not human peer review or formal
proof-assistant certification.

Reviewed on 4 October 2026. The audit was performed after, and independently of,
the preparation of the ten-file author packet. Its binding SHA-256 digest is:

```
SHA256SUMS.json
09157ef0639a7f2314ead2b1864be4e8080a0d5d6536c27f31a12049decbef58
```

All nine files named in that manifest match their recorded byte lengths and
digests; with the manifest itself, the packet has exactly ten regular files and
no extra directories or symlinks. No author file was changed. No remote
repository action was performed during this audit.

## 1. The exact mathematical target

The definition and question on printed page 23 of Hayman–Lingham were read in
the source PDF, including a visual examination of the page. The update on
printed page 24 was also visually examined. The source calls a **ray** a Julia
line; it does not mean the union of two opposite rays. Its defining condition
requires infinitely many preimages of each value, except at most two, in every
positive-aperture angular neighborhood. For an entire function infinity is
omitted everywhere, leaving at most one finite exception.

The concrete terminal question asks whether a single entire function can have
distinct finite exceptional values at two different Julia directions. The
frozen proof answers this existence question. It neither needs nor claims
prescribed arbitrary directions, minimal growth, or a full classification.

The proof's exceptional-value definition has the right quantifiers: a finite
value is exceptional at a direction if **some** angular neighborhood has only
finitely many preimages. A sufficiently large tail of that neighborhood then
omits it. The proof establishes infinite preimages in **every** neighborhood
for every other finite value. It does not claim that the exceptional value is
omitted in every possible wide sector or in the whole plane.

The distinction from an asymptotic value is essential. For example,
`1 + exp(-z)` tends to 1 along the positive real axis, while any sector about
that axis strictly contained in the right half-plane omits the value 3.
Thus that asymptotic limit alone would not prove the desired Julia property.
The reviewed argument supplies both sectorial omission and a separate
normal-family contradiction.

Primary source: [Hayman–Lingham, new edition, Problem and Update 2.4](https://arxiv.org/abs/1809.07200v2).

## 2. Historical attribution and source limits

The update credits Toppila's example. Both original pages of Hwang's 1977
article, printed pages 67–68, were visually examined independently. Its opening
identifies the same Problem 2.4 and explicitly credits the affirmative answer
to Toppila, followed by Barth–Schneider using another method. This is adequate
evidence for the limited historical classification made in the packet.

Hwang's own theorem prescribes **asymptotic values** along Julia rays. It is
not being used to infer the omitted-value property. The frozen proof has an
independent analytic omission argument, so no exceptional-value theorem is
silently substituted for an asymptotic-value theorem.

The original Toppila (1970) and Barth–Schneider (1972) constructions were not
retrieved in the preparation and were not recovered in this audit. Their proofs
have therefore not been checked here. The affirmative historical attribution
comes from the identified primary update and Hwang's original follow-up, not
from a claim of reading those unavailable papers. This limitation is plainly
disclosed in the author packet and is not a blocker for the explicit witness.

The opening definitions and theorem of Gol'dberg's 1968 article were inspected
to check the neighboring-problem distinction. They concern values whose
preimage arguments are dense among all directions, including the two-value
question recorded as Problem 2.5. Such a statement has different quantifiers
from the present two-specific-ray question. The two bibliography entries
[310] and [311] in Hayman–Lingham give translated titles for the same journal,
volume, pages, and year; the cross-reference in Update 2.4 is not itself a proof
of the present claim. The frozen packet correctly avoids relying on it.

Sources examined:

- [Hwang, original article in volume 29](https://real-j.mtak.hu/7427/1/MTA_ActaMathHung_29.pdf), printed pages 67–68
- [Gol'dberg, original article in volume 19](https://real-j.mtak.hu/7416/1/MTA_ActaMathHung_19.pdf), opening at printed page 191

The three corresponding source PDF byte lengths and hashes were independently
matched to `SOURCE_MANIFEST.json`. No source copies or source-page images are
included in this audit. The exact 1967 question leaf, current catalogue access,
DOI endpoints, and live pull-request search results were not independently
retrieved during this audit. No exhaustive literature-search claim is made.

## 3. Analytic audit of the witness

### 3.1 Entire primitive and the exact tail identity

The primitive of `exp(-z^2)` defines an entire, odd function with real Taylor
coefficients. Its derivative is `(2/sqrt(pi)) exp(-z^2)`, so the proposed
function is nonconstant and transcendental.

For

\[
I(z)=\int_0^\infty e^{-t^2-2zt}\,dt,
\]

entireness follows from locally uniform integrable majorants: on `|z| <= M`,
each differentiated integrand is bounded by a polynomial in `t` times
`exp(-t^2 + 2Mt)`. The ordinary real Gaussian integral gives the tail identity
on the nonnegative real axis. The identity theorem then gives it throughout
the complex plane. That use of the real axis is legitimate because it has
limit points inside the domain of two entire functions.

For `x = Re(z) > 0`, integrating against `exp(-2zt)` gives

\[
2zI(z)=1-2\int_0^\infty t e^{-t^2-2zt}\,dt=1+\delta(z).
\]

The boundary term at infinity vanishes, and the displayed signs and factor of
two are correct. Taking absolute values only after this exact identity yields

\[
|\delta(z)|\leq 2\int_0^\infty t e^{-2xt}\,dt
=\frac{1}{2x^2}.
\]

Consequently

\[
1-\operatorname{erf}(z)
=\frac{e^{-z^2}}{\sqrt{\pi}z}(1+\delta(z)).
\]

This is an exact formula with a proved uniform remainder bound. There is no
appeal to a sectorial asymptotic expansion at or beyond an unstated boundary.
The positivity of `Re(z)` is used in the bound, and is satisfied in the wedge
where it is applied.

### 3.2 Actual exceptionality at pi/4

In the open wedge of half-width `pi/12` around `pi/4`, the angle is between
`pi/6` and `pi/3`, hence `Re(z) > |z|/2`. For `|z| > 2` the remainder has
modulus strictly less than `1/2`. Thus `1 + delta(z)` is nonzero; the other
factors in the tail identity are also nonzero. This proves actual omission
of the value 1 throughout that tail wedge.

Only finitely many remaining 1-points lie in the radius-2 disk, because zeros
of the nonzero entire function `erf(z) - 1` are isolated and a compact disk
cannot contain infinitely many of them. Therefore 1 is a finite exceptional
value in the source's sense. A radial limit alone was not used to obtain this.

At `z = r exp(i pi/4)`, the exponential has modulus 1 and `x = r/sqrt(2)`.
The same bound gives `erf(z) -> 1`, with error at most
`(1 + r^(-2))/(sqrt(pi) r)`, while the derivative has modulus `2/sqrt(pi)`.
Both ingredients needed below are established independently.

### 3.3 All other finite values, all sectors, and all tails

Fix any finite `w != 1` and any angular neighborhood of `pi/4`. If it contained
only finitely many w-points, shrinking its half-width to a positive
`eta < pi/12` and enlarging a radial cutoff would produce a tail sector
omitting both 1 and w. There is no requirement that this cutoff be uniform
in w or eta; the proof requires, and obtains, the full pointwise universal
quantifiers.

With `omega = exp(i pi/4)` and fixed `0 < d < min(1/2, eta/4)`, the maps

\[
h_R(s)=\operatorname{erf}(R\omega(1+s)),\qquad |s|<d,
\]

are holomorphic on a **fixed** disk. For `|s| < d`, their arguments satisfy
`|arg(1+s)| <= arctan(d/(1-d)) < 2d < eta`, and their moduli are larger than
`R/2`. Thus when `R > 2R0` their images in the original z-plane stay entirely
inside the tail sector. Each function omits the same two distinct finite
values. Together with the absence of poles, these are exactly the hypotheses
of Montel's omitted-values normality theorem.

Normality gives a locally spherically convergent subsequence for any sequence
`R -> infinity`. The values at the center tend to 1, so its limit cannot be
identically infinity and cannot have a pole at zero. A sufficiently small
closed disk about zero contains no pole of the limit, and the limit is bounded
there.

This last localization is important: it is not necessary to assert that a
meromorphic spherical limit is bounded on the entire original disk. On the
smaller disk, the bounded limit has a positive spherical distance from
infinity. Uniform spherical convergence therefore bounds the approximating
functions there as well. On a common bounded set the spherical and Euclidean
metrics are equivalent, so the convergence is Euclidean. Cauchy's formula
then bounds the derivatives at zero along the subsequence.

But the chain rule gives

\[
|h_R'(0)|=\frac{2R}{\sqrt{\pi}}\longrightarrow\infty,
\]

a contradiction. An equivalent independent check is that the spherical
derivative at zero is asymptotic to `R/sqrt(pi)`, since `h_R(0) -> 1`; this
violates Marty's local boundedness criterion for a normal family. Marty's
theorem is not needed by the frozen proof.

Thus the assumed finite-preimage sector cannot exist for **any** `w != 1`.
Every such w occurs infinitely many times in every neighborhood of the ray.
Those preimages must have unbounded modulus by isolation of zeros on compact
sets, so the assertion also holds after any finite radial cutoff. This
addresses the stronger infinite-preimage requirement, rather than merely
establishing nonnormality without identifying the exceptional value.

### 3.4 Reflection and arbitrary distinct target values

The symmetry actually used is

\[
f(-\overline z)=-\overline{f(z)}.
\]

Negative conjugation preserves modulus and maps an angular neighborhood of
`pi/4` bijectively onto the corresponding neighborhood of `3pi/4`. The value
correspondence is likewise bijective, `w <-> -conjugate(w)`. Hence the latter
ray has unique finite exceptional value -1, with every other finite value
taken infinitely often in every neighborhood.

The commonly tempting substitution `z -> -z` would instead send `pi/4` to
`5pi/4`; it is not the substitution made in the frozen proof. The two actual
rays are distinct even if one ignores their orientations.

For arbitrary complex `a != b`, the affine map
`u -> (a+b)/2 + (a-b)u/2` has nonzero slope and sends 1 to a and -1 to b.
It preserves every finite-versus-infinite preimage assertion exactly. No
restriction to real a and b is present in the proof. Equality of a and b
would destroy bijectivity, and is correctly excluded.

## 4. Independent computational and integrity checks

- The author's 42 finite controls replayed successfully and produced a
  byte-identical `CHECKS.json`.
- The auditor's separately written `independent_checks.py` passed 60 additional
  finite controls. These include direct complex integral quadrature, the
  integration-by-parts identity, remainder estimates, rational disk bounds,
  spherical-derivative bounds, reflection, and complex affine target pairs.
- Nine numerical preimages were found for the finite values 0, 2, and i.
  For each target, the three samples have increasing moduli and decreasing
  angular displacement from `pi/4`. Their residuals are below `1e-60` at
  70-digit working precision. These are diagnostic samples only.
- Negative controls distinguish oddness from negative conjugation, reject
  equal target pairs, and expose the failure of deriving derivative growth
  merely from a finite asymptotic limit.
- All ten author files were verified before and after the audit. Three
  source PDF digests were independently checked. The audit files have their
  own inventory and hashes.

None of these numerical checks proves an infinite-preimage assertion,
Montel's theorem, or any asymptotic conclusion. The analytic review in Section
3 supplies those arguments. Floating-point quadrature and root finding are
explicitly non-rigorous diagnostics, not interval certificates.

Replay the extra diagnostics from this audit directory with Python 3 and
mpmath 1.3.0:

```
python independent_checks.py > /tmp/2302004-independent-results.json
cmp independent_results.json /tmp/2302004-independent-results.json
sha256sum -c SHA256SUMS
```

## 5. Prior-work scope and publication disposition

The saved nonrecursive repository listings were checked as a chain from the
recorded main commit through the queue directory to its attempts directory.
Each listing explicitly reports `truncated: false`, and the complete attempts
listing contains no child named `2302004`. The saved recursive listing is
truncated and was not used to establish absence. This verifies the packet's
limited directory-based check at the recorded snapshot; it is not an
exhaustive search of every branch, commit, or pull request.

Live all-state PR, code, and branch searches were not repeated by the auditor.
PR 491's attribution to neighboring Problem 2.5 remains a reported source-gate
check, rather than an independently refreshed remote-state result. The
primary-source distinction between Problems 2.4 and 2.5 was independently
confirmed and is sufficient for the mathematical audit.

The terminal existence question is answered, historical priority is retained,
and the completed direct verification is one substantive investigation rather
than five artificial turns. Therefore the proposed `already_solved` and `1/5`
status cells are justified within the stated scope. This audit requires no
change to the frozen author files and no publication override. Other queue
cells and unrelated repository content are outside this review.

The public audit contains only original review text, short original numerical
diagnostics, results, and hashes. It contains no source PDFs, OCR, page images,
copied corpus records, private paths, credentials, or coordination transcripts.
The historical retrieval limitations must remain visible when the packet is
published.
