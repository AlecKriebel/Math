# Exact source, campaign gate, and scope

Checked 2026-10-01 UTC. This is numeric ID 5100035, AMR-050-0035,
rank 243. The complete pinned statement and prior research report were
read. Their catalog hashes are verified in `TARGET.json`.

## Edition mismatch

- arXiv:2004.12497v11, dated **29 October 2020**, Table 7 p.9:
  k607 is the original-orbit focal **antipedal** signed-area ratio,
  value 1, N divisible by 4. The full table was visually inspected.
- The final *Fifty New Invariants of N-Periodics in the Elliptic Billiard*,
  Arnold Mathematical Journal 7 (2021), 341–355, DOI
  10.1007/s40598-021-00174-y, Table 7 p.349, has no such row.
  Its k607 is a different equality between two **pedal** area ratios.
  The final table and §3.7 were visually inspected.
- The imported prior report's assertion that the two tables contain the
  same k607 target is therefore corrected. The final paper is a source
  comparison, not evidence that the imported antipedal target vanished
  mathematically or was disproved.

ArXiv equation (1), p.3 defines all polygon areas as signed shoelace
areas. Section 3.5, p.6 defines antipedals by consecutive intersections
of perpendicular lines through original vertices. Their self-intersection
is explicitly allowed. The foci are the real foci of the outer ellipse;
the confocal elliptical caustic has the same foci.

## Known input and limitations

Stachel's full published *The geometry of billiards in ellipses and
their Poncelet grids*, J. Geom. 112, article 40 (2021), DOI
10.1007/s00022-021-00606-2, Corollary 4.2(i), pp.22–23, supplies
central inversion for even period and odd turning number. Its preceding
paragraph identifies the gcd/primitive-period distinction. The proof
uses this published theorem, including primitive stars, and does not
claim to establish billiard integrability.

The source itself uses the same symmetry mechanism for neighboring
focal-pedal rows. Extending this elementary equivariance to the actual
antipedal lines proves equality of signed areas. The explicit admissible
8-orbit shows that the raw quotient can be 0/0. It does not refute the
ratio's defined-locus invariance or its removable constant extension.
The proof states both facts prominently. The zero example varies the
ellipse/caustic during its construction; it is not a comparison of
different phases claimed to be in one family.

## Prior-work gate and credit

Before this attempt, exact GitHub PR searches for 5100035/k607 and a
branch search for 5100035 returned no matches; committed path history
for attempts/5100035 was empty. The related-target group file explicitly
groups this row with the central-inversion identities and warns to check
intersections, primitive periods and zero areas independently.

Related campaign PR110 proves k603 (sum of focal-antipedal distances),
PR140 concerns the k405 centroid, and PR210 proves the distinct outer
focal-**pedal product** (arXiv k605,a / final k606). None is used as the
present theorem. The listed 5100024 work folder contains no completed
target proof. No exact prior campaign attempt was identified.

Primary-source literature checks found no exact later theorem quoted as
the arXiv k607 result. This is not a comprehensive novelty guarantee.
The result is credited as an elementary consequence of established
central symmetry, with an exact additional denominator certificate.

Full PDF URLs/hashes are in `source_manifest.json`. PDFs and rendered
reading copies are local source material and are excluded from the
public artifact set.
