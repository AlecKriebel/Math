# Independent adversarial review of the abelian-extraction obstruction

Review scope: delta1 only. No other 21.122 approach family was read. This
is an audit of a supporting obstruction, not a solution, novelty assessment,
or theorem-closure review. Best-guess progress toward full resolution of
21.122: **0%**.

## Verdict

**Accepted as stated for every odd prime p.** I found no counterexample or
mathematical gap in the construction or in its claimed abelian-subgroup
bound. The exact conclusion is that a metrizable profinite group of
nilpotency class exactly two can have continuum many p-th-power values,
while every abstract abelian subgroup has at most p such values. Closed
abelian subgroups are included. This disproves the proposed general
abelian-extraction implication for a power word.

The input is independently snapshotted in `frozen_inputs/`; source paths,
byte sizes, and SHA-256 hashes are in `INPUT_MANIFEST.json`. The earlier
author checkpoint did not freeze delta1, so this review used its own
initial hashes and verified the sources again at completion.

## Independent algebraic verification

Let V be the countable product of Z/p²Z, let W be the countable product of
Fp, and let C be the product of Fp indexed by pairs i<j. Let q:V→W be
coordinatewise reduction. Set

    β(a,b)_(ij) = q(a)_i q(b)_j,
    (a,c)(b,d) = (a+b, c+d+β(a,b)).

The map β is additive in both variables, because q is additive. Thus

    β(a,b)+β(a+b,t) = β(b,t)+β(a,b+t),

which verifies associativity without any finiteness-of-support assumption.
The identity is (0,0), and the inverse of (a,c) is

    (-a, -c+β(a,a)).

For the convention [x,y]=x⁻¹y⁻¹xy the commutator is

    [(a,c),(b,d)] = (0, β(a,b)-β(b,a)).

It is central. The two coordinate lifts e1,e2 have a nontrivial commutator
in central coordinate (1,2), so the infinite group has class exactly two.
There is no need to identify the *abstract* derived subgroup with all of C;
the statement does not make that stronger claim.

Induction, using additivity of β, gives for every nonnegative integer m

    (a,c)^m = (ma, mc+binom(m,2)β(a,a)).

For odd prime p both p and binom(p,2) are zero as scalars on C, so

    (a,c)^p = (pa,0).

In particular the p-th-power map is a homomorphism here: β(pa,pb)=0 and
p(a+b)=pa+pb. Its image is exactly pV×{0}, and its kernel is pV×C.
The group has exponent p²: p-th powers have order at most p, and a
coordinate lift of 1 in Z/p²Z has order p².

## Infinite-coordinate topology and cardinality

Each output coordinate of multiplication depends on finitely many input
coordinates: output V-coordinate i depends only on a_i,b_i; output
C-coordinate (i,j) depends only on c_ij,d_ij,a_i,b_j. Each inverse
coordinate has the same finite-dependence property. All those coordinate
maps are maps between finite discrete spaces and hence continuous.
The universal property of the product topology therefore makes the group
operations continuous. This addresses the whole infinite product, not
just finite-support elements or a dense subgroup.

For n≥1 let G_n retain a_1,...,a_n and c_ij with 1≤i<j≤n, with the same
product. Restriction G_(n+1)→G_n is a surjective homomorphism. A coherent
sequence specifies every coordinate uniquely; conversely every infinite
coordinate tuple gives a coherent sequence. Any finite list of coordinate
conditions is captured by some G_n. Hence G with its stated product
topology is precisely the inverse limit of these finite groups, and is
profinite and metrizable. Its finite-stage orders are

    |G_n| = p^(2n+binom(n,2)).

Multiplication by p identifies pV with the product of countably many
copies of Fp, via (v_i)↦(p v_i). The latter has cardinality continuum
(binary sequences embed in it, and it embeds in the set of sequences of
integers). Thus the full power image has cardinality exactly continuum
and is a closed elementary abelian subgroup.

