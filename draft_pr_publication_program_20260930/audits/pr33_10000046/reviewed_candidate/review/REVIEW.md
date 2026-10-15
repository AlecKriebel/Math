# Independent review: random-walk coupling, 10000046

**Verdict: PASS for the unresolved partial and qualified source-status report.** The finite-transport proposition and elementary bounds are correct. The combined target remains unresolved because no three-dimensional construction or obstruction is established. This review does not certify the complete proof of the cited four-dimensional preprint.

Reviewed on 2026-09-30 by GPT-6 Astra at xhigh reasoning. Frozen PARTIAL.md SHA-256:

b5f326fcff5e86cee87c4b1c6db9c9633ee9b88efedda74976e1f7c63ebd9cfa

No correction to the frozen artifact is required. This is an independent adversarial AI review, not peer review or formal verification.

## 1. Original question and conventions

I read the original archived author PDF, including its introductory conventions and the context around Open Problem 12.33, and visually checked printed/PDF page 104. It asks for simple random walks on the three- or four-dimensional lattice, initially distance ten apart, with a coupling giving positive probability of nonintersecting paths. The notes define graph distance as shortest-path length on page 5; on the nearest-neighbor lattice this is the \(\ell^1\) distance used in the artifact. The document is dated October 30, 2013. The current university URL returns 404; the preserved archived PDF has the hash in the source manifest. [Archived author notes](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf)

The event is disjointness of complete vertex ranges, including both starting vertices:
\[
X_i\ne Y_j\quad\hbox{for all }i,j\ge0.
\]
Requiring only \(X_n\ne Y_n\) does not answer this question. Each complete marginal path law must be simple random walk; checking one-time marginals alone is insufficient. The question places no Markovian or co-adapted restriction on the joint law.

The artifact correctly seeks positive probability. Probability one is impossible even under unrestricted coupling, since the first walk has a fixed positive probability of visiting the second walk's deterministic starting vertex. No assumption about conditional laws in the joint filtration is needed for this upper obstruction.

## 2. Credited four-dimensional result and its audit boundary

Benjamini–Kozma's December 2024 preprint explicitly states the positive four-dimensional theorem on page 2, leaves the three-dimensional case unresolved on page 1, and defines intersection at different times in its introduction. Section 1.2 includes time zero in the trace. It uses Hall matching and a multiscale construction and separately asks whether a Markovian coupling is possible. Thus the preprint is directly relevant prior progress and does not settle a stronger Markovian variant. [Coupled but distant, version 1](https://arxiv.org/abs/2412.16600v1)

The introduction informally describes neighboring starting vertices. The proof of the theorem on pages 17–18 instead begins with independent walks from \(0\) and \(x\) to a sufficiently large sphere. No neighboring-site restriction on \(x\) is imposed in the induction. This supports the artifact's carefully stated intended scope for a fixed nonzero displacement, including distance ten. This is source-scope verification, not a new transfer proof obtained by conditioning or splicing an arbitrary neighboring-site coupling. Such a splice would require checking the full marginal laws and avoidance of all prefix vertices.

The initial nonintersection estimate cites Lawler explicitly for the neighboring case, without expanding the general fixed-\(x\) extension there. This belongs to the full proof-audit boundary already stated in the package; I do not claim to have independently verified every estimate or that extension from first principles.

I inspected the rendered paper and the TeX for the reported inconsistencies. Lemma 8 literally says that the events \(E_i\) occur with a probability close to one although its right-hand side depends on their small probabilities. Taking both events empty demonstrates the literal statement cannot be correct. The induction's first-step bound prints \(Cn_1^6\), although the preceding exceptional-event estimate has order \(n_1^{-6}\). There are related event-complement and inequality-direction inconsistencies in the final induction. Merely silently changing two symbols would not constitute a complete repair audit. The artifact explicitly does not claim such an audit, and this qualification must remain with any description of the four-dimensional prior result.

