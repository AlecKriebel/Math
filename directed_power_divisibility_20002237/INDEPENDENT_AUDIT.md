# Independent adversarial audit: rank 462 / 20002237

Audit date: 2026-10-03 UTC.
Target: the ten original research files listed in `AUTHOR_MANIFEST.json`.

## Verdict

**PASS for the stated partial-results packet.** All five substantive mathematical claims survive the audit. No counterexample, hidden appeal to an ineffective bound, invalid quantifier manipulation, or missing sign/zero case was found. No required mathematical repair is identified.

**The complete original AIM question remains unresolved.** This is not a PASS on a purported full decision procedure or undecidability proof. The packet accurately says that it does not supply either. Its five-attempt status, partial-results label, explicit source-access limitations, and absence of a global novelty claim should remain intact.

All ten original research-file SHA-256 hashes and byte lengths match the manifest. The supplied exact-integer regression script was rerun and reproduced the recorded output. Those tests are controls, not evidence replacing the proofs. The original research files were not edited during this audit.

## 1. Target and source identity

The archived primary AIM page was independently inspected in the research browser:

https://web.archive.org/web/20191210085514id_/http://aimpl.org/definedecide/3/

Problem 3.5 is attributed to Thanasis Pheidas and specifies a fixed prime, the directed relation y = p^s x, and the existential theory over Z with addition and constants 0 and 1. Thus the packet audits the correct problem. The archived page is historical evidence; it does not establish current live-page status.

The source's convention for N is immaterial to this decision question. If R_+ uses strictly positive exponents and R_0 includes zero, the interdefinitions are R_0(x,y) iff x=y or R_+(x,y), and R_+(x,y) iff R_0(px,y). They preserve (0,0), negative values, and direction. Here px is a fixed numeral multiple.

The following source hypotheses were checked independently:

- Gitin, arXiv:2408.13900v1, section "Pheidas' work," explicitly states the existential undecidability result over N with addition and directed p-divisibility. It does not establish the corresponding integer-domain reduct. This supports the packet's domain distinction. The original 1987 publisher article was not independently accessible through the web tool; the packet candidly uses Gitin as corroboration rather than claiming an original-PDF inspection. https://arxiv.org/html/2408.13900v1
- Lechner–Ouaknine–Worrell explicitly define ordinary divisibility over Z and state decidability of existential Presburger arithmetic with divisibility. Hence interpreting exponent addition, order, and ordinary divisibility does not supply the desired undecidability transfer. https://people.mpi-sws.org/~joel/publications/epad15.pdf
- Hieronymi–Reitmeir–Wang explicitly use unary power predicates. Their language does not contain variable binary p-power scaling. https://arxiv.org/html/2602.19602v1
- Rybalov's abstract and Theorem 2.9 use positive integers, order, and the function (x,y) -> x 2^y. Publication on 1 April 2026 is confirmed in the paper. A named multiplier U that happens to be a power does not provide the exponent input y required by that theorem. https://gcc.episciences.org/17806/pdf

The exact UnsolvedMath page and original Pheidas DOI did not become readable through the web tool in this audit. This does not undermine the independently observed archived primary statement or the elementary new proofs. A bounded search supplied no exact-target resolution; no claim of literature exhaustiveness is justified or needed.

## 2. Attempt 1: lattice avoidance

**PASS.**

For each atom with no coefficient identity M=p^k L, the nonzero-L part of its truth set inside a parameter cube admits only O(log(N+2)) exponents: |L|>=1 and |M|<=C(N+1). Each exponent then gives a nonzero affine equation and at most (2N+1)^(r-1) integer points. A constant nonzero affine equation has no points, which is consistent with this bound.

The zero-L part is handled separately and correctly. R_p(0,M) forces M=0. If L is not identically zero, this lies in its proper affine hyperplane; if L is identically zero, the nonidentity assumption ensures M is not identically zero, and its zero hyperplane suffices. Opposite signs are impossible; equal negative signs cause no change to the magnitude bound.

