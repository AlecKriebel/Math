# Independent audit: response functions, optimization, and quantifier transfer

**Checkpoint:** 2026-08-22 12:40 PDT
**Auditor:** response/quantifier subagent
**Best-guess completion:** **100% of the assigned response-function, optimization, rational-edge, and quantifier-transfer slice.**
**Boundary:** read-only review of `delivered_copy`; no network, contact, upload, commit, push, or modification of delivered material. The independent exact calculation is `independent_checks/response_math/independent_response_audit.py`. It does not import the authors' programs.

## Bottom line

I found **no critical, high, medium, or low mathematical defect in the audited algebra and quantifier chain**. Conditional on the weak-cut trace and center-module asymptotics supplied by Propositions 5 and 6, the gate ratios, both first-order response functions, their common feasibility gap, the sextic tangency, fixed-positive-parameter optimality, rational-edge threshold, and final diagonal transfer all check exactly.

The strongest independently verified statement in this slice is:

> If the compact-uniform asymptotics in Propositions 5, 6, and 12 hold, then the manuscript's explicitly defined, fitness-independent graph sequence has both normalized fixation gains positive for every fixed $1<r<R_{\rm hyb}$ once $t$ is sufficiently large; the exact response-model obstruction also prevents any fixed real σ, and hence any fixed positive σ, from extending a response-positive interval immediately past $R_{\rm hyb}$.

This does **not** independently certify the long stopped-process/expectation/logarithmic estimates underlying Proposition 6. Those are being audited separately. I treated them as hypotheses here and checked that the response proof uses them consistently and at the claimed error scale.

## Exact source anchors

| Component | PDF location | LaTeX source location |
|---|---|---|
| Update rules, uniform initialization, complete-graph baselines, and $R_{\rm sim}$ quantifiers | p. 3, equations (1)--(6), Definition 1 | `main.tex:141-199` |
| Sextic, $\sigma_*$, $\lambda_*$, graph parameters, and fitness-independent weak cut | pp. 3--4, equations (7)--(8), Lemma 2 | `main.tex:203-225`, `276-322` |
| Main amplification statement | p. 5, Theorem 3; proof on p. 18 | `main.tex:324-336`, `1348-1357` |
| Separated finite trace and weak-cut limit | pp. 5--6, Proposition 5, equations (9)--(10) | `main.tex:379-440` |
| Center-module inputs | p. 6, Proposition 6, equations (11)--(15) | `main.tex:445-466` |
| Portal functionals, gate-rate table, adverse reversals, and $Z_B,Z_D$ | pp. 16--17, Proposition 12 | `main.tex:1144-1247`, especially `1178-1179`, `1193-1205`, `1214-1245` |
| Two response functions and component simplifications | p. 17, Proposition 13, equations (41)--(44) | `main.tex:1249-1290`, especially `1261-1268`, `1280-1288` |
| Feasibility, tangency, sextic, and monotonicity | pp. 17--18, Lemma 14 | `main.tex:1292-1346` |
| Fixed-parameter response optimality | p. 18, Proposition 15 | `main.tex:1359-1382` |
| Rational-edge specialization | pp. 18--19, Corollary 16 | `main.tex:1384-1416` |
| Scope limitations and eventual-only nature of the theorem | p. 19, Discussion | `main.tex:1420-1465` |

## 1. Baselines and first-order bookkeeping

### Complete-graph baselines: verified

For Bd on (K_n), the down/up odds of the mutant-count chain are (1/r), so the standard product-of-odds solution gives

\[
 \rho_{\rm Bd}(K_n,r)=\frac{1-r^{-1}}{1-r^{-n}}.
\]

For dB, the one-step odds are not constant. At mutant count (k), direct cancellation gives

\[
 \gamma_k=\frac{n-1+(r-1)k}
 {r\{n-1+(r-1)(k-1)\}},
 \qquad
 \prod_{j=1}^k\gamma_j
 =r^{-k}\frac{n-1+(r-1)k}{n-1}.
\]

Substitution in the exact birth-death hitting formula telescopes to

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}\frac{1-r^{-1}}{1-r^{-(n-1)}}.
\]

