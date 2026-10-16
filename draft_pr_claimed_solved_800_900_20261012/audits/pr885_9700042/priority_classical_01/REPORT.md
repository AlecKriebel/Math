# Independent classical priority audit — PR885 / PID9700042

Completed 2026-10-15. Scope: exact canonical asymptotic only; no shared research, Git, classification, PR, DOI or publication state was changed. Initial assessment was frozen independently before other priority reports were read. No other new priority-family report was read; the parent later requested a focused check of BGT's half-penalty implication.

## Decision

**A full old-input corollary has been found.** The exact flow asymptotic follows from a larger bad-sequence bound already evaluated in Basdevant–Gouéré–Théret (2021 preprint; 2022 publication), together with classical strict Bernoulli-chain shape. The complete checkable model/event inclusion is in [BGT_FULL_COROLLARY.md](BGT_FULL_COROLLARY.md). The parent should read that derivation and the retained actual BGT source before promoting the priority conclusion.

This is a stronger finding than “similar method exists,” but it is not a claim that BGT explicitly announced a solution of Aldous's named conjecture, nor a certificate of who first noticed this consequence. No such explicit historical announcement was located. Neither novelty nor continued openness is certified.

## Exact target and source authentication

The target is the full north/east nearest-neighbor Bernoulli(p) edge-capacity-one square, with the canonical source and sink boundary arcs, allowing shared vertices among edge-disjoint flow paths. It asks for 1−v(p)~sqrt(2(1−p)) as p↑1. The source-premised fixed-p deterministic L1 limit is retained. The independently fetched Aldous HTML is exactly 3576 bytes with SHA256 1c3078bb05b25554b7ab7bc12e6d8567b777407b6c6ad24fecfc89715088a301. Its 2004 conjecture history and heuristic limiting gap are source evidence, not present-day openness evidence. No heuristic scaling assertion is used as a theorem. [Primary page](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html).

## Decisive mapping

Put q=1−p. The exact dual deficit is D_N=max(K−B), where K counts marked forward edges and B backward steps, and g(q)=lim E D_N/(2N)=1−v(1−q). Group the two outgoing marks at each site into iid Y-site marks of probability r=1−(1−q)². Strict increasing Y-chains have shape σ_r=2sqrt(r)/(1+sqrt(r)); every such chain inside [0,N)² can traverse a marked outgoing edge, so D_N≥S_r(N,N).

For the upper bound take n=N+1. List all visited Y-open sites except the target endpoint, keeping the origin indicator I_0 separately. Apply exactly the monotone extraction in BGT §2.5. With Q extracted blocks and discarded counts ℓ_k, K≤p+I_0 and S_r(n,n)≥Q−1+I_0 while p=Q−1+Σℓ_k. Therefore D_N−S_r(n,n)≤Σℓ_k−B. The geometric quantity C in BGT's (19)/Lemma19 uses the sum of individual negative other-coordinate increments and satisfies C≤2B. An excess ηn sqrt(r) consequently implies C<2Σℓ_k−2ηn sqrt(r), stronger than bond Lemma19 item5 with m=0. The remaining conditions hold; item4 follows from target segment optimality B_k≤K_k≤ℓ_k+1, which is stronger than its allowance 2(ℓ_k+1).

The m=0 summand of published (33) asks only for distinct open sites, weighted r^p; it requires no doubly-open data and no ordinary-FPP geodesic. Its already evaluated sum tends to zero at fixed sufficiently small q. Hence g(q) lies between σ_r/2 and σ_r/2+ηsqrt(r)/2. Taking q↓0 and η↓0 gives the entire exact target. This reuses the published counting estimate without altering its central comparison or recomputing it for a new penalty. Boundary/origin details and each deterministic predicate are supplied in the full derivation.

