# Independent adversarial audit

## Verdict

**Accept the unsolved status and the partial reductions, with the minor
scope correction and proof clarifications in CORRECTIONS.md.**

Problem: 30006276 / OWR-14299284-004, *Multiplicativity of Tautological Chow
Projections*. The audited target is the canonical rational projection on
CH*(A_g) over C. No proof or counterexample to the full target is present.
No novelty judgment is certified.

The frozen author SHA256SUMS has digest
`83549a36a97a878966348ab32cdfe0798e235e299b6841973e21c63434afec08`.
All seven listed files match their recorded hashes. The original packet was
not edited. `AUDITED_INPUTS.json` binds this audit to those exact bytes.

## Verified findings

- The original verifier reproduces its stored JSON byte for byte: 5,250
  exact assertions and 215,267 nontrivial partition cases.
- An independently written SymPy checker passes 2,736 further assertions.
  It constructs the Chern-relation ideals directly, without importing the
  author's ring-reduction implementation.
- For g=2,...,8 it checks independence of every squarefree basis and the
  nonzero determinant of every complementary-degree pairing.
- It independently confirms all three projected Torelli-square polynomials,
  all five normalized scalar targets, and completeness of the test bases.
  Every target-degree basis perturbation is detected by at least one test.
- A separate descending-partition enumerator, cross-checked against an
  unrelated coin-change count, examines 1,295,920 cases for g=2,...,50.
  It recovers exactly the four stated possible shapes, with small-genus
  restrictions. The self-product inequality is checked through g=1000.
- New logical controls distinguish the annihilator argument from the
  geometric vanishing theorem and homogeneous-square tests from the full
  polarization criterion. These controls are expressly abstract rings,
  not cycles or counterexamples on A_g.

## 1. Exact target and source scope

The printed OWR page 1492 was inspected visually, including Question 1.
Its operator has domain CH*(A_g), rather than the Chow ring of an individual
abelian variety. The nearby theorem concerns special pairs and is not a
universal solution. [S1]

The version-specific arXiv sources were inspected, and the current record
for the homomorphism paper still identifies June 9, 2026 as v3. Conjecture 8
is the global target. Proposition 39 is a fixed-fibre statement about X^s;
Section 5.6 discusses a further, distinct universal-family projection. None
can be substituted for the target. The normalization of the Torelli cycle
is Tor_*1. Theorem 7 proves selected mixed product cases through g=8. [S4]

The August families paper proves statements about projected Gromov-Witten
classes. Proposition 1.3 assumes g,h>=4 and vertical tautological
insertions; Proposition 5.7 supplies the general-characteristic-polynomial
vanishing. Theorem 1.8 and its proof give genus-two projected modularity.
They do not assert multiplicativity for arbitrary Chow classes. [S5]

This is a bounded literature check, not proof of a universally exhaustive
search. Access claims about earlier catalogue or publisher requests were
not promoted into new successful-access claims.

## 2. Kernel algebra: passes

Let A=R direct-sum K and P be the pairing-defined projection. Testing against
R proves R-linearity. Expanding a=P(a)+k_a and b=P(b)+k_b proves

    P(ab)-P(a)P(b)=P(k_a k_b).

Every equivalence in Section 2.1 follows: multiplicativity; K being an
ideal; P(KK)=0; vanishing of all kernel squares, including inhomogeneous
ones; and vanishing of complementary epsilon(klr). The radical formulation
also holds with epsilon extended by zero outside its socle degree.
The proof uses rational coefficients for polarization and the perfect
pairing for detection; it does not implicitly assume nondegeneracy on A.

The fixed product-polarized surface calculation is valid. On the subalgebra
Q[a,b]/(a^2,b^2), the degree projection to Q[a+b] has P(a)=(a+b)/2,
P(a^2)=0 and P(a)^2=ab/2. The cited geometry realizes the algebra, but the
space and trace differ from A_g and its lambda_g pairing. Its only valid
role here is to refute an automatic formal argument.