These agree with PDF equations (5)--(6), `main.tex:179-189`. The independent script also solved these product formulas exactly for (2\le n\le12) at three rational fitnesses.

On every fixed compact (r\in[r_-,r_+]\Subset(1,\infty)), with (n\asymp C=t^4),

\[
 \rho_{\rm Bd}(K_n,r)-p=O(r_-^{-n}),\qquad
 \rho_{\rm dB}(K_n,r)-p=O(C^{-1}),\qquad p=1-r^{-1}.
\]

Because $\eta:=q/C=t^{-3}$, both are $o(\eta)$. Thus replacing the finite baselines by $p$ in the first-order derivation on p. 17 is legitimate. Positivity is also clear: $r>1$ makes $p$, $1-r^{-n}$, and $1-r^{-(n-1)}$ positive.

### Pair and pendant components: verified from the stated asymptotics

For an isolated (K_2), a single mutant fixes with probability (r/(r+1)) under Bd. Under dB, the first uniformly selected death decides the outcome because the remaining vertex is the only possible parent, so the singleton value is exactly (1/2), independent of (r). This verifies `main.tex:1207-1212`.

The finite trace, PDF equation (9), is

\[
 \rho_U^0=\frac{C+m}{N}a_H^UP_U^H
 +\frac{2q}{N}a_P^UP_U^P,
 \qquad N=C+m+2q.
\]

Set (m/C=\lambda\eta+o(\eta)). Proposition 6 gives center numerators

\[
 \frac{C+m}{C}\,a_H^{\rm Bd}=p+\lambda\eta+o(\eta),
 \qquad
 \frac{C+m}{C}\,a_H^{\rm dB}=p+o(\eta).
\]

Together with (P_U^H=1-o(\eta)), the first-order normalized traces are therefore

\[
 \frac{p+\lambda\eta+2\eta\,[r/(r+1)]\,Z_B/(1+Z_B)}
 {p\{1+(\lambda+2)\eta\}}+o(\eta)
\]

for Bd and

\[
 \frac{p+2\eta\,[1/2]\,Z_D/(1+Z_D)}
 {p\{1+(\lambda+2)\eta\}}+o(\eta)
\]

for dB. Differentiating these rational expressions at η(=0) independently reproduces equations (41)--(42).

The pendant contribution is exactly

\[
 \lambda(1/p-1)=\frac{\lambda}{r-1}
\]

under Bd and (-\lambda) under dB. The (-2) inside each pair correction comes from the two pair vertices displaced in the vertex-count denominator. This accounts for every first-order component; there is no missing baseline or population-size term.

## 2. Gate odds and macro rates

The portal identities on p. 16 are exact:

\[
 I_P=2/W=2\sigma/C,\qquad J_P=1/W=\sigma/C.
\]

The second identity uses two dB singleton committors of $1/2$. Applying the Proposition 6 limits to the $A,D$ columns of the gate table gives

| Rule | $A$, pair invades center | $D$, pair is lost | $A/D$ |
|---|---:|---:|---:|
| Bd | $CrI_Pp\to2\sigma(r-1)$ | $2I_H/(r+1)\to2/(r+1)$ | $Z_B=\sigma(r^2-1)$ |
| dB | $2rJ_H(r)\to2(r-1)$ | $(C/r)J_P(1/r)=\sigma/r$ | $Z_D=2r(r-1)/\sigma$ |

This verifies the macro-rate formulas at `main.tex:1178-1179` and `1241-1244` independently of the supplied coefficient certifier.

The global-sweep use of adverse reversals is also consistent. From ((1,k)), the probability that the center reverses before the next successful pair conversion is (C'/(B+C')). At most (q) conversions are needed, hence

\[
 1-P_U^H\le q\frac{C'}{B+C'}.
\]

For Bd, $C'=CI_Pu_{\rm core}^{\rm Bd}(1/r)=2\sigma\,o(C^{-1})=o(C^{-1})$, while the conversion rate $B\to2r^2/(r+1)>0$. For dB, $C'=(2/r)J_H(1/r)=o(C^{-1})$, while $B=CrJ_P=r\sigma>0$. Thus $qC'/B=o(q/C)=o(\eta)$, uniformly on a fixed fitness compact. The exact first-step identity

