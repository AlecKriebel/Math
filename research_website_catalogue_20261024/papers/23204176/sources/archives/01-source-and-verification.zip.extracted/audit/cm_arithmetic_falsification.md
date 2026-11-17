# Independent arithmetic and assembly falsification audit

Audit checkpoint: 2026-10-06 21:50 PDT (2026-10-07 04:50 UTC).
Assigned-scope completion estimate: 100%; overall CM Hodge proof completion is
not estimated by this audit. The separate finite-locus/Hecke audit is complete
and its affirmative result has been reconciled below.

## Scope and independence

This audit independently read `01-introduction.tex`, `02-tensors.tex`,
`03-surface.tex`, `05a-moduli.tex`, `05b-frobenius.tex`,
`05b-satake-frobenius.tex`, `05c-cm-types.tex`, and `06-assembly.tex` in the
September 30 CM manuscript pinned at upstream commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. It did not start from or read the
root's favorable arithmetic audit. It did not reconstruct the analytic theta
construction in `04-theta.tex`; its exact finite-family conclusions are inputs
to the assembly checked here. A distinct agent independently checks the
finite tuple locus, compact reference component, Hecke quotient branches,
polarization, and marking descent.

No counterexample or substantive gap has been found in the arithmetic
Frobenius/filtered-projector/scalar-descent/assembly chain within this scope.
This is a mathematical reading audit with explicit hypothesis mapping and
small exact checks, not formal verification, conventional peer review, or a
standalone certification of the entire CM theorem.

Source SHA-256 values for the central modules:

| Source | SHA-256 |
| --- | --- |
| `05a-moduli.tex` | `3e25d6ae9fddf3ed47a695aad97714400c12e358beef24e703027b9a801ba346` |
| `05b-frobenius.tex` | `fa981f76a7ebc75b4395e4266b0619b08b74273cba346f3217ea5b736172b428` |
| `05c-cm-types.tex` | `7cd65bc8883c6bf513c89e841ae85812be096354516c1b90f58e81b52cb5bd79` |
| `06-assembly.tex` | `c9d120f17ba3b1da5b8f92700eb9bca3ca3502e9ec6a6e81558d8a44f2310a2f` |

## Good models, CM points, and ordinariness

`05a-moduli.tex`, Lemma `lem:good-ordinary-primes`, lines 273–356,
contains the required construction rather than assuming ordinary points on
each component. The models retain the full tuple coordinates after excluding
the finite boundary image (lines 288–301). The proof of Albanese generation
uses nested irreducible proper sum images of
`a_j(S_j)-a_j(S_j)`, obtains one finite surjective sum map in characteristic
zero, and spreads that proper surjection to the abelian model (303–318).
This supplies generation on every retained geometric special fiber without
asserting that reduction of an Albanese is automatically the new fiber's
Albanese.

The selected ordinary-point argument (320–355) uses a rational orthogonal
decomposition of the Hermitian three-space into E-lines with the negative
period line one summand. Its three rational projectors preserve the Hodge
filtration; denominator-cleared projectors are actual abelian endomorphisms
by the previously proved degree-one realization lemma. Adding their graphs
with the Hilbert polynomials at the selected point gives a finite-type
parameter scheme. Rigidity fixes their local matrices, and preservation of
the negative line by these projectors isolates that point in the ball
component. Thus the point and endomorphisms are defined over an algebraic
number field, which can be adjoined to K before selecting q.

At a completely split retained q, the projector and
`O_E tensor Z_q` idempotent pieces have height one. Their constant heights
come from the étale Tate ranks; a height-one p-divisible group over an
algebraically closed field is étale or multiplicative, according to its
dimension. Consequently these selected fibers are ordinary, and openness
gives density on every smooth geometrically connected component. The proof
does not require a uniform ordinary-prime assertion before adjoining these
finite point fields, nor does it assert ordinariness of the separate Albanese
variety `A_S`.

## Integral Frobenius congruence