A further test uses Q[x,y]/(x^2,y^2), with degrees 1 and 2, and projects to
Q[xy]. Each homogeneous kernel component has square zero, while P(xy)=xy.
Thus testing only homogeneous kernel squares is insufficient. The author's
explicit inhomogeneous qualification is essential and correct.

## 3. Cohomology and degree cutoffs: passes with clarification

The pairing construction and its compactification independence are the
correct ones. Boundary vanishing is a statement on the full toroidal
boundary; the extended lambda_g, rather than its zero open restriction,
appears in the integral. The residue proof of [S2, Theorem 3] and the
projection definition were reviewed.

The conclusion ker(cl) subset ker(P) is correct. To make the proof robust
for a singular boundary, CORRECTIONS.md supplies the missing explicit
comparison with its smooth normalization using [S7, Proposition 8.2.7].
The compactly supported lift then gives the asserted trace identity.
Consequently P factors through algebraic cohomology, R injects there, and
multiplicativity with a class cohomologous to a tautological class is
automatic. No algebraicity of arbitrary cohomology classes is assumed.

The inequality i+j>N is a valid automatic vanishing condition. The
conditional lower bound on the degrees of a possible witness is valid.
The input CH*(A_g)=R*(A_g) for g<=3 is stated with the principal-polarization
hypothesis in [S3, Section 1.3]. There is no unsupported induction in genus.

## 4. Nonsimple support: passes after the g>=2 scope correction

Theorem 6 of [S3] applies to both factors supported on the nonsimple
Noether-Lefschetz locus, and states that both projected expressions vanish.
It excludes the proposed two-supported-factor counterexample route.
Generally simple real-multiplication loci are outside that scope.

The splitting/vanishing argument gives lambda_(g-1)I=0. For g>=2 the
squarefree basis proves Ann_R(lambda_(g-1))=lambda_(g-1)R and
lambda_(g-1)^2=0. The displayed lemma needs this genus qualifier: lambda_0=1
at g=1. That case has I=0 and is already settled by the low-genus input.

Proposition 13's proof separates excess components with zero top Chern
class from components carrying a repeated positive-dimensional isogeny
factor. On the latter, its squared top Hodge class vanishes after
compactification. The final paragraph explicitly covers arbitrary
supported cycles. This is the extra geometric input required for P(II)=0;
the annihilator calculation alone does not supply it. [S3]

A concrete logical discriminator is A=Q[x]/(x^3), R=Q[x^2], lambda=x^2,
I=(x), with P deleting the x coefficient. The restricted trace is perfect,
P is R-linear, lambda I=0 and P(I)^2=0, yet P(x^2)=x^2. This mock ring
confirms the precise missing implication without claiming a moduli-space
counterexample. The conclusion on R+I and the warning about mixed arbitrary
classes are correct.

## 5. Torelli tests: passes; left sides remain unknown

The codimension c_g=(g-2)(g-3)/2 and N-c_g=2g-3 are correct. The projection
formula gives the displayed criterion, provided the compactification is
chosen compatibly with Torelli as specified in CORRECTIONS.md.

The partition proof is genuinely all-genus. For two parts r and g-r,
r>=3 gives (r-2)g-r^2+3 >= (r-1)(r-3), leaving only (3,3) at g=6.
For k>=3, the minimum occurs at (1,...,1,g-k+1). The k=3 equality case is
unique; k>=4 gives a strict excess over 2g-3. The finite enumerations check
this proof rather than replace it.

The self-product inequality reduces to g^2-9g+12<=0 for integral g>=2,
so the nonautomatic range is g<=7. Since the g<=4 classes are tautological,
only g=5,6,7 remain in this family. The source-normalized projections,
including the genus-three factor 2, were checked against [S4].

Independent polynomial reduction confirms:

    g=5: 55296 l1 l2 l3 - 64512 l2 l4,
    g=6: (26844659712/691) l1 l2 l4 l5
           - (20497563648/691) l3 l4 l5,
    g=7: (630538371072/691) l2 l3 l4 l5 l6.

