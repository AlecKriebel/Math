# Independent review: exact corrections of nonclosed one-forms

**Verdict: PASS_SCOPED_PARTIAL_RESULTS.** No mandatory mathematical
correction was identified. The intended connected-manifold conjecture
remains **unsolved, 3/5 attempts**. The disconnected example and the
small-perturbation obstruction are not resolutions of that conjecture.

Reviewed on 2026-09-30 by a separate GPT-6 Astra reviewer at xhigh effort.
The frozen `PARTIAL_RESULT.md` has SHA-256
`57211c9962d95f96a38c4cba61a10d20af827bbe76cf24fc4a0a71adf6a2a767`.
The author file was not edited; its bytes are preserved under `author_replay/`.
This review is not human peer review or a novelty certificate.

## Source scope

The full relevant workshop contribution and the statement on printed p.2500
of [Oberwolfach Report 47/2004](https://ems.press/content/serial-article-files/45966)
were read, and the problem page was checked visually. The operation is
addition of (df) for an unrestricted smooth real function. No smallness
condition on the correction appears there. The application is to a connected
odd-dimensional real projective space.

[Tabachnikov, *Existence and nonexistence of skew branes*, Conjecture 3.2,
p.13](https://pure.mpg.de/rest/items/item_3123074_1/component/file_3123075/content)
was also read and inspected visually. It explicitly requires a nonclosed
form, meaning that its derivative is not identically zero. Its subsequent
circle remark uses a nonzero period; that is a statement about nonexact
closed forms in dimension one, where every one-form is closed. The submitted
artifact correctly reports this mismatch without replacing the conjecture's
hypothesis. The primary-source hashes agree with the source manifest.

## Mathematical audit

**Flow-compatible criterion.** The compactness argument is valid. If the
critical set is nonempty, the continuous function (|\alpha(V)|) has a
positive minimum there; a neighborhood retains a positive lower bound.
The identity (dF(V)=0) makes evaluation of (\alpha+\lambda dF) on (V)
independent of (\lambda) in that neighborhood. On its compact complement,
(|dF|) has a positive minimum, so the stated reverse-triangle estimate
works. The empty-complement case is handled. The empty-critical-set case,
when relevant for a compact manifold with boundary, can use the empty
neighborhood and the same estimate.

The argument does not assume a Morse critical set, that (V) has unit
length, or a global fixed sign of (\alpha(V)). Its hypotheses are stronger
than Euler characteristic zero and nonclosedness of the form. In particular,
a nowhere-zero vector field supplied by Euler characteristic does not
automatically preserve a useful function (F), nor give the required
evaluation on its critical set. The product statement is read with the
compactness hypothesis of Proposition 1, as in the closed-manifold setting
of the artifact.

**All nonzero torus shears.** Since (a\not\equiv0), continuity supplies
an open interval on which (a) never vanishes. A nonnegative smooth bump
with positive integral exists inside it. The displayed (g) has mean zero,
so its integral defines a smooth periodic real function (F). If
(a(x)=0), then the bump is zero and (g(x)=1). If (g(x)=0), the point
lies in the interval where (a\ne0). Thus the two coefficients cannot
vanish together. No finite-zero, transversality, or analyticity assumption
is needed. A nonconstant periodic (a) indeed makes (a(x)dy) nonclosed;
the constant nonzero case is harmless extra scope. The excluded case
(a\equiv0) would be different because every periodic potential has a
critical point. The construction is not a normal-form theorem for
arbitrary one-forms.

**Explicit corrected form and norm.** Direct differentiation gives precisely
(\cos x\,dx+(1-\cos x)\,dy). Its squared norm is
(2(\cos x-1/2)^2+1/2), with equality in the lower bound attained when
(\cos x=1/2). The original form is nonclosed since
(d\alpha=\sin x\,dx\wedge dy\not\equiv0). All functions used are
globally smooth and periodic on the stated two-torus.

**Local index and the size of the correction.** The original coefficient map
has derivative (I) at ((0,0)), giving a nondegenerate zero of index one.
Its only other zero is ((0,\pi)), of index minus one, consistent with
Euler characteristic zero. The boundary homotopy used in the artifact is
valid for every continuous one-form perturbation whose boundary norm is
strictly smaller than the positive minimum of the original form there.
Degree one forces an interior zero. This controls the size of the one-form
(df), not merely the amplitude of its potential (f). It rules out only
an arbitrarily small correction requirement absent from the source.

As an additional independent quantitative check, the coordinate square
([ -\pi/6,\pi/6]^2) has boundary norm at least
((\sqrt3-1)/2>0). The vertical sides are controlled by (|\sin x|=1/2);
the horizontal sides by the second coefficient. Scaling its additional
(1-\cos x) term to zero preserves this boundary nonvanishing, giving
degree one directly from ((\sin x,\sin y)).

**Disconnected convention warning.** On the second torus of the disjoint
union the form is zero, and every smooth real function has an extremum.
This is a valid counterexample if nonclosedness is demanded only somewhere
on a disconnected manifold. It supplies no connected counterexample and
does not evade the stated remaining gap. The artifact preserves this scope.

## Exact checks and remaining gap

All six submitted symbolic assertions were rerun in `author_replay/`; the
generated `verification.json` is byte-identical to the submitted receipt.
The independent checker additionally verifies the correction, sharp norm
identity, both local indices, periodic shear examples with multiple zeros,
the nonvanishing algebraic condition, a flow-compatible example, negative
controls on weakened hypotheses, and the explicit boundary margin.
Its **57 exact assertions pass**. These controls support the symbolic
calculations; the general bump, compactness and degree arguments were
audited as proofs rather than inferred from examples.

The remaining task is precisely to produce suitable global data from the
original connected-manifold hypotheses, find a different exact-correction
construction, or exhibit a connected counterexample. The derivative must
remain fixed and the change must be exact. Ordinary vector-field zero
cancellation does not establish this constraint. The paper's own
critical-set argument following Lemma 3.4 also supplies context for this
type of sufficient criterion; no novelty of the elementary partial
arguments is certified here.

Recommended publication scope: a reviewed partial/obstruction package,
retaining **unsolved 3/5**, the nonclosed/nonexact distinction, the lack of
a smallness requirement, and the connectedness caveat. No mathematical
change to the frozen artifact is required.

For reproduction, run `python author_replay/verify.py` and
`python independent_checks.py`. The first rewrites its copied receipt;
the second prints JSON matching `independent_results.json`. Keep the
snapshot in `author_replay/PARTIAL_RESULT.md`, which the independent
checker hashes. Third-party source PDFs and source-page images are excluded
from the public bundle.
