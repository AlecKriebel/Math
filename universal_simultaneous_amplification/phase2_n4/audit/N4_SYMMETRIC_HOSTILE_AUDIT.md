# Hostile audit of the symmetric weighted K4 classification

Date: 2026-08-01 (America/Los_Angeles)

Scope: phase2_n4/n4_symmetric_classification.md,
phase2_n4/derive_lumped_certificates.py,
phase2_n4/crosscheck_full_chain.py, and phase2_n4/search_exact_k4.py.
No literature search or external contact was used. The source report and
scripts were not edited.

Labels:

* **[PROVED]** means the claim follows exactly under its stated domain;
* **[VERIFIED]** means an exact independent recomputation agreed;
* **[LIMITATION]** means a verification claim is narrower than a fully
  independent proof, without invalidating the theorem; and
* **[WORDING]** means a sentence should be tightened but is not mathematically
  false under its natural reading.

## Executive verdict

I found no counterexample and no theorem-level error. The two conclusions

\[
 \rho_{\rm dB}(G_{13}(x),r)\le \rho_{\rm dB}(K_4,r)
\]

for \(x>0,r>1\), with equality only at \(x=1\), and

\[
 \rho_{\rm dB}(G_{22}(x,y),r)\le \rho_{\rm dB}(K_4,r)
\]

for \(x,y>0,r>1\), with equality only at \(x=y=1\), are proved by the displayed
certificates.

The exact orbit transitions, both rational comparison identities, both
denominator arguments, the square-root substitution, every coefficient sign,
and all strictness implications check out. The claimed 123 monomials of
\(P_{22}\) are present, all with positive integer coefficients.

The main qualification is verification scope. The shipped full-chain
cross-check is genuinely a separate state-space implementation, but it imports
the orbit solver as its expected answer and performs full 14-state solves only
at four rational weight specializations. It is an independent implementation
cross-check, exactly as the status key defines that phrase, but not a second
independent symbolic proof of the global sign certificate. During this audit I
also ran the full 14-transient-state solver with symbolic \(x,y,r\); it agreed
identically with the orbit solution, although that expensive check is not in
the shipped script.

## 1. Orbit chain and baseline

### **[PROVED] Strong lumpability**

For a state with \(i\) mutants in class A and \(j\) in class B, all resident
A targets see mutant incident mass

\[
 i\alpha+j\gamma
\]

and resident incident mass

\[
 (p-i-1)\alpha+(q-j)\gamma.
\]

Multiplying the mutant-replacement probability by the chance
\((p-i)/(p+q)\) of selecting a resident A target gives the first line of (1).
For a mutant A target, its own absent self-loop changes the mutant internal
count from \(i\) to \(i-1\), giving the second line. The two B formulas follow
identically. Thus all transition totals depend only on \((i,j)\).

Equivalently, \(S_p\times S_q\) preserves the weighted graph, its mutant-set
orbits are exactly the count pairs, and its transition kernel is invariant.
The six and seven transient-orbit counts are correct:

\[
 2\cdot4-2=6,\qquad 3\cdot3-2=7.
\]

Terms omitted because of zero target multiplicity cause no missing
state-changing transition. In the two claimed families, every denominator
that remains is positive for the stated positive weights and \(r>1\).

### **[PROVED] Parameter normalization**

A singleton core has no internal edge orbit. Full \(S_3\) symmetry leaves only
the core--satellite and satellite--satellite orbits. Multiplying every edge
weight by one common positive constant cancels from each dB replacement
ratio, so normalizing the cross weight to one leaves exactly one parameter.
The report's parameter-count clarification is correct.

For the 2+2 action, the two internal pair edges and the four cross edges form
three edge orbits. The same normalization leaves exactly \(x,y\).

### **[PROVED AND VERIFIED] Complete baseline**

For \(k=1,2,3\) mutants on \(K_4\), the state-changing count probabilities are

