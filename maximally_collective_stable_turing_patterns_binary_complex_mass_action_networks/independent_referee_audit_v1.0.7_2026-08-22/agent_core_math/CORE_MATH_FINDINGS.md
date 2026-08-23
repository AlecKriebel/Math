# Independent referee findings: algebraic and linear core

## Bottom line

**Verdict on the assigned algebraic/linear core: independently verified.** I found no fatal, major, or minor mathematical defect in the indexed topology, realization-space description, all-spectrum principal-block theorem, principal-minor diffusion-ray theorem, omission-minor table, stationary diffusion law, or contrast/heterogeneity optimization claims. Their quantifiers, strict inequalities, exceptional dimensions, and stated scope are correct.

This is not a verdict on the whole manuscript. I independently verified the linear-algebraic portions of the selected unit and equilibrium-scaled families, but the cubic coefficient, center-manifold/Fredholm argument, branch stability, and robustness theorem were outside this sub-audit and must be combined with the other referee work.

The author-supplied programs provide useful exact regressions, but several central `PASS` programs are finite-dimensional and compare against hard-coded claimed formulas. They do **not** prove the all-dimensional theorems. The manuscript's deductive graph, sparse-determinant, principal-minor, and scalar-optimization arguments are what close those all-dimensional bridges; I reconstructed those arguments independently.

## Scope, sources, and evidence classes

I read the main manuscript and supplement completely:

- `repository/manuscript/main.tex`, lines 1–1217;
- `repository/manuscript/supplement.tex`, lines 1–971.

The relevant primary locations are main lines 145–253 (network and realizations), 255–359 (all-spectrum theorem), 374–425 (general diffusion-ray theorem), 436–593 (omission minors, diffusion law, and sharp contrast), 595–772 (unit-family algebra and nonlinear proof architecture), and 774–1006 (equilibrium-scaled family). Supplement Sections S1–S5 and S7–S8 give the corresponding details at lines 31–289, 467–778, and 779–859.

My exact reconstruction is in `independent_core_checks.py`; its machine-readable result is `independent_core_checks_output.json`. It imports no packet/project module, generated table, stored certificate, or expected output. Evidence below is labeled as:

- **deductive**: an all-dimensional proof from the displayed definitions;
- **exact finite**: rational/symbolic checks in specified dimensions;
- **numerical falsification**: floating-point counterexample search, never used as proof;
- **citation-conditional**: a historical/comparative assertion depending on a cited source.

## Independently reconstructed dependency map

| Result | Actual dependencies | Classification in this sub-audit |
|---|---|---|
| Proposition 2.1, semipositive conservation and flux cone | Indexed reaction vectors; balance equations; rank-nullity | **Independently verified (deductive + exact finite)** |
| Proposition 2.2, complete realization family | Proposition 2.1; mass-action derivative identity `J=Gamma diag(v)Y^T H`; inverse rate construction | **Independently verified (deductive)** |
| Lemma 3.1, SCC exhaustion | Nonzero-entry graph of `A_m(a,b)`; path forcing along the one-way chain; separate `m=3`; deletion at `b=2a` | **Independently verified (deductive + finite exhaustive corroboration)** |
| Theorem 3.2, maximum all-spectrum localization | Lemma 3.1; two long-cycle modulus inequalities; boundary-triad Routh–Hurwitz; signed determinant of the full `X` block | **Independently verified (deductive + exact finite)** |
| Corollary 3.3 | Theorem 3.2; cited general-matrix endpoint result; later stable-pattern construction | **Construction verified; historical comparison citation-conditional; nonlinear clause not checked here** |
| Theorem 4.1, principal-minor diffusion ray | Multilinear principal-minor expansion; coefficient positivity; monotonicity in `s` and in nonnegative real `lambda` | **Independently verified (deductive)** |
| Proposition 5.1, omission-minor table | Sparse `X`-chain determinant; boundary-triad determinant; two explicit nullvectors; positive column scaling by `H` | **Independently verified (deductive + exact finite)** |
| Theorem 5.2, exact stationary diffusion law | Theorems 3.2 and 4.1; Proposition 5.1; homogeneous relative stability giving a simple conservation zero and positive order-`m` sum | **Independently verified under its stated `(a,b,H) in S_m` hypothesis** |
| Theorem 5.3, sharp contrast/trade-off | Theorem 5.2; equal-damping coefficient; elementary extrema; one stable unit realization for sharpness | **Independently verified** |
| Theorem 6.1, items 1–3 and linear part of the bounds | Unit determinant factorization; 35/77-term modulus certificates; exact critical right/left vectors and derivative | **Independently verified algebraically** |
| Theorem 6.1, cubic sign and nonlinear stable branches | Harmonic corrections; cubic certificate; semilinear theory | **Not checked in this sub-audit** |
| Theorem 7.1, linear onset, interval, physical contrasts, within-family optimum, asymptotics | Row scaling; 22/84-term certificates; transformed adjoint; exact extrema of `H(L)` and `Dphys(L)`; Theorem 5.3 | **Independently verified algebraically** |
| Theorem 7.1, scaled cubic sign and nonlinear stable branches | Gauge correction and cubic bounds; semilinear exchange of stability | **Not checked in this sub-audit** |
| Proposition 8.1, retuned robustness | Smooth spectral continuation and nonlinear reduction | **Not checked in this sub-audit** |

