# Claims ledger

Audit date: 2026-08-09

This ledger is keyed to the revised **main.tex**. PROVED means that the
displayed analytic argument was reconstructed in the fresh adversarial audit;
it does not mean that a finite regression test proves the claim. COMPUTATION
CHECKED is supporting evidence only. Priority classifications belong to
**PRIORITY_AUDIT.md** and are not implied by the mathematical status here.

## Main analytic claims

| ID | Manuscript result | Precise audited claim | Status | Proof dependency | Computational artifact and boundary |
|---|---|---|---|---|---|
| CBR-001 | Framework and model-indexed definitions | The finite-dimensional tensor-product model $q$, its extended-correlation closure $qa$, and the pairwise-commuting three-party model $qc$ are distinguished both for Bell values and adversarial guessing. A scalar value, full behavior, maximizing face, observed uniformity, and operator-valued privacy are different constraints. | PROVED / DEFINITIONAL | Definitions of $\mathfrak S_q,\mathfrak S_{qa},\mathfrak S_{qc}$; $G\geq\max_{a,b}p(a,b)$. | The definitions do not assert equality of the three guessing suprema. |
| CBR-002 | Normalization remark and source-claim paragraph | For the displayed $\mathcal I_d$, the reduced and first-augmented values are $M_d=2\csc(\pi/(2d))$ and $M_d+1$. The isolated extra factor $d$ printed beside source Conjecture 2 is not used. In the operator normalization, the construction refutes its scalar-value implication for $d\geq4$. | SOURCE-CHECKED / PROVED CONSEQUENCE | Source operator, source Eq. (17), displayed $d=3$ augmented value, CBR-012, CBR-016. | Convention checks cannot replace source comparison. |
| CBR-003 | Lemma **lem:polar** | For commuting unital star-algebras, $C=V\lvert C\rvert$, and unitary $B$, the positive-factor identity holds with $P=\lvert C^\dagger\rvert^{1/2}-V\lvert C\rvert^{1/2}B$. The canonical partial isometry handles kernels. The displayed strong limit puts it in $\mathcal A''$, so it commutes with Bob because $\mathcal B\subseteq\mathcal A'$. | PROVED | Polar support identities; continuous functional calculus; strong closure for the support and $V$; bicommutant commutation. | **verify_merged.py** includes a genuinely nonunitary partial-isometry case. Finite matrices do not prove the arbitrary-Hilbert-space result. |
| CBR-004 | Lemma **lem:scalar** | For $\lvert z\rvert=1$, $\sum_y\lvert1+\omega^yz\rvert\leq M_d$, with equality exactly at the $d$ distinct roots $z^d=(-1)^{d-1}$. | PROVED | Parity-split trigonometric sum in Appendix **app:scalar**. | Exact-root and off-root tests are regression evidence only. |
| CBR-005 | Theorem **thm:exact** | For arbitrary unitaries on an arbitrary Hilbert space with only cross-party commutation, $\mathcal I_d\leq M_dI$. A finite order-$d$ strategy attains the bound, hence $\beta_q=\beta_{qa}=\beta_{qc}=M_d$ for every $d\geq2$. | PROVED | CBR-003, CBR-004, commuting-algebra functional calculus, CBR-008. | The $qc$ claim is analytic; finite direct sums do not sample nonspatial representations. |
| CBR-006 | Equation **eq:global-certificate** | The exact gap is the displayed sum of polar and functional-calculus squares. Operator equality $F_d(U)=M_dI$ is equivalent to $U^d=(-1)^{d-1}I$. On one maximizing vector, only the displayed residual annihilations follow without further support arguments. | PROVED, NARROWLY STATED | CBR-003, CBR-004, spectral mapping. | No maximizing-face classification follows from the vector equations. |
| CBR-007 | Corollary **cor:first-augmented** | The first augmentation satisfies $\beta_q=\beta_{qa}=\beta_{qc}=M_d+1$. | PROVED | CBR-005, $\operatorname{Re}(A_0B_d)\leq I$, CBR-008. | Sampled attainment supplements the algebraic proof. |
| CBR-008 | Appendix **app:attainment** and Table **tab:exact-values** | The Weyl/polar strategy has valid order-$d$, full-spectrum observables and attains $M_d$; its aligned augmentation attains $M_d+1$. It equals the source strategy under the stated transpose/conjugation convention. The exact $d=2,\ldots,6$ radicals and source numerical comparisons are correct. | PROVED / SOURCE-CHECKED | Weighted-cycle order, scalar equality roots, maximally-entangled trace identity, source coefficient DFT. | **verify_exact_benchmarks.py** checks five radicals and 77 source/polar Bob observables through $d=12$, including the qutrit formula. |
| CBR-009 | Theorem **thm:permutation** | Under the maximizing-phase, product-one, and polar-phase product-one hypotheses, every label permutation gives full-spectrum order-$d$ observables, attains $M+1$, and preserves the listed first-harmonic correlators and local first moments. | PROVED AS A SUFFICIENT THEOREM | CBR-003; weighted-cycle identity; characteristic polynomial; maximally-entangled trace identity. | The theorem is neither necessary nor a maximizing-face classification. |
| CBR-010 | Equations **eq:equality-roots** through **eq:visible-correlators** | The first-family roots and polar phases meet CBR-009's hypotheses, so every root ordering is an admissible exact maximizer with permutation-independent Bell-visible first harmonics. | PROVED | CBR-004, exact product identities, CBR-009. | Historical exact and family verifiers. |
| CBR-011 | Equation **eq:target-table** | For target $(A_1,B_d)$, $p_\kappa(a,b\mid1,d)=\lvert\widehat q_{-(a+b)}\rvert^2/d^3$; both marginals are uniform, and the joint table is uniform exactly when every squared Fourier magnitude equals $d$. | PROVED | Weighted-shift diagonalization and Parseval. | Historical exact verifier and exact $d=4$ projector replay. |
| CBR-012 | Theorem **thm:biased** | For every $d\geq4$, the final-two swap exactly maximizes the first augmented family, has uniform marginals and a nonuniform target table, and with trivial Eve obeys the strict bound in **eq:guessing-gap**. | PROVED | CBR-010, CBR-011, lag-two autocorrelation, mean-zero Fourier estimate. | Prime/composite tests through $d=20$ are regression evidence. |
| CBR-013 | Appendix **app:d4** | For both augmented families at $d=4$, the exact cyclotomic strategy gives probabilities $1/32$ and $3/32$, $G=3/32$, and displayed-realization min-entropy $5-\log_2 3<4$. | PROVED AND EXACTLY REPLAYED | CBR-011, CBR-015, exact $\mathbb Q(\zeta_{16})$ arithmetic. | Two independent exact implementations. This is not the exact optimized DI entropy. |
| CBR-014 | Equation **eq:second-sos** and adjacent value statement | The source second-family SOS is correctly normalized: $dI-\mathcal F_d=(2d)^{-1}\sum_\ell P_\ell^\dagger P_\ell$. It uses only cross-party commutation, giving values $d$ and $d+1$ in $q,qa,qc$ once CBR-015 supplies finite attainment. | PROVED / ESTABLISHED PRIOR ART | CBR-027, Bob Fourier orthogonality, cross-party commutation, CBR-015. | Exact $d=4$ expansion is a coefficient check, not an all-dimensional proof. |
| CBR-015 | Theorem **thm:second** | For every permutation, the displayed $D_\ell,A_\ell$ are order-$d$, obey $\widehat B_\ell=d\lambda_\ell D_\ell$, annihilate every source SOS factor, and attain $d+1$. The final-two swap has the same target table and guessing gap for $d\geq4$, and its first harmonics are permutation-independent. | PROVED | Exact geometric sums, weighted-cycle parity, CBR-014, maximally-entangled identity, CBR-011/012. | Independent exact $d=4$ SOS and broader finite regressions. |
| CBR-016 | Equations **eq:gval-model** through **eq:value-conditioned** | For each $\mu\in\{q,qa,qc\}$ and either augmented family, the finite counterexample embeds in $\mathfrak S_\mu$, so $G_{\mathrm{val}}^\mu$ is at least the CBR-012 bound. This is a lower bound on a model-indexed supremum, not its exact value. | PROVED | CBR-001, CBR-012, CBR-015, inclusion of the finite realization. | Trivial Eve witnesses the lower bound but is not claimed worst-case. |
| CBR-017 | Randomness-interpretation section | The counterexample directly defeats the displayed first-family scalar-value implication for $d\geq4$. It does not contradict a full-canonical-behavior calculation or show that the canonical strategy lacks maximal randomness. | PROVED LOGICAL SCOPE | CBR-001, CBR-002, CBR-011/012. | Full-behavior numerical results remain attributed to the source. |
| CBR-018 | Unlabeled endpoint-robustness corollary | No bound tending to $1/d^2$ can hold uniformly for every strategy whose deficit is at most $\varepsilon$, using only that deficit. | PROVED WITH TOLERANCE QUANTIFIER | CBR-016 and the zero-deficit biased strategy. | The claim would not follow under an exact-deficit-only interpretation. |
| CBR-019 | Proposition **prop:one-input** | If either party has one input, every finite-output nonsignalling behavior is local and has a compatible finite-dimensional pure projective flagged realization in which Eve guesses perfectly. Thus neither a score nor the full behavior can DI-force private randomness against all compatible realizations. | PROVED | Conditional-product hidden variable and coherent flag purification. | **verify_merged.py** gives 15 exact-rational reconstructions. This is a certification claim, not an intrinsic-randomness claim. |
| CBR-020 | Appendix **app:settings**, equation **eq:standard-tables** | For the specified Fourier-phase qudit realization, each ideal table has $p_{\max}=1/[2d^3\sin^2(\pi/(4d))]>1/d^2$ and the stated asymptotic min-entropy. | PROVED, SCOPED | Exact geometric overlap. | **satwap_ideal_audit.py**; not a theorem about all equivalent realizations beyond the listed symmetries. |
| CBR-021 | Appendix **app:settings**, perfect-anchor paragraph | The specified perfect third-setting anchor leaves a cross table with $p_{\max}=1/[d^3\sin^2(\pi/(2d))]>1/d^2$ for $d\geq3$, with $d=2$ the MUB exception. | PROVED, SCOPED | Direct Fourier overlap. | Not a general third-setting no-go theorem. |
| CBR-022 | Proposition **prop:mub** | In the stated real operator system, a computational eigenvector of a nonscalar $K$ cannot be extremal. Therefore the displayed coefficientwise separately bounded term cannot nontrivially expose the computational PVM on $\lvert\Phi_d\rangle$. | PROVED, NARROWLY STATED | Circulant decomposition, corner-block form, paired singular-value spectrum. | Nullspace regressions through $d=20$; no claim about joint SOS bounds, other MUBs, or all $(2,3,d,d)$ functionals. |
| CBR-023 | Theorem **thm:binary-benchmark** | The binary operator has value $3\sqrt3$ in $q,qa,qc$. Every attaining finite-dimensional tensor-product strategy with purifying Eve satisfies $\sigma_E^{ab}=\rho_E/4$, hence $G=1/4$ and two private bits at $(0,0)$. | PROVED / ESTABLISHED PRIOR ART | Exact two-square SOS; on-state stabilizers and anticommutation; three operator-valued binary Fourier zeros; finite attainment. | **verify_private_mub_binary.py** checks the SOS and strategy exactly over $\mathbb Q(\sqrt3)$. Privacy is not asserted for arbitrary $qa/qc$ adversarial realizations. |
| CBR-024 | Open-scope statements | The permutation family is Fourier-flat for $d=2,3$; complete maximizing faces, exact model-indexed guessing suprema, and higher-dimensional minimum settings remain unresolved. | VERIFIED AS A LIMIT, NOT A THEOREM | Exhaustive small-permutation replay plus absence of classification or optimization arguments. | Failure to find a witness is not evidence of rigidity. |
| CBR-025 | Theorem **thm:support-rigidity** | Every attained finite-dimensional tensor-product exact maximizer of the first augmented family has $K=\operatorname{supp}\rho_A$ reducing $U=A_0^\dagger A_1$; every equality root occurs in $U|_K$ with equal multiplicity, so $d\mid\dim K$. | PROVED, MODEL- AND FAMILY-SCOPED | CBR-006, augmented stabilizer, Schmidt-support cancellation, kernel-safe polar cancellation, CBR-026. | **verify_rigidity.py** checks phase/reflection identities through $d=64$ and multiplicity counts. No $qa/qc$, approximate, second-family, or $K^\perp$ claim. |
| CBR-026 | Lemma **lem:reflection-rank** | If a unitary $V$ on an $n$-dimensional space and a rank-$r$ projection $E$ obey $V^d=I$ and $(V(I-2E))^d=-I$, then $n\leq dr$. | PROVED | Rank subadditivity for $I-\prod_jR_j$ and unitary conjugates of $I-2E$. | **verify_rigidity.py** performs 840 exact-rational hostile products. |
| CBR-027 | Lemma **lem:lambda-normalization** | The second-family coefficients obey $\sum_\ell\lvert\lambda_\ell\rvert^2=1$, by differentiating the cotangent sum and specializing the resulting cosecant-square identity. | PROVED | $\sum_k\csc^2(x+k\pi/d)=d^2\csc^2(dx)$ at $x=-\pi/(2d)$. | **verify_exact_benchmarks.py** checks through $d=100$ and hostile general shifts. |
| CBR-028 | Corollary **cor:behavior-nonunique** | For either augmented family and every $d\geq4$, the scalar maximum does not determine a unique behavior even modulo local output relabelings: relabelings cannot map a uniform target table to a nonuniform one. | PROVED, BEHAVIOR-LEVEL ONLY | Canonical uniform table, CBR-012/015 nonuniform table, invariance of uniformity under permutations. | No full strategy-level equivalence classification is claimed. |
| CBR-029 | Corollary **cor:binary-minimality** | In the finite-dimensional projective DI model, two binary inputs per party suffice to certify two private bits, while one input on either wing cannot force private randomness against all compatible realizations. Thus $(2,2)$ is componentwise minimal for this task. | PROVED / ESTABLISHED PRIOR ART PLUS STANDARD BASELINE | CBR-019 and CBR-023. | The claim concerns total test-input alphabets, not one generation input in a larger test. |
| CBR-030 | Lemma **lem:private-mub** | A private reference PVM, exact state-level matching to Bob, and the state-supported MUB sandwich imply $\sigma_E^{a,\pi(b)}=\rho_E/d^2$. The criterion is sufficient only and does not construct a Bell functional or establish a low-setting regime. | PROVED, SUFFICIENT ONLY | Projectivity, cross-party commutation, arbitrary Hermitian Eve tests, operator-valued Fourier inversion. | **verify_private_mub_binary.py** checks $d=2,\ldots,12$ and three hostile controls deleting one hypothesis. |

