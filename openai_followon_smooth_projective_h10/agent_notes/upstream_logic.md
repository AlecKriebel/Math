# Independent audit: family 004 logic, quantifiers, and pole parity

Checkpoint: 2026-10-06 22:16 America/Los_Angeles (2026-10-07 05:16 UTC).
Reviewer: internal independent AI subagent `upstream_logic`.
Relevant audit-scope completion estimate: 100%. Overall mathematical resolution and publication completion are not certified by this sub-audit; their percentages must be maintained by the lead researcher. No source-clone files, Git state, or external services were mutated.

## Verdict and exact remaining gap

I found no concrete false step in the finite rational tests, compactness argument, coarsening lemma, or height contradiction of `02-reduction.tex`, when the stated arithmetic inputs are taken as hypotheses. I also found no concrete defect in the local-to-global pole-parity proof of `03-parity.tex` conditional on the precise pointwise 2-converse cited at lines 457–494. This is **not** a certification of the upstream undecidability theorem: the arithmetic inputs, particularly the unreviewed release theorem giving finite Tate–Shafarevich group from 2-primary Selmer corank at most one, remain indispensable dependencies.

The strongest verified result of this audit is a conditional logical reduction:

> If the fixed elliptic rank/logarithm inputs, five-point height estimate, prime-pattern ordinary-model witnesses, and positive existential pole-parity formula have exactly the properties stated in family 004, then decidability of rational polynomial solvability would imply decidability of integer polynomial solvability.

The reduction is an oracle/Turing reduction implemented by two dovetailed searches. It is not presented as a many-one reduction, an existential definition of the integers, or a dimension-preserving reduction. A material defect in any required arithmetic input blocks the claimed unconditional H10(Q) result and, therefore, blocks an unconditional geometric follow-on based on it.

## Sources actually inspected

All manuscript reads used `git show` on the read-only clone `/Users/alec/Desktop/math`, pinned at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

- Repository `README.md`: warns that outputs have different verification status and unformalized results may contain issues.
- `preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/README.md`: author OpenAI; supplied citation metadata.
- Same manuscript `build/sections/01-introduction.tex`, all 250 lines.
- Same manuscript `build/sections/02-reduction.tex`, all 888 lines. Git blob: `db15377e2584e47105f0ae215e3bc119f18acb33`.
- Same manuscript `build/sections/03-parity.tex`, all 718 lines. Git blob: `f319c4dac1ae248f95d5e76874d910cd86f04bc6`.
- Same manuscript bibliography entries `PointwiseTwoConverse`, `UnrestrictedTwoConverse`, `OddRegularFontaineMazurAtTwo`, `Cassels1962`, `PoonenStoll1999`.
- `lean/README.md`, `lean/formalization.yaml`, pinned `lean/docs` inventory, and targeted searches across pinned Lean sources.

This report's line numbers refer to these exact pinned TeX files, not to a regenerated PDF. The reviewer did not independently audit the complete 2-converse companion, the complete Fontaine–Mazur companion, or all of sections 04–06; those were assigned separately.

## Decision problem and representations

The actual main theorem at `01-introduction.tex` lines 7–11 is: no algorithm takes an integer-coefficient polynomial `f in Z[X_1,...,X_n]`, with `n` part of the input, and decides the existence of a zero in `Q^n`. There is no fixed-variable statement here.

For a precise conventional presentation, encode `n` and a finite list of coefficient/exponent tuples, using signed binary coefficients and nonnegative binary exponents. Duplicate monomials can be combined effectively and zero coefficients deleted. This or any effectively equivalent finite polynomial encoding supports the manuscript's operations. Constant polynomials, including the zero polynomial and the case of no indeterminates, are decidable directly. Integer tuple enumeration and rational tuple enumeration are computable in this presentation. Clearing finitely many fixed rational coefficients is effective.

## Finite-test and compactness reconstruction