## Detailed mathematical findings

### 1. Indexed topology, rank, flux cone, conservation, and Jacobian family

The reaction list is at main lines 168–179. Rebuilding each source and target vector gives, with species ordered `X1,...,Xm,Z`,

- `R0`: reaction vector `e1`;
- `Ri`: `e_{i+1}-e_i`, `2 <= i <= m-2`;
- `Ra`: `-e1-e_{m-1}+2e_m`;
- `Rb`: `e2-2e_m`;
- `R+`: `e1+e_m-2e_Z`;
- `R-`: `-e1-e_m+2e_Z`.

Every source and product has molecularity at most two, including the empty chain at `m=3`. The `Z` balance gives `v_+=v_-`; the `X1` balance then gives `v_0=v_a`; the `X2` and successive chain balances give `v_b=v_2=...=v_a` (with the direct `v_b=v_a` balance at `m=3`). Thus

`ker Gamma = span{(1_m,0,0),(0_m,1,1)}`.

The vector `c=(0,4,...,4,2,1)^T` annihilates every reaction vector. Since the displayed two kernel vectors are independent and the balance equations leave no third freedom, `rank Gamma=m`; hence `im Gamma=c^perp`. This verifies main Proposition 2.1 at lines 191–220 and supplement S1 at lines 31–63. The law is semipositive, not positive, because its `X1` coordinate is zero, exactly as disclosed.

Direct multiplication `Gamma diag(a 1_m,b,b)Y^T` reproduces every entry of `A_m(a,b)` at main lines 230–237, including the index-collision case `m=3`. The standard mass-action differentiation identity at main lines 157–166 then gives `J=A_m(a,b)H`. Conversely, for arbitrary `a,b>0` and positive diagonal `H`, choosing `x*=H^{-1}1` and `k_r=v_r/(x*)^{y_r}` realizes the triple. Proposition 2.2 (main lines 239–253) is therefore complete; there is no hidden realizability condition.

Exact independent checks for `m=3,4,5,6` are implemented at `independent_core_checks.py` lines 23–203 and recorded in the output under `reaction_rank_flux_and_omissions`.

### 2. SCC exhaustion and every smaller principal block

The directed graph convention and theorem are at main lines 260–359 and supplement lines 65–108. Positive column scaling by `H` does not change the graph. For `m>=4`, the only interior arrows are the forward chain

`X2 -> X3 -> ... -> X_{m-1}`.

Any SCC using an interior edge must return either through `X_{m-1}->X1`, which forces all of `X1,...,X_{m-1}`, or through `Xm->X2`, which forces all of `X2,...,Xm`. The remaining chain closure uses all `m` `X` vertices and is excluded when the retained set has size below `m`. Without a complete long cycle, every feedback component is contained in `{X1,Xm,Z}` and all retained chain vertices outside it are singleton blocks. This is a complete path argument, not an extrapolation from sampled dimensions.

