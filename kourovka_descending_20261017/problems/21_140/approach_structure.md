# 21.140 — independent structural approach

Checkpoint: **2026-10-17 21:30 UTC**. Discovery estimate: **10%** toward resolving
21.140, not a probability that the assertion is true. Status: **unresolved**.
This file records an independent structural screen, not a proposed solution.
No external communication, Git operation, release, or promotion was performed.

## Exact target and success criteria

Let `G` be torsion-free, of geometric type `F_infinity`, and satisfy
`cd_Z(G)=infinity`. The affirmative target is an injective homomorphism from
standard Thompson `F` into **every** such `G`. A negative target must verify all
three hypotheses and exclude every abstract copy of `F`.

Type `F_infinity` means a classifying CW complex with finitely many cells in
each dimension. It does not mean a finite complex. Integral cohomological
dimension is the projective dimension of the trivial `ZG`-module `Z`; it
quantifies over coefficient modules, rather than just ordinary homology.

## Mechanism ledger

| Family | Mechanism and evidence | Status and exact gap |
|---|---|---|
| Hierarchical finite-dimensional actions | The primary Kropholler–Mislin theorem gives a finite-dimensional proper classifying space for an `H F` group of type `FP_infinity`. Torsion-free makes its action free. | Strong exclusion. Every target group lies outside `LH F`. Proving that every such exception contains `F` is an unsupported extra assertion. |
| Infinite abelian rank | Disjoint dyadic supports in `F` yield a free abelian subgroup of countably infinite rank. | Necessary consequence of the desired conclusion, not a consequence established from `cd=infinity`. Even infinite rank plus any fixed finite finiteness length is insufficient; see the matrix boundary family below. |
| Finite-type classifying complexes and syzygies | Finite cell counts give a free resolution with a finite number of generators in each degree. Infinite dimension prevents truncation. | No mechanism extracts two group elements satisfying the `F` certificate. The finitely many generators in each degree are not a finite set of possible differentials or a repeated self-similarity pattern. |
| HNN self-similarity and disjoint supports | Two explicit commuting relations and one noncommuting pair certify an embedded `F`. | The certificate is proved below. Its existence in an arbitrary target group remains the entire missing structural bridge. |
| Universal embeddings and compression | Wreath products compress infinite-rank abelian groups to finitely generated groups; metabelian variants achieve every specified finite finiteness length. | These do not achieve `F_infinity`. A current primary theorem obstructs the classical Higman rope trick at `FP_3(Q)` under its exact nontriviality hypotheses. |
| Residual finiteness | Every finite image of `F` is abelian, so residually finite groups exclude `F`. | An affirmative answer implies finite `cd_Z` for every torsion-free residually finite group of type `F_infinity`. This is a special case, not an equivalence or an established theorem here. |

## 1. A verified obstruction covering familiar structural constructions

Write `mathcal F` for the class of finite groups, and `H mathcal F` for
Kropholler's hierarchy: start with finite groups and repeatedly allow actions on
finite-dimensional contractible CW complexes whose cell stabilizers belong to
earlier stages. `LH mathcal F` means locally in this hierarchy.