\[
 P_U^P=\frac{A}{A+D}p_{1,1}
 =\frac{A}{A+D}\frac{B+C'}B P_U^H
\]

then gives (P_U^P\to Z_U/(1+Z_U)). No branching-survival substitution is hidden here.

All rate and response denominators are positive for $r>1,\sigma>0$: $r-1>0$, $1+\sigma(r^2-1)>1$, $\sigma+2r(r-1)>\sigma$, and $1+Z_U>1$.

## 3. Response functions and feasibility gap

Writing the two brackets as $\mathcal B,\mathcal D$ to avoid confusion with the gate-rate labels,

\[
 \mathcal B(r;\sigma,\lambda)
 =\frac{2(\sigma-1)}{1+\sigma(r^2-1)}+\frac{\lambda}{r-1},
\]

\[
 \mathcal D(r;\sigma,\lambda)
 =\frac{2\{r(2-r)-\sigma\}}{\sigma+2r(r-1)}-\lambda.
\]

The independent expansion gives the same two pair simplifications as PDF equations (43)--(44):

\[
 2\left(\frac{[r/(r+1)]Z_B/(1+Z_B)}p-1\right)
 =\frac{2(\sigma-1)}{1+\sigma(r^2-1)},
\]

\[
 2\left(\frac{[1/2]Z_D/(1+Z_D)}p-1\right)
 =\frac{2\{r(2-r)-\sigma\}}{\sigma+2r(r-1)}.
\]

Define

\[
 L=\frac{2(1-\sigma)(r-1)}{1+\sigma(r^2-1)},\qquad
 U=\frac{2\{r(2-r)-\sigma\}}{\sigma+2r(r-1)}.
\]

Then, exactly,

\[
 \mathcal B=\frac{\lambda-L}{r-1},\qquad
 \mathcal D=U-\lambda.
\]

Consequently simultaneous positivity is equivalent to (L<\lambda<U). Direct common-denominator expansion gives the useful stronger identity

\[
 U-L=
 \frac{-2rF_r(\sigma)}
 {\{1+\sigma(r^2-1)\}\{\sigma+2r(r-1)\}},
\]

where

\[
 F_r(\sigma)=(r-1)\sigma^2
 +(r^3-4r^2+3r+1)\sigma+r(2r-3).
\]

The denominator is strictly positive, so (L<U\iff F_r(\sigma)<0), exactly as claimed at `main.tex:1300-1317`.

## 4. Minimizer, sextic isolation, tangency, and monotonicity

Because (r-1>0), (F_r) is a strictly convex quadratic in σ. Completing the square gives

\[
 \sigma(r)=\frac{-r^3+4r^2-3r-1}{2(r-1)},
\qquad
 \min_{s\in\mathbb R}F_r(s)=-\frac{P(r)}{4(r-1)},
\]

with

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1.
\]

Equivalently, the discriminant of (F_r) as a quadratic in σ is exactly (P(r)). These identities independently reproduce `main.tex:1318-1322`.

An independent Sturm sequence has sign-variation counts

\[
 V(1)=4,\qquad V(3/2)=4,\qquad V(151/100)=3.
\]

Thus there is no root in ((1,3/2)) and exactly one in ((3/2,151/100)). Exact endpoint evaluation gives

\[
 P(3/2)=1/64>0,
\qquad
 P(151/100)=-39866792399/10^{12}<0.
\]

The isolated root and resulting parameters are

\[
 R_{\rm hyb}=1.5028569127905696267\ldots,
\quad \sigma_*=0.13067728228704837686\ldots,
\quad \lambda_*=0.75080648303188049230\ldots.
\]

The sign premises used in Lemma 14 are exact, not merely decimal. For (3/2<r<151/100), writing (g(r)=-r^3+4r^2-3r-1=r^2(4-r)-3r-1), crude rational interval bounds already give

\[
 0<29/400<g(r)<801/4000,
\]

