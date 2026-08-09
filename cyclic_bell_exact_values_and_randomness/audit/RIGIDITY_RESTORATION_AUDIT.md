# Finite-dimensional support-rigidity restoration audit

Audit date: 2026-08-09
Audited repository snapshot: `9cc4d0da42d2c2aea0f5cc5e4d7754ae0350878d`
Historical source blob: `711f5496f42375e9e0c28b6482d075a4ed76f368`
Merged-manuscript blob before restoration: `6abf6b2a9ce9b701074b0fc63be3e72d57b276f6`

## Verdict

**PASS, with two scope corrections.** The substance of historical Lemma A.1
and Proposition A.2 is valid and should be restored. For every
finite-dimensional **tensor-product** exact maximizer of the first augmented
family, the support (K=\operatorname{supp}\rho_A) reduces the relative
unitary

\[
U=A_0^\dagger A_1,
\]

and every root of (z^d=(-1)^{d-1}) occurs in
\(\operatorname{spec}(U|_K)\) with the same multiplicity. Consequently
\(d\mid\dim K\).

The corrections are:

1. (U=A_0^\dagger A_1) is the **relative unitary**, not a polar unitary.
   The polar partial isometries in the proof are the (V_y).
2. The proof uses a tensor-product purification, Alice's reduced state, a
   partial trace, and the Schmidt-support cancellation lemma. It therefore
   does **not** establish a (qa) or (qc) equality theorem. The sharp value
   remains (q=qa=qc), but the restored rigidity statement is only about an
   attained finite-dimensional tensor-product maximum.

This is a necessary condition, not a classification, uniqueness theorem, Weyl
representation theorem, or self-test. It makes no claim on unused sectors in
\(K^\perp\).

## Exact source anchors

The historical results called Lemma A.1 and Proposition A.2 in the rendered
paper are located in
`cyclic_randomness_counterexample/manuscript.tex` as follows:

| Item | Stable TeX label | Source lines at the audited blob | Role |
|---|---|---:|---|
| First-family definitions and normalization | `eq:I`, `eq:Ibar`, `eq:Md` | 96--123 | Fixes the operator and (M_d+1) maximum. |
| Polar factor and scalar equality set | `lem:polar`, `lem:scalar` | 239--324 | Supplies the kernel-safe polar factor and the roots (z^d=(-1)^{d-1}). |
| Exact positive gap | `eq:gap` | 326--351 | Makes every equality residual positive. |
| Reflection-product rank bound (Lemma A.1) | `lem:reflection` | 726--756 | Converts two (d)-th-power relations into (\dim K\le d\operatorname{rank}E). |
| Equal supported multiplicities (Proposition A.2) | `prop:multiplicity` | 758--772 | States the result. |
| Equality residuals and support cancellation | `eq:Py0`--`eq:support` | 774--802 | Passes from exact saturation to (K\subseteq L) and (A_0K=K). |
| Kernel-safe polar cancellation | `eq:Vstab` | 803--835 | Establishes ((V_y\otimes B_y)\lvert\Psi\rangle=\lvert\Psi\rangle). |
| Invariance and adjacent phases | `eq:adjacent` | 836--887 | Makes (K) reducing for (U) and identifies one reflected root projection per (y). |
| Rank count and limitations | proof end and following remark | 888--908 | Forces equal ranks; explicitly excludes classification and restricts to the augmented family. |

The current merged notation occurs in
`cyclic_bell_exact_values_and_randomness/main.tex` at the audited blob:

| Merged item | Stable label | Lines before restoration |
|---|---|---:|
| (d)-outcome/order-(d) measurement convention and (q,qa,qc) models | none | 200--220 |
| Sharp value theorem | `thm:exact` | 284--298 |
| Kernel-safe polar factor | `lem:polar` | 303--335 |
| Exact equality roots | `lem:scalar`, `eq:scalar-equality` | 340--352 |
| Global equality certificate and vector-level conclusion | `eq:global-certificate` | 390--417 |
| First augmented maximum | `cor:first-augmented` | 419--438 |
| Conditional phase-permutation theorem and nonclassification warning | `thm:permutation` | 440--554 |
| Existing maximizing-face open problem | discussion list | 936--960 |

The natural visible insertion point is after `cor:first-augmented` and before
the conditional permutation theorem. The technical proof can be a separate
appendix following the scalar-extremum appendix.

## Notation crosswalk

