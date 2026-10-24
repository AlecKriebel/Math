# Independent adversarial audit of the triangular AT construction

Timestamp: 2026-10-24 18:39 UTC. Mathematical verification estimate: 100% for the stated construction and the supplied original-Rozhkov definition. No algebraic gap found. Historical-source custody retains the separate original-PDF/raster gap described below. No novelty claim is assessed here.

## Claim, assumptions, and exact success criterion

Let `p` be any prime, `X={0,...,p-1}`, and `T=X*`. An automorphism's section at a vertex `u` is denoted `g|u`; its permutation of the first `N` levels is `g^(N)`. Let `a` be the rooted cycle `(0 1 ... p-1)`, with every section at a nonempty vertex trivial.

Put `T_r=r(r+1)/2` and define `i(T_(r-1)+j)=j` for `1<=j<=r`. At the pairwise incomparable vertices

\[
v_n=0^{n-1}1\quad(n\ge1),
\]

place the rooted local cycle `a` exactly when `i(n)=i`. Let the resulting automorphism be `d_i`, and set

\[
G=\langle a,d_1,d_2,\ldots\rangle.
\]

The target claim is that this is an infinite locally finite `p`-group and is an AT-group under the original 1986 definition summarized in the independent definition audit. That definition permits an infinite subset `D` of longitudinal generators, requires every designated generator to have infinite coordinate-level support, and requires all accompanying permutation groups to be transitive.

## Check 1: definition of the infinite portraits and longitudinal support

If `m<n`, the `m`th letter of `v_m` is `1`, whereas that of `v_n` is `0`. Thus these vertices are incomparable. The corresponding supported rooted automorphisms commute, and their infinite product is well defined: every finite input word meets at most one of their support vertices. This also gives a direct action formula avoiding infinite-product notation.

For a word `x=x_1...x_l`, let `r` be its first nonzero letter position. If there is no such position, `d_i` fixes the word. Otherwise it changes only `x_(r+1)`, adding `1 mod p`, precisely when

\[
r<l,\qquad x_r=1,\qquad i(r)=i.
\]

It fixes the word in the other cases. The first deviation from `0^infinity` remains unchanged. The changed coordinate is exactly the next coordinate, and its permutation depends only on the deviation position and symbol. This is a longitudinal mutation in the supplied original definition. The identity permutations at deviation symbols other than `1` are permitted accompanying permutations.

The label `i` occurs at `n=T_(r-1)+i` for every row `r>=i`; hence `d_i` changes infinitely many coordinate levels. In zero-based coordinate indexing, the support vertex has depth `n`, and its local permutation changes coordinate `n`. Thus there is no finite-support or off-by-one loophole. Each `d_i` has order exactly `p`.

## Check 2: AT transitivity and infinitude

Take the root subgroup `C=<a>` and longitudinal subset `D={d_i:i>=1}`. The root accompanying group is `C_p`, transitive on `X`. At every companion level `n>=1`, the generator `d_(i(n))` supplies the cycle `a` at the vertex `0^(n-1)1`; every other accompanying permutation is identity. Consequently `Pi_n(D)=<a>=C_p`, transitive on `X`.

The elements `d_i` commute. A finite product `product_i d_i^(e_i)` is identity only when all `e_i=0 mod p`: for a nonzero coefficient choose a support vertex of that `d_i`; all other factors have trivial local label there. Therefore

\[
\langle D\rangle\cong\bigoplus_{i\ge1}C_p.
\]

In particular `G` is infinite, independently of any general AT infinitude theorem. All its local permutations lie in the prescribed cyclic group, so it also meets the supplied constant-prime `AT_omega` subclass definition.

## Check 3: exact depth-N sections

Fix a finite `I subset N_{>=1}`, with `m=|I|`. Choose `N>=1` with `i(N) notin I`; this always exists since the labels are unbounded. One explicit choice is `N=T_j`, where `j` is any positive integer outside `I`.

For `i in I`, define the tail `t_i=d_i|_(0^N)`. Its local labels are `a` at the vertices `0^(r-1)1` for `r>=1` satisfying `i(N+r)=i`, and identity elsewhere. Let `K=<t_i:i in I>`. Again the supports are pairwise incomparable, so these tails commute and have order `p`. Every label still occurs infinitely often after `N`, and the supports for different `i` are disjoint. Hence `K` is exactly `C_p^m`, although the upper bound `|K|<=p^m` suffices.

The full list of depth-`N` sections is

\[
a|_u=1\quad(|u|=N),\qquad
d_i|_u=\begin{cases}t_i,&u=0^N,\\1,&u\ne0^N.\end{cases}
\]

To verify exhaustiveness, split the portrait levels `n` into three cases:

1. `n<N`: a rooted permutation at a vertex of depth `n` has identity sections at all vertices of depth `N`. It can permute those vertices, but it leaves no nontrivial depth-`N` section.
2. `n=N`: the possible section at the side vertex `0^(N-1)1` would be `a`; it is absent from every selected generator because `i(N) notin I`.
3. `n>N`: the support vertex begins with `0^N`, so all remaining labels lie in the single ray section `t_i`.

This argument uses sections of the complete automorphism, not pointwise stabilizer membership. The selected `d_i` need not fix level `N`.

## Check 4: closure of sections under products and finite p-group containment