\[
 p_k^+=\frac{4-k}{4}\frac{rk}{rk+3-k},
 \qquad
 p_k^-=\frac{k}{4}\frac{4-k}{r(k-1)+4-k}.
\]

Direct solution of the three count equations gives

\[
 \rho_{\rm dB}(K_4,r)
 =\frac34\frac{1-r^{-1}}{1-r^{-3}}
 =\frac{3r^2}{4(r^2+r+1)}.
\]

The separate generic 14-transient-state solver returned exactly the same
rational function.

## 2. The 1+3 certificate

### **[PROVED] Rational identity (4)**

The derivation script builds the six equations directly from (1), solves them
over the rational-function field, averages the singleton core and satellite
states with weights \(1/4\) and \(3/4\), and checks

\[
 \Delta_{13}
 :=\rho_{\rm dB}(G_{13}(x),r)-\rho_{\rm dB}(K_4,r)
 =-\frac{3r^2(r-1)(x-1)^2F_{13}}
 {4(r^2+r+1)P_{13}}
\]

by exact symbolic cancellation. I independently recomputed the full
14-transient-state chain with symbolic \(x,r\), without lumping, and obtained
zero residual against this orbit answer.

Manual comparison of the report and script found no transcription mismatch in
\(F_{13}\) or \(P_{13}\).

### **[PROVED] Denominator and strictness**

Expanded \(F_{13}\) has 14 nonzero monomials and \(P_{13}\) has 27; both lie in
\(\mathbb Z[r,x]\), and every nonzero coefficient is strictly positive.
Consequently both are positive for \(r>1,x>0\). The remaining denominator
factors are manifestly positive.

The numerator is zero in the stated open domain exactly when \(x=1\), because
\(r-1>0\), \(r^2>0\), and \(F_{13}>0\). At \(x=1\), all six edges have equal
weight, so this is precisely the complete-graph equality case.

There is another equality boundary at \(r=1\) for every \(x\), as neutrality
requires, but the theorem explicitly assumes \(r>1\). No equality case is
missing.

## 3. The 2+2 rational identity and denominator

### **[PROVED] Rational identity (5)**

The seven orbit equations yield a canceled rational comparison. The code
extracts its numerator and denominator and verifies exactly that

\[
 \Delta_{22}
 =-\frac{r^2(r-1)H_{22}(x,y,r)}
 {4(r^2+r+1)P_{22}(x,y,r)}.
\]

It also verifies that division of the comparison numerator by
\(-r^2(r-1)\) leaves a polynomial, rather than a rational expression.

As a stronger audit check than the shipped specializations, I ran the generic
full subset-state solver with symbolic \(x,y,r\). The computation took about
113 seconds and returned an identically zero residual against the orbit
solution.

### **[PROVED] Coefficientwise denominator positivity**

Exact inspection gives

\[
 P_{22}\in\mathbb Z[r,x,y],
\]

with exactly 123 nonzero monomials. Every coefficient is a positive integer;
the smallest coefficient is 2. Hence \(P_{22}>0\) for every
\(r,x,y>0\), independently of the determinant argument.

The helper named positive_integer_coefficients checks exact SymPy positivity
of every nonzero coefficient. It does not explicitly assert integrality or
the count 123, but direct polynomial-domain inspection confirms both report
claims.

### **[PROVED] Determinant/M-matrix certificate**

Let \(M_{22}\) be the holding-step-free transient matrix constructed by the
script: its diagonal entry is the total probability of a state-changing move,
and its transient off-diagonal entries are the negatives of the corresponding
move probabilities. If \(D\) is its positive diagonal and \(\widehat Q\) is
the transient matrix of the embedded state-change chain, then

\[
 M_{22}=D(I-\widehat Q).
\]

All positive-weight finite chains in this family reach an absorbing state
almost surely, so \(\rho(\widehat Q)<1\). Thus \(M_{22}\) is a nonsingular
M-matrix and