`05b-frobenius.tex`, Proposition `prop:albanese-congruence`, lines 39–328,
proves

\[
\Phi^3-D_1\Phi^2+qD_2\Phi-q^3D_3=0
\]

as an integral abelian endomorphism identity. I attempted the following
specific failure mechanisms.

1. **Incorrect specialization multiplicities.** At an ordinary point the
   active block is height three, with a distinguished multiplicative line
   and an étale plane. The finite flat lifted label components have rank q.
   Generic subspaces disjoint from the distinguished line are graph lifts;
   over a b-dimensional étale label subspace there are exactly `q^b` such
   lifts (81–122). Rank-one closure on each label specializes to its unique
   reduced point. A subspace containing the distinguished line instead
   specializes to the full multiplicative component. Thus the multiplicity
   table (124–138) gives precisely one multiplicative-line branch and q
   copies of each étale line for D1, one mixed plane for each étale line and
   `q^2` copies of the étale plane for D2, and one full-space branch for D3.
   Exact enumerations below agree, but the geometric flat-closure argument,
   not the enumerations, supplies the all-prime deduction.
2. **Loss of target tuple information.** Properness extends each generic
   neighbor in the full tuple model; the generic isogeny extends by the
   Néron property over the newly ramified DVR (141–181). The polarization
   identity forces finite fiber kernels, constant isogeny degree, and finite
   flatness. Its kernel is therefore the schematic closure of the generic
   one. Cartier duality and annihilators commute with this specialization.
   Equal full kernels give canonically identified quotient tuples with
   unique descended action, polarization, and transported marking. Branch
   multiplicities remain even when quotient tuples coincide.
3. **Frobenius inverse or marking shift.** X0 is the connected q-torsion
   quotient on all blocks and hence relative Frobenius, with polarization
   multiplier q (188–213). The level label group is constant and its
   Frobenius preserves labels; the N-torsion marking is transported to its
   twisted marking, without multiplication by q. Over the Fq model this is
   coordinate q-power on geometric points. It is not inverse Frobenius.
4. **Unsupported commutation or composite annihilators.** Naturality
   `F_{B'} f = f^(q) F_B` commutes X0 with Y0 and Z0 as multisets of full
   tuples (215–226). Only these two commutations are later used. The
   adjoint-isogeny identity and total kernel ranks force equality in each
   pairwise annihilator inequality (227–263). This identifies the opposite
   kernels and multipliers of the composed operations, yielding
   `D1=X0+qY0`, `D2=X0Y0+q^2 Z0`, and `D3=X0Z0` (265–270).
5. **Invalid rationalization of finite-field points.** The proof applies
   these identities to actual Albanese differences in geometric point
   groups (274–300), with integral coefficients. Cubic cancellation is
   immediate after the two X0 commutations (302–319). Density of ordinary
   pairs first gives a zero morphism on the product of each component with
   itself; finite-sum Albanese generation then makes the endomorphism zero
   (320–327). It does not tensor the torsion point groups with Q.

The transition to cohomology (330–341) uses the q-power endomorphism's
pullback on crystalline H1. Since q is prime and the residue field is Fq,
Witt Frobenius on Zq is the identity. Additivity of abelian pullback in H1
and commutation give the displayed polynomial with the same coefficients,
not a reciprocal polynomial.

## Central scalar normalization and Frobenius root selection

I independently checked the finite-order proof for T3 and C0 in
`05b-satake-frobenius.tex`, `lem:central-finite-order`, 347–383. T3 is
principalized by the norm-one scalar supported on w and its opposite,
followed by a power fixing the marking. For C0 its exponent-one ideal I
contains exactly one prime from every conjugate pair, so `I bar I=(q)`.
If `I^m=(a)` and `a bar a=q^m u` with u a totally positive F-unit, then
`b=a^2/u` has the exponents of `I^(2m)` and `b bar b=q^(2m)` exactly.
This avoids an unjustified square root or unit norm equation. Another power
fixes the finite marking. An E-scalar preserves every component's E-linear
filtration, so finite order applies on the full tuple space and its induced
Albanese action, not only on the original ball component.

