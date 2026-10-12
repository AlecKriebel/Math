# Independent adversarial review: branching and local exploration

Original PR173 head: `eb68ee2ecda39a8ec2748796d716c7a7598b7bc6`. Problem: 30003677 / OWR-15962-003. Family: probabilistic local exploration and continuous-time branching. Audit completed 2026-10-12 UTC. This report uses the exact original scientific inputs, not a later revision, and preserves the substantive first assessment under `first_seal/` unchanged.

## Assessment and strongest verified result

I found no in-scope mathematical falsification of the candidate's theorem. The strongest independently verified result is the following fixed-parameter estimate, with a proved route to the proposed deterministic diagonal schedules:

For each fixed threshold k>d0, path length R, and time T>0,

    limsup_n P(an independent uniform U_n is not type 1 by T)
      <= (1-P(D*>=k))^R + R/(lambda1 T).

The scope is an i.i.d. configuration multigraph degree law with D>=2 almost surely, unbounded support, E[D^2]<infinity, independent uniform one-vertex parity repair, fixed positive rates, degree-only threshold seeds, and one degree-d0 uniformly selected competitor. It does not cover a fixed number of hubs, a prescribed polynomial budget, optimal thresholds, an adversarial graph-dependent competitor, n-dependent rates, arbitrary passage-time laws, or historical priority. In this precise scope, the original claimed existence conclusion follows from the independently proved estimate and the diagonal/resource calculations in the first seal.

No stochastic universal claim is inferred from simulation. The proof is genealogical expectation plus a finite incident-stub cutoff and uniform matching estimates. Finite deterministic controls check separate mechanisms and identify an incorrect alternative, rather than substitute for this proof.

## Complete probabilistic mechanism, with a quantitative cutoff

Let mu=E[D], m=E[D*]=E[D^2]/mu, and nu=m-1. The first seal derives nonexplosion from the expected deaths in every genealogical generation, bounding their total by

    d0 sum_{l>=0} nu^l (lambda2 T)^(l+1)/(l+1)! < infinity.

It then obtains the exact active population and event expectations

    E[A(s)] = d0 exp(lambda2(nu-1)s),
    E[C(T)] = lambda2 d0 integral_0^T exp(lambda2(nu-1)s) ds.

Both are finite. This is noncircular: the generation sum is defined on the entire genealogical tree, and its finite expectation rules out infinitely many events before the population identity is used.

For an immediate-partner revelation construction, also charge the full degrees of seen frontier targets. This gives a combined incident-stub exposure upper bound H with

    E[H] <= (1+m)(mu + R m) + d0 + m E[C(T)] + m E[A(T)].

The selected path vertices contribute mu+Rm, and their fresh off-path neighbors contribute at most m times that amount. The selected ball vertices contribute d0+m E[C(T)]; the seen but uninfected boundary targets contribute m E[A(T)]. A new target's degree mark is independent of whether its incoming active individual has rung by T: that decision uses the individual's ancestry and lifetime, whereas its own offspring mark does not influence that event. Summation by genealogical generation and Tonelli justify both terms. Double-counting between the path and ball only strengthens the upper bound. Markov's inequality gives P(H>M)<=E[H]/M. No third moment, or variance of D*, is required. Merely counting infected vertices' incident stubs would need a deferred-partner construction; it is insufficient for this immediate-partner variant's collision accounting.

Conditional on a typical degree list, the empirical size-biased law Q_n converges in total variation to Q. For any fixed M, a coupling of at most M draws with i.i.d. Q marks fails with probability at most

    ||P_n-P||_TV + M ||Q_n-Q||_TV
      + O(M^2/(L_n-M)) + O(M/N_d0) + O(1/n),

on the M-stub cutoff, where P_n and P are the empirical and limiting uniform-root degree laws. These root laws converge in total variation by the same finite-set argument. The O(M^2/(L_n-M)) term controls matching reuse, collisions, and removal of already exposed stubs; O(M/N_d0) controls an exposed degree-class root; the last includes U=W. The order of limits is essential: choose M for fixed R,T, take n to infinity, then M to infinity. There is no direct assertion that this bound works with arbitrary growing R or T. The diagonal chooses each such parameter triple first and only then its finite-n threshold.

The exposure bound must count incident half-edges, not merely discovered vertices. On the no-collision event, every frontier edge is distinct, so assigning its independent type-2 exponential mark when its first endpoint is infected agrees exactly with static undirected edge-weight FPP. One may reveal incident partners immediately and stop on any repeated vertex/frontier target. This avoids needing a global equivalence involving independent clocks at both ends of an internal edge. The primary paper's deferred half-edge mechanism supplies a standard alternative construction, but the stopped tree argument already suffices here.

