# Low-setting restoration audit

**Date:** 9 August 2026
**Verdict:** **RESTORE, WITH SCOPE AND PROOF REPAIRS**

This audit rederives the private-MUB composition lemma and the complete
binary benchmark from the historical `minimum_bell_randomness` paper.  Both
results are correct.  The reviewer recommendation is therefore substantively
sound, subject to four qualifications:

1. the private-MUB hypotheses are a **sufficient design criterion**, not an
   existence theorem and not necessary conditions;
2. the binary privacy proof must keep every equality explicitly on the tested
   state and must test all Eve operators, not only scalar moments;
3. the binary theorem is established prior art, although the short two-square
   proof is a useful self-contained replay; and
4. the one-input statement is a device-independent **certification/forcing**
   impossibility.  It does not say that a particular one-input realization
   cannot contain private randomness.

No cyclic-family theorem depends on either restoration.  Their value is to
make the measurement-resource discussion mathematically complete and to
illustrate why scalar uniformity is weaker than operator-valued privacy.

## 1. Audited sources and exact anchors

The local snapshot audited here has Git commit
`9cc4d0da42d2c2aea0f5cc5e4d7754ae0350878d`.  The line anchors below refer to
that snapshot.

| Artifact | SHA-256 / Git blob | Relevant lines |
|---|---|---|
| `minimum_bell_randomness/manuscript.tex` | SHA-256 `cd91ef2b907367b8160260b317fea91cb6a21679897b46779a250fcb4c3b7904`; blob `d197caa3672acf520213318e40d5478d073c0f2b` | framework and conditional states 101--123; one-input theorem and binary calibration 125--162; flagged proof 164--206; private-MUB lemma 916--960; binary appendix 1048--1085; bibliography 1111--1118 |
| `minimum_bell_randomness/STRUCTURAL_RESULTS.md` | blob `96f77d99da0d4659bb6f47cab668efe005cef7b6` | one-input construction 6--43; private-MUB summary 45--67; detailed binary derivation 69--157 |
| `minimum_bell_randomness/PRIOR_ART_AUDIT.md` | blob `e7a93b3f272355c17f8a1a4ba3d91bed798942ca` | Wooltorton--Brown--Colbeck comparison 6--37 |
| `minimum_bell_randomness/verify_binary_2x2.py` | historical verifier | exact formal SOS 26--110; ideal strategy and probabilities 175--246 |
| `cyclic_bell_exact_values_and_randomness/main.tex` | SHA-256 `c9cc3f75122845cb27ce879ee5b3a2289e6bd4eca524f316ae70003ca4a5dd7c`; blob `6abf6b2a9ce9b701074b0fc63be3e72d57b276f6` | current conditional-state convention 233--251; one-input proposition and abbreviated binary citation 885--934; scoped MUB obstruction 1124--1199 |
| `cyclic_bell_exact_values_and_randomness/audit/CLAIMS_LEDGER.md` | current ledger | CBR-019 and CBR-023 at lines 29 and 33; historical disposition HIST-002--003 at lines 58--59 |

