# Fresh adversarial audit: rank 463 / problem 20002290

Audited 2026-10-03 UTC. Scope: the ten original research files listed in ORIGINAL_MANIFEST.json, reviewed without mathematical edits. This audit describes the original text; NARROW_REVIEW.md clears the subsequent precision repairs.

## Verdict

**HOLD the frozen text for one false, unqualified summary sentence. PASS the substantive restricted and conditional mathematics.** After the README correction below, the report is suitable to retain as **unresolved with partial progress**, subject to the explicitly unrefereed status. The other listed edits improve precision and should accompany that correction. Nothing in the report proves positive-existential definability of all rational nonsquares, proves nondefinability in the full language, or proves the uniform genus-two hypothesis.

### Required correction

README.md, line 12, says that a disjunct with at most one square atom contributes only O(sqrt(H)) positive integers. This is false without a hypothesis: the primitive-positive formula `exists s P2(s)` defines all of Q, and so does `x=x` with no square atoms.

Replace that sentence by:

> A disjunct with at most one square atom whose solution set contains no rational square contributes only O(sqrt(H)) positive integers up to H, so finitely many such disjuncts cannot define the nonsquares.

The proof in turn_02.md already excludes the all-Q branches correctly. This repair changes no theorem or proof.

### Other exact precision repairs

1. **turn_03.md, line 5:** Replace “only one independent equation involving the free parameter” with “at most one independent linear equation in all the remaining variables after additive elimination.” Add: “No additional witness-only constraints are allowed in this restricted fragment.” With a scalar parameter x, row operations can concentrate x into one equation even when arbitrarily many independent witness-only equations remain. Such systems are not unrestricted quadratic polynomial images and are not excluded here. The theorem and later boundary discussion already use the correct restriction.

2. **turn_05.md, line 55:** Replace “The argument above establishes compatibility only for a restricted family of quadratic-image tests” with: “The argument above only excludes each individual square-disjoint quadratic-image test. It does not prove finite satisfiability of even the restricted positive type at a square: a finite conjunction of these tests can reintroduce simultaneous diagonal systems.” This is the exact logical strength of the ultrapower calculation.

3. **SOURCE_GATE.md, line 9:** Replace “The source gives two equivalent target sets” with “The source gives two target sets whose positive-existential definability together is equivalent to the original assertion.” The original equivalence is to the conjunction of the two definability demands, not to either demand in isolation. The surrounding baseline discussion does correctly reduce the remaining problem to nonsquares once the nonzero definition is available.

