# Independent review B of city ODE persistence

Problem 9700026, AMR-096-0026, rank 934. Review date: 6 October 2026.

## Decision

ACCEPT the exact pinned author bundle for a full negative answer to the literal 2007 Conjecture 32(a), and consequently to the catalog's conjunction containing that assertion. For every finite collection of at least two distinct interior sites, every positive initial probability vector, and beta > 2 alpha > 0, every city weight remains uniformly positive. Thus alpha > 1 by itself cannot imply convergence of one weight to 1. The explicit alpha=2, beta=8 example is valid, and the argument covers an open family rather than an exceptional symmetric equilibrium.

This is a mathematical refutation of the literal universal statement. It is not a classification of the remaining dynamics, a proof or refutation of the beta < 2 alpha restriction, a resolution of the positive-limit uniqueness/convergence clause, or a refutation of the later stochastic model. Calling the result merely a numerical example or a formulation suspicion would understate the proof. Calling the entire intended stability problem solved without these qualifications would overstate it.

The review was performed independently from the other auditor's conclusions. No author-file changes were required. This is an AI-assisted mathematical/source review, not human peer review, formal proof-assistant certification, or a novelty claim.

## Exact material accepted

- Author ZIP: CITY_STABILITY_9700026_AUTHOR_SAFE_FREEZE.zip; 11844 bytes; SHA-256 adc58ab6c2b52963f303582261ee603470dbf2728eee8b4546c04ba7cf9b201d.
- External author manifest: CITY_STABILITY_9700026_AUTHOR_EXTERNAL_MANIFEST.json; 1878 bytes; SHA-256 1e2c8f73e3d7d0bb127773a089901d11d70f3f44445f08f128c399ee71c68fe9.
- PROOF.md: 5736 bytes; SHA-256 8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767.

All eight ZIP members match their manifest byte counts and SHA-256 digests, match the inspected working copies, and form exactly the listed member set. All seven entries in the inner MANIFEST.json also match. The author snapshot's pending-review labels describe the frozen snapshot; this separate acceptance does not rewrite them.

## Primary source scope

The [2007 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf), dated April 25, permit positive alpha and beta on p.2. Their p.7 conventions impose no exponent normalization. Section 6.4 on p.40 displays the fixed-site simplex ODE and includes alpha > 1 in the collapse disjunction. Assumption and parameter passages throughout the 41-page document were inspected; no global restriction removes this case. Local restrictions in earlier sections do not override p.40.