For a full numerical Hecke character extending the active parameter,
`05c-cm-types.tex`, 146–179, writes the absorbed triple as
`b(q^(1/2),q^(-1/2),e')`; the finite-order determinant relation is
`b^3 e'` a root of unity. Hence every complex conjugate of b has modulus
one, as does e'. The raw Satake normalization supplies `q e1`, `q e2`,
and `e3`, so the Frobenius candidates are
`b q^(3/2)`, `b q^(1/2)`, and `q b e'` (198–264).

The degree-one Weil polynomial P_Phi is rational and annihilates Phi as
an endomorphism, by prime-to-q Tate faithfulness and Cayley–Hamilton. It
therefore annihilates crystalline pullback too (224–239). An algebraic
candidate whose iota-image is a root of P_Phi is itself a root because
P_Phi has rational coefficients. Its complex absolute value must be
`q^(1/2)`. The other two candidates have moduli `q^(3/2)` and q, so only
`b q^(1/2)` survives. This argument does not assume that `A_S` is CM or
ordinary. Simultaneous triangularization handles generalized character
spaces; it does not discard nilpotent parts.

The subsequent valuation is
`nu_iota(b q^(1/2)) = 1/2 - nu_iota(e')/3`, which is 0 or 1.
The conjugate-valuation computation at
`05b-satake-frobenius.tex`, 318–338, consistently uses `w=p_c` and
`d(g^(-1))=v(g)`. The possible sign in a conjugated square root changes no
valuation. I found no sign error in this linkage.

## Filtration and scalar conjugation

`05c-cm-types.tex`, `lem:filtered-hecke-summands`, 54–130, has the
essential idempotent hypothesis: the algebraic-coefficient projector and
its complement preserve the Hodge filtration and commute with Frobenius.
This is justified by their being polynomials in extending algebraic Hecke
endomorphisms (10–48), with Betti faithfulness transferring the polynomial
relations to other degree-one realizations.

After coefficient extension, the underlying Qq module is a finite direct
sum of copies of the original weakly admissible module, not a geometric
extension of the base field. Both projected modules have `t_H<=t_N`;
additivity and equality on the whole module force equality on each. With
only filtration indices 0 and 1, pure Newton slope 0 gives zero F1, and
pure Newton slope 1 gives full F1. This avoids the known counterexample
where a slope projector fails to preserve the filtration.

