# Geometric and invariant-region adversarial audit

Problem 9700026 / AMR-096-0026; PR880; supplied original head `fba74a301786f9648e48722e76f440097b0746c2`; supplied queue `claimed_solved2/5`.

Audit completed: 2026-10-15T09:33:57.186909+00:00. Completion estimate: 100% of this geometric/invariant-region family review.

## Decision and scope

**ACCEPT the frozen author's geometric persistence argument without a mathematical repair condition.** For every finite collection of at least two distinct sites in the open unit square, every positive initial probability vector, and every alpha,beta>0 with beta>2alpha, every classical trajectory of the displayed fixed-city ODE exists globally and every coordinate stays uniformly positive. In particular alpha=2,beta=8 rules out any coordinate tending to 1. This refutes the unrestricted alpha>1 alternative in the literal 2007 Conjecture 32(a), including ordinary generic-position interpretations.

This decision concerns the stated geometric/invariant-region mechanism. It is not a current-queue or repository-state verification, a novelty claim, human peer review, formal proof-assistant certification, or a solution of collapse for beta<2alpha, the critical case, convergence/unique positive limits, or the stochastic process with new cities. Those remaining mathematical questions are outside this audit, rather than gaps in this counterexample.

The accepted proof is exactly 5,736 bytes with SHA256 `8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767`. The frozen SOURCE_MANIFEST.json is 9,234 bytes with SHA256 `b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b`. No candidate or frozen-author file was edited.

## Independence and primary-source reconstruction

INDEPENDENT_RECONSTRUCTION.md was written before reading the author proof, its certificate or checker, or inherited reviews. It reconstructs a disk version of the local capture estimate from the actual primary model. Only after this memo existed were PROOF.md and the complete checker read. Inherited audit A and review B were consulted afterward for comparison; their conclusions were not premises of this decision. No discrepancy affecting this mechanism was found.

The actual April 25, 2007 notes permit positive alpha and beta in the global model and display the fixed-city ODE in section 6.4, printed p.40. Its cell is selected by a hard maximum of z_i^alpha times distance^(-beta). The literal collapse hypothesis is an OR, including alpha>1 by itself. The source's general-position qualification is not defined. The 11-page arXiv:1209.5120v1 article instead displays alpha<=1, concerns the stochastic process with city founding, and does not itself state this fixed-city conjecture. These are distinct scopes.