For `m=3`, the chain is empty and the only non-singleton cases of order below three are the two long-cycle pairs `{X1,X2}`, `{X2,X3}` and principal pairs in `{X1,X3,Z}`. I enumerated them directly. At `b=2a`, the sole vanishing edge is `X1->Xm`. It belongs to neither long cycle; deleting it can only split a boundary-triad SCC into another boundary-triad principal subgraph. Thus the edge-deletion case is valid. The manuscript's short phrase “can only split components” at main lines 273–274 is correct here because of that additional observation.

The two long-cycle characteristic equations have diagonal products strictly larger than their cycle products:

- `(a+b)a^{m-2} prod h_i > a^{m-1} prod h_i`;
- `(4a+b)a^{m-2} prod h_i > 4a^{m-1} prod h_i`.

Hence neither has a closed-right-half-plane root. The boundary triad has exactly the coefficients at main lines 339–345. Independent expansion gives

- `c1=a h1+4a hm+b h1+b hm+4b hZ`;
- `c2=a(4a h1hm+7b h1hm+4b h1hZ+16b hmhZ)`;
- `c3=16a^2b h1hmhZ`;

and `c1 c2-c3` has 14 strictly positive monomials. The three two-vertex boundary determinants are respectively

`a h1hm(4a+7b)`, `4ab h1hZ`, and `16ab hmhZ`,

with negative traces. Thus every SCC block in the classification is Hurwitz, and Frobenius permutation proves every nonempty principal block of order below `m` Hurwitz.

For the full `X` block, eliminating rows `X3,...,X_{m-1}` contributes `(-a)^{m-3}` and leaves the direct `m=3` boundary matrix

```
[ -(a+b)   -a       -b      ]
[ -a       -a        2a      ]
[ 2a-b      2a      -(4a+b) ]
```

whose determinant is `2a^2b`. Therefore `(-1)^m det J_X=-2a^{m-1}b prod_i h_i<0` in every dimension. The characteristic polynomial is negative at zero and positive for sufficiently large positive `lambda`, so this block has a positive real eigenvalue. Theorem 3.2 and the first-instability order `m=n-1` are valid.

As corroboration only, `independent_core_checks.py` lines 130–153 enumerated every retained set below order `m` for `m=3,...,9`, both generically and at `b=2a`, with no unclassified SCC. Lines 407–440 tested 39,380 random positive principal blocks under eight-decade concentration scalings; no counterexample appeared. The largest sampled spectral abscissa was `-4.77e-8`, a small negative numerical margin caused by extreme scaling, not proof.

### 3. Principal-minor diffusion-ray theorem

Theorem 4.1 is at main lines 376–425 and supplement lines 110–149. Its proof is correct as written. Multilinearity in the selected diagonal entries gives

`det(sD-J)=sum_I a_I prod_{j notin I}(s d_j)`.

After `det J=0`, this is `s q_D(s)` with the stated `beta_k`. For `k>=2`, all contributing sets have order at most `n-2`, so every `beta_k>0`. Hence `q_D` is strictly increasing on `[0,infinity)`, and it has exactly one positive root iff `beta_1<0`. At that root the scalar derivative is positive.

For fixed `s>0`,

`chi_s(lambda)=sum_I a_I prod_{j notin I}(lambda+s d_j)`.

Every derivative contribution from order at most `n-2` is positive for `lambda>=0`, and all order-`n-1` contributions sum to the assumed positive number. Thus `chi_s'(lambda)>0` on the nonnegative real axis. The sign of `chi_s(0)=s q_D(s)` gives exactly one positive real root for `0<s<s*`, none for `s>s*`, and `chi'_{s*}(0)>0`, which is ordinary algebraic simplicity of the zero eigenvalue. The theorem correctly declines to rule out nonreal unstable pairs after the threshold (main lines 399–400).