| Historical source | Merged notation | Meaning |
|---|---|---|
| (C_y=A_0+\omega^yA_1) | (L_y=A_0+\omega^yA_1) | Alice linear form |
| (U=A_0^\dagger A_1) | same | relative unitary |
| (F_d(U)=\sum_y|I+\omega^yU|) | same | scalar-functional-calculus sum |
| (C_y=V_y|C_y|) | (L_y=V_y|L_y|) | canonical polar decomposition; (V_y) may be partial |
| (P_y) | (P_y=P_{L_y,B_y}) | positive-factor residual |
| (M_dI-F_d(U)) | (G^\dagger G), (G=(M_dI-F_d(U))^{1/2}) | scalar-equality residual |
| (L=\operatorname{ran}\mathbf1_{\mathcal Z_d}(U)) | same proposed notation | equality-phase spectral subspace |
| (E_y^{\rm bad}) | same proposed notation | projection at the unique possible kernel phase (-\omega^{-y}) |
| (S_y=A_0^\dagger V_y) | same proposed notation | polar phase as a function of (U) on (L) |

The no-adjoint Bell convention in the merged manuscript is compatible with
the historical proof. Under the globally adjointed Bob convention, replace
each (B_y) by (B_y^\dagger); the support argument and order-(d) relation
are unchanged.

## Independent proof audit

### 1. Saturation of the positive residuals

For the first augmented operator,

\[
\overline{\mathcal I}_d=\mathcal I_d+\operatorname{Re}(A_0\otimes B_d),
\]

combine `eq:global-certificate` with

\[
I-\operatorname{Re}(A_0\otimes B_d)
=\tfrac12(I-A_0\otimes B_d)^\dagger(I-A_0\otimes B_d).
\]

Every summand in the augmented gap is positive. If a unit vector
\(\lvert\Psi\rangle_{ABE}\) has expectation (M_d+1), the sum of their
nonnegative expectations is zero, hence each square annihilates the vector:

\[
P_y\lvert\Psi\rangle=0,\qquad
G\lvert\Psi\rangle=0,\qquad
GA_0^\dagger\lvert\Psi\rangle=0,\qquad
(I-A_0\otimes B_d\otimes I_E)\lvert\Psi\rangle=0.
\]

There is no cancellation between residuals. This also works for a mixed
finite-dimensional strategy after adjoining a purifying (E).

### 2. Vector relations versus the support of (\rho_A)

Let

\[
\rho_A=\operatorname{Tr}_{BE}|\Psi\rangle\!\langle\Psi|,
\qquad K=\operatorname{supp}\rho_A.
\]

For every Alice operator (R), a Schmidt decomposition across (A:(BE))
gives

\[
(R\otimes I)|\Psi\rangle=0
\quad\Longleftrightarrow\quad R|_K=0.
\]

Equivalently, the squared norm is
\(\operatorname{Tr}(\rho_A R^\dagger R)\), whose vanishing says that (R)
vanishes on the range of (\rho_A^{1/2}), namely (K). This explicitly
handles a nonfaithful (\rho_A); nothing is inferred on (K^\perp).

Since (G) is a continuous function of the unitary (U), the equality set in
`lem:scalar` implies

\[
K\subseteq L:=\operatorname{ran}\mathbf1_{\mathcal Z_d}(U),
\qquad
\mathcal Z_d=\{z\in\mathbb T:z^d=(-1)^{d-1}\}.
\]

The added stabilizer gives
\(\rho_A=A_0\rho_AA_0^\dagger\), hence (A_0K=K).

### 3. Kernel-safe cancellation of the polar residual

Write

\[
L_y=A_0(I+\omega^yU)=V_y|L_y|,
\qquad
E_y^{\rm bad}=\mathbf1_{\{-\omega^{-y}\}}(U).
\]

The initial and final support projections of (V_y) are

\[
V_y^\dagger V_y=I-E_y^{\rm bad},
\qquad
F_y:=V_yV_y^\dagger=A_0(I-E_y^{\rm bad})A_0^\dagger.
\]

The bad phase cannot be an equality phase because

\[
(-\omega^{-y})^d=(-1)^d\ne(-1)^{d-1}.
\]

Thus (E_y^{\rm bad}K=0). Together with (A_0K=K), this gives
\(F_y|_K=I_K). Polar functional calculus factors the residual as

\[
P_y=|L_y^\dagger|^{1/2}(I-V_y\otimes B_y).
\]

