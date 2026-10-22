# Source, prior-work and domain audit

Checked 2026-10-01 UTC. Numeric ID 5100038, AMR-050-0038, rank 246.
The complete pinned statement and prior report were read. Their
catalog hashes are verified in `TARGET.json`.

## Exact edition and objects

The relevant row is **arXiv:2004.12497v11, 29 October 2020, Table 7
p.9, k610**: focal antipedal signed-area ratio of the inner polygon,
value 1, even N. The table was visually inspected in this source series.
Appendix A, Table 12 explicitly distinguishes original, outer and inner
pedal and antipedal vertices. The inner vertices are caustic contacts;
their antipedal lines pass through those contacts, perpendicular to the
corresponding focal rays. They are not pedal projections onto inner
chords. Source equation (1) specifies signed shoelace area.

The final *Fifty New Invariants*, Arnold Math. J. 7 (2021), 341–355,
DOI 10.1007/s40598-021-00174-y, Table 7 p.349 ends at k607 and has
no k610 row. The imported prior report's assertion of a matching final
table is corrected. The final companion is used only for edition
comparison, not as a replacement theorem or evidence of disproof.

The full published Stachel paper *The geometry of billiards in ellipses
and their Poncelet grids*, J. Geom. 112, article 40 (2021), DOI
10.1007/s00022-021-00606-2, Corollary 4.2(i), pp.22–23, supplies
central inversion for primitive even elliptical-caustic billiards.
Its primitive/turning-number convention and hyperbolic-caustic distinction
were checked. The proof credits this theorem and the source authors'
neighboring focal-pedal symmetry arguments.

## Campaign gate and shared credit

Exact 5100038/k610 PR searches and branch search returned no matches.
Committed main history under attempts/5100038 was empty; available local
all-ref commit-title search was empty. QUEUE row 246 was queued, 0/5.
The related-target group flags this as part of the central-inversion
family and requires independent construction and domain checks.

Related campaign k607 and k609 use the same classical mechanism for
different derived polygons. Their reuse is disclosed rather than
counted as multiple discoveries of central symmetry. The present exact
axis-diamond certificates concern inner antipedals and do not follow
by copying an original-antipedal or inner-pedal denominator conclusion.

Current primary-source searches did not identify an exact published
k610 proof. This is a credited elementary symmetry consequence, not a
novelty guarantee or a new integrability theorem.

## Essential domain distinctions

The full result is equality of the rational signed areas on their
common finite-intersection locus and quotient 1 when nonzero. There
are two different exact convex four-periodic exceptions:

1. At aspect square 2, all antipedal vertices exist uniquely, but each
   focal antipedal collapses to the opposite focus. Both areas are zero
2. At the golden-ratio aspect square, a required consecutive pair of
   antipedal lines is parallel and distinct. A vertex, and thus the
   finite area expression, is undefined

Neither is a counterexample to a defined rational invariant. No raw
0/0 or infinite polygon is silently assigned an ordinary area. The
constant simplified quotient can be continued algebraically, while
the geometric exclusions remain explicit. These examples vary the
ellipse/caustic during their construction; they do not purport to show
phase variation of a defined quotient in one family.

Full PDF access was used for the relevant primary definitions and
theorem/proof passages. URLs and hashes are in `source_manifest.json`.
PDFs and images are local reading copies, not public packet files.
