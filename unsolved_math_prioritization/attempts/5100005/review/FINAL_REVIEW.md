# Independent source/arithmetic review: 5100005, edition-specific k111

**Verdict: PASS — the imported arXiv-v11 assertion is false as a credited consequence of the prior campaign witness.** No mandatory mathematical/source correction to V2. Recommended queue disposition: `already_solved`, 0/5 new author proof-search turns, with explicit PR147 reuse credit and no additional discovery claim.

## Exact frozen version

Reviewed SOURCE_CONSEQUENCE_V2.md SHA256 `fc2f32c6ad852d753e75334936a444080cdfd0562282d70e16e20592df23969f`. Recomputed all seven hashes in FROZEN_REVIEW_MANIFEST.json; all match. Read the exact imported problem and complete prior report. Their sorted-JSON pair hash `965e3c4beec43b5fec0f0ee150489643e95cd13ffd220154154d501082de4084` matches the catalog. The earlier local draft is historical; this verdict applies to V2.

This reviewer is separate from the packet author. Before freeze I shared the common polarity observation and warned about the table-numbering/product discrepancy while investigating neighboring k110. Accordingly, this is separate verification of a credited known-witness consequence, not a claim of blind independent rediscovery. For the present audit I independently rebuilt caustic contacts by solving the double-root chord equation, rather than using the submitted linear-map construction.

## Source identity and edition audit

The primary tables were inspected visually in full, together with the definitions:

- [arXiv:2004.12497v11](https://arxiv.org/pdf/2004.12497v11), Table2 p.5, k111: A'A'', even N, unproved marker. This is exactly the imported target.
- [Published 2021 companion](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table2 p.345, k111: A'A''/A²=1, odd N. This is a different statement.
- That published table also literally prints A'A'' at k112, for all N, beside the dimensionless value (ab/(alpha beta))². The v11 table's ratio A'/A'' with that value is at k113. V2 records the discrepancy without silently replacing the displayed product or claiming the product expression vanished entirely.

The source convention is signed shoelace area in traversal order; P' uses intersections of consecutive tangents to the outer ellipse, while P'' uses caustic contacts. No focal antipedal, pedal-foot, half-angle or perimeter expression is substituted. I found no basis here to claim an author withdrawal, erratum, intended correction, or refutation of the published odd k111. V2 appropriately makes none of those claims.

## Pinned prior witness and geometric scope

Fetched the full PR147 proof at commit `502de2f863a63ca205814da4194411847797a7c3` using the repository object store. Its SHA256 `d34e4347358f54b20c9cea7d974e2c6a2308a5e69c7abf46de16132d83f9edbd` matches both V2 and the prior independent review. Read the full proof and that review, rather than relying only on PR metadata.

The two ordered orbits are D=((4,0),(0,3),(-4,0),(0,-3)) and R=((16/5,9/5),(-16/5,9/5),(-16/5,-9/5),(16/5,-9/5)). Their outer squared axes are16,9 and caustic squared axes256/25,81/25, with common positive difference144/25<9. Each has four distinct consecutive vertices; direct unit-velocity reflection checks pass. All caustic contacts lie strictly inside the relevant edges. Thus neither an even listed length from odd repetition nor a singular/hyperbolic caustic is involved.

The prior proof also supplies a continuous connecting family. Its normalized circle map is induced by the linear map (c,d)↦(-a²d,b²c). Squaring gives -a²b² times the identity, so normalization gives T²=-Id; its positive determinant preserves orientation. The positive chord determinant and support-square identity in that proof are correct. At (c,d)=(1,0) and (a/s,b/s), s²=a²+b², it gives exactly D and R. Hence they belong to one fixed-caustic oriented family, not merely two caustics with equal numerical parameters.

## Area relation and exact counterexample

For a side n·X=h, h cannot vanish because it is tangent to a strictly nested centered ellipse. The outer pole is T=E n/h, with E=diag(a²,b²). It lies on both endpoint tangents and is their finite intersection. The caustic contact is S=C n/h for C=diag(alpha²,beta²); therefore S=CE^(-1)T. Equality of the cyclic polygons under this fixed linear map gives A''=det(CE^(-1))A', without any division by area. V2's argument is correct.

The independently computed area triples (A,A',A'') are:

- D: (24,48,6912/625)
- R: (576/25,50,288/25)

The multiplier is144/625. Consequently A'A'' is331776/625 on D and576 on R, with positive difference28224/625. Both cases have convex positively oriented derived polygons, so signed versus ordinary-area conventions do not affect the contradiction. The neighboring AA'' equals165888/625 on both, a useful control that the two assigned targets have not been conflated.

## Verification and status disposition

The author's exact standard-library checker was read and replayed without editing the frozen packet. Its complete JSON output equals verification.json byte-for-byte. The separately authored independent_check.py passes101 exact rational assertions, reconstructing each contact as the repeated root of the caustic equation restricted to its chord. It also verifies reflection, tangency, incidence, cyclic/reversal behavior and final unequal products. These checks support the explicit finite witness and are not a new search or universal numerical argument.

`already_solved0/5`, described as **credited campaign consequence / already covered**, is appropriate:

1. The exact imported expression and source edition are identified, so an unresolved source hold is unnecessary.
2. PR147 concerned a different expression, k107. This target is not a literal duplicate of that assertion, although the same reviewed geometry settles it immediately.
3. A prior campaign witness plus a source-recorded elementary relation already provides the negative answer. Repackaging that consequence must not create a second independent discovery or restart the five-turn budget.

Keep the historical OPEN-TRIAGE report as history, retain the V1 correction record, and make V2 the current conclusion. Any public title should say “old/arXiv-v11 k111 product” or equivalently identify A'A'' with even N. No remote write, queue edit, outreach, merge or release was made by this reviewer. Publication remains with the parent/author workflow.
