# Fresh adversarial mathematical review

Audit date: 2026-08-09

Object reviewed: revised
**cyclic_bell_exact_values_and_randomness/main.tex**

Method: line-by-line proof reconstruction from the revised manuscript,
comparison with all three preserved standalone TeX sources, targeted replay
of the primary literature, and independent execution of the historical and
new hostile verifiers. The earlier merged review was treated as a baseline,
not as proof of the restored claims. Detailed subaudits are in
**RIGIDITY_RESTORATION_AUDIT.md**, **LOW_SETTING_RESTORATION_AUDIT.md**, and
**SOURCE_QC_BIBLIOGRAPHY_AUDIT.md**.

## Verdict

**Central mathematical verdict: PASS.** The sharp first-family value and its
commuting-operator extension, finite-dimensional support rigidity, the
conditional phase-permutation mechanism, biased exact maximizers for both
augmented families at every $d\geq4$, and the scalar-value randomness
obstruction are supported by analytic arguments at their stated scopes.

**Restoration verdict: PASS.** The equal-supported-multiplicity theorem,
reflection-rank lemma, coefficient normalization, source-observable
identification, exact $d=2,\ldots,6$ table, complete binary benchmark, binary
setting corollary, and private-MUB sufficient criterion have been restored and
independently reconstructed. No substantive theorem from the three source
papers remains silently omitted.

**Scope verdict: PASS.** In particular:

- support rigidity is restricted to an attained finite-dimensional tensor-
  product maximum of the first augmented family;
- binary $q=qa=qc$ value is separated from finite-dimensional tensor-product
  privacy;
- private-MUB composition is sufficient, not necessary or existential;
- value-conditioned guessing is model-indexed and only lower-bounded; and
- behavior nonuniqueness, one-input minimality, and the remaining setting
  obstructions use their precise behavior or certification hypotheses.

**Release verdict: PASS subject to final package replay.** This is a fresh
internal adversarial reconstruction, not external peer review. The revised
PDF, manifest, website assets, and live routes still require the repository's
ordinary final reproduction workflow after content freeze.

## 1. Models, normalization, and source boundary

The framework defines separate Bell and adversarial strategy classes:

- $q$: finite-dimensional tensor-product strategies;
- $qa$: closure of the corresponding finite extended correlations; and
- $qc$: vector-state realizations with Alice, Bob, and Eve algebras commuting
  pairwise across parties.

This makes $G_{\mathrm{val}}^\mu$ unambiguous. It does not assert equality of
the three guessing suprema.

The first reduced operator is

$$
\mathcal I_d
=\sum_{y=0}^{d-1}\operatorname{Re}
\bigl[(A_0+\omega^yA_1)B_y\bigr],
\qquad
\omega=e^{2\pi i/d},
$$

with sharp value

$$
M_d=2\csc\left(\frac{\pi}{2d}\right).
$$

The first augmentation has value $M_d+1$. This convention agrees with the
source operator, its reduced-value equation, and its displayed $d=3$
augmented value. The extra factor $d$ printed beside source Conjecture 2 is
correctly isolated as a normalization discrepancy and is not used
rhetorically.

The revised attribution is accurate: Perito et al. proved
$\beta_q(\mathcal I_d)\leq d\sqrt2$, supplied the all-dimensional strategy of
value $M_d$, and reported NPA agreement through $d=6$. The present paper
proves the sharper upper bound. The older bound has the same linear order but
is not asymptotically tight: its ratio to $M_d$ tends to
$\pi/(2\sqrt2)=1.110720\ldots$.

The exact benchmark table checks:

$$
\begin{array}{c|c}
d&M_d\\ \hline
2&2\sqrt2\\
3&4\\
4&2\sqrt{4+2\sqrt2}\\
5&2(1+\sqrt5)\\
6&2(\sqrt6+\sqrt2).
\end{array}
$$

## 2. Polar positive factor and the commuting model

For $C=V\lvert C\rvert$, with $V$ the canonical polar partial isometry, the
factor

$$
P_{C,B}
=\lvert C^\dagger\rvert^{1/2}-V\lvert C\rvert^{1/2}B
$$

satisfies

$$
P_{C,B}^\dagger P_{C,B}
=\lvert C^\dagger\rvert+\lvert C\rvert-CB-B^\dagger C^\dagger.
$$

The revised proof closes the earlier expository gap. If
$\mathcal M=\mathcal A''$, continuous functional calculus puts
$\lvert C\rvert$, its square root, and
$(\lvert C\rvert+\varepsilon I)^{-1}$ in $\mathcal M$, while strong closure
gives