\[
 \det M_{22}>0.
\]

The script verifies the exact reduced identity

\[
 \det M_{22}=\frac{P_{22}}{128L_{22}},
\]

with precisely the eight factors of \(L_{22}\) displayed in (6). Every factor
is positive in the stated domain. Therefore this second denominator argument
is also valid.

### **[LIMITATION] The two denominator checks are not implementation-independent**

Coefficient positivity and the determinant identity are logically distinct
certificates, but both are computed in the same SymPy script from the same
orbit matrix. The phrase "independently checks both" is safe if it means
"checks both separately." It should not be read as two independent software
implementations. This is only a verification-scope qualification because
either exact certificate proves positivity on its own.

## 4. Square-root substitution

### **[PROVED] Symmetrization is exact**

Swapping the two vertex pairs exchanges \(x\) and \(y\), so the comparison is
symmetric. More concretely, the script applies exact polynomial
symmetrization to \(H_{22}\), checks zero remainder, and obtains a polynomial
in

\[
 s_1=x+y,\qquad s_2=xy.
\]

It then substitutes

\[
 s_1=2g+d,\qquad s_2=g^2,\qquad r=1+t.
\]

The expanded residual against \(\sum_{k=0}^4C_k(g,t)d^k\) is checked to be
identically zero. No numerical square-root evaluation is involved.

### **[PROVED] The substitution covers the whole positive quadrant**

For \(x,y>0\), taking the positive roots

\[
 g=\sqrt{xy}>0,\qquad
 d=(\sqrt x-\sqrt y)^2=x+y-2g\ge0
\]

obviously gives the required elementary symmetric functions.

Conversely, every formal sign-domain point \(g>0,d\ge0\) comes from positive
\(x,y\). Put

\[
 u=\frac{\sqrt{d+4g}+\sqrt d}{2},\qquad
 v=\frac{\sqrt{d+4g}-\sqrt d}{2}.
\]

Then \(u,v>0\), \(uv=g\), \((u-v)^2=d\), and one may take
\(x=u^2,y=v^2\). The only ambiguity swaps \(x\) and \(y\), which cannot affect
the symmetric polynomial. Therefore the sign proof loses neither a branch nor
a parameter region.

Also,

\[
 d=0\iff x=y,\qquad
 d=0,\ g=1\iff x=y=1.
\]

## 5. Numerator coefficients and strictness

### **[PROVED] \(C_0\)**

For \(g>0,t>0\), every nonzero coefficient of \(R_0\) is positive, so
\(R_0>0\). The factorization

\[
 C_0=2t(g-1)^2(g+1)(t+1)R_0
\]

therefore gives

\[
 C_0\ge0,\qquad C_0=0\iff g=1.
\]

The last equivalence uses \(t>0\); at the excluded neutral boundary \(t=0\),
\(C_0\) vanishes for every \(g\).

### **[PROVED] \(C_1\)**

Every coefficient in powers \(t^0,\ldots,t^5\) is a polynomial in \(g\) with
positive coefficients. The only negative displayed monomial in the
\(t^6\) coefficient is controlled exactly by

\[
 g^4+4g^3-2g^2+4g+1
 =(g^2-1)^2+4g(g^2+1)>0
\]

for \(g>0\). Thus \(C_1>0\). The script checks the identity and all six lower
coefficients exactly.

### **[PROVED] \(C_2,C_3,C_4\)**

Every nonzero coefficient in the displayed polynomials is a positive integer.
Each polynomial is nonzero, so

\[
 C_2>0,\qquad C_3>0,\qquad C_4>0
\]

throughout \(g>0,t>0\). The report and code formulas agree term for term.

### **[PROVED] Unique zero**

If \(d>0\), then \(C_1d>0\), while every other summand in (8) is nonnegative,
so \(H_{22}>0\). If \(d=0\), then \(H_{22}=C_0\), which is positive unless
\(g=1\). Hence