The positive order-`(n-1)` sum is substantive. If it is deleted, take

`J=[[-1,1],[-3,3]]`, `D=diag(1,2)`.

Then `det J=0`, the only `n=2` lower-order hypothesis is `a_empty=1`, but the signed order-one sum is `-2`. One has `det(sD-J)=s(2s-1)`, so the scalar threshold is `s*=1/2`; nevertheless, at `s=51/100>s*`, both eigenvalues of `J-sD` are positive:

`(47-sqrt(1801))/200` and `(47+sqrt(1801))/200`.

This exact outside-domain counterexample confirms the necessity of the hypothesis for the advertised post-threshold exclusion. It is not a counterexample to the stated theorem.

### 4. Omission table and exact stationary law

Proposition 5.1 is at main lines 442–489 and supplement lines 151–187. Right multiplication by `H` multiplies each retained principal determinant by the retained column product. At `H=I`:

- omitting `Z` leaves the full `X` block derived above;
- omitting an interior `X_j` breaks the chain into feed-forward singleton pieces and the boundary triad, giving the signed determinant `a^{m-3} * 16a^2b =16a^{m-1}b`;
- omitting `X1` leaves the restriction of `c` as a nonzero left nullvector;
- omitting `Xm` leaves the restriction of `H^{-1}(2,-2,...,-2,0,1)^T` as a nonzero right nullvector.

This yields exactly the table at main equations (5.1)–(5.3) and

`beta_1(D)=2a^{m-1}b(prod_{i=1}^m h_i)[8hZ sum_{j=2}^{m-1} d_j/h_j-dZ]`.

I reproduced the complete symbolic table independently for `m=3,4,5,6`, with arbitrary symbolic positive `a,b,H`, at script lines 155–203. The `m=3` interior omission has no singleton factor and is exactly the boundary triad, so no empty-range error occurs.

For `(a,b,H) in S_m`, `c^T J=0` and the restriction to `c^perp` is invertible/Hurwitz. Consequently the full zero eigenvalue is algebraically simple and the order-`m` signed-minor sum—the coefficient of `lambda`—is positive. The lower signed minors are positive by Theorem 3.2, so Theorem 4.1 applies. The strict criterion

`dZ > 8hZ sum_{j=2}^{m-1} d_j/h_j`

is therefore necessary and sufficient for a nonzero stationary determinant crossing on the ray; uniqueness, algebraic simplicity, and the positive-real band follow. Scaling `D` by `gamma` replaces `s` by `gamma s`, giving the stated inverse threshold scaling. Theorem 5.2 is valid.

Boundary equality is correctly excluded. At `m=3`, `a=b=1`, `H=I`, and `D=diag(1,1,1,8)`, exact reconstruction gives

`det(sD-J)=4s^2(2s^2+17s+32)`.

Thus `beta_1=0` and there is no nonzero threshold. Likewise, at `m=3`, `H=diag(1,1,1,1/8)`, one has `T(H)=1` and

`det(lambda I-J)=lambda^2(2lambda^2+17lambda+32)/2`;

the conservation zero is algebraically double, so this point is not in `S_m`. With `hZ=1/16`, `T(H)=1/2` and the complementary characteristic factor has negative constant term and a positive real root. These checks confirm why homogeneous stability and strictness cannot be omitted from the Turing interpretation.

### 5. Sharp contrast, equality, and scope

Theorem 5.3 is at main lines 555–593. Equal damping has

`beta_1(I)=positive_factor * [T(H)-1]`.

For a homogeneously stable realization this coefficient is positive, so `T(H)>1`. If the stationary criterion holds, then

`dZ>d_min T(H)` and `d_max>=dZ`, hence `chi_D>T(H)`.

Conversely, set every `X` diffusivity to one and `dZ=T(H)+epsilon`. Because `T(H)>1`, the contrast is exactly `T(H)+epsilon`; the infimum is `T(H)` and is not attained. At `H=I`, this is `8(m-2)`.

For every interior `j`, `hZ/hj>=1/chi_H`; therefore

