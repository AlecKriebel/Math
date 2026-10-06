# Arrow formula, normalization, and scope audit of PR66

Frozen head: `78f4a7fadac0fd24e147a617956cb409eb6a579e`.
Target: `10400033`, Ohtsuki Conjecture 2.11 / AMR-103-0033.

**Disposition: PASS for the bounded mathematical audit.** I found no gap in the
classical invariant-to-combinatorics bridge or tournament domination. The exact
candidate formula is supported by freshly retrieved primary sources when counts
are per crossing-subset image. A citation precision improvement is recommended
below. This report does not decide priority, whole-package readiness, or release.

## Independence and custody

This audit is **prior-opinion-exposed**, not an untouched fresh whole-package
review. I accidentally read the final “Independent review's primary convention
clarification” paragraph of the original `SOURCES.md` while reading its source
inventory. That paragraph stated the historical opinion about Östlund's symmetry
factor and reflected-path identity. I disclosed it immediately. No original
review file, sibling finding, or ROOT verdict was opened for this audit.

The exposure interval is preserved in `evidence/original_scope_read.json`. The
first conclusion was sealed at `2026-10-04T16:22:15.054188+00:00`, 3,865 bytes,
SHA-256 `caa243f72f7e4d44d3e421c71df8cba89903f9b7a5abfed15807fbccbeb74f5c`.
It records the exposure and the then-pending diagram-convention question.
`FIRST_CONCLUSION.md` was not revised as later evidence resolved that question.

Fresh curl retrieval receipts preserve observed child PID, exact argv, cwd,
UTC start/end, exit code, and stdout/stderr byte counts and hashes. Source
PDFs, extracted texts, source-containing stdout, headers, and pixels are private
under `/Users/alec/.cache/codex-pr66-arrow-audit-20261004`. One initial
source-containing stdout was relocated there; the receipt records that later
custody action explicitly. `PRIVATE_SOURCE_PINS.json` hashes the private files.
No copyrighted primary body or pixel is redistributed in this report.

The original candidate (9,121 bytes) and source record (3,676 bytes) match the
assigned SHA-256 values. All six PDFs listed in the frozen source manifest match
fresh byte counts and hashes. The additional Östlund PDF is 650,569 bytes,
SHA-256 `70626b1ab79e7cee964fa1239061b48fb088391db551f5c267b9a47c1e6c68c0`.

## Source hypotheses and exact formula

