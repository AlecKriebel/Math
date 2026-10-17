# Source-faithful acceptance contract: row 1785 / 10000037

Prepared 14 October 2026 UTC. Source recovery and authored scope clarification only. Zero mathematical passes; no new proof, construction, experiment, or resolution certificate.

## Source identity and remaining quantifier issue

Itai Benjamini, *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013, Open Problem 9.6, printed page 64 / PDF page 64. The complete 115-page manuscript was recovered from the [preserved author-hosted copy](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf). The corresponding [published chapter](https://doi.org/10.1007/978-3-319-02576-6_9) occupies pages 69–84 of LNM 2100; publisher pagination must not be substituted for manuscript pagination.

The problem asks for uniqueness on bounded-degree graphs roughly isometric to Z^d. Its short sentence does not itself specify p, an almost-sure qualifier, or a dimension range. Section 9 opens by specifying the supercritical regime p>p_c. The preceding results concern almost-sure uniqueness. Thus supercritical almost-sure uniqueness is the context-supported reading. An exact later citation explicitly interpreting Problem 9.6 was not located in this bounded recovery.

A separate all-parameter at-most-one formulation is stronger. Treat the following targets separately:

- **Supercritical reading:** for every admissible G and every fixed p with p_c(G)<p≤1, P_p^G(N∞=1)=1.
- **All-parameter normalization:** for every admissible G and every fixed p∈[0,1], P_p^G(N∞≤1)=1. In particular, this also includes p=p_c(G).

Before an attempt is declared a complete answer, identify which target it addresses. The primary context supports the first; the second is a distinct stronger normalization. Do not silently assert that the primary question expressly quantified over all p. Do not silently omit the critical parameter from a claimed resolution of the all-parameter normalization. A theorem only for sufficiently large p, or only p>p_u, is not a full supercritical answer without an additional justified bridge.

These are pointwise assertions for each fixed p. Simultaneous uniqueness at every p in one coupled process is a further assertion and is not imposed by the recovered wording.

## Graph and metric model

Use the source's conventions from pages 5 and 33: G=(V,E) is infinite, connected, countable, undirected and simple. It has no loops or parallel edges. Every vertex has finite degree; the problem additionally requires one finite bound for all vertex degrees of G. The bound may depend on G. Use shortest-path distance with unit edge lengths.

There is **no standing transitivity, quasi-transitivity, Cayley-graph, stationarity, or unimodularity assumption**. Nor is a lattice embedding, planarity, or periodic decoration assumed. No separate amenability hypothesis appears in Problem 9.6. A result for transitive amenable graphs alone is already preceding material, not the requested generalization.

Definition 1.25, page 9, expressly uses the quasi-isometry sense of rough isometry. With H=Z^d, there must be a map f:G→H and 0<C<∞ such that, for all x,y∈G,

C^(-1) d_H(f(x),f(y)) − C ≤ d_G(x,y) ≤ C d_H(f(x),f(y)) + C,

and every z∈H satisfies d_H(f(x),z)<C for some x∈G. Both multiplicative and additive distortion are permitted. The constants are uniform over the entire graph, not chosen separately for points or scales. The map need not be injective, surjective, an edge map, or a graph homomorphism. Additive-only rough isometry is a narrower convention and must not replace this definition. Definition 3.10 on page 29 gives an alternative formulation with two coarse-Lipschitz, approximate-inverse maps.

The lattice has its usual nearest-neighbor graph metric. The short question gives no d≥2 exception. Preserve positive integer dimensions, and explicitly account for d=1 if narrowing the substantive analysis to d≥2. This recovery does not supply a proof for the full rough-isometry-to-Z boundary class. Dimension zero is outside the standing infinite-graph setting. Do not claim a high-dimensional-only theorem settles all dimensions.

## Percolation and probability model

The relevant process is **Bernoulli bond (edge) percolation**, fixed by Section 4.1 and repeated in Theorems 9.2–9.3. All vertices are retained. Each edge is independently open with the same probability p∈[0,1]. An open cluster is a connected component of the spanning subgraph of open edges; N∞ counts its infinite components.

The source defines p_c(G,o)=inf{p:P_p(o belongs to an infinite open cluster)>0}, with root independence for connected G (Definition 4.2 and Exercise 4.3). Site percolation, nonconstant edge probabilities, dependent processes, and random environments are different models unless a valid transfer is supplied. A site theorem cannot be imported as a bond-uniqueness theorem merely from a comparison of critical probabilities.

At-most-one does not demand existence where there is no percolation. Almost-sure uniqueness on the existence event and a positive probability of existence are not to be interchanged without explaining the probabilistic implication. In this nontransitive graph class, do not import the transitive 0/1/∞ cluster-count theorem or transitive uniqueness-monotonicity theorem without verifying their assumptions.

## Prior-work gates and evidence standard

The source already gives lattice uniqueness (Theorem 9.2) and transitive amenable uniqueness (Theorem 9.3). Its neighboring Conjecture 9.11 proposes rough-isometry invariance of p_c<p_u; it does not establish such invariance.

A proposed shortcut via general rough-isometry invariance is not authenticated by the inspected sources. The cited Benjamini–Schramm hyperbolic-plane paper treats transitive planar hyperbolic graphs; its inspected statements do not establish the claimed blanket theorem. Lyons–Peres Exercise 7.13 concerns preservation of p_u<1 for **quasi-transitive** graphs. That is neither invariance of the numerical threshold nor uniqueness at every supercritical parameter on arbitrary bounded-degree graphs.

Teixeira's [Theorem 1.4](https://arxiv.org/abs/1409.5923), Candellero–Teixeira's [Theorem 1.8](https://arxiv.org/abs/1507.07765), and Hutchcroft–Tointon's [Theorem 1.8](https://doi.org/10.4171/JEMS/1453) provide high-density uniqueness under their respective geometric/model hypotheses. Their inspected statements do not say that their p* equals p_c. Treat any application and extension beyond their stated range as a separate obligation. The existence of a nontrivial uniqueness phase is not the requested full-supercritical conclusion.

A positive result must cover the chosen parameter range and every graph in the source class with complete, checkable reasoning. A negative result must identify an admissible infinite graph, verify its degree and rough-isometry conditions, and establish nonuniqueness with the required positive probability at an appropriate p. Finite simulations, a proposed route, an unverified citation, or a result after adding transitivity do not settle this row.

No complete exact-target resolution was authenticated in the bounded literature screen. This is not a certificate of current openness or novelty. This contract is an authored scope report; it reproduces no source documents.