1. `02-reduction.tex` lines 335–468 define a recursive first-order ring theory. Every exponent in a localization condition is a fixed ordinary integer for its particular axiom. No variable exponentiation, prime predicate, valuation predicate, height predicate, or full true-arithmetic oracle is built into the recursive theory. The field-quotient, quadratic-extension, elliptic group-law, and localization statements can be expressed as ring formulas with quantifiers, as explained at lines 407–433.
2. The fixed finite constants may be hardcoded (lines 461–467). Their existence suffices for the contradiction “there exists a deciding algorithm”; the proof does not require a uniform search for them from the input polynomial. This is legitimate provided they really have the required properties. The height exponent and constants need not be known by the finite-test enumeration; the converse proof selects an ordinary precision contained in the full enumerated scheme.
3. Add the proposed root constants and `f(a)=0`, then Skolemize each recursive axiom (lines 503–511). For a countable recursive axiom family this can be done effectively with countably many finite-arity function symbols. The relevant witnesses are ring-valued. The original ring-valued functions and the new Skolem functions are total in the expanded theory.
4. Enumerate ground terms and give each a prospective rational value (lines 513–524). Ring-operation identities make their value set a subring. Functionality constraints make every added function well-defined on equivalence classes of term values. Every universal ground instance is included. Because every element of the term-generated ring is represented by a ground term, these instances really imply the universal Skolemized axioms on that ring.
5. The witnesses for `Phi` and for inversion of a polynomial inequation are external rational witnesses, not new function values (lines 525–529). They need not belong to the modeled subring and do not generate further ground terms. Confusing these two sorts of witnesses would create a closure issue, but the manuscript explicitly avoids it.
6. A finite initial constraint list is an existential Boolean combination of rational polynomial equalities/inequations (lines 531–538). Negated equalities are handled by inverse witnesses, finite Boolean formulas by disjunctive normal form, and each conjunction by a sum of squares over Q. The assumed H10(Q) oracle decides each of the finitely many resulting polynomial queries. This is a finite oracle computation for each finite test.
7. If an integer root exists, the fixed ordinary Z-model can be expanded by root constants and Skolem functions; its term values are integers and satisfy `Phi`. Thus every test succeeds (lines 540–543). Choosing Skolem functions need not be computable for this soundness argument.
8. Conversely, add constants for prospective term values to the elementary diagram of the ordinary many-sorted structure containing Q, Z, R, F and the arithmetic functions (lines 555–584). Any finite diagram fragment is already true in that ordinary structure, and the finitely many prospective term constraints belong to a successful rational test. Interpret all those term constants simultaneously using that test's rational assignment; the diagram creates no additional constraint on them. Thus every finite fragment is satisfiable.
9. Compactness supplies a model of the full diagram and term constraints; the named ordinary structure embeds elementarily. The diagram need not be recursive and is never submitted to the decision oracle. A language with names for all real elements is large but still a set-sized first-order language, so ordinary compactness applies. Restrict to term values, use functionality, and obtain the asserted R embedded in the rational sort of the one ambient extension.

The final algorithm (lines 876–886) dovetails enumeration of integer tuples with evaluation of successive finite rational tests. If an integer root exists, the first search halts; if none exists, compactness plus the arithmetic converse says some test must fail, so the second halts. This uses exactly the arbitrary-variable H10(Q) decision oracle.

## Coarsening lemma: the delicate nonstandard step is valid as stated

`02-reduction.tex` lines 643–717 deserves special scrutiny. Write `nu=v_q` and let `J` be the convex subgroup of the ambient ordered integer group generated by negative valuations of nonzero ring values.