## Mapping of every named result in main.tex

| Named environment | Claim ID |
|---|---|
| Sharp commuting-operator value, **thm:exact** | CBR-005 |
| Polar positive-factor identity, **lem:polar** | CBR-003 |
| Roots-of-unity extremum, **lem:scalar** | CBR-004 |
| First augmented family, **cor:first-augmented** | CBR-007 |
| Equal supported multiplicities, **thm:support-rigidity** | CBR-025 |
| Conditional phase-permutation theorem, **thm:permutation** | CBR-009 |
| Biased exact maximizers, **thm:biased** | CBR-012 |
| Coefficient normalization, **lem:lambda-normalization** | CBR-027 |
| Permutation maximizers of the second family, **thm:second** | CBR-015 |
| Behavior-level nonuniqueness, **cor:behavior-nonunique** | CBR-028 |
| No value-only endpoint robustness, unlabeled corollary | CBR-018 |
| One-input certification baseline, **prop:one-input** | CBR-019 |
| Binary two-input benchmark, **thm:binary-benchmark** | CBR-023 |
| Binary setting minimality, **cor:binary-minimality** | CBR-029 |
| Private-MUB composition, **lem:private-mub** | CBR-030 |
| Reflection-product rank bound, **lem:reflection-rank** | CBR-026 |
| Computational-MUB exposure obstruction, **prop:mub** | CBR-022 |

