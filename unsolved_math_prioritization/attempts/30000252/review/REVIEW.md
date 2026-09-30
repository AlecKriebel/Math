# Independent source-application review: critical polyharmonic uniqueness

**Verdict: PASS_KNOWN_NEGATIVE_ANSWER_UNRESTRICTED.** The cited published
theorem supplies the claimed counterexample to unrestricted critical-endpoint
uniqueness. It therefore answers negatively the literal question whether
Theorem 5 extends as a whole. No mandatory mathematical correction was found.
The separate positive-only higher-order variant is not classified here.

Reviewed on 2026-09-30 by GPT-6 Astra at xhigh effort, independently of the
source-application author. The frozen `KNOWN_RESULT.md` has SHA-256
`401cf0b937e23c22f8da09a4b26890cdd64f1a27aae7a3cadffebbcb123ef888`.
Its bytes were not changed and are preserved under `author_replay/`.

## 1. Source and scope adjudication

The original workshop contribution, including Theorem 5 and its endpoint
question on printed pp.1616–1617, was read. Both relevant pages were also
inspected visually in the [full primary report](https://oa.tib.eu/renate/server/api/core/bitstreams/91dd0822-361f-44ee-a77f-fa862bb21ab6/content).
The question asks whether the stated theorem extends to the critical
exponent. Its unrestricted uniqueness conclusion is a constituent of that
theorem, not an additional hypothesis imposed on its positive-solution
conclusion. A valid counterexample to unrestricted uniqueness therefore
disproves the proposed extension as a whole and the dataset's unqualified
uniqueness formulation.

This does not logically settle every restricted variant. Two solutions of
unspecified sign need not be two positive solutions. Accordingly the
recommended queue status is **already_solved**, meaning a known negative
answer to the literal umbrella question, with the explicit qualification
that this application does not classify the separate positive-only
higher-order problem. If that restricted problem is separately catalogued,
its status must not be inherited from this verdict.

The displayed operator in the report is \(-\Delta^m\), whereas the standard
operator and its positivity remark use \(( -\Delta)^m\). The application
retains this discrepancy and uses odd order three, where the two coincide.
The report is numbered 29/2005 and concerns the 2005 workshop; the imported
“2006” label does not affect the mathematical application.

## 2. Published multiplicity input

The full author-hosted version of
[Clapp–Squassina, *Nonhomogeneous polyharmonic elliptic problems at critical
growth with symmetric data*, CPAA 2(2) (2003), 171–186](https://www.dmf.unicatt.it/~squassin/papers/lavori/clapsqua.pdf)
was available. The problem on p.171 and Corollary 1.1, its relation to
Theorem 1.3, and the regularity statement on p.172 were checked directly
and visually. The corollary gives two distinct solutions for every nonzero
forcing sufficiently small in the dual Sobolev norm. It imposes no
nontrivial group action, special topology, or exclusion of the center of
a ball. The trivial group in Theorem 1.3 is expressly discussed immediately
after the regularity statement.

The source explicitly gives regularity up to the boundary for smooth enough
boundary and Hölder forcing. This audit accepts the published multiplicity
and regularity statements as analytic inputs. It does not independently
reconstruct their variational, concentration-compactness, or elliptic
regularity proofs. The article predates the workshop question; this package
is a credited source application, not a new multiplicity result.

## 3. Scaling and all hypotheses

For the critical exponent, set

\[
p=\frac{n+2m}{n-2m},\qquad q=p+1=\frac{2n}{n-2m},\qquad
a=\frac1{p-1}=\frac{n-2m}{4m}.
\]

If (v=\lambda^a u), linearity of the differential operator and
homogeneity of ( |u|^{p-1}u ) give

\[
(-\Delta)^m v
=\lambda^{a+1}+\lambda^{a+1-ap}|v|^{p-1}v
=\lambda^{p/(p-1)}+|v|^{p-1}v.
\]

The identity (a+1-ap=0) is the essential cancellation. The exponent in
the published right-hand side is (q-2=p-1), exactly as needed. The inverse
scaling works for every positive parameter, preserves distinctness, and
does not impose any sign condition on a solution.

The constant functional (1\in H^{-m}(\Omega)) has finite, strictly positive
norm (C). Finiteness follows from the continuous Sobolev inclusion into
(L^2) on a bounded smooth domain, and positivity follows by pairing with a
nonnegative nonzero smooth compactly supported function. Thus the forcing
has norm (C\lambda^{p/(p-1)}). The stated threshold

\[
\lambda_0=(\kappa/C)^{(p-1)/p}>0
\]

ensures that every (0<\lambda<\lambda_0) satisfies the corollary's strict
smallness condition. The forcing is nonzero, and the zero function cannot
solve the forced equation. Consequently both solutions are nonzero.

For (m=3,n=7), the relevant numbers are (p=13,q=14,a=1/12). The unit
ball is smooth, bounded and conformally contractible: (\xi(x)=-x) has
(D\xi+D\xi^T=-2I), divergence (-7), and flow (e^{-t}x), which
strictly preserves and contracts the ball for positive time. The requirement
(p\ge2) in the unrestricted uniqueness clause is met. At this odd order,
((-\Delta)^3=-\Delta^3). Since (|u|^{12}u=u^{13}) for every real (u),
the displayed example is valid for solutions of either sign.

The homogeneous linear problem at (\lambda=0) has only the zero solution
by the coercive Dirichlet energy. That isolated endpoint cannot rescue
uniqueness on any positive interval, because two distinct solutions exist
for every sufficiently small positive parameter.

## 4. Boundary conditions and regularity

The paper's (H_0^m) Dirichlet data are zero normal derivatives through
order (m-1). For a smooth function on a smooth boundary these are
equivalent to the zero full boundary jet used in the workshop. In boundary
normal coordinates, differentiate each zero trace tangentially; induction
on total order eliminates all mixed derivatives. Terms arising from changes
of frame involve lower-order jets, which already vanish. For (m=3) this
gives (u=\nabla u=D^2u=0) on the sphere.

No Navier condition is substituted. As a direct diagnostic, in dimension
seven the test function (w=(1-|x|^2)^3) has zero full jet through order
two on the unit sphere, while (\Delta^2w=-864) there. It therefore
distinguishes these Dirichlet conditions from the third Navier trace. This
test function is not asserted to solve the nonlinear problem.

The forcing is constant and the ball has smooth boundary, so the published
regularity statement supplies (C^{6,\alpha}(\overline{B_1})) solutions
for a Hölder exponent (0<\alpha<1). These satisfy the classical solution
regularity required for the counterexample; no weak/classical gap remains
after importing that stated regularity theorem.

## 5. Verification boundary and publication recommendation

The 8,403 submitted exact assertions reproduce their receipt byte for byte.
The independent checker verifies symbolic scaling, the critical exponent,
the odd-order sign, the conformal field and flow, and the distinction between
the full Dirichlet jet and Navier data. Its **53 exact assertions pass**.
These controls do not construct PDE solutions or certify the imported
analytic theorem; that limitation is explicit in both the source artifact
and this review.

Recommend a source-correction package credited to Clapp and Squassina,
recording the single source-application route and a known negative answer
to unrestricted endpoint uniqueness. Keep the positive-only qualification,
the operator-notation discrepancy, the exact boundary conditions, and the
absence of an independent reconstruction of the published analytic theorem.
No campaign novelty or human peer-review claim is warranted.

Run `python author_replay/verify.py` and `python independent_checks.py` to
reproduce the receipts. The first writes its copied receipt; the second
prints JSON matching `independent_results.json`. Keep the frozen source
snapshot used by the hash check. Source PDFs and rendered third-party pages
are excluded from the public bundle.