The currently available arXiv record still lists the 2024 version. A bounded additional search did not locate a three-dimensional solution. The September 2026 Shi–Liu–Li–Li–Deng preprint studies numerical intersection exponents for independent walks and related moments; its stated scope does not establish an unrestricted avoidance coupling. This is a scope check, not an independent audit of its numerical results. [Intersection Exponents of Simple Random Walks in Two and Three Dimensions](https://arxiv.org/abs/2609.25968)

## 3. Finite matching and infinite compactness

The proposition in the artifact is correct.

There are \(L_N=(2d)^N\) labeled increment sequences of length \(N\) on either side, each having probability \(1/L_N\). Different paths that happen to have the same range are still different equally likely outcomes. After multiplying a finite coupling matrix by \(L_N\), its rows and columns sum to one. The Birkhoff decomposition makes its allowed-edge mass at most the largest allowed-edge count in a permutation matrix. A maximum matching can be completed to a permutation; a permutation with more allowed edges would contradict maximality of that matching. Therefore the exact finite optimum is \(M_N/L_N\).

The Hall-deficiency formula is also correct:
\[
M_N=L_N-\max_{S\subseteq\mathcal P_N(x)}
          (|S|-|\mathcal N(S)|).
\]
The empty set ensures the maximum deficiency is nonnegative. Neighborhood here means being disjoint from at least one path in the selected set, as the artifact states.

For the infinite statement, increment path space is a compact metrizable product of a finite alphabet. The set of probability measures with the prescribed two marginals is weakly compact. Every finite optimizer extends to such a measure by sampling independent uniform tails conditionally on the two prefixes; this preserves both entire simple-random-walk marginal laws.

Each finite avoidance event \(R_k\) is a clopen cylinder event. For an optimizer at horizon \(N\ge k\), its mass on \(R_k\) is at least \(a_N\). A weak subsequential limit consequently has mass at least \(\inf_Na_N\) on every \(R_k\). Continuity from above gives that bound on their intersection, the infinite avoidance event. Conversely every infinite coupling has mass at most \(a_N\) on full avoidance for every \(N\). This establishes the equality and, in particular, attainment of the optimal infinite mass.

This argument does not presuppose that the different finite optimizers are projectively consistent. Extension followed by compactness is exactly what addresses that issue. Nor does it interchange a supremum and a limit without justification.

The formula is a complete reformulation, not an evaluation of the unknown limit. Finite certificates give upper bounds on that limit; positive values at every finite horizon would still not provide a strictly positive infimum.

## 4. Elementary controls and remaining gap

For synchronous translation by \(v=y-x\), the range of a length-\(N\) walk cannot contain two vertices differing by \(v\) when \(N<\|v\|_1=10\). The maximum distance between two vertices along one such path is at most \(N\), not \(2N\). Therefore \(a_N=1\) for \(N\le9\), exactly as stated.

The same translation coupling fails almost surely over infinite time. Choose a fixed ten-step increment word summing to \(v\). Disjoint blocks of ten independent increments equal that word independently with probability \((2d)^{-10}>0\). Almost surely at least one, indeed infinitely many, blocks do so. Such a block gives \(X_{10k+10}=Y_{10k}\). In contrast, simultaneous collision never occurs because the displacement at equal times stays equal to \(v\). The artifact uses this correctly as a failed coupling, not as a universal obstruction.

For every coupling,
\[
\alpha(x,y)\le1-\mathbb P_x(T_y<\infty)<1.
\]
The strict inequality follows from a single prescribed shortest path having positive probability. If the coordinate distances are \(a_i\) with sum ten, a visit by time ten must occur at exactly time ten and follow a shortest path. Counting the orderings of its coordinate steps gives
\[
\mathbb P_x(T_y\le10)=
  \frac{10!}{\prod_i a_i!}(2d)^{-10}.
\]
The formula handles zero coordinates and either sign of each displacement.

The remaining three-dimensional question is exactly whether the limiting optimal finite avoidance mass is positive. Neither the transport reduction, the short-horizon perfect matchings, the hitting upper bounds, nor independent-walk exponent estimates decide this.

As a separate illustration of the logical limitation, in one dimension every finite horizon has some disjoint pairs of positive probability, while recurrence forces \(\alpha=0\): the first walk eventually visits the other starting vertex under every coupling.

## 5. Independent exact checks

The author checker was replayed in a separate directory, and its verification receipt reproduced byte for byte.

The independent checker takes a different computational route. It groups paths by identical vertex ranges while retaining their integer multiplicities, solves the resulting capacitated transport problem by a layered max-flow algorithm, reconstructs a matching of individually labeled paths, and verifies a minimum weighted vertex cover. It completes the matching to a permutation and checks the exact uniform marginal on every labeled path. For the smallest cases it also enumerates every Hall subset directly.

All **665 independent exact assertions pass**, covering:

- 28 matching/cover cases, including all 12 author cases with identical results
- One-dimensional controls through horizon ten, non-axis distance-two starts in dimensions two and three, and time-zero collision controls
- 352 actual distance-ten shortest-path counts in dimensions three and four, checked against unrestricted random-walk endpoint recursion
- Signed non-axis displacement and cross-time collision examples

For example, the two-step optimum from displacement \((1,1)\) in dimension two is \(7/8\), and from \((1,1,0)\) in dimension three is \(17/18\). For a one-dimensional displacement of ten at horizon ten, the matching and cover both have size 1023 out of 1024. These are finite diagnostic results, not evidence of a uniform infinite-horizon lower bound.

The four review deliverables are REVIEW.md, review_summary.json, independent_checks.py, and independent_results.json. Reproduce the independent receipt with:

    python independent_checks.py > independent_results.json

The review source images and the author's replay directory are not publication deliverables.

## 6. Disposition

The package is suitable as a reviewed unresolved attempt with credited, qualified four-dimensional literature progress. The three-dimensional target and thus the combined target must remain unresolved. No novelty claim, full four-dimensional proof certificate, or Markovian-coupling result is supported or requested.