`T(H)>=8(m-2)/chi_H`,

and the strict product law `chi_D chi_H>8(m-2)` follows. Equality cannot occur because the stationary criterion is strict. Sharpness as an infimum follows from the stable unit realization `a=b=1,H=I` and the preceding `epsilon` sequence. This is an exact scalar optimization, not finite evidence.

The manuscript accurately restricts the conclusion to this topology and stationary crossings. It expressly does not classify wave instability or a global Pareto frontier (main lines 548–553, 840–847, and 1075–1086).

### 6. Unit-family linear algebra and coefficient equality cases

The selected profile is at main lines 597–617. Direct substitution from the reaction-list matrix gives `(A_m-D_m)r=0` and `ell^T(A_m-D_m)=0` exactly for `m=3,4,149`; the row identities are rational and dimension-formula based, not numerical. The displayed inner products `ell^T r<0` and `ell^T D r<0` also hold exactly.

I independently checked the determinant identities from direct matrices for `m=3,4,5,6`:

- `det(lambda I-A_m)=(1+lambda)^{m-3}P-R`;
- `det(lambda I-A_m+tD_m)=Q_m F-G`.

The chain factorization supplies the all-dimensional bridge; the finite direct checks are corroboration. For `m=3`, the homogeneous quotient is exactly `(lambda+7)(lambda^2+5lambda+2)`. For `m>=4`, I regenerated from the displayed `P,R` definitions the 35-term polynomial `|1+lambda|^2|P|^2-|R|^2`; all nonconstant coefficients are positive and the axis restrictions are positive away from the origin. This proves homogeneous relative stability in all dimensions.

Likewise, rebuilding the displayed `F,G` gives the 77-term spatial polynomial with all positive coefficients and zero constant. Separate pure-axis restrictions in `x`, `z=y^2`, and `s=t-1` are positive, so equality occurs only at `(lambda,t)=(0,1)`. Coefficient signs alone would not have sufficed for this equality statement; the axis check closes it. The algebraic simplicity derivative is separately positive, as required.

These findings verify Theorem 6.1 items 1–3. I did not audit its cubic sign or local nonlinear stability in this subtask.

### 7. Equilibrium-scaled family, endpoints, contrasts, and asymptotics

The scaled family is at main lines 774–1005 and supplement lines 467–778. The physical-to-normalized transformation is correct: `xhat=H(L)x` sends the mode operator to `H(L)(A-t Delta)`, the left critical vector to `H(L)^{-1}ell`, and the physical conservation covector to `H(L)^{-1}c`. The kernel remains `span{r}`. Since `(H^{-1}ell)^T r<0`, a generalized zero eigenvector is impossible; the critical zero is algebraically simple. The transformed transversality numerator is exactly `ell^T Delta r<0`.

I regenerated both scaled determinant identities for `m=3,4,5,6` and independently regenerated the all-parameter modulus polynomials:

- the 84-term spatial polynomial has coefficient polynomials in `A=2nu L` with nonnegative rational coefficients, nonzero for `A>0`, and positive pure-axis restrictions;
- the 22-term homogeneous polynomial has coefficient polynomials in `U=A-1/4` with nonnegative rational coefficients.

At the sharp coefficient-certificate boundary `B=5/4`, the linear `z` coefficient vanishes, but the exact `x=0,U=0` restriction is

`z^2(5z^2+299z+3181)/4`,

so equality still occurs only at `lambda=0`. The manuscript correctly says `5/4` is sharp only for this coefficientwise certificate, not an intrinsic dynamical boundary (supplement lines 569–575).

The contrast extrema follow directly. For `2<=i<=m-1`,

`h_i=K_i/(L K_{i-1})` decreases with `i`; its minimum interior value is `L1/L>=1`, so the global minimum of `H` is one and the maximum is `h_2=(91nu-1)/(91nu L)`. Meanwhile

`(Dphys)_i=h_i/K_i=1/(L K_{i-1})`;

the global minimum is the `i=2` value `1/(91nu L)`, and the global maximum is `d1=23/63`. Hence