All seventeen named theorem-like environments in the revised manuscript are
mapped exactly once.

## Historical-result disposition after revision

| Historical statement | Current disposition |
|---|---|
| Equal supported multiplicities and $d\mid\dim K$ | Restored as CBR-025 with CBR-026; finite-dimensional tensor-product first-augmented scope is explicit. |
| Private-MUB composition lemma | Restored as CBR-030, expressly sufficient and nonexistential. |
| Binary two-input SOS/global-randomness theorem | Restored as CBR-023 and CBR-029, with prior art and finite-dimensional privacy scope explicit. |
| Source coefficient normalization and exact $d=2,\ldots,6$ table | Restored as CBR-027 and CBR-008. |
| Numerically disfavored powers-based repair | Preserved as a failed approach, not promoted to a theorem. |
| All-dimensional minimum-setting claim | Not established; narrowed to the proved baseline, benchmark, scoped obstructions, sufficient design lemma, and explicitly open regimes. |

## Ledger verdict

Every named result and every restored substantive theorem from the three
standalone manuscripts is represented. The ledger does not certify a complete
maximizing-face classification, a $qa/qc$ support-rigidity theorem, an exact
value-only guessing optimum, a $qa/qc$ binary privacy theorem, a necessary
private-MUB criterion, or a general low-setting no-go theorem.
