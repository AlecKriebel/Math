# Fresh V3 transfer, scope, and priority review

Checkpoint: 2026-10-07 05:19 UTC (2026-10-06 PDT). Assigned mathematical
transfer/scope review completion estimate: 100%; assigned publication-scope
and priority review completion estimate: 100%. These percentages describe
this slice, not the complete upstream proof or production publication.
No external individual was contacted. No candidate, upstream, Git, deposit,
or tracker state was changed. Writes were confined to this review and
`checks/package_review_3/scope/`.

## Exact version and independence

I first read the original human request in the attached `Pasted text.txt`,
`/Users/alec/Documents/Math/AGENTS.md`, frozen `manuscript/main.tex`, the
primary Bülles/Markman/Arapura texts, and the pinned companion statements
and pertinent proof sections. I derived the correspondence degrees and
the non-fine normalization before reading the earlier review opinions.
Only after that pass did I reconcile `agent_notes/bulles_transfer.md`,
`agent_notes/priority_audit.md`, `reviews/scope_transfer_v2.md`, the relevant
parts of complete reviews 1 and 2, both response documents, the triage
section 8 and its geometry notes, and the actual archived counterparts.
I was not asked to reconstruct the full upstream analytic/CM geometry,
which is a separate review obligation.

The independently checked candidate hashes are:

| File | SHA-256 |
|---|---|
| `manuscript/main.tex` | `f9566f03e925bc2cff721fc80d231276733a4540d27450589da98df6c229cfe8` |
| `publication/upload-kit/paper.pdf` | `483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612` |
| `publication/upload-kit/source-and-verification.zip` | `8f44cd5f9c447e40a97a07a3bcc62998accdb7aad4fce94b4020c5fe87f77ce0` |
| `zenodo-deposit.json` | `e8236c37dfd400a5aa6b68cbaf9db39443cff37044812f8167fd58b79c4fad8d` |
| `publication/README.md` | `4800c02267767ab92d909a9635cbafe4dd256e3a0912e6efe095aacee5fd398e` |

These agree with the V3 snapshot. Small source/query and archive-hash
evidence is retained in `checks/package_review_3/scope/current_snapshot.json`.

## Verdict and exact remaining dependency

No substantive error in the V3 transfer, hypotheses, boundary cases,
scope claims, companion attribution, or corollary-level priority framing
was identified. The proof correctly invokes the mixed-K3 theorem; it does
not obtain the universal result from separate self-power statements.
The exact twisted/non-fine construction can be interpreted in rational
algebraic Chow groups, with the required multiplicity and divisor
normalizations. The source's printed shorthand must not be read literally
as a formula for an arbitrary unnormalized quasi-universal Ext complex.

The strongest independently established conclusion in this slice is:
**rational HC on all actual mixed products of the K3 bases implies rational
HC on all eligible mixed moduli products**. The unconditional conclusion
still imports OpenAI's mixed-K3 theorem with all its geometric and CM
dependencies. This scoped review does not supply an independent proof of
that input and cannot replace its separate complete-package audit. There
is no additional unsupported transfer assertion identified here.

The contribution has very low independent originality. The restricted
moduli/self-power template is an exact earlier disclosure in the quadratic
companion; unrestricted single-base consequences are already implicit
after universal exact KS. The different-base assembly is not explicitly
printed in the inspected companion corpus, but is immediate from the
published mixed-K3 premise and established splitting. No claim of being
first, discovering a new reduction, or independently solving the base
conjecture is justified. V3 makes none of those claims.

## Primary transfer theorem and eligibility