Let `P_N` be the finite group of depth-`N` rooted-tree automorphisms all of whose local permutations belong to `<a>`. Recursively `P_0=1` and `P_(N+1)=P_N^p semidirect C_p`, so

\[
|P_N|=p^{1+p+\cdots+p^{N-1}}.
\]

For the left-action product convention `gh=g o h`, the section formula is

\[
(gh)|_u=g|_{h(u)}h|_u.
\]

Thus the collection of automorphisms whose depth-`N` sections belong to `K` and whose depth-`N` truncation belongs to `P_N` is a subgroup, identified with

\[
K^{X^N}\rtimes P_N.
\]

There is no unsupported invariance of `K` under conjugation by `a` in this step: `P_N` acts only by permuting the `p^N` section coordinates. The generators `a` and `d_i` for `i in I` have precisely the required section data, so

\[
H_I=\langle a,d_i:i\in I\rangle
\hookrightarrow K^{p^N}\rtimes P_N.
\]

The section/truncation map is injective because an automorphism is determined by its finite top action and all sections at one level. Its target has order

\[
p^{mp^N+(p^N-1)/(p-1)}.
\]

Hence `H_I` is a finite `p`-group. Any finite subset of `G` uses only finitely many `d_i` in its defining words and lies in such an `H_I`. This proves local finiteness and that every finite subgroup is a `p`-group. The empty-`I` case is simply `<a>=C_p` and causes no exception.

## Falsification checks and reproducibility

`check_construction.py` independently evaluates the explicit first-deviation formula and the original vertex-portrait action, then checks every leaf word in five cases with `p=2,3,5`, including `I={1,2}` and a depth-6 cutoff. It completed 11,778 generator-word comparisons and section identities without failure. Exact breadth-first closure enumeration for `p=2`, `I={1}` gives group orders `2,8,16,16,32,32,32,32` at depths 1 through 8. These computations support the proof; finite depths alone would not establish local finiteness.

The program also tests the closest erroneous variant: dropping the cutoff hole. For `p=2`, `I={1}`, `N=1`, the word `10` maps to `11`, so `d_1|_1=a`. Every ray tail `d_i|_0` fixes the first level, so the side section `a` does not belong to their subgroup. The proposed containment fails at this bad cutoff. The actual construction explicitly avoids it.

Reproduce with `python3 check_construction.py` in this directory. Saved output: `computation_results.json`.

## Strongest result, residual gap, and publication status

**Strongest verified mathematical result:** the displayed construction is an infinite locally finite `p`-group with an original-longitudinal infinite-support generating set and transitive companions at every level. The finite-generation proof has no remaining algebraic gap.

**Exact source dependency:** original-definition interpretation uses the parent-provided local `independent_definition/definition_audit.md` and its primary OCR receipt `sources/rozhkov_1986_successful_web_excerpt_receipt.md`. These expressly say `D` is a subset, allow infinitely generated groups, and require infinite support. The original PDF bytes/raster have not been independently acquired in this subtask; that historical-source custody limitation is not filled by the proof or computation. A requirement absent from the supplied definition could change the applicability claim; no such requirement appears in the supplied excerpt.

**Status:** mathematical candidate verified under the supplied original definition; no independent novelty or literature-completeness assessment. No Git actions, release, publication, outreach, or other external communication was performed by this subtask.

## Addendum: independent verification of a derived-subgroup embedding

Timestamp: 2026-10-24 18:40 UTC. Addendum completion estimate: 100%; no gap found.

Let `H` be any locally finite `p`-group generated by elements of order `p` (in particular the group verified above), and put

\[
K=H^p\rtimes\langle t\rangle,\qquad t^p=1,
\]

with the exact convention

\[
t^{-1}(x_0,\ldots,x_{p-1})t=(x_1,\ldots,x_{p-1},x_0).
\]

The diagonal map `Delta:H -> H^p`, given by `Delta(h)=(h,...,h)`, is an injective homomorphism even when `H` is noncommutative: multiplication in each coordinate gives `Delta(h)Delta(k)=Delta(hk)` without interchanging `h` and `k`.

Use `[u,v]=u^{-1}v^{-1}uv`. For one order-`p` generator `h`, take `w=(1,h,...,h^(p-1))`. Then

\[
\begin{aligned}
[w,t]
&=w^{-1}(t^{-1}wt)\\
&=(1,h^{-1},\ldots,h^{-(p-1)})
  (h,h^2,\ldots,h^{p-1},1)\\
&=(h,h,\ldots,h,h^{-(p-1)})
 =\Delta(h),
\end{aligned}
\]

where the last coordinate equals `h` because `h^p=1`. The only cancellations use powers of this one element `h` inside one coordinate. Neither commutativity of `H` nor commutativity between different generators is needed. Each diagonal generator therefore belongs to `K'`. Since `Delta` is a homomorphism and `K'` is a subgroup, `Delta(H)<=K'`; this proves an embedding of `H` into the derived subgroup of `K`.

Finally, any finite subset of `K` has finitely many base coordinates in `H`. These coordinates generate a finite `p`-subgroup `F<=H`. The finite subset is then contained in the finite `p`-subgroup `F^p semidirect <t>` of order `p|F|^p`. Thus `K` is itself a locally finite `p`-group. This argument is valid for noncommutative `F`, since cyclic coordinate permutation preserves `F^p`. No additional computation or source assumption is needed for this algebraic addendum.
