# Independent algebra/geometry adversarial audit — PR #618 / 30004609

Audit completed 2026-10-13 UTC. The frozen candidate is `native/unsolved_math_prioritization/attempts/30004609/PROOF.md`, SHA-256 `73716fdb49896b2443ada06ed707dba1e0d08f304d9e563cf251c949d8752798`.

**Verdict:** no mathematical obstruction or mandatory mathematical repair found. The candidate gives a complete proof of the stated characteristic-zero theorem, conditional only on established factorization and freeness-implies-formality theorems. The direct geometric pruning proof is valid and does not reuse the failed withdrawn inference. This is a mathematical audit, not a certificate of priority or human peer review.

**Strongest verified result:** every finite central free arrangement over a field of characteristic zero whose nonzero exponents are 1 or 2, with at most one 3, has a maximal modular chain. Reducible and nonessential arrangements are included. Empty rank-zero arrangements are covered by the trivial lattice convention.

## 1. Exact target and external premises

The original Oberwolfach contribution sets up central essential arrangements over a characteristic-zero field on printed p. 283 and states the target supersolvability conjecture on printed p. 284. Both pages were visually inspected. The candidate's theorem matches it and safely adds products and essentialization. [Original report](https://ems.press/content/serial-article-files/46883).

The manuscript was withdrawn in January 2022 for unguaranteed hand enumeration and an unjustified factor-size inference. I inspected the v3 p. 14 inference and the v4 notice. The candidate never assumes inductive freeness, the disputed enumeration, or the assertion that one deletion factor must have size one. Its historical counterexample is correctly retained as an example satisfying the desired conclusion. [Withdrawn record](https://arxiv.org/abs/1707.07091v4), [previous mathematical text](https://arxiv.org/pdf/1707.07091v3).

The required formality is linear-relation formality, not topological formality: if the normal map is `K^E -> V*`, its kernel must be spanned by relation spaces of complete rank-two flats. The modern formality paper defines precisely this surjectivity and recalls freeness implies formality, with attribution to Yuzvinsky Corollary 2.5, in a field-valued arrangement setup. The original publisher PDF was unavailable (HTTP 403). A separate direct proof of the stronger implication appears in DiPasquale Corollary 4.10; specializing multiplicity to one supplies the same premise. No algebraic closure, real ordering, or complex topology is needed in the candidate's own arguments. [Formality paper](https://arxiv.org/pdf/2202.09104v2), [DiPasquale primary proof](https://arxiv.org/pdf/1806.05295v1).

Factorization is used only for the number of hyperplanes and the rank-two coefficient. The original OWR source itself records this theorem in the relevant notation. The candidate derives its needed rank-two multiplicity bound separately, so no questionable localization-exponent comparison is a premise.

## 2. Exponent-one and essentialization reductions

For an essential arrangement, a degree-zero logarithmic derivation is a constant vector annihilated by all defining normals, so it is zero. Consequently, for a free arrangement, the dimension of `D(A)_1` is exactly the multiplicity of exponent one.

Choose independent defining forms `x_1,...,x_r` as coordinates. A linear logarithmic derivation satisfies `theta(x_i)=lambda_i x_i`. Every further defining form `alpha=sum a_i x_i` satisfies `theta(alpha)=lambda alpha` for some scalar. Therefore all coordinates in its nonzero support have the same `lambda_i`. A nonscalar diagonal derivation splits all normals among its distinct coordinate eigenspaces. Those eigenspaces are defined over the original field because the matrix is already diagonal. The arrangement decomposes as a product. Conversely each product factor contributes an independent Euler derivation. This establishes the exact reduction to one exponent one for an irreducible essential factor.

A nonessential arrangement has defining polynomial independent of complementary coordinates; its derivation module is the essential module after scalar extension plus one degree-zero partial derivative for each complementary coordinate. Quotienting the common center identifies the lattices. Product lattices have modular chains obtained by concatenating the factor chains. Thus these reductions preserve the desired conclusion without importing the withdrawn product-factor claim.

Rank one is a single hyperplane after essentialization. Rank two is automatically supersolvable. With the permitted irreducible exponent lists it has either three or four normals. Rank zero has the single-element lattice. These limiting cases cause no exception.

## 3. Direct low-degree multiplicity bound

Let a complete rank-two normal flat have forms `x,y,x+c_1 y,...,x+c_{m-2}y`, with distinct nonzero scalars. For a homogeneous logarithmic derivation of degree `q`, write `theta(x)=xP`, `theta(y)=yQ`, where the coefficient degrees of `P,Q` are `q-1`. Reducing tangency to `x+c_i y` modulo that linear form gives

`c_i y (Q-P) = 0 mod (x+c_i y)`.

Since `y` is coprime to `x+c_i y`, every such factor divides `P-Q`. Distinct linear factors are coprime in the full polynomial ring, even with other ambient variables. If `m-2 > d-1` and `q<=d`, their product has degree greater than `P-Q`, forcing `P=Q`.

If all basis degrees are at most `d`, every free-basis column then has its first two entries `xP_j,yP_j`. The two rows are proportional over the fraction field, contradicting basis independence. Hence `m<=d+1`. This is a genuine direct deduction and does not use any withdrawn lemma. It also handles smaller-degree basis columns by taking zero quotients where appropriate.

In the all-2 case the nontrivial rank-two flats are triples. In the one-3 case they are triples or four-point pencils. The usual pair count gives `binom(n,2)-b_2=sum_L binom(|L|-1,2)`. Together with factorization and formality it yields the candidate's exact counts and `v<=1`. I found no hidden assumption in the arithmetic.

## 4. Independent proof of the terminal-pencil lemma

This is the most important geometric step. Let a complete pencil `L={a,p_1,...,p_{m-1}}` meet the remaining configuration `E'` only in `a`, with no `p_i` in another nontrivial rank-two flat. Let `R` be the full relation kernel and `S` the span of all remaining local relation spaces, viewed in `K^E`.

Formality gives `R=R_L+S`. The supports of `S` lie in `E'`. Moreover `R_L intersect K^{E'}=0`, because a relation in this intersection is supported on the single nonzero normal `a`. Hence the sum is direct. If a relation is supported in `E'`, its `R_L` part must vanish on every `p_i`, and therefore be zero. Thus `R'=S`, not merely a subspace of it. This proves formality of the deletion and

`dim R'=dim R-(m-2)`.

There are `m-1` removed normals, so `rank(E')=r-1` exactly. Write `W=span(E')` and `U=span(L)`. The full span is `W+U`, and dimension counting gives `U intersect W=K a`. Every removed normal is nonproportional to `a`; therefore none lies in `W`. It follows that `E'` is exactly the represented coatom consisting of all normals lying in `W`. This shorter dimension proof also verifies the candidate's separate support proof of flatness.

For any represented flat `F`, choose a set of its normal generators. If there are no outside generators, `F` is contained in `W`. If there is exactly one, its image in `V*/W` is nonzero, so `F intersect W` is the span of the inside generators. If there are at least two outside generators, their distinct projective classes span `U`, and

`F intersect W = span(inside generators) + K a`.

Every intersection is therefore spanned by represented normals. For a linear matroid this is precisely the modularity condition: the represented meet has the full vector-space intersection dimension, making the modular rank equality hold. Thus `W` is a modular coatom.

If `C` is modular inside the deletion's lattice, then for every full flat `F`, the intersection `W intersect F` is a represented flat inside `W`. Hence `C intersect F=C intersect (W intersect F)` is represented as well. This proves `C` is globally modular. Lifting the whole chain and appending the full space is valid. No assumption that the deletion is free, or that arbitrary deletions preserve formality, is used.

### Exact premise-failure witness

Without formality the lemma fails. Take normals

`a=(1,0,0), p_1=(0,1,0), p_2=(1,1,0), b=(0,0,1), c=(1,2,3)`.

The only nontrivial rank-two flat is `{a,p_1,p_2}`, so its two outward points meet no other nontrivial line. But the remaining normals `{a,b,c}` have full rank three, and their closure contains all five normals. The full relation kernel has dimension two whereas local rank-two relations span only dimension one. A fresh degree-one computation gives dimension one, so the arrangement is irreducible despite disconnected rank-two incidence. This simultaneously demonstrates why both the pruning lemma and the incidence connectedness argument need formality. The candidate satisfies that premise throughout.

## 5. Represented K4 core and lifting back to all ranks

The minimal dependency of triple relations has all coefficients nonzero; each normal in its support must occur at least twice. The cycle-rank bound and the fact that distinct complete normal lines meet in at most one point force exactly four relations on six normals, each normal appearing twice. All pairs of relation supports meet at a distinct point. I checked the inequalities and equality conditions directly: no missing small support or larger support can survive the cycle budget.

The surviving relation vectors have rank three because their chosen dependency is minimal. After pruning, formality is retained, so the six surviving normals have rank `6-3=3`. Deletion cannot create a new collinear triple; any such triple would already have been a line in the original configuration. Thus the complete nontrivial lines are exactly the four star triples of the K4 indexing.

Fix a star triple `L_i`. Every other triple line meets it at a represented normal. Every ordinary rank-two flat is a pair of disjoint K4 edges, and those edges cover the four vertices. Consequently exactly one of the two normals belongs to the fixed star `L_i`. Its two-dimensional span again meets `span(L_i)` at a represented normal. Every rank-two flat has represented intersection with `span(L_i)`; rank-zero, rank-one, and full-rank cases are immediate. This proves the chosen line is modular in any allowed representation, not only the rational fixture.

Every atom is modular in a simple geometric lattice. The atom, modular line, zero, and full normal space give a maximal modular chain. Applying the already verified terminal-pencil extension finitely many times yields the original rank. The tree cases end in rank-two pencils instead. No rank-specific enumeration or inductive-freeness hypothesis is hidden in this step.

## 6. Fresh exact computation and reproduction

`verify_algebra.py` imports no candidate code. It uses SymPy exact rational matrices, exhausts independent generating subsets to compute the complete small lattices, solves all polynomial tangency equations for derivations, and searches the resulting derivation spaces for Saito certificates. Results are in `ALGEBRA_CHECKS.json`.

| Independent check | Exact result |
|---|---|
| K4 full derivation-space calculation | Dimensions `D_1=1,D_2=4,D_3=10`; basis degrees `(1,2,3)`; determinant divided by defining polynomial `-1` |
| Non-Fano full cubic calculation | `D_1=1,D_3=8`; basis degrees `(1,3,3)`; determinant ratio `1`; no modular coatom in full lattice |
| Withdrawal example | `D_1=1,D_2=6,D_3=19`; basis degrees `(1,2,2,3)`; determinant ratio `1/2`; full modular chain |
| Arbitrary-slope terminal pencils | 24 exact cases on triple, four-point, K4, and non-Fano bases; kernel direct sum, rank drop, coatom closure, modularity, and all modular base flats lifting passed |
| Nonsupersolvable base boundary | All six tested attachments to non-Fano remain nonsupersolvable, showing the base supersolvability premise is not accidentally omitted |
| Omitted formality | Explicit five-normal counterexample above |
| Historical deletion | Two direct factors with sizes 4 and 3; degree-one derivation space has dimension two |
| Frozen author diagnostics | Parsed rerun JSON is exactly equal to frozen `RESULTS.json` |

The independently found Saito bases differ from the candidate's witness basis. Their coefficients and full lattice chains are serialized for checking. All arithmetic is rational or symbolic; there are no numerical tolerances. The finite tests are diagnostic evidence. The universal conclusion rests on the arguments in Sections 2-5.

To reproduce with the environment supplied by the parent audit:

```
/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python verify_algebra.py
```

## 7. Repairs, priority caveat, and remaining gap

**Mandatory mathematical repairs: none found.** No intermediate lemma was invalidated under its stated assumptions. Optional exposition improvement: explicitly mention the empty rank-zero arrangement and state the represented-intersection criterion for modularity as a named elementary lemma.

**Relevant prior work to account for before publication:** DiPasquale's 2018 Section 6 already introduces the same rank-two incidence graph and shows a free arrangement with independent local relation spaces in the `TF2` class is supersolvable, with the graph a tree. Proposition 6.1 and Theorem 6.6 cover the candidate's tree mechanism. This does not settle the one-dependent-relation K4-core case by itself, but the paper should credit the existing graph/tree method and avoid claiming that the incidence graph or tree supersolvability mechanism first appears here. Full priority review is outside this audit's assignment.

**Exact remaining mathematical gap identified by this audit: none.** I recommend advancing this frozen candidate through the separate priority and final-package adversarial reviews. This recommendation does not substitute for those reviews or authorize any external publication operation by this reviewer.
