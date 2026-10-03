# PR 372 / 9700034: metric and moment adversarial audit

The five scoped mathematical results survive this source-first audit. The unrestricted SIRSN target remains unresolved, and no geometric counterexample is provided. This report gives no overall merge decision and no historical novelty certification.

Candidate head: f30fb696da92fd4b998d61859d6ed06012ce78d4. All candidate inspection and execution used the supplied snapshot; execution used a private copied directory. No Git/service writes, installations, or external communications occurred.

## Independent sequence and seals

Before reading any candidate TURN, proof, code, receipt, or old review, I read only SOURCE_MANIFEST locators; freshly fetched Aldous 2012, Aldous 2014, Aldous's maintained index, and Kahn 2016; extracted their relevant mathematical sections; rendered and visually inspected the target pages and Kahn's formula/proof pages. All four fetched byte counts and SHA256 hashes match the candidate source manifest. I also fetched the Kendall primary dependency and checked its confinement, simultaneous connectivity, existence and fixed-pair uniqueness statements. Its separate receipt is retained without pretending it was one of the four candidate source bindings.

The independent baseline was sealed at **2026-10-03T09:57:04.425708Z**, SHA256 **da9f3fe1c433b10808d2c961518bf0b1469236123d7cc05e297ce1d23c8f4c1c**. The baseline includes a complete nested-radius record derivation using joint events. Only then did I read all five TURNs and the final mathematical/source statements. The mathematical verdict was sealed at **2026-10-03T09:59:54.512808Z**, SHA256 **8ce10a95ac2140ee904a89ce1e888efb4ad8978e2582f52be90ba5e3cb6f8c39**, before any program or receipt was read. The old candidate review was read only after these seals and after program inspection/replay began. No root or sibling artifacts informed the baseline or verdict.

The full derivations and claim-by-claim reconstruction are in INDEPENDENT_BASELINE.md and MATHEMATICAL_VERDICT.md. The sealed files were not rewritten after candidate inspection.

## Verified metric distinction and threshold

Let gamma>d>=2, q=gamma-1, a=gamma-d. The Poisson-line maximum speed in radius r has tail governed by c_d r^(d-1)v^(-q). All time-minimizing routes to destinations in the unit ball have a common environmental time bound Tau with P(Tau>t)<=C exp(-ct^q). A long route's initial arclength-r segment lies within the radius-r ball, so time at most t forces V(r)>=r/t. This is an arclength statement, independent of the route's ultimate Euclidean confinement.

A single-radius union bound only yields route-length moments p<a. It would require gamma>3 to prove the first moment in the plane, and does not settle gamma=3. The candidate instead proves a nested-radius record bound. The nested maximum speeds themselves are dependent; independence occurs only in disjoint marked-line-space layers. Correct event inclusion is

    P(M>r_m, Tau<=t) <= P(all deterministic speed constraints).

The record-composition sum bounds the right side, and the time-tail union bound yields E M^p finite for every **0<p<gamma-1**. This covers the first moment for every planar **gamma>2**, without any endpoint-count factor or infinite union bound. No boundary moment at p=gamma-1 and no conjectured stronger moment is claimed. This independently verifies TURN_1 and matches the sealed derivation.

The bound is common to all admissible paths from the fixed root with time at most Tau, so it supports any measurable countable chosen-route family. It does not assert a measurable uncountable route supremum or all-pair uniqueness. Independent iid endpoint sampling is used to interpret the original question and to use countable/FDD laws; it is not an independence assumption between travel time and the line environment.

## Source formula issues and repairs

Visual inspection found these errors in Kahn's supplied source version:

- PDF p.9 equation (2) prints travel time as sum v(l)L_g(l). The immediately preceding identity requires sum L_g(l)/v(l).
- PDF p.12 reverses inequality signs in a lower-bound argument for the hitting-line measure, and its displayed cone normalization is unsuitable as written in general dimension. A direct positive geometric lower bound with the correct scaling repairs the no-forbidden-set input used here.
- PDF p.13 speed-threshold constants do not cancel as printed. The tail bound needs only a finite positive deterministic constant, which a correct choice supplies. Its displayed exponential-moment constant has the wrong exponent: from T<=C(log(1/epsilon))^(1/q), the usable range is delta<C^(-q) for E exp(delta T^q).
- PDF pp.26-27 use a conditional probability without the necessary denominator. The record estimate correctly controls a joint event followed by addition of P(Tau>t).

The candidate uses Theorem 3.1's qualitative common tail and explicitly repairs the last issue. It never uses the erroneous sum vL expression or the exact erroneous exponential-moment constant. These printing issues therefore do not falsify the scoped candidate theorem. They should remain visible in source-audit notes to prevent a later proof from copying the formulas literally. This report does not certify every formula or every forbidden-set claim in the source paper.

## General geometric and probabilistic reductions

TURN_2's dyadic criterion requires alpha p>2; its route-length triangle corollary expressly adds that triangle hypothesis and a p>2 moment. Minimum-time routes with heterogeneous speeds need not meet that route-length triangle hypothesis. The critical log-log random field is scalar only and supplies no SIRSN obstruction.

