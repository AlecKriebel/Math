# Source, identity, and prior-attempt audit

Checked on 5 October 2026. Metadata does not establish a proof.

## Identity

The target is ID 30005613, OWR-14297736-021, queue rank 800. The catalog
statement SHA-256 agrees exactly with the UTF-8 statement in the supplied
problem dataset: 783db58de5f1183fa9abd1cbacee659b6029b8d4ab61dd04b0fb47fb986d9ea2
(198 bytes). Full public-dataset hash/byte checks are recorded separately.
The supplied research-results dataset has no matching target entry; it is
not used as mathematical evidence.

The requested live catalog page was tried first at
https://www.unsolvedmath.com/problems/30005613 . The web reader could not
retrieve it; a direct read returned HTTP 403. No claim is made to have
verified its live contents. The exact source problem was instead checked
against the official primary report and the supplied statement identity.

## Primary problem and scope

The official report is Geometric Spectral Theory, DOI
https://doi.org/10.4171/OWR/2023/36 , workshop 20-25 August 2023, published
in the 2023 volume in April 2024. The relevant contribution is by Vladimir
Lotoreichik, joint work with David Krejcirik, pp. 2077-2078. These two pages
were visually inspected, not merely located in a search snippet. The
question concerns the Dirichlet Laplacian in a connected open subset of
R^d, d>=2, containing balls of arbitrarily large radius. The construction
uses larger and larger cubes with positive windows in their common faces.
It asks to remove both continuous spectral types. There is no boundedness,
smooth-boundary, or Neumann condition imposed on this target. The bounded
Neumann rooms-and-passages construction mentioned nearby is a comparison,
not the target operator or geometry.

Official report PDF: https://ems.press/content/serial-article-files/47475 .
The source PDF is not included in this packet.

## 2024 paper and analytic dependency

Krejcirik--Lotoreichik, Quasi-conical domains with embedded eigenvalues,
Bulletin of the London Mathematical Society 56 (2024), 2969-2981,
https://doi.org/10.1112/blms.13113 . The inspected author version is
https://arxiv.org/abs/2205.08172v2 , dated 20 May 2024 and marked accepted.
Its Section 2.2 and Section 3 give the exact norm-resolvent convergence
for the bounded shrinking-window step used in PROOF.md. Section 3 leaves
subsequent cube widths free to be chosen inductively. Section 5 leaves
singular-continuous absence open. The present argument credits those inputs
and handles complete finite spectral subspaces, including multiplicities.

## Current-literature check

David Krejcirik's Spectral geometry: old questions and new answers,
https://arxiv.org/abs/2609.28602v1 , was submitted 23 September 2026. The
public abstract page says the manuscript is in revision at Annales de la
Faculte des Sciences de Toulouse; this is manuscript status, not a claim of
acceptance. PDF page 16, visually inspected, still explicitly presents the
singular-continuous question as Open Problem 1. The preceding theorem is
numbered 2.9 in the PDF; the experimental HTML has different numbering.
The arXiv PDF version and page are the authoritative locator used here.

Searches for quasi-conical pure point and singular-continuous results did
not locate a later primary resolution. This is bounded search evidence,
not proof that no such resolution exists. The catalog's August 2026 triage
is not substituted for this fresh primary-source check.

## Actual repository checks

Read-only checks were made in https://github.com/AlecKriebel/Math :

- Exact attempt path `unsolved_math_prioritization/attempts/30005613`
  returned 404.
- The actual attempts tree c6b68b279db013a0511bfd9a3f3aa2cc2673dc5e was
  inspected and contains no directory for 30005613.
- PR searches, all states, for 30005613, quasi-conical, quasiconical, and
  the phrase Dense Pure Point returned no matching PRs.
- Branch search for 30005613 returned none; the paginated search for quasi
  returned only an unrelated quasiconformal branch, then exhausted.
- Exact-ID commit and default-branch code searches returned no matches.
- The actual QUEUE.md row is rank 800, queued, 0/5, with blank findings;
  this is queue metadata rather than an attempted proof.
- The current state.json and RESEARCH_LOG.md had no target-ID or topic
  match. They are context checks, not proof of an exhaustive history.

An initial overly broad PR query also returned PR 517, which is about the
different de Gennes problem 30005598. It does not count as a prior attempt
on this problem. Whole-repository recursive-tree retrieval failed twice;
the smaller actual attempts-tree read succeeded instead. The result is
"no matching actual attempt located," not an absolute absence claim.

## Publication boundary

Only authored mathematics, authored audit/checker material, and public
verification metadata belong in the frozen packet. No source PDF, copied
article passage, extracted source text, screenshot, raw dataset, or private
coordination file is included. No remote write occurred in this investigation.
