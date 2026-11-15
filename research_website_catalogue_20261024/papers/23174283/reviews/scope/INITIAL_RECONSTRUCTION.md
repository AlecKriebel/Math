# Independent initial scope reconstruction: record23174283

UTC: 2026-11-15T00:51:49.892176+00:00. Completion estimate:18% of this source/scope review. No verdict.

## Early independence and source custody
I personally read all3actualPDFpages, all200lines/8,651bytes of controlling TeX, and viewed all3rendered page images individually BEFORE any foreign primary body, supplied code/results, old triage, archived/current review or sibling/root scientific opinion. SOURCE_READY.json SHA-256:b9f69bfea594378f8cd69a00d214ce14c894fd33e850047a915327432d96ae20. Actual publishedPDF SHA-256:d708af8be2f035af994bca24166a19c0c8ee1d4ea405ca213fe032ef55e9e8ee (61,391bytes). ControllingTeX SHA-256:56a9eb3d76574d8521589988d6f1024be7653f524a450f9745104cf60a6f8553. All physically checked. Prior110/112/113 packets remain immutable and no113science is being released.

## Exact mathematical claim, assumptions and quantifiers
Define Fibonacci F0=0,F1=F2=1 and Fn+1=Fn+Fn-1. For EVERY integer n>=3, put q=Fn,p=Fn-1 and use EXACTLY q points indexed0<=k<q on the UNIT sphere:
 z_k=(2sqrt[(k/q)(1-k/q)]cos(2pi pk/q),
      2sqrt[(k/q)(1-k/q)]sin(2pi pk/q),1-2k/q).
Theorem1 asserts minimum AMBIENT EUCLIDEAN CHORD exactly2/sqrt(q), with UNIQUE minimizing unordered pair{z0,z1}. It is a finite exact theorem for every Fibonacci cardinality, not just an asymptotic lower bound or infinitely many n. The corresponding geodesic minimum is2arcsin(1/sqrt(q)). The singleton n=2 is excluded. No claim for arbitrary cardinalities, midpoint latitude shifts, irrational golden-angle longitudes, arbitrary Fibonacci naming conventions, discrepancy, or optimal sphere packing.

The proof is self-contained after recurrence/elementary sine facts. Lemma2 claims for every n>=3, EVERY integer1<=m<q, and EVERY integer ell,
 m|mp-ell q|>=q/3.
Choose unique j>=2 with Fj<=m<Fj+1 (duplicatedF1=F2does not affect this range), h=n-j>=1. Expand(m,ell) in the unimodular adjacent-Fibonacci basis, with integer S,T. S cannot vanish. Either T=0,S>0 or S,T have opposite signs. The alternating determinant errors give|mp-ell q|=|S Fh-T Fh-1|>=Fh, including h=1. Then Fn=FjFh+1+Fj-1Fh<=3FjFh<=3m|mp-ell q|. This universal lemma is weaker than the separately credited exact hyperbolic-cross index Fn-2.

Lemma3 concerns ALL latitude parameters0<=a<b<=1 and longitude cosine c in[-1,1), with d=b-a. SetU=2(a+b-2ab),V=4sqrt[a(1-a)b(1-b)]. Claimed identities: D²=2(U-cV), U-2d=4a(1-b)>=0, V²=U²-4d². For c<=0, D²>=4d. For0<c<1, positivity and[(U-cV)²-4d²(1-c²)]=(V-cU)² giveD²>=4d sqrt(1-c²). The equal-area map is NOT assumed to preserve planar distances.

For i<j, m=j-i,d=m/q, choose least absolute nonzero residue r=mp-ell q with|r|<=q/2; consecutiveFibonacci coprimality ensures r!=0. Ifc=cos(2pi r/q)<=0, D²>=4m/q>=4/q. Otherwise0<|r|<q/4 and sin(2pi|r|/q)>=4|r|/q, givingD²>=16/(3q)>4/q. Pole pair hasD²=4/q. Equality forcesm=1,U=2d, and becauseb=j/q<1, a=0; hence ONLY{i,j}={0,1}. This includesq=2,3,5, not sampled exceptions.

## Source-interface and historical claims
The manuscript identifies its exact formula/range and pole upper bound with Brauchart's2012Oberwolfach contribution, especially printedp2438, while acknowledging a following set-notation endpoint shift there. A range1<=k<=q is claimed ISOMETRIC via k->q-k and(x,y,z)->(x,-y,-z). Including BOTH endpoints instead makes q+1 points; this must not be conflated with the q-point theorem or uniqueness statement.