TURN_3 correctly separates the marginal route tail E Q(t) from the maximum tail P(Q(t)>0), treats the random visibility factor through the invariant sigma-field and Holder without independence, and preserves the joint-law assumptions in every sufficient condition. Its heavy-environment example has all individual moments but an infinite mean of the finite maximum; it is scalar only.

TURN_4 uses Aldous's established major-road process, p(r)=p(1)/r and planted-origin equality (6.4). Those are exact source dependencies, including the source's measure-theoretic random-set formulation. The finite circle crossing set implies at most N choose 2 exterior arcs by compatibility. Their finite random union gives almost-sure confinement and finite total exterior length, while leaving its mean unsupported. The dyadic fixed-root annuli sum to **3pi p(1) eta** and the bounded middle has expectation at most **9pi p(1)/eta**. Varying terminal neighborhoods receive no such fixed-center estimate. Disc/annulus equivalence uses scaling and countable iid shell subsequences, not independence between shell maxima.

TURN_5's mixture result is valid for the ordinary nonergodicity-requiring class. It requires genuine models with unbounded H/(Delta+p) before producing a counterexample. The rotated affine construction is genuine, but the projection argument forces Delta to grow linearly with the same anisotropy as the maximal upper bound, with constants dependent on the fixed base's transverse variation. It cannot settle the universal ratio bound or rule out varying base models/local deformations.

## Complete program replay and evidential limit

I read every line of all nine candidate Python programs: check_turn_1 through check_turn_5, verify_packet, verify_publication, review/independent_check and review/replay_author. Eleven invocations, including optional source-directory variants, ran under ordinary CPython 3.14 with assertions enabled, PYTHONHASHSEED=0 and bytecode writes disabled. Every invocation exited 0 and produced empty stderr. All full stdout/stderr streams are preserved under private/replay_streams. REPLAY_RESULTS.json includes complete parsed JSON (or full mixed stdout text), command, interpreter path, private working directory, UTC timestamps, byte counts and stream hashes. No output was accepted from a truncated terminal view.

| Program | Exact finite assertions | Reproduction |
|---|---:|---|
| check_turn_1 | 151,582 | byte-exact stored receipt |
| check_turn_2 | 183,315 | byte-exact stored receipt |
| check_turn_3 | 51,476 | byte-exact stored receipt |
| check_turn_4 | 104,312 | byte-exact stored receipt |
| check_turn_5 | 12,734 | byte-exact stored receipt |
| candidate old independent checker | 2,507 | stored output reproduced by publication verifier |

The five author programs total **503,419** assertions. verify_packet validates **64** frozen bindings and all five exact receipts; its source variant validates all **4** fresh primary hashes. verify_publication validates publication/review bindings and frozen hashes; both source variants pass. The old replay_author additionally reports **111** bindings. These counts refer to their distinct scripts and do not count independent theorems or proof steps.

TURN_1's checker verifies finite monotone speed profiles/compositions and rational exponent identities; it does not verify Poisson geometry or the existence/time-envelope theorem. TURN_2 checks grids and algebra, not Sobolev/analytic passage or FDD measurability. TURN_3 checks finite directing-law second moments, not the full exchangeable limiting proof. TURN_4 checks finite trees, not continuum circle regularity or selected-arc expectations. TURN_5 checks weights/projections, not actual SIRSN class closure. Their reported scopes accurately state these limitations.

An additional independent finite control explicitly enumerates **8,476** independent-increment histories, hence dependent nested maxima, and checks **31** record-event intersections with exact rational probabilities. Its **121** assertions also show why conditioning the speed event on itself violates the shortcut P(H|B)<=P(H), and test strict first-moment thresholds arbitrarily close to gamma=d. All pass; full output is ADVERSARIAL_CONTROLS.json. This is an adversarial finite surrogate, not a Poisson-line simulation or continuum proof. No replay failed and no failures were suppressed.

## Strongest verified result and exact gap

Verified scoped result: the concrete planar Poisson-road model has an integrable countably sampled maximum for every gamma>2, with positive moments strictly below gamma-1. General additional-condition criteria, finite-exterior/annular localization and the mixture equivalence also survive their stated hypotheses. No mandatory mathematical correction to those candidate scoped proofs was found.

The ordinary SIRSN axioms have not supplied the required integrable terminal maxima, exterior maximal first moment, endpoint-tail visibility, increment bound, or universal H/(Delta+p) estimate. No genuine SIRSN family with the needed divergent ratio has been constructed. These remain the exact unsupported central steps; scalar examples, single-route moments and finite checkers do not replace them. The audit is complete for its assigned scope, without making a discovery/novelty or overall PR decision.

Raw primary PDFs/HTML, extracted primary text, rendered pages and candidate copies/streams remain private and ignored. The public manifest explicitly binds only original audit proofs, code, generated finite-control output and metadata.
