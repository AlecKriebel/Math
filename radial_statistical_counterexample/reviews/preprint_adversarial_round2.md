# Independent adversarial preprint review — round 2

Review checkpoint: 26 September 2026, 21:29 UTC (14:29 America/Los_Angeles).
Reviewer: a newly assigned OpenAI Codex subagent. The proof was reconstructed
before consulting any earlier review verdict. No earlier adversarial review
report was opened. The current verification report was read only after the
independent mathematical and reproduction checks, to assess consistency.

**Verdict: no actionable mathematical, source-attribution, or preprint-package
issue found in the frozen version 1.0.1 reviewed here.** No blocking, major,
minor, or cosmetic revision is requested. This verdict is limited to the
checks below; it is neither external human peer review nor a priority finding.
Completion estimate: **100% of this round's defined review checklist**. The
separate historical-priority investigation remains unresolved.

The review did not change the manuscript, publish or upload anything, contact
any individual, or create another reviewer. Scratch evidence is under
`tmp/preprint_round2/`. The main coordinator is responsible for the subsequent
readiness-record update and rebuilt release copies; their expected intermediate
state is not a defect in this review.

## Frozen objects

| Object | SHA-256 |
| --- | --- |
| `manuscript/paper.tex` | `3a9e3cd1e012480afcb30438e5e292a6ff03c045f63b7f06dbc22654351a4482` |
| `output/pdf/paper.pdf` | `0dc15e4fa038dcb80cbfd062ac7636f2c790e42885c940626ea726626b62fd8a` |
| `output/source-and-verification.zip` at review | `a0c70c5676759784c55ad3b206b02f01113483c29114aebc352fbbd65fa20e68` |
| `output/zenodo-upload-kit.zip` at review | `919aaf3d09bc87c3f2702b59d64d82a19dd30663b6d62339b5f91e19125af768` |

The source and PDF hashes were checked both before and after the substantive
review. The archives above necessarily predate this report and the final
readiness update; their hashes identify the tested snapshot, not a promise
that later release archives have the same bytes.

## Mathematical falsification attempts

### Independent projective-curvature route

With the stated curvature and Ricci conventions, let
`eta = dt`, and write the connection difference as

\[
P_XY=\eta(X)Y+\eta(Y)X.
\]

For the product connection, `eta` is parallel. Direct multiplication gives

\[
[P_X,P_Y]Z=\eta(Y)\eta(Z)X-\eta(X)\eta(Z)Y,
\]

so, in every dimension `n >= 3`,

\[
R^1(X,Y)Z=R^0(X,Y)Z+
\eta(Y)\eta(Z)X-\eta(X)\eta(Z)Y,
\qquad
\operatorname{Ric}^1=\operatorname{Ric}^0+(n-1)\eta\otimes\eta.
\]

In particular the changed Ricci tensor is symmetric. Substitution into

\[
W(X,Y)Z=R(X,Y)Z-
\frac{\operatorname{Ric}(Y,Z)X-\operatorname{Ric}(X,Z)Y}{n-1}
\]

shows `W^1 = W^0` componentwise. For a unit Euclidean-factor vector `e3`
and a unit sphere vector `e1`,

\[
W^0(e_3,e_1)e_1=W^1(e_3,e_1)e_1=-\frac{1}{n-1}e_3\ne0.
\]

This independently excludes projective flatness of both original and
deformed connections. Kurose's duality criterion therefore excludes
1-conformal flatness of both dual statistical structures. In dimension
three, the changed connection has Ricci diagonal `(1,1,2)`, while the
original has `(1,1,0)`; the unchanged Weyl component is `-e3/2`. There is
no illicit use of the original Ricci tensor for the changed connection.

An independent scratch checker, `tmp/preprint_round2/projective_check.py`,
implements this matrix-commutator calculation without importing either
distributed verifier. In dimensions 3, 4, 5, and 6 it checks all Weyl
components, the Ricci transformation and symmetry, and the nonzero component.
The same projective change applied to a flat-curvature control has zero Weyl
tensor. All checks passed. These finite checks support the displayed
dimension-independent derivation; they are not its substitute.

