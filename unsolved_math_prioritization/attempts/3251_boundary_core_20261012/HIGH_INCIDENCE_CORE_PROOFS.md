Editorial note: Complete authored proof or audit prose is preserved below. Only operational artifact identities, byte counts, locations and obsolete replay directions have been replaced; all mathematical arguments, finite scopes and limitations remain. The public manifest identifies the actual distributed edition.

# Derived high-incidence-core restrictions

## Scope and dependency

This is a separately sealed mathematical addendum to the unchanged clique-boundary-flexibility packet. It adds no finite enumeration claim and makes no novelty claim. The unrestricted odd-hole-free division conjecture remains unresolved.

The dependency is the separately frozen [clique-boundary-flexibility proof](BOUNDARY_EXTENSION_PROOFS.md). The original external pin, manifest and proof identities were verified before this edition was prepared. We use its Lemma 1, which solves incidence-at-most-two mixed hypergraph constraints, and Theorem 3, which extends every admissible clique-boundary coloring when all outside maximum-clique incidences are at most two.

All graphs here are finite and simple with k=omega(G)>=3. A division has no monochromatic maximum k-clique. Let

X = {v in V(G): v belongs to at least three distinct maximum cliques of G}.

Maximum cliques are counted in G itself. The incidence threshold is not recomputed inside G[X]. None of the conclusions below needs odd-hole-freeness.

## 1. Prescribed-color extension criterion

**Proposition A.** Let P contain X. Suppose a prescribed two-coloring of P has no monochromatic (k-1)-clique. Then that coloring extends to a division of G.

**Proof.** Discard each maximum clique already seeing both prescribed colors. Any remaining maximum clique meets P in a monochromatic clique, of size at most k-2 by hypothesis. Delete its vertices in P, leaving a residual edge of size at least two. Give this edge demand B if its original clique missed P, and otherwise the one-sided demand forbidding the prescribed color that it saw. Every residual vertex is outside P, hence outside X, and appears in at most two residual constraints. Every size-two residual edge is one-sided: its original clique had k>=3 vertices, so some prescribed vertex was deleted. Thus no pure odd-cycle component can have demand B on every edge. Lemma 1 of the frozen packet gives a coloring of all residual vertices satisfying every constraint. Combining this with the prescribed coloring divides G. □

In particular, if omega(G[P])<=k-2, every coloring of P extends. This variant imposes no requirement that P be a clique and permits P to contain arbitrarily many vertices.

## 2. Necessary structure of X in every indivisible graph

**Corollary B.** If G has no division, then all of the following hold:

1. omega(G[X])>=k-1.
2. X is not a clique, so it contains two nonadjacent vertices of maximum-clique incidence at least three.
3. chi(G[X])>=2k-3.
4. |X|>=2k-2.

**Proof.** If omega(G[X])<=k-2, the special case P=X of Proposition A supplies a division, proving (1).

If X were a clique, an admissible coloring of X would extend by Theorem 3 of the frozen packet. Such a coloring always exists: color arbitrarily if |X|<k, and choose a mixed coloring if |X|=k. This proves (2).

If G[X] had a proper coloring with at most 2k-4 colors, group those color classes into two groups of at most k-2 classes each. Each resulting color induces clique number at most k-2. Proposition A again extends, proving (3).

For (4), suppose first that |X|<=2k-4. Partition X into two sets of at most k-2 vertices each and apply Proposition A. The only additional order to rule out is |X|=2k-3. By (2), select a nonedge ab in G[X]. Put a and b in a set A of size k-1 and put the remaining k-2 vertices in B. This is possible because k>=3 and |X|>=k-1. The set A is not a clique, so its clique number is at most k-2; B also has clique number at most k-2 by its size. Coloring A and B differently satisfies Proposition A, again giving a division. Therefore |X|>=2k-2. □

The fourth statement does not follow merely by combining the first three numerical inequalities; its proof uses the nonedge supplied by the full clique-boundary theorem.

For the unresolved k=4 frontier, every indivisible graph therefore has at least six vertices belonging to at least three maximum cliques. These high-incidence vertices induce a graph of chromatic number at least five and clique number at least three, and they are not all pairwise adjacent. These are necessary conditions only.

## 3. A stronger clique statement under induced minimality

Call G minimal indivisible if G itself has no division but every proper nonedgeless induced subgraph has a division at its own clique number.

**Corollary C.** In a minimal indivisible graph with k>=3, omega(G[X])=k. In particular, there is a maximum clique all of whose vertices belong to at least three maximum cliques of G.

**Proof.** If X=V(G), the statement is immediate. Suppose X is proper and, toward a contradiction, omega(G[X])<=k-1. If G[X] is edgeless, give X any coloring; both color classes have clique number at most one, and one<=k-2. If G[X] has an edge, induced minimality gives a division of G[X] at its own clique number t<=k-1. Each color class then has clique number at most t-1<=k-2. In both cases Proposition A extends this coloring to a division of G, contradiction. Hence omega(G[X])=k. □

Corollary C does not assert that X is a clique; Corollary B says the opposite. It asserts that X contains at least one maximum clique. Nor does this establish compatibility of arbitrary separator sides. All conclusions are scoped structural consequences of the frozen mixed-constraint and boundary-extension proofs.