[Bülles, arXiv:1806.08284v1](https://arxiv.org/pdf/1806.08284v1), Theorem
0.1, printed p. 1, assumes a complex projective K3 or abelian surface,
a Brauer class, and either a smooth projective Gieseker-stable twisted-sheaf
moduli space or a smooth projective stable-object moduli space for a generic
stability condition. Its conclusion is a summand of a finite sum of
Tate-twisted motives of powers of the surface, with exponents between one
and the dimension for positive-dimensional moduli. The theorem has no
separate fine-moduli or primitive-vector condition. V3 uses the K3 case
only and fixes the sheaf/polarization or numerical/stability data.

In particular, genericity is relative to the numerical problem; it does
not make the base K3 very general, and it does not guarantee projectivity
of every open stable locus. A nonprimitive vector can leave strictly
semistable objects; V3's actual smoothness and projectivity assumptions
remain essential. The qualification that objects are those covered by
Bülles' theorem is retained in the theorem and supporting metadata.

I read Bülles §2.1, printed pp. 5–7. The mechanism factors each positive
Chern-character component through one surface, closes the factorization
ideal under intersection by exterior products and diagonal pullback, and
expresses the diagonal as the weighted top-Chern polynomial. The number
of factors in a monomial is at most the moduli dimension. This supplies
the splitting and its exponent bound, rather than merely a surjection of
unidentified Hodge structures. Finite-dimensionality is a separate
conditional corollary and is unnecessary here.

I also read [Marian–Zhao, arXiv:1711.10045v3](https://arxiv.org/pdf/1711.10045v3),
printed pp. 2–4, which describes the stable-complex diagonal mechanism
referenced by Bülles Remark 2.1. Objects in a common stability heart have
the needed Ext amplitude; stability and K3 Serre duality give the highest
Ext and dual cokernel as lines on the diagonal. The virtual rank is
`m−2`. Although Marian–Zhao's main zero-cycle theorem is stated with a
primitive vector, those local diagonal conditions do not use primitivity.
Bülles' own splitting theorem imposes none. This is not an extension to
arbitrary spaces lacking the eligible moduli gerbe/perfect-family setup.

## Re-derived cycle proof and boundary cases

For `A in CH^a(X x K)` with `D=dim X`, its cohomological action shifts
`(p,p)` to `(p+a−D,p+a−D)`. A return cycle `B in CH^b(K x X)` has
composite codimension `a+b−dim K`. Thus actual split correspondences
give, term by term,

    a_j+b_j=D+N_j,   sum_j B_j o A_j=Delta_X,
    N_j=dim K_j.

For a Hodge class `z` of codimension `p`, set `q_j=p+a_j−D`.
Its image is a rational Hodge class of codimension `q_j` on `K_j`.
If that degree lies in `[0,N_j]`, HC supplies a representing cycle;
otherwise the target group is zero. Returning that cycle gives

    q_j+b_j−N_j=p.

Compatibility of cycle classes with proper pushforward, pullback and
intersection proves that the sum of the returns has class `z`.
This independently confirms V3 lines 99–143. Bülles' printed twist sign
for one map is opposite to the Hom convention in his §1; V3 avoids that
source bookkeeping issue by using the actual cycle codimensions.

Exterior products commute with composition of correspondences. Their
codimensions and the source/target dimensions add. Expanding the product
of the individual diagonal identities therefore gives the diagonal on
the moduli product through precisely the varieties
`product_i S_i^{k_ij}`. All cycle classes have even total degree, so there
is no omitted Koszul sign. OpenAI's mixed-K3 Theorem 1.1 includes every
such different or repeated base. Separate self-power HC cannot justify
this step. Conversely `S^[1]=S` makes the universal target imply the base
mixed-K3 assertion, so the equivalence stated in V3 is correct.

The zero-dimensional case is handled directly as finitely many complex
points; it cannot satisfy the literal positive exponent range or the
positive-dimensional Markman lemma. An empty factor is vacuous, no
factors give a point, and out-of-range cohomology targets are zero.
The ideal-sheaf vector `(1,0,1−n)` gives `S^[n]` for positive `n`;
`n=0` is a point and `n=1` is the surface. The two-dimensional isotropic
case has virtual rank zero but is covered by Markman's `m>=2` lemma.
No boundary case silently needs an integral normalization.

## Non-fine and twisted normalization: actual check

[Markman, arXiv:math/0009109v4](https://arxiv.org/pdf/math/0009109v4),
Theorem 1 initially assumes universal families. His Lemma 4, printed
pp. 6–11, is the geometric blow-up/Porteous Chern calculation; the
three-term complex has outer line supports on a smooth codimension-`m`
locus, virtual rank `m−2`, and for even `m` top Chern class that locus.
I read those hypotheses and the proof's algebraic Chern/pushforward
operations. Section 3, printed p. 12, is the normalization for
semi-universal data, using a Brauer–Severi bundle and an auxiliary bundle.
Its cohomological presentation can be interpreted in rational Chow
groups using the same algebraic lemma and injective rational pullback;
it is not legitimate to infer a Chow splitting only from an unspecified
cohomological projector.

A concrete falsification of the raw shorthand is `M=S`, parametrizing
skyscraper sheaves, with universal family on the diagonal. Its relative
Ext virtual class has `c_1=0` and `c_2=Delta_S`. Duplicating both universal
families gives four copies of that virtual class and therefore
`c_2=4 Delta_S`. A quasi-universal family can have precisely that
multiplicity. The literal unnormalized display cannot be the intended
diagonal formula. V3 lines 178–186 explicitly recognize the issue.

The multiplicity normalization follows directly from Markman's bundle
relations. Locally `F=E_i tensor V_i^dual`, with `rank V_i=rho`. The
bundles `W_i=V_i^(tensor rho) tensor (det V_i)^dual` glue; `rank W=rho^rho`.
The root of `ch(W^dual)` is chosen with constant coefficient `rho`, not
one. Dividing the quasi-universal character by that root removes the
family multiplicity and its auxiliary-bundle dependence. On the
associated Brauer–Severi cover, put `h=c_1(O_P(rho))/rho`. The relations

    p*F=Vtilde(1)^dual tensor Etilde,
    p*W=Vtilde(1)^(tensor rho) tensor O_P(-rho)

force the normalized character to pull back as
`ch(Etilde) exp(-h)`. Markman's intermediate sentence prints a plus sign
instead. I inspected the actual p. 12 image as well as its text: it is
an internal sign inconsistency with the displayed relations and equation
(27), not an alternative convention. The normalization equation fixes
the needed sign. The archived transfer supplement already explicitly
identifies this issue and uses the minus sign; no wrong formula is
propagated into V3.

For the twist on the K3 base itself, choose a positive-rank locally free
`alpha`-twisted sheaf `A`, of rank `s`, from an Azumaya representative.
Set

    b=sqrt(ch End(A)), b_0=s,
    q_A(E)=ch(E tensor A^dual)/b.

The numerator is an untwisted perfect complex and hence an algebraic
Chow class. Roots and division are finite rational expressions in the
nilpotent ideal of positive codimension. This remains valid when `E`
itself has rank zero. Since `End(A)` is self-dual, the sign involution
fixes `b`. Ordinary tensor cancellation then gives

    q_A(E)^dual q_A(F)=ch(E^dual tensor F).

This identity is a direct check of the supplement's algebraic twisted
character, not a use of a transcendental B-field as a cycle. GRR therefore
still factors the relative Ext character through the two surface factors.
Combining the base-twist character with the quasi-universal correction
gives

    Q=q_A(F) ch(W^dual)^(-1/rho),
    p*Q=q_A(Etilde) exp(-h).

On `P x P`, the support locus is `Z=P x_M P`, smooth of codimension `m`.
The actual relative Ext class satisfies the line-support, dual-support,
and virtual-rank hypotheses of Lemma 4. Line twists preserve them.
Polynomial dependence on integral powers of `O_P(rho)` extends the
unchanged top-Chern identity to the rational divisor exponential above.
Equivalently, for virtual rank `m−2`, the Chern polynomial identity is
`c_m(T exp(ell))=c_m(T)−ell c_(m−1)(T)`; the latter Chern class vanishes
by the lemma. Thus the normalized diagonal survives the correction.
Rational pullback is injective because `p_*(h^(rho−1))=1`, with the
analogous product formula and projection formula. The diagonal identity
descends in rational Chow groups.

Finally, each positive-degree GRR component factors through one `S`.
The top Chern polynomial has weighted degree `m`, so each monomial
factors through at most `m` copies of `S`. This recovers the actual
splitting used in V3. It repairs the raw source display without adding
a stronger unsupported hypothesis. Accepted standard inputs here are
existence of the eligible quasi-universal/perfect families and Azumaya
representative, GRR, rational Chow/projective-bundle functoriality and
Markman's geometric Chern lemma. I did not reconstruct general moduli
existence or the foundational proof of GRR.

## Companion dependency and exact duplication

The pinned quadratic companion's theorem `ext:criterion`, source lines
151–161, assumes only a projective K3 and one algebraic exact
full-even-Clifford map `v -> (a -> vaw)` with rational nonisotropic `w`.
There is no quadratic-locus embedding assumption in that criterion.
I read its ordinary-HC proof, especially source lines 366–633 and
674–846. Alternated exact Clifford compositions inject exterior powers
by PBW and invertibility of `w`. Polarization, transposition and a
finite-dimensional polynomial inverse give algebraic returns from
degree two on an abelian square; Lefschetz (1,1) then algebraizes the
exterior Hodge vectors. The subsequent Zarhin/invariant-theory argument
uses those exterior volume tensors, algebraic endomorphisms/pairings,
and rational coefficient descent to generate all self-power classes.
It does not quietly retain the locus condition in the proof. The
standard foundations accepted for this scope check are PBW, Hodge–Riemann,
Lefschetz (1,1), Zarhin's group description, Buskin's isometry theorem,
and the cited invariant-theory spanning statements; this review is not
a reconstruction of each foundational theorem.

Corollary 9.5, source lines 5216–5255, *does* retain the rational isometric
embedding `T_S -> V_P`. It explicitly states HC/GHC for the indicated
Hilbert schemes, twisted sheaf and generic Bridgeland moduli, every
self-power, and appropriate birational hyperkähler models. Its proof
already tensors Bülles' split correspondences and invokes Arapura.
This is exact template duplication, not merely similar terminology.

The universal KS companion's main theorem, source lines 109–121, supplies
the prescribed exact full-even-Clifford tensor for every projective K3,
including transported isogenous models. Combining it with the preceding
unrestricted criterion removes the base restriction for the existing
single-base moduli consequences. Products of different eligible moduli
on one fixed base are also immediate from that same source-power
argument, whether or not separately printed. These consequences cannot
be advertised as the present note's independent discovery.

The mixed-K3 companion's Theorem 1.1 explicitly permits arbitrary distinct
or repeated surfaces. Its introduction describes the additional joint
Hodge-group and central-sign work that cannot be replaced by self-power
HC. I inspected the main statement and searched its actual manuscript
files and the universal companion for moduli/Hilbert/Bülles consequences;
their uses of moduli terminology concern source constructions, not an
arbitrary-different-base mixed-moduli theorem. A read-only search across
the entire upstream `preprints/` TeX corpus for Bülles and mixed-moduli
HC statements found the quadratic companion as the relevant template.
This is a bounded corpus result, not an exhaustive novelty certificate.

[Arapura math/0102070v5](https://arxiv.org/pdf/math/0102070v5), Theorem 5.4,
printed pp. 20–21, transfers HC/GHC to a length-`n` surface Hilbert scheme
from surface powers through `n`. Theorem 5.7(3), printed pp. 21–22, treats
components of torsion-free sheaf moduli when the stable and semistable
loci agree and all base powers satisfy the conjecture. Its proof uses
Markman's quasi-universal cohomology generators. The V3 attribution does
not incorrectly assign it Bülles' full twisted/Bridgeland scope.
[Arapura math/0501348v3](https://arxiv.org/pdf/math/0501348v3), Lemma 4.2,
printed pp. 9–10, transfers the listed conjectures to all powers of a
motivated variety; Theorems 7.4 and 7.8, pp. 16–17, cover Hilbert schemes
and projective stable torsion-free sheaf moduli. I read those proofs and
their reliance on diagonal/cohomology generation. V3's locators and
attribution are accurate.

## Current primary searches and public-priority limits

Fresh searches on 2026-10-06 PDT/2026-10-07 UTC included the exact candidate
title and combinations of rational HC, mixed/finite products, K3 moduli,
Bülles, Arapura and KS. I opened the primary arXiv version pages and
actual PDFs specified above. No search result supplied a verified exact
duplicate of the arbitrary-different-base mixed-moduli statement.
Search absence is not proof of novelty.

The GitHub primary repository and `commits/main` APIs were checked afresh
at 05:17:13 UTC. The public main commit remains
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with no parents or later
correction commit. Repository creation is 2026-10-06 21:47:02 UTC;
commit time is 21:58:50 UTC; push metadata is 22:01:11 UTC. These establish
current public access and the pinned version, not the earliest public
visibility time or absence of an earlier release elsewhere. V3 properly
calls its manuscript dates cover dates and supplies an access date.
The upstream README itself cautions that unformalized papers may have
issues; publication status is not proof.

I reopened the earlier broad claim
[Bhattacharjee–Bhattacharya v3](https://www.preprints.org/manuscript/202602.0462/v3),
posted 23 July 2026. Its Theorem 18 incorrectly treats all `H^2` as divisor
classes and all hyperkähler manifolds as K3-Hilbert deformations. These
specific failed deductions agree with the archived priority note.
The latest [v5](https://www.preprints.org/manuscript/202602.0462), posted
5 August 2026 under the title *Relative Secant Cycles and Hodge Classes*,
also claims universal HC. Its §8.6 assumes algebraic KS correspondences
from Deligne/canonical models and treats odd Clifford multiplication as
acting within the even algebra. Those steps do not give the required
exact algebraic tensor. I did not audit its entire universal argument.
It is an earlier broader claim to record, not a verified duplicate
solution or a valid source input for this note. V3 makes no first claim.

The triage REPORT §8 and geometry notes correctly downgrade originality
for this same duplication chain. They do not identify a counterexample
to the transfer. Their optional cubic/Fano and birational suggestions
were not included in V3; none is needed to repair this core note.

## Reconciliation of historical reports and V3 metadata

The ZIP's `audit/bulles_transfer.md` is byte-equal to the project report
(21968 bytes; SHA-256
`b208467a70375cdc0618add31d0027225ee392e3dc1b30c22d1cf175ec2a749d`).
Its normalization explicitly uses the correct minus sign and explains
the raw-duplication counterexample. Its historical unconditional `0%`
estimate means that its transfer-only route did not prove the mixed-K3
input. It does not prove that the source theorem is false. That route
is correctly blocked if used alone, because it moves the task to an
equivalent universal assertion. Separate source-proof audits, not a
priority verdict, are required to discharge that input.

The ZIP's `audit/PRIORITY_AUDIT.md` is byte-equal to the project priority
report (15474 bytes; SHA-256
`ffaf03454898d0215ab015f4f410a8eaa987603a7b399b9a86275290ebfb951a`).
Its very-low-originality conclusion and version-specific v3 broader-claim
record are historically accurate; current v5 evidence is recorded above.
The conditional-transfer supplement is likewise consistent with the
explicit implication and does not claim unconditional closure alone.

`scope_transfer_v2.md` independently checked this same normalization and
scope, including the Markman sign issue. This fresh check agrees for
the mathematical reasons given above, rather than merely because its
verdict was favorable. Reviews 1 and 2 identified no different transfer
or priority objection; their requested documentary/reproduction repairs
are separate obligations. Response 1 preserves the early audits' limits
and adds the completed source obligations and scripts. Response 2
corrects the queued-editor description and stale transcription wording.
The V3 current theorem and README now use the corrected wording; no
theorem or hypothesis changed in those repairs.

The reviewed title, abstract, provenance paragraph, README and intended
Zenodo description all say that the work combines cited results and
records an assembled corollary. They consistently credit the base
mixed-K3 theorem to OpenAI, the exact motive reduction to Bülles, and
the earlier conditional transfers to Arapura. Supplied upstream citation
blocks are retained rather than attributing the result to an anonymous
commit author. Smoothness, projectivity, eligible stability and Brauer
scope are consistent. None of the prohibited integral/generalized HC,
singular-moduli, all-abelian-base, arbitrary-deformation or
finite-dimensional-motive claims appears. AI use and absence of
conventional human refereeing are disclosed.

No necessary change to frozen V3 is requested within this slice. If an
exact already-public mixed-moduli theorem with a valid proof is later
found, the human's explicit duplication condition must be reconsidered.
This review does not certify exhaustive priority, the full upstream
unformalized geometry, a DOI, remote files, or tracker completion.
