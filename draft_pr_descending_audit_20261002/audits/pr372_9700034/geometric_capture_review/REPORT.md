# PR372 / problem9700034: independent geometric capture audit

Frozen candidate head: f30fb696da92fd4b998d61859d6ed06012ce78d4. Audit completed 2026-10-03 UTC. This report addresses source identification, proof validity and exact scope of the geometric mechanisms, with supporting checks of the remaining five-turn mathematics. It does not give an overall publication disposition or historical novelty certification.

## Result and exact gap

The candidate's universal geometric localization is supported by the ordinary SIRSN source axioms and their credited major-road consequences. All countably sampled prescribed routes whose endpoints lie in a bounded disc have a common random bounded spatial capture, and their union outside a larger deterministic disc has finite total length almost surely. These statements do **not** establish that the full infinite sampled route-length maximum is finite almost surely, or has finite expectation.

For annular destinations, the candidate proves the stronger exact reduction

    E M_A < infinity  iff  E J_eta < infinity and E O < infinity,

where J_eta is the supremum of the length inside each route's varying destination ball and O is the supremum of each individual route's exterior length. Its fixed-root union and bounded trimmed middle already have finite expected length. This is the strongest universal result verified in this audit. Neither missing expectation has been derived from the general axioms, and no actual SIRSN violating either expectation has been constructed. The iid disc maximum has finite expectation exactly when the annular maximum does, with E M_A <= E M_disc <= 2 E M_A.

The distinction between O and total exterior union length matters. Finiteness of the exterior union pathwise supports O<infinity almost surely; its total expected length is a stronger question. The actual reduction uses E O, not an unsupported expectation of the union or a sum over randomly selected arcs.

## Source-first chronology and independence

Only SOURCE_MANIFEST.json was read to locate primary sources before candidate mathematics. Fresh copies of the long Aldous manuscript, published Aldous paper, maintained SIRSN page, and Kahn2016 were fetched into ignored private storage; all four byte sizes and SHA256 hashes matched the frozen manifest. The exact long OpenProblem34 PDF50 and published OpenProblem8 PDF38 were read and rendered. Definitions and major-road dependencies were read in complete page batches and critical published PDF6-8,28-30,35 were rendered and inspected.

An independently derived baseline and adversarial controls were sealed at 09:57:19.333522 UTC, SHA256

    981653909f1e8ae0c4c72cd518913956b657c6967442ab397d5a45aaaf03a6cb.

It already derived almost-sure compact capture using finite crossing pairs, before TURN4 was seen. All five TURN proofs, FINAL_RESULT and FINAL_SOURCE_MAP were then read completely. Additional relevant primary-source passages were checked, including Aldous bounded stretch and no initial segments, and Kahn's uniform diameter and speed-record proofs. Kahn PDF10 and25 were rendered. The proof-only verdict was sealed at 10:01:00.013190 UTC, SHA256

    9b65adbbc4e641b1bc33586bc48750c00ddd064cdaf478ca64e13e23f2a784ea.

At that seal no candidate program, check receipt, old review, root artifact or sibling artifact had been read. The mathematical checker programs were then inspected in full and replayed in a private copy. No old review was used as evidence. No external individual was contacted, no installation or Git/API write occurred, and no branch change occurred.

## Reconstructed universal geometry

Let p=p(1). The published source's (6.2), Proposition6.3 and planted-point consequence (6.4) provide a common sampled major-road process E_r with intensity p/r, even for routes rooted at the planted origin. The independent iid destinations can be realized as successive spatial arrivals of a space-time PPP inside their bounded region, completed independently outside it. This ties the source's sampled networks to the countable family without an all-point realization or continuity assumption.

For endpoints in the unit disc, every route contact with circle(0,3) is strictly more than unit distance from both endpoints, hence belongs to E_1. The source crossing formula gives E N<=12p for the number N of distinct contacts. Thus N is finite almost surely. A simple route's connected exterior excursion has two distinct such endpoints. Route compatibility identifies any two excursion arcs with the same unordered pair. There are at most N(N-1)/2 distinct arcs, each a finite-length subroute of a sampled witness. Their finite union is bounded and has finite length. No expectation of selected witness length follows from deterministic-pair first moments or E N<infinity. The source-first independent proof used radius2 and r=1/2, giving the same conclusion with E N<=16p.

For V_i uniform on 1/2<|v|<1, eta<=1/4 and root shell eta*2^(-j-1)<|x|<=eta*2^(-j), every route point lies in E_{eta*2^(-j-1)}. The expected union length in that shell is at most (3pi/2)p eta*2^(-j); summing gives 3pi p eta. This uses deterministic shells and includes every return to the root ball. The bounded middle is contained in E_eta intersect B(0,3), with mean at most9pi p/eta. After taking the individual-route supremum,

    M_A <= root_union + bounded_middle + J_eta + O.

Since J_eta,O<=M_A, the displayed expectation equivalence follows. Dyadic shells of the iid disc sample provide infinitely many annular endpoints almost surely. Scaling gives shell maximum law2^(-k)M_A, and summing expectations gives the factor2. No independence between shell maxima is required.

## Other candidate mechanisms and limits

