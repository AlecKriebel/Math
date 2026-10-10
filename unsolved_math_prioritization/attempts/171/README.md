# Rotation-only pyjama coverings: an elementary lower bound

Problem 171 / GREEN-083, rank 1260. Original source: Ben Green, *100 open problems*, Problem 41, printed/PDF page 21. Accepted partial quantitative result, substantive attempt 1 of 5.

## Established results

For a unit normal u, let P_u(epsilon) be the points x in R² satisfying dist(u·x,Z) <= epsilon. Let N(epsilon) be the least number of these sets covering every point of the entire plane. All rotations are about the origin, strips are closed, and no translation or dilation is allowed.

The [complete mathematical report](MATHEMATICAL_REPORT.md) and [independent mathematical audit](MATHEMATICAL_AUDIT.md) establish, for 0 < epsilon < 1/2,

\[
N(\varepsilon)\geq
\left\lceil\max\left\{
\frac{\pi}{2\arcsin(\varepsilon/(1-\varepsilon))},
1+\frac1{2\varepsilon}\right\}\right\rceil,
\qquad
\liminf_{\varepsilon\downarrow0}\varepsilon N(\varepsilon)\geq\frac\pi2.
\]

The first-circle obstruction excludes every noncentral strip on circles with epsilon < r < 1-epsilon. Angular measure and the limiting radius give the arcsine bound. The separate second-moment argument uses only single-strip and pairwise periodicity, with no common lattice assumption.

The full proof and audit retain:

- The exact largest-angular-gap criterion for central-strip coverage of the radius-(1-epsilon) disk, including equality and equally spaced sharpness for that disk
- The complementary bound 1+1/(2epsilon), its lattice averaging justification, and exclusion of the epsilon=1/2 endpoint from that argument
- The credited equality N(epsilon)=3 for 1/3 <= epsilon < 1/2, N(epsilon)=1 for epsilon >= 1/2, and N(epsilon)>=4 for 0 < epsilon < 1/3
- Source hypotheses, the closed/open-strip transfer, and the distinction between rotation-only and rotation-plus-dilation problems

The audit required no mathematical correction. The edition applies its two optional clarifications: explicitly state 0<epsilon<1/2 in Proposition 2 and “bounded measurable function” in the averaging lemma.

## Remaining gap and credit

The first-circle bound improves the explicit cited volume lower bound 1/(2epsilon) by an asymptotic multiplicative factor pi. Both have order epsilon^(-1). This does not determine the asymptotic order of N(epsilon), prove epsilon N(epsilon) tends to infinity, or give a polynomial upper bound. Sharpness for the central disk is not a whole-plane construction.

Manners supplies the credited finite-existence theorem. Kravitz–Leng supply the prior triple-exponential upper bound for 0<epsilon<1/10. Malikiosis–Matolcsi–Ruzsa supply the equilateral construction, and Malikiosis's roots-of-unity theorem excludes equally spaced whole-plane covers below width 1/3. Those long source proofs were not independently audited here. Public citations and exact recorded source limits are in [SOURCE_METADATA.json](SOURCE_METADATA.json).

## Review and distribution

This AI-assisted, unrefereed proof-and-audit edition makes no historical novelty, priority, current-openness, external human peer-review, journal-acceptance or formal proof-assistant certification claim. Scoped acceptance rests on the complete written mathematics. Edition preparation claims no fresh scholarly retrieval, PDF rehash, source inspection or literature search.

[STATUS.json](STATUS.json) records partial attempt 1/5. [MANIFEST.json](MANIFEST.json) lists exactly six distributed files and hashes the other five; the pull-request body independently pins the manifest. These identities establish packaging integrity, not mathematical correctness.

Programs, checker outputs, computational results, fixtures, datasets, copied third-party source bodies and private coordination material are excluded. No excluded computation is rewritten as prose. The addition-only edition leaves QUEUE.md and unrelated entries unchanged, adds no substantive proof turn, and does not reset attempt accounting.
