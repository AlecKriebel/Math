# PR211 / 5100063 geometry and algebra adversarial audit

**Local verdict: independently verified in the stated strict elliptical-caustic scope.** No counterexample, false local identity, hidden real inversion singularity, or unresolved local geometric/algebraic gap was found in (3)--(15). This report does not promote the overall candidate or certify the independent global meromorphic audit, priority, or publication status.

## Exact claim and strongest verified result

For 0<k<1, alpha>0, beta=alpha sqrt(1-k^2), c=alpha k, 0<v<K(k), and a=alpha dn(v)/cn(v), b=beta/cn(v), the actual intersections of tangents to E at P(u-v),P(u+v) are exactly the submitted Q(u). They are finite for every real u, lie outside E, and cannot equal either original focus. The exact squared-distance factorization (5), denominator products (9)--(10), translated determinant (11), inverse-edge formula (8) with q^4, and triple-angle formulas (12)--(14) all follow from the full derivations in INDEPENDENT_DERIVATION.md. Every real translated inverse edge determinant in (8) is strictly positive by exact inequalities, so its cyclic shoelace sum is positive.

For v=2K tau/N, gcd(tau,N)=1, 0<tau<N/2, the argument includes every primitive star turning number. It uses the original foci even if the outer locus's major axis is vertical. It excludes changing primitive parity by repeating an orbit. Unit inversion and straight joining give the source's signed shoelace area. Reversal changes both signed areas' signs. Original-geometry scaling by lambda gives each inverse area scale lambda^-2 and the product scale lambda^-4.

The N=3 merged triple-angle zero is independently checked in CRITICAL_CASE_NOTE.md: 3v=2K, L0=Z,L1=-Z, and the double zero of 1-k sn(u) at K+iK' is canceled by exactly one simple numerator zero dn(u), leaving a nonzero simple pole. This local calculation does not assume anything about the eventual cyclic divisor.

## Source and independence controls

The complete submitted PROOF.md and source_record.json were read first. Relevant primary content was read from the already supplied shared copies; no duplicate full-source copy was made. Primary PDF hashes were independently checked and match the parent's specified values:

- invariants_v11.pdf: c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da.
- invariants_final.pdf: c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42.
- stachel_published.pdf: 9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8.

Stachel's full relevant Theorem 4.3 proof and equation (4.9), printed p.1614, were read along with the preceding canonical-flow construction. PDF pp.12--14 were rendered and visually inspected. Its modulus equals caustic eccentricity c/alpha; mpmath instead expects the squared parameter k^2. The theorem explicitly admits coprime turning number tau; only separate Corollary 4.5 assumes tau=1. The coordinate and tangent-incidence formulas were independently reconstructed rather than inferred from a source label.

**Source slip:** printed p.1613 really contains the false auxiliary line dn(u+2jK)=(-1)^j dn(u). The correct dn real period is 2K. The candidate uses the correct period and does not depend on this slip. This warrants a source-reading note, not rejection of the independently checked canonical formulas.

The v11 signed-area definition on printed p.3 and Section 3.9/figures/Table 10 on pp.9--12 match the submitted target. In particular k904,a is the odd-period product of the two outer inverse areas, and k906 uses different foci of the outer locus. Relevant PDF pages were also visually inspected. The published Fifty New Invariants text has an 800-series inversive section and no 900-series target table; the candidate correctly distinguishes it from v11. These are target-identification checks, not a bounded literature or priority search.

The independent derivation was frozen at 2026-10-15 10:21:22 UTC, SHA256 1fb69feb99325781c8853833dbed1c922d784903c968fd888a14f5a228da4f1e. No inherited reviewer verdict, checker implementation, or inherited checker output was consulted at any point. No proof from PR200, PR206, or PR207 was read or used. The controls were independently authored from the frozen derivation. No individual was contacted and no external outreach was prepared. All writes stayed in this shard.

## Checkable exact and numerical controls

`controls.py` runs under the designated existing runtime (Python 3.14.6, Sympy 1.14.0, mpmath 1.3.0), without dependency installation or writes. Its exact controls reduce nine independent polynomial residuals to zero, including the confocal relation, sine-product identity, all focal-distance coefficients, denominator linear coefficient, two triple-angle numerators, and triple norm identity. It also checks a nontrivial rational Jacobi datum

    k=25/39, sn(v)=3/5, cn(v)=4/5, dn(v)=12/13,

by direct tangent incidence, actual inverse determinant, and (8). The exact edge is 1521 sqrt(14)/39500. Geometry scaling by 1/7 and 7 is checked exactly. This is a concrete reproducibility control in addition to the universal algebraic derivation.

The 100-digit direct-geometry diagnostics use actual tangent-line intersections and actual Euclidean inversions. They passed 96 local corner cases, including k^2 near 0 and 1 and v/K near 0 and 1; 70 primitive closed families for N=3,5,7,9,11; 280 phases; 40 families with reversed outer-axis ordering; orientation reversal; and direct-geometry product scaling by lambda^-4. The worst normalized discrepancy was 4.7813e-62, from focal-distance cancellation at an extreme corner. The numerical product discrepancy was below 3.771e-88 under the normalization max(1,abs(a),abs(b)). These are unvalidated numerical support only, not interval enclosures or a universal constancy proof. Small products can make this normalization effectively absolute; the exact derivations carry the mathematical conclusion.

Safe summary results are in CONTROL_SUMMARY.json. Detailed diagnostic rows and rendered primary pages remain under private/ and are excluded from the authored manifest. Reproduce from the repository root with the designated runtime invoking this shard's controls.py. It reads no submitted checker and regenerates only this shard's summary/private diagnostic rows.

## Exact remaining gap and disposition

There is no remaining gap in this shard's real geometry or identities (3)--(15) under the stated assumptions. The universal *product constancy* still requires the separate global audit of complex periods, complete fibers, pole orders, cyclic Laurent cancellation, quotient lattice, zeros/divisor, and the opposite-focus shift. This report neither assumes that audit's conclusions nor substitutes finite sampling for it. Parent retains overall verdict, promotion, and priority authority. Overall goal remains active and incomplete pending its other required work.

Authored artifact integrity is recorded by relative path, byte size, and SHA256 in AUTHORED_MANIFEST.json. It deliberately excludes primary-source payloads, private rendered pages, copied checker code (none was copied), and detailed numerical rows.