The external binary comparison was checked against the primary paper:
Lewis Wooltorton, Peter Brown, and Roger Colbeck, *Tight analytic bound on
the trade-off between device-independent randomness and nonlocality*,
[arXiv:2205.00124](https://arxiv.org/abs/2205.00124),
[Phys. Rev. Lett. 129, 150403 (2022)](https://doi.org/10.1103/PhysRevLett.129.150403).
Proposition 1 gives the coefficient family, exact quantum bound, attaining
strategy, and uniqueness up to local isometries.  This audit inspected the
official arXiv source and supplement, not only its abstract.

## 2. Common model and Fourier normalization

The cleanest restoration uses the same finite-dimensional tensor-product
randomness model as the historical paper.  Let

\[
 |\Psi\rangle\in\mathcal H_A\otimes\mathcal H_B\otimes\mathcal H_E
\]

be a normalized purification.  For target (d)-outcome PVMs
\(\{R_a\}_{a\in\mathbb Z_d}\) and
\(\{Q_c\}_{c\in\mathbb Z_d}\), define

\[
 \sigma_E^{a,c}
 =\operatorname{Tr}_{AB}\!\left[
 (R_a\otimes Q_c\otimes I)|\Psi\rangle\!\langle\Psi|
 (R_a\otimes Q_c\otimes I)\right],
 \qquad
 \rho_E=\sum_{a,c}\sigma_E^{a,c}.
\]

The one-sided convention in the historical paper is equivalent: cyclicity
of the partial trace over (AB), projectivity, and commutation with Eve imply

\[
 \operatorname{Tr}_{AB}(\Pi|\Psi\rangle\!\langle\Psi|\Pi)
 =\operatorname{Tr}_{AB}(\Pi|\Psi\rangle\!\langle\Psi|)
\]

for every joint outcome projector \(\Pi=R_a\otimes Q_c\).

Set \(\omega=e^{2\pi i/d}\), with the observable convention

\[
 R^{(k)}=\sum_{a=0}^{d-1}\omega^{ka}R_a,
 \qquad
 Q^{(\ell)}=\sum_{c=0}^{d-1}\omega^{\ell c}Q_c.
\]

The **operator-valued Fourier coefficients** and their inverse are

\[
 \widehat\sigma_E(k,\ell)
 =\sum_{a,c}\omega^{ka+\ell c}\sigma_E^{a,c},
 \qquad
 \sigma_E^{a,c}
 =\frac1{d^2}\sum_{k,\ell}
 \omega^{-ka-\ell c}\widehat\sigma_E(k,\ell).
 \tag{F}
\]

For every Hermitian test operator \(T_E\),

\[
 \operatorname{Tr}\!\left[T_E\widehat\sigma_E(k,\ell)\right]
 =\langle\Psi|R^{(k)}Q^{(\ell)}T_E|\Psi\rangle.
 \tag{FT}
\]

Consequently,

\[
 \sigma_E^{a,c}=\frac{\rho_E}{d^2}\quad\forall a,c
 \quad\Longleftrightarrow\quad
 \widehat\sigma_E(0,0)=\rho_E,
 \quad
 \widehat\sigma_E(k,\ell)=0\quad\forall(k,\ell)\ne(0,0).
 \tag{P}
\]

Unlike the composition hypotheses below, (P) is necessary and sufficient.
Equation (FT) also shows why observed scalar uniformity is insufficient: it
checks only \(T_E=I\), whereas privacy requires the equality for every Eve
test operator.

## 3. Private-MUB composition lemma

### 3.1 Integration-ready statement

```tex
\begin{lemma}[Private-MUB composition; sufficient criterion]
\label{lem:private-mub}
Let $\lvert\Psi\rangle_{ABE}$ be a finite-dimensional purification.
Alice has two $d$-outcome PVMs $P=\{P_b\}_{b\in\mathbb Z_d}$ and
$R=\{R_a\}_{a\in\mathbb Z_d}$, and Bob has a $d$-outcome PVM
$Q=\{Q_c\}_{c\in\mathbb Z_d}$.  Let $\pi$ be a permutation of
$\mathbb Z_d$, and put
\[
 \tau_E^b=\operatorname{Tr}_{AB}
 [(P_b\otimes\Id)\lvert\Psi\rangle\!\langle\Psi\rvert
  (P_b\otimes\Id)].
\]
Suppose that, for every $a,b$,
\begin{align*}
 \tau_E^b&=\rho_E/d, &(i)\\
 (\Id\otimes Q_{\pi(b)}\otimes\Id)\lvert\Psi\rangle
   &=(P_b\otimes\Id)\lvert\Psi\rangle, &(ii)\\
 (P_bR_aP_b\otimes\Id)\lvert\Psi\rangle
   &=d^{-1}(P_b\otimes\Id)\lvert\Psi\rangle. &(iii)
\end{align*}
Then, for the target input pair $(R,Q)$,
\[
 \sigma_E^{a,\pi(b)}=\rho_E/d^2
 \qquad\text{for every }a,b.
\]
Thus the target outputs are uniform and private from Eve.  Conditions
$(i)$--$(iii)$ are sufficient; no necessity assertion is made.
\end{lemma}
```

Here (P) and (R) are two Alice inputs and (Q) is the designated Bob
input.  A larger Bell test may be needed to certify the three hypotheses.
The lemma therefore does **not** establish a (2\times1), (2\times2), or
(2\times3) construction by itself.

### 3.2 Integration-ready proof

```tex
\begin{proof}
Fix $a,b$ and a Hermitian operator $T_E$.  Suppressing identity factors,
projectivity, cross-party commutation, and commutation with $T_E$ give
\begin{align*}
 \operatorname{Tr}(T_E\sigma_E^{a,\pi(b)})
 &=\langle\Psi|R_aQ_{\pi(b)}T_EQ_{\pi(b)}R_a|\Psi\rangle\\
 &=\langle\Psi|P_bR_aT_ER_aP_b|\Psi\rangle\\
 &=\langle\Psi|P_bR_aP_bT_E|\Psi\rangle.
\end{align*}
The second line uses hypothesis~$(ii)$ on both the ket and the bra.  The
last line uses $R_a^2=R_a$ and the fact that $T_E$ commutes with all
Alice and Bob operators.  Hypotheses~$(iii)$ and~$(i)$ now imply
\[
 \operatorname{Tr}(T_E\sigma_E^{a,\pi(b)})
 =\frac1d\langle\Psi|P_bT_E|\Psi\rangle
 =\frac1{d^2}\operatorname{Tr}(T_E\rho_E).
\]
Since this holds for every Hermitian $T_E$, the corresponding trace-class
operators are equal.  The permutation $\pi$ exhausts Bob's output labels,
which proves the claim.
\end{proof}
```

This proof also implies the Fourier cancellation in (P), with exactly the
(1/d^2) inverse normalization shown in (F).

### 3.3 Hostile checks and scope

Each hypothesis is load-bearing for this proof route:

* If (i) is deleted, the GHZ-type state
  \(d^{-1/2}\sum_b|b\rangle_A|b\rangle_B|b\rangle_E\), with computational
  (P,Q) and Fourier (R), satisfies (ii)--(iii).  Its observed target table
  is uniform, but Eve knows Bob's output.
* If (ii) is deleted, a maximally entangled state with Fourier-conjugate
  (R,Q) has perfectly correlated target outcomes despite (i) and (iii).
* If (iii) is deleted, take (R=P) on a maximally entangled state and match
  (Q) to (P); the target outcomes are perfectly correlated.

These examples do not say that (i)--(iii) are individually necessary for
privacy.  They show only that none can be silently removed from this
sufficient composition argument.

## 4. Complete binary benchmark

### 4.1 Integration-ready theorem

```tex
\begin{theorem}[Binary two-input benchmark]
\label{thm:binary-benchmark}
Let $A_0,A_1$ and $B_0,B_1$ be binary projective observables, so that they
are Hermitian unitaries, and assume cross-party commutation.  Define
\[
 \mathcal W_2=A_0B_0-2A_0B_1+2A_1B_0+2A_1B_1.
\]
Its finite-dimensional tensor-product, approximate, and commuting-operator
values are all $3\sqrt3$.  Moreover, every finite-dimensional
tensor-product strategy attaining $3\sqrt3$, with arbitrary purifying Eve,
satisfies at the target pair $(x,y)=(0,0)$
\[
 \sigma_E^{ab}=\rho_E/4\qquad(a,b\in\mathbb Z_2).
\]
Hence $G(AB\mid0,0,E)=1/4$ and
$H_{\min}(AB\mid E)=2$ bits.
\end{theorem}
```

The value assertion extends to (qc) because its proof is an operator SOS
using only cross-party commutation.  The privacy assertion above is stated
only in the finite-dimensional tensor-product/purification model actually
proved here.  It should not be silently promoted to a (qc) adversarial
formalism without defining that formalism and replaying the last step there.

### 4.2 Exact SOS and equality relations

Tensor identities are suppressed in the following displayed identity, but
all Alice letters commute with all Bob letters:

\[
\begin{aligned}
3\sqrt3 I-\mathcal W_2
={}&\frac1{2\sqrt3}
 \bigl(\sqrt3A_0-B_0+2B_1\bigr)^2\\
&+\frac1{\sqrt3}
 \bigl(\sqrt3A_1-B_0-B_1\bigr)^2.
\tag{SOS}
\end{aligned}
\]

Expanding (SOS) uses only
\(A_x^2=B_y^2=I\).  The two Bob cross terms are
\(-\{B_0,B_1\}/\sqrt3\) and
\(+\{B_0,B_1\}/\sqrt3\), so they cancel without any same-party
commutation assumption.  This proves the upper bound in the commuting model.

If a purified strategy saturates the bound, positivity of both squares gives

\[
 (B_0-2B_1)|\Psi\rangle=\sqrt3A_0|\Psi\rangle,
 \qquad
 (B_0+B_1)|\Psi\rangle=\sqrt3A_1|\Psi\rangle.
\tag{E}
\]

Define the Hermitian operators

\[
 X_A=\frac{A_0+2A_1}{\sqrt3},
 \qquad
 Z_B=\frac{B_0-2B_1}{\sqrt3}.
\]

Solving (E), and keeping the state dependence explicit, yields

\[
 B_0|\Psi\rangle=X_A|\Psi\rangle,
 \qquad
 Z_B|\Psi\rangle=A_0|\Psi\rangle.
\tag{S1}
\]

Cross-party commutation and unitarity then give

\[
 X_A^2|\Psi\rangle=Z_B^2|\Psi\rangle=|\Psi\rangle.
\tag{S2}
\]

The exact operator identities

\[
 \{A_0,X_A\}=\sqrt3(X_A^2-I),
 \qquad
 \{Z_B,B_0\}=\sqrt3(Z_B^2-I)
\]

therefore imply the **state-supported**, not global, relations

\[
 \{A_0,X_A\}|\Psi\rangle=0,
 \qquad
 \{Z_B,B_0\}|\Psi\rangle=0.
\tag{S3}
\]

This repairs the historical appendix's compressed wording at lines
1074--1079: (B_0=X_A), (Z_B=A_0), and the anticommutators must all be
read as relations on \(|\Psi\rangle\).

### 4.3 Operator-valued privacy proof

Let

\[
 S_A=X_AB_0,
 \qquad
 S_B=A_0Z_B.
\]

These are Hermitian, and (S1)--(S2) give
\(S_A|\Psi\rangle=S_B|\Psi\rangle=|\Psi\rangle\).
For every Hermitian (T_E), (S3) implies

\[
\begin{aligned}
 \langle A_0T_E\rangle
 &=\langle S_AA_0T_E\rangle
 =\langle X_AA_0B_0T_E\rangle\\
 &=-\langle A_0X_AB_0T_E\rangle
 =-\langle A_0T_E\rangle,
\end{aligned}
\]

and similarly

\[
 \langle B_0T_E\rangle
 =\langle S_BB_0T_E\rangle
 =-\langle B_0T_ES_B\rangle
 =-\langle B_0T_E\rangle.
\]

Thus both local operator-valued moments vanish.  For the joint moment, (S1)
gives

\[
 \langle A_0B_0T_E\rangle=\langle A_0X_AT_E\rangle.
\]

The left side is real because (A_0,B_0,T_E) are mutually commuting
Hermitian operators.  The complex conjugate of the right side is

\[
 \langle X_AA_0T_E\rangle=-\langle A_0X_AT_E\rangle
\]

by (S3), so the right side is purely imaginary.  Hence

\[
 \langle A_0T_E\rangle=
 \langle B_0T_E\rangle=
 \langle A_0B_0T_E\rangle=0
 \quad\text{for every Hermitian }T_E.
\tag{BFT}
\]

With binary output convention

\[
 M_a^0=\frac{I+(-1)^aA_0}{2},
 \qquad
 N_b^0=\frac{I+(-1)^bB_0}{2},
\]

the exact binary Fourier inversion is

\[
\begin{aligned}
 \operatorname{Tr}(T_E\sigma_E^{ab})
 =\frac14\bigl(&\operatorname{Tr}(T_E\rho_E)
 +(-1)^a\langle A_0T_E\rangle
 +(-1)^b\langle B_0T_E\rangle\\
 &+(-1)^{a+b}\langle A_0B_0T_E\rangle\bigr).
\end{aligned}
\]

Equation (BFT), for every Hermitian (T_E), proves
\(\sigma_E^{ab}=\rho_E/4\).  Eve's success for any POVM
\(\{F_{ab}\}\) is therefore

\[
 \sum_{a,b}\operatorname{Tr}(F_{ab}\sigma_E^{ab})
 =\frac14\operatorname{Tr}\!\left[(\sum_{a,b}F_{ab})\rho_E\right]
 =\frac14,
\]

which gives exactly two conditional min-entropy bits.

### 4.4 Exact attaining strategy

On \(|\Phi_2\rangle=(|00\rangle+|11\rangle)/\sqrt2\), take

\[
 A_0=Z,
 \quad A_1=-\frac12Z+\frac{\sqrt3}{2}X,
 \quad B_0=X,
 \quad B_1=-\frac{\sqrt3}{2}Z+\frac12X.
\]

All four observables square to (I).  Using
\(\langle\Phi_2|C\otimes D|\Phi_2\rangle
=\tfrac12\operatorname{Tr}(C^{\mathsf T}D)\) gives

\[
 \langle A_0B_0\rangle=0,
 \quad
 \langle A_0B_1\rangle=-\frac{\sqrt3}{2},
 \quad
 \langle A_1B_0\rangle=\frac{\sqrt3}{2},
 \quad
 \langle A_1B_1\rangle=\frac{\sqrt3}{2}.
\]

Thus \(\langle\mathcal W_2\rangle=3\sqrt3\), proving attainability and
hence (q=qa=qc=3\sqrt3\).  The target observables (Z) and (X) are
mutually unbiased, so all four target probabilities are (1/4).

## 5. Precise one-input/two-input minimality

The current merged statement at `main.tex` lines 893--897 is mathematically
supported by its proof, but “necessary for any private global randomness” can
be misread as an assertion about intrinsic randomness of a selected physical
realization.  The logically exact conclusion is about what the observed data
can force over **all compatible realizations**.

### Integration-ready statement

```tex
\begin{proposition}[One-input certification baseline]
If either party has only one input, every finite-output nonsignalling
behavior is local.  Moreover, it has a compatible finite-dimensional pure
projective realization in which Eve guesses both outputs perfectly at every
input pair.  Therefore neither a Bell score nor even the complete behavior in
such a scenario can device-independently force positive private global
randomness against all compatible realizations.
\end{proposition}

\begin{corollary}[Binary setting minimality]
In the finite-dimensional projective device-independent model considered
here, two binary inputs per party are sufficient to certify two private
global output bits: saturation of $\mathcal W_2$ does so at $(0,0)$.  One
input on either wing is insufficient to force any private global randomness
against all compatible realizations.  Thus $(2,2)$ is componentwise minimal
for the binary maximal-global-randomness certification task.
\end{corollary}
```

For completeness, if Alice has one input, nonsignalling gives
\(p(a)=\sum_bp(a,b|y)\), independent of (y).  Set

\[
 r_y(b|a)=\frac{p(a,b|y)}{p(a)},
 \qquad
 \mu(a,b_1,\ldots,b_m)=p(a)\prod_y r_y(b_y|a),
\]

with arbitrary (r_y) on zero-probability branches.  This is a deterministic
local model after adjoining the stored response tuple.  Its coherent flagged
realization

\[
 \sum_\lambda\sqrt{\mu(\lambda)}
 |\lambda\rangle_A|\lambda\rangle_B|\lambda\rangle_E
\]

with grouping PVMs reproduces the complete behavior and lets Eve read every
output.  The symmetric case is identical.  This proof is independent of the
number of outcomes and is a standard locality fact, not a novelty claim.

This corollary concerns the **total test-input alphabets**.  It does not
exclude a larger test having one designated generation input per party.

## 6. Prior-art boundary

At \(\delta=\pi/6\), Proposition 1 of Wooltorton--Brown--Colbeck has

\[
 I_{\pi/6}
 =A_0B_0+2A_0B_1+2A_1B_0-2A_1B_1,
 \qquad
 I_{\pi/6}^{Q}=3\sqrt3.
\]

The output flip (B_1\mapsto-B_1) gives exactly \(\mathcal W_2\), while
leaving the target pair ((A_0,B_0)) unchanged.  Their target strategy also
maps exactly to the one in Section 4.4.  Their result establishes uniqueness
up to local isometries and two global random bits.  Accordingly:

* the binary value, maximal-private-randomness theorem, and (2\times2)
  sufficiency are **ESTABLISHED PRIOR ART**;
* the restored two-square/Fourier derivation should be described as a
  self-contained verification, not a novelty claim;
* “the \(\delta=\pi/6\) member of the Wooltorton--Brown--Colbeck family,
  after flipping Bob's (y=1) output” is more precise than the current
  phrase “a known tilted Bell score”; and
* the private-MUB lemma is an elementary sufficient design lemma retained
  from the historical manuscript.  No standalone priority claim should be
  made for it or for the Fourier inversion criterion.

The value paper's (qc) language and this binary prior-art statement should
also be kept distinct: the operator SOS immediately supplies the binary (qc)
value, but Wooltorton--Brown--Colbeck's randomness theorem is framed in the
usual tensor-product DI setting.

## 7. Independent verifier and results

New verifier:

```text
cyclic_bell_exact_values_and_randomness/verification/verify_private_mub_binary.py
```

Command:

```bash
python3 cyclic_bell_exact_values_and_randomness/verification/verify_private_mub_binary.py
```

Result on 9 August 2026:

```text
PASS: binary SOS coefficients cancel exactly over Q(sqrt(3)).
PASS: exact binary strategy attains 3*sqrt(3) and has flat target Fourier data.
PASS: private-MUB normalization checked in d=2,...,12 (1980 checks).
PASS: deleting each composition hypothesis triggered a hostile control.
```

The verifier uses only the Python standard library.  It independently checks
the noncommutative SOS over \(\mathbb Q(\sqrt3)\), the exact ideal strategy,
the binary (1/4) inverse Fourier normalization, the (1/d) MUB sandwich and
(1/d^2) table through (d=12), permutations of the matching basis, and the
three hostile controls in Section 3.3.  These tests support but do not replace
the analytic proofs above.

## 8. Final audit disposition

| Requested restoration | Disposition | Necessary repair |
|---|---|---|
| Private-MUB composition | **RESTORE** | Define subnormalized Eve states; give both Fourier transforms; say sufficient, not necessary; do not imply existence of a low-setting Bell functional |
| Exact (3\sqrt3) SOS | **RESTORE** | Show the Bob anticommutator cancellation and state that the operator value is (q=qa=qc) |
| Three binary Fourier coefficients | **RESTORE** | Qualify all auxiliary equalities as on-state and prove vanishing against every Hermitian (T_E) |
| Two private bits | **RESTORE** | Derive \(\sigma_E^{ab}=\rho_E/4\), (G=1/4), and (H_{\min}=2\), not merely uniform scalar probabilities |
| (d=2) setting minimality | **RESTORE, NARROWLY** | Say “DI certify/force against all compatible realizations”; specify finite-dimensional projective model and total test inputs |
| Novelty language | **DO NOT CLAIM NOVELTY** | Credit Wooltorton--Brown--Colbeck precisely; call the short proof an independent replay |

The two mathematical restorations pass this adversarial audit.  The main
remaining editorial risk is scope drift: neither the MUB lemma nor the narrow
computational-MUB obstruction solves the open higher-dimensional minimum-
setting problem.
