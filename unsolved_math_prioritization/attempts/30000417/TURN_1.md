# Turn 1: exact finite reduction and source-normalized controls

Problem 30000417 / OWR-1189-007. The original floor conjecture remains unresolved.

## 1. Scope

The original Kohl contribution in OWR 7/2006, pp. 414–417, Conjecture 2 on p. 416, concerns n>=3 and integer d>=1:

    chi_list^(d,d)(P_n) = floor(3d(1−1/n)) + 1.

The catalog's ceiling is a transcription error. Lists are arbitrary finite sets of natural numbers. Chosen labels must differ by at least d at path distances 1 and 2. The parameter is list cardinality, not span. Thus the problem is also initial-interval T-list coloring of the square of a path, with forbidden differences 0,...,d−1. Lists need not themselves be intervals. Translating all labels by a common integer does not change any condition.

Kohl's 2006 dissertation, printed pp. 100–102, records the same conjectural upper bound, some small cases, and proofs for lists sharing the global minimum/maximum or lists of consecutive integers. Those established restricted-list results do not prove the arbitrary-list case. The original report states the matching lower bound as Theorem 6. No complete later resolution was found by the primary-literature gate; this does not certify openness or novelty.

## 2. Gap-compression lemma

Fix positive integers n,d,k, and a k-list assignment L_1,...,L_n. Let the union of its labels be a_1<...<a_M, so M<=nk. Define

    b_1=1,
    b_{j+1}=b_j+min(d,a_{j+1}−a_j).

Replace each a_j by b_j in every list. This is an injective order-preserving map, so all list cardinalities and intersections are retained. For any i<j, it preserves the truth of

    a_j−a_i >= d.

Proof: if the original difference is <d, every intervening positive gap is <d, so none is changed and the difference is identical. If the original difference is >=d, then either some intervening gap is >=d, in which case its compressed size d alone suffices, or every gap is <d, in which case the whole sum is unchanged. This proves both directions, including the equality boundary.

Consequently every valid labeling of one instance corresponds bijectively to a valid labeling of the compressed instance. In particular, a counterexample exists for fixed n,d,k if and only if one exists with every label in

    {1,...,1+d(nk−1)}.                                      (1)

This is a finite *exact* reduction for fixed parameters. It does not bound n or d and does not turn a bounded search into a proof of the conjecture. The lemma works for any graph with the single separation d, not just a squared path. One must not rank-compress all gaps to 1: that can change a formerly sufficient distance into a forbidden one.

## 3. Exact reachable-pair certificate

For a given list assignment and n>=2, define

    R_2={(a,b) in L_1 x L_2 : |a−b|>=d}.

For i>=3 let

    R_i={(b,c) in L_{i−1} x L_i : |b−c|>=d
           and some a has (a,b) in R_{i−1} and |a−c|>=d}.

Then R_i is exactly the set of possible last two labels of valid labelings of the first i vertices. Induct on i. The base enforces the sole first edge. Appending c creates precisely the two new constraints to the previous two vertices; all earlier constraints are already enforced. Conversely, every valid prefix gives the displayed predecessor. Thus R_n is empty exactly when the assignment is impossible, and predecessor pointers recover a labeling whenever it is nonempty.

There are at most k² states per layer and a direct implementation uses O(nk³) comparisons. A complete table of the R_i can be checked by recomputing every transition, so an empty final table supplies an exact finite obstruction certificate. This is an explicit reconstruction of the standard path dynamic-programming idea, consistent with the algorithms described in Kohl–Schreyer–Tuza–Voigt (2005); no algorithmic novelty is claimed.

Combining this with (1) gives a terminating, finite decision procedure for each fixed (n,d,k). It does not assert that exhaustive search at that bound is practical.

## 4. Exact boundary families, with credit

For d=1 and n>=3, the answer is 3. In path order, each new vertex has only its preceding one or two labels forbidden, so arbitrary 3-element lists work. Three consecutive vertices form a triangle in the square of the path; identical two-element lists on them obstruct 2. This agrees with the original floor formula. The same calculation at n=4 makes the catalog ceiling version equal to 4, proving the transcription is material but not settling the original problem.

For n=3 and any d>=1, the answer is 2d+1. To label the triangle from lists of that size, choose the smallest label in the union of the three lists and assign it to a vertex containing it. In every other list at most d labels are then forbidden: no remaining label is below the chosen global minimum, and the forbidden interval is its next d integer positions. Choose the new global minimum among the remaining two lists and repeat; the last list retains at least one label. All three pairwise separations hold. Conversely, three pairwise d-separated integers require span at least 2d, so three identical lists {1,...,2d} are impossible. These are standard/previously recorded special cases, also compatible with the source's exact star values; no novelty is claimed.

Similarly n=1 has value 1 and n=2 has value d+1. The latter follows by the same global-minimum argument and identical d-element obstruction lists. This explains why extending the floor conjecture to n=2 would be unjustified. If d=0 is allowed by the definition, every nonempty list works and the value is 1.

## 5. Experiments and remaining gap

The standard-library verifier cross-checks reachable-pair feasibility against full tuple enumeration, validates compression including equality/gapped-label controls, and checks the explicit boundary-family constructions. A separate deterministic-seed C++ local search tested 2,800,000 proposed list assignments at the conjectured cardinality over fourteen (n,d) choices. It found no obstruction. This local search is nonexhaustive, even within its bounded palettes, and gives no universal upper bound. Its output is preserved only as an experimental receipt.

The new useful reduction is that an obstruction at fixed parameters has an explicit finite alphabet bound and a short exact transition certificate. The unresolved step is an all-n, all-d argument that arbitrary lists of size floor(3d(1−1/n))+1 admit a labeling, or a genuinely impossible assignment at that cardinality. Known interval/common-extremum results and the d=1 or n=3 families do not cover that step.

### Primary references

- A. Kohl, Some notes on L(d,s)-list labellings of trees and cacti, OWR 7/2006, pp. 414–417: https://ems.press/content/serial-article-files/46037?nt=1
- A. Kohl, Knotenfärbungen mit Abstandsbedingungen, dissertation (2006), especially printed pp. 87–102 and Conjecture 4.2: https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf
- A. Kohl, J. Schreyer, Zs. Tuza and M. Voigt, List version of L(d,s)-labelings, Theoretical Computer Science 349 (2005), 92–98: https://doi.org/10.1016/j.tcs.2005.09.032