and (2(r-1)\ge1), so (0<\sigma(r)<801/4000<1). Moreover

\[
 \sigma(r)(r-1)^2
 <\frac{801}{4000}\left(\frac{51}{100}\right)^2<1.
\]

At $r=R_{\rm hyb}$, $P(r)=0$ makes the quadratic minimum zero, hence $F_r(\sigma_*)=0$ and $\partial_\sigma F_r(\sigma_*)=0$: this is the asserted double tangency. Since $\lambda_*=L(R_{\rm hyb},\sigma_*)$, the gap identity also gives $U(R_{\rm hyb},\sigma_*)=\lambda_*$.

Finally,

\[
 \partial_rL=
 \frac{2(\sigma-1)\{\sigma(r-1)^2-1\}}
 {\{1+\sigma(r^2-1)\}^2}>0,
\qquad
 \partial_rU=
 \frac{4r(\sigma-r)}{\{\sigma+2r(r-1)\}^2}<0.
\]

The exact signs above imply (L(r,\sigma_*)<\lambda_*<U(r,\sigma_*)) for every (1<r<R_{\rm hyb}), and both responses vanish at the endpoint.

### Fixed-parameter optimality: scope and proof verified

On ((R_{\rm hyb},151/100]), uniqueness of the root and the negative value at (151/100) give (P(r)<0). Hence

\[
 \min_{s\in\mathbb R}F_r(s)=-P(r)/\{4(r-1)\}>0.
\]

No real σ can be feasible at any such (r). Any putative response-positive interval beginning at one and extending beyond (R_{\rm hyb}) contains such points immediately to its right, so Proposition 15 follows.

The manuscript scopes this result correctly: it is optimality only among **fixed positive** ((\sigma,\lambda)) in the displayed first-order dilute pair--pendant response model. It is not an upper bound on (R_{\rm sim}), and pp. 18--19 / `main.tex:1449-1458` explicitly exclude singular or size-dependent parameters, other scales, second-order boundary gains, nonseparated dynamics, other modules, and non-dilute interactions. I found no optimization overclaim.

## 5. Rational-edge specialization

For $\sigma=19/137$, $\lambda=20/27$, direct exact substitution at $r=3/2$ gives

\[
 \mathcal B=\frac{232}{17361}>0,
 \qquad
 \mathcal D=\frac{65}{12123}>0,
\]

as stated in Corollary 16. The full dB response factors as

\[
 \mathcal D(r)=
 -\frac{2(6439r^2-10138r+703)}
 {27(274r^2-274r+19)}.
\]

Its denominator is positive for (r>1), and the unique root in ((1,2)) is

\[
 R_{\mathbb Q}=\frac{5069+12\sqrt{147001}}{6439}
 =1.5017681522336868846\ldots>3/2.
\]

The Bd response is

\[
 \mathcal B(r)=
 \frac{4(95r^2-1593r+2183)}
 {27(r-1)(19r^2+118)}.
\]

It is still positive at (R_{\mathbb Q}). One entirely rational sign check is: the dB quadratic is already positive at (751/500), so (R_{\mathbb Q}<751/500); the Bd numerator is decreasing on ((1,2)), and at (751/500) its numerator, over the common denominator (250000), is (1{,}158{,}595>0). Thus it is positive at the smaller (R_{\mathbb Q}). The monotonicity signs for (L,U) then prove both responses positive throughout ((1,R_{\mathbb Q})).

Every specialized graph weight is rational: unit core/pendant weights; (W_t=C_t/\sigma=137C_t/19); (m_t=\lfloor(20/27)t\rfloor); and the least-dyadic weak cut (2^{-e_t}). The phrase "rational-edge family" is therefore exact.

## 6. Effective diagonal and exact quantifier order

### Denominator and decidability check

For every positive weak cut, the graph is finite and connected. Every nonabsorbing configuration of either update chain is transient, so its transient matrix (Q(r)) has spectral radius below one. Therefore (I-Q(r)) is a nonsingular (M)-matrix; in particular its determinant and all event denominators are positive. The Bd denominators (F(S)) and (d_u) are positive, and each dB parent-choice denominator is a positive weighted sum because every vertex has positive degree. The same argument applies after normalizing the finite macro generator to a transient discrete chain.

