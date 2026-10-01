# Source and scope audit

Checked 2026-09-30. Target 7000019 / AMR-069-0019.

## Exact formulation

The pinned dataset reproduces Ghomi's 2019 Problem 4.3, printed p. 12.
The complete relevant section and introductory conventions were read.
The question uses one fixed positive width, smaller than the extrinsic
diameter. The source's surrounding section concerns convex surfaces.
Ghomi's own 2017 formulation explicitly defines the surface as the
boundary of a compact convex set with interior points:
https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere

This matters. The short extracted phrase “closed surface” alone can be
read to include disconnected surfaces, where nested spheres supply a
counterexample. That scope loophole is documented but is not counted as
solving the convex source target. The 2017 question currently displays
no answer; a bounded search found no later full resolution, which does
not certify that the problem is still open worldwide.

## Related results are stronger hypotheses, not solutions here

Kim–Kim's *Some characterizations of spheres and elliptic paraboloids II*,
arXiv:1208.5361, pp. 1–4, was checked. Its cap-area properties concern all
sufficiently small heights and imply spherical rigidity through curvature.
Those hypotheses cannot be obtained by sending the one fixed h to zero.
The paper explicitly recounts the earlier 2012 result in Proposition 2.
https://arxiv.org/abs/1208.5361

Ghomi's related plank-measure question remains a separate formulation:
https://mathoverflow.net/questions/283370/plank-invariant-measures-on-convex-bodies
It concerns measures on planar convex bodies. Replacing surface area by
an arbitrary measure would change the target and creates additional
support and positivity issues. No such replacement is made in the proof.

The discussion of the all-width question at
https://math.stackexchange.com/questions/449772/does-this-interesting-property-characterize-a-sphere
was used only as a bibliographic lead to Kim–Kim and to separate the
quantifiers. Its easy all-width centroid argument is not a fixed-width
proof and is not relied on as a theorem here.

## Exact external theorem used in the partial result

Reichel, Z. Anal. Anwend. 15 (1996), 619–635, Section 2, printed p. 622,
was read and visually checked. It states that a bounded C^{2,alpha}
domain with connected exterior can carry a constant positive equilibrium
surface-charge density only if it is a ball. The kernel is 1/(4πr) in
three dimensions. Our unnormalized kernel differs by a constant only.
https://doi.org/10.4171/ZAA/719
https://ems.press/content/serial-article-files/34877

The candidate proves exactly the potential-constancy hypothesis when
h is strictly smaller than twice the inradius. It does not assert the
additional inradius inequality from the source assumptions, or remove
the source theorem's boundary regularity.

## Prior-attempt and provenance gate

Repository path, code/ID and subject PR searches across all states,
branch search, shortlist and queue row, and related-target groups were
checked. No earlier research attempt was found. The initial queue row
was rank 48, queued, 0/5. The imported prior report is preserved unchanged
in prior_report.json. Its broad references to section rigidity do not
certify the fixed-width surface-area conclusion.

The source datasets are pinned at revision
37e53eabe540fb458758e198be61634bd02ee008. Downloaded primary PDF hashes
are recorded in source_provenance.json. PDFs are not redistributed.
The search is bounded and does not establish novelty of the partial
averaging consequence or definitive global open status.

## Current superseding qualifications


The exact intended source is the convex positive one-fixed-width question. Fresh source bytes agree with all three original PDF provenance entries. Ghomi2019 Problem4.3 p12 is abbreviated; his2017 MathOverflow body explicitly defines a convex surface and0<h<diameter. Ghomi2004 Problem22 p5 already records the question (last revised21October2004), SHA94f4e39e69c9f320bcc081cdd172dba3b4caab07a766da00ad415fc9899e3320. This establishes occurrence by2004, not earliest proposal. Preserve raw proposed_year2019 as a source-list field.

The imported prior report is historical desk triage, not a verified section-rigidity or fixed-height theorem: a sphere's planar cross-sectional disk area varies with offset while its surface slab area does not. Its broad literature descriptions cannot close this target or certify novelty. Kim–Kim1208.5361 concerns all sufficiently small varying heights and takes t→0; a single fixedh cannot supply that hypothesis. Reichel's exact constant-density, bounded C²,alpha connected-exterior theorem is verified with its full relevant proof and matches the restricted claim. No additional source is used to broaden it.

Historical model/effort, query absence, independent-execution and old pre-header acd8d7... claims remain documentary attestations; current replay does not independently authenticate them. The exact final original proof147b64bc267744e83ede73f7e89200c21931585f91e3e639cf0efc7bd7de5e46 is recovered from Git and fully reviewed. Original files, old review and its header-only claim are preserved; the unrecovered earlier proof is not needed for acceptance.

Raw cached source/prior and read-only SQLite match pinned revision37e53eabe540fb458758e198be61634bd02ee008; prior joins uniquely byAMR-069-0019, not numericID. Current all-state searches and adjacent literature are bounded observations, not authenticated old queries or worldwide absence. Extensive AI tools were used; this current audit is unrefereed and asserts no humanpeer review/proof-assistant certificate. Full target remains unresolved by this package; novelty is unclaimed.
