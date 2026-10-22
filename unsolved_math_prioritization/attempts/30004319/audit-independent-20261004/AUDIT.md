# Independent adversarial audit: problem 30004319

Date: 2026-10-04 (UTC). Target: OWR-17295-003, rank 602.

## Verdict

**PASS as an unsolved, five-approach partial-results checkpoint.** No mathematical
correction is required to the frozen release. This is not a proof or a
counterexample to the original open problem. The correct disposition remains
`unsolved`, `5/5`, with no novelty or prior-resolution claim.

The audited release contains 17 files including its manifest. The manifest's
SHA-256 is
`0976c70b467a4341514e5aa1c30ca54e88c34a9636a23921312f285b9ed2b396`.
All 16 entries verified before and after this audit. No release file was edited.
No repository, pull-request, queue, or other remote write was performed.

All three supplied programs replayed byte-for-byte. A separately written,
coordinate-based exhaustive implementation also reproduced every main count,
the full list of 576 survivors, and the hash of the intermediate 3,900 tables.
The essential distinction between necessary ring identities and a faithful full
six-root graded-group realization is correctly maintained throughout.

## 1. Exact target and source verification

The [original report](https://ems.press/content/serial-article-files/46832),
printed p. 3261, asks whether every ring parametrizing an A2-graded group is
alternative. The nearby C3 result and the 5-plump-polygon special case do not
answer that question.

I inspected the relevant full-text sections of
[Wiedemann's monograph](https://arxiv.org/abs/2404.02042v1): Definitions 2.1.4,
2.1.20, 2.2.2, 2.5.2, 5.1.1, 5.1.9, 5.1.12, and 5.6.2; Examples 5.6.5 and
5.6.9; Proposition 5.6.6 and Remark 5.6.7; and the statements 5.3.3, 5.6.10,
and 5.6.11. These cover the ring, root relations, standard signs, strong inverse,
Weyl element, and nondegeneracy conventions actually needed here. They agree
with `EXACT_TARGET.md`. The monograph explicitly leaves the unrestricted A2
problem open. Its rank-at-least-three result cannot be specialized to A2.

The precise unit-Moufang parentheses on printed p. 129 were checked against the
page image as well as extracted text. The checkpoint accurately attributes the
input to Remark 5.6.11 and its reference to Faulkner's Theorem 13.8. This audit
does not independently reprove or certify Faulkner's original proof.

Full-group axiom coverage is complete: nontriviality, generation, commutator
relations, Weyl elements, and intersections with positive-system subgroups.
The unital nonzero-ring convention is appropriate because all coordinate maps
are additive isomorphisms onto nontrivial root groups. No division, finiteness,
extra stability, characteristic restriction, or linear representation has been
inserted.

The five private PDFs and selected source-record JSON match their listed
SHA-256 values. I did not redistribute their text or images. The original
catalogue endpoint remained unavailable through the web tool; this does not
undermine the independently inspected original report. I did not independently
refresh the repository's duplication/queue state or recompute the full imported
corpus hashes; those are provenance observations rather than mathematical
premises of this audit.

## 2. Lemma 1 and Proposition 2: strong units and nuclear translates

**Accepted relative to the explicitly cited unit-Moufang theorem.**

The definition of strong inverse requires a single ring element whose left and
right multiplication maps are the respective two-sided inverses. It is not
replaced by two ordinary product equations or by unrelated inverse linear maps.
The three displayed Moufang identities are correctly transcribed.

Setting the middle parameter to the unit in the first two identities gives the
left and right alternative laws with the repeated argument equal to the strong
unit. This substitution neither cancels a ring factor nor divides by 2.

For `a=u+n`, trilinearity of the associator expands either repeated-argument
associator into four terms. One is the strong-unit term and the other three
contain the nuclear element. Every term vanishes, including in characteristic
2. The nucleus assumption is used in all required slots. Integer multiples of
the two-sided identity are nuclear by distributivity. The `a` or `1-a` special
case is valid because the negative of a strong unit is again strong, with the
negative inverse. In the division special case, "division" must retain the
source's strong-inverse convention; the checkpoint does so.

The stated gap is genuine: additive generation by units does not remove the
mixed terms in a diagonal associator. There is no proof here that the full
grading forces the stronger sumset condition `R=R^×+N(R)`.

## 3. Positive-root and naive-representation controls

**Proposition 3 accepted.** The two associative parenthesizations in H(R) differ
only in the cocycle expression, and distributivity makes these equal. Both
sided inverse formulas are correct. With the stated commutator convention,
the root commutator has parameter `ab`, not `-ab`. The three root embeddings
and the adjusted third coordinate in the factorization are faithful.

This construction works for arbitrary distributive ring multiplication because
there is no nested ring product in the cocycle identity. It therefore gives the
claimed obstruction to a positive-root-only argument, while leaving every
negative-root and Weyl obligation open. A2 has no positive-root chain with
both intermediate sums and the length-three total still roots; A3 does.

**Matrix/Lie calculation accepted.** Direct expansion of the cyclic Jacobi
expression gives the three cyclic associators on distinct diagonal entries.
Thus imposing Jacobi on that particular full matrix commutator structure would
force associativity. The analogous left-operator shear relation likewise
requires `L_a L_b=L_ab`, which becomes associativity on evaluation. The text
correctly limits these objections to the specified constructions rather than
claiming that all possible Lie-theoretic routes fail.

## 4. The explicit rings R0 and R1

**Both witnesses accepted with their stated limitations.**

For R0, the multiplication matrices and determinant formula are correct. The
only elements with both multiplication operators bijective are `1`, `1+e`,
and `1+f`. The latter two have the displayed ordinary inverse, but each fails a
required operator-inverse identity. Hence only `1` is strong. The two written
alternative-law failures are correct. Consequently R0 really does show that
the unit-Moufang test alone is insufficient.

The witness `a=e,b=f,c=e,t=1` violates (Z) in R0, so it cannot coordinate a full
group with these injective root maps. This conclusion uses the proved
obstruction below and is stronger than merely calling R0 an unconstructed
candidate.

R1 is nonalternative, has only the strong unit `1`, and passes (Z). These facts
were checked both by the supplied independent witness implementation and by
the new exhaustive audit. Neither ring is silently promoted to a counterexample:
R0 is excluded, and R1's full-group existence remains unproved.

## 5. Lemma 4 and Proposition 5: opposite-root compatibility

**Accepted without a characteristic or associativity assumption.**

I checked the indices, multiplication order, and all four root-injectivity uses.
If `X=x12(a)` and `Y=x21(d)` commute, the required same-row or same-column
commutations yield the following chains:

1. Y centralizes X and x23(t), hence x13(at); its commutator there has parameter
   `d(at)` in U23.
2. Y centralizes x31(t) and X, hence x32(ta); the commutator of x32(ta) with Y
   has parameter `(ta)d` in U31.
3. X centralizes Y and x13(t), hence x23(dt); the resulting parameter is
   `a(dt)` in U13.
4. X centralizes x32(t) and Y, hence x31(td); the resulting parameter is
   `(td)a` in U32.

The commutator of two elements centralized by a third is also centralized by
that third in every group. No Hall–Witt simplification or unstated nilpotency
assumption is needed. Injectivity converts each identity root element into its
zero ring parameter.

For Proposition 5, `ab=ca=0` makes x12(a) centralize both x23(b) and x31(c).
Their commutator is exactly x21(bc). Substituting `d=bc` into Lemma 4 gives
all four equations with precisely the displayed parentheses. If bc is strong,
the specialization t=1 allows cancellation by its inverse operator. Only this
explicit strong-unit implication is asserted.

The code checks the implication on all a,b,c,t. Restricting only to basis
vectors would be invalid because its zero-product hypotheses are nonlinear;
no such restriction is made.

## 6. Proposition 7: full universal-presentation equivalence

**Accepted. No missing realization hypothesis is being concealed.**

For the forward implication, a realized coordinated group is a quotient of S(R).
If a coordinate generator is trivial in S(R), its faithful image in the quotient
forces its parameter to vanish. If an element of one root image belongs to a
positive-system subgroup in S(R), the same is true in the quotient; its
nondegeneracy and coordinate injectivity again force the parameter to vanish.
The quotient need not itself be faithful on the whole of S(R).

For the converse, generation and the required commutator inclusions follow
from the relations. Assumption (I) makes the six images faithful and nontrivial.
Assumption (N) is the remaining grading axiom. The only issue requiring a
calculation is the existence of Weyl elements, and it is valid without ring
associativity.

Here is a direct audit expansion for `p=x21(-1)`, `q=x12(1)`, and `w=pqp`.
Each arrow is conjugation successively by p, q, p. Factors combined or cancelled
in these lines share a row or column and therefore commute:

- x13(a) → x13(a)x23(a) → x23(a) → x23(a).
- x23(a) → x23(a) → x23(a)x13(-a) → x13(-a).
- x31(a) → x31(a) → x31(a)x32(a) → x32(a).
- x32(a) → x32(a)x31(-a) → x31(-a) → x31(-a).

These follow from `g^h=g[g,h]`, the defining root relations, and multiplication
by `1` or `-1` only. For example,
`[x13(a),x21(-1)]=x23(a)` follows by reversing the defining commutator whose
value is x23(-a). There is no reassociation of three ring parameters.

The remaining two roots are recovered as commutators:

- x12(a)=[x13(a),x32(1)] maps to [x23(a),x31(-1)]=x21(-a).
- x21(a)=[x23(a),x31(1)] maps to [x13(-a),x32(1)]=x12(-a).

Thus conjugation gives equality with each reflected root image, not merely
containment, since `a↦±a` is surjective. Relabeling indices proves the formula
for every ordered pair i,j. The required Weyl word already lies in
`U_ji U_ij U_ji`. In fact this calculation does not require (I) or (N); those
are needed for faithful coordinates and the nondegenerate grading.

Consequently S(R) being a defined group presentation alone proves neither (I)
nor (N). All 576 surviving tables still lack exactly the obligations stated in
the release. This audit ran no universal-group solver and did not resolve them.

## 7. Replays and independent exhaustive validation

All three commands in `REPRODUCIBILITY.md` completed with exit status 0, and
`cmp` confirmed byte identity of each output with its frozen JSON:

- `finite_algebra_controls.py` → `replay-finite.json`
- `symbolic_controls.py` → `replay-symbolic.json`
- `verify_small_witnesses.py` → `replay-witness.json`

The new `independent_finite_audit.py` imports no release code. It uses explicit
coordinate triples and polynomial coordinate multiplication, a different
lexicographic element ordering, inversion of multiplication permutations to
determine strong units, and all-element associativity tests. It consults the
release JSON only after computing the full results, solely for comparisons.

It independently obtained:

| Quantity | Count |
|---|---:|
| Labelled unital F2³ tables | 4096 |
| Alternative tables | 76 |
| Associative tables | 76 |
| Unit-Moufang tables | 3976 |
| Nonalternative unit-Moufang tables | 3900 |
| Of those, rejected by (Z) | 3324 |
| Nonalternative survivors of both tests | 576 |
| Integer-shift-covered tables | 24 |

The nonalternative unit-test survivor histogram is 3,888 with one strong unit
and 12 with two. The full ordered list of 576 tables matches. The independently
computed hash of the sorted intermediate 3,900-table JSON list is
`095743192830178949bde5381254ffc1b15e4da1e9147c34514f5b114aa7f47d`, matching
the frozen output. Every alternative table passes (Z). The sufficient
integer-shift implication was independently rechecked.

The supplied finite program's positive-group checks accurately describe 512
inverses, 4,096 cocycle cases, and 64 root-commutator cases. They are not presented
as all 512³ associative triples. The supplied symbolic program preserves binary
tree parentheses and performs no hidden reassociation. These controls support
the exact finite and symbolic claims, not a group-existence theorem.

## 8. Literature scope and final disposition

[Voronetsky 2024](https://arxiv.org/abs/2406.03558v1) expressly works in rank at
least 3. Its existence theorem does not address the unrestricted rank-two
question. The inspected 2026 full texts have different targets:
[Weyl-element squares in isotropic reductive groups](https://arxiv.org/abs/2601.14419v2)
and [G2/F4 constructions from cubic norm pairs](https://arxiv.org/abs/2602.06147v1).
Their hypotheses and conclusions do not supply the missing A2 converse.

The [Gvozdevsky 2025 abstract](https://arxiv.org/abs/2505.04749) concerns abstract
isomorphisms for specified group-scheme point groups. The
[Mühlherr–Weiss publisher abstract](https://ems.press/journals/jca/articles/16120)
describes a root-graded-group/Tits-polygon correspondence. Neither abstract is
an unconditional alternativity proof. Neither is represented here as a full-text
proof review.

An independent targeted search also located
[Zezhou Zhang's 2014 dissertation](https://escholarship.org/uc/item/24x1f8n5),
§3.3.2. Its Conjecture 3.3.3 and subsequent conditional discussion are consistent
with the checkpoint, not a new resolution. Search-result dates were not used as
publication dates: the repository cover identifies this work as 2014.

No inspected source contradicts the bounded open-status assessment. This
negative search result is not a certification that no resolution exists
anywhere. The five recorded approach responses remain partial and distinct.
The audit adds verification, not a sixth claimed proof-search response.

**Required corrections: none.** Preserve the frozen manifest. Attach or publish
this separate audit alongside the unchanged release if publication is later
authorized. The release's pending-audit fields describe its historical freeze;
the completed independent status is supplied by this audit and `AUDIT_RESULT.json`.