**Primary theorem used.** Kropholler–Mislin, *Groups acting on finite dimensional
spaces with finite stabilizers*, Comment. Math. Helv. 73 (1998), Theorem A,
printed p.123: an `H mathcal F` group of type `FP_infinity` admits a
finite-dimensional model for its proper classifying space. The full primary
paper is [available from EMS](https://ems.press/content/serial-article-files/42793).

**Deduction S1.** If `G` is torsion-free and of type `F_infinity` and
`cd_Z(G)=infinity`, then `G` is not in `LH mathcal F`.

Proof. Geometric `F_infinity` implies algebraic `FP_infinity` by the augmented
cellular chain complex of the universal cover, and it implies finite generation.
If a finitely generated group is locally in `H mathcal F`, a member of the
hierarchy contains a generating set and hence is the whole group. The primary
theorem gives a finite-dimensional proper model for `G`. Its stabilizers are
finite, hence trivial by torsion-freeness, so its quotient is a finite-dimensional
`K(G,1)`. The free augmented cellular chain complex is a finite-length free
resolution of `Z`, contradicting `cd_Z(G)=infinity`. QED.

**Corollary S1a.** A target group cannot act on a finite-dimensional contractible
CW complex all of whose cell stabilizers have finite integral cohomological
dimension. Each such stabilizer lies in `H_1 mathcal F`, so the proposed action
would put `G` in `H_2 mathcal F` and S1 applies. This does **not** prohibit the
infinite-dimensional free action supplied by its given `F_infinity` model.

**Verified subfamilies.** Kropholler's own
[hierarchical-decomposition paper](https://doi.org/10.1017/CBO9780511566073.015)
states that soluble and linear groups of type `FP_infinity` have finite virtual
cohomological dimension. Thus a torsion-free linear group cannot satisfy the
target hypotheses. Separately, the primary
[Kropholler–Martínez-Pérez–Nucinkis theorem](https://eprints.soton.ac.uk/349586/)
gives a cocompact proper classifying space for every elementary amenable group of
type `FP_infinity`; in the torsion-free case this is a finite `K(G,1)`.

Consequently one cannot obtain a counterexample by selecting a torsion-free
linear group with an infinite-rank unipotent subgroup and merely assuming it is
`F_infinity`. That finiteness property is precisely what the theorem rules out.

**Finite HNN boundary.** An HNN extension of a finite-cohomological-dimensional
base again has finite cohomological dimension. One can build its classifying
space as a graph of classifying spaces, or use the Bass–Serre cellular
resolution, giving

`cd(G) <= max(cd(base), cd(edge)+1) <= cd(base)+1`.

The same graph-of-spaces argument applies to a finite graph of groups with
finite-dimensional vertex and edge classifying spaces. Infinite dimension must
already enter the vertex data, or arise through an infinite process whose
finiteness properties require a separate proof. Replacing the target problem by
an equally difficult infinite-dimensional base is a blocked route.

## 2. An exact finite certificate for an embedded F

Use composition as the group product and `[u,v]=u^-1 v^-1 u v`. The standard
two-generator presentation is

`F = <A,B | [AB^-1,A^-1BA]=1, [AB^-1,A^-2BA^2]=1>`.

The presentation and the fact that every proper quotient of `F` is abelian are
proved in Cannon–Floyd–Parry, *Introductory notes on Richard Thompson's groups*,
Enseign. Math. 42 (1996), §3, Theorem 3.4, and Theorem 4.3. The paper also
identifies `F'` with the elements trivial near both endpoints (Theorem 4.1), and
the subgroup supported on a proper standard dyadic interval with a copy of `F`
(Lemma 4.4). [Primary paper](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf).

**Lemma S2 (certificate).** A group `G` contains `F` if and only if there are
`a,b in G` with

1. `[ab^-1,a^-1ba]=1`;
2. `[ab^-1,a^-2ba^2]=1`;
3. `[a,b] != 1`.

Proof. A copy of the displayed presentation supplies the forward implication.
Conversely, the first two relations give a homomorphism `F -> G` sending
`A -> a`, `B -> b`. If its kernel were nontrivial, its image would be abelian
by Theorem 4.3. Condition 3 rules that out, so the homomorphism is injective.
QED.

This is a finite, checkable success criterion, not an affirmative proof. The
companion exact-rational calculation `structure_artifacts/verify_f_certificate.py`
checks the two relations and noncommutation for the usual PL generators.

**Geometric sufficient condition.** For a faithful permutation or homeomorphism
action, disjoint supports of `ab^-1` and each of `a^-1ba`, `a^-2ba^2`, together
with noncommutation of `a,b`, imply S2. This supplies a transparent mechanism in
many Thompson-like constructions. Neither finite generation of syzygies nor
infinite projective dimension presently supplies this support arrangement in an
arbitrary target group.

## 3. Closure lemmas and what they do not achieve

These are direct deductions from S2's primary quotient theorem. They do not use
an assumption about the amenability of `F`.

**Lemma S3.** The class of groups containing no copy of `F` is closed under
subgroups, arbitrary direct products, extensions, and directed unions.

Proof. The subgroup statement is immediate. For a homomorphism
`phi:F -> product_i H_i`, if no `H_i` contains `F`, each projection of `phi` is
noninjective and hence has abelian image. Therefore `phi(F)` is abelian, so
`phi` cannot be injective.

For `1 -> N -> E -> Q -> 1` with both `N,Q` excluding `F`, suppose `F` embeds
in `E`. The map from this `F` to `Q` is noninjective; its kernel contains `F'`.
The group `F'` contains the copy of `F` supported in, for example, `[1/4,1/2]`.
Thus `N` contains `F`, a contradiction. Finally, a finite generating pair for an
embedded `F` in a directed union belongs to one member, giving the contradiction
there. QED.

**Consequences.** Restricted wreath products of two groups excluding `F` also
exclude `F`, since their base is a directed union of finite direct products and
the wreath product is an extension. Thus `Z wr Z` is an especially simple
torsion-free, finitely generated, infinite-`cd_Z` group excluding `F`: its base
`direct_sum_Z Z` contains `Z^r` for every finite `r`. The two standard generators
are the shift and one lamp. For torsion-freeness, a finite-order element projects
trivially to the torsion-free shift group, and its remaining lamp coordinates
also have no torsion.

This boundary example satisfies neither the required `F_infinity` claim nor a
replacement proof of that claim. It instead demonstrates that unbounded abelian
rank, even combined with finite generation and torsion-freeness, does not force
`F`.

**Lemma S4 (residual finiteness boundary).** A residually finite group contains
no copy of `F`.

Proof. Every homomorphism from infinite `F` to a finite group has nontrivial
kernel, hence abelian image; it kills `F'`. If `F` embedded into a residually
finite group, a finite quotient separating a nonidentity element of that `F'`
would contradict this observation. QED.

In particular, an affirmative answer to 21.140 would imply finite integral
cohomological dimension for all torsion-free residually finite groups of type
`F_infinity`. No proof of this special case was obtained here.

**Tree-action strengthening, checked at 21:30 UTC.** Absence of `F` is also
preserved by arbitrary abstract graphs of groups with injective edge maps.
Every action of `F` on a simplicial tree has a subcopy of `F` fixing a vertex.
The complete primary-source proof and fixed-end audit are in
[structure_tree_closure.md](structure_tree_closure.md). The proof uses a
finitely generated interval copy inside `F'`; it does not assume `F'` itself
is finitely generated. This strengthens the HNN/amalgam screen but does not
supply the missing `F_infinity` property of a universal host.

## 4. Arbitrarily high finite finiteness length still does not force F

This is a verified boundary construction, not a new discovery and not a
counterexample to 21.140.

For `n>=2`, let `G_n` be the subgroup of `GL_2(Q(x))` generated by

`U(1) = [[1,0],[1,1]]`,

`D(x) = [[x,0],[0,1]]`, `D(n!)`, and `D(x+i)` for `1<=i<=n`.

**Primary input.** Kropholler–Mullaney,
*Homological finiteness conditions for a class of metabelian groups*,
Bull. Lond. Math. Soc. 50 (2018), 17–25, prove that these matrix groups are
`FP_{n+1}` but not `FP_{n+2}`. Their §2 records finite presentability and the
split structure with additive kernel

`A_n = Z[x,x^-1,(x+1)^-1,...,(x+n)^-1,1/n!]`.

[Primary paper](https://arxiv.org/pdf/1208.1083),
[published theorem statement](https://doi.org/10.1112/blms.12093).

Here are independent checks of the properties relevant to 21.140.

* The group consists of lower triangular matrices `[[q,0],[a,1]]` whose diagonal
  factors `q` belong to a torsion-free subgroup of `Q(x)^*`. A finite-order
  element has `q^m=1`. Such a product of positive rational constants and monic
  factors `x+i` cannot be a nontrivial root of unity, so `q=1`. Then its `m`th
  power has lower-left entry `ma`, forcing `a=0`. Thus `G_n` is torsion-free.
* The subgroup `U(A_n)` is abelian and the diagonal quotient is abelian, so
  `G_n` is metabelian. By Lemma S3 it excludes `F`, since abelian groups exclude
  nonabelian `F` and extensions preserve exclusion.
* Exact multiplication gives `D(x)^-1 U(1) D(x)=U(x)`, and hence
  `U(x^j)` lies in `G_n` for every integer `j`. The elements
  `1,x,...,x^(r-1)` are linearly independent over `Z`, so their unipotents
  generate `Z^r` for each `r`. Restricting a projective resolution to a subgroup
  gives `cd_Z(G_n)>=r`, so `cd_Z(G_n)=infinity`.
* Finite presentation plus `FP_{n+1}` gives geometric `F_{n+1}`. An explicit
  proof of the conversion appears as Lemma 2.1 of
  [Fournier-Facio–Zaremsky (2026)](https://arxiv.org/html/2607.21727v1).
  Failure of `FP_{n+2}` prevents `F_{n+2}`, and therefore prevents `F_infinity`.

Taking a different `G_n` for every `n` does not produce one group of type
`F_infinity`. There is no uniform finite-length substitute for the original
infinite finiteness hypothesis. Passing to a directed union also does not preserve
finite generation, finite presentation, or geometric `F_infinity` without a
separate mechanism.

## 5. The classical universal-embedding route has a specific obstruction

**Primary input with boundary cases.** Fournier-Facio–Zaremsky,
*Finiteness properties and Higman's rope trick*, arXiv:2607.21727v1,
Theorem B: write `G=F_0/R`, with `F_0` finitely generated free, `G` infinite,
and `R!=1`. Let `L=F_0 *_R F_0`, let `pi:L -> G` kill the second free factor,
and let `iota:L -> P` embed into a finitely generated group. The HNN extension
of `P x G` conjugating `iota x 1` to `iota x pi` has infinite-dimensional
`H_3(-;Q)`, so it is not `FP_3(Q)`. The paper's Remark 3.1 explicitly excludes
finite `G` and trivial `R` from this obstruction.
[Full primary proof](https://arxiv.org/html/2607.21727v1).

Consequently the ordinary Higman/Leary rope trick cannot be invoked to turn an
infinite-dimensional group excluding `F` into a group of type `F_infinity`
in the stated nontrivial situation. A materially different embedding theorem
would be needed, with both `F_infinity` and absence of `F` independently checked.

Another tempting universal construction is the labelled Thompson group
`V(H)`. Palmer–Wu, *Embedding groups into acyclic groups*, Theorem A, prove its
acyclicity; their introduction records preservation of geometric `F_n`.
[Primary paper](https://mdp.ac/papers/embedding-into-acyclic-groups/2510.16879v1.pdf).
However, trivial labels already give a subgroup `V`, which contains standard
`F`, and the output has torsion. It is therefore not a counterexample mechanism.
This also warns against treating ordinary homology as an embedding detector.
No torsion-free acyclic target example is claimed by this observation.

## 6. What infinite cohomological dimension actually supplies

For a ring `R`, a module `M` has projective dimension at most `d` if and only if
`Ext_R^(d+1)(M,N)=0` for every `R`-module `N`. This follows by dimension shifting
and the characterization of projectivity by the vanishing of `Ext^1`.
Consequently `cd_Z(G)=infinity` yields coefficient modules detecting nonvanishing
in arbitrarily high degrees. It does not identify these modules with `Z`, nor
produce commuting elements, abelian subgroups, or a self-embedding.

The missing argument cannot be replaced with any of the following assertions:

* `cd_Z(G)=infinity` automatically gives `Z^r` subgroups for every `r`;
* unbounded abelian rank supplies the two noncommuting generators in S2;
* finite generation of successive syzygies gives a repeating differential;
* a self-embedding of a base group, without the two S2 relations, supplies `F`;
* embedding a group in a finitely presented host supplies geometric
  `F_infinity` for the host.

The first statement is deliberately **not** used or asserted here. Even if a
separate argument established unbounded abelian rank for target groups, section
4 shows why an additional mechanism using the full `F_infinity` hypothesis
would still be necessary to get `F`.

## Strongest verified result and remaining gap

The target groups are forced outside the usual finite-dimensional hierarchy.
An embedded `F` has the exact two-relation/noncommutation certificate S2, and
absence of `F` has robust closure properties S3. Explicit matrix groups satisfy
torsion-freeness, infinite integral cohomological dimension, absence of `F`, and
arbitrarily prescribed **finite** geometric finiteness length. Their proven
failure in the next dimension explains exactly why they do not resolve 21.140.

No mechanism was found that either produces S2 from the target hypotheses or
preserves every finite finiteness condition while keeping infinite dimension
and excluding `F`. These are the exact outstanding gaps. Routes that simply
postulate either bridge are blocked, pending materially new evidence.
