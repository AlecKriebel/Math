# Independent audit of the exponential auxiliary systems

Target: 30000707 / OWR-1460-014, rank 607. Audit date: 4 October 2026 UTC.

## Verdict

**PASS as scoped, unsolved partial research, after the explicit growth-input
clarification in CORRECTIONS.md. No full resolution is certified.**

The original frozen package was checked without modification and is retained
privately. This public projection excludes provenance-only metadata and
uses a separate safe-payload inventory. Mathematical audit sections are
unchanged.

The 37 submitted controls passed when run from a separate copy, and their
result file was byte-identical to the frozen result. A separately written
audit script passed 45 checks. These counts are supplementary evidence, not
formal verification of the analytic theorems or the unresolved problem.

No fatal algebraic error or omitted branch was found in the stated partial
results. One proof-support omission is repaired: the passage from the
maximum characteristic to each function's exact order, and the exclusion
of a mixed rational/transcendental pair, need the characteristic comparison
in Steinmetz's section 1, printed page 2, formula (Na). The corrected copy
makes that standard input and its hypotheses explicit. All acceptance here
is conditional on that correction accompanying the research notes.

The final mathematical status is **UNSOLVED, five of five substantive
approaches used**. This audit verifies existing claims and fills their
cited standard dependency; it does not pursue a sixth classification
approach. It gives no novelty, priority, publication, or DOI certificate.

## Scope and source identity

