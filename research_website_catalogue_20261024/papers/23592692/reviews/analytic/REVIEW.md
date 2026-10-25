# Independent analytic review — Zenodo 23592692

**Verdict: PASS for the exact stated finite-graph theorem.** No substantive mathematical gap was found in the seven-page published version. This is an independent internal AI proof review, not human peer review, a formal proof certificate, or a certification of worldwide novelty. Standard published stochastic theorems are accepted at their checked interfaces.

Reviewed title: *A sharp forest bound and an improved whisker bound for finite WARM graphs*, Alec Kriebel, version 1.0.0, printed 21 October 2026. Review completed 25 October 2026 UTC.

## Source binding and read scope

The complete seven-page public PDF was read, including definitions, proofs, limits, disclosure and references. Main source TeX and the necessary published verification programs/certificates were inspected. The archive's only PDF is byte-identical to the public seven-page PDF; there is no separate unread mathematical reader supplement.

- Main PDF SHA256: `42c5c632de7e942df6b7c407fb95d877a165281f215e4aa7d1dfa862b08b2157`.
- Source/verification ZIP SHA256: `e92f6fa13245686525a0dd8fc4c5327bd03e58a1f02ae7dcae918668c16c5fee`.
- Main TeX SHA256: `c38cd59fafe43e0637c2c89a60389c7f59940a95e86bb6ba749fe97d4de5def1`.
- Externally pinned SOURCE_MANIFEST SHA256: `e3db5fb166e0823ebacb4048f8330c398e80c0c237bfc02c897f0891026508ba`.

`source_binding.json` independently rechecks both public sizes, MD5 and SHA256 against the fresh acquisition receipt; ZIP CRC and all 45 extracted file bytes; the identical embedded PDF; and all four retained primary PDFs. It includes exact source URLs and hashes. Hashes establish identity, not truth. Page 6 was also rendered and visually inspected to resolve the extraction's displaced square-root symbol: the actual printed constant is correctly (C=3-\sqrt2).

No sibling findings or dedicated historical review bodies were read. Universal reasoning and the fresh 87-check control artifact preceded supplied-helper inspection. The manuscript itself discusses historical statuses; the required `verify_priority.py` code and replay expose literal historical-outcome checks. Those incidental assertions were not adopted as evidence of correctness or priority. Historical reports were read only as opaque bytes by custody verification. This is therefore independent derivation with disclosed incidental status exposure, not a claim of perfectly blinded review.

## Exact claim and boundary conditions

The graph is finite, simple, undirected and loopless. Each non-isolated vertex has an independent Poisson clock of fixed positive finite rate. At each firing it selects one incident edge with probability proportional to its positive integer count raised to a fixed real power \(\alpha>1\), then increments that count by one. Initial counts may be any fixed positive integer vector. Isolated vertices have no effect. The model has no explosion because the total clock rate is finite and constant.

Theorem 1 asserts:

1. For arbitrary positive rates and \(\alpha>4/3\), the infinitely reinforced edges almost surely form a forest.
2. For equal rates and \(\alpha\ge17/4\), every surviving component almost surely is a tree of diameter at most three.
3. For each \(1<\alpha<4/3\), a unit-initialized equal-rate triangle has positive probability that all three edges survive. Thus the forest threshold constant cannot be decreased; no assertion is made at equality.

The proof does not establish the suggested sharp equal-rate whisker bound throughout \((4/3,17/4)\), nor the stochastic equality case \(4/3\). It does not cover noninteger initial offsets, zero initial edges, infinite graphs or loops. Unequal-rate whisker assertions are excluded. The 17/4 number is a sufficient bound, not a claimed optimum. Empty graphs are immediate; disconnected graphs are handled componentwise if a cited formulation is read with connected-graph conventions, using only finitely many components.

## Stochastic bridge and initialization (pages 2–3)

Write \(\Lambda=\sum_v\lambda_v\), \(S_v=\sum_{e\ni v}a_e^\alpha\) and
\[
F_e(a)=-a_e+\sum_{v\ni e}\lambda_v a_e^\alpha/S_v(a).
\]
With \(p_v=\lambda_v/\Lambda\), \(x=a/\Lambda\), the identity \(F_\lambda(a)=\Lambda F_p(a/\Lambda)\) is exact. Differentiation shows that the Jacobians agree. This correctly distinguishes counts per unit Poisson time from counts per jump; it creates no threshold rescaling error.

