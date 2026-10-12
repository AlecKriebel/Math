# PR 73 / KP-4.109: independent geometric and symplectic adversarial report

Report UTC: 2026-10-04T18:06:02.929456+00:00
Submitted head: `6f82e81631fd43abc0140a831acfb43c150f4210`.
Original literal publication status assigned for audit: `claimed_solved`, substantive proof-attempt budget `1/5`; this report independently assesses the mathematical claim and does not alter that record.

## Verdict and scope

**The main prescribed-surface counterexample is mathematically valid under the usual definitions. No essential geometric, symplectic, quotient, integrality, genus, or self-intersection gap was found.** The fresh symbolic check strengthens the cutoff positivity argument to an explicit uniform bound. The result gives a connected embedded symplectic surface of genus three in a closed symplectic four-manifold, with integral real class `PD[Sigma]=[Omega]` and self-intersection four, whose complement admits no Weinstein structure for any symplectic form.

This negates the main universal question in KP-4.109. It does not answer its CP2 specialization, show that every degree-one surface in the constructed manifold has a non-Weinstein complement, or provide effective Donaldson degree bounds. It gives no historical-priority clearance. The candidate states these limits correctly. The audit did not search for priority or consume an additional proof-search program disguised as verification.

The report concerns the exact submitted candidate, not a repaired version. Two small editorial clarifications are proposed below; neither is needed to supply a missing mathematical mechanism.

## Independence, custody, and phase order

Before the first conclusion, project mathematical reading was restricted to the designated `CANDIDATE.md` and `TARGET_STATEMENT_ONLY.json`. Primary-source reading consisted of the cited Giroux paper and the cited K3 author PDF. The independent first conclusion was sealed at `2026-10-04T17:50:39.738805+00:00`, SHA256 `59918b4b63afc059de2c641ea06d4d0ac21840a4acdc2ecb0429521ea60a9fdf`, 6689 bytes, before any mathematical computation, original checker, old review, background triage, or other agent opinion.

After the seal, read-only GitHub tree/raw access authenticated the candidate at the assigned submitted head. The remote candidate has 10731 bytes, SHA256 `78ab061c9c0c6c16f2e6b249e764001361933782d7381982c733f92cefda3c8f`, and Git blob SHA1 `a26d0c232cdd02aecb177e6d90086d023432130e`; it is byte-identical to the restricted input. No fetched ref, shared Git index, branch, PR, editor, paper, tracker, upload, DOI, or publication record was mutated.

The remote filename locator exposed names of old review/checker files, but no file contents or conclusions. A subsequent ROOT message supplied only authentication locators and permission to read diagnostics. That permission was not exercised. No source_record.json, TARGET_PROBLEM_ONLY.json, SOURCES, old checker/review, project mathematical log, ROOT/sibling mathematical opinion, or original diagnostic was read before the independent report draft at 2026-10-04T18:02:39.010903+00:00. At that point the only ROOT messages read concerned task instructions, first-seal notification protocol, and exact authentication locators. After that independent draft, a ROOT status message reported successful old-checker replays. This post-draft external diagnostic summary was read; no original checker code or full output was read, and the summary did not supply or alter the mathematical verdict. Before the final evidence seal, ROOT additionally reported having read this independent report and finding no mathematical concern, and clarified that 1/5 labels the substantive proof-attempt budget. That bounded post-draft ROOT opinion and factual correction are recorded; the opinion was not used to derive or change the independent result. No sibling mathematical conclusion was read.

## Exact target and source reading

