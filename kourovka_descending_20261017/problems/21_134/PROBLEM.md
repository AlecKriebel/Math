# Kourovka Notebook 21.134 — previously known negative answers

Source: official 21st edition, October 2026 update 3, modified 20 October 2026, printed p. 199, zero-based PDF index 198. Proposer: A. V. Vasil'ev. The main file and updates-only file both mark the entire entry solved.

## Complete mathematical statement

For a finite group G define its type to be the function t_G on positive integers given by

    t_G(n) = |{x in G : x^n = 1}|.

(a) If finite groups G,H have identical type and G has trivial solvable radical, must H also have trivial solvable radical? The problem notes that equal type does not generally force both groups to be solvable or both nonsolvable; it refers to 12.37.

(b) If a finite group H has the same type as an almost simple finite group G, must H be isomorphic to G? The statement notes that this recognition is known for a simple source group, by the affirmative answer to Archive 12.39.

There are no degree/character hypotheses. “Almost simple” means S <= G <= Aut(S) for a nonabelian finite simple S. “Type” retains counts for all n, not just the set of element orders. Equivalently it specifies the multiplicity m_G(d) of each element order, because t_G(n)=sum_{d|n}m_G(d) and these relations invert recursively (or by Möbius inversion).

Authoritative statement and known-solution notice:
https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf
https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf

## Prior counterexample addressing both parts

The official notice attributes both negative answers to an example already given by J. G. Thompson. It cites Y. Li and W. Shi, *A note on Thompson problem*, Ricerche di Matematica 74(1) (2025), 559–563, DOI 10.1007/s11587-023-00835-4, and the proposer's letter of 18 May 2026. The article was first published online 16 December 2023; its preprint is arXiv:2303.09460v1, submitted 15 March 2023.

The example consists of the specified maximal subgroups of M_23:

    G = L_3(4).2,        H = 2^4 : A_7.

Use the L_3(4).2 extension occurring as that maximal subgroup; do not interpret the notation as an arbitrary outer involution extension. Li–Shi's ATLAS notation distinguishes this extension. Both groups have order 40320. Li–Shi, Theorem 9, explicitly gives the same element-order counts for them:

| Order d | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Number of elements | 1 | 435 | 2240 | 6300 | 8064 | 6720 | 5760 | 5040 | 5760 |

All other orders occur zero times. Therefore these counts give exactly the same type function for every positive n. These are the counts reported in the primary paper's MAGMA computation, not a newly reproduced computational certificate from this project.

The source G is almost simple and hence has trivial solvable radical; H has the nontrivial normal elementary abelian 2-group 2^4. Thus (a) fails and, since radical triviality is an isomorphism invariant, (b) fails too. This logical scope check does not claim a new construction.

The proposer's contemporary survey, arXiv:2608.12783v2 (9 September 2026), §3, printed pp. 5–6, independently records exactly these two M_23 maximal subgroups as a Thompson example and contrasts their element-order multisets with the still-open character-degree question. This result must not be transferred to 21.135, whose invariant is a character-degree multiset.

Primary sources:

- https://arxiv.org/abs/2303.09460
- https://doi.org/10.1007/s11587-023-00835-4
- https://arxiv.org/abs/2608.12783

Outcome: **already_solved**, both parts. No new mathematical result, publication, or DOI.