The actual published HHK 2023 Theorem 1 (printed p.3016) says that for finite graphs, positive rates and \(\alpha>1\), the unit-initialized normalized counts converge almost surely to a stable or critical equilibrium, meaning the Jacobian has no positive eigenvalue. It also gives positive probability of attaining any strictly linearly stable equilibrium. Its Proposition 1, under bounded degrees and bounded positive clock rates, identifies divergence with positive limiting lower growth. These hypotheses hold here, and finiteness makes the simultaneous assertion over edges immediate. Consequently \(E_\infty=E_+\) equals the positive support of the limit.

The paper does not mistakenly promote the older 2016 convergence conjecture to a theorem; it uses the published 2023 convergence result. I checked its statement, model/normalization, and proof interface. I did not reprove all the stochastic approximation and coupling machinery underlying that published theorem.

Lemma 2 is valid. From unit counts, prescribe exactly \(n_e-1\) choices of each edge, along with an endpoint mark. Every factor in this finite sequence has strictly positive probability. The terminal state is exactly the requested integer vector. The Markov and Poisson memoryless properties give the subsequent process the desired restarted law. A positive-probability failure of a tail event from the target state would therefore imply a positive-probability failure from unit counts. Finite prefixes and time shifts do not change normalized limits or divergence. This transfers almost-sure assertions only; the manuscript correctly does not infer positive attainment from every initialization.

At a limit each non-isolated vertex has an incident positive edge: the total count on its incident edges dominates its firing count, and division by time gives at least \(\lambda_v\). Thus all denominators remain positive. Because \(\alpha>1\), derivatives of zero coordinates' powers vanish; using the stated local positive-part \(C^1\) extension, the full Jacobian splits into the positive-face Jacobian and \(-I\) on absent edges. This closes the boundary-support issue.

## Universal weighted-cycle argument (pages 3–4)

I independently differentiated the potential
\[
L(a)=-\sum_ea_e+\alpha^{-1}\sum_v\lambda_v\log S_v(a).
\]
It satisfies \(F=\operatorname{diag}(a)\nabla L\). At a positive-face equilibrium, \(\nabla L=0\), so \(DF=\operatorname{diag}(a)\operatorname{Hess}L\) is similar to the symmetric matrix \(\operatorname{diag}(\sqrt a)\operatorname{Hess}L\operatorname{diag}(\sqrt a)\). Thus one positive Hessian direction suffices even if other directions are critical. The change \(y_e=a_e^\alpha\) gives a Hessian congruence because the gradient vanishes at the equilibrium.

Putting \(b_v=\lambda_v/S_v\), \(c_v=\lambda_v/S_v^2\), \(D_e=a_e^{1-2\alpha}\), equilibrium implies \(a_e^{1-\alpha}=b_u+b_v\). Direct differentiation gives precisely
\[
\alpha^2\operatorname{Hess}\Phi[w,w]
=(\alpha-1)\sum_eD_ew_e^2-\alpha\sum_v c_v\Big(\sum_{e\ni v}w_e\Big)^2.
\]
For any simple positive support cycle, put \(A_i=a_{e_i}^\alpha\). Then
\[
\sum_i D_{e_i}=\sum_i b_{v_i}(A_{i-1}^{-1}+A_i^{-1}),\qquad
c_{v_i}\le\frac{b_{v_i}}{A_{i-1}+A_i}\le\frac{b_{v_i}}4(A_{i-1}^{-1}+A_i^{-1}).
\]
The second difference is exactly \(b(A-B)^2/[4AB(A+B)]\). Extra incident edges only strengthen the first inequality. This yields \(4\sum c_{v_i}\le\sum D_{e_i}\) without uniform weights, equal rates, induced-cycle assumptions, or absence of attachments.

On an even cycle, alternating signs cancel every incident sum; all off-cycle perturbations are zero, including chords. The positive diagonal term proves instability for every \(\alpha>1\).