The cited Berkeley K3 author PDF, printed and physical page 281, supplies the original prescribed-surface question and its two remarks. The full relevant page was extracted and rendered; the literal target does not require simple connectivity or restrict the ambient manifold to CP2. The two remarks distinguish a CP2 specialization from an existential large-degree construction and effective bounds. This example satisfies the main hypotheses at k=1; it does not settle those additional questions. [K3 author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

Giroux's actual Proposition 9 is attributed to Auroux and constructs disconnected hyperplane sections in the four-torus. Its proof uses the same two integral forms and local desingularization of pairs of affine tori. Giroux also states the hyperplane-section convention and the Weinstein Morse-index constraint. The candidate supplies explicit offsets and a free quotient, plus its own local cutoff argument. Giroux's shorthand a != b does not guarantee all cross-pair disjointness equations for arbitrary offset vectors; the candidate's four unequal constants prove the needed separation directly. Giroux's [Au4] is a private communication and was not accessed. This review makes no independent claim about Auroux's thesis. [Giroux's primary preprint](https://arxiv.org/abs/1803.05929).

Reading scope: Giroux extracted pages 1-4, 8-10, 19-20; rendered pages 8-10 inspected in full. K3 page 281 extracted and rendered in full. A source locator exposed K3 bibliography entries citing 4.109 and adjacent unrelated entries; this incidental exposure is recorded. The source PDFs, full extracted text, page pixels, and full source-bearing read receipts are kept in `/tmp/pr73_geometric_smoothing_adversary_20261004`, outside Git. Their bytes and SHA256s are recorded in `source_evidence_manifest.json`.

## Specific affine and orientation checks

The two torus parametrizations are embeddings: A has parameters recovered from x2 and x4, while B has parameters recovered from x1 and x2. Their tangent frames are

- A: `(0,1,1,0)`, `(0,0,0,1)`;
- B: `(1,0,0,0)`, `(0,1,-1,0)`.

The omega0 area coefficient of each ordered frame is exactly 1. With A's frame followed by B's, the ambient determinant is 2. Thus their intersections have the asserted positive signs, independently of any generic assertion that symplectic intersections must be positive.

The modular equations reduce their intersections to x1=0, x4=1/4, x2=x3=t, and `2t=1/4 mod 1`. There are exactly two roots, 1/8 and 5/8. The local normal-equation Jacobian also has determinant 2, so both nodes are transverse. The normal fiber coorientations have determinant +1 relative to the specified symplectic tangent orientations, giving the claimed Poincare duals.

The involution squares to the identity modulo the unit lattice, has no fixed point because x1 changes by 1/2, and preserves omega0 because both dx3 and dx4 change sign. The four possible cross-pair intersections of the two nodal unions fail by conflicting constants in x1, x4, x2-x3, or x2+x3. Since the two compact unions are disjoint, an averaged invariant metric gives neighborhoods with disjoint closures after shrinking. All later smoothing charts can be chosen within the first neighborhood U.

No global affine-coordinate assumption is used. At the first node, local normal lifts have `s3=x2+x3-1/4`. At the second, if the standard coordinate lifts x2=x3=5/8 are used, the normal lift vanishing at the node is `s3=x2+x3-5/4`. Equivalently one lifts the modular normal equations independently near zero. Their differentials, the inverse local Jacobian, and both forms are identical. The candidate's phrase about appropriate local lifts allows this; an explicit second-node constant would improve clarity.

## Continuous smoothing, including central and transition seams

In each local chart, let z=s1+i s2 and w=s3+i s4. Then

`alpha=ds1 wedge ds2+ds3 wedge ds4`,
`beta=ds1 wedge ds3-ds2 wedge ds4=Re(dz wedge dw)`,
`omega0=(alpha+beta)/2`.

Choose fixed `0<a<b` small enough that the closed local polydisc is inside the chosen chart and U. Choose a real `epsilon>0` with `epsilon<a^2`, and a smooth cutoff chi taking values in [0,1], nonincreasing on [a,b], equal to 1 on an inner collar and 0 on an outer collar. Such a cutoff exists by integrating a nonnegative smooth bump supported in the intervening interval.

The central annulus is `zw=epsilon`, with `epsilon/a <= |z| <= a`; both coordinate magnitudes are at most a. Its complex tangent plane has beta=0 and strictly positive alpha. Attach the graph `w=epsilon*chi(|z|)/z` for `a<=|z|<=b` and the symmetric graph `z=epsilon*chi(|w|)/w` for `a<=|w|<=b`. On each inner collar the graph agrees exactly with the central holomorphic formula; on each outer collar it agrees exactly with the corresponding original axis. Equality of the formulas on collars makes all derivatives match. Thus there is no finite-order seam or corner left to smooth separately.

For an independent universal positivity calculation, put z=x+i y, r=(x^2+y^2)^(1/2), and write the z-arm as `w=A+i B`, where `A=g(r)x`, `B=-g(r)y`, `g=epsilon*chi/r^2`. With `h=g'(r)/r`, its Jacobian has entries

`A_x=g+h*x^2`, `A_y=h*x*y`,
`B_x=-h*x*y`, `B_y=-g-h*y^2`.

Consequently beta has coefficient `A_y+B_x=0`, while

`det D(A,B)=-g^2-g*h*r^2`
`=epsilon^2*chi^2/r^4-epsilon^2*chi*chi'/r^3`.

Therefore the omega0 area coefficient is

`(1+epsilon^2*chi^2/r^4-epsilon^2*chi*chi'/r^3)/2 >= 1/2`

at every point of the transition annulus. The w-arm has the same alpha coefficient and an opposite beta sign, still zero. In the central region the coefficient is `(1+epsilon^2/r^4)/2>0`. This is a universally quantified calculation, not a finite parameter grid. The exact polynomial identity in g,h,x,y was executed independently; the substitution and monotonicity inequality are explicit written deductions.

Each arm is an embedded graph. The z-arm has |z|>=a and |w|<=epsilon/a<a; the w-arm has |w|>=a and |z|<a, so their interiors cannot overlap. The central annulus is an injective graph over nonzero z and meets the arms only in the intended formula-agreement collars. It misses each axis away from the retained outer pieces. Both local modifications can be chosen in disjoint balls at the nodes; outside those balls the original affine tori remain unchanged. Agreement near each ball boundary makes the difference an oriented 2-cycle supported in a contractible ball, hence null-homologous. This proves smoothness, embeddedness, positivity, locality, and preservation of the class simultaneously.

The case epsilon=0 would be singular and is explicitly excluded. The bound epsilon<a^2 is essential for this convenient arm separation. No claim is made for large parameters or oscillatory cutoffs. The candidate needs only one valid choice, and the monotone choice is among its permitted smooth cutoffs. For arbitrary fixed cutoffs the candidate's small-C1 perturbation argument also works; the stronger calculation above removes the need for that estimate in the selected construction.

## Free quotient, periods, genus, and self-intersection

The smoothed surface S stays inside U and its image tau S stays inside tau U. Defining the second surface as that image handles equivariance exactly, with no second independent gluing parameter. S and tau S are disjoint. The quotient map is a smooth oriented twofold covering; its restriction to S is an injective immersion of a compact surface and hence an embedding and diffeomorphism onto Sigma. It follows that Sigma is smooth, connected, embedded, and symplectic for the descended form and its positive rescaling Omega.

Two genus-one surfaces have Euler characteristic zero. Removing four disks at the two nodes gives Euler characteristic -4; inserting two annuli preserves that value and connects the two punctured tori. Thus S, and therefore Sigma, has genus three.

Poincare duality naturality for the oriented finite cover gives `p*PD_X[Sigma]=PD_T4[S+tau S]=[alpha+beta]=2[omega0]`. The real transfer identity `tr p*=2 id` establishes real injectivity and therefore `PD_X[Sigma]=[Omega]`. Its integral lift is the genuine integral Poincare dual of the embedded surface. Every integral cycle consequently has an integer Omega period. This does not assume injectivity of integral pullback, identify a preassigned integral lift, or remove possible torsion by hand.

A useful separate rationality check is the invariant torus x3=x4=0. Its quotient has parametrization `p(t/2,u,0,0)` for t,u modulo one. Its bar-omega period is 1/2, and its Omega period is 1. Thus one must not casually infer that bar-omega itself is integral from its integral pullback. The factor-two rescaling used by the candidate is consistent with an explicit primitive integral period.

The exact exterior products are `alpha^2=beta^2=4 vol_T4`, `alpha beta=0`, and `omega0^2=2 vol_T4`. The quotient volume is `integral_X Omega^2=(1/2)*integral_T4 (2 omega0)^2=4`. The surface self-intersection is therefore 4. It also follows directly upstairs: the normal bundle of S is unchanged by the diffeomorphism p restricted to S, so Sigma^2=S^2=integral alpha^2=4. These two calculations agree and use the degree-two factor in different places.

## Topological obstruction and limits of imported facts

Removing a closed embedded codimension-two submanifold from the connected four-torus leaves it path connected: a path with fixed endpoints outside the surface can be made transverse, and the dimension sum 1+2<4 makes its transverse intersection empty. The punctured complement retracts onto the compact exterior M by radial movement in disjoint tubular neighborhoods.

For the oriented rank-two normal bundles, excision and the Thom isomorphism identify `H4(T4,M;Z)` with `H2(S disjoint-union tau S;Z)=Z^2`. The ambient fundamental class maps to the two oriented component classes, `(1,1)`. Exactness therefore embeds `Z^2/<(1,1)> = Z` into `H3(M;Z)`. Normal Euler numbers do not change that map, and no torsion can remove the free cokernel after it injects.

A Weinstein four-manifold has an exhausting Morse function whose critical indices are at most two; its ordinary homotopy model has no cells above dimension two. A finite cover lifts the symplectic/Liouville/Morse data; the lifted exhaustion remains proper because the covering is finite, and the indices remain unchanged. Equivalently, a CW homotopy model lifts to the corresponding covering. Thus every finite cover of a Weinstein four-manifold has zero ordinary third homology. The connected twofold cover of the candidate complement has the nonzero H3 just proved, giving the contradiction. The audit does not assert that the base complement itself has nonzero H3. In particular, anti-invariant homology upstairs may disappear in the base, which is why the covering argument matters.

Imported standard facts: regular-fiber Poincare duality, oriented Thom isomorphism/excision and the homology sequence, real transfer for finite coverings, general-position avoidance of codimension two by paths, properness under finite covers, and the Weinstein Morse-index theorem. The candidate proves its own affine placement, orientations, local smoothing, separation, free quotient embedding, integral real class, genus, self-intersection, and specific relative homology map. Neither the code nor the cited disconnected example substitutes for those smooth and universal arguments.

## Adversarial mechanism ledger

| Mechanism tested | Evidence | Status | Exact gap remaining |
|---|---|---|---|
| Wrong affine fiber count or orientation | Modular reduction, ordered tangent determinant 2, fiber coorientation determinants +1 | Refuted | None |
| Cross-pair collision or mandatory global gluing | Four inconsistent constant pairs, disjoint neighborhoods, second surface defined as tau S | Refuted | None |
| Central symplectic failure | beta vanishes on zw=epsilon, positive alpha | Refuted | None |
| Transition or seam failure | Exact radial Jacobian identity and density >=1/2; formula equality on collars | Refuted | None |
| Smoothing self-overlap | Graph injectivity and strict epsilon/a<a separation | Refuted | None |
| Quotient singularity or surface identification | Free first-coordinate shift; p restricted to S injective | Refuted | None |
| Descent rationality/integral-torsion defect | Real transfer plus actual integral PD lift; explicit period 1 | Refuted | None |
| Genus or degree-two volume mistake | Euler characteristic -4; both upstairs normal Euler and quotient volume give 4 | Refuted | None |
| Wrong base/cover homology inference | Integral cokernel injection upstairs; finite-cover index obstruction | Refuted | None |
| Scope inflation to CP2 or existential k=1 failure | Full original p.281 checked and candidate exclusions retained | Refuted for stated theorem | Those separate questions remain outside theorem |
| Historical originality assumed from correct math | No priority clearance undertaken or inferred | Not assessed | Historical priority remains unconfirmed |

## Repairs, reproducibility, and receipt limitations

No theorem-level repair is required. Editorial suggestions: replace literal `quad` in the displayed local coordinate line with `\quad`; explicitly write the second node's `-5/4` local normal constant (or say that the normal equations themselves are lifted independently); optionally choose epsilon real and chi monotone and add the uniform area identity above. The existing small-parameter positivity argument already establishes the needed existence.

Actual fresh diagnostic executions are recorded in receipts 025 and 028. All computations use Python standard-library exact integer/rational and polynomial arithmetic; no author checker, sampled numerical test, or external mathematical computation service is used. The first run checked the initial exact data; the second followed the single added invariant-torus period check. There was no unrelated repeat or broadened test run.

Process receipts record actual cwd, launched child PID, argv, UTC start/end, exit code, and full stdout/stderr. Source-bearing full streams are private and referenced by a byte manifest. Two early attempts to launch a nonexistent `/opt/homebrew/bin/rg` failed during subprocess creation, before a successful rg process was returned. The first wrapper version had not persisted its own PID/timestamps on spawn failure: those two runner PID and exact UTC fields are unavailable and are labeled, not reconstructed. A transient process used internally by subprocess to attempt exec may have existed; its PID was not exposed. No successful rg diagnostic ran in those attempts. Their exact attempted argv, full native error streams, and bounded time window are retained. This is a process-evidence limitation, not a mathematical gap. The wrapper was then repaired and both locators rerun successfully using rg on PATH. The local Git object lookup also failed (exit 128) and has a complete receipt; read-only remote authentication then succeeded.

No outside individual was contacted or messaged, and no outreach text was prepared. All output writes were confined to the assigned audit namespace, with private source intermediates in the stated temporary directory. Git commits/pushes and release decisions are left to ROOT because this subtask expressly prohibited shared Git mutations.

Final checkpoint estimate: **100% of this assigned independent geometric/symplectic adversarial audit**; this is not an estimate of solving the CP2 or degree-bound questions or clearing historical priority. The strongest verified result is the exact submitted theorem's main connected counterexample. Remaining mathematical gap for that theorem: none found. Remaining separate limitations: publication-priority assessment and the ancillary source remarks.
