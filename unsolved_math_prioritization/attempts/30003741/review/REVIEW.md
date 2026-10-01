# Independent review: agonist-only equilibrium reduction and the four-site bound

**Verdict: PASS_SCOPED_AGONIST_REDUCTION_PARITY_BOUND_AND_N4_WITNESS.** No mandatory correction was found. Recommend **unsolved, 2/5** for the original higher-multiplicity question. The sharp four-site result does not decide whether the agonist-only system can have more than three equilibria for higher $N$.

Reviewed 30 September 2026 by a separate gpt-6-astra agent at xhigh. This is an adversarial AI review, not human peer review. No historical-priority, stability or clinical claim is made.

## 1. Frozen artifact and exact source

- `PARTIAL.md`: SHA-256 `fcfb9ad76db48049753641577b132fd079712084e32fd149b400c83870b398a6`
- Submitted `verify.py`: SHA-256 `53480f627875d64dada51efa47a5c41b845d5a37188eab247fc36126ab30ec54`
- Submitted receipt: SHA-256 `ebe222f839a7ae2c68ad933a3086ed08e0fc2a915c8f377daf9a37e9329cefa2`
- All 1,543 submitted exact controls reproduce byte-identically in an isolated copy.
- All 10,436 independent exact controls pass.

I independently read the complete Rendall contribution in [OWR8/2018, pp.487–489](https://ems.press/content/serial-article-files/46732), and visually checked the exact question on p.488. Its response-function discussion uses one ligand amount and one dissociation rate. I then checked the model equations and the relevant complete Section3 discussion in the [published Rendall–Sontag paper](https://www.sontaglab.org/FTPDIR/2017_rendall_sontag_tcells_royal_open_reprint.pdf). Equations2.1–2.7 describe two ligands, but the section explicitly restricts to the agonist-only system before Theorem3.1 and the following higher-$N$ count question.

The candidate’s equations are exactly that restriction: set the antagonist total and all antagonist complexes to zero, and rename the agonist total and dissociation rate. The physical positivity statement applies to the retained species and their free pools; it does not falsely demand positive antagonist concentrations on this boundary restriction. The source-scope qualification is appropriate because the OWR prose does not reproduce every model assumption.

The [September2026 two-ligand candidate](https://evidencepress.org/releases/tcell-exactly-five/) explicitly excludes the narrower agonist-only question. I checked that scope statement, not its proof or verifier. Its claimed five-equilibrium example is not used to settle the target or to support the mathematical deductions reviewed here.

## 2. Binding balance and conservation class

Summing the receptor equations cancels the phosphorylation and dephosphorylation transfers and gives

$$\dot\Sigma=\kappa(L-\Sigma)(R-\Sigma)-\nu\Sigma.$$

On $0\le\Sigma\le\min(L,R)$, this expression is positive at zero and negative at the other endpoint. Its derivative is

$$-\kappa(L+R-2\Sigma)-\nu<0$$

throughout the interior. Thus it has exactly one physical zero $\sigma$, strictly between zero and both totals. This holds whether $L<R$, $L>R$ or $L=R$.

The conserved quantities are $L,R,S_T$ in the full mass-action description. The sum of complexes $\Sigma$ is not conserved; it acquires the uniquely determined value $\sigma$ only at equilibrium. The candidate makes this distinction explicitly and does not count equilibria from different binding totals as though they were in one fixed class.

## 3. Tail recurrence and complete positive reconstruction

At a steady state, summing the receptor equations from index $j$ through $N$ gives

$$\phi C_{j-1}=(b+\gamma S)C_j+\nu\sum_{i=j}^NC_i.$$

Starting at $C_N$, this gives the author’s positive recurrence, including $P_1=u$ and

$$P_m=uP_{m-1}+vD_{m-2},\qquad D_m=\sum_{i=0}^mP_i.$$

There is no sign error from the terminal dissociation term: it is included in $u=(b+\nu+\gamma S)/\phi$, whereas the earlier tail contribution carries $v=\nu/\phi$. For $N=1$, the middle equations are absent and the same initialization works.

Every $P_m(u)$ and $D_m(u)$ is positive for $u>0$, $v>0$. Fixing $\sum C_j=\sigma$ therefore gives one and only one receptor-chain solution for each phosphatase level:

$$C_j=\sigma\frac{P_{N-j}(d+t)}{D_N(d+t)}.$$

The converse is complete. The recurrence gives every tail balance; differences give the individual interior equations, the final tail gives the terminal equation, and the aggregate binding balance supplies the remaining $C_0$ equation. It is not merely a necessary elimination relation.

Substitution into the phosphatase equation yields the exact residual

$$\dot S=-\frac{\beta\phi}{\gamma D_N(d+t)}F_N(t).$$

The denominator is strictly positive. At $t=0$, $F_N$ is strictly negative; for $t\ge h$, it is strictly positive. Consequently every positive scalar root is in $(0,h)$ and reconstructs $0<S<S_T$, positive complexes, and positive free ligand and receptor pools. Conversely every physical equilibrium yields one such root. Since $S=\phi t/\gamma$ is injective in $t$, distinct roots give distinct equilibria. There are no lost roots, denominator poles or artificial physical roots.

## 4. All-parameter root-count bound

The induction behind the coefficient claim is valid for all $N$, not only the checked values. Multiplication of the monic $P_{m-1}$ by $u$ supplies the degree-$m$ leading term; its missing subleading coefficient remains missing, and the added term $vD_{m-2}$ has degree at most $m-2$. Adding $P_{m-1}$ into $D_m$ supplies its subleading coefficient one.

It follows that $F_N$ is monic of degree $N+1$, its coefficient at degree $N$ is

$$Nd+1+A>0,$$

and its constant coefficient is negative. The term involving $-AhP_{N-1}$ cannot affect the top two coefficients. This remains correct at $N=1$.

After zero coefficients are removed, the sign list starts negative and ends with two positive entries. The total number of sign changes is odd, while the equal signs of the top two coefficients force it to be at most $N$. Therefore the largest permitted number is $N$ for odd $N$ and $N-1$ for even $N$. Descartes’ rule bounds positive roots **with multiplicity**, and hence also bounds the number of distinct physical equilibria through the bijection.

The published 2017 paper states the elementary higher-$N$ bounds $N$ and $N+1$, respectively, after its separate small-$N$ theorem. The candidate’s even-$N$ coefficient observation improves that general bound by two; this is not a claim that the already-known $N=2$ uniqueness result is new. For $N=4$ it proves at most three. For $N\ge5$ it does not establish a uniform three-root ceiling.

## 5. Exact four-site witness

All parameters in the proposed witness are strictly positive, including $b$ and $\nu$. The binding equation has the physical root $\sigma=1/2$; the other algebraic root of the quadratic is outside the physical interval and is not used. The dimensionless parameters and all six displayed integer coefficients are correct.

As an independent elimination check, I formed the receptor linear system directly from the ODE at $\phi=1$. Its negative coefficient matrix has diagonal entries

$$1+v,\ 1+u,\ldots,1+u,\ u,$$

subdiagonal $-1$, and superdiagonal $-(u-v)$. The source vector is $v\sigma e_0$. Determinants and Cramer’s rule recover the displayed quintic without using the author’s recurrence to construct it. The cleared phosphatase numerator is exactly its stated positive scalar multiple.

The four exact evaluations in the candidate have the stated alternating signs, so the three disjoint brackets each contain a root. The all-parameter bound permits at most three positive roots counted with multiplicity; hence these are all the positive roots and each is simple.

I additionally used an independent exact Sturm calculation: there are three roots in $(0,20)$, one in each stated bracket, three in $(0,\infty)$ in total, and none above20. The polynomial has constant gcd with its derivative. These are exact rational certificates, not numerical root approximations.

The reconstruction has $\sum C_j=1/2$, free ligand and receptor both $1/2$, and inactive phosphatase $20-t>0$. Each $P_{4-j}$ is strictly positive throughout every bracket. Symbolic substitution verifies the receptor equations identically and the phosphatase equation modulo the witness polynomial. Thus the three roots correspond to three genuinely physical equilibria in the same fixed conservation class.

Scalar simplicity does not by itself classify the spectrum of the full ODE Jacobian. The absence of any claimed stability, bistability or physiological conclusion is correct.

## 6. Independent checks and exact limits

The independent checker does not import the submitted code. It uses 90 direct rational solves of the original receptor linear system, symbolic determinant/cofactor comparisons, exact feedback residuals, exhaustive low-degree sign-pattern controls, and an independent Sturm analysis of the witness. The unrestricted theorem is justified by the written induction and Descartes argument; finite degree checks alone would not prove it.

The exploratory grid in the package is expressly labeled noncertifying. Observing at most two sampled derivative sign changes cannot rule out unsampled turning points. It is not used in the proof of the count bound or the four-site witness. The higher-$N$ root-count problem remains open in this attempt, and the distinct two-ligand candidate does not fill that gap.

From this report’s directory:

```sh
(cd author_replay && cp verification.json /tmp/agonist-expected.json && python verify.py > /tmp/agonist-author-stdout.json && cmp verification.json /tmp/agonist-expected.json)
python independent_checks.py > /tmp/agonist-independent.json
cmp independent_results.json /tmp/agonist-independent.json
```

**Final recommendation:** publish only as a reviewed partial package, with `unsolved`, two approaches, the agonist-only source qualification and the exact $N=4$ theorem. No mandatory correction remains. No full higher-multiplicity resolution, external-candidate certification, historical novelty, human peer review or clinical implication is established.