Choosing a degree-d0 root first deletes only one vertex and d0 stubs. The class has N_d0/n->P(D=d0)>0, so this deletion and overlap with the independently sampled path are negligible. The auxiliary forward choice uses only revealed matching/order information, leaving the partner's size-biased mark and the type-1 edge time unbiased. D*>=2 ensures a forward stub always exists in the limiting tree. Reversing the found path uses the same type-1 marks on the undirected edges.

The competitor's actual infection ancestors give a type-2 path with the actual sum of type-2 traversal times; therefore its set at T is a subset of the unopposed ball B2(T). A weak path avoiding that ball and of weak total length at most T is safe at every intermediate vertex through T. Induction along the path proves arrival, including earlier arrivals from other weak seeds. This is a sufficient protected-route argument, not a comparison of two final distance fields.

The full fixed-parameter estimate, limsup-to-eventual bound, deterministic diagonal, independent-uniform-vertex identity E[Z_n]=P(U missing), Markov bound, binomial seed counts, and seed-degree tail bounds are all derived in `first_seal/assessment.md`. Every choice of N_j depends only on the law and fixed rates. Increasing N_j to ensure log N_j>=j T_j imposes no incompatible requirement and yields t_n/log n<=1/J(n). The fact that a fixed T_j ball may have an enormous expectation is harmless because T_j is fixed before its eventual n-threshold is selected.

## Repairs, gaps, and status of each route

| Mechanism or claim | Independent status | Exact remaining issue |
| --- | --- | --- |
| Finite-time ball tightness / nonexplosion | Proved by generation sum and finite exposure bound | Original prose could include the noncircular derivation; no mathematical obstruction remains in this family. |
| Empirical size-biased sampling | Proved by finite-set total-variation argument and stub-removal bound | State that the cutoff counts all incident stubs. Weak empirical distribution convergence alone would not suffice. |
| Joint path / degree-conditioned competitor | Proved with degree-class density and cutoff matching | Conditioning is on the preselected degree class; graph- or weight-adversarial choices are outside scope. |
| Parity repair | Proved; resource correction <=D_V+1, moment correction <=(2D_V+1)/n | Independence/uniformity of V is an explicit model assumption. E[D_V]=mu gives a stronger repair bound than the candidate's max argument. |
| Static edge weights / clock mechanism | Exact until stopped collision, which has vanishing probability | Original proof should make this cutoff explicit. A global endpoint-clock equality is not needed or asserted here. |
| Protected-path implication | Proved by infection ancestry and path induction | No gap; ties in deterministic controls are resolved in favor of the competitor. Exponential weights have ties with probability zero. |
| Deterministic diagonal and macroscopic victory | Proved from the fixed-parameter estimate | Existence only: no numerical construction of the eventual N_j or optimal budget. |
| Vertex and half-edge seed resources | Proved by binomial variance and integrable tails | Requires unbounded degree support for every q_j,p_j to be positive. |
| Naive unopposed Voronoi ownership | Falsified by explicit four-vertex control | Blocked as a replacement proof route; final independent distances can miss intermediate blocking. |
| Arbitrary growing-time local coupling | Unsupported and unused | Would require additional quantitative estimates; the diagonal never makes this transfer. |
| Fixed-hub or sharp rate/degree thresholds | Unresolved and outside this theorem | The slowly diverging seed family supplies no such threshold. |
| Novelty or priority | Not assessed | Two primary bodies checked for model/scope only; no exhaustive search or regular-graph theorem audit. |

These are proof expansions and scope restrictions, not a request to treat a central unsupported equivalent claim as established. This family has no remaining central probabilistic gap under the exact candidate assumptions.

## Adversarial controls and boundary laws

`public/controls.py` uses only exact rational finite weights and Python's standard library. It exhausts all 15,625 four-vertex simple graph states where each edge is absent or has each type weight in {1,2}; for T in {1,2,3,4}, it checks 125,000 target/time comparisons. All 5,900 cases with a protected path infect the target weakly by T. Separate controls cover loops, parallel channels, and 3,564 degree-list/threshold/parity cases. These counts describe a finite tested domain; induction proves the general deterministic lemma.

