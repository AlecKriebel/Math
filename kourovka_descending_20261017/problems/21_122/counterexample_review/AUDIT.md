# Independent audit of restricted counterexample-family deductions

UTC: 2026-10-24T23:34Z. Assigned audit completion: **100%**. Frozen family discovery estimate:2%; the overall21.122 discovery estimate is not advanced by this review. Reviewer: `/root/p21124_retraction_adversary`, who authored none of the three input notes.

**PASS for the final frozen three-note package and exact finite probes.** No complete21.122 answer, novelty assessment, or publication approval is implied.

Audited proof hashes:

- `FIBER_PRODUCT_OBSTRUCTION.md`: `6ca595d9410d0a5be0e26d2ae4bebac025c4838b27f8c535205b270db8cf6e88`.
- `LAW_AND_BRANCH_REDUCTIONS.md`: `4899131c55d5797eb78e6b2eda238d6be8b8cfb593a7d13511951e1f44b91e6f`.
- `CENTRAL_KERNEL_GAP.md`: `c9f7e189b7a992a965869db777ed2b21486de78afd066b306b7b9ca7bd421a0a`.

The input/output manifest records current bytes. Earlier boundary objections were relayed through root; the author repaired the empty-index case, deterministic-versus-active wording, and explicit continuous-surjective hypotheses before this final freeze. No author file was edited by this reviewer.

## Finite common quotient, all index sets

For empty I the product group is trivial, and there is one word value. The final proof handles that case before invoking a common quotient map. For nonempty I, each map π_i:F_i→H is onto, and the common-quotient map from the fiber product to H is onto. The fiber product is a closed subgroup of the compact product, because equality of the coordinate quotient values is a closed condition.

Fixing h∈H^k, every restricted set S_i(h) is nonempty and finite. If a coordinate value z_i lies in S_i(h), choose a realizing k-tuple in that coordinate. Assemble the jth entries across all coordinates. Every assembled variable has quotient h_j, so belongs to the fiber product. This proves the exact equality of the restricted image with ∏S_i(h), rather than only an inclusion. No further compatibility between distinct coordinates is imposed by this model.

If infinitely many S_i(h) have at least two elements, choose countably many such indices and two alternatives at each; fixing a base value in every other coordinate embeds Cantor space. This proves a lower bound of continuum even for an uncountable indexing set; it does not falsely assert that the whole image has exactly continuum cardinality. If only finitely many factors vary, the product is finite. Finally H^k is finite because both H and the ordinary word's variable set are finite. Its finite union of restricted images therefore has the required dichotomy.

The final consequence correctly defines active to mean |S_i(h)|>1 for some h. Nonidentity singleton outputs do not create activation: F_i=H=C2, π_i=id, w=x gives a deterministic nonidentity value at infinitely many coordinates while the group and value set are finite. This earlier potential overstatement is repaired.

The theorem permits noninjective and nonsplit quotient maps. The independent S4→C2 test uses a kernel of order12; the C4→C2 boundary has no homomorphic section. Neither proof nor computations assume π_i is globally injective or that extensions split.

## Infinite controller and clopen activation

The repaired paragraph explicitly assumes continuous **surjective** homomorphisms π_i:E_i→H of profinite groups with finite kernels. For a nonempty index set, all restricted fibers are finite and nonempty, the Cartesian restricted-image argument remains valid, and projection sends the word image onto H_w. Thus a subcontinuum global image forces only finitely many varying coordinate fibers for each fixed input tuple. This is necessary, not sufficient for a counterexample.

Here is the full local-section justification. For K=kerπ finite, choose an open normal U≤E avoiding every nonidentity element of K. Then π|U is injective. Its image is open: a continuous surjection from compact E to Hausdorff H is a quotient map, and π^-1(πU)=UK is open. The compact-to-Hausdorff bijection U→πU is a homeomorphism. Translate its inverse over a coset of πU to obtain a continuous local section. This uses injectivity only on the chosen open subgroup, never on all of E; it does not produce or require a splitting homomorphism H→E.

On a small rectangle of H^k, choose such sections for the k inputs. Every lift is one of finitely many continuous choices obtained by multiplying by kernel elements. For any two choices, their word values have the same quotient. Their ratio is consequently a continuous map into the finite, discrete subspace K. Equality and inequality of these word values are both clopen conditions. A finite union of the inequality conditions gives the local activation set; applying this at every point shows that activation is globally clopen. This argument applies to each index separately, so the countable-index assertion in the note is valid without any unjustified uniform section across indices.

Point-finiteness of these clopens cannot be upgraded to finiteness of the family by compactness. The p-adic valuation annuli are an infinite disjoint clopen family, with0 in none. No genuine fixed-word extensions realizing that pattern have been constructed by the note. The stated realization obstruction remains an unsupported central step, correctly marked blocked.

## Nontrivial law from the iterated verbal theorem