Primary references, read locally as supplied source material: [2007 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf), section 6.4 and global pp.2–5; [2012 paper](https://arxiv.org/abs/1209.5120v1), complete text. No third-party source text is republished in this package.

## Checkable analytic reconstruction

Put q=alpha/beta and p=2q. For positive weights a point away from the sites belongs to S_i exactly when, for every j,

    |y-x_i| <= (z_i/z_j)^q |y-x_j|.

Thus the hard-max cells, their areas and the ODE depend only on alpha/beta. In particular (2,8) and (1/2,2) produce identical vector fields in the same time variable. This ratio observation is a consistency check, not an assumption that either branch of the conjecture holds.

### Partition, positivity and existence

For a pair of distinct sites, the tie equation is

    |y-x_i|^2 - (z_i/z_j)^(2q)|y-x_j|^2 = 0.

It is a nonzero polynomial: a nonunit ratio leaves a nonzero quadratic coefficient, and a unit ratio leaves a nonzero linear coefficient because the sites differ. Its zero set is a line or circle and has planar measure zero. Finitely many ties and sites have measure zero. Therefore 0<=A_i<=1 and sum A_i=1, irrespective of any convention at ties or the infinite influence at a site.

At almost every spatial point a positive state has a unique winner; its strict comparisons persist under sufficiently small weight perturbations. Dominated convergence therefore proves continuity of A_i on the positive orthant. Peano existence applies there. Summing the ODE gives s'=1-s, so s(0)=1 implies s=1. Also z_i'>=-z_i, hence z_i(t)>=exp(-t)z_i(0)>0 on every finite time interval. These facts are established before the stronger persistence estimate, so normalization/positivity are not circular assumptions.

On any finite interval the coordinates are bounded above by 1 and below by exp(-T)z_i(0), and derivatives have absolute value at most 1. A finite maximal endpoint would therefore have a limiting state in the positive orthant, where a new Peano solution could extend it. Thus solutions exist globally. Uniqueness is unnecessary: the following argument applies to every such solution. This audit makes no extra uniqueness claim.

### Capture against every competitor and the domain boundary

Fix city i. Choose h_i>0 such that its full square x_i+[-h_i,h_i]^2 lies in the unit square and

    |x_i-x_j|^2 >= 8h_i^2     for every j != i.

Finitely many distinct interior sites permit this. For any positive probability vector define Q_i=x_i+[-h_i z_i^q,h_i z_i^q]^2. It lies in the actual domain because z_i<=1. Every y in Q_i satisfies

    |y-x_i| <= sqrt(2)h_i z_i^q,
    |y-x_j| >= |x_i-x_j|-|y-x_i|
              >= 2sqrt(2)h_i-sqrt(2)h_i z_i^q
              >= sqrt(2)h_i.

Consequently |y-x_i| <= z_i^q |y-x_j| <= (z_i/z_j)^q |y-x_j| for every j, using z_j<=1. This is a simultaneous all-competitor argument, including whichever rival is dominant. It is not a nearest-cell approximation. Hence Q_i is won by i except for irrelevant null conventions and

    A_i(z) >= 4h_i^2 z_i^(2q) = K_i z_i^p,   K_i=4h_i^2>0.

There is no unaccounted boundary loss, factor of pi, soft allocation, symmetry, fixed-point assumption, numerical area integration, or hidden time change.

The independently reconstructed disk proof gives the same exponent: with c_i no greater than the boundary clearance or half every intersite distance, the open disk of radius c_i z_i^q is strictly won by i and has area pi c_i^2 z_i^p. The square proof's rational constants are sufficient and correct; it does not require the optimal capture constant.

### All-time invariant bounds

When beta>2alpha, 0<p<1. From z_i'>=K_i z_i^p-z_i and positive z_i, set u_i=z_i^(1-p). The chain rule and a positive multiplier give

    u_i' >= (1-p)(K_i-u_i).

Integrating an exponential factor gives, in the actual displayed ODE time,

    z_i(t) >= [K_i+(z_i(0)^(1-p)-K_i)exp(-(1-p)t)]^(1/(1-p)).

The bracket is a convex combination of positive K_i and positive z_i(0)^(1-p), including when the initial weight is below the limiting threshold. Therefore

    z_i(t) >= eta_i := min(z_i(0), K_i^(1/(1-p))) > 0,
    liminf z_i(t) >= K_i^(1/(1-p)) > 0.

Every coordinate's barrier follows using only normalization, not another coordinate's barrier, so simultaneous first-crossing reasoning has no circularity. Equivalently, at any lower boundary strictly below K_i^(1/(1-p)) the derivative points upward. Summing the already obtained bounds gives z_i(t)<=1-sum_(j!=i)eta_j<1 for every i. No coordinate can tend to 1. These are time-uniform analytic statements, rather than finite simulations; they do not assert convergence.

## Exact asymmetric certificate

Independent rational arithmetic from certificate.json gives q=1/4, p=1/2, h=1/16, K=1/64 and K^(1/(1-p))=1/4096. The three initial weights (1/6,1/3,1/2) exceed that threshold and sum to 1. The squared site distances are 557/1800, 137/400 and 49/144; the respective excesses over 8h^2=1/32 are 2003/7200, 249/800 and 89/288. The minimum site boundary clearance minus h is 11/80. All margins are strict. The signed triangle determinant is 343/1200, and the three distances differ, so the illustration is noncollinear and scalene with unequal initial weights.

Thus, for every t>=0 and every coordinate of this actual ODE,

    1/4096 <= z_i(t) <= 1-2/4096 = 2047/2048.

The theorem covers every distinct interior configuration and every positive probability vector, for every fixed finite m>=2. Strict geometric margins are stable under perturbation; alpha>1,beta>2alpha is an open parameter region. Usual genericity exclusions of symmetric or lower-dimensional exceptional sets cannot remove this open family. No formal definition of general position is invented. The exact same numerical bound is not asserted under arbitrary parameter changes.

## Falsification attempts and finite evidence

The independent exact_geometric_stress.py imports no author code. An isolated execution passed 34,000 exact hard-max influence comparisons across q=1/3,1/4,2/5,3/7,1/25. Its rational states include very small target weights and highly unequal competitors; its geometries include equality in the separation condition, capture-square contact with the domain boundary, nearly coincident but distinct sites, the asymmetric witness, and eight competing cities. Each tested capture square uses 25 rational points. Ten exact exponent identities support the scalar transformation.

The script also supplies controls with actual losing capture points when normalization is omitted, h is enlarged beyond the separation hypothesis, or a third competitor is ignored. Separate exact scalar controls show the downward lower-bound derivative possible at p=1 and p=2; the proof cannot cross the beta=2alpha boundary. The p=1/2 comparison has the right derivative signs below, at and above K^2, and remains valid for a positive starting weight below K^2.

The unchanged author's checker replay passed the certificate under isolated Python and its self-test under isolated optimized Python. Its 216 exact influence comparisons, four comparison coefficient identities, sixteen rejected invalid-input controls and two accepted positive controls are recorded separately. The code's specialized q=1/4 scope is stated correctly and does not prove the general theorem on its own.

These computations are finite stress evidence only. The continuum geometric inclusion, existence, every-time bounds, and asymptotic noncollapse are proved by the analytic reasoning above. No numerical trajectory or sample grid is treated as their proof.

## Boundary cases and exact remaining gap

- beta=2alpha makes 1-p=0; the transformation and sublinear barrier do not apply. beta<2alpha likewise receives no persistence conclusion here.
- Zero starting weights and coincident sites are excluded. At zero weight the positive comparison substitution fails; coincident equal sites can create positive-area ties and invalidate the partition argument as written.
- Boundary sites are not needed for this counterexample. The theorem explicitly treats the open interior subset allowed by the source and enough for general-position refutation.
- m=1 is excluded and would trivially have z_1=1. Every fixed finite m>=2 is covered, including arbitrarily close but distinct sites; the constants can become small without becoming zero.
- Neither local Lipschitz regularity nor unique trajectories need be supplied to repair the proof. Every Peano trajectory obeys the same contradiction to collapse.

Strongest verified result: the exact frozen theorem and rational witness refute the literal unrestricted alpha>1 collapse clause. **Remaining gap in this geometric mechanism: none found.** Remaining classifications of critical/restricted collapse, convergence, uniqueness of a positive limit, and stochastic city founding are outside the result. Public material is restricted by PUBLIC_ALLOWLIST.json; local primary PDFs, extracts, inherited corpora, and private outputs are excluded.