For fixed (t,e), all weights lie in (\mathbb K=\mathbb Q(R_{\rm hyb})) and all first-step entries are in (\mathbb K(r)). Cramer's rule thus makes actual fixation, separated fixation, and the finite complete-graph baseline rational functions over (\mathbb K). Clearing the verified positive denominators turns each absolute-value condition in Lemma 2 into two polynomial inequalities on the algebraic interval (I_t). Exact real-algebraic decision is therefore valid in principle.

Existence does not require a uniform rate in $t$: for each fixed $t$, $I_t$ is a compact subset of $(1,\infty)$, and Proposition 5 gives uniform convergence as $\varepsilon\downarrow0$ on that one interval. Hence at least one dyadic exponent is admissible, and testing positive integers terminates at the least $e_t$. This verifies the logical content of Lemma 2; it does not supply a useful complexity or size bound, and none is claimed.

### Diagonal transfer

The exact quantifier order is

\[
 \exists\{G_t\}_{t\ge2}\
 \forall r\in(1,R_{\rm hyb})\
 \exists t_0(r)\
 \forall t\ge t_0(r):
 \quad \rho_{\rm Bd}(G_t,r)>\rho_{\rm Bd}(K_{n_t},r),\quad
 \rho_{\rm dB}(G_t,r)>\rho_{\rm dB}(K_{n_t},r).
\]

The sequence is chosen first: (C_t=t^4,q_t=t,m_t=\lfloor\lambda_*t\rfloor,W_t=C_t/\sigma_*), and (e_t) is selected by a supremum over the whole expanding interval (I_t=[1+1/t,R_{\rm hyb}-1/t]), not at a later chosen fitness.

For every fixed interior (r), eventually (r\in I_t). Proposition 13 and Lemma 14 give

\[
 \frac{n_t}{q_t}
 \left(\frac{\rho^0_{U,t}(r)}{\rho_U(K_{n_t},r)}-1\right)
 \longrightarrow \mathcal R_U(r)>0,
\]

because ((n_t/q_t)(q_t/C_t)=n_t/C_t\to1). Lemma 2 changes this scaled gain by at most (1/t). The actual connected-graph gain is therefore positive eventually for each rule. This is exactly Definition 1's pointwise-in-fitness eventual quantifier, not a stronger unclaimed uniform (t_0) over the open interval.

## Findings and unresolved dependencies

### RESP-01 — Verified, no adverse finding — algebra/optimization

All response, gap, derivative, minimizer, sextic, endpoint, rational-margin, and threshold identities pass independent exact calculation. The independent Sturm variation counts reproduce the stated root isolation.

### RESP-02 — Verified, no adverse finding — diagonal/quantifiers

The least-dyadic construction is fitness-independent, its existence follows from fixed-(t) compact uniformity, and the scaled-error inequality has exactly the strength needed for the pointwise eventual theorem.

### RESP-DEP-01 — Cross-audit dependency, not a defect in this slice — stochastic asymptotics

The response conclusion is conditional on Proposition 6's (o(q/C)), (o(C^{-1})), and compact-uniform estimates and Proposition 5's weak-cut trace. Their proofs contain expected-value, logarithmic-time, stopping, Green-function, and renewal claims (`main.tex:499-1140`). The symbolic response calculations do not validate those claims. No inconsistency in their use was found: every imported error is at or below the scale required in Proposition 13. These dependencies are assigned to the separate stochastic-mathematics audit.

## Reproducibility note

`independent_checks/response_math/independent_response_audit.py` reconstructs the complete-graph odds, gate ratios, full trace derivatives, feasibility gap, quadratic minimum, sextic discriminant, Sturm counts, tangency signs, and rational-edge specialization. Its final run passed using exact SymPy arithmetic. The script is evidentiary support; the derivations above state the mathematical reasons and do not treat program output as proof by itself.

**Final completion estimate:** **100% of assigned slice.** No unresolved response-algebra or quantifier gap remains; only the explicitly separated stochastic premises remain outside this report.