ABD Section5.2 allegedly reverses the planar-coordinate order. The manuscript claims the resulting UNORDERED spherical set is isometric after reindexing k=pj modq and usingp²=(-1)^n modq; oddn also needs reflection of the second spherical coordinate. This is a source-specific exact congruence/isometry claim and must be verified, rather than treating all constructions called spherical Fibonacci as equivalent.

The dual lattice{(h1,h2)inZ²:h1+p h2=0 modq} is credited with exact hyperbolic-cross index min_nonzero max(1,|h1|)max(1,|h2|)=Fn-2, to Zaremba1970p186 and SCN2015Theorem2.2. For(-r,m), both factors nonzero, this givesm|r|>=Fn-2>=q/3. The proof does not depend on the stronger index assertion, but its attribution and exact convention remain claims of the published paper.

Novelty scope: construction, pole upper bound and arithmetic estimate are prior work; contribution is claimed to be the all-pair spherical lower bound/exact resolution of the precisely stated report conjecture. The paper expressly disclaims worldwide firstness and current openness, and retains an unverified Brauchart-Dick in-preparation lead and some final graphics editions. These limits must remain public-facing if the paper passes. Versionmetadata says1.0, initialpublication5Oct2026, recordupdated10Oct2026; actual reviewed source/publication objects and any differently indexed primary versions must be identified exactly.

## Independent source/scope validation families

A. Actual conjecture and coordinate conventions. Acquire/read Brauchart's COMPLETE relevant contribution, definition of Lambert/equal-area map, the stated separation conjecture and pole witness atp2438, including exact point range, metric, sphere radius, indexing and endpoint mismatch. A statement for an asymptotic, shifted or irrational construction cannot be substituted. Preserve a precise formula dictionary and source page locations. If the target does not answer the actual published claim under an exact isometry, document the gap rather than promote a repaired variant.

B. Arithmetic primary interface. Inspect Zaremba's exact Fibonacci-index definition and SCNTheorem2.2 in native primary bodies. Distinguish primal/dual lattice, product|h1h2|versusmax-factors, coordinate transpose, modular sign, initialFibonacci indices, exceptional smalln, and exactminimum versus lowerbound/asymptotic. Independently check the elementary all-ell proof, terminalh=1, S/Tzero cases, sign identities andq/3constant. A misquoted optional index theorem is still a source defect even if the weaker proof survives; label its affected claim exactly.

C. ABD and isometries. Read actual Section5.2 and relevant definitions/theorems in the stated version. Derive the map from planar coordinates through Lambert to the target formulas, including the required modular inversep^(-1)=(-1)^n p. Check parity, k=0/endpoint, reversedcoordinate order and scalar sphere normalization. Compare labelledpairs versus unorderedsets and uniqueness under reindexing. Direct exact algebra, not rough visual similarity, must support the convention equivalence.

D. Whole exact proof cross-check. Independently derive U,V identities and the two c-sign bounds, verify positive-sine range/c=0/c=1exclusion, smallq and uniqueequalitylogic, and distinguish chord/geodesic metrics. Use a small read-only verifier for exact integer/Fibonacci/congruence identities and rational algebraic certificates. Full theorem cannot be established by floating nearest-neighbor samples or a large enumeration.

E. Primary literature/priority bounds. Focused search for prior EXACT separation resolution of this rational unshifted Fibonacci configuration, including the actual closest sphere/Fibonacci graphics and lattice papers and the Brauchart-Dick lead. Distinguish approximate golden-angle/shifted/optimizedcardinality results and discrepancy/cubature/inverse-map papers. Credit whatever is already known. Failed searches do not prove novelty; do not assert human recognition, currentopenness, or worldwidepriority. If an authenticated earlier exact theorem matches, record it precisely; do not initiate outreach or prepare any.

F. Deposited code/certificates and native versions. After this seal inspect all5supplied programs, declared dependencies, package manifest and finite results/certificates. Determine whether chord checks are certified rational intervals or merely floating point, what cardinalities/ranges actually run, whether every finite assertion remains guarded, and whether coordinate/control variants are tested correctly. Reproduce only meaningful bounded checks and retain analytic universality separately. All13originalZIPpayloads, actualPDF and controllingTeX are immutable. No archived/currentreview findings or oldtriage opinions will substitute for this work.

## Success criteria and gate
Pass requires the FULL exact published claim, including uniqueness and source convention equivalences, supported by checkable proof and primary interfaces. A substantive gap/counterexample means precise evidence and stop repair; no weaker substitute or silently narrowed promotion. Keep all114science local until root114initialgate; only rawidentity/earlyseal/primarylocators/readiness notices before then. No source/site/core/configs/Sheet/Git/outreach/releases. This lane is source/scope, with independent mathematical scrutiny to validate the interfaces.