| Mechanism | Reconstructed support | Exact limit |
|---|---|---|
| TURN1 common Poisson time/speed envelope | Kahn uniform time diameter, initial-arclength speed barrier, unconditional record partition and convergent moment sum | Model-specific moments q<gamma-1; ordinary routes need not arise from any time metric or Poisson speeds |
| TURN2 dyadic increment criterion | Parent-grid maximum estimates and summable sampled-endpoint approximation, using measurable FDD kernels | Additional alpha p>2 increment estimate; route-length triangle inequality is extra |
| TURN3 tail visibility | Elementary exchangeability frequency proof, rational right limits, positive-frequency maximal-tail identity and Holder/Cauchy bounds | Positive-mass visibility or inverse-frequency estimates remain additional joint-law assumptions |
| TURN4 localization | Finite circle contacts and pairwise compatibility, deterministic root annuli and middle intensity | Compact capture and exterior length are a.s. statements; terminal/exterior expectations remain |
| TURN5 mixtures | Countable-mixture closure and exact diagonal weights | Actual laws with unbounded H/(Delta+p) are needed; arbitrary scalar triples do not construct them |
| TURN5 affine family | Linear transport preserves compatibility/scaling; random rotation restores isotropy; transverse variation forces Delta growth | Fixed-base ratio constant depends on c0 and the base law; no uniform estimate over all SIRSNs follows |

No unsupported transfer from minimum travel cost to Euclidean route-length triangle inequalities was found in the stated proofs. No all-point supremum is silently substituted for the iid maximum. The model-specific bound uses one common event, so it avoids an infinite union bound and avoids treating the route time bound as independent of speeds. The scalar translated log-log field and geometric-environment mixture are valid controls at their declared level; neither supplies compatible routes or the SIRSN symmetry and intensity axioms.

The sufficient conditions and exact reductions answer portions of the source's invitation to investigate extra assumptions. They do not establish that extra assumptions are necessary, or remove them from the general statement. A hypothesis that directly bounds J_eta, O or positive tail visibility must remain identified as a hypothesis rather than counted as a solution of the central claim.

## Independent adversarial construction

The audit supplied a concrete compact compatible tree control rather than relying on an abstract length field alone. For each n>=1, put a rectangle

    [2^(-n), 2^(-n)+2^(-n-2)] x [0,2^(-n-2)]

on a horizontal trunk in the unit disc. The rectangles are disjoint. Within rectangle n, a finite simple serpentine with n*2^(n+2) horizontal rows and increasing vertical levels has exact length n+2^(-n-2). Attach its initial point to the trunk and take its final point as terminal endpoint. Unique tree paths are compatible and individually finite, every path stays in the unit disc, but the root-to-terminal supremum is infinite over n. For each fixed r>0 all sufficiently small hairs lie entirely in their own terminal r-ball and disappear from the trimmed route. Hence compact containment plus compatibility and fixed-r trimmed local finiteness alone cannot rule out arbitrarily long endpoint decorations.

This infinite tree is not a SIRSN: no stationary, similarity-invariant continuum route law or p(r)=p(1)/r certification is provided, and its endpoint configuration accumulates. It falsifies a shortcut, not Aldous's claim. Its finite N=7 realization has 12,313 embedded vertices and36 all-pair prescribed routes; the independent exact checker verifies its geometry and pairwise common subroutes. The infinite conclusion follows from the explicit length formula and the unique-tree-path argument, not from the finite run.

A separate correlation control has P(A=2^k)=3*4^(-k), so E A=3, while a captured local length4^k/k has expectation3*sum_k1/k=infinity. Arrange these local lengths outside radius2^(k-1); every fixed bounded window has finite mean because it sees finitely many locations. Even an integrable capture radius cannot be substituted into a deterministic-window first-moment identity without joint control. This is an abstract local-measure control, not an edge-process/SIRSN construction.

## Reproduction and evidence limits

All five frozen checker programs reproduced their exact stdout receipts, with503,419 exact finite assertions in total. The author verifier also passed all64 public bindings and all4 independently fetched source hashes. Full stdout/stderr streams, including empty stderr files, are preserved in ignored private/replays. AUTHOR_REPLAY_METADATA.json records the program and stream hashes. The old publication-review verifier was inspected for dependency scope but not executed; it invokes previous review work and is not independent evidence for this audit.

The independent geometric checker passed31,893 exact finite assertions, including seven planar hairs, all-pair route compatibility,22 whole-hair Euclidean trimming controls, dyadic constants and100 random-radius truncations. Its full mathematical stream is GEOMETRIC_CONTROL_STREAM.json. These counts certify the executions' limited finite assertions. They are not formal verification of the continuum proof and cannot establish the infinite SIRSN claim.

No mathematical script failed. An initial optional PyMuPDF availability probe failed because that module was absent; existing Poppler was used without installation. One combined source text output was truncated and the critical pages were reread completely in smaller batches. These incidents and corrections are recorded in the baseline and research log. The audit's sealed proof judgment was not revised to fit checker output; the successful replays support reproducibility only.

## Primary references

The exact question is in [Aldous long manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf), PDF50, and [Aldous published paper](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf), PDF38. The published PDF6-10,28-30,35 support the route/setup/major-road distinctions and endpoint gap. [Kahn2016](https://arxiv.org/pdf/1503.03976v3), Theorem3.1 and Theorem5.1/Remark5.1 support the model-specific time and speed mechanisms. Raw source assets and rendered pages remain private and ignored.