Ohtsuki PDF pages 31/33, printed 403/405, were read as bodies and pixels. The
target is every classical knot admitting an n-crossing diagram, with no
minimality, positivity, or primeness restriction. Its v3 is primitive/additive,
mirror-odd, integer-valued, and +1 on the right trefoil. Willerton Section 1,
PDF pages 1–2, supplies the same canonical normalization and
`v3=−(J'''(1)+3J''(1))/36`. The known `T(2,n)` evaluation supplies sharpness for
odd n only. [Ohtsuki primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf),
[Willerton v1](https://arxiv.org/pdf/math/0104061v1).

PV printed 446–447 defines arrows from overpass to underpass, crossing signs,
oriented-circle isomorphisms, and sign products with arrow multiplicities.
Theorem 2, printed 448 / PDF page 4, has multiplicity-one arrows and precisely
the right/left trefoil calibration. The unbased formulation does not demand a
base point. No positivity, minimality, or alternating hypothesis occurs.
The page was inspected at 200 dpi and its formula at 600 dpi.
[PV primary source](https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf).

The candidate's path tuple P is
`((3,0),(5,1),(2,4))`; write its reflected cyclic type as
`Q=((3,0),(1,5),(4,2))`. These are distinct oriented cyclic types; reversing
circle order exchanges them. The PV printed 448 unbased icon has no visible
circle-orientation arrow, so a literal tuple extraction from that icon alone
needs a circle convention. This ambiguity causes no mathematical gap: PV
printed 451 / PDF page 7 explicitly gives both alternative path formulas and
their equality on classical Gauss diagrams. Östlund printed 301 defines
`O3=Q−P`; Proposition 4(1) makes its signed evaluation zero on knot diagrams.
Zhang Remark 4.1, pages 19–20, independently displays the same reflected-path
equality. Thus either path convention yields the candidate's classical formula.
[Östlund primary source](https://journals.msp.org/mscand/article/download/775/774),
[Zhang v1](https://arxiv.org/pdf/2306.01591v1).

The important pairing distinction is image count versus parametrized embedding
count. PV's original nonbased definitions are imprecise about rotational
symmetries; Östlund explicitly identifies and corrects this in printed 297,
and explains the divisor again in printed 302. His displayed V3 at printed 301
has coefficient 1/3 for the nonbased triangle in his symmetrized-based pairing
and coefficient 1/2 for the path. A triangle image has three cyclic
automorphisms and a path image has one. Consequently the candidate's *image*
coefficients are 1 and 1/2. Multiplying the triangle contribution by three would
be the wrong convention and would fail the three-crossing trefoil calibration.

CDM Section 13.1.1, printed 375–376 / PDF pages 383–384, defines its pairing
as the coefficient in the sum of subdiagrams. It takes diagrams based/long in
that exposition; it is a definition of image counting, not by itself an
unbased symmetry correction. Zhang's conversion and Östlund's correction supply
that missing distinction. Zhang uses the reverse over/under arrow convention,
so its icons must not be copied without conversion. These hypotheses were
checked from the relevant complete pages and pixels.
[CDM author manuscript](https://www.math.cinvestav.mx/~mostovoy/cdbook/cdbook-as-submitted.pdf).

The CDM scale is `j3=−6v3`, as follows directly by expanding `J(exp(h))` and the
Willerton derivative identity. Its older bound in printed 418 is consequently
the coarse v3 bound with coefficient 1/4, not the candidate's 1/24 bound.
Abe's Theorem 3.10, PDF page 22 / printed 21, explicitly assumes a torus knot;
it cannot supply the universal step. Both are supplementary scope checks.
[Abe primary thesis](https://sucra.repo.nii.ac.jp/record/10402/files/GD0000751.pdf).
The inconsistent denominator-15 older display in Ohtsuki is quarantined by the
candidate and is not a premise of its proof.

## Universal deductions, independent of finite controls

For alternating chord endpoints, exactly one tail lies on the directed open arc
from the other tail to its head. This makes the graph edge direction unique.
For candidate P, the two intersection edges are `b→c→a`, and for T all three
edges are `c→b→a→c`. These conclusions follow by direct modular endpoint order,
and are invariant under positive cyclic relabeling. Reversing the entire circle
reverses graph edges and preserves being a path or cycle.

Each selected three-crossing subset contributes at most one pattern term.
P and T cannot overlap because their chord intersection graphs have respectively
two and three edges. In a random completion of absent graph edges, each P
subset has cyclicity probability exactly 1/2; each T subset has probability 1.
Every other subset has nonnegative cyclicity probability. Thus the signed
formula, ordinary triangle inequality, and linearity of expectation give

`|v3| ≤ N_P/2+N_T ≤ E[C]`.

Shared edges or dependent triple indicators cause no problem. The construction
is one global finite probability space, and linearity uses marginal
probabilities. There is no requirement that all signed terms agree, and no
requirement that arbitrary signs or completions be realizable by a knot.

Every tournament satisfies

`C=binom(n,3)−Σbinom(d_i,2)`

because each transitive triple has one unique source vertex. Using
`Σd_i=binom(n,2)` gives

`C=n(n²−1)/24−(1/2)Σ(d_i−(n−1)/2)²`.

The integer cycle count is at most `floor(n(n²−1)/24)` in every completion;
its expectation obeys the same integer upper bound. No integrality assumption
on v3 is needed for this last rounding step. For even n every squared deviation
is at least 1/4, giving `n(n²−4)/24`. For `n=2k` this is
`k(k−1)(k+1)/3`, an integer. The empty diagram and n=1,2 have no formula triples,
so both asserted bounds include all small cases. Composite knots and
nonminimal diagrams introduce no additional hypothesis.

This proves the exact classical target using the established formula; it does
not transfer the central difficulty to a new unsupported assertion.

## Checkable virtual boundary

The same formal count is bounded on every signed arrow diagram by the graph
argument, but it is **not** a virtual-knot invariant. An explicit counterexample
is the virtual closure of the positive three-braids `121` and `212`, with the
same bottom-to-top virtual permutation `[0,2,1]`. They differ by the usual
positive braid Reidemeister III move inside a fixed closure. Both have one
component, traversing original strands in order 0,1,2, and all three classical
crossings have sign +1.

Their Gauss arrows respectively are

`[(0,2),(1,4),(3,5)]` and `[(2,4),(0,5),(1,3)]`.

The first is P and evaluates to 1/2. The second has only one intersection edge,
contains neither P nor T, and evaluates to 0. `virtual_boundary.py` records the
strand histories and verifies these equations. The universal graph bound still
holds for each formal diagram; the invariant identity and integrality fail
outside the classical domain. This is consistent with the candidate's express
virtual-invariance exclusion and is not a counterexample to its theorem.

## Executed finite evidence

I inspected all three original verification scripts before copying them into
the disposable `replay/` directory. Original files, native ledger, index,
Git refs, PR, editor artifacts, and release state were not modified.

| Control | Observed result | Exact boundary |
| --- | --- | --- |
| Own `scope_controls.py` | PASS, 595,705 assertions | 32,054 oriented chord diagrams with 1–5 arrows; all 27,892 sign assignments for diagrams with 1–4 arrows; all 33,868 tournaments with 0–6 vertices |
| Original copied `verify.py` | PASS, 42,867 assertions | 1,814 oriented diagrams, 1,099 tournaments, 59 classical braid closures |
| Mirror/orientation/stabilization replay extension | PASS | Nine explicit classical closures, including both trefoil signs and both stabilization signs |
| Own `virtual_boundary.py` | PASS | The exact shared-closure virtual RIII construction above |

These executions support transcription and normalization. They are not the
universal proof. The own program imports none of the original code. Its final
run uses rational arithmetic throughout, including n=0. The original Jones
state sum was also checked algebraically: for one state, with `u=3w−exponent`
and `l=loops−1`, the h³ coefficient is the state sign times
`2^l*(u³/384+u*l/32)`; dividing by −6 gives the stated v3 normalization.

## Required repairs and exact remaining gap

No mathematical repair is required for the audited theorem or proof. A useful
citation improvement is to cite PV printed 451 and Östlund Proposition 4 plus
the printed 302 symmetry note directly beside equation (4). This makes the
reflected-path and embedding-versus-image conventions unambiguous without
requiring a reader to follow historical review commentary in `SOURCES.md`.

There is no remaining mathematical gap within this bounded audit. Historical
priority, current novelty, complete frozen-tree authentication, publication
metadata, and final promotion are outside this report's verdict. The accidental
prior-opinion exposure means this report must not be counted as the requested
untouched fresh whole-package reviewer. Audit completion: 100%.