The external weak-admissibility input matches
[Brinon–Conrad, Theorem 9.3.4](https://math.stanford.edu/~conrad/papers/notes.pdf):
crystalline representations produce weakly admissible filtered modules.
For the coefficient treatment,
[Hellmann, Proposition 2.17(ii) and Corollary 2.22](https://arxiv.org/pdf/1102.0119)
support strict images of equal-slope maps and preservation of semistability
under extension and finite restriction of coefficients. The manuscript
also supplies its own direct-sum/complement argument, so it does not need an
unstated extension-of-coefficients theorem in the form actually used.

The comparison of each scalar-conjugate projector with complex Hodge type
(281–315) uses matrices over the actual compositum of K and the projector
coefficients. Matrix ranks survive the fixed embedding iota. Each
conjugated projector is evaluated separately in the same K-defined
operators. No automorphism fixing K or linear disjointness between K and
the character field is asserted. Complex Hecke operators preserve both
H10 and H01, so full or zero projected F1 identifies the whole generalized
space's Hodge type.

## Rational sources and assembly

`05c-cm-types.tex`, proof of `thm:cm-extraction`, 326–389, handles
transcendental theta coefficients by first spanning the active spaces with
algebraic Betti vectors. For an algebraic vector x in one active space, the
map from U(v) supported on its identity embedding line and sending its
generator to x is defined over Qbar. Every scalar conjugate has source and
target of matching type because the conjugate active space's type is
`(1+v(g))/2` (339–370). The trace-dual scalar descent lemma in
`02-tensors.tex`, 34–61, then makes it a Qbar span of rational Hodge maps.
Complex spans of those algebraic vectors cover the full active space.

The finite-family extraction corollary (`05c`, 395–430) fixes levels and
inputs before auxiliary primes, takes one common deeper principal cover,
and uses rational Hodge pullback to preserve all four type spans. Different
families may use different auxiliary primes; no common-prime conclusion is
needed in the final period calculation.

`06-assembly.tex`, 10–97, explicitly pulls the fixed finite theta endpoint
expansions to this common smooth projective surface Y. The nonzero period
is multiplied by the covering degree, selects a nonzero cup-product term,
and all four selected classes have rational CM-source spans on that same
surface. Complex conjugation commutes with rational maps and exchanges
source labels 1 and c. The surface-span criterion applies exactly.

I independently checked the final class construction in
`03-surface.tex`, 29–124. The pushed-forward surface gives a functional in
degree `2n-4`, not the desired vector in degree four. Four pure divisor
kernels, each all-scalar-conjugate type (1,1), turn that functional into
`k t_beta`, with k nonzero and algebraic. The six degree-one crossings
give sign +1, and the codimension is `(n-2)+4-n=2`. Thus no unproved
Hodge projector on higher cohomology is inserted. Scalar conjugation
finally restores the requested labels.

The tensor reduction (`02-tensors.tex`, 332–479) uses auxiliary factors,
finite column-wise two-row switches, pure algebraic two-factor transition
tensors, and algebraic polarization contractions. The middle pairings are
nonzero by conjugate embedding lines and Hodge–Riemann positivity; their
values are algebraic Betti numbers. The composition codimension
`p+p+p(s-1)-ps=p` is correct. Transfer back to distinct original exterior
slots followed by the diagonal does not kill the supported monomial.
The scalar intersection with rational cohomology gives the original
rational cycle span. It does not claim that codimension-two classes
generate the Hodge ring of an unchanged abelian power.

## Reproducible finite checks and limits

`checks/cm_arithmetic/verify_hecke_counts.py` is a standalone standard-library
Python 3 exact enumerator. It ran successfully for q = 2, 3, 5, 7, 11,
producing `checks/cm_arithmetic/hecke_counts.json`.

For every nonzero residue vector in each Fq3 it checks one containing
projective line and q+1 containing planes; each total is `q^2+q+1`.
With M a distinguished line, it checks q graph lines for every étale
label line, one plane containing M for every label line, and q2 planes
disjoint from M. It asserts the integer bracket coefficients of the raw
radial minuscule actions and the exact formal cubic cancellation using
commuting X0,Y0,Z0. These are finite combinatorial checks only. They do
not prove representability, finite flat specialization, theta covariance,
crystalline comparison, or any Hodge-conjecture statement.

Strongest checked conclusion: given the theta finite-family/nonzero-period
outputs and the stated standard algebraic/p-adic comparison inputs, the
arithmetic CM-source extraction and algebraic assembly in the audited
modules have a complete matching deduction. No additional unsupported
claim replacing their central arithmetic difficulty was identified.

The distinct review in `agent_notes/cm_finite_locus_falsification.md` is
complete and agrees on the finite-type graph bound, proper action locus over
fixed polarized moduli, compact components, Hecke polarization homomorphism
descent, full marking transport, and equal-kernel specialization. It also
independently recruited a narrower Hecke polarization/marking reviewer. Its
remaining limit is that every underlying GIT/integral-base theorem was not
reconstructed; it suggests a more explicit graph-locus and relative Hom
citation as exposition improvements, without identifying an obstruction.

No work remains in this assigned audit. Beyond this assigned scope, the
theta existence/covariance arguments and the unrelated Kuga–Satake
analytic/category chain require their own audits. The present affirmative
result is a dependency-level mathematical audit with the stated scope and
limits, not a claim that all these separate modules have been formally
verified.
