# Independent priority and original-source recheck: PR 932

Verdict: **retain the theorem-novelty PRIORITY HOLD**. Fresh primary-source
inspection confirms that Winter's Theorem 1 covers the candidate's exact
all-pairs normal-Gram conclusion, without a simplicity or equal-support
assumption. The central polar/degree bridge is valid. No additional theorem
beyond that prior statement was identified in the original candidate.

**New evidence materially strengthens the chronology.** This review recovered
a successful GitHub Pages build and deployment of the exact PDF-containing
commit on September 4, 2026. The supplied starting brief's statement that no
independent platform provenance had been recovered is therefore superseded.
The evidence is described precisely below; it is not a claim of exhaustive
worldwide priority research or an Internet Archive snapshot of every page.

## Scope and immutable candidate

The input is original/public/PROOF.md at PR head
c09ef9df8b1f4642be0396ba6343344be8fa25b0. Its 21,855 bytes hash to
6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415,
matching SOURCE_SNAPSHOT.json. It describes itself as prepared October 8,
2026. ORIGINAL_PIN_CHECK.json records the fresh byte check. No original
scripts were executed and no original files were changed.

The exact hypothesis is edgewise weak comparison of corresponding interior
dihedral angles for bounded, full-dimensional, combinatorially equivalent
convex 3-polytopes, with a fixed facet correspondence. The conclusion is
equality of every labeled facet-normal Gram entry. It is not congruence of
the original polytopes. The no-simplicity and different-support cases are
part of the target, not optional extensions.

The provided DUPLICATE_CHECK.json was read as an input receipt. It reports
178 tracker rows and 197 own-account Zenodo items over eight pages, with no
same-result record or draft identified. This reviewer did not repeat the
authenticated account search; that receipt is not evidence of worldwide
priority absence. No provider, tracker, Git, release, or Zenodo mutation was
performed. There was no contact with outside individuals or other reviewers.

## Original question recovered

The fresh MFO PDF is 753,616 bytes, SHA256
47630a7d50e12e5ea3b88ef7dfaf6e7d6fc2f1d7c4fadf82785c97ff25dc5c0d.
Printed p.1198, problem 4, asks the one-edge weak-comparison question in
R^3, with an additional all-equal alternative. The full relevant page was
rendered and visually inspected. That alternative is logically redundant
when comparison is weak. Akopyan--Karasev v2, Conjecture 5.1, gives the
analogous one-corresponding-codimension-two-face question in R^d.

The original question is weaker than the candidate. The stronger theorem
implies it by reversing P and Q if all inequalities went strictly the wrong
way. The question alone would not imply the full normal-Gram conclusion.

