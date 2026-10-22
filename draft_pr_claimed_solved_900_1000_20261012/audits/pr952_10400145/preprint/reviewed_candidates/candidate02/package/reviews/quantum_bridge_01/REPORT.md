# Independent quantum-normalization and source-bridge review

PR 952; problem 10400145 / AMR-103-0145. Original head: `989a532ae1d50894190d010a0a02ba8c3d71ee05`.

Review timestamp: 2026-10-16T16:20:59.045925+00:00. This is an independent agent review of the mathematical bridge, not human referee certification. Priority, novelty and exhaustive literature status are outside this report.

## Judgment

**The literal disproof in the pinned PROOF_AND_STATUS.md passes this review. No required mathematical correction was found.** The exact printed ring forces the coefficient of q−1 to be affine in the matrix size n. The actual fixed-Lie-algebra invariant has cubic first-coefficient dependence. For the orientation explicitly selected by the candidate, the first coefficients at n=1,2,3 are 0,−6,−24; the required second difference is instead zero. Its actual value is −12.

This conclusion uses published prior quantum-invariant results. I checked the actual controlling primary formulas and their conventions, and independently reproduced the algebraic obstruction. I also derived and exactly tested a separate type-A theta-weight mechanism. I did not execute or import candidate checkers, read old audits, or treat their conclusions as evidence.

## Independence and authentication

Before mathematical/source intake, START_AUTH.json mechanically authenticated all 33 pinned original bodies, byte sizes, disk modes, and Git blob identities against ORIGINAL_FILE_RECORDS.json and ORIGINAL_SNAPSHOT.json. The exact source statement hashes to `87dd83734fc8c51eb132f501c5d05947ed7057268dfba61627fb78f53da10af8`; the source record's review-hash field matches the supplied `12e089388884a531bdc98f888e203ec0be06aa637e3ce342ac1e502a7af266f5` (I do not claim to have reconstructed that latter digest's underlying serialization).

I read the primary question and relevant primary formulas, then saved and reread INITIAL_ATTACK.md before reading the candidate proof. Its finite-second-quotient argument, cubic-coefficient suspicion, directly oriented Poincare test, and planned theta mechanism are independent of the candidate and old audits. No source, Git state, index, reference, configuration, or files outside this assigned review folder were changed by this review. No external communication or publication action occurred.

## Exact question and independent finite-quotient proof

Ohtsuki's printed pages 490–492, personally visually read, fix

\[
R=\varprojlim_m\mathbb Z[q,q^{-1}]/\Bigl(\prod_{j=1}^m(q^j-1)\Bigr),\qquad
S=\varprojlim_m R[t]/(E_m(t)),\quad E_m(t)=\prod_{j=1}^m(t-q^j).
\]