## Abstract abelian subgroups: no hidden closure assumption

The projection π:G→W, π(a,c)=q(a), is a homomorphism to an elementary
abelian additive group. For an abstract abelian B≤G, π(B) is therefore an
Fp-vector subspace, regardless of whether B is closed.

If v,w are reductions of two commuting elements, all minors
v_i w_j-v_j w_i vanish for i<j. If v≠0, choose one index k with v_k≠0.
The equations involving k, with their signs reversed when necessary,
give

    w_j = (w_k/v_k)v_j for every j.

This argument uses only one nonzero coordinate and works for arbitrary
infinite sequences. Therefore all elements of π(B) lie in one Fp-line,
unless π(B)=0. Its cardinality is at most p.

The map T:W→pV, T(v)_i=pv_i modulo p², is injective, and the power formula
says (a,c)^p=(T(π(a,c)),0). Consequently the number of p-th powers in B is
exactly |π(B)|, hence at most p. The bound is sharp: the complete preimage
of any one-dimensional subspace of W is closed and abelian and has
exactly p power values. Thus neither passing to closure nor choosing a
maximal abelian subgroup rescues the proposed extraction mechanism.

## Boundary cases and numerical checks

The odd-prime hypothesis is sufficient and is used in the displayed
power simplification. It must not silently be dropped from that formula:
for p=2,n=2, the element ((1,1),(0)) squares to ((2,2),(1)), rather than
((2,2),(0)). Squaring is not a homomorphism in that finite group. This is
a boundary failure of the simplified formula; it is not a counterexample
to the odd-prime claim. The original claim does not cover composite p.
At n=1 the finite stage is abelian (class one); stages n≥2 and the
infinite group have exact class two.

The author's checker was run only from a temporary copy inside this
review directory. It passed and matched its frozen JSON result after
removing the timestamp. Its test scope was correctly limited: p=3,
n=1,...,4, all a with central coordinate zero, and all pairs of reduced
vectors. It does not itself enumerate abelian subgroups or prove the
infinite statement. The absent central-coordinate enumeration in that
checker is justified by the general power formula, but is worth keeping
distinct from a computational check of those coordinates.

The independent stdlib checker also passed. It checked:

- Cocycle identities and the commuting/dependence criterion for p=3 at
  n=2,3, and p=5,7 at n=2, including 153686 reduced cocycle triples.
- Exact repeated p-th powers of all central-zero representatives for
  p=3 through n=5, p=5 through n=3, and p=7 through n=2. Full image
  cardinalities were p^n in every stage.
- Every one of the 243 elements of G_2 for p=3, including every central
  lift, for inverse and power formulas (exponents 0,...,9). All 59049
  ordered element pairs satisfied the exact commutator formula and
  power-map homomorphism identity. The center had order 27 and the full
  power image had order 9.
- All four complete line preimages in that small group. Each was an
  abelian subgroup of order 81 with exactly three power values, so every
  abelian subgroup there is covered without subgroup enumeration.
- The explicit p=2 boundary failures above.

These finite computations supplement the proof. They do not certify
infinite-coordinate continuity, continuum cardinality, or a universal
claim about all profinite groups.

## Strongest verified result and remaining gap

The displayed construction and its abelian-extraction obstruction are
verified. No correction to the author's mathematical statement is
required. An optional explanatory improvement is to spell out the
finite-coordinate continuity argument and to distinguish the finite
checker from the proof of the abstract-subgroup bound.

The obstruction supplies no general mechanism showing that an arbitrary
infinite word image in an arbitrary profinite group has continuum many
values. This example already has continuum many values, so it is not a
counterexample to a finite-versus-continuum dichotomy. No other route to
21.122 was audited, and no full-solution claim follows. Completion of this
narrow audit: 100%; estimated progress toward full resolution of 21.122:
**0%**. No novelty or priority claim was assessed, and no outreach,
publication, or Git action was taken.