The exact external theorem is [Shumyatsky2401.15707v2, Theorem1.1](https://arxiv.org/html/2401.15707v2#S1): under the small-image assumption, the **closed** subgroup w(w(G)) is finite. It does not already settle the original value-set question.

Let w≠1 in the free group F_k, k≥1. With K=w(G), F=w(K), choose the positive exponent e of finite F, taking e=1 if F is trivial. Inner values w(x_i1,...,x_ik) belong to K, so the outer w-value belongs to F; its eth power is1. This proves a law on G, with e allowed to depend on G and w.

To verify that the resulting free word is nontrivial, split the k² free variables into k disjoint blocks. Their ambient free group is the free product of the block free groups. In each factor the block copy w_i is nontrivial and has infinite order. Alternating nonzero powers of w_i from distinct factors cannot cancel by the free-product normal form. Therefore y_i↦w_i defines an injective homomorphism F_k→F_(k²). Its image of the nontrivial outer w is nontrivial, and its positive eth power remains nontrivial by free-group torsion-freeness. Unused variables do not change this argument. For k=1 and w=x^r, r≠0, it gives x^(r²e)≠1. The trivial-word boundary has value set{1} and is excluded from this reduction.

Thus hypothetical counterexamples must satisfy some nontrivial law. This does not prove the target for all law groups or provide a uniform law independent of G. Rephrasing the remaining target as an assertion about all law groups is not a completed solution.

## Abstract free subgroups and weakly branch groups

A group with an abstract nonabelian free subgroup satisfies no nontrivial law. More concretely, F2 contains free subgroups of every finite rank, so any nontrivial fixed word has a nonidentity value there. That value has infinitely many conjugates in the free subgroup. In the ambient profinite group its conjugacy orbit is a homogeneous profinite quotient by a closed centralizer; an infinite such orbit has cardinal at least continuum. It is not enough merely to say that the orbit is compact, since arbitrary infinite compact images can be countable. The orbit is contained in the word-value set.

For the stated closed faithful weakly branch action, the rigid stabilizer R_v is closed. Infinitely many pairwise disjoint descendant subtrees give arbitrarily large independent products of nonidentity rigid elements, so R_v is infinite and hence has cardinal at least continuum. If g moves v, the subtrees rooted at v and g(v) are disjoint. An r∈R_v commuting with g also belongs to R_(g(v)); disjoint support and faithfulness force r=1. Therefore r↦g^r injects R_v into the conjugacy class of g. Every nonidentity word value thus already supplies continuum values. This proves the stated {1}-or-continuum alternative for that class.

[Abért's primary paper, Corollary4](https://arxiv.org/pdf/math/0306364) separately supplies abstract free subgroups for profinite weakly branch groups without finite generation or bounded-degree assumptions in its first clause. Those extra assumptions belong to the further dense-free-subgroup conclusion. The note does not conflate them. A law passes to quotients, so a counterexample cannot have a weakly branch quotient either.

## Central-kernel formula and exact remaining gap

For a central kernel K and a word with exponent sums r_j, collecting the central kernel terms in the word evaluation proves

`w(g1 k1,...,gk kk)=w(g1,...,gk) product_j kj^(rj)`.

Negative exponents and zero sums cause no exception. With d=gcd(r_j)≥0 and K^0={1}, Bezout's identity gives ∏K^(r_j)=K^d. Thus every restricted fiber over a fixed quotient tuple is a coset of the same finite subgroup K^d, and its cardinality does not depend on the input tuple. Lift variation cannot create rare clopen activation. Infinitely many nontrivial K_i^d already force continuum values for any fixed tuple; a small global image leaves only finitely many such factors.

When all r_j vanish, the word depends on the **whole quotient input tuple**, not just its resulting word value in H. The independent Heisenberg control has two quotient tuples with the same trivial quotient commutator but different central commutator values. The note correctly retains this distinction. If w is a law on H, its descended value map H^k→∏K_i is continuous: the word map factors through the continuous surjection from the compact fiber-product input space onto H^k. The remaining constraint is realization by genuine central extensions, not arbitrary choice of a continuous function.

If E is a central extension of metabelian H, then E'' lies in the central kernel, so E has derived length at most3. The displayed word [[x,y],[x,y]^x] lies in E'', is a law on H, and is a nontrivial free word (independent reduction gives length14). This identifies only a possible framework; no small infinite image or new open-status claim for that specific word is established. A central extension of a nilpotent group of class c has class at most c+1, so the cited nilpotent results really do exclude that subclass. [Zozaya2608.02237v1, Theorem1.1](https://arxiv.org/html/2608.02237v1#S1) covers profinite metabelian groups, without thereby covering every central-by-metabelian group.

Finally, for odd p the semidirect square calculation is exact: in Z_p⋊C4 with inversion action, even C4 coordinates give all (2a,1) and odd coordinates give only(0,t²). Since2 is a p-adic unit, the first part is the full Z_p translation subgroup. The isolated second value does not imply a finite image. Finite levels have p^n+1 square values, including n=0. No counterexample is asserted from this metabelian control.

## Independent reproduction

`independent_models.py` imports no author implementation. It uses:

- AGL(2,2) as an independent S4 model, with its sign quotient and order12 kernel; direct two-factor fiber products have order288. All four word-image counts are computed directly there, and n≤12 counts use membership-mask intersection dynamic programming rather than the author's inclusion–exclusion.
- Recursive wreath multiplication tables, giving group orders2,8,128, root-flip centralizer orders2,4,16 and class sizes1,2,8. All four finite word-image sequences match the submitted counts. The general class recurrence is separately justified by the diagonal centralizer; the root flip is not claimed to be a tested word value.
- Three central-extension models (Heisenberg groups over F2,F3 and C8×C2→C2), checking all restricted cosets for six words, including negative exponents and the identity. A nonsplit C4→C2 boundary separates local sections from homomorphic splitting.
- Twelve odd-prime finite semidirect square cases and free reduction of the residual word.

Every corresponding author certificate field matches the independently calculated results. The author's full checker was also executed read-only with its output redirected; all non-timestamp fields match the submitted JSON. The fresh `law_branch_secondary/` reviewer independently checked the general law and branch proofs and supplied additional exact word/subgroup controls. Its receipt hashes were checked.

No substantive objection remains in the final audited scope. The outstanding original problem is still to exclude or realize a genuine fixed-word central cocycle with infinite subcontinuum image; none of these restricted obstructions closes it.
