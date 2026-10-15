# PR13 fresh complete adversarial acceptance review

**Verdict: PASS for the clarified, credited partial audit.** No mandatory
mathematical revision is needed. The literal target must remain **unsolved**;
the accepted result is nonvanishing in two expressly defined repairs, with
existing public-witness attribution. No paper, DOI, new-solution claim, tracker
closure, or neighboring-question resolution is warranted. This review is an
independent AI audit, not human peer review or a formal proof certificate.

Reviewed on 2026-10-01 UTC, after the three approach-family audits and before
administrative promotion. The exact current `AUDIT.md` SHA256 is
`305deec60d853ee610f8c80b0dde791ea0e3b078e99a2110d5d58e91c2655af9`.
The preserved original PR head is
`7a845f7e025a24affe1b712cf7ada648570f9c64` (16 original files); the clarified
current manifest covers 18 files. Acceptance ordering after PR12 is an
administrative prerequisite managed by the parent task, not a mathematical
dependency.

## Independent mechanism and falsification criteria

I first read the current exposition and verifier implementations, independently
reconstructed the mechanism, retrieved and visually inspected the source
pages, and recorded `INDEPENDENT_CONCLUSION.md` at 14:02 UTC. Only afterward
did I read the historical `REVIEW.md`/verdict and the three sibling-family
reports. This is an independent adversarial reconstruction of a disclosed
witness, not an independently discovered witness. A separate subagent reached
a blind metadata/integrity conclusion before historical or sibling comparison.

The exact hypothesis is that, over `F=Q(q)`, for every `n>=3`, `X3!=0` in each
of

\[
A_n=FB_n/\langle R_2,\ldots,R_{n-1}\rangle,\qquad
C_n=FB_{n+1}/\langle R_2,\ldots,R_n\rangle.
\]

The ideals are two-sided and the elements are exactly those in the candidate.
Success requires a unital `F`-algebra representation killing every listed ideal
generator and retaining a nonzero `X3` image. Failure would include an illegal
index, omitted exceptional row, wrong inverse order, unchecked terminal row,
zero generic image, invalid specialization, or promotion from image dimension
to universal-algebra dimension. A finite suite alone cannot establish the
arbitrary-index theorem.

## All-index reconstruction

Let `S=F[u,u^-1]` and `K=F(u)`, where `u` is transcendental over `F`.
On `m>=3` coordinates use identity blocks except for

\[
B_i|_{i,i+1}=\begin{pmatrix}1-u&u\\1&0\end{pmatrix},\qquad
B_i^{-1}|_{i,i+1}=\begin{pmatrix}0&1\\u^{-1}&1-u^{-1}\end{pmatrix}.
\]

The inverse products equal the identity. Distant blocks commute, and adjacent
three-coordinate braid products both equal

\[
\begin{pmatrix}1-u&u(1-u)&u^2\\1-u&u&0\\1&0&0\end{pmatrix}.
\]

Thus this is a braid representation and extends to the group algebra. Put
`v_r=u^(1-r)e_r-u^(-r)e_(r+1)` and `lambda=-e_1^T+e_2^T`.
The whole-word convention gives
`(B_(r+1)...B_a)^-1=B_a^-1...B_(r+1)^-1`; the rightmost factor acts first.
The direct three-coordinate actions on an arbitrary vector
`(a,-a/u,0)^T` are

\[
B_rB_{r+1}(a,-a/u,0)^T=(0,a,-a/u)^T,
\quad
B_r^{-1}B_{r+1}^{-1}(a,-a/u,0)^T=(0,a/u,-a/u^2)^T.
\]

These formulas are valid for any amplitude, including zero. In translated
coordinates they send `v_r` respectively to `u v_(r+1)` and `v_(r+1)`.
All preceding factors of index at most `r-1` fix the new support
`{r+1,r+2}`. Hence, for `a<=r` and `r<=m-2`,

\[
(B_a\cdots B_{r+1})v_r=uv_{r+1},\qquad
(B_{r+1}\cdots B_a)^{-1}v_r=v_{r+1}.
\]

Direct block computation starts the recursion with
`rho(X2)=(q-u)v1 lambda`. The propagation formula with `a=1` then proves

\[
\rho(X_k)=\left(\prod_{j=1}^{k-1}(q^j-u)\right)v_{k-1}\lambda,
\qquad 2\le k\le m.
\]

The exceptional `R2` needs a separate calculation. Its two multiplier sides
send `v1` to `(q-u)v2`; the `(1-q)I` term is essential. For every ordinary
row `3<=k<=m-1`, use `r=k-1` with `a=1` and `a=2`. Both multiplier sides
send `v_(k-1)` to `(q^(k-1)-u)v_k`, so their difference kills `rho(Xk)`.
The kernel is a two-sided ideal, so these checks suffice for factorization.
For `A_n` take `m=n`; for `C_n` take `m=n+1`. The latter checks `R_n`
as a legal terminal row separately rather than assuming survival under an
additional quotient.