- The externally described set of values whose absolute value is bounded by a finite sum of absolute negative ring valuations is indeed a convex additive subgroup. External definition is permitted because J is used only for a mathematical existence construction, never in an algorithm or transferred formula.
- If `nu(a)` lies in J, one can choose a finite product b of ring elements with negative valuation such that `nu(b)<-|nu(a)|`. For example, first take a product supplying the finite bound and then square that product to make the domination strict. Both b and ab have negative valuation. Since every ring value satisfies the ambient `Phi`, its transferred soundness makes both valuations even; their difference `nu(a)` is even (lines 664–673).
- Therefore the selected odd-valued r lies outside J. Its valuation must be positive, since every negative ring valuation is in J by construction (lines 675–676).
- Extend nu to an ambient place of the quadratic field, and quotient its unramified ordered value group by J. This coarsened valuation is nonnegative on R and on R[sqrt(2)]. Its center is a proper prime ideal containing r (lines 677–690).
- The quotient `R[sqrt(2)]/r` is the product of two copies of the field R/r, because the supplied B_r is a root of X²−2 and 2B_r is invertible. Hence a prime containing r is exactly one of the two tested maximal branch ideals (lines 692–698).
- For `D'=r^l X/Y` with Y outside that center, the quotient valuation is at least l times the positive quotient value of r. If J=0, the original valuation is at least l. If J is nonzero, convexity makes it contain every ordinary integer; every representative of a positive quotient class then exceeds every ordinary integer. The required original bound `v_*(D')>=l` holds for every **ordinary** l (lines 700–711).
- The last conclusion would not justify arbitrary nonordinary precision l. The theorem requires only ordinary precision K and correctly preserves this restriction. It also correctly concludes only `v_*(D')>=l`, rather than the potentially stronger `v_*(D')>=l v_q(r)` in the nonzero-J case.

The proof may choose coarsenings externally one prime at a time. This does not invalidate lines 802–813: it establishes the truth, in the ambient structure, of an internal universal assertion about all primes of the internally finite radical. Transferred finite-product divisibility can then be applied to that assertion. No uniform internal choice of valuations or coarsenings is needed.

## Height contradiction and index quantifiers

`02-reduction.tex` lines 75–89 transfer the identity `mE(F)=ZP` in a many-sorted language containing the integer-multiple map. The associated eta is injective, additive, and unital. It is not assumed multiplicative. The proof explicitly identifies the potentially different ratio eta(ha)/eta(h) (lines 91–94).

The local comparison at lines 178–216 uses the same h and j0 for all a, including a=1. The conjugate comparison makes eta((h−4)a) divisible by q^K, so eta(ha) is congruent to 4 eta(a) and eta(h) to 4. Hence the denominator index is a q-unit, and the primary logarithm ratio recovers eta(a). The shared witnesses for all a are crucial; the representation axioms quantify them in exactly that order (lines 381–405). The proof does not silently interchange forall a and exists h.

For fixed ordinary precision K, every contact prime for a representation of any A forces congruence of all root coordinates with their integer indices. Thus the same nonzero integer error delta is divisible by every relevant radical to order K (lines 792–814). The polynomial bound on delta is uniform, so the slope heights, then the heights of **every** ring value, have one ordinary bound depending on f and B but not A (lines 816–840).

Applying this to the three ring elements presenting x(T_a_j) gives the upper height bound. The transferred canonical-height lower bound is quadratic in the integer index (lines 842–865), which forces B into an ordinary bounded interval. The transferred finite interval of integers consists exactly of its finitely many named ordinary members (lines 867–869). Additivity, eta(1)=1, and injectivity identify a_j with those ordinary integers (lines 870–873). This is a valid way to avoid assuming multiplicativity of eta.

## Independent pole-parity and matrix audit

`03-parity.tex` lines 71–103 prove soundness with a direct local valuation argument. If b has negative odd valuation, the quotient defining U has valuation zero, and H' has valuation 3v(b). Of the two twist parameters e and eH', one has even valuation. Scaling it to a local unit-parameter curve preserves x square class; every nonzero x on that curve has even valuation away from 2,3, contradiction. This includes t=0 and excludes zero coordinates by the formula's explicit inequations.

The fixed multiplier lists at lines 108–137 exist by finite local square-class groups and weak approximation; all their supports are incorporated into the finite exceptional set. Local choices of t in lines 139–216 give positive square-class representatives beta,theta with disjoint prime supports B,J and the mutual-square conditions. In particular B is nonempty because beta is a nonsquare at 3. This argument also covers J empty, t=0 in the valuation comparison, and denominators in U.