Set
\(q_y=(I-V_y\otimes B_y\otimes I_E)|\Psi\rangle\). The first term in
\(q_y\) lies in (\operatorname{ran}F_y\otimes\mathcal H_{BE}) because
\(F_y|_K=I_K); the second does because (F_yV_y=V_y). Hence (F_yq_y=q_y).
But (P_y|\Psi\rangle=0) places (q_y) in
\(\ker|L_y^\dagger|^{1/2}=\ker F_y\). Therefore (q_y=0), i.e.

\[
(V_y\otimes B_y\otimes I_E)|\Psi\rangle=|\Psi\rangle.
\]

No inverse of (L_y), no globally unitary extension of (V_y), and no
assumption about its action on (K^\perp) is used.

### 4. Invariance, reduction, and polar phases on (K)

Because (K\subseteq\ker(E_y^{\rm bad})), (V_y) is an isometry on (K).
Tracing the last stabilizer over (BE) yields

\[
\rho_A=V_y\rho_AV_y^\dagger.
\]

Its supports give (V_yK=K). Thus (V_y|_K) is unitary, and
\(S_y=A_0^\dagger V_y\) is unitary on (K). On (L), the canonical polar
calculus gives

\[
S_y=s_y(U),\qquad
s_y(z)=\frac{1+\omega^yz}{|1+\omega^yz|},\qquad
s_y(z)^2=\omega^yz.
\]

Consequently (U|_K=\omega^{-y}(S_y|_K)^2), so (UK=K). Since (U) is
unitary and (K) is finite-dimensional, (K) is reducing for (U). The
spectral projections (E_k) of (U|_K) are therefore well defined. This is
the step that justifies speaking about multiplicities on (K), rather than
merely vector-level equality phases.

### 5. Adjacent phase and reflection-product identities

Set

\[
\delta_d=\begin{cases}0&d\text{ odd},\\1&d\text{ even},\end{cases}
\quad
z_k=\exp\!\left(\frac{\pi i(2k+\delta_d)}d\right),
\quad
\eta=e^{\pi i/d},
\quad
r_*=\left\lfloor\frac{d-1}{2}\right\rfloor.
\]

Writing (s_y(z_k)=(1+\omega^yz_k)/|1+\omega^yz_k|), direct half-angle
division gives, with all indices modulo (d),

\[
\overline{s_y(z_k)}s_{y+1}(z_k)
=\begin{cases}
-\eta,&[k+y]_d=r_*,\\
\eta,&[k+y]_d\ne r_*.
\end{cases}
\]

Let (k(y)=[r_*-y]_d). The map (y\mapsto k(y)) is a bijection, and

\[
S_y^\dagger S_{y+1}=\eta(I-2E_{k(y)}),
\qquad
V_{y+1}=\eta V_y(I-2E_{k(y)})
\quad\text{on }K.
\]

The verifier described below independently checks the parity split, wraparound
at (y=d-1), and exceptional label for all (2\le d\le64).

The stabilizer and (B_y^d=I) give

\[
(V_y^d-I)\otimes I\,|\Psi\rangle=0,
\]

so (V_y^d=I_K) by support cancellation. Since (\eta^d=-1), the adjacent
identity and (V_{y+1}^d=I_K) imply

\[
\bigl(V_y(I-2E_{k(y)})\bigr)^d=-I_K.
\]

### 6. Reflection rank and equal multiplicities

The historical reflection lemma is correct. If (T^d=I),
\((T(I-2E))^d=-I), and (r=\operatorname{rank}E) on an (n)-dimensional
space, then

\[
(T(I-2E))^d
=T^dR_{d-1}\cdots R_0,
\qquad
R_j=T^{-j}(I-2E)T^j.
\]

Each (I-R_j) has rank (r), while repeated use of
\(I-AB=(I-A)+A(I-B)\) gives

\[
n=\operatorname{rank}(2I)
=\operatorname{rank}(I-R_{d-1}\cdots R_0)
\le\sum_{j=0}^{d-1}\operatorname{rank}(I-R_j)=dr.
\]

Apply this with (T=V_y|_K) and (E=E_{k(y)}). If
\(n=\dim K\) and (r_k=\operatorname{rank}E_k), bijectivity of (k(y))
gives (n\le dr_k) for every (k). Since the (E_k) are mutually
orthogonal and sum to (I_K),