Consequently every forbidden set that is not all of the lattice has density zero in lattice-parameter cubes, and finitely many cannot cover the lattice. This also proves the converse of the coefficient-identity criterion for an atom true everywhere; it is not being assumed in a circular way. For rank zero the lattice is a singleton, and the coefficient vector consists only of the constant, so direct evaluation gives the stated criterion.

The decision procedure does not need a numerical bound on the first good lattice point. Its yes/no test uses only Smith normal form and coefficient identities. If a witness is requested, enumeration terminates by the density argument.

Important uniformity point: when this lemma is later applied fiber by fiber, constants in the density estimate may depend on the chosen exponent. No uniform density estimate or common witness-size bound is used or required.

## 3. Attempt 2: one positive atom and arbitrary negatives

**PASS.**

### Fiber arithmetic and exceptions

The reduction q(T)z=h(T) has the correct signs. The all-zero coefficient-polynomial case, including no free variables, is separated before taking a gcd. Its affine h has either all exponents or at most one possible power root. The chosen nonzero q_j has at most one root, and that exponent is tested directly.

For every nonempty integer fiber, its integer homogeneous kernel spans the rational kernel: clear denominators in a rational basis. Translating by an integer solution proves equality of affine rational spans. This argument is conditional on integer nonemptiness and is never used to claim that a rational solution is integral.

The disequality and relation cross-product formulas have the correct constant-term sign. They test identities on that rational affine span, including singleton fibers. Vanishing restricted L is separated from the ratio test, preventing division by zero. Numerical zeros of a chosen B_k and nonidentically-zero cross products are finite exceptional parameters.

### Rational-function tail lemma

For G=T^a g and H=T^b h with nonzero constant terms, taking s larger than both constant-term p-adic valuations makes the constant term uniquely valuation-minimal in each evaluation. Thus both evaluations are nonzero and the valuation of a putative power value forces t=(a-b)s+c. This is the key effective step.

After cancellation of p^((a-b)s), power membership reduces to g(p^s)=p^c h(p^s). For negative c, multiplying by its fixed p-power denominator is legitimate. A nonzero resulting polynomial has a computable root bound, yielding a finite exponent search. A zero resulting polynomial means exactly f=p^c T^(a-b), with the remaining condition t>=0 an elementary linear inequality. This covers positive and negative degree, constant functions, a negative overall sign, zero numerator, and potential presentation poles. Beyond the valuation threshold there are no denominator zeros.

There is no approximation theorem, ineffective finiteness result, or unbounded search in the decision step. The finite/cofinite conclusion really is justified, rather than a finite empirical pattern.

### Tail nonemptiness

When gcd over Q[T] is 1, a cleared polynomial Bezout identity gives a nonzero integer N. The exact numerical gcd is gcd(N,q_1(T),...,q_r(T)), so testing its divisibility into h depends only on T modulo |N|. The multiplication-by-p orbit is finite even when p divides the modulus; modulus 1 causes no problem.

Otherwise the common polynomial gcd is primitive linear. Gauss's lemma ensures integral constant cofactors. If h is proportional to that primitive polynomial, its scalar is integral, and the test reduces to C|k. If not, Q(T)|ad-bc gives only finitely many candidates, on which the original divisibility must be evaluated. Zero-Q parameters are already separate.

A common computable threshold covers all negative-literal tests and exceptional roots. The algorithm only combines their eventual truth values with the positive-fiber nonemptiness test. It does not require an effective lattice parametrization varying polynomially with s.

## 4. Attempt 3: named-power multiplication

**PASS, including the p=2 case.**

In Ax+pU=B(x+p), p not dividing x excludes x=0. Cases A=B or B=U force complete synchronization. In the remaining case valuation comparison gives min(a,b)=1+min(b,u), hence u<b. The two orderings of a and b produce exactly x=-(p+1) or x=1, because p^k-1 dividing p-1 forces k=1. The displayed exceptional assignments genuinely satisfy the equation and are not silently ignored.

