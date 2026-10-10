# Independent audit of equal-pressure foam cell routes

## Verdict and scope

The packet is accepted as a scoped partial analysis, with three presentation clarifications and expanded independent checks. No theorem-level error was found. This is not acceptance of a solution to catalogue problem 5900021. Finiteness of all admissible cell types, occurrence of a tetrahedral cell, occurrence of a dodecahedral cell, and the source's two-faced continuation are unresolved. Five bounded approaches have been exhausted. No new global foam or novelty claim is accepted.

The mathematical conclusions concern sufficiently regular finite simple cells with ball closures, disk faces, interval borders, trivalent cell vertices, and finite Gauss–Bonnet terms. The broad source category is not silently replaced by this narrower category. Cell volume equality, congruence, periodicity, convexity, stability, and global minimizing behavior are not assumed in the original target. Periodicity is introduced only for the separate averaged counting obstruction.

The original five authored files and archive are preserved. The `current` derivative changes only explanatory wording and adds machine-readable scope/status records. No GitHub action or queue change is part of this audit.

## Primary source restoration

Sullivan–Morgan, *Open Problems in Soap Bubble Geometry* (1996), author-version pages 4–5, poses the finite-type question and specifically discusses tetrahedral and dodecahedral cells. The following page records a necessary condition for a two-faced cell: a common boundary for two minimal surfaces making the specified angle along that curve. The note is not itself a construction. These passages were checked in extracted text and rendered pages. The target and neighboring context in the eight-page author version were read; its pagination differs from the journal's 833–842. Author PDF: https://page.math.tu-berlin.de/~sullivan/Papers/foams/soap-prob.pdf . DOI: https://doi.org/10.1142/S0129167X9600044X .

Sullivan, *The Geometry of Bubbles and Foams* (1998), printed pages 388–393, first gives a locally finite geometric definition and then separately restricts to simple cells and faces. The survey also explains edge-curvature cancellation in averages and tetrahedral stellar insertion. This supports the packet's category distinction and its attribution of the topological operation, without supplying geometric realization of the altered complex. Relevant pages were independently read and key pages rendered. Author PDF: https://page.math.tu-berlin.de/~sullivan/Papers/cargese/cargese.pdf . DOI: https://doi.org/10.1007/978-94-015-9157-7_23 .

The two PDFs were fetched again during the audit. Both returned HTTP 200 and PDF bytes; their sizes and SHA-256 hashes exactly match the original manifest. Browser-style web opening failed for these URLs, but ordinary public byte retrieval succeeded; that is a retrieval-tool limitation, not a permissions bypass. Source bytes remain excluded from the deliverable.

Kusner, *The Number of Faces in a Minimal Foam* (1992), was independently inspected through its ResearchGate HTML full-text representation: definitions, Theorem 1, proof, and noncompact qualifications. The page advertises a Royal Society preview. This audit did not independently verify that provenance, did not acquire a publisher copy, and did not inspect a Kusner PDF. OCR equations are imperfect; the needed Euclidean formulas are rederived below. The compact theorem is not a universal noncompact averaging theorem. Source: https://www.researchgate.net/publication/2348802_The_number_of_faces_in_a_minimal_foam . DOI: https://doi.org/10.1098/rspa.1992.0177 .

Publication years refer to the articles, not search-index crawl dates. This audit is not a comprehensive current-literature survey or a certificate that no resolution exists anywhere.

## Geometric verification

### Plateau angles and incidence

Choose the four unit tangent-ray directions obtained by normalizing (1,1,1), (1,−1,−1), (−1,1,−1), and (−1,−1,1). Every distinct pair has inner product −1/3. Hence the face corner angle is α=arccos(−1/3), the exterior turn is θ=π−α=arccos(1/3), and the cell's intrinsic vertex defect is 2π−3α=3θ−π=δ. The defect is positive.

Euler's identity for the spherical disk-face boundary and trivalence give F−E+V=2 and 3V=2E, hence V=2F−4 and E=3F−6. No convexity is needed. These relations and ensuing proofs do not apply automatically to a nonspherical boundary, nondisk face, or circular border without vertices. The independent arithmetic includes F=3 as an incidence-algebra case; this is not an assertion that any such minimal cell exists. The original helper's F≥4 input domain is adequate for its stated tested examples, but is not an additional geometric exclusion theorem.

### Signed facewise Gauss–Bonnet