Primary references: [MFO report](https://publications.mfo.de/handle/mfo/3583),
[Akopyan--Karasev v2](https://arxiv.org/abs/1505.05263v2).

## Fresh current and commit-pinned Winter statement

Both the live author PDF and the PDF at commit
766c313bc2187a5eafd5757dca43ffefc6a9ced6 were downloaded independently.
They are byte-identical: 289,110 bytes, SHA256
520aed6feadfdda0906f61a3d780830142d36fbbd93bca80678533ee321610e1.
The computed Git blob ID is 592725cde9a0783de0f4a6216f241ab07db2518b,
equal to the commit API's added-file blob ID. Both pages were rendered and
visually inspected, including the inequality sign and September 4 date.

Theorem 1 states the same weak adjacent-facet comparison and concludes one
orthogonal transformation carries all corresponding normals to one another,
in any dimension. Orthogonality gives every Gram entry, including
nonadjacent facets. Conversely full Gram equality of spanning normal
families implies one orthogonal transformation. Thus the candidate's
all-pairs wording is not stronger than this theorem's conclusion.

The note is an author-hosted note, not itself verified as a journal article.
Its abstract attributes its derivation to a document produced by Akopyan
with an LLM. This review makes no assertion about independent human
verification or the provenance of that underlying document.

Primary references: [live author note](https://martinwintermath.github.io/pdf/publications/Stokers_conjecture.pdf),
[exact commit](https://github.com/martinwintermath/martinwintermath.github.io/commit/766c313bc2187a5eafd5757dca43ffefc6a9ced6).

## Does the proof actually cover the target?

Yes, conditional on the explicit earlier Wachspress expansion theorem.
The complete checkable bridge is in public/DERIVATION.md. The essential
adversarial checks were:

| Potential failure | Fresh finding |
| --- | --- |
| The angle convention reverses the edge inequality | With interior angle pi-arccos(c), the normal inner product increases with angle; scaled polar edge lengths contract in exactly the required direction. |
| Rescaled target normals need to realize the source polar | They do not. Earlier Theorem 3.2 and Lemma 4.3 allow a general graph embedding. |
| Only the convex hull surrounds 0; the required Wachspress image may miss 0 | A facewise exposing functional keeps the full boundary homotopy off 0; its nonzero degree forces an interior preimage of 0. This checks the stronger, required condition. |
| The boundary Wachspress map must be injective | No. A face-preserving PL homeomorphism supplies a boundary homotopy; degree is nonzero regardless of Wachspress injectivity. |
| Nonsimple vertices break the argument | The support property and half-space separation work for faces with any number of vertices. |
| Affine equality could conceal nonorthogonal deformation | Equal radii and unchanged polar edge lengths, together with the affine equality case, force the symmetric distortion matrix to vanish; the detailed edge-direction argument is supplied. |
| Orthogonal mapping only establishes adjacent Gram entries | One common orthogonal transformation preserves every pair. |
| The theorem assumes equal support numbers or original edge lengths | Neither. Equal radii are imposed only on the auxiliary graph embedding by division by the source supports. |
| Orientation-reversing combinatorial matching destroys degree | Degree -1 is as sufficient as +1. |

The nontrivial imported machinery is Winter's expansion theorem and its
equality characterization, derived there from the Izmestiev matrix. I read
the relevant version-pinned statements, coordinate properties, and argument
sections in arXiv:2302.14194v2, including Theorem 3.2, Remark 3.7,
Definition 4.2, Lemma 4.3, and Section 4.4. This does not constitute a fresh
from-scratch proof of all spectral and convex-geometric foundations in the
paper. In particular a spectral theorem was not replaced by numerical
evidence.

The old paper's bibliographic publication is independently confirmed by
Crossref and the publisher's indexed primary page: online December 21,
2023; IMRN 2024(9), 7721--7747, DOI 10.1093/imrn/rnad298. The exact full PDF
read here is arXiv v2, submitted January 8, 2024 (its printed date is January
9). The publisher's indexed page also supplies the graph-embedding lemma
and coordinate properties; direct publisher PDF requests returned 403 and
the Warwick repository timed out. No claim of byte identity between the
arXiv PDF and the journal version is made.

Primary references: [version-pinned older paper](https://arxiv.org/abs/2302.14194v2),
[publisher](https://academic.oup.com/imrn/article/2024/9/7721/7480215?login=false),
[DOI](https://doi.org/10.1093/imrn/rnad298).

## Chronology: new platform evidence

Git commit author and committer times both read
2026-09-04T20:55:42Z, and GitHub marks the commit unsigned. Those fields
alone would not establish a platform upload time: Git allows them to be set
by the commit author. The live PDF's Last-Modified response header is
October 10, 2026, 23:13:33 GMT, which does not establish September access.
These limitations were explicitly tested rather than silently dismissed.

A read-only GitHub Actions query by the exact head SHA then returned
platform records:

| Record | Checkable evidence |
| --- | --- |
| Actions run 33918657115 | pages build and deployment; exact head SHA 766c313bc2187a5eafd5757dca43ffefc6a9ced6; event dynamic; created and started 2026-09-04T20:55:50Z; success; completed by 20:56:33Z. |
| Build job 101171625643 | Checkout, Build with Jekyll, Upload artifact all success; started 20:55:55Z, completed 20:56:20Z. |
| Deploy job 101171749682 | Deploy to GitHub Pages success; same head SHA; started 20:56:25Z, completed 20:56:32Z. |
| Deployment 6272679551 | exact SHA; ref main; environment github-pages; created 20:56:21Z. |
| Deployment success status 17842306951 | created 2026-09-04T20:56:33Z; environment URL https://martinwintermath.github.io/; links to the same deploy job. |

The public Actions page independently displays the September 4 trigger,
commit prefix, success, and build/deploy jobs. The raw API responses are
preserved privately and their hashes and a sanitized extracted record are
included in the public source pins and PROVENANCE.json.

These platform event times are materially stronger than authored Git
dates: they tie a successful Pages deployment to the content-addressed
commit containing the exact theorem PDF, before the candidate's stated
October 8 preparation. This is strong evidence supporting prior public
availability. It is not a retrieved September HTTP response for the PDF
itself. No historical site-artifact body was recovered: the run's artifact
list is empty. A later inactive status at 21:02:20Z indicates replacement of
that deployment, not failure of the earlier successful deployment.

Primary references: [Actions run](https://github.com/martinwintermath/martinwintermath.github.io/actions/runs/33918657115),
[run API](https://api.github.com/repos/martinwintermath/martinwintermath.github.io/actions/runs/33918657115),
[deployment status API](https://api.github.com/repos/martinwintermath/martinwintermath.github.io/deployments/6272679551/statuses),
[Git date documentation](https://git-scm.com/docs/git-commit#_commit_information).

## Recent analytic papers and possible residual contribution

Fresh arXiv primary pages confirm WXY v1 was submitted June 29, 2026 and Bi
v1 August 6, 2026. Their full PDFs were freshly downloaded. WXY's Theorem
1.2, Definition 2.8, and Remark 2.9 were inspected. The definition explicitly
allows maps nonsmooth at vertices and the remark discusses combinatorially
equivalent polyhedra with four or more facets at a vertex. Thus a blanket
exclusion of nonsimple vertices would be inaccurate. The displayed theorem
gives angle equality and flatness under a nonzero-degree polyhedral map.
This review did not certify its full 74-page singular-index proof or derive
every nonadjacent Gram entry solely from that displayed statement.

Bi's Theorem 1.1 concerns a smooth metric on a fixed embedded polytope.
The candidate's PL correspondence does not automatically give a smooth
metric at nonsimple vertices, so a naive metric pullback is not a verified
shortcut. The candidate instead combines Brendle's smooth-domain input,
Bi's acknowledged smoothing/cutoff family, and a globally compatible
degree-one map for the target normals. This is methodologically different
from Winter's finite-dimensional polar proof, but is not an established new
method merely because the proof is different. The precise potentially
distinct adaptation is the hemisphere-compatible auxiliary map in Section
3 together with the three-dimensional L2 boundary cutoff control in
Sections 5--7. No comparative novelty claim for that adaptation is
established here, and the original proof still needs its separate complete
analytic audit. No new theorem should be invented to rescue publication.

Neither recent analytic preprint is needed for the hold: the exact Winter
statement, valid polar bridge, and newly recovered September platform
records are sufficient for this disposition. A checkable derivation from
older machinery supports mathematical overlap; by itself, derivability
from older machinery would not establish when the dihedral corollary was
first publicly stated.

Primary references: [WXY v1](https://arxiv.org/abs/2606.30130v1),
[Bi v1](https://arxiv.org/abs/2608.06320v1).

## Disposition and validation boundary

Retain PRIORITY HOLD for the candidate as a new theorem solving
30003471 / OWR-15427-013. The adversarial effort did not uncover a missing
hypothesis that separates its theorem from Winter's. Its possible value is
as a separately validated alternative analytic proof of an already stated
theorem; no material novel result or method is certified by this review.

public/check_bridge.py supplies exact rational/integer diagnostics for the
angle-to-polar-edge sign, equal radii, a positively rescaled cube-face
nonplanarity witness, preserved boundary half-spaces, and all-pairs Gram
preservation. They are diagnostics, not a substitute for the written proof
or imported theorem. Source pins, candidate hash check, exact file manifest,
and detached hash seal make the review's scope reproducible.

This is an independent agent review of specified sources, not independent
human certification, formal verification, a guarantee of universal priority
absence, or authorization to publish, mutate a provider, or contact anyone.