For p=2, r=3 modulo 4 is a unit and misses both exceptional values, which are congruent to 1 modulo 4. For p>=3, r=2 is a unit and differs modulo p^2 from both 1 and -(p+1). Every integer x has an allowed constant shift c. The integer k is unrestricted, so negative x are covered. The two relation atoms yield the lemma's equation with the correct +pU term.

Every occurrence of cU, pU, or p^2 k is multiplication by a fixed integer, so the construction uses only permitted additive syntax. R_p(1,U) makes U a positive p-power. It excludes U=0 and negative U; U=1 is allowed. The converse and forward implications work for x=y=0 as well as either sign.

The exponent interpretation is also correct. In the divisibility formula, U=1 forces V=1, realizing 0|b iff b=0; V=1 permits z=0 for every U, realizing a|0. For a>0 the geometric-series congruence proves p^a-1 | p^b-1 iff a|b. This is ordinary exponent divisibility, not the relation b=a p^s required for a Pheidas transfer. No exponent extraction or nonnegative-cone definition has been obtained.

## 5. Attempt 4: one shared polynomial-matrix parameter

**PASS.**

### Rank and integral lattice membership

A fixed nonzero generic minor provides a finite exceptional root set. If the augmented generic rank is larger, every possible consistent specialization must lie in that finite set. At equal positive generic ranks, a nonvanishing chosen minor of A guarantees both specialized ranks stay equal. Rank zero and the identically zero matrix are separated.

At a fixed equal-rank specialization, unimodular Smith reduction preserves the maximal-minor gcds. After diagonalizing A, the augmented minors are its diagonal product D and the numbers (D/d_i)b_i. Their gcd equals D exactly when every d_i divides b_i. The transformed b vanishes below the rank by rational consistency. Therefore this criterion is equivalent to integer, not just rational, solvability. Rectangular, underdetermined, and rank-deficient matrices are covered.

### Polynomial gcd and residue reduction

A primitive integral representative G of a rational polynomial gcd divides each integral f_i in Z[T] by Gauss's lemma. The integral cofactors have rational gcd 1 and hence a cleared constant Bezout identity. Their evaluated gcd divides that fixed nonzero constant. Formula (3) consequently gives the exact numerical gcd, including the all-zero evaluations when G(T)=0.

For each residue modulo the common positive modulus, the bounded cofactor-gcd multipliers d and e are constants. Squaring the equality of the two nonnegative determinantal gcds loses no sign information. A nonidentity polynomial has only bounded finitely many power roots; an identity permits every generic parameter of that residue. Finite-state residue dynamics plus these finite exceptions gives an effective eventually periodic exponent set. No factoring oracle or inverse of p modulo the modulus is assumed.

### Negative constraints and expression in the original language

Gaussian elimination over Q(T) yields a rational particular solution and rational kernel basis. Excluding denominator and pivot-minor zeros makes their specializations valid. Restricted affine forms may have rational coefficients: only their identities are tested on the rational span, whereas lattice avoidance is applied to the actual integer fiber. This distinction is handled correctly.

Proportionality cross products and the rational-function power lemma make every whole-fiber obstruction effectively eventually constant. A finite union of nonuniversal forbidden sets is then avoidable separately on every nonempty integer fiber. No uniform density radius is necessary.

Using G_p repeatedly to evaluate a polynomial in the shared U is a valid existential flattening. Intermediate products are uniquely determined when U is a power, so adding positive graph witnesses outside a negative final atom preserves that atom's truth. These graph formulas do not authorize synchronizing arbitrary independent original atoms.

## 6. Attempt 5: positive-existential negation elimination

**PASS.**

Unit_p uses all nonzero residues modulo p with an unrestricted integer quotient. Thus negative p-free integers are included. Every nonzero integer has exactly one signed p-free core u with R_p(u,x). Zero has none. This establishes the positive-existential NZ definition without presupposing an order predicate.

For the complement of R_p:

- The first two branches cover exactly one zero.
- Different signed cores cover different chains, including opposite signs.
- Equal cores and failure of the forward relation mean the x exponent is strictly greater; precisely this is expressed by R_p(py,x).
- NZ(y) in the last branch is necessary and is present. It prevents the false complement witness at (0,0).

There is no recursive use of negation in either replacement formula. Renaming witnesses and pulling existential quantifiers through conjunctions and disjunctions preserves the existential-positive fragment. The domain is nonempty. This is removal of atomic negations, not quantifier elimination, and the packet explicitly recognizes that new independent positive atoms are introduced.

The positive conjunction is equivalent to the stated independent-power linear system: each relation row introduces its own external s_i>=0. At zero arguments any exponent can witness an atom; this remains correct. The converse translation is valid for the stated special row form. More general polynomial coefficients are expressible through repeated G_p evaluation, with no claim that the extra powers become one shared parameter.

The multivariable Bezout obstruction is exact: T_1-1 and T_2-1 have no common nonconstant factor but vanish together, ruling out a constant in their ideal. The numerical gcd identity includes zero exponents with gcd(0,0)=0. Consequently the displayed equation has a solution iff gcd(a,b)|c with that convention. This last exponent predicate can indeed be expressed in decidable ordinary addition/divisibility arithmetic: over Z, use existence of u,v with a|u, b|v, and u+v=c. It therefore supplies no undecidability proof.

The unbounded-gcd family defeats the particular bounded-gcd/constant-modulus extension used in one variable. It is not a theorem ruling out every conceivable finite-state or other multivariable algorithm; the packet's local wording limits the claim to the attempted strategy.

## 7. Regression controls and independent checks

The supplied script reproduced exactly:

- directed complement pairs: 66,564
- nonzero witnesses: 4,100
- synchronization assignments: 289,792
- genuine exceptional assignments: 48
- named-power graph assignments: 201,240
- multi-exponent gcd cases: 8,788
- rational-function tail certificates: 1,244
- rational-function tail evaluations: 39,808
- maximal-minor lattice checks: 12,400
- fiber-identity cross-product checks: 6,281

The packaged determinant test uses nonsingular 2-by-2 matrices only. As an independent audit control, 480 small integer matrices of dimensions 1..4 by 0..4 were checked by comparing equal-rank maximal-minor-gcd membership with equality of column Hermite normal forms before and after adjoining b. All passed: 135 rank-zero, 49 rank-deficient, and 296 maximal-rank cases. This supports the rectangular/degenerate implementation intuition but is still only a bounded control.

The packaged complement checker computes p-free cores directly, and the named-power checker computes the unique residue shift directly. Those are legitimate reduced checks of the displayed formulas because the accompanying proofs establish uniqueness; they are not exhaustive searches over all existential witnesses. The manuscript accurately limits the tests' role.

## 8. Required repairs and optional clarifications

Required repairs: **none found**.

Optional clarifications, not publication blockers:

1. In the one-row common-linear-factor case, explicitly say to test the original divisibility for every candidate produced by Q(T)|ad-bc; the finite candidate condition is necessary rather than sufficient on its own. This is already explicit in the credited prior report and implicit in the decision procedure.
2. In the polynomial-matrix proof, explicitly discard identically zero minors from the polynomial-gcd lists, and state the rank-zero convention separately. The current rank split and phrase "nonzero polynomial list" already provide the intended treatment.
3. State in one sentence that density-one is relative to integer lattice parameter cubes, and that no uniform radius across exponential fibers is needed. The present proofs already work on exactly those parameter cubes.
4. If more implementation evidence is later desired, add rectangular and rank-zero matrix controls; these do not change the proof or justify claiming a complete general solver has been implemented.

Do not change the original problem status to solved, treat the rational-function lemma as a multivariable statement, silently substitute N for Z, infer an exponent-input graph from G_p, or describe the regression counts as a proof. Under those preserved limits, the frozen packet passes this audit.