The primary problem was checked in the official [Oberwolfach report](https://ems.press/content/serial-article-files/46093),
printed pages 541–542, including a fresh visual inspection of page 542.
Both prescribed systems occur there, with the ordered auxiliaries and
the common Möbius and affine-source equivalence. The package has not
replaced the quadratic system by the linear one or assumed finite order,
bounded spherical derivative, or periodicity.

The supplied private PDF hashes agree with the source record. The PDFs
have 62, 17, and 48 pages, respectively, for the Oberwolfach report,
Steinmetz's paper, and Li–Zhai–Yi v8. The arXiv identity and date of
[Li–Zhai–Yi v8](https://arxiv.org/abs/2402.03248v8) were checked again:
6 January 2026 is the stated revision date, while its abstract-page
comment still says 39 pages. This audit makes no claim that the
48-page manuscript's theorem statement is false.

The mathematical dependencies checked are [Steinmetz's paper](https://arxiv.org/abs/1102.3383),
section 1 page 2, sections 2–3, and section 6 pages 12–14. They support
the corrected four-value background, characteristic comparison and
growth estimate, and periodic rational-in-exponential theorem. The
1987 correction to Gundersen's 1983 proof is expressly recorded in
Steinmetz's references and discussion. This audit does not claim to have
refereed every analytic dependency from first principles.

## Local multiplicities and residues

The local valuations in Proposition 1 are correct for all positive integer
orders, not only the finite grid used in the submitted controls.

At a common pole with unequal orders m and n, the two valuations are
m−1 and 2n−m−1 if m>n, with the roles reversed if n>m. They cannot
both vanish. With equal pole orders and distinct leading coefficients,
both valuations are m−1; equal leading coefficients make them at least
m. Thus every actual common pole is simple and its two residues differ.

At a finite shared value a, f'/P(f) and g'/P(g) have simple poles with
principal coefficients m/P'(a) and n/P'(a). The nonvanishing auxiliaries
force ord(f−g)=1. Hence min(m,n)=1, and their quotient has value m/n.
This proves e^(2Q(z0))=m/n with the stated orientation. The logarithmic
branches are exactly Q(z0)=±(log k)/2+πiℓ, k≥1 integer. There is no
missing sign or half-integer imaginary branch.

Solving the two leading pole equations gives A=s−e^(−Q(z0)) and
B=e^(Q(z0))−s, with s=±1 and e^(Q(z0))≠s. The sign is local to each
pole; the proof never assumes a single sign for all poles. The excluded
case makes both purported residues vanish and is not a pole. Derivative
zeros outside the three shared finite fibers, and finite coincidences
outside those fibers, would make a nonzero auxiliary vanish. Those
exclusions are sound.

## Growth and the correction

Steinmetz's section 6 theorem applies because infinity is now known to
be shared CM. Its ratio Φ is exactly the package's ψ1/ψ2, not its
reciprocal. Omitting the nonpositive pole-counting term from the upper
estimate only weakens it. With Φ=e^(2z^d), its characteristic is exactly
2r^d/π, for d=1 or 2. Absorbing the small error yields the stated
two-sided bound for the maximum characteristic off a finite-linear-
measure exceptional set.

The additional formula (Na) needs only four distinct shared values IM,
distinct nonconstant meromorphic functions, and the usual remainder.
It includes the present infinity value; the infinity modification in
Steinmetz's footnote concerns a different counting identity, not (Na).
The original proof already rules out two rational functions because
their auxiliary ratio would be rational. At least one function is
therefore transcendental, so the maximum characteristic divided by
log r tends to infinity and the stated error is o(T). Formula (Na)
then excludes one rational function paired with a transcendental one
and makes each individual characteristic comparable to T.

There is no exceptional-set gap. After taking the finite union of the
relevant exceptional sets, its tail has measure less than one. For an
individual upper bound use a good point in [r,r+1]; for a lower bound
use one in [r−1,r]. Monotonicity extends both bounds to all large r.
Thus both functions have exact order d in the non-CM branch, not just
an upper bound or a statement about their maximum. The explicit CM
classification supplies order one in the first system and excludes
the CM branch of the second.

The multiplicity-counting argument for the logarithmic-width confinement
is correct: a zero at radius r with multiplicity m contributes m log 2
at radius 2r. The first main theorem bounds m and n by a constant times
r^d; their minimum is one. The resulting bound on |Re Q| does not imply
that all multiplicities equal one.

## Complete extra-CM branch and phase constants

The corrected 2CM+2IM theorem applies as soon as one finite value is
CM, because infinity already is. Its four-value conclusion has two
omitted values and a nonidentity Möbius involution that fixes the other
two. Both possibilities for infinity are covered.

If infinity is not omitted, it is fixed; the involution is 2b−w.
Substitution gives ψ1=ψ2 identically, contradicting the prescribed
nonconstant ratio. If infinity is omitted, f and g are entire and their
second omitted value is b. The two fixed finite values are b±k and
(f−b)(g−b)=k². A global logarithm exists because f−b is zero-free on
the simply connected plane. No local-logarithm assumption is being
extended without justification.

For f=b+k exp(h), g=b+k exp(−h), the auxiliaries are
(h'/k) exp(−h) and (h'/k) exp(h). Their product gives h'/k=ε with one
constant ε∈{−1,1}. The first prescribed identity gives
exp(−h)=ε exp(Q), including every possible logarithmic branch, so
h'=−Q'. Thus the quadratic case is impossible. In the linear case
k=−ε and exp(h)=ε exp(−z). Both choices and all additive 2πi branches
give exactly f=b−exp(−z), g=b−exp(z). No free phase remains.

The source's positive pair has the negative auxiliary signs in that
ordering. A simultaneous value change w↦−w puts it in the exact
negative-sign representative's equivalence class. Such a value change
scales the auxiliaries; the stated equivalence of source representatives
does not assert that every Möbius or affine change preserves the exact
right-hand sides. The package correctly keeps these claims separate.

## Differential equation and pole recursion

The reconstruction g=f−exp(Q)P(f)/f' has the correct exponential
factor. Independent formal-jet substitution verifies the scalar equation
and its exact multiplier. On the declared open set, the multiplier is
nonzero, so equivalence of the two differential identities follows.
Neither the scalar equation nor reconstruction supplies global
meromorphic continuation or four-value sharing without extra work.

Linearization of the pole coefficient equations gives determinant
(a−s)^4(k+2)(k+3)/a². It is nonzero for all nonnegative integral k under
the actual-pole condition. Uniqueness of any actual pole germ follows;
existence and convergence of formal germs do not. In particular, the
negative formal resonances are not free nonnegative coefficients, and
periodicity cannot be inferred from periodic differential coefficients.
The package makes precisely these limitations.

## Rational endpoints and degree two

All endpoint cases in Proposition 3 were checked. At infinity, if both
R and S have poles of unequal orders m,n and L=max(m,n), the prescribed
auxiliary powers require L−2m=1 and L−2n=−1. Thus n=m+1, L=n, n=1,
and m=0, contradicting two poles. Equal orders, even with cancellation
in R−S, give equal auxiliary powers and cannot work. If only R has a
pole, its auxiliary decays. If both functions have finite limits, the
first auxiliary is bounded or decays, including roots of P as limits.
The only remaining alternative has S∼−x and R tending to a root a,
with P'(a)=−r when R−a has order r at infinity.

The zero endpoint follows by the exact involution
(R(x),S(x))↦(S(1/x),R(1/x)); it gives R∼−1/x. Hence each rational
map has total pole degree one plus the number of its common poles in
C*. These interior poles are simple and have nonzero residues.
This is the degree of the map and the number of points in a generic
fiber, counted with multiplicity. Endpoint cancellation is not silently
assumed absent. For a generic regular value away from endpoint images,
all fiber points lie in C* and are simple; the exponential covering is
unramified there. The degree bound has no hidden fiber-multiplicity
assumption.

With one interior pole, the residue formulas yield exactly the two
families displayed in (13). The x↦−x, w↦−w symmetry exchanges the
residue signs and preserves the rational identities and monicity of P.
The case c=0 belongs to an endpoint and is excluded. The case c=s
removes both residues and returns to the no-interior-pole case.
For the remaining positive-sign branch, c=2 is the complete exceptional
case in which the first 1/x term vanishes. Its two coefficient
conditions contradict each other. Otherwise q=−1, the constant
coefficient fixes B, and the remaining two factors have no common
solution for c≠1. An independent polynomial-ideal calculation confirms
both contradictions. No grid search or generic-only specialization is
being used as a completeness argument.

The periodic reduction is used only after finite order and infinity-CM
sharing have been established, matching Steinmetz's theorem. The degree
three and higher cases remain open here. In the quadratic system,
simultaneous rational dependence on exp(z²) makes both functions even
and ψ1 odd as a meromorphic identity. A nonzero even right-hand side
cannot equal it. General meromorphic functions need not satisfy that
ansatz, and no such inference is made.

## Narrow audit of the recent positivity inference

The normalized control pair F=(exp(z)+1)/2 and G=(exp(−z)+1)/2 is
nonconstant, distinct, entire, of order one, and shares 0,1,1/2,infinity
CM. In the preprint's equation (28), its ratio is exp(−2z). Thus its
Case 2 polynomial has degree n=1 and leading argument θn=π.
Its growth sector is indexed j=1 in equations (117) and (89). Taking
ε=π/12 gives the trimmed sector [−π/3,π/3], with angular exponent
3/2. The further inset used before (152) has ε0=π/18, endpoints
±5π/18, and exponent 9/5. This supplies an exact match to the
preprint's nested sector geometry, rather than only an arbitrary sector.

On both sectors, log|F(re^(iθ))|=r cos θ−log 2+O(exp(−κr)) uniformly
for some κ>0. Dividing by either r^(3/2) or r^(9/5) tends uniformly to
zero. The positive-real ray forces both proposed leading coefficients
to be zero. The logarithmic angular integral nevertheless grows
linearly and exceeds a positive multiple of T(r,F)/log r. The angular
characteristic is bounded: there are no poles, the radial boundary
integrals are bounded by a constant times the integral of t^(−ω)
for ω>1, and the circular term is O(r^(1−ω)).

Accordingly the stated lower-growth bound and bounded angular
characteristic do not force a positive leading coefficient in Lemma 13.
The failure concerns the printed upgrades before (152) and (154),
visually checked on page 39. The control pair satisfies the conclusion
of Theorem 7; it is not a counterexample to that theorem. The source's
ability to relabel a growth sector does not fix the mismatch in growth
scales. No other claim about the manuscript's correctness or possible
repairs is needed or certified.

## Publication and lifecycle limits

No source PDF, screenshot, extracted source corpus, private repository
snapshot, or private coordination belongs in the deliverable. The
corrected bundle contains original prose, references, and the unchanged
bounded algebra controls. Private visual checks stay outside it.

The historical repository checks in SOURCE_STATUS.md were read as
evidence of that investigator's gate, not independently re-certified as
the current remote state. No remote mutation, queue mutation, external
communication, release, paper, or DOI action was made during this audit.
The root must apply the current repository lifecycle gate without
resetting the five-turn budget. The mathematical label UNSOLVED must
not be promoted to a resolution or used to reopen proof search.
