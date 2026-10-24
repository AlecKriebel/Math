# Independent secondary audit: law and weak-branch reductions

UTC: 2026-10-24T23:28:00Z. Narrow audit completion estimate: 100%.
Verdict: **PASS for the stated reductions**, with one explanatory cardinality
clarification below. No full solution, novelty determination, or publication
approval follows.

Frozen input: `counterexample/LAW_AND_BRANCH_REDUCTIONS.md`, SHA256
`4899131c55d5797eb78e6b2eda238d6be8b8cfb593a7d13511951e1f44b91e6f`.

The reviewer read AGENTS.md and the target only. No other family conclusions
or author computational implementation were read. Parent separately audits
the finite wreath image counts and fiber-product arguments; those are outside
this secondary audit.

## External theorem and scope

The freshly read [Shumyatsky primary v2](https://arxiv.org/html/2401.15707v2)
defines verbal subgroups as closed subgroups and its Theorem 1.1 gives finite
`w(w(G))` under fewer-than-continuum word values on any profinite group. The
statement does not require finite generation or countable basing. The target
uses precisely that conclusion, not strong conciseness of all words. This
audit accepts the cited theorem as an external mathematical input; it is not
a new proof or formal verification of that theorem.

The freshly read [Abért primary v1](https://arxiv.org/pdf/math/0306364v1),
Theorem 1, establishes law-freeness from a separating action. The first part
of Corollary 4 gives abstract free subgroups of every finite rank almost
surely in a profinite weakly branch group. Bounded tree degree and finite
generation occur only in its subsequent dense-free-subgroup assertion.
The target does not import those unnecessary restrictions or claim density.

## Universal law: independent proof and boundaries

Let `w` be a nonidentity element of `F_k`, with finite `k>=1`. Write
`K=w(G)` and `F=w(K)`. By the external theorem `F` is finite. Its exponent
is a positive integer `e`, with `e=1` permitted for trivial `F`.

For each `i=1,...,k`, let `A_i` be the free group on a disjoint block of
`k` symbols and `w_i` the copy of `w` in `A_i`. Each `w_i` is nonidentity
and has infinite order. The canonical map

`<y_1> * ... * <y_k> -> A_1 * ... * A_k`, `y_i -> w_i`,

is injective: after collecting maximal consecutive powers of each `y_i`,
the image of a nonempty free-product normal form has nonidentity syllables
in distinct adjacent factors. Thus the image `u=w(w_1,...,w_k)` is
nonidentity. A free group is torsion-free, so `v=u^e` is nonidentity.

On evaluation in `G`, every inner value lies in `K` and the outer value
lies in `F`; its `e`-th power is the identity. Therefore `v` is a
nontrivial group law on `G`. No statement that `w(G)` itself is finite
has been used.

Boundary checks:

- For `k=1`, `w=x^n` with `n!=0` and `v=x^(n^2 e)`, a nonzero power.
- Variables unused by `w` cause no failure: every renamed `w_i` is still
  nonidentity and each block remains disjoint.
- The identity word is excluded from the external definition and from the
  nontriviality assertion. Its value set is `{1}`, so it cannot witness an
  infinite small word-image counterexample in any event.
- Rank zero has only the identity word and belongs to the preceding boundary.
- `G=1` or `F=1` causes no problem; the constructed formal word is nontrivial
  even when its evaluation is universally the identity.

A continuous epimorphism maps the set of `w`-values onto the quotient's
set of `w`-values, and laws also descend to quotients. Thus a group with a
law-free profinite weakly branch quotient cannot satisfy the small-word-image
hypothesis for a nontrivial `w`. This is a valid exclusion, not an inference
that all remaining law groups have finite word image.

## Every nonidentity weak-branch conjugacy class

Let `B` satisfy the target's exact hypotheses. The automorphism group of
a locally finite rooted tree is profinite, and closed `B` is profinite.
For each vertex `v`, its rigid stabilizer `R_v` is the intersection with
`B` of point stabilizers outside the subtree at `v`, so is closed.

There are arbitrarily large finite collections of pairwise disjoint
descendant subtrees of `v`. For each of `n` of these choose a nonidentity
element of its nontrivial rigid stabilizer. Their supports are disjoint,
they commute, and all `2^n` products choosing or omitting each one are
distinct: restrict a putative product identity to a subtree whose element
was selected. Hence `R_v` is infinite. It is therefore an infinite
profinite group, of cardinality at least continuum.

For any `g!=1`, faithfulness supplies a vertex `v` with `g(v)!=v`.
The two vertices have equal level, so their rooted subtrees are disjoint.
Conjugation carries `R_v` to `R_g(v)`. If `r in R_v` commutes with `g`,
then `r` belongs to both rigid stabilizers; disjoint support and
faithfulness give `r=1`. Consequently `C_B(g) intersect R_v=1`.

For `r,s in R_v`, equality `r^-1 g r=s^-1 g s` implies
`s r^-1 in C_B(g) intersect R_v`, so `r=s`. The conjugation map on `R_v`
is injective. Every nonidentity conjugacy class has at least continuum
elements. Simultaneous conjugation preserves word values, so any word
having one nonidentity value has at least continuum values. The argument
does not require that the root flip or any prechosen automorphism be a
word value. The trivial word and nontrivial laws both give the singleton
value set `{1}` and are consistent with this proof.

## General abstract-free-subgroup exclusion: cardinality clarification

The target's independent abstract-free-subgroup argument is correct.
A nonabelian free subgroup contains copies of every finite-rank free group,
so every nontrivial word has a nonidentity value `g` in it. Such a `g`
has infinitely many conjugates inside that free subgroup: its centralizer
is cyclic and has infinite index. Its ambient conjugacy class is therefore
infinite.

The sentence passing from this infinite compact conjugacy class to
continuum cardinality must be read using the **homogeneous orbit structure**,
not mere compactness. An arbitrary infinite compact profinite space can
be countable. In this setting the conjugacy class is homeomorphic to
`G/C_G(g)`, because the continuous orbit map from that compact quotient
to the Hausdorff orbit is bijective. This quotient is a homogeneous
profinite space. An isolated point would make all its points isolated;
compactness would then make it finite. Thus the infinite quotient has
no isolated points. Recursively split nonempty clopen sets into two
nonempty clopen subsets; compactness gives a point for each infinite
binary path, with distinct paths giving distinct points. The resulting
cardinality is at least continuum. Alternatively, the contrapositive of
Shumyatsky's cited Lemma 2.4 supplies this conclusion directly.

This supplies the reasoning for an already true claim. It is an
explanatory clarification, not a counterexample or substantive failed
inference.

## Independent bounded controls

Run `python3 independent_checks.py` in this directory. The standard-library
checker imports no author code. It passed:

- 9,082 nonempty freely reduced input words, with 27,246 positive-power
  controls after disjoint-block self-substitution; conjugated and unused
  variable boundary controls are included.
- 336 finite-group law constructions in `S_3` and the order-eight dihedral
  group, with 10,410 outer-value exponent checks.
- 512 disjoint-support instances in the depth-three full binary-tree
  automorphism group, with 1,792 injective-conjugation checks.

These are falsification controls, not substitutes for the preceding
unbounded proofs. No finite wreath word-image enumeration is certified
by this secondary audit. The remaining unrestricted law-group problem
is not resolved here.