Finally the row-2, column-1 entry is

\[
\rho(X_3)_{2,1}=-\frac{(q-u)(q^2-u)}u\ne0\quad\text{in }S\subset K.
\]

If `X3` were zero in either original `F`-algebra quotient its image under
this `F`-algebra map would be zero. The contradiction proves the hypothesis.
No faithful representation, injective quotient map, or finite-dimensional
source assumption is used.

## Source and parameter boundaries

Fresh downloads of the [preprint](https://arxiv.org/pdf/math/0505064),
[published scan](https://web.math.ucsb.edu/~bigelow/publications/10.pdf), and
[edited-volume draft](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf)
have recorded byte hashes in `source_retrieval.json`; their relevant pages
were rendered and visually inspected in ignored scratch. They visibly retain
the terminal `sigma_n` in `RB_n`, despite generators only through
`sigma_(n-1)`. The bar denotes the inverse of the complete word. The defect
is present in the typeset pages, not merely extracted text. The source's
Section 6 unit assumption and Section 7 parameter convention give the
inherited `q` and `q-1` unit regime. `F` meets it; numerical `q=1` tests do
not belong to it. No inspected source selects one of the repairs as the
author's intended correction. The [author's errata list](https://web.math.ucsb.edu/~bigelow/publications.html)
has no correction for this item and is headed as of 2020; absence there
does not establish absence everywhere.

Evaluation `u=q^3` is legitimate on `S`, where `q^3` is a unit. It is
impossible as a homomorphism on all of `K`, because the nonzero invertible
element `u-q^3` would map to zero. The specialized model has `X4=0` when
`m>=4`, and its generic `X3` entry is nonzero in `F`. `A3` has no `X4`;
`C3` has four coordinates and does. At `u=q`, `X2` dies; at `u=q^2`,
`X3` dies. Further numerical `q=-1,u=-1` also kills `X3`, despite `q=-1`
satisfying the inherited unit regime. Thus generic nonvanishing does not say
every numerical specialization retains this witness. Numerical tests evaluate
the integral Laurent coefficient formulas, not the entirety of `Q(q)`.
`u=0` is inadmissible because the Burau block has determinant `-u`.

The checked twist identities are `B1 X2=-u X2` and
`(B1 B2)^3 X3=u^3 X3`. Their scalars are linked by
`t3=-t2^3`; independently prescribed arbitrary twists are outside this
construction. The full twist is not scalar on the entire unreduced module.
After `u=q^3` the image lies in `M_m(F)` and is finite-dimensional over `F`.
Before specialization, `1,B1,B1^2,...` are linearly independent over `F`:
applying any asserted finite relation to `v1` would give a polynomial
relation in the transcendental `-u`. A finite-dimensional module over `K`
therefore cannot be treated as a finite-dimensional image over `F`.
Neither generic nor specialized image observations supply an upper bound
for the universal quotient with extra relations. This leaves Question 7 and
the other adjacent records untouched.

## Scalar-route falsification

A scalar braid representation sends adjacent invertible generators to the
same unit `s`, by cancellation in the braid relation. Independent direct
factorization gives

\[
x_2=(1-s)(s+q)/s,\quad
R_2\text{ coefficient}=(s^2-q)(s^2-s+1)/s^2,
\]

\[
R_3\text{ coefficient}=(s-1)(q^2+s^5)/s^3,
\quad R_4\text{ coefficient}=(s-1)(q^3+s^7)/s^4.
\]

If `x3!=0`, the first branch `s^2=q` is excluded. The remaining branch
has `s^2-s+1=0`, `s^3=-1`, and `s^6=1`. `R3` then forces `q^2=s^2`.
`q=-s` kills `x2`, so only `q=s` survives, incompatible with generic `q`.
The small-rank scalar construction therefore applies to `A3` but cannot
establish the all-rank generic result. At the exceptional algebraic `q=s`,
`x4=2x3` and `R4*x4=4-8s!=0` modulo `s^2-s+1`, ruling out the fifth
strand. The sibling reproduction report's `8-4s` is the reduced numerator
with denominator `s`; dividing it in that quadratic field gives this same
`4-8s` residual. There is no inconsistency in the obstruction. The candidate
correctly records this route as blocked for the generic higher-rank task.

## Reproduction and mutation evidence

All execution occurred on copies in ignored scratch. No frozen or current
candidate evidence was rewritten. The following independent finite checks
supplement the arbitrary-index proof:

| Computation | Fresh result | Comparison |
|---|---:|---|
| Current `verify.py` | 42 cases, 1,590 assertions | Exact preserved receipt match |
| Current symbolic checker | 23 assertions | Exact preserved receipt match |
| All-index family's sparse matrix probe | 426 assertions | Every non-timestamp field matches |
| Reproduction family's Laurent-vector probe | 5,976 checks, 160 specialization cases | Every non-timestamp field matches |
| New direct-word reconstruction | 231 equality/boundary assertions | Passed; six deliberate mutation failures detected |

`replay_results.json` and `family_replays.json` bind the replay scripts and
outputs. `reconstruct_check.py`/`reconstruction_results.json` are my independent
SymPy 1.14.0 harness and receipt. Symbolic direct words use `m=3,4,5,6`;
28 rational cases use `m=3,4,7,10`, negative, unit, zero, and fractional
controls with nonzero `u`. The tests catch incorrect inverse ordering, wrong
`X3` recurrence, omission of the exceptional constant, sign corruption of
the `C3` terminal row, a scalar full-module twist claim, and an arbitrary
independent twist parameter claim. The proof's assumptions distinguish
inadmissible or degenerate controls from counterexamples.

For reproduction from the workspace, use the isolated scratch interpreter
created for this audit (Python with SymPy 1.14.0):

```
draft_pr_publication_program_20260930/audits/pr13_11000263/final_adversary/tmp/venv/bin/python draft_pr_publication_program_20260930/audits/pr13_11000263/final_adversary/reconstruct_check.py
draft_pr_publication_program_20260930/audits/pr13_11000263/final_adversary/tmp/venv/bin/python draft_pr_publication_program_20260930/audits/pr13_11000263/final_adversary/replay_candidate.py
```

The ignored runtime is not a required publication artifact; a clean Python
environment with `sympy==1.14.0` reproduces these saved scripts. Finite tests
are not a formal proof certificate or a substitute for the induction above.

## Prior review, source attribution, and integrity comparison

All three independent families agree with the conclusion after my provisional
artifact: all-index local propagation, source/attribution scope, and exact
reproduction have materially distinct evidence. Their stronger auxiliary
ring/dimension observations do not widen the canonical target claim. The
historical review passes the original `AUDIT` hash
`f363afd4932f5e1ba5d5df4141efbf182ef2c05145b631dbe0676b4b618af2f5`;
it is preserved as a historical result, not a certificate for current bytes.
The current README/readiness/acceptance summary correctly identify the fresh
complete audit as pending before this report. That wording needs an
administrative update following this audit, with a refreshed manifest; it is
not a mathematical fault.

The pinned public [Argus review package](https://raw.githubusercontent.com/Argus-AiTeam/argus-mathematics/b8f60542f758750e263016cad1d45cc0650ed64d/results/11000263/review-package.md)
contains the same two repairs and Burau induction. The
[extension README](https://raw.githubusercontent.com/Argus-AiTeam/argus-mathematics/5abed447441b42dbe9f735e8b2960ee0a0705235/results/11000263/README.md)
explicitly bounds the finite construction to its image. The primary family
and integrity subaudit verify the exact archive blob at both pins and the
unsigned author/committer dates. Those dates are repository observations,
not independently anchored first-publication or worldwide-priority dates.
The attribution to Argus AI Team is supported by its archive metadata; the
extension's displayed Zimo and Qiugu names are preserved without inventing
identities. No private correspondence, internal review, or source-author
approval is accepted as independent evidence.

The separately logged integrity subaudit validates 18 current manifest entries,
16 original snapshot files against hashes/sizes/Git blobs at the PR head,
the original review's hash binding, 34 sibling-manifest entries and 21 cached
primary/archive source entries. Metadata retains one substantive attempt out
of five, `unsolved`, no paper/deposit/tracker closure, and exact related-target
boundaries. Three public sibling report links return their local saved bytes.
See `integrity_consistency/REPORT.md` and its results for checkable details.

Two nonblocking historical/provenance nits were found. The frozen original
PR body claimed every change was inside the attempt folder despite a queue
diff; the current proposed body corrects that scope. The primary family's
archive API ledger labels the review-package's Unicode-character length
`4891` as bytes, while raw UTF-8 length is `4893`. Exact blob/SHA256/content
verification still passes. These are not current mathematical claims or hash
mixups; the original evidence should stay immutable, with this correction
recorded as an audit note. No mandatory current-candidate issue remains.

## Acceptance boundary and remaining gap

Acceptance audit completion: **100%**. This is not a percentage of resolving
the malformed original target. The strongest verified result is the generic
nonvanishing theorem for both explicit repaired algebras, with reproducible
calculations and existing-public-work attribution. Author-intended correction,
universal finite dimension after extra relations, exhaustive literature
coverage and globally anchored priority remain unestablished. They are
explicitly outside the accepted claim. Source repair is required before an
unconditional literal-target resolution can be discussed.

Recommended administrative action after PR12: publish PR13 as this credited
partial source-scope/prior-art audit, keep the literal queue target unsolved,
link this current-hash review, and preserve all historical evidence. No new
research attempt or budget reset is called for. This audit made no canonical
or Git edits and no external communication or outreach preparation.