$$
\operatorname{supp}\lvert C\rvert
=\operatorname*{s-lim}_{\varepsilon\downarrow0}
\lvert C\rvert(\lvert C\rvert+\varepsilon I)^{-1},
\qquad
V=\operatorname*{s-lim}_{\varepsilon\downarrow0}
C(\lvert C\rvert+\varepsilon I)^{-1}.
$$

Elementwise cross-party commutation is
$\mathcal B\subseteq\mathcal A'$, hence every element of
$\mathcal A''=(\mathcal A')'$, including $V$, commutes with Bob. The support
identities

$$
V^\dagger V=\operatorname{supp}\lvert C\rvert,
\qquad
\lvert C^\dagger\rvert^{1/2}V=V\lvert C\rvert^{1/2}
$$

justify the expansion with kernels present. No inverse, unitary extension of
$V$, tensor factorization, finite trace, or tracial cyclicity is used.

## 3. Scalar extremum, functional calculus, and attainment

The parity-split trigonometric calculation gives

$$
\sum_y\lvert1+\omega^yz\rvert\leq M_d
$$

with equality exactly at the $d$ distinct roots
$z^d=(-1)^{d-1}$. Endpoint and parity cases check at $d=2,3$ and for general
even and odd $d$.

Writing $U=A_0^\dagger A_1$ and
$F_d(U)=\sum_y\lvert I+\omega^yU\rvert$, functional calculus inside Alice's
von Neumann algebra gives $F_d(U)\leq M_dI$. Summing the polar factors proves
the arbitrary-$qc$ operator bound. A finite order-$d$ strategy attains it, so

$$
\beta_q(\mathcal I_d)=\beta_{qa}(\mathcal I_d)
=\beta_{qc}(\mathcal I_d)=M_d.
$$

The complete gap is correctly retained as positive polar and functional-
calculus residuals. At operator level,
$F_d(U)=M_dI$ exactly when $U^d=(-1)^{d-1}I$. On a single maximizing vector,
the gap alone gives only annihilation by each residual; the manuscript does
not infer a global polynomial relation from that fact.

The Weyl/polar attaining strategy was reconstructed. Its order-$d$ and full-
spectrum properties follow from the weighted-cycle product and characteristic
polynomial. The source coefficient DFT yields

$$
\sum_yB_y^{\mathrm{src}}=\alpha_dZ^\dagger,
\qquad
\sum_y\omega^yB_y^{\mathrm{src}}=\alpha_dX,
\qquad
\alpha_d=\csc\left(\frac{\pi}{2d}\right).
$$

Termwise polar equality fixes
$(B_y^{\mathrm{src}})^T=V_y^\dagger$. The explicit $d=3$ formula agrees with
the source. This comparison records where transpose, conjugation, and Bob
outcome inversion enter.

## 4. Finite-dimensional support rigidity

The restored theorem survives adversarial reconstruction with its stated
finite-dimensional tensor-product, first-augmented scope.

### 4.1 Residual saturation

At augmented value $M_d+1$, the reduced deficit and augmentation deficit are
nonnegative and sum to zero in expectation. Every positive square in the
global certificate therefore annihilates the purification, and

$$
(A_0B_d)\lvert\Psi\rangle=\lvert\Psi\rangle.
$$

This uses
$I-\operatorname{Re}W=(I-W)^\dagger(I-W)/2$ for unitary $W$.

### 4.2 Passage to Alice's support

For $K=\operatorname{supp}\rho_A$, finite Schmidt decomposition gives

$$
(R\otimes I)\lvert\Psi\rangle=0
\quad\Longleftrightarrow\quad
R|_K=0.
$$

This treats nonfaithful $\rho_A$ and makes no assertion on $K^\perp$. The
functional-calculus residual puts $K$ inside the spectral subspace of the
equality roots. The augmented stabilizer gives
$\rho_A=A_0\rho_AA_0^\dagger$, hence $A_0K=K$.

### 4.3 Polar kernels and invariance

The only possible kernel phase of $I+\omega^yU$ has $d$-th power $(-1)^d$,
so it is disjoint from the equality-root set, whose elements have $d$-th
power $(-1)^{d-1}$. Thus the relevant polar final projection fixes $K$.
Factoring the polar residual shows

$$
(V_yB_y)\lvert\Psi\rangle=\lvert\Psi\rangle
$$

without inverting a singular operator or extending $V_y$ globally. After
tracing, $V_yK=K$; consequently $S_y=A_0^\dagger V_y$ is unitary on $K$, and
$K$ reduces $U$.

### 4.4 Reflections and multiplicities

Adjacent half-angle phases give on $K$

$$
S_y^\dagger S_{y+1}=\eta(I-2E_{k(y)}),
$$

where $y\mapsto k(y)$ permutes all equality-root labels. Cross-party
commutation and $B_y^d=I$ give $V_y^d=I_K$; the adjacent relation gives
$(V_y(I-2E_k))^d=-I_K$.

The reflection-product lemma is correct: if $E$ has rank $r$, expansion of
$I-R_{d-1}\cdots R_0$ and rank subadditivity give $n\leq dr$. Applying it to
each spectral projection yields

$$
\dim K\leq d\,\operatorname{rank}E_k
$$

for every $k$. Since the $d$ orthogonal $E_k$ sum to $I_K$, all ranks are
exactly $\dim K/d$. Therefore every equality root occurs with equal supported
multiplicity and $d\mid\dim K$.

This is a necessary support restriction, not Weyl rigidity, uniqueness,
self-testing, or a maximizing-face classification. It is not proved for
$qa$, $qc$, approximate maximizers, the second family, or $K^\perp$.

## 5. Conditional phase-permutation mechanism

The theorem is valid under its stated sufficient hypotheses:

1. each labeled phase maximizes the scalar function;
2. the relative phases have product one; and
3. each labeled polar-phase list has product one.

The product hypotheses enforce the order-$d$ relations. Permuting complete
labeled data preserves them. Bell-visible first harmonics are symmetric sums,
while cyclic ordering remains visible to higher powers. A deliberately broken
product fails the order relation in hostile replay. The theorem does not claim
necessity or cover arbitrary phase data.

For the cyclic roots, exact polynomial products verify every hypothesis.
Weighted-shift diagonalization gives

$$
p_\kappa(a,b\mid1,d)
=\frac{\lvert\widehat q_{-(a+b)}\rvert^2}{d^3}.
$$

Parseval gives normalization and uniform marginals. For the final-two swap,

$$
R_2=(z_{d-1}-z_{d-2})(z_{d-3}-z_0),
\qquad
\lvert R_2\rvert
=4\sin(\pi/d)\sin(3\pi/d)>0
$$

for all $d\geq4$. Hence the target table is nonuniform and the displayed
guessing bound follows. No worst-case assertion is made. At $d=2,3$, this
particular permutation orbit is flat and the full question remains open.

The restored support theorem and permutation theorem are consistent: each
explicit $d$-dimensional permutation strategy has every equality root once.
Neither theorem says these exhaust all maximizers.

## 6. Second augmented family

Differentiating

$$
\sum_{k=0}^{d-1}\cot\left(x+\frac{k\pi}{d}\right)=d\cot(dx)
$$

gives

$$
\sum_{k=0}^{d-1}\csc^2\left(x+\frac{k\pi}{d}\right)
=d^2\csc^2(dx).
$$

At $x=-\pi/(2d)$, this proves
$\sum_\ell\lvert\lambda_\ell\rvert^2=1$, including every dimension-dependent
factor. With Bob Fourier orthogonality, the complete source SOS is

$$
dI-\mathcal F_d
=\frac1{2d}\sum_\ell P_\ell^\dagger P_\ell.
$$

Its expansion needs only cross-party commutation, so its values have the
stated $q,qa,qc$ reading. The geometric sum gives
$\widehat B_\ell=d\lambda_\ell D_\ell$, the parity exponent gives
$D_\ell^d=I$, and $A_\ell=\overline{D_\ell}$ annihilates every SOS factor on
$\lvert\Phi_d\rangle$. This proves global saturation rather than merely
vanishing selected candidate equations. The target $A_1$ is the same weighted
cycle as in the first family, so the target table and guessing gap are
identical.

The SOS and its value remain source results. The new claim is the permutation-
biased maximizer and its consequence.

## 7. Randomness logic and model indices

For each $\mu\in\{q,qa,qc\}$, the finite-dimensional nonuniform strategy
belongs to $\mathfrak S_\mu$. With trivial Eve,
$G\geq\max_{a,b}p(a,b)$. Therefore, for both augmented families,

$$
G_{\mathrm{val}}^\mu(d;\mathcal B)
\geq\frac1{d^2}
+\frac{2\sin(\pi/d)\sin(3\pi/d)}{d^2(d-1)}
>\frac1{d^2}.
$$

This is a common lower bound on three separately defined suprema. It does not
show that the suprema are equal or that the swap is worst.

In the displayed normalization, this finite witness directly contradicts the
first-family scalar-value implication in source Conjecture 2 for $d\geq4$.
That statement is precise: it does not determine the exact adversarial optimum
or apply to protocols conditioning on extra statistics.

The canonical uniform target table and the permuted nonuniform table attain
the same maximum. Local output relabeling only permutes table entries, so it
cannot map one to the other. The behavior-level nonuniqueness corollary is
therefore valid. It is not promoted to a classification under every strategy-
level isometry, ancilla, or transposition convention.

At $d=4$, the exact maximum target probability in the displayed realization
is $3/32$, giving

$$
-\log_2(3/32)=5-\log_2 3<4.
$$

This is an upper bound on value-only worst-case min-entropy in each model, not
the exact optimized value. The endpoint corollary is valid because it
quantifies strategies with Bell deficit at most $\varepsilon$: the zero-
deficit biased maximizer is feasible for every tolerance.

The witness changes higher Fourier correlators. It is excluded by a program
that fixes the complete canonical behavior, so the source's fixed-behavior
numerical result and $d=3$ second-family self-test are not challenged.

## 8. Low-setting benchmark and composition criterion

### 8.1 One-input certification baseline

With one Alice input, nonsignalling gives $p(a)$ independent of Bob's input.
The conditional-product hidden variable

$$
\lambda=(a,b_1,\ldots,b_m),
\qquad
\mu(\lambda)=p(a)\prod_yr_y(b_y\mid a)
$$

reproduces the entire behavior. Its coherent finite flag and grouping PVMs
give a compatible pure projective realization from which Eve guesses every
target pair. Thus such data cannot DI-force private randomness against all
compatible realizations. This is a certification statement about total test
inputs, not an intrinsic-randomness claim.

### 8.2 Binary benchmark

The exact identity

$$
\begin{aligned}
3\sqrt3I-\mathcal W_2
={}&\frac1{2\sqrt3}
\bigl(\sqrt3A_0-B_0+2B_1\bigr)^2\\
&+\frac1{\sqrt3}
\bigl(\sqrt3A_1-B_0-B_1\bigr)^2
\end{aligned}
$$

expands correctly. The Bob anticommutator terms cancel without same-party
commutation. Thus the value upper bound holds in $qc$, and the finite Pauli
strategy establishes $q=qa=qc=3\sqrt3$.

For an attaining finite-dimensional tensor-product purification, each square
annihilates the state. The derived $X_A,Z_B$ equalities, squared-unitarity, and
anticommutation relations are all explicitly on-state. The two cross-party
stabilizers force, for every Hermitian Eve test $T_E$,

$$
\langle A_0T_E\rangle
=\langle B_0T_E\rangle
=\langle A_0B_0T_E\rangle
=0.
$$

These are exactly the three nontrivial binary operator-valued Fourier
coefficients, so $\sigma_E^{ab}=\rho_E/4$, $G=1/4$, and
$H_{\min}(AB\mid E)=2$ bits. Combining this with the one-input proposition
proves componentwise $(2,2)$ minimality for the stated finite-dimensional
projective DI certification task.

The privacy conclusion is finite-dimensional tensor-product; only the value
assertion is stated in $qa,qc$. The theorem is established prior art: it is
the Wooltorton--Brown--Colbeck $\delta=\pi/6$ member after flipping Bob's
$y=1$ output. The included proof is a self-contained benchmark.

### 8.3 Private-MUB composition

For target conditional states, the $d\times d$ operator Fourier transform and
inverse carry factors $1$ and $1/d^2$, respectively. Privacy is equivalent to
the vanishing of every nonzero operator coefficient, not merely its trace.

The restored lemma assumes:

1. each reference outcome gives Eve $\rho_E/d$;
2. Bob's relabeled projector matches Alice's reference projector exactly on
   the state; and
3. $P_bR_aP_b\lvert\Psi\rangle=d^{-1}P_b\lvert\Psi\rangle$.

Testing the target state against every Hermitian $T_E$, projectivity and
cross-party commutation reduce it first to
$\langle P_bR_aP_bT_E\rangle$, then to
$d^{-1}\langle P_bT_E\rangle$, and finally to
$d^{-2}\operatorname{Tr}(T_E\rho_E)$. Hence
$\sigma_E^{a,\pi(b)}=\rho_E/d^2$.

The lemma is sufficient only. A GHZ flag, a mismatched Fourier target, and
$R=P$ respectively show that deleting any one of its three hypotheses breaks
this proof route. It does not produce a Bell functional, certify that its
hypotheses hold, or settle the $2\times3$ problem.

### 8.4 Remaining scoped observations

The ideal Fourier-table, perfect-anchor, and computational-MUB calculations
pass. The last excludes only a coefficientwise separately bounded spectral
route. None is a general $2\times3$ no-go theorem, and none is used in a
cyclic-family conclusion.

## 9. Fresh hostile and regression replay

The three revision-specific commands were rerun on 9 August 2026:

    PYTHONDONTWRITEBYTECODE=1 python3 \
      cyclic_bell_exact_values_and_randomness/verification/verify_rigidity.py
    PYTHONDONTWRITEBYTECODE=1 python3 \
      cyclic_bell_exact_values_and_randomness/verification/verify_exact_benchmarks.py
    PYTHONDONTWRITEBYTECODE=1 python3 \
      cyclic_bell_exact_values_and_randomness/verification/verify_private_mub_binary.py

Results:

- supported phase and reflection identities, $d=2,\ldots,64$: 89,439
  triples, **PASS**;
- exact-rational rank subadditivity: 840 hostile products, **PASS**;
- multiplicity/divisibility counts, $d=2,\ldots,64$ and
  $\dim K=1,\ldots,256$: 16,128 cases, **PASS**;
- exact radical values $d=2,\ldots,6$, source decimals, and $d=4$ entropy:
  **PASS**;
- cosecant-square coefficient normalization through $d=100$, including
  hostile general shifts: **PASS**;
- source/polar/Fourier observables through $d=12$: 77 Bob observables,
  including the explicit $d=3$ identity, **PASS**;
- exact binary SOS and attaining strategy over $\mathbb Q(\sqrt3)$, including
  flat binary target Fourier data: **PASS**;
- private-MUB normalization for $d=2,\ldots,12$: 1,980 checks, **PASS**; and
- three controls deleting one private-MUB hypothesis: all failed privacy as
  intended, **PASS**.

The earlier unified hostile suite and preserved historical exact replays
remain the regression base: nonunitary polar kernels, canonical, reversed,
random, prime/composite and inadmissible phase data, exhaustive $d=2,3$
permutations, final-two witnesses, independent first/second-family $d=4$
certificates, one-input rational behaviors, and scoped setting tests. The full
**reproduce.sh** workflow must be rerun after final content freeze.

None of these finite results proves an all-dimensional theorem, the $qc$
bound, finite-dimensional support rigidity, operator-valued privacy for all
strategies, or an exact guessing supremum. Those conclusions rest on the
written proofs.

## 10. Defects and feedback dispositions

1. **Formerly omitted support theorem:** restored after proof repair. The
   corrected theorem is finite-dimensional tensor-product and first-augmented
   only; no $qa/qc$ extension is claimed.
2. **Compressed polar $qc$ closure:** repaired with the bicommutant and strong-
   limit argument. The $qc$ value theorem survives.
3. **Formerly omitted private-MUB lemma:** restored as a positive sufficient
   criterion with exact conditional states and Fourier normalization; no
   existence claim survives.
4. **Abbreviated binary calibration:** restored with the exact SOS, operator-
   valued Eve proof, $G=1/4$, and setting corollary. Value and privacy model
   scopes are separated, and prior art is explicit.
5. **Ambiguous one-input wording:** repaired to DI certification or forcing
   against all compatible realizations.
6. **Ambiguous guessing model:** repaired with
   $G_{\mathrm{val}}^\mu(d;\mathcal B)$; only a lower bound is claimed.
7. **Source attribution omissions:** the proved $d\sqrt2$ source bound, NPA
   evidence through $d=6$, exact radicals, source-observable identification,
   and coefficient norm derivation are restored.
8. **Source randomness relationship:** the manuscript states plainly and
   respectfully that the normalized scalar-value implication is false for
   $d\geq4$, while preserving the full-behavior distinction.
9. **Behavior self-testing language:** narrowed to the invariant actually
   proved, namely nonuniqueness even modulo output relabelings.
10. **Endpoint robustness:** retains the correct “deficit at most
    $\varepsilon$” quantifier.
11. **Unsupported broad setting law and powers repair:** remain excluded as
    unproved or exploratory, with preserved historical records.

No load-bearing mathematical result had to be removed after reconstruction.
The remaining specialist risks are the support-level invariance and rank
chain, convention-sensitive second-family phases, and the still-open
maximizing-face, worst-case guessing, and higher-dimensional minimum-setting
problems.