`chi_D=(23/63)91nu L`, `chi_H=(91nu-1)/(91nu L)`,

and their product is exactly `23(91nu-1)/63`, independent of `L`. Since `chi_D/chi_H` is increasing in `L` and is already greater than one at `L0`, `max(chi_D,chi_H)=chi_D` throughout the closed interval and has the unique within-family minimum at `L0`.

For `nu>=2`, `L0=sqrt(5)/(2sqrt(nu))`, so both contrasts are `Theta(sqrt(nu))`; the topology-wide product lower bound gives `max(chi_D,chi_H)>sqrt(8nu)`. Thus the exponent `1/2` is optimal for stationary-crossing realizations of this topology. No constant-optimality or global Pareto claim is made.

Exceptional and endpoint checks:

- `m=3` (`nu=1`) was checked by the direct cubic Routh calculation at both `L0=1/sqrt(3)` and `L1=90/91`;
- `m=4` was checked at both closed endpoints, including the equality `nu L0^2=5/4`;
- `m=149` was checked with exact critical right/left residuals and numerical spectral falsification at both current endpoints. At current `L0`, the homogeneous complementary spectral abscissa was about `-3.96e-3`; at current `L1`, about `-9.08e-4`.

As a control, the superseded `m=149` endpoint `L=1/21=1/sqrt(3*147)` lies outside the current interval and has the unstable homogeneous pair approximately

`0.000136549671610 + 0.880678386744 i`.

The current manuscript uses the repaired `sqrt(5)/(2sqrt(nu))` endpoint and does not make the false legacy claim.

### 8. Excluded `m=2` and positivity boundaries

The family is correctly defined only for `m>=3`. A naïve `m=2` continuation makes `Ra` equal `2X1->2X2` and `Rb` equal `2X2->X2`. It then has five reactions rather than `m+2=4`, stoichiometric rank three, and no left conservation kernel. Thus `m=2` is structurally different, not an omitted endpoint.

Similarly, the strict assumptions `a,b>0`, `H>0`, and `D>0` matter. At `a=0` or `b=0`, the Jacobian rank and signed-minor structure degenerate (for the direct `m=3` checks the zero eigenvalue multiplicity rises). These are outside-domain controls, not defects.

## Semantic audit of the supplied core verifiers

The following distinctions are essential when interpreting the packet:

1. `minimal_verifier/verify_all_spectrum.py` lines 101–142 enumerates finitely many `m` and two parameter sets; its symbolic core determinant regression is only `m=3,...,8` (lines 126–132). Its triad calculation is genuinely symbolic in positive `a,b,h` (lines 79–98). The program does not prove the all-dimensional SCC or core-determinant recurrence.

2. `verify_order_m_minors.py` lines 4–7 and `dd_verify_order_m_minors.py` lines 7–10 test `m={3,4,5,6,8,10}`, one `(a,b)`, and `H=I`, against a hard-coded claimed list. The computed side does come from determinants of a reaction-list reconstruction, so the test is not vacuous, but it is finite. The `dd_` version differs only by an assertion-enabled guard and uses the same `common.signed_omissions`; it is not an independent implementation.

3. `verify_diffusion_criterion.py` lines 32–45 and its `dd_` counterpart test finitely many dimensions and one rational `H,D`, plus one symbolic `m=3` example at lines 7–27. They do not prove necessity/sufficiency, uniqueness, ordinary eigenvalue simplicity, or the exact positive-real band. Those are supplied by Theorem 4.1's human proof.

4. `verify_principal_minor_diffusion_ray.py` lines 70–82 checks finite reconstructed example families. Its own docstring correctly says these checks are “not a finite substitute” for the proof (lines 2–7).

5. `verify_contrast_bounds.py` lines 3–8 only checks the selected unit profile for `m=3,...,20`. It does not check the general fixed-`H` infimum or topology-wide product theorem. `verify_stable_contrast.py` similarly samples a finite list and evaluates formulas already encoded in `common.py`.