\[
n=\sum_kr_k\ge\sum_k\frac nd=n.
\]

Every inequality is therefore equality: (r_k=n/d) for every (k). In
particular every equality root occurs, all multiplicities agree, and
\(d\mid n\).

## Ready-to-integrate theorem statement

The following formulation matches the merged notation and avoids all
unsupported model extensions.

```tex
\begin{proposition}[Finite-dimensional support rigidity]
\label{prop:support-rigidity}
Let a finite-dimensional tensor-product strategy with order-$d$ observable
unitaries and state $\rho_{AB}$ attain
\[
  \langle\overline{\cI}_d\rangle=M_d+1.
\]
Let $\lvert\Psi\rangle_{ABE}$ be a purification, and put
\[
  \rho_A=\Tr_{BE}\lvert\Psi\rangle\!\langle\Psi\rvert,
  \qquad K=\supp\rho_A,
  \qquad U=A_0^\dagger A_1.
\]
Then $K$ reduces $U$, and every root of
$z^d=(-1)^{d-1}$ is an eigenvalue of $U|_K$ with the same multiplicity.
Consequently
\[
  d\mid\dim K.
\]
No conclusion is asserted on $K^\perp$, for approximate maximizers, or for
general commuting-operator realizations.
\end{proposition}
```

A concise main-text lead-in replacing the last sentence after
`eq:global-certificate` is:

> These vector-level equality relations do not provide a global
> classification or constrain sectors outside the state support. For an
> attained finite-dimensional tensor-product maximum of the first augmented
> family, however, the added (A_0)-(B_d) stabilizer upgrades them to the
> following support-level spectral restriction.

The proof can be integrated almost verbatim from the six audited steps above.
For readability, first state the reflection-product rank lemma in the proof
appendix, then prove the proposition. The main text should immediately add:

> Equal supported multiplicities are necessary but do not imply a Weyl
> representation, uniqueness, or self-testing; the permutation maximizers
> remain compatible with this restriction.

## Required open-problem correction

The complete maximizing face remains open, but it is no longer accurate to
say that only vector-level relations are known for arbitrary finite-dimensional
first-family maximizers. A sharper discussion item is:

> Determine whether the support-level rigidity conditions, admissible phase
> permutations, direct sums, and irrelevant ancillary systems generate all
> finite-dimensional tensor-product exact maximizers of the first augmented
> family, and separately characterize the (qa) and (qc) maximizing faces.

The existing questions about the exact worst-case guessing probability and
the (d=2,3) maximizing faces remain unchanged. Notice that the divisibility
theorem applies in (d=2,3); it does not settle their full maximizing faces or
randomness.

## Regression artifact

`verification/verify_rigidity.py` is dependency-free and deterministic. It
checks:

- the equality-root polynomial and exclusion of every polar-kernel bad phase;
- (s_y(z_k)^2=\omega^yz_k);
- every adjacent half-angle phase, including parity and cyclic wraparound;
- the bijection (y\mapsto k(y));
- the weighted-cycle and one-reflection (d)-th-power identities;
- the rank subadditivity used in Lemma A.1 using exact rational arithmetic;
- and the final multiplicity/divisibility count, including hostile unequal
  rank vectors.

Audit run:

```text
PASS: supported phase and reflection identities d=2..64 (89439 triples)
PASS: exact-rational rank subadditivity (840 hostile products)
PASS: multiplicity/divisibility count d=2..64, dim K=1..256 (16128 cases)
PASS: support-level rigidity regression suite
```

These finite tests are regression evidence only. The theorem rests on the
analytic support, polar, invariance, and rank argument above.

## Final scope matrix

| Proposed conclusion | Audit status |
|---|---|
| Exact finite-dimensional tensor-product maximizer of the **first augmented** family has equal root multiplicities on (K) | **PROVED** |
| (d\mid\dim K) | **PROVED** |
| (K) reduces (U=A_0^\dagger A_1) | **PROVED** |
| Relation on (K^\perp) | **NOT CLAIMED** |
| Same result for the unaugmented first operator | **NOT PROVED**; the proof uses the added stabilizer |
| Same result for the second augmented family | **NOT PROVED BY THIS ARGUMENT** |
| Same result for arbitrary (qa) or (qc) maximizers | **NOT PROVED** |
| Classification of all exact maximizers | **OPEN** |
| Weyl structure, uniqueness, or self-testing | **DOES NOT FOLLOW** |
