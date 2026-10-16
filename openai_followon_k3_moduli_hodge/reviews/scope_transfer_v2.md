# Independent V2 scope, transfer, and companion-statement review

Checkpoint: 2026-10-07 UTC. Assigned transfer/scope review completion estimate:
100%. This is a scoped mathematical review, not a completion estimate or
certificate for the full upstream geometric proof or publication workflow.
No external individual was contacted, and no source, publication, or Git state
was modified. Only this review was written.

## Reviewed version and independence

I read the original human target in the attached `Pasted text.txt`, the current
`manuscript/main.tex`, primary Bülles and Arapura texts, and the actual pinned
companion statements before reading archived project audit opinions. I did not
read `reviews/package_review_1.md` or `reviews/response_to_review_1.md` during
that independent pass. A further independent child reviewer inspected the
Bülles/Markman/Marian–Zhao scope and boundary hypotheses. Subsequently, at the
parent reviewer's request, I reconciled the archived
`agent_notes/bulles_transfer.md` and `agent_notes/priority_audit.md` with the
primary texts and current ledger.

Current manuscript SHA-256:
`f9566f03e925bc2cff721fc80d231276733a4540d27450589da98df6c229cfe8`.
Current dependency-ledger SHA-256:
`b15df71a6e9aa7f9f43e91088abbedf2c26162a81b1a70051a20e6707ca9adbb`.
The read-only upstream clone's HEAD is
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

## Verdict within the assigned scope

No substantive mathematical or exact-scope defect was found in the current
manuscript's transfer. Its statement matches Bülles's stated hypotheses,
its codimension argument is correct, and its product argument really requires
the cited mixed-K3 theorem. The primary source's raw quasi-universal display
requires normalization; the manuscript recognizes this, and the archived
algebraic normalization repair withstands independent checking. The paper's
corollary-level attribution accurately distinguishes the already printed
restricted-locus moduli statement, the implicit unrestricted self-power
consequence, and the mixed-base premise supplied by the mixed-K3 theorem.

This verdict does not verify the central new geometric theorem merely because
it appears in a public release. The strongest result independently proved in
this scope is the explicit implication from rational HC on the actual mixed
K3 source products to rational HC on the eligible mixed moduli products.
The complete-package reviewer must separately assess the upstream proof audits.

## Re-derived correspondence proof

For a correspondence `A` of codimension `a` from a smooth projective variety
`X` of dimension `D` to `K` of dimension `N`, pullback, multiplication, and
pushforward send a rational `(p,p)` class to a rational
`(p+a-D,p+a-D)` class. For a return correspondence `B` of codimension `b`,
composition has codimension `a+b-N`. Thus a split motive summand gives

    a_j+b_j=D+N_j,
    sum_j B_j o A_j=Delta_X.

For a Hodge class `z` of codimension `p`, put `q_j=p+a_j-D`. If
`0 <= q_j <= N_j`, rational HC on `K_j` supplies an algebraic `Z_j` with
class `A_j*z`; otherwise that target cohomology is zero and `Z_j=0` is
legitimate. Every `B_j*Z_j` has codimension

    q_j+b_j-N_j=p,

and `sum_j B_j*Z_j` has class `z`. Projectors and rational Tate twists are
absorbed into homogeneous algebraic correspondences, so no convention for
the name or sign of the Tate twist is needed. This independently confirms
`main.tex` lines 99–143.

For products, exterior products of the split maps commute with composition.
Algebraic cycle classes have even total degree, so there is no unaccounted
Koszul sign. Expanding the product of the individual diagonal identities gives
the diagonal of `product_i M_i`; codimensions and dimensions add. Its source
varieties are exactly `product_i S_i^{k_ij}`, allowing distinct and repeated
bases. The mixed-K3 theorem's main statement explicitly covers these products;
separate assertions about each base's self-powers would not suffice. This
independently confirms lines 145–166.

## Bülles's actual scope and proof mechanism