\[
 H_{22}=0
 \iff d=0,\ g=1
 \iff x=y=1
\]

for \(x,y>0,r>1\). Combined with the positive denominator and outer negative
sign, this proves the theorem and all strictness claims.

No unmentioned cancellation between the \(C_kd^k\) terms is possible because
all summands are nonnegative in the full transformed domain.

## 6. Exact asymptotic and boundary attacks

The following exact expansions provide checks independent of the large
displayed numerator polynomials.

### **[VERIFIED] Strong selection**

For fixed positive weights,

\[
 \Delta_{13}
 =-\frac{3(x-1)^2}{16x}\frac1r+O(r^{-2}),
\]

and

\[
 \Delta_{22}
 =-\frac18\left(
   \frac{(x-1)^2}{x}+\frac{(y-1)^2}{y}
 \right)\frac1r+O(r^{-2}).
\]

These are exactly the complete-support sum-of-squares coefficients obtained
directly from incident-star heterogeneity. They have the same unique equality
cases as the finite-\(r\) certificates.

### **[VERIFIED] Weak selection**

At \(r=1\),

\[
 \left.\frac{\Delta_{13}}{r-1}\right|_{r\downarrow1}
 =-\frac{(x-1)^2(3x+2)}
 {8(x+1)(3x^2+4x+2)}.
\]

For 2+2,

\[
 \left.\frac{\Delta_{22}}{r-1}\right|_{r\downarrow1}
 =-\frac{(x-y)^2(xy+2x+2y+5)}
 {4(x+2)(y+2)(x+y+2)(x+y+4)}.
\]

The first-order term vanishes along \(x=y\), as expected because those graphs
are weighted-regular. On that diagonal the next term is

\[
 \left.
 \frac{\Delta_{22}(x,x,r)}{(r-1)^2}
 \right|_{r\downarrow1}
 =-\frac{(x-1)^2}{24(x+2)^2},
\]

so noncomplete diagonal members remain strict suppressors for every
sufficiently small positive selection strength. This independently confirms
the extra factor \(t\) in \(C_0\).

### **[VERIFIED] Zero and infinite internal-weight boundaries**

Although the theorems assume positive internal weights, their rational
expressions have informative one-sided limits:

\[
 \lim_{x\downarrow0}\Delta_{13}
 =-\frac{(r-1)(3r^3+12r^2+8r+1)}
 {16(r+1)^2(r^2+r+1)}<0,
\]

\[
 \lim_{x\to\infty}\Delta_{13}
 =-\frac{r(r-1)(r+2)}
 {4(r+1)(r^2+r+1)}<0.
\]

On the 2+2 diagonal,

\[
 \lim_{x\downarrow0}\Delta_{22}(x,x,r)
 =-\frac{r^2(r-1)^2}
 {4(r^2+r+1)(3r^2+2r+3)}<0,
\]

\[
 \lim_{x\to\infty}\Delta_{22}(x,x,r)
 =-\frac{r^2(r-1)^2}
 {4(r^2+1)(r^2+r+1)}<0.
\]

For fixed \(y>0\),

\[
 \lim_{x\to\infty}\Delta_{22}(x,y,r)
 =-\frac{(r-1)(2r+1)}{4(r^2+r+1)}<0.
\]

The same final limit occurs along the extreme reciprocal path
\(x\downarrow0,y=1/x\) and after taking \(x\downarrow0,y\to\infty\).
No boundary approach revealed a positive comparison or an extra equality.

There is an expected noncommutation of limits: for every fixed positive
complete-support weighting, \(\Delta\to0\) as \(r\to\infty\), whereas setting
an internal weight to zero first changes the support and can leave a nonzero
strong-selection gap. The report makes no uniform-in-weights claim, so this is
not a defect.

### **[VERIFIED] Exact adversarial points**

Using the separate Fraction-only 14-state solver, I checked:

* \(x,y\in\{0,10^{-6},10^{-2},1,10^2,10^6\}\);
* \(r\in\{1+10^{-6},2,10^6\}\); and
* all corresponding 1+3 points and the full 2+2 Cartesian product.

All 126 comparisons had the asserted sign, including the connected
zero-internal-edge boundaries. The only exact equalities were \(x=1\) for
1+3 and \(x=y=1\) for 2+2.

These tests are not needed for the proof, but they found no counterexample in
the numerically delicate weak-selection, strong-selection, tiny-weight, or
large-weight regimes.

## 7. Audit of software independence and replay claims

### **[PROVED] Derivation script**

derive_lumped_certificates.py does not import src.exact_markov. It constructs
the quotient equations directly from the dB rule and checks:

* exact equality of (4) to the solved 1+3 quotient;
* exact equality of (8)--(13) to the transformed 2+2 numerator;
* all elementary coefficient claims and identity (14);
* polynomiality and coefficient positivity of both reduced denominators; and
* the determinant identity (6).

All assertions passed under the project's Python 3.14 / SymPy 1.14
environment.

### **[PROVED, with a precise limitation] Full-chain cross-check**

crosscheck_full_chain.py obtains transition rows from src.exact_markov, not
from the orbit builder. It aggregates those rows over explicit bitmask orbit
cells, verifies strong lumpability, solves the quotient with a locally written
linear system, and compares against the orbit solver. It then solves the full
14-state system at four rational weight specializations. All checks passed.

This is a valid separate-implementation check of transitions, lumpability,
and orbit solutions. Its limitations are:

1. it imports solve_average from derive_lumped_certificates.py as the expected
   answer;
2. its four full-state solves specialize the weights before solving;
3. it does not independently derive or sign-check the \(C_k\) certificate; and
4. the statement that it checks row stochasticity partly duplicates an
   assertion already performed inside src.exact_markov.transition_row.

Thus the report's specifically defined phrase "comparison with the separate
full subset-state solver" is accurate. A phrase such as "independent proof of
the full theorem" would be too strong, but the report does not use that phrase.

For additional audit assurance, full symbolic subset-state recomputations for
both families also returned zero residual. The 2+2 symbolic solve is much
slower than the quotient calculation, explaining why the replay script uses
rational specializations.

### **[VERIFIED OBSERVATION] Exact search**

The default exact search replay completed and reported:

* 1,352 2+2 grid comparisons;
* zero positive family comparisons;
* 5,000 deterministic unrestricted trials; and
* no positive unrestricted trial.

The count \(13^2\cdot8=1{,}352\) is correct. The search uses a separately
implemented Fraction Gaussian solver and no floating-point arithmetic.

### **[WORDING] Trials need not be distinct**

The deterministic unrestricted loop samples with replacement, so its 5,000
trials are not guaranteed to be 5,000 distinct six-edge weightings. Calling
them "5,000 trials" is exact; calling them "5,000 weightings" can weakly imply
distinctness. This has no bearing on the theorem because the report correctly
labels the search observational.

## 8. Final claim-by-claim status

* **[PROVED]** 1+3 rational formula, denominator positivity, strict
  suppression, and equality only at \(x=1\).
* **[PROVED]** 2+2 rational formula and \(P_{22}>0\).
* **[PROVED]** square-root substitution is exact and covers all
  \(x,y>0\).
* **[PROVED]** every \(C_k\) sign and the sum-of-nonnegative-terms argument.
* **[PROVED]** equality only at \(x=y=1\) for \(r>1\).
* **[PROVED]** family-level classification for the two stated symmetric
  complete-support families.
* **[CORRECTLY OPEN]** unrestricted six-edge weighted \(K_4\) remains
  unclassified by this report.
* **[LIMITATION ONLY]** the shipped cross-check is independent at the
  transition/state-space implementation level, not a second global
  positivity proof.

Subject only to the minor independence and wording qualifications above, the
report meets an exact first-principles proof standard.
