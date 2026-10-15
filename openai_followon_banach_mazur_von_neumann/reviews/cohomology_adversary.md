# Independent adversarial audit of upstream family 295

Reviewer: internal AI subagent `cohomology_adversary`; this is not human peer review.

Audit completed: 2026-10-06 22:15 PDT (2026-10-07 05:15 UTC).
Checkpoint estimate: 95% complete for this mathematical source audit. This percentage is an estimate of audit work, not evidence for the theorem or the parent project's publication readiness. Formal build/axiom reproduction is assigned to a separate reviewer.

## Verdict and exact scope

No substantive mathematical gap or counterexample was identified in the arguments actually needed from family 295. I independently read all five manuscript source sections, following the proof through its central new steps rather than treating the theorem statement, release provenance, or Lean scope document as a certificate. At the level of a conventional proof audit using the cited classical von Neumann algebra results, the manuscript supports

\[
 H_b^k(M,M)=0\qquad(k\ge2)
\]

for every complex von Neumann algebra, where cochains are ordinary bounded complex multilinear maps, coefficients are the original algebra with multiplication actions, and coboundaries are the actual image of the Hochschild differential. In particular, the ordinary self-coefficient groups in degrees 2 and 3 are within the checked scope.

The strongest directly reconstructed intermediate result is: for a type II1 algebra with a faithful normal tracial state, every separately normal bounded cocycle in degree at least two has a bounded primitive of norm at most the cocycle norm. The manuscript then correctly removes the remaining restrictions. Its global conclusion is not merely a normal or completely bounded cohomology assertion.

No exact mathematical obstruction remains from this audit. Its practical limitation is that I did not recompile the complete actual Lean dependency closure, and I did not reprove every classical structural theorem used in the manuscript from first principles. The separate formal reviewer must supply the build/axiom evidence; my source search or review of declarations is not a substitute for that check.

## Sources actually inspected

Original manuscript directory, read only:

`/Users/alec/Desktop/math/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026`.

Pinned source copy:

`sources/upstream/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026`.

The five source sections have identical SHA256 hashes in the original and pinned copy:

| Section | SHA256 |
|---|---|
| 01-introduction.tex | ddec01dc15fa257e3f1e85004b54225dd43df633bbdfa957de98353c069ce4b2 |
| 02-walk.tex | 3d1015a1c20d2cfc8a4c8991652d93eed756763cd982cbc28a53fd625b7b3314 |
| 03-liouville.tex | 7782c390e534a15d35d7aee470ff425fcb6823c4073b29886f3dbffbc8d31622 |
| 04-rigidity.tex | 9cf9cf2b11fc838326321b4c0384904a303ecec43d732cd748c9204059f4ea60 |
| 05-cohomology.tex | c6c8e63bac0e543624ac63fd50a046878ba7082a531115111563455682e4d437 |

I also inspected the original README, bibliography, real Lean declarations in `OAI/Analysis/BoundedHochschild/Main.lean`, and the relevant definitions/proofs in `Conditional.lean`, `ClassicalVanishingReduction.lean`, `ProperlyInfinitePrimitives.lean`, `TracialDecomposition.lean`, `TypeIICharacterization.lean`, `RightModuleAveragingExistence.lean`, and `Liouville.lean`.

Primary external sources read during this audit (2026-10-06 PDT):