The complementary tests and their normalized values are exactly:

    g=5: l4 -> 55296; l1 l3 -> 377856,
    g=6: l3 -> 26844659712/691; l1 l2 -> 86881075200/691,
    g=7: l1 -> 630538371072/691.

The source data determine these right sides; neither verifier computes
P(J_g^2), Tor^*(J_g), or any of the five geometric left-hand integrals.
All five could hold without proving the full conjecture. Replacing a
geometric J_g by P(J_g) in such an integral would be circular.

## 6. Compact restriction criterion: passes as a sufficient condition only

Under the stated compactified class identity [V]=c lambda_g with c nonzero,
restriction of R to V is injective by the trace and perfect pairing. If
all restricted algebraic classes already lie in this image, the same trace
identifies restriction with P, proving multiplicativity. This argument
requires a graded ring-valued cycle-class theory with compatible products
and fundamental-class trace, as the text stipulates. V need not be smooth.

The compact-subvariety obstruction is correctly attributed to Keel-Sadun:
its strict dimension bound for g>=3 rules out the proposed complex V.
The proof strategy uses positivity, rigidity of the limiting tangent
spaces and noncompactness of the resulting symmetric-domain image. [S6]
The characteristic-p locus supplies the dimension and class, but no
restriction-image equality. The packet does not infer that equality from
properness, nor treat the specialization discussion as a proven input.

## 7. Remaining obligations and audit limits

The unsolved obligation is P(KK)=0, equivalently the weighted product
vanishing against every complementary tautological test class. No genuine
A_g counterexample has been furnished. The five routes are completed
investigations, not five proofs of the desired theorem.

The source proof mechanisms and hypotheses relevant to the packet were
reviewed. Published external implementations of the Torelli excess
calculation were not rerun; those cases are cited prior theorems, not new
certificates produced here. The audit does not compute arbitrary Chow
groups, establish the characteristic-p image hypothesis, or certify a
numerical percentage of progress toward a solution.

## Sources

[S1] A. Iribar López, contribution to OWR 28/2025, Question 1, p.1492:
https://doi.org/10.4171/OWR/2025/28 .

[S2] Canning–Molcho–Oprea–Pandharipande, arXiv:2401.15768v4,
Theorems 1 and 3, Definition 4, and Sections 2.4–2.5:
https://arxiv.org/abs/2401.15768v4 .

[S3] A. Iribar López, arXiv:2411.09910v2, Sections 1.2–1.3,
Proposition 13 and its proof, Theorem 6 and its proof, Proposition 20:
https://arxiv.org/abs/2411.09910v2 .

[S4] Canning et al., arXiv:2601.04353v3, Sections 1.3, 1.7–1.9,
3.5–3.6, 5.3 and 5.6: https://arxiv.org/abs/2601.04353v3 .

[S5] G. Oberdieck, arXiv:2608.16737v1, Propositions 1.3 and 5.7,
Theorem 1.8 and its proof: https://arxiv.org/abs/2608.16737v1 .

[S6] Keel–Sadun, arXiv:math/0204229v2, Main Theorem 1.1,
Corollary 1.2 and Section 2: https://arxiv.org/abs/math/0204229v2 .

[S7] P. Deligne, *Théorie de Hodge III*, Propositions 8.2.5 and 8.2.7,
printed pp.39–40: https://www.numdam.org/articles/10.1007/BF02685881/ .

## Reproduction

With Python and SymPy 1.14.0 installed, run:

    python3 audit/independent_checks.py > /tmp/independent_results.json
    diff -u audit/independent_results.json /tmp/independent_results.json
    cd audit && sha256sum -c SHA256SUMS

The audit contains original analysis, a checker, results and hash metadata.
It contains no source PDFs, reproduced full text, imported catalogue corpus,
or coordination records.