I independently checked the descent setup and local conditions of lines 233–454. At each odd local field the quotient E/2E has order four; at support primes the two torsion classes have independent valuation vectors; at 3 they give all first-coordinate classes with square second coordinate. The 2-adic argument is a necessary condition only, which is all the upper bound requires. Matrix calculations imply an upper bound of eight Selmer classes, and the explicit class gamma supplies the third independent direction, giving equality. Nothing in this argument claims that a Selmer class is automatically a rational point.

The actual rational-point transition is lines 457–525. Let d=dim Sha[2]. The computed Selmer dimension and full rational two-torsion give r+d=1. The usual cofinitely generated structure of Sha[2∞] gives its corank t<=d, hence 2∞-Selmer corank r+t<=1. If the cited exact pointwise 2-converse theorem really gives finite Sha under these hypotheses, the Cassels–Tate pairing for an elliptic curve with rational origin divisor is perfect and alternating on the finite group. Its finite 2-primary part has paired cyclic factors, so d is even. The manuscript correctly uses the full finite 2-primary group, not a falsely claimed perfect restriction to Sha[2]. It follows that d=0, r=1 and gamma is rational. The needed dependency is genuinely substantive and cannot be replaced by “Selmer dimension 3 implies rank 1” without the intervening finiteness input.

The simultaneous-matrix construction at lines 553–703 is internally valid. The projection `T=Id−1_B a^t` factors K through `K^#=K+lambda a^t`. A one-dimensional kernel for K^# yields `ker K=<1,1_B>` and lambda outside im K. The smaller deleted block uses an even-sum basis C and is nonsingular even when |B| is even. Adding J leaves that smaller block intact because the fixed mutual-square row sums vanish. Each free q0–J symbol independently toggles the corresponding J diagonal. The determinant's full-product coefficient is det M0=1, so the multilinear polynomial cannot vanish on the entire Boolean cube. Reciprocity-consistent prescribed symbols are realizable successively by CRT and Dirichlet.

As a falsifiable numerical check of this algebra, `parity_matrix_check.py` independently generates abstract reciprocity-consistent fixed symbols and the construction in the manuscript. With deterministic seed 4003 it checked 1,960 cases with |B|=1..7 and |J|=0..6; in each case it exhaustively tried all q0–J toggles, verified K1_B=0, nonsingularity of the smaller deleted matrix, existence of a nonsingular larger deleted matrix, rank(K)=|Q|−2, and the augmented-rank test lambda not in im K. Result: PASS. This is supporting finite evidence only; the preceding symbolic argument establishes the general mechanism. It does not certify Selmer calculations or the 2-converse.

Script SHA-256: `0cc151308e59f0e601c7e1b4c80aa703dc8667acb6b47a26e458141b3c655c51`.

## Lean scope

At the pinned commit there is no `lean/docs/004.md`. The formalization catalogue, whose header says it lists papers with formalized main results, does not list the H10(Q) manuscript. A targeted pinned Lean search for its title/path, Hilbert's tenth problem, pole parity and five-point height produced no matches.

The only nearby-name candidate found by a narrow inventory, `lean/ComparatorChallenges/RationalHitting.lean`, was actually inspected. It defines arithmetic formulas evaluated on rational matrix tuples, admissibility/nonzero evaluations, encodings and matrix-size outputs. Its semantic target is unrelated to rational Diophantine solvability or family004. It is not verification of this result. No applicable Lean declarations were identified, and no Lean build was claimed or performed. Absence of a formalization is not itself evidence of a false theorem.

## Promotion recommendation

Do not call the H10(Q) input independently verified merely because this logical audit found no defect. Complete the separately assigned arithmetic and companion audits and record their exact status. If the required 2-converse, height, rank/logarithm or prime-pattern theorem has a material unsupported step, label the unconditional follow-on blocked at that specific dependency. The finite-test/compactness route does not supply an alternative arithmetic mechanism that could repair such a gap by itself.
