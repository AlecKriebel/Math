# 30004047: final five-turn partial result

**Proposed original disposition: unsolved, 5/5 substantive author turns. Independent review pending.**

The exact bundled question asks whether the mono-constrained function phi satisfies phi(x,x)>=1/2 for x>1/3, and more generally whether x+ky>1 and kx+y>=1 imply phi(x,y)>=1/k for every integer k>=1. Both parts remain unresolved here. The function is a universal guarantee over all finite graphs, with only the two forward degree conditions and distinct reached vertices counted.

The adjacent completed psi-symmetry target 30004048 has two additional reverse degree conditions and is a different problem. Its publication in PR364 is credited as related context, not a previous attempt of this target or a theorem that resolves phi's thresholds.

## Proved scopes

1. **Complete-uniform middle templates.** If C=[n], B consists of all r-subsets, and B--C uses membership, the fixed-template optimum is h/n, where h is the smallest integer with binomial(h,r)>=ceil(x binomial(n,r)). The full source integer-k implication holds for all first parts over this family. No universal reduction to the family is claimed.
2. **Rank-two weighted first incidence.** If every middle vertex meets at most two positive-weight A-types, below-half reach forces x<=2/5 and, if x>1/3, y<=1/4. The strict endpoints and the 14-vertex sharp control are explicit. This proves the diagonal source assertion in that restricted class.
3. **Cardinality-sensitive maximal-type bounds.** For n equally weighted first vertices, r=floor((n-1)/k) and y>1/(k+1), a putative below-1/k example has at most k-1 distinct maximal r-types and satisfies the exact charge inequalities in TURN_3.md.
4. **The symmetric threshold through |A|<=5k.** For all k>=2 and x,y>1/(k+1), the original conclusion holds when the ordinary first part has at most 5k vertices. The final extra rank uses pairwise-union compatibility, an elementary triple-family classification and explicit charges. In particular a diagonal half-reach counterexample needs at least eleven first vertices. This is not a bound on the size of all potential counterexamples.
5. **Disjoint-maximal/laminar families.** The full asymmetric integer-k implication holds, without a size bound, when the maximal nonempty A-neighborhoods of middle vertices are pairwise disjoint. Laminar families are included. A quantitative middle-deletion stability theorem states the exact degree losses and strict/weak inequalities.

These are restricted positive theorems, with standard finite LP and source machinery credited and no historical novelty claim. The proofs use weighted extensions only where their hypotheses explicitly permit them; the finite-size theorem keeps A equally weighted.

## Failed mechanisms and exact gap

- A 396-vertex strictly diagonal-admissible graph has no two-vertex C-cover of A, even though its maximum reach is 9/11. Thus a small integral covering certificate is not necessary.
- The nine-vertex first-incidence relaxation in turn 3 attains the charge bound but cannot support the required C-degrees. It is not a tripartite counterexample.
- Union/intersection replacement preserves first degrees, but a specific crossing pair in the 396-vertex graph cannot be uncrossed locally while maintaining positive C-degree and nonincreasing maximum reach with all other edges fixed. It does not rule out arbitrary global rearrangements.

Arbitrary large overlapping higher-rank neighborhoods remain unhandled. No support reduction, general laminarization, universal proof or original counterexample is supplied. The fifth turn is final; review is not a sixth author search.

## Reproducibility and source history

The five deterministic author checkers replay exactly and contain 12,967,236 finite assertions: 377,063; 20,643; 12,105,108; 164,794; 299,628. These control algebra, finite families, graph incidence and exact charge formulas. They do not replace the written universal arguments. The exploratory floating-point LP probe used during turn 4 was replaced by explicit rational charges and is not a proof dependency or public certificate.

Run `python verify_packet.py` from this directory; optionally add `--source-dir PATH` to check the two bound primary PDFs. All five historical manifests and states remain unchanged. FINAL_STATE.json is the current state; FINAL_AUTHOR_MANIFEST.json binds the complete public author packet. Raw PDFs, renders and imported records stay local-only.
