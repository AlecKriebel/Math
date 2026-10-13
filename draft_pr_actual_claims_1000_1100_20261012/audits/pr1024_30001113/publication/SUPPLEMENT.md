# Source, mathematical verification and priority supplement

Companion to *A characteristic-two counterexample to dévissage for local
deformation functors*, Alec Kriebel, 12 October 2026. Reviews and retrievals
took place 12 October PDT / 13 October UTC. Extensive AI use and unrefereed
status apply to both the paper and supplement.

## Target, assumptions and scope

The exact original question is Byszewski's contribution to
[Oberwolfach Report 54/2008](https://ems.press/content/serial-article-files/46200),
printed pp.3038–3040, question p.3039. Earlier/later full formulations are
[the 2009 Utrecht thesis](https://dspace.library.uu.nl/handle/1874/33749),
Question 6.4.4, and [arXiv:1112.0352v1](https://arxiv.org/abs/1112.0352v1),
Question 4.4. They are one question, not separate discoveries.

For a perfect residue field k, a faithful local G-action and normal subgroup
N, the question asks for a prorepresentable F and natural maps from the
actual quotient and invariant-subgroup deformation functors to F, making
restriction–induction into their fibre product formally smooth. Its refined
formulation specifies H^1(G/N,Theta-sharp/Theta^N) as F's tangent space.
Neither question assumes the component functors prorepresentable. Those
assumptions are stated separately in OWR Theorem 3 and arXiv Remark 4.5 /
Theorem 4.9. Their conditional variant is not resolved by this counterexample.

The category is local Artinian W(k)-algebras with identified residue k;
coordinate equivalence is all conjugations reducing to the identity.
Equicharacteristic k-algebras are valid objects via W(k) to k. Nilpotent
constant coordinate terms are allowed, explicitly as in
[Byszewski–Cornelissen (2009)](https://doi.org/10.5802/aif.2450), Section 2.1.
They define continuous substitutions because the constant is nilpotent;
changing to zero-section-preserving automorphisms would change the question.

The candidate uses k=F4, G=(F4,+), N=(F2,+), rho(a)(t)=t/(1+at).
It excludes every prorepresentable recipient and arbitrary natural maps,
including any proposed one-dimensional recipient. It does not require a
Klein-four universal deformation ring, an extension of a map from D_N^Q to
D_N, linear tangent maps, or replacement of actual functors by versal hulls.

## Independently verified proof mechanisms

The N-fixed parameter is y=t^2/(1+t); the quotient involution is y/(1+y).
Formal bases 1,t over k[[y]] and 1,y over k[[z]], z=y^2/(1+y), prove full
fixed rings and fields. They are not finite truncations. Perfectness in
characteristic two makes every algebraic derivation a coefficient derivation,
through h=a(t)^2+t b(t)^2, excluding hidden discontinuous derivations here.

Restriction of integral N-invariant derivations is exactly
M=y k[[y]] partial_y. Extending b(y) partial_y to k((t)) gives coefficient
b(y)(1+t)^2/t^2, with sharp valuation threshold ord_y b >=1. The quotient
operator is T(f)=(1+y)^2 f(y/(1+y)). Its invariant module is y^2 k[[z]],
and every invariant has the exact preimage y h(z) under T-1. Hence
H^1(G/N,M)=0 on full formal series. Independent direct cocycle and actual
first-order conjugation arguments verify tangent restriction injectivity.

Over B=k[e]/e^3, the involution (y+e)/(1+y) has a class fixed by the ring
automorphism e to e+e^2. The displayed matrix conjugacy treats the actual
class, not a hull parameter. B's fixed subring reduces to constants in
A=k[e]/e^2, so naturality makes every prorepresentable recipient kill its
reduced tangent v. An arbitrary identity-reducing conjugator y+e h(y) has
zero constant first-order conjugacy perturbation, while v's constant
coefficient is one. Thus v remains nonzero against every allowed conjugator.

For any proposed fibre product, naturality places (0,v) in its tangent.
Smoothness for the small surjection A to k would lift this pair to a
G-tangent with restriction zero. Injectivity makes that tangent zero,
whose induction is zero, a contradiction. The proposed obstruction quotient
is the trivial module k, so its first cohomology is indeed one-dimensional;
the contradiction is stronger than requiring that particular dimension.

Two fresh mathematical families independently reconstructed these steps.
The formal-series family challenged fixed fields, derivations, valuations,
module conventions and completeness. The functor family challenged actual
classes, all coordinate conjugators, naturality/pointedness, mixed
characteristic recipients, the invariant subfunctor and the precise
small-extension smoothness quantifier. Both found no mathematical blocker
in the stated unrestricted example. Their reports are stage-specific AI
reviews, not priority or human-review certificates.

## Prior credit and bounded priority audit

The involution parameter shift is the explicit published
Byszewski–Cornelissen Proposition 4.1 (2009). More strongly, their Proposition
6.1, printed p.899, already exhibits an injection k[e]/e^2 into k[w]/w^3,
e to w^2, under which distinct involution tangent/basepoint classes become
equal. A prorepresentable Hom-functor preserves injections, so naturality
immediately implies recipient tangent collapse. The direct cubic-ring proof
in the note is useful for fixing v, but the collapse phenomenon is credited
as an elementary consequence of that prior proposition.

The weakly ramified additive Klein-four family and the tangent-cohomology
framework are also established ingredients. The contribution evaluated here
is combining them with the independently computed zero restriction kernel
to exclude the proposed unrestricted factorization. It is not a newly
discovered involution pathology or additive action.

The independent priority audit ran 65 focused queries and inspected 11
primary/source-version records. It compared the original OWR question,
2009 thesis, arXiv v1, AIF published/preprint versions, Dokchitser's quotient
criterion, the published 2012 order-five universality paper, Obus's 2017/2019
survey, the 2022 Nottingham-group paper, Dang's 2026 cyclic-tower paper and
the explicit metacyclic hypotheses of a 2025 preprint. No matching prior
negative restriction–induction assertion was identified in inspected bodies.
The key prior antecedents were identified and credited, including the
previously insufficiently emphasized Proposition 6.1.

The search is bounded: unindexed or differently worded work, unpublished
arguments, inaccessible bodies and incomplete citation records may remain.
No claim of first counterexample, exhaustive originality, or verified
openness through 2026 is made. No 2013 journal edition of arXiv:1112.0352 was
verified and none is invented in the bibliography. Original author/source
contact was neither prepared nor initiated.

## Reproducibility, provenance and remaining gates

Submitted PR head: 37b4b2fa44368f49e534e4982bd11f5667e0bf36,
[PR #1024](https://github.com/AlecKriebel/Math/pull/1024), catalogue problem
30001113 / OWR-2492-004. Original authored files and historical seals remain
unchanged in the program's submitted snapshot; fresh findings are separate.

Root reproduced 30 exact baseline/control executions, two positives and
eight intended rejections in each of normal, -O and -OO modes. Complete
stdout/stderr and exit codes matched the submitted FINITE_CONTRACT exactly.
The finite checks cover F4 rational action and quotient identities, the
derivation operator, matrix conjugacy/involution, fixed subring and selected
formal monomials. They do not prove infinite formal-series statements,
quantification over all natural transformations, or source/priority claims.
Those are supplied by the written derivations and independent source audits.

Direct finite-program replay is distinct from the old UID1000 sealed-packet
permission harness; no replay of that historical environment is claimed.
Source bodies are retained locally for inspection and are not redistributed.
Retrieved-byte hashes and public primary URLs accompany the authored material
in the [portable evidence index](evidence/INDEX.md). Historical absolute paths
describe the environment of that stage; the index maps them to portable copies.

The portable runner adds a third independently written F4 cubic-ring arithmetic
check. Its eleven original assertion predicates were converted to explicit
RuntimeError guards by an AST-preserving adaptation, with unchanged predicates
and original source retained. All checks survive -O and -OO. The runner passed
39 executions: nine baselines, twelve actual-source fault controls and eighteen
runtime fault controls. Complete stdout/stderr, exact JSON types and exit codes
match fixed references. Python 3.10+ and only the standard library are required;
the recorded run used Python 3.14.6 on macOS. No other operating system was
tested here. This is finite corroboration, not a formal proof certificate.

Exact metadata and the source/verification inventory accompany the package.
The first fresh whole-package review independently passed with zero actionable
concerns; its unchanged report and receipts are indexed below. A NEW second
whole-manuscript/package adversarial review remains pending in
[the current state](evidence/CURRENT_REVIEW_STATE.json). The package is not yet
approved for immutable publication. Every actionable issue must be corrected
in current artifacts and reviewed by a new independent adversarial subagent.
The final metadata and tracker retain **unrestricted** scope, the untouched
prorepresentable-component variant, known-ingredient credit and extensive-AI /
unrefereed disclosure. No formal proof-assistant or human peer-review certificate
is claimed.