The [author page](https://www.stat.berkeley.edu/~aldous/Research/OP/cities.html) links these technical notes and the later paper. The [2012 paper](https://arxiv.org/abs/1209.5120v1), section 2, restricts alpha to (0,1] and includes stochastic city formation. It does not state Conjecture 32. The present result does not target that paper.

Fresh HTTP retrievals of both PDFs returned 200 and matched the recorded sizes and hashes. The decisive 2007 pages 2 and 40 and 2012 page 2 were independently rendered and visually inspected. No copied source pages or text are included in this review package.

## Independent mathematical derivation

Let D=[0,1]^2, n>=2, and x_1,...,x_n be distinct interior points. For alpha,beta>0 and z_i>0, sum z_i=1, define A_i(z) as the area where city i maximizes z_i^alpha |y-x_i|^(-beta). The differential equation under review is

z_i'=A_i(z)-z_i.

Write q=alpha/beta and p=2q. Outside the finite set of sites, city i beats j precisely when

|y-x_i| <= (z_i/z_j)^q |y-x_j|.

Taking a positive beta-th root preserves the inequality, so only q affects the cells and the vector field. In particular, (2,8) and (1/2,2) yield exactly the same differential equation in exactly the same time variable. This observation diagnoses a problem with an alpha-only threshold, but alone would not decide which of two competing conjectural conclusions fails. The persistence proof below supplies that decision without assuming either conjectural conclusion.

### Tie sets and continuity

For a positive ratio r=(z_i/z_j)^q, a pairwise tie is the zero set of

f_r(y)=|y-x_i|^2-r^2|y-x_j|^2.

This polynomial is nonzero: for r=1 it has nonzero linear part because the sites differ, and for r!=1 it has nonzero quadratic part. It is a line or a circle and has planar measure zero. Finitely many such sets, plus the sites, still have measure zero. Almost every y has a unique winner. Its winning strict inequalities persist as z varies sufficiently little. Dominated convergence gives continuity of A_i on the positive orthant. Area bounds and the almost-everywhere partition give 0<=A_i<=1 and sum A_i=1. No convention at ties changes the ODE.

### Existence, positivity, and simplex invariance

Continuity gives a local C^1 solution from every positive initial state. Summing the equations gives s'=1-s for s=sum z_i, hence s(t)=1 when s(0)=1. Also z_i'+z_i=A_i>=0, so

z_i(t)>=e^(-t)z_i(0)>0

at every finite time on its interval of existence. On a finite interval [0,T], each coordinate is at least e^(-T)z_i(0) and at most 1. The solution therefore stays in a compact subset of the positive orthant and has bounded derivative. If a maximal interval had a finite endpoint, bounded derivative would give a limiting state there, and local existence would extend the solution. Thus solutions exist for all t>=0. This reasoning is valid without uniqueness and applies to every solution.

### Uniqueness can also be established

The author correctly does not need uniqueness to refute collapse, because the ensuing inequality holds for every solution. For completeness, the vector field is locally Lipschitz in the positive orthant.

Fix distinct sites a,b and a positive r. Direct expansion gives

|gradient_y f_r(y)|^2 = 4 r^2 |a-b|^2 + 4(1-r^2) f_r(y).

Consequently the gradient on f_r=0 has magnitude 2r|a-b|>0, including r=1. For r in a sufficiently small closed positive interval, the zero set over the compact square admits a finite cover by coordinate rectangles in which one spatial partial derivative is bounded away from zero. Each one-dimensional slice through such a rectangle is monotone in that coordinate. Fubini's theorem bounds the area of |f_r|<=epsilon there by a constant times epsilon. Outside this finite cover, compactness excludes a sufficiently small zero band. Constants can be chosen uniformly over the closed r interval.

Furthermore |f_r-f_s|<=C|r-s| on D for r,s in that interval. Where the signs differ, |f_r|<=C|r-s|. Thus the pairwise dominance sets have symmetric-difference area O(|r-s|). A city's cell is the intersection of finitely many pairwise dominance sets; its symmetric difference is contained in the union of the pairwise symmetric differences. The ratios (z_i/z_j)^q are smooth on the positive orthant. It follows that every A_i, and therefore the ODE vector field, is locally Lipschitz. Standard local uniqueness follows and combines with the preceding continuation argument to give a unique global positive trajectory. This supplementary regularity argument is not needed to repair any gap in the author's all-solutions proof.

### Geometric lower bound without boundary loss

Choose h_i>0 with x_i+[-h_i,h_i]^2 contained in D and 8h_i^2<=|x_i-x_j|^2 for all j!=i. Interiority and finitely many positive pairwise separations guarantee that such h_i exist. For any positive simplex state define

Q_i=x_i+[-h_i z_i^q,h_i z_i^q]^2.

Because z_i<=1, this square remains in D. For y in Q_i,

|y-x_i|<=sqrt(2)h_i z_i^q,

|y-x_j|>=|x_i-x_j|-|y-x_i|>=2sqrt(2)h_i-sqrt(2)h_i z_i^q>=sqrt(2)h_i.

Hence |y-x_i|<=z_i^q |y-x_j|<=(z_i/z_j)^q |y-x_j|, where the last step uses 0<z_j<=1 and q>0. Therefore Q_i is in the i-th cell, apart from irrelevant site conventions, and

A_i(z)>=area(Q_i)=4h_i^2 z_i^(2q)=K_i z_i^p,

with K_i=4h_i^2>0. This is uniform over the entire positive simplex, not a local linearization or sampled assertion. Every square is explicitly contained in the actual unit-square domain; no whole-disc area is assumed near its boundary. Boundary sites need not be covered to refute a statement applying to general-position interior configurations. The earlier source's caveat about disc boundary effects does not affect this square argument.

### Comparison in the actual time variable

If beta>2alpha, then 0<p<1 and

z_i'>=K_i z_i^p-z_i.

Positivity permits differentiating u_i=z_i^(1-p). Multiplying by the positive factor (1-p)z_i^(-p) gives

u_i'>=(1-p)(K_i-u_i).

Direct integrating factors, rather than an unproved comparison principle, yield

u_i(t)>=K_i+(u_i(0)-K_i)e^(-(1-p)t).

The right side is a positive convex combination of K_i and u_i(0), even when u_i(0)<K_i. Raising it to 1/(1-p)>0 preserves order. Therefore

z_i(t)>=[K_i+(z_i(0)^(1-p)-K_i)e^(-(1-p)t)]^(1/(1-p)),

z_i(t)>=min(z_i(0),K_i^(1/(1-p)))>0,

liminf as t tends to infinity of z_i(t)>=K_i^(1/(1-p))>0.

The exponent is computed in the displayed autonomous ODE time; no hidden rescaling was introduced. For each i the positive lower bounds on the other n-1 coordinates and sum z_i=1 bound z_i strictly below 1 for all time. Thus no coordinate can converge to 1. These conclusions do not assert that the coordinates converge at all.

## Independent exact witness arithmetic

For alpha=2, beta=8, q=1/4 and p=1/2. The stated sites are (1/5,1/4), (3/4,1/3), (2/5,4/5). Their minimum coordinate distances to the square boundary are respectively 1/5, 1/4, 1/5, all strictly exceeding h=1/16. Independently calculated squared pairwise distances are

- |x_1-x_2|^2 = 557/1800;
- |x_1-x_3|^2 = 137/400;
- |x_2-x_3|^2 = 49/144.

Each exceeds 8h^2=1/32; their respective excesses are 2003/7200, 249/800, 89/288. They are pairwise different, and the signed triangle determinant is 343/1200, so the illustrative configuration is noncollinear and scalene. The initial weights (1/6,1/3,1/2) are strictly positive, distinct, sum to 1, and exceed 1/4096. Since K=4h^2=1/64 and K^(1/(1-p))=K^2=1/4096, the comparison proves, for all t>=0 and all i,

1/4096<=z_i(t)<=1-2/4096=2047/2048.

## General position and parameter boundaries

The source does not formalize its general-position qualification. Noncollinearity and scaleneness alone cannot certify every possible genericity convention for the rational illustration. That ambiguity does not undermine the result: the theorem covers every distinct interior configuration, every positive initial probability vector, and every parameter pair in the open region alpha>1, beta>2alpha. The geometric inequalities at the witness are strict and persist under small perturbation. Therefore ordinary exclusions of symmetric, degenerate, stationary, lower-dimensional, or measure-zero initial configurations cannot restore collapse. The result works for each finite n>=2. It is not a statement about the trivial one-city case.

There is no division by zero because alpha,beta,z_i,h_i are positive and sites are distinct. The proof requires strict beta>2alpha. At beta=2alpha the exponent transformation degenerates and no persistence conclusion of this form is claimed. The beta<2alpha case, zero initial weights, and coincident sites are outside this acceptance. Interiority is an explicit sufficient hypothesis for the proof; its admissible open family already contradicts the general-position assertion.

## Execution evidence and limits

All 16 fresh runs passed: certificate verification and adversarial self-test, each under normal Python, optimized Python, isolated Python, and isolated optimized Python, both against the inspected author files and a fresh ZIP extraction run from an unrelated working directory. Each certificate execution performed 216 exact influence comparisons and four comparison-ODE coefficient identities. Each self-test rejected 16 negative cases and accepted the two declared positive controls. REPLAY_B.json contains the complete new receipts and all eight file-identity checks.

The checker is specialized to q=1/4 (p=1/2) and certifies the rational illustration and specified controls. Its finite samples do not prove the geometric inclusion for every state or the all-time trajectory claim; those were established above analytically. No simulation was used as proof. The broader theorem is not restricted by the checker's deliberate specialization.

The exact target record and its matching source statement were inspected. This focused review does not independently renew the author's historical repository searches, current queue state, complete dataset hashing, or exhaustive literature status. It makes no claim of novelty or absence of prior resolution. It verifies the frozen identities, primary-source interpretation, and mathematical counterexample at issue. No GitHub write or external publication was made by this reviewer.

## Publication-safe conclusion

A precise summary is: "The literal alpha>1 collapse alternative in the 2007 fixed-site city ODE conjecture is false. When beta>2alpha, every positive coordinate persists; alpha=2, beta=8 gives an explicit asymmetric example with all weights between 1/4096 and 2047/2048. Restricted collapse and convergence questions remain unresolved by this argument."

The review package contains only authored audit reasoning, public source metadata, cryptographic verification metadata, and exact-check receipts. It contains no third-party PDF, copied source passage, dataset record, private source, personal information, or coordination material.