With η pointing into a face from its boundary, the signed boundary geodesic curvature is κ·η. This convention gives positive curvature on a convex planar disk boundary, and negative curvature on the inner boundary of a planar annulus. The stated sign is therefore correct.

Summing facewise Gauss–Bonnet gives −Q+B+3Vθ=2πF. Substitution of the incidence equations yields −Q+B+Vδ=4π, or B=4π+Q−(2F−4)δ. For a minimal surface with principal curvatures λ and −λ, K=−λ²≤0, so Q≥0.

At a triple border, the three sheet conormals are unit vectors separated by 120 degrees. Their sum is zero. A cell uses two of them, whose vector sum has squared norm 2+2(−1/2)=1. Thus the cell contribution along that edge has absolute value at most |κ|. The integral triangle inequality gives |B|≤T, where each cell edge is counted once. A factor two would be a valid but weaker bound; claiming zero for the pair would be false. Cancellation occurs only when all three adjacent regions are summed, with the appropriate face incidence multiplicity.

The displayed deficits for F=4,12,13,14 and their signs are correct. For F≤13, D_F>0 and T≥D_F+Q. These are lower bounds on required bending; without an independent upper bound they exclude no tetrahedral or dodecahedral realization.

### Straight borders and convexity

If all borders are straight, every edge term on every face is zero. A disk face with m corners then obeys mθ=2π+Q_f≥2π. The rigorous scalar inequality 5θ<2π forces m≥6. But the incidence sum is Σm=2E=6F−12, contradiction. This excludes all-straight borders in the stated category, not just low-face cells.

For a convex cell, the second fundamental form on each smooth boundary face is semidefinite after a consistent choice of normal. Zero mean curvature forces it to vanish. Each connected face is planar, and adjacent distinct planar faces meet along a line. The nonzero Plateau angle rules out coincident planes. The straight-border contradiction applies. A convex combinatorial name alone does not impose geometric convexity.

### Exact local circular junction

For a=√3/2, b=log(√3), and u=z/a−b, r=a cosh u has r′=sinh u and r″=cosh u/a. Therefore rr″−(r′)²=cosh²u−sinh²u=1 for every z. At z=0, e^b=√3 gives r=1 and r′=−1/√3. The derivative's arclength factor is 2/√3. The inward conormals are consequently e_r and −e_r/2±√3e_z/2. The circle has curvature vector −e_r, so its three sheet geodesic curvatures are −1, 1/2, 1/2.

The pair of catenoid sheets bounds the positive local sector; its integrated contribution is 2π. Each remaining pair contributes −π. Their sum is zero, and the positive sector saturates the norm-one edge bound. The third sheet is necessary for the full triple junction. Reflection supplies the sign of the lower vertical component.

Take 0<ε<ab and truncate the plane to 1≤r≤1+ε. The upper catenoid lies at positive z and has radius below one until its waist; the reflected sheet lies at negative z. They have no other common points. Each sheet is embedded, and each has an artificial outer boundary. The patch is not a completed bounded cell. In particular the catenoid annuli do not give two complete minimal disks spanning the unit circle. It does not decide the source's two-faced note or provide a global space-filling foam.

The original prose called the planar sheet a small annulus but wrote r≥1 without an upper cutoff. Adding that harmless cutoff makes its artificial outer boundary explicit. The original displayed catenoid ODE was already true; expanding its identity removes any confusion with the original code's weaker check at just z=0.

### Compact stationary film obstruction

For the specified regular boundaryless film system, minimal interiors contribute no mean-curvature force. Boundary conormals cancel along every triple border; isolated vertices contribute no one-dimensional boundary term. This is stationarity for compactly supported ambient variations. A cutoff vector field equal to x on the compact support has tangent divergence two everywhere on a sheet. Therefore δA=2A, which is incompatible with stationarity for positive finite area.

Compact support and absence of external boundary are essential. The argument does not exclude an infinite locally finite foam, a framed patch, or bubbles whose shared interior pressure differs from exterior pressure. It also does not justify extrapolating a finite local patch to a global partition. This is a classical first-variation proof, not a computational existence test.

### Conditional finite incidence types

The signed identity gives (2F−4)δ=4π+Q−B≤4π+Q+T. A uniform per-cell bound Q+T≤M therefore bounds F, and hence E and V. Bounded finite graph incidence data and cyclic orders admit only finitely many possibilities. Restricting to the required spherical disk-face boundaries gives finitely many combinatorial incidence types. Continuous geometric embeddings need not be finite in number, and are not the claim.