On an odd cycle of length \(m\), the cosine/sine pair with frequency \(\theta=\pi-\pi/m\) is cyclically consistent because \(m\theta=(m-1)\pi\) is an even multiple of \(\pi\). Their edge square sums equal one and their incidence square sums equal \(4\sin^2(\pi/(2m))\). Adding the two quadratic forms gives a lower bound
\[
[\alpha\cos^2(\pi/(2m))-1]\sum_iD_{e_i},
\]
positive exactly in the claimed sufficient range. At least one direction is positive. The universal argument works for every finite cycle length; the finite controls are corroboration, not the proof.

Every finite nonforest contains a simple cycle. For odd \(m\ge3\), the maximum threshold is the triangle's \(4/3\). Also \(\mathbf1^TDF=-\mathbf1^T\), so any positive-eigenvalue eigenvector is mass-tangent; no spurious radial instability has entered.

For the equal-rate unit-weight triangle, the Jacobian's eigenvalues are \(-1\) and \(3\alpha/4-1\) twice. Therefore the interior equilibrium is strictly stable for \(1<\alpha<4/3\), and the published attainment theorem supplies the stated positive-probability obstruction. At \(4/3\), the transverse eigenvalues are zero; neither this attainment argument nor strict instability determines the outcome. The manuscript explicitly respects that limitation.

## Equal-rate whisker argument (pages 4–6)

After common-rate normalization, an edge has weight \(a=q+r\), with endpoint choice probabilities \(q,r\in(0,1]\). The diagonal Jacobian condition is
\[
(q^2+r^2)/(q+r)\ge 1-1/\alpha.
\]
This follows from negative semidefiniteness of the symmetric similar Jacobian, whose diagonal entries equal those of the original Jacobian. It is used only as a necessary condition.

The least-weight argument is correct: if a minimum-weight positive edge has no leaf endpoint, each endpoint has a competitor of at least its weight, so \(q,r\le1/2\), contradicting the diagonal condition for \(\alpha>2\). A leaf endpoint contributes exactly one, hence every edge in that component has weight at least one.

For an internal edge with \(a\in[1,3/2]\), each endpoint has a competitor of weight at least one, so \(q,r\le s_\alpha(a)=a^\alpha/(1+a^\alpha)\). Convexity gives \((q^2+r^2)/a\le f(a,s_\alpha(a))\), where \(f(a,s)=[s^2+(a-s)^2]/a\). Feasibility ensures \(s\ge a/2\), exactly the domain on which \(f\) increases in its second argument.