[Bülles v1](https://arxiv.org/pdf/1806.08284v1), Theorem 0.1, printed p. 1,
states the rational Chow-motive splitting for a complex projective K3 or
abelian surface, a Brauer class, and either a smooth projective Gieseker-stable
twisted-sheaf moduli space or a smooth projective stable-object moduli space
for a generic stability condition. It imposes no separate primitivity or
fine-moduli hypothesis. Its positive-dimensional exponent bound is
`1 <= k <= dim M`; twists are arbitrary integers. The present manuscript uses
only the K3 part and retains actual smoothness and projectivity. Genericity is
relative to fixed moduli data, not a very-general assumption on the K3 base.

In Section 2.1, printed pp. 5–7, Bülles factors positive Chern-character
components through `S`, shows that intersection products of such
correspondences factor through additional copies of `S`, and obtains the
diagonal as a weighted Chern polynomial. Extracting homogeneous terms gives
actual split maps. The weighted degree of the top Chern polynomial bounds
the number of source copies by `dim M`. This mechanism is a proof of the
splitting, rather than only its assertion.

Two printed-source bookkeeping problems do not infect the manuscript.
First, the twist sign assigned to a displayed map in Section 2.1 is opposite
to the Hom convention in Section 1; arbitrary integral twists still exist,
and the manuscript works with actual cycle codimensions. Second, Bülles
introduces quasi-universal data before displaying an Ext diagonal formula
whose literal unnormalized version is false for arbitrary multiplicity.
Markman's normalized rational character must be used.

The latter issue is falsifiable: for `M=S` parametrizing skyscraper sheaves,
the ordinary universal family gives `c_1(W)=0`, `c_2(W)=Delta_S` for
`W=-Rpi_*RHom(E,F)`. Doubling both families gives `4W` and hence
`c_2(4W)=4Delta_S`, not `Delta_S`. The warning in manuscript lines 178–186
is therefore substantive and correct; the proof itself uses the splitting,
not this false substitute.

## Rational algebraic normalization check

[Markman v4](https://arxiv.org/pdf/math/0009109v4), Theorem 1, initially
assumes universal families; Section 3, printed p. 12, uses semi-universal data,
an auxiliary bundle, and injective Brauer–Severi pullback to define a normalized
rational character. Remark 3(1), printed p. 3, explains polynomial invariance
under rational divisor twists. Its intermediate hyperplane-sign display is
not convention-free; the preceding bundle relations and normalization
equation determine the required sign.

The archived repair can be checked directly in rational algebraic Chow groups.
Choose a locally free `alpha`-twisted sheaf `A` of positive rank `s` on `S`
and put

    b=sqrt(ch End(A)),  b_0=s,
    q_A(E)=ch(E tensor A^dual)/b.

The numerator is untwisted and algebraic. All inverses and roots are finite
rational expressions in positive-codimension classes. Since `End(A)` is
self-dual, `b^dual=b`; untwisted tensor cancellation gives

    q_A(E)^dual q_A(F)=ch(E^dual tensor F).

Thus GRR still factors through algebraic correspondences on `S`; no
transcendental B-field exponential has been used. This check also accommodates
perfect objects of rank zero, because the denominator has positive rank.

Locally a quasi-universal family is `F=E_i tensor V_i^dual`, where `V_i`
has rank `rho`. The bundles
`W_i=V_i^{tensor rho} tensor (det V_i)^dual` glue. With the root having
constant coefficient `rho`, define

    Q=q_A(F) ch(W^dual)^(-1/rho).

On the associated Brauer–Severi cover `p:P -> M`, with
`h=c_1(O_P(rho))/rho`, the bundle relations give
`p^*Q=q_A(E_tilde) exp(-h)`. The actual relative Ext complex on `P x P`
has virtual rank `m-2`; its outer support locus is the smooth
`Z=P x_M P`, of codimension `m`. Markman's geometric Lemma 4 gives its
top Chern class `[Z]=(p x p)^*Delta_M`. Twisting the actual families by line
bundles preserves the lemma's hypotheses; polynomial dependence extends
invariance from all integral powers of `O_P(rho)` to the required rational
twists. The class constructed from `Q` therefore pulls back to this same
diagonal. Pullback in rational Chow groups is injective, because
`p_*(h^{rho-1})=1` and the projection formula recovers the source class.
The normalized diagonal descends. The independent child reviewer also checked
the rational-divisor correction directly: for virtual rank `m-2`,
`c_m(T exp(ell))=c_m(T)-ell c_{m-1}(T)`, and Markman's lemma gives
`c_{m-1}(T)=0`. Thus that correction preserves the diagonal exactly. Here
`O_P(rho)` denotes Markman's global line bundle including its determinant
correction, rather than arbitrary unrelated local hyperplane bundles.
The GRR components and weighted Newton polynomial then give the same splitting
through powers of `S`, with `k<=m`.

This validates the archived repair's algebraic content and the current
manuscript's reliance on normalized rational split correspondences. The
existence of quasi-universal/perfect families on the appropriate moduli gerbe
and cover is part of the eligible moduli setup in the cited sources; this
review does not extend the theorem to a space lacking those structures.

## Stable-object and boundary checks

Bülles Remark 2.1, printed p. 7, cites the stable-complex diagonal mechanism
of [Marian–Zhao](https://arxiv.org/pdf/1711.10045v3), printed pp. 2–4.
The common heart and K3 Serre duality give Ext amplitude `[0,2]`, and stability
gives the line-supported highest Ext and the dual cokernel conditions.
The virtual rank is `m-2`. Their main zero-cycle theorem has a primitive-vector
hypothesis, but those local diagonal checks do not use primitivity; Bülles's
own stated theorem adds none. Actual smoothness and projectivity remain
essential, and an open stable locus in a singular projective semistable space
is not automatically eligible.

Markman Lemma 4 expressly permits `m=2`, with rank `m-2=0`, and Remark 3(2)
discusses that case separately. The isotropic-vector, two-dimensional case
has not been silently excluded. Dimension zero cannot satisfy the literal
positive exponent bound, but manuscript lines 168–175 handle it directly as
a finite disjoint union of complex points. An empty factor gives zero cycle
and cohomology groups; no factors give a point. Out-of-range codimensions have
zero target. The ideal-sheaf vector `(1,0,1-n)` identifies `S^[n]` for `n>=1`
with the untwisted stable-sheaf case; `n=0` is a point and `n=1` is `S`.

## Arapura and actual companion scope

[Arapura math/0102070v5](https://arxiv.org/pdf/math/0102070v5), Theorem 5.4,
printed pp. 20–21, transfers HC/GHC to `X^[n]` from the surface powers through
exponent `n`. Theorem 5.7(3), printed pp. 21–22, treats each component of the
torsion-free sheaf moduli when `M=M^s`, the surface is K3 or abelian, and all
surface powers satisfy the relevant conjecture. Its proof uses quasi-universal
cohomology generators. The manuscript's attribution to this conditional work
is accurate and does not claim its full twisted/Bridgeland scope.

[Arapura math/0501348v3](https://arxiv.org/pdf/math/0501348v3), Lemma 4.2,
printed pp. 9–10, transfers the listed conjectures to all powers of a motivated
variety. Theorems 7.4 and 7.8, printed pp. 16–17, cover Hilbert schemes and
projective stable torsion-free sheaf moduli. This confirms the additional
locators cited by the manuscript.

I inspected the actual quadratic-locus source at lines 154–162 and
5216–5255, and verified its PDF numbering: Corollary 9.5 explicitly records
restricted-locus twisted/Gieseker/Bridgeland moduli and all self-powers,
including birational smooth projective hyperkähler models. Its general
exact-tensor criterion is unrestricted in `S`. The universal KS companion's
main theorem, lines 109–121, supplies that precise full-even-Clifford tensor
for all projective K3 surfaces, so the unrestricted self-power consequence
is already implicit in that public dependency chain if its proofs hold.
The universal KS companion does not print a moduli conclusion.

The mixed-K3 companion's introduction, Theorem 1.1, covers arbitrary distinct
or repeated K3 surfaces. I searched its actual manuscript files and the two
other supplied companion texts for moduli/Hilbert/transfer statements. No
arbitrary-different-base mixed-moduli assertion was found there. This is a
bounded corpus observation, not proof of novelty. The manuscript accordingly
claims only an assembled corollary, credits the mixed-base quantifier to the
mixed-K3 theorem, and makes no first-proof or substantial-novelty claim.
The restriction to rational ordinary HC and eligible smooth projective K3
moduli is preserved globally in the reviewed statement.

## Archive reconciliation and minor wording

The earlier transfer note's `0%` unconditional estimate and language about an
unvalidated mixed-K3 input describe that route's original scope and timestamp.
They are not proofs that the input failed. The current ledger explicitly
distinguishes those early limits from its later separate audits, rather than
quietly erasing them. The priority note's low-originality and limited-search
verdict agrees with the current abstract and provenance paragraph.

One minor stale phrase remains in `CURRENT_THEOREM.md`: “to be transcribed
from the primary source” persists despite the precise transcription now in
the manuscript and ledger. It does not affect the theorem or reviewed proof.
An optional precision change to the manuscript would say that the non-fine
diagonal is *interpreted using Markman's normalized rational character*, since
Bülles's printed proof compresses that step. Neither wording item is a
substantive mathematical finding or a necessary repair to this scoped verdict.