The deliberately wrong ownership rule is detected on vertices s=0, w=1, a=2, v=3. Edges s-a and a-v have weak weight 1; fast weights are 100. Edge w-a has fast weight 1/10 and weak weight 100. Edge w-v has fast weight 3 and weak weight 100. Unopposed weak distance to v is 2, unopposed fast distance is 3, yet fast captures a at 1/10, blocks the weak route, and captures v at 3. The protected-route condition correctly fails because a lies in B2(2).

A concrete counterexample to dropping the minimum-degree assumption has

    P(D=1)=1/2,
    P(D=2m)=2^(-m-1), m>=1.

It still has unbounded support and finite second moment, with mu=5/2 and E[D^2]=25/2. Let a=P(D=1)=1/2 and let m_n denote the number of degree-one vertices, L_n the half-edge total. The number Y_n of vertices in isolated degree-one pairs has conditional expectation

    E[Y_n | degrees] = m_n(m_n-1)/(L_n-1).

For two distinct degree-one stubs i,j, their joint indicators have expectation

    1/(L_n-1) + (m_n-2)(m_n-3)/((L_n-1)(L_n-3)).

Subtracting the square of (m_n-1)/(L_n-1) gives covariance O(1/L_n); hence Var(Y_n | degrees)=O(n) on typical lists. The laws of large numbers and conditional Chebyshev give Y_n/n -> a^2/mu=1/10 in probability. Repair changes at most one degree-one vertex. For k_n>2 and a degree-two competitor, these components contain neither weak seeds nor the competitor. Thus weak occupation cannot tend to 1. This is outside the theorem and demonstrates that its lower degree bound is substantive.

For a separate empirical-moment negative control, a deterministic list with one degree n and n-1 degrees 2 has uniform-root degree converging weakly to the constant 2, but the exceptional hub carries asymptotically one third of all half-edges. Its size-biased distribution therefore does not converge in total variation to the constant 2. A bound based on only the number of exposed vertices also fails: after exposing that hub, a fresh hub half-edge has self-collision probability asymptotically one third. This list violates the required moment convergence; it catches two invalid weakenings of the coupling proof.

Other scope boundaries are immediate: bounded degree support makes the diverging-threshold seed set empty eventually; lambda1=0 prevents any weak growth beyond its vanishing initial fraction. The proved mechanism actually works for any ordering of two fixed positive rates, but its intended application is lambda1<lambda2.

The candidate's even-geometric example is correct: P(D=2m)=2^-m has mu=4, E[D^2]=24, E[D*]=6 and nu=5. The exact size-biased tail at 2j is (j+1)/2^j. The generation calculation gives E[A(T)]=2 exp(4 lambda2 T) and E[C(T)]=(exp(4 lambda2 T)-1)/2 for a degree-two root. This concrete example has even total degree and needs no repair.

## Source access and provenance limits

The [Ahlberg-Deijfen-Janson preprint](https://arxiv.org/pdf/1711.02902) was obtained in full. Complete relevant pages 2, 6, 7 and 15 were read; pages 2, 7 and 15 were rendered and visually inspected. Page 2 verifies the edge-time model, A1-A2, and repair. Section 2 verifies the finite-time size-biased branching coupling. Section 5 discusses growing initial sets and degree-based starts. The [OWR contribution](https://ems.press/content/serial-article-files/46721), printed pages 3442-3443, was read, and page 3442 visually inspected. It describes the same finite-variance setting and the high-degree starting question. The source_record's linked label “OWR Report 57/2019” conflicts with the body header 57/2017.

The downloaded bodies, raw response headers, extracted full text, rendered pages and raw access records remain under `private/` and are excluded from the public allowlist. Their hashes and sanitized access metadata are in the source ledger and complete retained-file manifest. A web screenshot attempt for the EMS page timed out; the independently downloaded PDF and local rendering succeeded. No failed route is treated as evidence of source content. The web connector's ephemeral response bytes were not retained and have no asserted exact-byte hash; the scientific PDF bytes used in local reading/rendering are retained and exactly hashed. This is the explicit access-provenance limit, not a claim of identical web-cache transport bytes.

The regular-graph background article, journal DOI metadata, and wider novelty literature were not consumed or used as mathematical premises. No original readiness/review verdict, other-family file, or root conclusion was read at any stage. There was no Git/index/ref/checkout mutation, package installation, PR action, publication, or external outreach. Team messages reported only this family's own results after the first seal.

Final completion estimate: 100% of the assigned independent branching/local-exploration audit. This percentage concerns this review family, not completion of the broader open problem or historical novelty verification.