4. **turn_01.md, line 33, optional rigor cleanup:** The proposed adjustment by 2^(k-1) toggles the next square bit, but is not itself a lift preserving the chosen root modulo 2^k. Replace the redundant root-lifting aside with: “The standard criterion that a 2-adic unit congruent to 1 modulo 8 is a square applies.” Alternatively use strong Hensel: for f(T)=T^2-x, v2(f(1))>=4>2v2(f'(1))=2. The claimed local-square construction itself is correct.

## Source and baseline gate

The live original [AIM problem list](https://aimath.org/pastworkshops/definabilityinntproblems.pdf), printed page 2, Question 6, agrees with the archived text and inspected page image. Its header is September 9–13, **2013**. The target language is exactly {0,1,+,P2}; P2 means rational square values, including zero. The displayed semantic square in the nonsquare target supplies no additional squaring function.

The credited prior formula Theta is valid. All its square-valued summands are nonnegative. At x=0 all must vanish, contradicting P2(a+2) when a=0. For x>0, rational t sufficiently close to sqrt(2) gives a=((t-2/t)/2)^2 in (0,x), while a+2=((t+2/t)/2)^2. Lagrange's four-square theorem applied to AB represents any positive rational A/B as a sum of four rational squares. Hence Theta defines positivity, and Theta(x) or Theta(-x) defines nonzero rationals, with -x expressed additively.

Nonzero then replaces every negated equality. A positive-existential nonsquare formula would replace every negated P2 atom; distributing the quantifier-free part into disjunctive normal form handles existential formulas in every finite arity. Conversely, the general existential-to-positive-existential assertion includes these unary complements. Fixed rational parameters can be eliminated by unique additive equations. This is correctly credited baseline, not a full solution or an extra fresh attempt.

## Attempt 1: finite square classes and fixed places — PASS

The fixed class c Q*^2 is positively definable using a square-value variable, the prior nonzero formula, and a fixed-scalar additive equation. A prime outside the finite numerator/denominator support of c_1,...,c_r has valuation 1 there, whereas each c_i q^2 has even valuation. This defeats every finite collection, including collections containing square coefficients.

For a finite prime set S, m=4 product(S) is at least 4, so m^2 < m^2+1 < (m+1)^2. An integer that is a rational square is an integer square; therefore x=m^2+1 is a positive rational nonsquare. At each odd p in S, x=1 modulo p and the root 1 is simple. At p=2, x=1 modulo 16, hence is a square in Q_2. At the real place x>0, hence is a real square. The empty S case also works (x=17).

Thus the candidate defeats any finite list of local nonsquare predicates, even if the real place is included. No step converts an arbitrary positive-existential formula into such a list. That missing implication is correctly not claimed.

## Attempt 2: normal form and one-atom bound — PASS, with README repair

Positive-existential formulas distribute into finitely many primitive-positive branches. Every additive term is affine linear. Introducing s_j for each P2 argument and taking a rational basis of the left nullspace of the unrestricted-witness coefficient matrix eliminates precisely those unrestricted witnesses. This gives C's+B'x=d' together with P2(s_j). Rational denominators and negative coefficients can be cleared or moved across equations. The reverse translation of each fixed-coefficient simultaneous diagonal system is also valid. No original-language variable squaring or mixed product has been introduced.

For one square atom, the affine feasible set in (x,s) has dimension 0, 1, or 2, or is empty. Its square-restricted projection is empty, a singleton, all Q, or {x:P2(ax+b)} with a nonzero. This exhausts horizontal, vertical, nonvertical, and rank-zero cases; zero square atoms give the stated affine projection special case.

If an integer n belongs to the last set, choose D with Da,Db integral. Then (Dq)^2=A n+B for integers A=D^2 a != 0 and B=D^2 b. Since Dq is rational with integral square, it is integral. There are O(sqrt(H)) possible integer roots for 1<=n<=H, and A!=0 gives at most one n per root. Negative A and negative radicands cause no exception. All-Q branches cannot occur in a union equal to nonsquares. The remaining branches have O(sqrt(H)) positive integer values, versus H-floor(sqrt(H)) nonsquares. This is an unbounded proof; the bounded controls are unnecessary for its validity.

## Attempt 3: all multivariate degree-at-most-two images — PASS

The exact classical input is [Poonen's arithmetic geometry notes](https://math.mit.edu/~poonen/782/782notes.pdf), Theorem 26.3, with all completions including R. Its application uses a nonzero represented target, so the convention requiring a nonzero representing vector for target zero is irrelevant.

If c+q(Q^r) avoids all rational squares, then c itself is a nonsquare and in particular c!=0. The form h(z,w)=q(z)-w^2 fails to represent -c. After deleting its radical, h is nondegenerate and still has rank at least one because of the -w^2 summand. Hasse–Minkowski supplies a completion where -c is not represented. Every rational value in the original image that were square in this completion would furnish such a representation. This yields one fixed local obstruction for the whole image.

The affine/projective gap is closed correctly: if a rational zero of h(z)-a t^2 has t=0, its z component is a nonzero isotropic vector of the nondegenerate h. Choosing w with B(z,w)!=0 makes h(sz+w)=2sB(z,w)+h(w) attain every rational target. Thus a point at infinity does not invalidate affine representation. Removing the radical first is essential and is done in the report. Rank-one, constant-image, and zero-dimensional-input cases are covered.

For f(z)=z^T A z+l^T z+c with A symmetric, if l does not annihilate ker A, some rational kernel direction makes f surjective onto Q. Otherwise l belongs to im A, so 2Ah=l is solvable over Q; completing the square and rational diagonalization reduce the image to the preceding form. This includes singular A, A=0, linear and constant polynomials, and any finite number of variables. Every constituent of a putative union equal to nonsquares must avoid squares, so surjective cases cannot occur. Selecting the finite set of obstruction places and applying Attempt 1 gives the contradiction.

This proof concerns unrestricted polynomial images, or one remaining equation total. It does not apply to a parameter equation with additional witness-only equations, intersections of images, or general projections of constrained varieties. The scope edit above prevents that overreading.

## Attempt 4: conditional genus-two/Büchi argument — PASS as conditional

The hypothesis is a single uniform B for the rational-point count of every smooth projective genus-two curve over Q (in the usual geometrically integral sense). Pointwise finiteness for each curve would not suffice. The report does not assert this hypothesis as a theorem.

For delta=y-x^2 != 0, the monic quadratic f has at most two roots, so one epsilon in {0,1,2} has f(epsilon)!=0. For g(U)=f(U^3+epsilon)=(U^3+c)^2+delta, g'=6U^2(U^3+c). A common root forces either f(epsilon)=0 or delta=0. Neither is allowed. Thus g is squarefree of degree six, its hyperelliptic double cover is geometrically integral, and its smooth projective model has genus two. Affine points with U=1,...,B+1 are distinct and inject into that model. Their tested indices j^3+epsilon are <=(B+1)^3+2=M-1. Even a zero V-coordinate still supplies a rational point, so there is no square-zero exception. This contradicts the uniform B.

Consequently M=(B+1)^3+3 square tests define y=x^2 under the hypothesis. Polarization then defines multiplication, using 2c=u-s-t and characteristic zero. Ring polynomial equations can be compiled with finitely many intermediate variables while preserving existential positivity. [Poonen's nonsquare theorem](https://math.mit.edu/~poonen/papers/nonsquares.pdf), Theorem 1.1, is a full-ring-language input and becomes usable only after this compilation. Its set Q* minus Q*^2 is exactly Q minus Q^2 because zero is a square.

The discriminant identity and the rational five-term example check exactly. [Lipman's notes](https://www.math.purdue.edu/~jlipman/Buchitalk-Huge.pdf) give the tuple on printed page 10 (PDF page 11), so the report's page citation is correct. The rational exceptional quadratic T(T-1) explains why blindly copying an integer two-shift argument is unsafe; the three-shift proof is valid. [Pasten's Theorem 5.9](https://indico.ictp.it/event/9617/session/2/contribution/4/material/1/0.pdf) supplies the credited integer uniformity strategy, not the stated rational theorem as an unconditional citation.

The inspected [Xiao v3 Theorem 1.3](https://arxiv.org/html/2412.16740v3) explicitly concerns integer squares; the current arXiv record still identifies v3 as the June 7, 2025 revision. No validation of that proof is needed or supplied. Clearing denominator D changes second difference 2 to 2D^2, so it cannot transfer that statement to the needed rational problem. The [Pasten–Vidaux abstract](https://people.math.harvard.edu/~hpasten/preprints/PVmultPoly.pdf) is conditional and over integers. None of these sources closes the remaining unconditional gap.

## Attempt 5: projections, preservation, and ultrapower — PASS, with type precision edit

For finite r>=1, additive homomorphisms Q^r to Q are Q-linear. Predicate preservation on the square-valued standard basis implies square coefficients c_i, and preservation of the named 1 implies their sum is 1. Two nonzero coefficients permit the square-valued input with entries 1/c_i and 1/c_j, whose image is the nonsquare 2. Thus exactly one coefficient is 1. This proves the stated classification, including r=1. It says nothing about infinite powers or all nonstandard model homomorphisms. Coordinate projections preserve every relation, so these tests are indeed vacuous for distinguishing nonsquares.

For T=Th(M), the relative preservation criterion is correct. The key compactness step uses all positive-existential consequences of phi=not P2. A finite inconsistency in the proposed type would give a finite disjunction of excluded positive-existential formulas, contradicting satisfaction of those consequences. This supplies A,a whose positive-existential type is included in that of B,b. The positive atomic diagram of A together with the elementary diagram of B is finitely satisfiable by existentially quantifying the finitely many extra A constants. Compactness gives a homomorphism A to an elementary extension B* with a sent to b. Reflection then implies phi(b). A final compactness argument produces one finite conjunction equivalent to phi modulo T. Function symbols and named constants are handled by the positive atomic diagram. No injectivity assumption is smuggled in; the known positive nonzero definition subsequently implies injectivity. The indexed primary text of [Bodirsky, Theorem 2.5.2](https://wwwpub.zih.tu-dresden.de/~bodirsky/Book.pdf) confirms exactly the cited criterion, although a full direct fetch was unavailable.

The inclusions into R or Q(sqrt(2)) are correctly rejected because their targets do not satisfy T. Finite powers M^r are not a replacement for arbitrary models of T either.

For the displayed nonprincipal ultrapower, every a_n is nonsquare, so Los gives not P2(a). Each fixed square-disjoint quadratic-image formula is eventually false along a_n by its one fixed obstruction place. This establishes exactly the claimed avoidance result. It does not establish finite compatibility of the positive type with P2, nor a required homomorphism. The missing step includes finite conjunctions of individually permissible quadratic-image tests; the proposed wording repair makes this particularly important point explicit.

## Reproducibility and controls

All ten files match the frozen manifest's byte counts and SHA-256 hashes. The verifier was copied to a temporary directory and rerun there, so its write of verification.json did not alter the release. All eight groups passed and the regenerated JSON equals the archived JSON exactly: 32 finite-place examples / 80 prime-power checks; four counting samples; 255 rational samples for 3+2z^2; the five-square rational tuple and defect; the degree-six discriminant; the two-shift rational exception; polarization; and the representative failed nonprojection.

These are controls and exact displayed-identity checks. They prove neither uniformity nor global definability or nondefinability. No issue was found with the report's repeated statement of that limitation.

## Final boundary

The nonsquare-complement problem remains unresolved by these five attempts. The valid output is a corrected partial-results report, with no historical novelty claim. The only demonstrably false theorem-like sentence found is the unqualified README counting summary, and its correction is already contained in the body proof. Additional scope and type wording repairs above prevent stronger, invalid interpretations without changing the established deductions.