The evaluation requested is t=q^n for sl_n, including I^{sl_1}=1. Thus n is matrix size; the Lie rank is n−1. This is the integral ring in the printed question. Inversion of q adds no difference to the usual polynomial Habiro ring: at finite level the defining polynomial has unit constant coefficient, so q is already a unit. [Primary question](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed 490–492.

Put x=q−1 and D=Z[x]/x². The Habiro quotient at m=2 maps to D, so R does as well. For any F in S, its second component has a unique representative

\[
a+b(t-q),\quad a,b\in R,
\]

because E_2 is monic. Its value at q is a; if F(q)=1 then a=1. At any higher level m≥max(2,n), a representative differs from this one by E_2(t)H(t). Evaluating t=q^n and then mapping to D kills that difference, since each q^n−q^j is divisible by x. Therefore

\[
T(F(q^n))=T(1+b(q^n-q))=1+(n-1)b(1)x.
\]

In particular v_3=2v_2. This proof uses only finite compatible quotients. It does not evaluate an undefined map on the second quotient before taking the Taylor jet, divide by node differences, assume a global Newton-series representation, or differentiate an infinite series. The candidate's third-quotient proof is also correct and gives the general affine condition without F(q)=1.

## Primary mathematical inputs and normalization bridge

The decisive published first coefficient is on Le, Topology 39 (2000), printed 821 / physical PDF9, immediately after Conjecture1.9:

\[
c_1^{(n)}(M)=|H_1(M;\mathbb Z)|^{-n(n-1)/2}n(n^2-1)\lambda_C(M).
\]

The same body's printed815 / PDF3 uses q=1+x, sl_n with n−1 simple roots, and Cartan-matrix inner products (type-A roots have squared length2). Its Theorem1.7 defines the perturbative coefficients through congruences with quantum PSU(n) invariants. Here |H_1| is cardinality, hence1 on integral spheres. The named invariant is Casson–Walker in Lescop normalization; no separately remembered factor-of-two convention is needed. The arXiv v2 first-coefficient paragraph was also visually checked: its additional Legendre symbol is1 in this setting. The published formula controls. [Author-hosted published primary body](https://people.math.gatech.edu/~letu/Papers/PERT_NEW01.pdf).

For identification of the invariant, I checked Habiro–Le's published Theorem1.1 (2690), Proposition1.2 (2691), Proposition1.9 and the immediately following LMO relation (2693), plus §3A1–2 (2726). The unified invariant has the required WRT evaluations, also the projective evaluations; on integral spheres the two versions agree where both are defined. Its Taylor series is the Ohtsuki series. The same body specifies short roots squared length2 and q=v²=e^h. Type A has no varying root-length multiplier. The accepted arXiv v2 equations were visually cross-checked independently. The printed question itself states the relevant projective equality and perturbative connection. [Habiro–Le published primary body](https://msp.org/gt/2016/20-5/gt-v20-n5-p04-s.pdf).

These facts identify the question's fixed-rank invariant with the one whose coefficient is displayed above. One may use equality at infinitely many sufficiently large prime-order roots and the Habiro evaluation uniqueness stated on published2689; small exceptional orders are immaterial. There is also a direct first-jet verification that avoids relying on the full Taylor-identity theorem:

1. For an odd prime r, the map Z[ζ_r]→F_r[x]/x² given by ζ_r↦1+x is well-defined, because Φ_r(1+x)=r+binom(r,2)x=0 in that ring.
2. A Habiro representative at level r computes its ζ_r evaluation; its reduction in F_r[x]/x² agrees with the Taylor reduction, by compatibility with level2.
3. For fixed n and sufficiently large r, Le's Theorem1.7 may be reduced to this jet. Since |H_1|=1, its homology/Legendre prefactors are1. The first Taylor coefficient and the published perturbative c_1 therefore agree modulo every sufficiently large prime outside their finitely many denominators.
4. A rational difference with this property is zero.

This makes the needed degree-one identity checkable without assuming any analytic expansion of a function defined only at roots of unity.

## Orientation, Casson calibration, and contradiction

Le's Quantum invariants paper, printed133 / PDF9, explicitly labels P as −1 surgery on the left-handed trefoil. Its displayed sl_2 formula agrees with Ohtsuki492. Habiro's arXiv:math/0605314v1, PDF61 equation(16.1), independently displays the same expression as a unified invariant, so using its Taylor jet is justified within the completion. [Le primary body](https://people.math.gatech.edu/~letu/Papers/QUANTUM.pdf), [Habiro primary body](https://arxiv.org/pdf/math/0605314v1).

The k=0 term is1. The k=1 term equals

\[
q(1+q)(1-q^3)=-6x-15x^2-14x^3-6x^4-x^5.
\]

For k≥2, the k+1 numerator factors each contain x; the denominator1−q removes one such factor. Thus those terms are in x^k, and cannot contribute to the first jet. Consequently c_1^{(2)}(P)=−6. Substitution into the controlling n=2 coefficient formula fixes λ_C(P)=−1 in precisely that source's convention. At n=3 the same formula gives −24. The contradiction is

\[
-24-2(-6)+0=-12\ne0.
\]

Changing orientation reverses the nonzero sign and preserves the obstruction. A common change from q−1 to log(q), q^{1/2}−1, or q^{-1}−1 multiplies all first coefficients by the same nonzero scalar. None changes ratio4 into ratio2. The sources actually match q, so no such change is needed.

## Independent weight-system mechanism

This corroboration does not use Le's first-coefficient assertion. The LMO-to-perturbative identity is independently stated and proved as Theorem1.1 of Kuriya–Le–Ohtsuki, Journal of Topology5 (2012),458–484. I checked that theorem and the weight-system definitions, Lemma3.2, and equations(6.3)–(6.4) in the actual published body. A closed degree-one Jacobi diagram is a theta graph up to sign; a graph with a self-loop vanishes by antisymmetry. Therefore the first coefficient is a manifold scalar times its theta weight. [Kuriya–Le–Ohtsuki primary body](https://letu.math.gatech.edu/Papers/LMO_Conjecture.pdf).

For B(X,Y)=tr(XY) on sl_n, root lengths squared are2. If e_a,e^a are dual bases, the adjoint Casimir is

\[
C_B(X)=\sum_a[e_a,[e^a,X]]=2nX\quad(X\in\mathfrak{sl}_n).
\]

A direct derivation uses matrix units in gl_n:

\[
\sum_{i,j}[E_{ij},[E_{ji},X]]=2nX-2\operatorname{tr}(X)I.
\]

The removed central direction commutes with X, so restriction to sl_n gives the formula. The theta contraction, up to a fixed graph sign, is consequently

\[
\operatorname{Tr}_{\mathrm{ad}}C_B=2n(n^2-1).
\]

Calibration at n=2 with −6 makes the manifold scalar −1/2 in this sign convention. The predicted coefficient is then −n(n²−1), giving −24 at n=3 independently of the Casson name or convention.

The metric must be handled explicitly: Kuriya–Le–Ohtsuki literally uses the Killing form, K=2nB on complex sl_n. Its raw theta weight is dim(sl_n), not the trace-form value. For a closed degree-d graph, scaling the form by c scales its weight by c^{-d}. In degree1 this is immediate from the Casimir. Equations(6.3)–(6.4) show that the accompanying formal parameter rescales as hbar_K=2n h when returning to the root-length2 q=e^h convention. Thus hbar_K W_K(theta)=h W_B(theta), and the cubic dependence is restored. Using the unconverted Killing result would be a false normalization argument. This caveat concerns this optional independent check; it is not a defect in the candidate, which uses the directly normalized published PSU(n) coefficient.

INDEPENDENT_CHECKS.py uses exact rational matrices, the off-diagonal basis E_ij, and diagonal H_i=E_ii−E_nn with inverse Gram matrix I−J/n. It verifies C_B(X)=2nX for every basis vector at n=2,...,6, checks the Poincare polynomial exactly, and checks both node triples1,2,3 and2,3,4. CHECK_RESULTS.json records the successful run. The all-n matrix-unit calculation supplies the proof; finite computations are corroboration, not a substitute.

## Adversarial attempts and findings

The following hypotheses failed against the source bodies or exact algebra:

- The printed R might permit a pole in q−1: it maps to the dual-number ring, which rules that out.
- n might be Lie rank, or the interpolation nodes might be q^{n−1}: both printed displays explicitly use sl_n and q^n.
- SU(n) versus PSU(n) could change this coefficient on P: the integral-sphere equality and unified projective evaluation close that route.
- A square/inverse parameter or Lescop factor could repair the ratio: uniform factors cancel, and sl_2 calibration fixes the source's exact coefficient.
- The Poincare sum might only exist at roots of unity: the unified identity in Habiro's body closes that route.
- The contradiction might be an artificial sl_1 convention: sizes2,3,4 have coefficients−6,−24,−60 and second difference−18, again nonzero.
- A raw Killing-form theta weight might be quadratic: correct conversion to the fixed normalized q produces the cubic value.
- The second quotient might be evaluated outside its nodes: the proof only uses its evaluation after killing x², justified by lifting to an actual compatible higher quotient.

**Required findings: none.** Optional improvements: the independent finite-second-quotient proof and the modulo-prime first-jet bridge could shorten or strengthen exposition; the weight-system corroboration can be appended only with its explicit metric conversion. They are not needed to make the candidate's existing proof valid.

The strongest verified result is the literal nonexistence claim for the specified Poincare sphere, and more generally for every integral homology sphere with nonzero λ_C in the controlling convention. No mathematical gap in that deduction remains under the cited published inputs. The long prior topology theorems are source-level checked inputs, not fully reproved here; neither finite tests nor this report assert formal certification. A broad priority/novelty audit remains outside this assigned phase. The scope-only Beliakova–Gorsky lead was not used or adjudicated.

All source bodies, extracts and rendered pages are private and excluded from the public payload manifest. SOURCE_READING.json separates entire-body hashing from the pages personally read. END_AUTH.json repeats the original authentication at completion.