The direct manuscript argument was also independently recomputed. For
`B(X,Y) = -h(X,Y)V`, the derivative terms and commutator give
`Rhat = R - h(Y,Z)A(X) + h(X,Z)A(Y)` with
`A(X) = nabla_X V - d(phi)(X)V`. The signs agree with the declared curvature
convention. The sphere and mixed planes force inconsistent values of the
same vector `A(e1)` at each point. Allowing a completely unrestricted
endomorphism makes the contradiction stronger, so no unproved differential
integrability condition for `A` is being used.

### Universal quantifiers and parameter domains

The first-variation proof applies to every center and every connection-convex
neighborhood in the usual smooth-geodesic sense of the printed question.
It uses the energy of the unique connecting segment, not an assumption that
the global distance function is smooth. The fixed initial endpoint removes
one boundary term; affine parametrization removes the interior term. A
nonconstant geodesic cannot have zero terminal velocity, and positive
definiteness then makes `dE` nonzero off the center. Its kernel is a regular
integrable hyperplane distribution. No minimizing property, global
completeness, or extension through a cut locus is required.

The projective deformation does not weaken these quantifiers. Along a
product-affine segment parametrized by `u in [0,1]`,
`t(u) = t0 + a u`. The changed affine parameter, normalized to the same
endpoint interval, is

\[
s(u)=\begin{cases}
\dfrac{e^{2au}-1}{e^{2a}-1},&a\ne0,\\
u,&a=0.
\end{cases}
\]

It is smooth, strictly increasing, and has positive finite derivative on
the entire compact segment for either sign of `a`. The `a=0` limit is
regular. The inverse reparametrization exists. Connecting paths contained
in a convex neighborhood consequently correspond in both directions;
uniqueness is preserved. Their terminal velocity vectors differ by a
nonzero scalar, and `h1 = exp(t) h0` preserves their orthogonal kernels.
Local smooth dependence follows equally from this formula and the geodesic
equations. Geodesic completeness of the deformed connection is unnecessary.

The dual formula was checked from its defining identity:
`(nabla1)*_X Y = nabla0_X Y - h0(X,Y) partial_t`. A further 1-conformal
factor `psi` produces exactly the base change with factor `t + psi`;
metric rescaling cancels correctly in `h1 grad_h1(psi)`. The cubic tensor
is symmetric and evaluates to `-3 exp(t)` on three copies of `partial_t`,
so the non-self-dual example really has nowhere zero cubic tensor.

Boundary attacks did not produce a counterexample to the proof. Dimension
two lacks the third independent direction and is explicitly outside the
claimed result. Sphere-coordinate poles do not affect the intrinsic
orthonormal-frame proof. Ordinary conformal flatness of the cylinder metric
does not supply the restricted connection change required by statistical
1-conformal flatness. The words “nowhere locally” are justified by the
pointwise contradiction at every point, not merely by one bad neighborhood.

## Direct source inspection and attribution

The following original pages were rendered and visually inspected, including
the formulas. Their hashes match the corresponding source records.

| Source PDF | Pages inspected here | SHA-256 |
| --- | --- | --- |
| `tmp/original_1998.pdf` | printed 125–126 | `fa552d73c0f1e1017608102a7a80eff048cd3d95ed413ae04c2fdf710da3b8f5` |
| `tmp/kurose_1994.pdf` | printed 428 | `adfe06cd01217b31e82d3371dd7cd50803c3ff24380a168b2db215883875d138` |
| supplied `/Users/alec/Downloads/Download.pdf` (Matsuzoe 1999) | printed 178 | `a10835acdc04536bfacb9a4c2698a5ce7d5546fd7f48cf8af4ff708baeda2bea` |

The 1998 item 3(e) explicitly punctures the neighborhood at the center,
uses the velocity at the endpoint, quantifies over every such distribution,
and asks about the dual structure. Item 3(a) explicitly includes the
Levi–Civita statistical case. No nonzero-cubic or hidden hypothesis from
another numbered question applies. Kurose's page 428 confirms the
`hhat = exp(phi) h` convention, the manuscript's alpha=1 connection formula,
and Proposition 1's projective-flatness/symmetric-Ricci criterion for the
dual. Matsuzoe's page 178 gives equation (2.1) and, immediately below it,
the exact metric rescaling making it a statistical (-1)-conformal change.
It also confirms the projective Weyl convention used in this review.

The mathematical target is correctly identified and the deformation is
correctly credited as prior work. This limited source inspection does not
establish who first assembled the counterexample. The uninspected sources
listed in `research/PRIORITY_STATUS.md` remain genuine priority gaps; this
review did not inspect them or infer their contents.

