# Independent primary-source target freeze

Frozen at 2026-10-15T09:35:40Z, before access to the candidate proof, its publication status, its sources, supporting claims, or inherited reviews. Completion estimate for this source-scope audit: 35%.

## Provenance and actual reading

The sole candidate artifact read before this freeze was `source_record.json`, used as a curation lead. Its formalization is not an assumption. The primary source is Roser Homs, joint work with Olga Kuznetsova, *Weak maximum likelihood threshold of colored Gaussian graphical models*, in *Algebraic Structures in Statistical Methodology*, Oberwolfach Report 55/2022, DOI 10.4171/owr/2022/55, printed pp. 3146-3149. Official PDF: <https://ems.press/content/serial-article-files/46992>. Downloaded bytes SHA-256: `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`.

I read the entire contribution from its title and initial threshold definitions on p. 3146 through its references on p. 3149. I rendered and visually inspected all four physical PDF pages 26-29 (printed pp. 3146-3149), including the graphs, colors, captions, Proposition 3 and Conjecture 4. The preceding contribution ends above this contribution on p. 3146 and supplies no inherited graph hypotheses.

## Frozen source-defined objects

1. A colored graph is an undirected graph on `m` vertices with arbitrary partitions of vertices into `r` classes and edges into `s` classes. Its linear concentration model has zero entries for absent edges and equal entries within each diagonal or edge color class, intersected with real positive definite symmetric matrices. No connectivity, proper coloring, nontrivial-color, edge regularity, four-cycle, or fixed-`m` hypothesis is stated.
2. The real linear map `pi_G` records sums of sample covariance diagonal entries over vertex classes and sums of off-diagonal entries over edge classes, without a factor two in the displayed map. The cone `C_G = pi_G(Sym_m^{>0})` is open. MLE existence is identified with sufficient statistics lying in this cone.
3. `I(G,n)` is the elimination ideal in `R[t_1,...,t_{r+s}]` formed from equations `t = pi_G(S)` and all `(n+1)`-minors of a generic real symmetric matrix `S`. The ideal parameterizes the Zariski closure of the rank-at-most-`n` projection. Its defining ideal equations do not impose positive semidefiniteness or a real positive semidefinite lift. Complexification is useful for algebraic dominance, but cannot replace real cone or probability arguments.
4. WMLT is the minimum number of observations with strictly positive probability of MLE existence. MLT is the minimum from which MLE existence is almost sure. The contribution associates `n` observations with rank-at-most-`n` covariance. It does not state an unknown-mean/centering adjustment. Any imported theorem must match this convention.

## Frozen literal target

Proposition 3 assumes `I(G,n+1)=0` and a nonzero ideal `I(G,n)=<f_1,...,f_u>`. The `f_i` are pulled back through `t=pi_G(LL^T)` for a triangular Cholesky factor with strictly positive diagonal. Its first displayed case is: if one such pullback is an everywhere-nonzero SOS, or its negative is, then `(WMLT,MLT)=(n+1,n+1)`. Its second displayed case is: if `C_G intersect V_R(I(G,n))` is nonempty, then `WMLT=n` and `MLT=n+1` (the source writes `n=WMLT <= MLT=n+1`).

Conjecture 4 reads, in full: “The two cases in Proposition 3 are the only possible scenarios.” This one-sentence conjecture imports the antecedent hypotheses of Proposition 3 and refers to cases containing both a mechanism and numerical threshold assertions. The source does not explicitly rewrite it as a Boolean disjunction of antecedents alone, nor as a numerical pair classification alone. The full literal assertion and the bare mechanism reading must be kept distinct when assessing a counterexample.

Define `A` to mean the signed nonvanishing SOS certificate stated in the first case, and `B` to mean the real intersection condition in the second case. There are three logically distinguishable claims:

- Printed proposition implications: `A => (WMLT,MLT)=(n+1,n+1)` and `B => (WMLT,MLT)=(n,n+1)`.
- Full printed scenarios: every model satisfying the elimination hypotheses lies in one of those mechanism-and-threshold scenarios.
- Bare predicate exhaustiveness: `A or B` for every such model, independently of whether the printed numerical implications are valid.

I will not presume that refuting one of these automatically refutes all three. Conversely, I will not silently replace the printed cases by a weaker Boolean conjecture to insulate a false numerical assertion. Any final conclusion must identify exactly which statement has been refuted or left open, and whether that warrants the database classification.

## Scope and curation controls

The uncolored four-cycle and colored variants are explicitly examples on p. 3147. The paragraph after Proposition 3 applies the result to four-cycles. Neither Proposition 3 nor Conjecture 4 restricts `G` to a four-cycle. A general colored connected graph is within the written domain; asserting a four-cycle-only restriction would require additional evidence absent from this contribution.

The curation lead inserts “exactly one” and makes the two mechanisms determine the thresholds. The source says “only possible scenarios,” not “exactly one.” Mutual exclusivity of the mechanisms may be a deduction: a signed SOS nonzero on all positive definite Cholesky matrices precludes the real PD intersection. It must not be assumed merely from the cleaned text. The cleaned strict inequality in the second pair follows from the source's equalities if `n` is an integer, but is not an independent extra hypothesis.

## Falsifiable audit success criteria

For any proposed counterexample, check all of the following: legal graph/color model; correct real statistic map; `I(G,n) != 0` and `I(G,n+1)=0` as exact algebraic facts; the claimed probabilities under the source's sample-rank convention; WMLT as a *minimum*, including every smaller sample size; and MLT as an almost-sure threshold rather than a weak existence threshold. Determine `A` and `B` independently wherever feasible. An interior real point of the algebraic projection variety alone does not prove the existence of a real PSD rank-`n` preimage. A single PSD completion alone gives an open positive-probability set only if continuity and strict positivity give a valid stability argument.

Potential boundary checks: singleton-color graphs are allowed by the written definition; nontrivial colors need exact equality constraints; PSD and PD cones are distinct; rank-at-most versus exact rank matters for minimal sample sizes; a threshold smaller than the last nonzero-elimination index would falsify a printed minimum equality but might still satisfy `B`; and a generator-dependent SOS condition requires tracking the generator choice or establishing a stronger absence for every ideal member.

## What is not yet claimed

No assessment of the candidate construction, mathematics, novelty, or priority has been made at this freeze. No external individual has been contacted. This is an immutable logical checkpoint; later findings will be recorded separately rather than overwriting this interpretation.