[BGT primary preprint](https://arxiv.org/abs/2106.12266), [journal DOI](https://doi.org/10.1214/22-AAP1795).

## Failed direct mapping is preserved

The literal ordinary-FPP theorem alone is insufficient. On a common path, ordinary deficit is K_f+K_b−2B whereas target deficit is K_f−B; their difference is B−K_b≥0. A matching numerical coefficient cannot repair this one-sided mismatch. A potential transform creates negative forward weights, outside ordinary nonnegative FPP. Simple site relabeling also leaves the penalty issue. [BGT_MODEL_MAP.md](BGT_MODEL_MAP.md) preserves these failures and records why the larger published event, rather than a false model identity, resolves them.

## Other verified classical facts and exact limits

| Route | Verified result or mismatch | Scope |
|---|---|---|
| Strict Bernoulli Hammersley | The exact strict-chain shape gives σ_r and the canonical previously reported lower formula sqrt(1−p²)/(1+sqrt(1−p²)). | Exact target lower bound; BGT event inclusion supplies matching upper bound. |
| Greedy animals/paths | Martin's growth bound implies O(sqrt(q)) target deficit and O(sqrt(q)N) optimal-path marks/backtracking by a complete site grouping and length calculation. | Sharp coefficient absent from that bound alone. Full derivation: [GREEDY_ORDER_COROLLARY.md](GREEDY_ORDER_COROLLARY.md). |
| Martin directed shape | A directional-boundary asymptotic for monotone paths with fixed weight law. | The direction parameter and absence of backward paths prevent a direct target application. |
| Grimmett–Kesten flow duality | Undirected left/right rectangle flows relate to ordinary FPP. | Different directions and boundary model; no false substitution into target. |
| Grimmett–Suen/Welsh networks | Complete directed graphs, complete networks and branching trees. | Different graph families. |
| Broken-line process | Geometric/exponential oriented LPP with explicit shape and concentration. | Classical method context, not an asymmetric Bernoulli target theorem. |

The primary strict-chain theorem is available in [Basdevant–Enriquez–Gerin–Gouéré 2016, Theorem1.1](https://alea.impa.br/articles/v13/13-02.pdf), which credits Seppäläinen 1997/1998. The original Seppäläinen publisher bodies were not accessible in this run; this audit does not pretend otherwise. The retained primary later theorem is sufficient for the corollary above.

## Ingredient credit and claim scope

The current C4 chain input is classical: the actual Deuschel–Zeitouni introduction and Theorem2 give constant 2 and a positive upper-tail rate. Its Poisson use is an elementary consequence. The original BK1985 Theorem3.3 and finite-many path Corollary3.10 were checked in the actual article; van den Berg–Jonasson2011 pp.2–3 independently restate the required product theorem and witness definitions. Their fixed-size Theorem1.2 is not the input. These are ingredient credits, not by themselves the full interchange argument. [DZ primary PDF](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf), [BK1985 DOI](https://doi.org/10.2307/3213860), [primary-author restatement](https://arxiv.org/abs/1105.3862).

The qualitative square-root upper order and sparse-path control should not be advertised as new. More materially, once the BGT event inclusion is accepted, the sharp asymptotic and hence the weaker e/2 asymptotic upper estimate are already old-input corollaries. The specific C1 finite count and C4 BK–Poisson proof can be different proofs; their precise originality has not been established by this audit. Distinguish an alternative proof, an explicit identification of an old consequence, and a new theorem.

## Remaining gaps and nonclaims

The positive full-corollary finding uses available actual primary bodies; it does not depend on the inaccessible Sidoravicius–Vares–Surgailis1999 paper. That paper's publisher page gives only an abstract and the attempted PDF returned subscription HTML. Aldous–Diaconis1995 repository requests returned empty HTTP202 responses. Original Seppäläinen PDF routes returned HTML challenges. Those gaps prevent an exhaustive older-history review, and no absence conclusion is drawn from them.

A source-precision correction was made after the parent caught an initial net-negative-part transcription: the source uses the sum of individual negative parts. Actual PDFp16 was re-viewed at higher resolution; the same C≤2B proof applies to the correct stronger quantity. The correction is recorded candidly in the full derivation and research log.

No whole BGT proof certification, formal verification, earliest-discoverer determination, exhaustive bibliography, or current-openness certificate is claimed. The parent must adversarially verify the event inclusion before using it to reframe the result. No outside individual was contacted; no outreach was prepared.

## Artifacts and completion estimate

SEARCH_LOG.json records the exact query strings, UTC date, ordered search batches, follow-up mechanisms and limitations. SOURCE_LEDGER.json distinguishes primary metadata, body reads, visual checks and missing bodies, with actual HTTP/byte/hash records. All source bodies and renders are private and excluded from PUBLIC_MANIFEST.json. Only explicitly listed authored artifacts are eligible for parent review/publication; there is no recursive publication permission.

Completion estimate: **100% of this assigned classical priority/model-mapping audit**. Historical first notice and broader priority remain unresolved; that uncertainty is explicit rather than hidden behind the completion estimate.