The identity likewise equates a uniform upper bound on F with a uniform upper bound on Q−B in this category. The stronger Q+T condition is sufficient, not established. Scaling sends K to K/s² and area to s² times area, while sending |κ| to |κ|/s and ds to s ds; all integrated quantities are unchanged. Unit size normalization is not a curvature estimate. This proof supplies no compactness, nondegeneration, or uniform cellwise bound.

### Periodic stellar insertion

A dual stellar insertion replaces one tetrahedron by four. It adds one dual vertex and four dual edges. Since dual vertices are cells and every dual edge counts twice in total face incidence, N rises by one and S by eight. Equivalently the new cell has four faces and each of its four neighbors gains one. Repeated identifications in a quotient must be counted by incidence multiplicity. A purported quotient with pathological cell identifications is not thereby a realization satisfying the simple-cell hypotheses.

For the conditional 14-face start, the arithmetic mean is (14N+8t)/(N+t). In a compact flat quotient of a sufficiently regular simple foam, all cell edge contributions cancel in the total, including quotient multiplicities. Summing the signed identity gives average F=2+2π/δ+average Q/(2δ)≥f_*. The inequality used is a correct weak necessary bound. In this regular flat category equality would force every face planar and thus contradict the straight-border argument, so a strict inequality is also available; weakening it to ≥ does not invalidate any obstruction here.

Solving the weak bound gives t/N≤(14−f_*)/(f_*−8). One insertion first passes the arithmetic test at N=9. The exact average there is 13.4, strictly above f_*. For full decoration, the initial cell has 24 corners, and four cells meet at each corner, so t=6N; the mean is 62/7. This fails the bound.

These counts neither construct a nine-cell periodic quotient nor realize its interfaces by minimal surfaces. The statement that an average theorem alone leaves room for a rare low-face cell is correctly limited to numerical compatibility. A sparse defect would still need a complete embedding and Plateau/minimal-surface existence argument.

## Independent computational checks

The original checker was inspected, including its seven negative controls, and its historical JSON output and archive were checked against the listed hashes. It uses explicit exceptions rather than assertions, so optimization does not remove its checks. Its controls test invalid incidence counts, a bad cosine-series input, duplicated or missing conormals, and invalid subdivision inputs; they are not semantic mutants of the mathematical formulas.

The independent checker does not reuse the original arctangent formula or the original theta endpoints. It bounds π using π=4(atan(1/2)+atan(1/3)) and independently brackets arccos(1/3) by rational bisection with Taylor remainder bounds. All decisions use exact fractions. Its deficit intervals are contained in the wider original intervals. Decimal displays are separately checked against their rounding/truncation units.

The catenoid check is an exact Laurent-polynomial identity in t=e^u, so it covers every real u analytically via t>0. Algebra in Q(√3) checks boundary derivatives, speed normalization, conormal angles and signs. Finite incidence and scalar checks verify the first passing count and decoration threshold. These computations support the written proofs; they are not a formal verification of Gauss–Bonnet, first variation, topology, PDE solvability, or global foam realization.

Sixteen semantic mutation modes alter one claim each. Ten alter explicit geometric or arithmetic claims: defect coefficient, Q sign, conormal norm, catenoid scale, circle curvature sign, reflected sheet, ODE sign, stellar increment, threshold count, and decoration multiplicity. The remaining six guard against the disproved local sign shortcut, dropping compactness, claiming an unproved uniform estimate, inferring global realization, erasing simple-cell scope, or resolving the two-faced note. The receipt distinguishes numerical/algebraic rejection from hypothesis/status guards; these are not interchangeable evidence.

The acceptance harness runs original and independent checkers in normal, -O, and -OO modes under actual UID=EUID=1000. It records positive and negative exit statuses, before/after hashes, permission-denial probes, external-output success, internal-output and overwrite rejection, payload tamper detection, and contextual patch roundtrip. The exact successful run counts and output hashes are recorded in `ACCEPTANCE_RECEIPT.json`; that receipt, rather than this procedural description, is the execution evidence.

## Remaining limitations

Read-only Unix permissions are a verified accidental-write barrier for the observed user, not kernel immutability or protection against the owner intentionally changing modes. Hashes prove byte consistency, not truth. Textual claim guards protect stated hypotheses but do not establish analytic theorems. Source hashes identify inspected files but do not grant redistribution rights. The delivery payload therefore contains authored material and public verification metadata only, excluding source bodies and private coordination material.