For \(3\le B\le7\), the claimed \(1/2\le s_B(a)/a\le2/3\) holds throughout \([1,3/2]\). The lower bound reduces to \((a-1)(1+a-a^2)\ge0\). The upper bound follows from \(R(a)=2a^7-3a^6+2\), with derivative \(2a^5(7a-9)\) and minimum \(52763/823543>0\). Differentiating \(f(a,s_B(a))\) gives \(1-2z^2+2(2z-1)s'_B(a)\ge1/9\). All monotonicity directions in the subsequent comparison are correct.

I independently recomputed every power cap, value and positive margin in all five closed intervals covering \([17/4,7]\). In particular the smallest displayed margin at the left endpoint is still strictly positive, \(1/1734\); the weak inequality \(\alpha\ge17/4\) is justified. Both fractional-power caps are reduced to exact integer-power inequalities, not floating-point estimates. All cap probabilities lie above \(3/4\), so the final second-argument monotonicity is valid.

For the unbounded tail \(\alpha\ge7\), setting \(a=1+r_0\) yields \(h(r_0)=\alpha r_0^2-(\alpha-1)r_0+1\ge0\) with \(r_0\in[0,1/2]\), while \(h(1/2)<0\). Therefore \(r_0\) is no larger than the smaller root. The exact constant \(C=3-\sqrt2\) obeys \(C^2+C=7(C-1)\) and \(h(C/\alpha)=-(C-1)(1-7/\alpha)\le0\), giving \(r_0\le C/\alpha\). The Taylor-plus-geometric estimate \(e^{8/5}\le510973/103125<6\) is correct, so \(a^\alpha\le e^C<6\le\alpha-1\). Both endpoint probabilities then lie strictly below \((\alpha-1)/\alpha\), contradicting their required weighted mean. This is a genuine all-\(\alpha\) tail argument.

Thus every internal edge has weight strictly above \(3/2\), and its probability at each endpoint is above \(1/2\). Two internal edges cannot meet. Internal edges form a matching, ruling out every cycle and every four-edge path. Hence components are precisely trees of diameter at most three. This argument does not depend on the new odd-cycle estimate, as the paper states.

## Primary attribution and prior bound (pages 6–7)

The four primary bodies are retained with URL/version/hash in `source_binding.json`:

- HHK 2023, published *Nonlinearity*36,3013–3042: Theorem1, Proposition1 and even-cycle Lemma2. Exact model and hypotheses match.
- Van der Hofstad–Holmes–Kuznetsov–Ruszel 2016, published *Annals of Applied Probability*26,2494–2539: uniform odd-cycle threshold, triangle obstruction and stable attainment are prior results. Their formula matches the independently derived triangle eigenvalues.
- Holmes–Kleptsyn 2017 author manuscript, title page dated March2017: Theorems2–3 and Section5.1 Lemmas5–8. The manuscript's least-weight/champion attribution is appropriate. The proof's actual constant is \((9/4)(e^{9/4}+1)\), rather than an intrinsically necessary25.
- Oberwolfach Reports12/2023, Kleptsyn contribution printed653–655: the requests to improve2 and25 are separate from the stronger suggested sharpness at4/3.

The prior-24 bridge is valid: the old split requires \(\alpha>81/4\), and the exact exponential upper bound gives \((9/4)(e^{9/4}+1)<189/8<24\). At \(\alpha>24\), large edges exceed \(29/16>3/2\), so the matching argument and the published stochastic bridge yield whiskers. `prior24_fresh_arithmetic.json` records the independently computed rational bound. This supports the paper's careful credit and prevents calling17/4 the first possible numerical improvement of25. No exhaustive novelty conclusion is inferred from this bounded interface review or from the replay's historical-status checks.

## Reproducible checks and limits of computation

`fresh_controls.py` imports no submitted helper and passed87 exact checks. It verifies the Hessian and incidence identities, closed exponent-interval arithmetic, tail constants, triangle spectrum/endpoint signs, and five fresh rational equilibrium constructions with a weighted five-cycle, chord and pendant at \(\alpha=1+1/k\), \(k=2,\ldots,6\). Those constructions use arbitrary positive vertex \(b_v\), set \(a_e=(b_u+b_v)^{-k}\), then \(\lambda_v=b_vS_v\); each equilibrium equation and the positive odd-cycle Hessian trace is checked exactly. These finite cases do not establish the universal theorem.

One initial reviewer assertion compared expanded and factored SymPy expressions structurally. It was corrected to compare their expanded difference; the mathematical identity was true and no manuscript or supplied source was changed. This was a control-harness representation issue, not a paper defect.

After inspecting the called code, I replayed the public `verification/run_checks.py` in an unmodified isolated copy with the external manifest hash supplied. All nine runs (forest, whisker, prior24 in normal, `-O`, and `-OO` modes) passed, including13 deliberately false-control rejections per mode across forest/whisker. The runner pins complete typed JSON outputs and verifies all44 manifest payloads plus its manifest, as well as unchanged source/copy bytes. `published_replay.json` and its receipt retain the complete output and runtime.

The first attempted runtime `/usr/bin/python3` exited69 due to the host's unaccepted Xcode license before executing the verifier. That attempt is preserved. The unchanged verifier then completed with Python3.12.14 from an existing runtime. No license, source or system configuration was changed. The full historical private-capture custody programs are outside the public portable replay and were not represented as rerun.

## Final assessment

The strongest verified result is the exact full Theorem1 in its stated finite simple loopless WARM model, together with the weighted-cycle instability theorem and the strict triangle obstruction below4/3. No remaining proof gap was identified within that scope. The stochastic imports remain ordinary published dependencies, not independently re-proved foundational results. Priority, human peer review, formal verification, infinite/noninteger/zero-edge extensions, the equality case4/3 and the sharp whisker conjecture are not certified. Follow-up proposal: none added; this review does not turn the stated open range into a new research conjecture.