- [Popa, Independence properties in subalgebras of ultraproduct II1 factors, arXiv:1308.3982v3](https://arxiv.org/pdf/1308.3982), especially Theorem 0.1(a), pp. 1–2, and the ultrapower factor/commutant discussion in section 1.6.
- [Christensen–Pop–Sinclair–Smith, Hochschild cohomology of factors with property Gamma](https://arxiv.org/pdf/math/0107078), especially equation (1.1) and the normal reduction discussion in section 2. These support the two classical cohomological inputs without adding Gamma to the new proof.
- [Johnson–Kadison–Ringrose, Cohomology of operator algebras III, bibliographic primary record](https://www.numdam.org/articles/10.24033/bsmf.1731/). The original full PDF was not needed for this audit because the exact normal-reduction statement is recalled in the inspected CPSS primary paper.

## Independent reconstruction and attack record

| Mechanism | What was independently checked | Status / precise remaining gap |
|---|---|---|
| Popa freeness | Constant coordinate factors `M_n=Q_n=P` in Theorem 0.1(a); scalar relative commutant; finite iterative adjunction | Supports the stated input; no amenability requirement on the coefficient algebra in case (a) |
| Finite path tests and one measure | Distinguished labels, reduced-word freeness, finite simultaneous tests, fiberwise measurable selection, four bad-event bounds | No gap found; uses classical separable direct-integral structure |
| Martingale and endpoint selection | Hilbert martingale increments, reversed inverse paths, independence of disjoint half paths, fixed-stage conditioning and diagonal selection | No independence of a path and its inverse is assumed |
| First-letter rigidity | Haagerup decomposition, operator-norm transfer by faithful moments, surviving-index errors, ordered blocks, Catalan law and polar approximation, spectral compression | No gap found; finite faithful trace is essential |
| Normality and averages | Orthogonal-support random-sign argument, surviving continuity modulus, pointwise ultraweak compactness, stationary limit | No normality of the limit is assumed; no commutation of averaging with `d` is needed |
| Cocycle primitive | Explicit averaged `df=0` identity, degree signs, evaluation at 1 and norm bound | Produces an actual bounded primitive; no closure of the range |
| Nonseparable and central completion | Countable II1 subalgebras, expectation/bimodularity, eventual exactness, uncountable central product, correction of mixed inputs | No separability or faithful scalar trace remains in the final theorem |

### The pivotal Popa scope

This was the most plausible place for a concealed amenability or separability restriction. It passes the direct-primary-source check. Apply case (a), not case (b), with every coordinate equal to a II1 factor `P` and the full coordinate subalgebra also equal to `P`. The ambient ultraproduct is `P^omega`; the relative commutant of its full subalgebra is scalar because the ultrapower is a factor. A nonzero diffuse factor corner cannot embed into the scalar algebra or its finite matrix amplifications, so the nonintertwining assumption is satisfied. For a separable-predual subalgebra `B`, take the separable 2-norm subspace `B` orthogonal to the scalars. Popa's relative freeness becomes ordinary scalar freeness. Adjoining finitely many Haar unitaries retains separable predual, allowing iteration in the same ultrapower. None of this requires `B` to be amenable, `P` to have Gamma, or `P` to have a Cartan subalgebra.

For an algebra with a center, the manuscript does not apply this factor statement blindly. It first proves finite tests in almost every factor fiber and then selects the first successful tuple from a countable family of measurable unitary tuples. Openness of a finite trace-word test follows from the elementary 2-norm telescoping estimate. This addresses the center without claiming freeness over the center.

### Probability and the two ultrapowers

The walk uses a positive base component to supply dense atoms, then very rare increasingly large label families. At its stage times, each path sees a new label, label repetitions and later levels are negligible, and the finite tests were fixed before choosing those labels. The number of finite tests is enormous but finite; the proof does not need a computable time bound.

The endpoint argument uses independent variables made from disjoint halves of a path and its reversed inverse, then estimates replacement errors by martingale Cauchy bounds. It does not assert independence of `G` and `G^{-1}`. The later concatenation estimate is correctly restricted to pairwise distinct unsigned indices. Conditioning mass may shrink arbitrarily with the finite stage; the subsequence time is selected after the stage and its positive mass are fixed.

The first ultrapower turns the selected finite tests into exact Haar moments and exact first-letter identities. The second ultrapower averages an increasing number of already exact free generators. These indices have different purposes and are not interchanged. Bounded-ball 2-continuity has a uniform modulus and survives both quotients.

### Rigidity: attempted repeated-index and spectral attacks

The first-letter hypothesis alone covers distinct unsigned indices. The manuscript does not extend it directly to arbitrary polynomials. In the expansion of a product of `B_d(z)=z(z* z)^d`, each internally reduced block has positive endpoint signs and remains nonempty. Adjacent block boundaries cannot cancel. For a reduced surviving word of length `q`, noncrossing cancellation pairings give coefficient size `O_L(r^{-q/2})`. The number with a repeated surviving unsigned index is `O_q(r^{q-1})`, yielding 2-norm error `O_L(r^{-1/2})`. The homogeneous free-group length estimate upgrades this to operator norm. Repetitions that cancel completely remain in the retained coefficients, as required.

The Catalan moment computation distinguishes leading labelings with exactly `d` labels from lower-order labelings. Faithful moments transfer the free-group norm bound. Compact moment determinacy identifies the law of `s* s` and proves zero kernel; finiteness makes the polar partial isometry a unitary. Polynomial regularization followed by bounded-ball 2-continuity passes ordered block identities to every positive and negative unitary power.

Finally, bounded sine sums control `(a-b)X` while the real part grows on a short spectral arc. Right multiplication by the inverse on that arc gives a bound on `(a-b)e` without assuming that `a` or `b` commutes with the unitary. Summing squared bounds weighted by the trace of each spectral projection avoids a factor proportional to the number of arcs. This is the crucial correct distinction between an operator-norm sum and the tracial compression estimate.

The finite trace cannot be dropped from this rigidity lemma: on `ell2(Z)`, take the bilateral shift `V`, the rank-one projection `p` onto `e_0`, the projection `q` onto negative indices, and `S(X)=pXq`. Then `S(V^k)=pV^k` and `S(V^{-k})=0` for `k>=1`, so distinct multipliers exist. This is a valid boundary counterexample, not a counterexample to the manuscript's finite-trace lemma. The paper itself records it.

### Cohomology, signs, and scope removal

The normal-map 2-continuity proof genuinely uses normality when compressions converge ultraweakly. Tail supports decrease to zero by the faithful normal finite trace; selected annular supports are orthogonal. Random signs keep the input operator norm bounded while forcing the sum of output squared 2-norms to grow. This proves the required modulus without assuming positivity or complete boundedness.

For the averaged cocycle, ultraweak compactness preserves bounded multilinearity. The countable probability sum is pointwise ultraweak continuous on a fixed norm ball by truncation with a uniform tail bound. The averaging limit is stationary and retains the last-slice continuity modulus even if it is no longer normal. Liouville therefore identifies it as right multiplication in the last variable.

Expanding the original cocycle equation at a final unitary and averaging gives `dh=(-1)^k f`, hence `g=(-1)^k h`. In degree 2, `g=h`; in degree 3, `g=-h`. This check avoids an unjustified claim that the average commutes with the Hochschild differential.

To remove separability, each finite input set is placed with its finitely many cocycle outputs in a countably generated tracial subalgebra. Adding unital matrix systems of all sizes excludes every type I summand. The conditional-expectation pullback solves the cocycle equation exactly on that finite set. The cofinal subnet then gives exact equality on every tuple. Nestedness of the selected subalgebras is not needed.

To remove a global faithful scalar trace, central II1 pieces are chosen using supports of normal states on the center, and center-valued trace gives faithful scalar traces on them. The explicit central homotopy corrects mixed inputs before assembly. Its degree-k bound is `(k-1)||f||`, so the norms remain uniformly bounded across even an uncountable partition. The exceptional no-II1 piece is treated once, and its finite primitive norm creates no uncountable uniformity problem. The resulting cochain lies in `M`, not a larger representation algebra. Classical normal reduction then handles the original ordinary bounded cocycle.

## Consequences of the stronger normal estimate

For a tracial II1 algebra and a normal bounded linear map `T:M->M`, the degree-2 assertion implies

\[
 \operatorname{dist}(T,\operatorname{InnDer}(M))\leq\|dT\|.
\]

Indeed `dT` is separately normal, so choose `g` with `dg=dT` and `||g||<=||dT||`; then `T-g` is a bounded derivation and is inner. This also proves that this degree-2 primitive `g` is normal, although normality of the averaging limit was not assumed. The estimate is strong, but it is consistent with norm-one unitary averaging already available in finite-dimensional and abelian cases; no contradiction was found.

This is not a universal Banach–Mazur threshold proof. The global paper only explicitly gives a norm-one estimate at the normal tracial stage. Its unrestricted ordinary theorem uses other reductions, and neither the formal statement of vanishing nor this estimate alone supplies all quantitative constants in Roydor's stability argument. Do not infer a universal epsilon from it. Also do not extend the theorem to arbitrary coefficient bimodules or to Banach-space comparison objects beyond von Neumann algebras.

## Exact computational boundary checks

Reproduction command:

`python3 research/cohomology_adversary_checks.py`

Artifacts: `research/cohomology_adversary_checks.py` and `research/cohomology_adversary_checks.json`.

- The central identity `dJ+Jd=id-cut` was checked with exact integers for every cochain basis vector on `C direct-sum C`, with coefficient module the first central summand, in degrees 0 through 6: 5,461 scalar equations passed. This includes degree-zero and degree-one conventions and tests the identity on arbitrary cochains, not merely cocycles.
- Leading Catalan label counts were checked exactly for `d=1,...,4` and `r=1,...,4`: all 16 cases equal `Catalan(d)*(r)_d`.
- Seven ordered block products, including multiple blocks and nontrivial internal cancellations, were exhaustively reduced at three generators. Every reduced term was nonempty with positive endpoint signs.

These are falsification checks on the finite mechanisms. They are not computational evidence that alone proves infinite-dimensional Hochschild vanishing.

## Lean evidence and its limits

The real declarations inspected in `OAI/Analysis/BoundedHochschild/Main.lean` are `KadisonRingrose.bounded_primitive`, `KadisonRingrose.vanishing`, and `KadisonRingrose.normal_tracial_primitive`. They quantify ordinary `ContinuousMultilinearMap` cochains and the original self-coefficient differential. The latter has the normal tracial estimate; the first two have unrestricted algebra scope via predual data or `WStarAlgebra`.

The actual file has theorem proof terms invoking defined and proved structural inputs. For example, `ProperlyInfiniteVanishingInput` and `ClassicalVanishingInput` are proposition definitions, but `properlyInfiniteVanishingInput` is a theorem in `ProperlyInfinitePrimitives.lean`, and the global theorem does not simply assume those input propositions. A search of the BoundedHochschild family found no explicit axiom declarations or proof `sorry` tokens. That search is incomplete formal evidence: it does not audit all imports, binaries, elaboration settings, or semantic correctness of every auxiliary definition.

`ComparatorChallenges/KadisonRingrose.lean` has a `sorry` in its comparator statement. The scope document and that comparator cannot verify the input. A separate clean build and dependency/axiom check of the actual declarations remains the formal reviewer's task. No claim is made here that the Banach–Mazur consequence itself is formalized.
