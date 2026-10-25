# NP-completeness of aggregate root-dependent spanning-tree cost

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

6 October 2026 · Version 1.0 · Unrefereed preprint · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

Choosing one network tree can become computationally hard when its cost depends on the starting vertex. This note proves strong NP-completeness for the total cost of all rooted orientations, even with costs drawn from three small integers.

## Original abstract

An undirected spanning tree induces an arborescence at every vertex root. Given an independent arc-cost vector for each root, we prove that deciding whether the sum of the costs of these entire rooted orientations is at most a given threshold is NP-complete, even when every cost belongs to $\{0,1,2\}$. A reduction from satisfiability uses two hubs, variable vertices, and clause vertices. A symmetric cost vector at one hub forces a tree at threshold to encode an assignment with one selected literal per clause; the corresponding clause-root costs test those literals. Uniformly shifting the costs yields the same conclusion for costs in $\{1,2,3\}$. This resolves Problem 1 in Volker Kaibel's November 2018 Oberwolfach workshop contribution, whose report was published in December 2019. Exact finite checks accompany the all-size proof.

## One tree, a cost for every root

Start with a finite connected simple undirected graph with $N\ge1$ vertices. Choose one spanning tree and orient every edge away from a chosen vertex. Do this for every vertex root, keeping the same underlying tree throughout. Each root has its own independently supplied cost for every directed edge, and the objective adds the costs of all edges in all these rooted orientations.

The input explicitly lists all $2N|E|$ nonnegative integer costs in binary, together with an integer threshold. The decision problem asks whether some common tree has aggregate cost at most that threshold. The theorem proves strong NP-completeness already when every cost is in $\{0,1,2\}$. Finding a minimum-cost tree is therefore NP-hard. Adding one to every cost gives strong NP-completeness for the positive alphabet $\{1,2,3\}$, because every tree acquires the same total increment $N(N-1)$.

Orienting toward each root gives an equivalent convention when every input arc-cost pair is transposed. The model charges the entire rooted tree at every root; it does not optimize a different tree for each root or charge only a selected destination path.

## How the reduction works

The reduction starts from satisfiability with at most three literals per clause. Two hub vertices represent the two truth values. Variable vertices attach to hubs, and clause vertices select literals. A symmetric cost table at one hub forces every tree meeting the threshold to contain the hub edge, give each variable exactly one hub attachment, and make every clause vertex a leaf.

The forcing step accounts for every possible spanning tree. If $p$ counts hub–variable edges, $q$ counts clause–variable edges, and $h$ records the hub edge, then the base cost is $p+2q=K+(1-h)+(q-m)$, with $K=2m+n$ and $q\ge m$. Nonnegative costs at the other roots force $h=1$ and $q=m$ at the threshold. Only after this step is the tree interpreted as an assignment.

When the tree is rooted at a clause leaf, its selected variable's edge points toward that variable's chosen hub. The clause-root table charges one precisely when this selected literal is false. Thus a satisfying assignment supplies a tree at the threshold, and a tree at the threshold supplies a satisfying assignment. The graph, every entry of the cost table, and the threshold have polynomial size. The proof handles clause simplification, empty instances, and sparse variable labels explicitly.

## Context and limits

The result answers the whole-orientation objective in Problem 1 of Volker Kaibel's November 2018 Oberwolfach contribution, published in the workshop report in December 2019. The satisfiability machinery is classical, as developed by Cook and Karp. Martin's spanning-tree formulation is also prior work; the note credits the expositions by Conforti, Cornuéjols and Zambelli and by Friesen. Integrality of a formulation's edge projection alone does not settle arbitrary objectives on all its root-orientation variables.

The statement concerns the written finite, explicitly encoded integer-input model. It does not settle Kaibel's neighboring Problem 2 or claim NP membership for arbitrary unencoded real inputs. The false-selected-literal identity applies to the forced structured trees; it is not a formula for the unrestricted optimum in terms of the smallest number of unsatisfied clauses. Historical first discovery and present worldwide open status are not established.

The complete support archive contains the source and exact finite verification material. These checks illustrate and test the construction; the all-size reduction is what proves hardness.

## Research status and contributions

AI tools were used extensively in solving, drafting, literature checking, code generation, verification, and adversarial review. This preprint is unrefereed and has not received conventional human peer review. It is not a formal proof-assistant certificate.

Substantive proof checks, counterexamples, and precise comparisons with prior work are welcome. Authorship and acknowledgments depend on actual research contributions and mutual agreement.

## References

Volker Kaibel, Open Problem: Arborescences and NP-hardness, Oberwolfach Report 50/2018, pp. 3014–3015. [Workshop report](https://doi.org/10.4171/OWR/2018/50).

Richard M. Karp, Reducibility among combinatorial problems, Complexity of Computer Computations (1972), pp. 85–103. [Chapter](https://doi.org/10.1007/978-1-4684-2001-2_9).

Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Extended Formulations in Combinatorial Optimization, revised February 2010, Section 6.1. [Author manuscript](https://www.andrew.cmu.edu/user/gc0v/webpub/ExtFor-Feb2010.pdf).

M. Friesen, Extended Formulations for Higher Order Polytopes in Combinatorial Optimization (2019), Proposition 2. [Dissertation](https://d-nb.info/1219966134/34).

## Paper, source and citation

Read the complete 4-page paper, open it directly, or download the deposited PDF. The complete source and verification archive is available alongside the paper at [the selected Zenodo edition](https://zenodo.org/records/23181280).