6. `frontier_verify_determinant_identity.py` lines 15–29 directly checks only `m=3,4,5`. `frontier_verify_mode_certificates.py` lines 33–63 genuinely regenerates the 22/84-term generic polynomials and checks their coefficients at lines 185–222, but connects the characteristic determinant to `QF-R` only in `m=3,4,5` (lines 66–82). The manuscript's chain elimination is therefore the all-dimensional bridge.

7. `frontier_verify_pareto.py` lines 17–38 checks finitely many endpoint instances. `frontier_verify_master_certificate.py` lines 12–34 parses formulas from a stored JSON certificate and checks internal identities; this is consistency, not an independent derivation of the physical extrema or asymptotics.

8. `minimal_verifier/core.py` and `minimal_verifier/common.py` are byte-identical. Several `verify_`/`dd_verify_` pairs differ only by the assertion guard. Their separate `PASS` strings must not be counted as independent corroborations.

None of these code limitations invalidates the mathematics because the all-dimensional deductive arguments are present and correct. They do mean that a referee must not infer an all-dimensional theorem merely from the advertised program count or `PASS` output.

## Commands and outcomes for this sub-audit

Primary independent replay:

```text
cd independent_referee_audit_v1.0.7_2026-08-22/agent_core_math
python independent_core_checks.py > independent_core_checks_output.json
```

Final outcome: exit status 0. The run independently reconstructed and checked:

- exact reaction/rank/kernel/conservation and symbolic omission tables for `m=3,4,5,6`;
- every induced SCC below order `m` for `m=3,...,9`, generic and `b=2a`;
- exact triad coefficients, all 14 positive Routh-gap terms, and all boundary pairs;
- exact diffusion-polynomial coefficients for `m=3,...,7`;
- direct unit/scaled determinant factorizations for `m=3,4,5,6`;
- independently generated 35/77/22/84-term modulus polynomials and equality axes;
- 39,380 floating-point principal-block falsification cases;
- exact critical kernels for `m=3,4,149`, current endpoint spectra, and the excluded legacy `m=149` control;
- exact criterion-equality, homogeneous-boundary, removed-hypothesis, and naïve-`m=2` counterexamples.

I also compared paired packet scripts with `diff -u`; the order-minor, diffusion-criterion, and contrast `dd_` variants differ from their counterparts only by the `__debug__` guard.

## Defects and repairs

### Mathematical defects

None found in the assigned core. No hypothesis, conclusion, or headline repair is required.

### Reproducibility/evidentiary limitations

- **Nonfatal, material to referee interpretation:** finite regressions and hard-coded expected formulas do not certify the all-dimensional SCC, omission, diffusion-law, or contrast theorems. The exact repair to any claim that the programs themselves prove those theorems would be to call them finite/exact regression and mutation checks. The manuscript generally does treat the human proof as primary, so this does not change a theorem.
- **Nonfatal independence concern:** several `dd_` checks share the same helper and essentially the same source as their paired checks. They should not be counted as independent implementations. This changes only the evidentiary description, not a mathematical hypothesis or conclusion.

### Optional expository clarifications

- In the `b=2a` SCC sentence, explicitly note that the deleted edge belongs to neither long cycle, so any nontrivial refinement remains within the permitted boundary-triad class.
- In the sparse full-`X` determinant proof, displaying the three-by-three Schur/elimination remainder above would make the all-dimensional recurrence immediately checkable.

These are optional clarifications, not gaps; no theorem or headline changes.

## Confidence and remaining uncertainty

Confidence in the assigned algebraic core is **very high (about 98%)**. The strongest evidence is the conjunction of a complete deductive reconstruction, independent exact matrices and determinants, exact regeneration of the generic coefficient polynomials, explicit boundary counterexamples confirming the hypotheses, and numerical falsification across exceptional/high-dimensional cases.

The strongest remaining uncertainty for the manuscript as a whole is outside this sub-audit: the all-dimensional cubic-sign derivation and the functional-analytic passage from the reduced bifurcation to local exponential stability. I make no whole-manuscript validity recommendation until those independent audits are combined.
