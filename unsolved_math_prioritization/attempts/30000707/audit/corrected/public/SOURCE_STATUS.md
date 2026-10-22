# Source, status, and provenance

Checked 4 October 2026 UTC. This is bounded source research, not a complete
literature review or a novelty certificate.

## Exact primary problem

* Requested catalogue: https://www.unsolvedmath.com/problems/30000707.
  Both the web reader and a direct HTTP check were tried. The latter
  returned HTTP 403, with a Vercel denial. No access restriction was
  bypassed.
* Numeric ID 30000707 / OWR-1460-014 was extracted from the pinned
  UnsolvedMath catalogue corpus. Its August 2026 literature assessment
  says open; that assessment is only triage. The pinned prior-report
  corpus contains no entry for this ID/code; the absence was recorded,
  rather than manufacturing a previous attempt.
* The actual primary statement was read in the official
  [Oberwolfach report](https://ems.press/content/serial-article-files/46093),
  DOI [10.4171/owr/2007/09](https://doi.org/10.4171/owr/2007/09).
  Definitions and theorem context: printed p.541 (PDF page 55).
  Problem 2: printed p.542 (PDF page 56). The displayed page was inspected
  visually. The target consists of both systems; one is not substituted
  for the other, and finite order is not silently assumed.
* Private primary-PDF SHA-256:
  `d38624e71305f8fbd26b92a7903e8d7fb57c22c24763409b1a7126887ba10496`.

## Mathematical dependencies and current literature

1. [Steinmetz, arXiv:1102.3383v1](https://arxiv.org/abs/1102.3383v1),
   subsequently Southeast Asian Bulletin of Mathematics 36 (2012),
   399–417. The privately retrieved PDF was read in §§2–3 and §6.
   It supplies the corrected classical four-value/2CM+2IM background,
   the characteristic estimate used for the order reduction, and the
   periodic rational-in-exponential theorem. The independent audit also
   checked §1, printed p.2, formula (Na), supplying the explicit individual-
   characteristic comparison in the corrected proof; see CORRECTIONS.md.
   These are credited standard
   inputs. Their analytic foundations are not machine-formalized here.
   Private PDF SHA-256:
   `3561b744796a0e2e3c1819d3296049577be41b991bcd985080026c3cc4fcb0bb`.
2. Gundersen, *Meromorphic functions that share four values*,
   [1983 DOI](https://doi.org/10.1090/S0002-9947-1983-0694375-0), and its
   1987 correction, Trans. Amer. Math. Soc. 304, 847–850. The correction
   is explicitly acknowledged by Steinmetz's §2, whose §3 provides a
   separate short proof. We use the corrected theorem as standard
   background, not the uncorrected original proof. Direct publisher
   retrieval was unavailable in this pass.
3. [Li–Zhai–Yi, arXiv:2402.03248v8](https://arxiv.org/abs/2402.03248v8),
   revised 6 January 2026, claims the finite-order 3IM+1CM theorem.
   The actual PDF has 48 pages. The relevant proof, especially §3 and
   printed pp.39–40, was inspected. DEPENDENCY_CHECK.md gives a precise
   canonical test of a failed positivity inference. No conclusion that
   the theorem statement is false is drawn. Its claimed result is not
   used to mark this target solved. Private PDF SHA-256:
   `d25d83eee8f5cb6f3312077a975186603310410d9505d168497f6a7a01d0d607`.
4. [Zhai–Li, 2025 publisher record](https://www.sciopen.com/article/10.16441/j.cnki.hdxb.20240031?issn=1672-5174)
   is a different, restricted finite-order result. Its abstract includes
   a critical-value-size hypothesis; it is not an unconditional closure
   of the target, and no proof from it is imported here.
5. Steinmetz's [2024 five-pair paper](https://arxiv.org/abs/2410.01624)
   concerns four pairs plus a fifth CM pair, not this four-value system.
   The adjacent investigation shared that source distinction. No
   theorem from that different problem is used here.

## Repository and duplicate checks

Live reads used AlecKriebel/Math on its default main branch. The queue
path is `unsolved_math_prioritization/QUEUE.md` (not `research_queue`).
Its GitHub-reported blob at the check was
`c1009ab2e12b93cffb15cb17c0ac893979ce5a44`. The row was rank 607,
`queued`, `0/5`. The live state blob was
`5d61841df2ecf0363dfba1858e568fc79734819f`, with no entry for this ID.
The repository and queue instructions and README were read.

Exact numeric-ID/code searches found no code or PR match; the title PR
search and exact-ID branch search were also empty. The attempt directory
and its README returned 404. The live related-target groups do not list
this ID. Search indexing and differently named work remain limitations.
The neighbouring 30000706 is the separate psi=1 Problem 1: this target
implies its equation, but its converse is not being assumed. Sources and
one dependency warning were shared; there is no independence claim.

No remote write was made by the investigator. The proposed queue
classification is `unsolved`, turns `5/5`, subject to fresh independent
and root verification. No Findings edit, paper, release, DOI, or outreach
is authorized by this artifact. The exact publication action is for the
parent's existing gate to decide.

## Reproducibility and redistribution

The public files contain original deductions, references, and controls.
Primary PDFs, extracts/screenshots, catalogue corpora, raw repository
reads, scratch derivations and private coordination are excluded from
public redistribution. The manifest binds only the intended review
package, not those private research files. Standard mathematical inputs
and the recent-source limitation remain explicit even when controls pass.