## Fresh-package reproduction

The archives were validated before extraction into new directories under
`tmp/preprint_round2/`. The source ZIP contains 43 members, with 337,808
uncompressed bytes. The outer upload kit contains 7 members, with 262,558
uncompressed bytes. Checks found no CRC failures, duplicate or case-colliding
names, absolute/traversal paths, backslash paths, encrypted entries, links,
special files, or unexpected large members. Entries are sorted regular
0644 files with the fixed release timestamp. The source archive has one
expected top-level directory; there are no downloaded third-party PDFs,
environments, scratch directories, credentials, or repository internals in
the listed package contents. The expected nested source ZIP is present only
in the upload kit.

All 42 source-manifest entries matched their files, with exact coverage of
every source member except the manifest itself. Every extracted source file
also matched its working-tree counterpart byte for byte. The two upload
payloads matched their checksums and the original source ZIP/PDF. Kit metadata
and licenses matched the source materials. The site manifest covered all
eight intended payloads and all hashes matched.

Using `/Users/alec/Documents/Math/.venv/bin/python` (Python 3.9.6,
SymPy 1.14.0), the following four runs from the extracted source directory
all exited successfully, produced no standard-error output, and matched
their bundled expected transcript exactly:

| Verifier | Normal run | `-O` run |
| --- | --- | --- |
| `verification/verify_exact.py` | exact expected output | exact expected output |
| `verification/verify_symbolic.py` | 403 checks; exact expected output | 403 checks; exact expected output |

The exact-check transcript SHA-256 is
`fd79621a0688a8fcc700cf56f63bcb53f773a0bab41f31709d452ad1cfc7debe`;
the symbolic-check transcript SHA-256 is
`a2600e983dcae371af08c5176d5cf793670fc3a92fb03a44ab108692178feb79`.
Reading the checker implementations found the expected explicit failure
checks, compatible controls, and deliberately incompatible unscaled-metric
control. The scripts do not silently rely on disabled Python assertions.

Running `build_package.py` from that extracted source directory reproduced
both ZIP archives, all generated site files, and all generated manifests
**byte for byte**. This tests deterministic packaging of the supplied PDF;
it does not claim byte-identical TeX PDF generation across engines or build
timestamps. Separately, the native desktop LaTeX compiler reported successful
compilation of the extracted `manuscript/paper.tex`. The supplied PDF was
rendered and all four pages inspected: the equations, bibliography, links,
page numbers, attribution, and version/date are legible, without clipping
or unresolved references. `pdfinfo` confirms four pages and no embedded
JavaScript.

The scratch audit driver is `tmp/preprint_round2/reproduce_package.py`;
machine-readable results and the four reproduced transcripts are saved
beside it. No original output was rebuilt or replaced during this review.

## Active metadata and publication scope

The manuscript, README, site source, CFF preferred citation, upload guide,
Zenodo metadata, API wrapper, source record, and current priority statement
agree on version **1.0.1**, date **2026-09-26**, the four-page manuscript,
the mathematical result, the Matsuzoe attribution, and the absence of a
first-resolution or continued-open-status claim. The site correctly separates
the proof from the checks and discloses AI assistance. The current verification
report is consistent with the independently checked scope. Historical reports
are not treated as new evidence establishing priority.

`CITATION.cff` validates against the saved CFF 1.2.0 schema, including format
checks. Its software-level MIT license and manuscript preferred citation
with CC BY 4.0 notice match `LICENSES.md`. The API wrapper equals
`{"metadata": metadata.json}` exactly. The saved legacy Zenodo schema
validates all recognized fields; its only full-object objection is to
`version` and `language`, fields absent from that older schema. Removing
only those two fields for the historical-schema check leaves no errors.
This is local compatibility evidence, not Zenodo server validation; the
upload guide correctly makes the same distinction and claims no existing
deposit or assigned DOI. No external submission was attempted.

Scope limits remain: this review is not an exhaustive literature audit,
independent human refereeing, proof-assistant formalization, cross-platform
test of all Python/TeX versions, remote deployment audit, or confirmation
of acceptance by Zenodo. None of those is represented as completed by this
verdict. Within the frozen preprint and package scope tested above, there
is no concrete issue requiring another manuscript revision.
