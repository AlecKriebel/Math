# Proof dependency map

Audit date: 2026-08-09

This map separates analytic dependencies from regression artifacts. A script
can catch a normalization, phase, support, or indexing error; it does not
establish an all-dimensional, closure-model, or commuting-operator theorem.

## A. Exact value and first augmentation

The dependency chain is:

1. CBR-004 proves the scalar extremum and its exact equality roots.
2. Continuous functional calculus applies that result to
   $U=A_0^\dagger A_1$ and gives $F_d(U)\leq M_dI$.
3. CBR-003 supplies the polar positive-factor identity. Its commuting-model
   proof uses:

   - continuous functional calculus for $\lvert C\rvert$ and its bounded
     regularizations in $\mathcal A''$;
   - strong limits for $\operatorname{supp}\lvert C\rvert$ and the canonical
     partial isometry $V$;
   - $\mathcal B\subseteq\mathcal A'$, hence
     $\mathcal A''=(\mathcal A')'$ commutes with Bob; and
   - the canonical polar support identities, with kernels retained.

4. Summing CBR-003 with the functional-calculus bound proves the arbitrary-
   Hilbert-space inequality $\mathcal I_d\leq M_dI$ in CBR-005.
5. CBR-008 supplies a finite order-$d$ attaining strategy. Therefore

   $$
   \beta_q(\mathcal I_d)=\beta_{qa}(\mathcal I_d)
   =\beta_{qc}(\mathcal I_d)=M_d.
   $$

6. The inequality $\operatorname{Re}(A_0B_d)\leq I$ and aligned finite
   attainment give CBR-007, the augmented value $M_d+1$ in all three models.

The $qc$ conclusion is analytic. In particular,

$$
V=\operatorname*{s-lim}_{\varepsilon\downarrow0}
C(\lvert C\rvert+\varepsilon I)^{-1}
$$

places the polar partial isometry in $\mathcal A''$. No tensor decomposition,
finite-dimensional trace, or tracial state is used. Finite direct sums are
regression cases only.

The equality layers must remain distinct:

1. CBR-004 classifies scalar equality roots.
2. Spectral calculus gives
   $F_d(U)=M_dI$ exactly when $U^d=(-1)^{d-1}I$ as an operator statement.
3. CBR-006 gives only residual annihilation on an individual maximizing
   vector.
4. CBR-025 upgrades those vector relations only for an attained finite-
   dimensional tensor-product maximum of the first augmented family.

## B. Finite-dimensional support rigidity

CBR-025 depends on the following chain:

1. CBR-006 and equality in $\operatorname{Re}(A_0B_d)\leq I$ force every
   positive residual and the augmented stabilizer to annihilate
   $\lvert\Psi\rangle$ separately.
2. Finite Schmidt decomposition across $A:(BE)$ gives

   $$
   (R\otimes I)\lvert\Psi\rangle=0
   \quad\Longleftrightarrow\quad
   R|_K=0,
   \qquad K=\operatorname{supp}\rho_A.
   $$

3. The functional-calculus residual puts $K$ inside the scalar equality-root
   spectral subspace.
4. The augmented stabilizer gives
   $\rho_A=A_0\rho_AA_0^\dagger$, hence $A_0K=K$.
5. The possible polar-kernel phase is disjoint from the equality-root set.
   Kernel-safe cancellation of each polar residual then yields
   $(V_yB_y)\lvert\Psi\rangle=\lvert\Psi\rangle$ without an inverse or a
   global unitary extension.
6. Tracing the stabilizer gives $V_yK=K$. Thus
   $S_y=A_0^\dagger V_y$ is unitary on $K$, and $K$ reduces $U$.
7. Adjacent half-angle phases give

   $$
   S_y^\dagger S_{y+1}=\eta(I-2E_{k(y)})
   \quad\text{on }K,
   $$

   where $y\mapsto k(y)$ permutes the equality-root labels.
8. The supported stabilizers imply
   $V_y^d=I_K$ and
   $(V_y(I-2E_k))^d=-I_K$.
9. CBR-026 then gives
   $\dim K\leq d\,\operatorname{rank}E_k$ for every root projection.
10. The orthogonal $E_k$ sum to $I_K$, forcing
    $\operatorname{rank}E_k=\dim K/d$ for every $k$.

This proof is finite-dimensional because it uses finite Schmidt support,
finite ranks, and a dimension count. It is a necessary condition on exact
tensor-product maximizers of the first augmentation. It is not a $qa$ or
$qc$ equality theorem, an approximate theorem, a second-family theorem, or a
classification of $K^\perp$ or the maximizing face.

## C. Conditional phase permutations and first-family bias

CBR-009 depends on:

- CBR-003;
- maximizing scalar labels $z_j$;
- $\prod_jz_j=1$;
- exact polar phases $s_{rj}$ with $\prod_js_{rj}=1$;
- the weighted-cycle identity; and
- the maximally-entangled trace identity.

The cyclic root products in CBR-010 specialize this sufficient theorem. The
weighted-shift diagonalization then proves CBR-011. For the final-two swap,
the exact lag-two autocorrelation is nonzero, so CBR-012 follows.

CBR-009 is sufficient, not necessary. Its product hypotheses enforce the
order-$d$ relations. Its explicit orbit is compatible with CBR-025 because
the constructed support is $\mathbb C^d$ with each equality root once. Neither
result claims that this orbit exhausts the maximizing face.

## D. Second augmented family

The second-family chain is:

1. Differentiating the cotangent sum gives the cosecant-square identity.
2. Specializing at $x=-\pi/(2d)$ proves CBR-027:
   $\sum_\ell\lvert\lambda_\ell\rvert^2=1$.
3. Bob Fourier orthogonality and cross-party commutation give the complete
   source SOS in CBR-014:

   $$
   dI-\mathcal F_d=\frac1{2d}\sum_\ell P_\ell^\dagger P_\ell.
   $$

4. The exact geometric sum
   $S_\ell=d\lambda_\ell r_\ell$, weighted-cycle parity, and
   $A_\ell=\overline{D_\ell}$ prove CBR-015 and finite attainment.
5. The source SOS then gives values $d$ and $d+1$ in $q,qa,qc$.
6. The displayed $A_1$ is the first-family weighted cycle, so CBR-011/012 give
   the same nonuniform target table and guessing gap.

Global optimality comes from the complete source SOS. Killing selected
candidate residuals would not prove an upper bound. The present contribution
is the permutation-biased maximizer and its randomness consequence, not the
source SOS or its value.

## E. Model-indexed randomness consequences

CBR-001 defines $\mathfrak S_q,\mathfrak S_{qa},\mathfrak S_{qc}$. The finite
nonuniform maximizers from CBR-012 and CBR-015 embed in all three classes, and
trivial Eve gives $G\geq\max_{a,b}p(a,b)$. Therefore CBR-016 supplies the same
explicit lower bound for each separately defined
$G_{\mathrm{val}}^\mu(d;\mathcal B)$.

From there:

- CBR-017 states the exact scalar-value refutation and full-behavior boundary.
- The zero-deficit witness is feasible for every deficit tolerance, giving
  CBR-018.
- The canonical uniform and permuted nonuniform target tables cannot be
  related by output relabeling, giving CBR-028.

No dependency identifies the three model-indexed guessing suprema or turns
the explicit lower bound into their exact value. CBR-028 is behavior-level
only; no complete strategy-level self-test formalism is invoked.

## F. Low-setting certification and design criteria

### One-input and binary benchmark

The one-input chain is:

1. Nonsignalling plus one Alice input gives a conditional-product local model.
2. A coherent finite flag and grouped PVMs give a compatible realization with
   perfect Eve guessing.
3. This proves CBR-019.

The binary chain is:

1. The two-square SOS proves the commuting-operator upper value
   $3\sqrt3$.
2. A finite Pauli strategy attains it, giving the value in $q,qa,qc$.
3. At finite-dimensional tensor-product equality, the SOS gives on-state
   stabilizers and anticommutation.
4. These make all three nontrivial binary operator-valued Fourier
   coefficients vanish for every Hermitian Eve test.
5. Fourier inversion gives $\sigma_E^{ab}=\rho_E/4$, proving CBR-023.
6. CBR-019 and CBR-023 together prove CBR-029.

The value part of CBR-023 is a commuting-operator theorem; its privacy part is
proved only for attaining finite-dimensional tensor-product strategies with
purifying Eve. CBR-029 concerns DI certification against all compatible
realizations and total test-input alphabets.

### Private-MUB composition

The positive design route uses:

- the operator-valued $d\times d$ Fourier transform and its $1/d^2$ inverse;
- private reference states $\tau_E^b=\rho_E/d$;
- exact state-level Alice/Bob projector matching; and
- the state-supported MUB sandwich
  $P_bR_aP_b\lvert\Psi\rangle=P_b\lvert\Psi\rangle/d$.

Testing against every Hermitian Eve operator proves
$\sigma_E^{a,\pi(b)}=\rho_E/d^2$, which is CBR-030. This is sufficient only.
It neither proves that a Bell score enforces the hypotheses nor establishes a
$2\times3$ construction.

### Scoped negative observations

- The specified Fourier-phase ideal tables give CBR-020.
- The specified perfect anchor gives CBR-021.
- The two-circulant operator system, corner block, and paired singular-value
  spectrum give CBR-022.

CBR-020--022 do not combine into a general $(2,3,d,d)$ no-go theorem.

## G. Analytic proof versus computational evidence

| Claim group | What proves it | What tests contribute |
|---|---|---|
| CBR-003--008 | Polar algebra, scalar trigonometry, bicommutant functional calculus, explicit Weyl strategy and source DFT | Genuine nonunitary polar case; radicals; source/polar observables through $d=12$ |
| CBR-025--026 | Support cancellation, invariance, kernel-safe polar cancellation, adjacent reflections, finite-rank inequality | 89,439 phase/reflection triples, 840 exact-rational hostile products, 16,128 dimension counts |
| CBR-009--012 | Product identities, weighted cycles, trace identity, Fourier analysis | Canonical, reversed, random, prime, composite, and deliberately inadmissible cases |
| CBR-013--015 and CBR-027 | Cyclotomic arithmetic, complete SOS, cosecant identity, exact geometric sum | Two independent $d=4$ routes; normalization through $d=100$ |
| CBR-016--018 and CBR-028 | Explicit finite witness plus definitions and behavior logic | Exact $d=4$ entropy identity and target tables |
| CBR-019, CBR-023, CBR-029--030 | Explicit local model; binary SOS/Fourier proof; projector/test-operator composition proof | 15 rational local reconstructions; exact $\mathbb Q(\sqrt3)$ binary replay; 1,980 MUB checks and three hostile controls |
| CBR-020--022 | Exact overlap and linear-algebra arguments | Formula and nullspace regressions through finite $d$ |

No finite test is cited as establishing $qc$, support rigidity, an all-
dimensional identity, the exact scalar equality set, an exact guessing
supremum, or a complete maximizing-face classification.
