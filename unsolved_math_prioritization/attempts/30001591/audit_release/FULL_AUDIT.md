# Independent audit of the borderline soliton packet

Problem 30001591 / OWR-4429-002, queue rank 978. Audit date: 7 October 2026.

## Verdict

The original PDE question remains **unsolved, with five approaches completed out of five**. The packet contains substantial, correctly delimited partial results. Its original Section 5 has one genuine hypothesis error: strict increase of a C² potential does not imply that its derivative is positive at a proposed turning point. Without that derivative condition, the claimed finite-time reflection can fail. The supplied correction explicitly assumes a′>0 in Section 5 and includes a counterexample demonstrating the need for this repair.

The corrected mathematical partials are accepted at the level of an independent AI-assisted mathematical audit. This is neither human peer review nor formal verification, and it establishes no novelty or exhaustive literature claim. The original bytes are preserved. Two additional edits make existing dependencies explicit: boundedness of a in the cubic compactness proof, and the separation between an energy-determined scale and a center-velocity law.

Original frozen inputs:

- AUTHOR_MANIFEST.json SHA-256: ce4ff19beb1fa50a1ba6f504bd1373943b355171e932f39ba1a4770ccbf7ad30
- PARTIAL_RESULTS.md SHA-256: 30d352188a97a117b29079ff714acdae753ef4f5bbdb5d350d80662f0cb08115

The corrected proof is PARTIAL_RESULTS.corrected.md. CORRECTION.patch is an exact unified diff against the frozen original. This correction is an audit repair, not a sixth research approach.

## Primary problem and source reconciliation

The target equation is

u_t + (u_xx − λu + a(εx)u^m)_x = 0 on R × R, m∈{2,3,4}.

The solution is incoming in H¹ to Q(x−(1−λ)t), where Q solves Q″−Q+Q^m=0 and is centered, positive, and decaying. The order of limits is fixed positive, sufficiently small ε, followed by t→+∞. Reversing these limits, allowing ε to depend on the observation time, or analyzing only a finite interaction interval does not answer the question.

The corpus statement specifies smooth positivity and limiting values 1 and 2; that alone is broader than the source theorem class. The official Oberwolfach contribution places the equality question in Remark 1, printed page 2405. Its Theorems 4 and 5 treat strict inequalities on opposite sides of the threshold; Theorem 6 also excludes equality. Page 2405 was independently viewed to check the transmitted amplitude 2^(−1/(m−1)). The report's bibliographic year is 2010 and its publication date is 2 March 2011. [Official report](https://ems.press/journals/owr/articles/4429), [official PDF](https://ems.press/content/serial-article-files/46300).

The detailed manuscript arXiv:1009.4905v1 assumes a∈C³, 1<a<2, a′>0, exponential approach at both ends, exponential bounds on derivatives 1–3, and |(a^(1/m))‴|≤K(a^(1/m))′. Equations (1.23), (2.19), and (3.1) give the threshold and reduced system. Theorems 1.3–1.4 exclude equality; Remark 1.13 discusses it without proof. Proposition 2.1 states the H¹ energy and mass laws, and Proposition 2.3 supplies incoming existence and uniqueness at positive λ, including the critical value. Lemma 3.1 uses finite initialization; Remark 3.3 identifies the degeneration of the useful escape-time bound. [Manuscript](https://arxiv.org/pdf/1009.4905), [journal record](https://doi.org/10.1137/100809763).

The later arXiv:1107.5328v1, Theorems 1.2–1.4, explicitly excludes λ=λ̃. Theorem 1.4 gives a lower bound for the outgoing H¹ defect for fixed off-threshold λ; Remark 1.3 discusses its exponent. Remark 1.1 still identifies equality as unresolved at that time. The published CMP abstract independently retains the exclusion. It supplies no critical-parameter classification. [Manuscript](https://arxiv.org/pdf/1107.5328), [publisher abstract](https://link.springer.com/article/10.1007/s00220-012-1463-6).

All three local PDF hashes and page counts match the recorded metadata. The complete author manuscripts and relevant official-report pages were inspected. The final SIAM and CMP full-text proofs were not independently inspected; publisher records and the CMP abstract were checked. Failed versioned arXiv abstract retrievals were resolved by inspecting the accessible PDF routes, whose first pages identify v1. The audit does not promote the bounded literature search into proof of present global openness.

## Threshold and normalization checks

Set q=(5−m)/(m+3), p=4/(m+3), α=2/(m−1)−1/2=q/(1−q), and β=1/(m−1)−1/2. Each q lies in (0,1), and α>0. On λ∈(q,1), the logarithmic derivative of λ((1−q)/(λ−q))^(1−q) is q(λ−1)/(λ(λ−q))<0. Its endpoint values are +∞ and 1, whereas 2^p>1. Thus the specified critical parameter is unique.

The quartic value λ̃=1/4 is exact. Raising the positive-base threshold equation to the seventh power gives λ^7(6/7)^6=16(λ−1/7)^6; substitution verifies it without a numerical root choice. Independent exact brackets are 0.63<λ̃<0.64 for m=2 and 0.42<λ̃<0.43 for m=3. Integer powering introduces no ambiguity because the original bases are positive on the asserted interval.

The amplitude A^(−1/(m−1)), mass normalization M(v)=∫v²/2, energy sign, and constant-coefficient speed c−λ are all consistent. A negative transmitted amplitude exponent is essential.

## Approach 1 and the exact critical auxiliary orbit

The invariant H(C)/a(εP)^p is correct: multiplication of H′/H by the reduced C equation cancels pε(a′/a)(C−λ). The relevant interval is 0<C<λ/q, where H is positive. H attains its unique maximum at C=λ; at the critical parameter H(1)=1 and H(λ)=2^p. Consequently the upper branch is uniquely defined for every finite P by H(C*)=a(εP)^p and lies in (λ,1).

The implicit-function theorem applies at each finite P because C*>λ, even if a′ vanishes there. C* is C¹, the scalar field C*(P)−λ is locally Lipschitz and strictly positive, and separation gives a solution unique up to time translation. Its speed is bounded above by 1−λ. Neither spatial infinity can be reached in finite time, and a finite limiting P would leave a positive limiting speed. Hence it exists for all real time and P→±∞ at the respective ends. Strict increase of a makes C*(P) strictly decreasing as a function, although its derivative can vanish at individual points. This part does not require a′>0 everywhere.

At the incoming end, H′(1)≠0. The exponential upper bound on a−1 gives an integrable correction to dt/dP−1/(1−λ), so the claimed finite phase limit and its removal by time translation are justified.

At the outgoing end, H″(λ)/H(λ)=−q/[λ²(1−q)] gives the square-root potential-tail relation with coefficient pλ²(1−q)/q. Under the separately stated exact tail equivalent 2−a(r)∼A e^(−κr), differentiating exp(κεP/2) gives a derivative converging to κεD/2>0. Cesàro integration then yields the time equivalent, the logarithmic center asymptotic, and P′∼2/(κεt). No derivative equivalent for a′ is required. The exact tail equivalent is stronger than the source's mere upper exponential estimate, and the constants are allowed to depend on fixed ε.

Accepted conclusion: an exact auxiliary-ODE orbit and conditional logarithmic escape. No critical PDE approximation is established by this reasoning.

## Approach 2 and functional analytic details

For a real stationary H¹ distributional solution U, the differentiated stationary expression is zero, hence U″−λU+a(εx)U^m is a constant distribution. Every term is in H⁻¹: U″ is the derivative of an L² function, and boundedness of a together with H¹(R)⊂L∞(R) gives U^m∈L². A nonzero constant is not in H⁻¹. Indeed, for a smooth scaled plateau φ(x/R), its integral grows as R and its H¹ norm as R^(1/2), contradicting a uniform dual bound. The constant therefore vanishes.

The resulting ODE gives U″∈L² and hence U∈H². Both U and U′ are H¹ functions, so their continuous representatives tend to zero at both infinities. Since the ODE right-hand side is continuous, U is C². For even m, a negative value forces a strictly negative global minimum because U vanishes at infinity. At that minimum λU−aU^m<0, contradicting U″≥0. For cubic m, no sign deduction is needed.

Integration against U′ is legitimate: U″U′ and UU′ are L¹, bounded a′ times U^(m+1) is L¹, and the boundary terms involving U, U′, and aU^(m+1) vanish. The resulting integral of a′U^(m+1) is zero. It is nonnegative and, with a′>0, positive wherever U≠0. Thus U=0. This stationary ODE sign argument asserts no positivity preservation for time-dependent gKdV.

For m=3, bounded a makes the energy continuous on H¹. More explicitly, polynomial factorization, H¹→L∞, and Cauchy–Schwarz control the quartic-energy difference on any bounded H¹ set. Bounded a′ similarly makes F(v)=∫a′(εx)v⁴ continuous. Since a′>0 everywhere, F(v)>0 for every nonzero v. If the forward orbit had compact closure K in H¹ and conserved positive energy, then 0∉K and min_K F>0. The integrated mass identity would drive nonnegative mass below zero in finite time, a contradiction.

The correction makes bounded a explicit in the compactness lemma, matching the problem/source class rather than silently using it in the continuity step. Energy conservation and the integrated mass law are assumed there. For the source-class incoming solution, Proposition 2.1 supplies those flow identities and Proposition 2.3 confirms E=(λ−q)M(Q)>0 at critical λ. They are an external PDE dependency, not a consequence of the finite algebra checks.

Accepted conclusions: no nonzero real stationary H¹ profile under the stated assumptions, and no precompact unshifted forward H¹ orbit for the cubic positive-energy solution. Neither excludes a profile drifting to infinity, compactness modulo unbounded translations, radiation, or nonstationary recurrent dynamics. Extending the mass-sign argument to sign-changing even-power solutions would be invalid.

## Approach 3 and conserved energy

For smooth decaying solutions, the energy variational derivative is −F, while u_t=−F_x. Thus dE/dt=∫FF_x=0. The mass calculation gives −ε/(m+1)∫a′u^(m+1), with the stated sign and factor. These formal computations require their indicated decay and do not by themselves justify an H¹ flow limit.

Q_c decays exponentially with its derivatives, so the two Pohozaev integrations, including the xQ_c′ multiplier, have no residual boundary term. Solving the resulting two linear equations gives K=(m−1)cL/(m+3) and N=2(m+1)cL/(m+3). The energy therefore equals A^(−2/(m−1))M(Q)c^α(λ−qc).

The derivative of c^α(λ−qc) is αc^(α−1)(λ−c). Its maximum on positive c is uniquely attained at λ; beyond λ/q the energy expression becomes negative, and there is no omitted high-scale positive-energy root. At the threshold, E_2(λ)=E_1(1)>0.

For a hypothetical outgoing H¹-pure translated soliton whose center tends to +∞, change variables to the centered profile. Bounded a and pointwise convergence a(ε(y+ρ))→2 permit dominated convergence against the integrable profile power. The H¹ error gives an o(1) energy error by the same continuity estimate. Energy therefore forces c=λ. For clarity, the correction does not infer a center-velocity law from this scalar identity: the phrase positive terminal speed uses the usual additional relation speed=c−λ. Establishing that relation for a given moving-center decomposition is a kinematic/PDE step.

Under the expressly conditional energy-decoupled radiation definition, D=E_2(λ)−E_2(c), with the stated positive quadratic coefficient and O(|c−λ|³) remainder. Taylor expansion is legitimate in a neighborhood of the positive number λ. Both algebraic branches are available for small positive D. On the left, f(0+)=0<f(1)<f(λ), strict increase below λ and strict decrease above it give exactly the two positive roots c_R∈(0,λ) and 1.

Accepted conclusions: pure transmitted scale restriction, quadratic energy degeneracy, and reflected-scale algebraic compatibility. Neither a radiation decomposition nor dynamical branch selection is proved.

## Approach 4 and signed integrals

The conserved quantity is ∫u, when integrability and boundary fluxes allow it; it is not ∫|u|. H¹ incoming convergence alone does not identify its value. Incoming L¹ convergence, combined with the stated conservation, does identify it as ∫Q.

The scaling exponent β=(3−m)/(2(m−1)) gives the three outgoing critical ratios. The quadratic and cubic transmitted ratios are strictly below one; the quartic ratio is exactly one because λ̃=1/4. The reflected ratio c_R^β differs from one only for m=2,4. Therefore the exclusions under simultaneous outgoing H¹ and L¹ purity, incoming integral identification, and integral conservation are correct, including both exceptions.

The broad-tail construction has fixed signed integral b and H¹ norm squared b²[L^(−1)∫φ²+L^(−3)∫(φ′)²]. Translation preserves both. Independent controls use an explicit compactly supported C¹, H¹ polynomial tail with integral one and exact coefficients ∫φ²=5/7 and ∫(φ′)²=15/7. The packet's smooth compactly supported version follows from any smooth normalized bump. These are functional-analytic counterexamples to an inference, not constructed PDE radiation.

Accepted conclusion: conditional signed-integral obstructions and a genuine obstruction to deriving them from H¹ convergence alone. No extra L¹ property is silently supplied to the critical incoming solution.

## Approach 5 and the required repair

The perturbed-invariant identity is exact under the stated differentiability and strip restrictions. The coefficient multiplying r_C is H′/H and the r_P contribution has a minus sign. A pointwise error bound integrated over an infinite interval gives no finite accumulated bound without integrability. Even a convergent signed integral can change the limiting invariant. These observations neither prove such errors occur for the PDE nor bound them.

For J<1, the upper inverse branch exists for every P because Ja(εP)^p<2^p. Its C values stay in a compact subinterval of (λ,λ/q), bounded away from the strip endpoints for each fixed J>0. Hence its positive speed has a positive terminal limit and separation gives transmission. For J>1 but J<2^p, the equation a(εP*)=2J^(−1/p) has a unique finite solution. If a′(εP*)>0, expansion of a at P* and the nondegenerate maximum of H give C−λ comparable to sqrt(P*−P), whose reciprocal is integrable. C′ at the turning point is negative, so the smooth ODE crosses to the lower branch. Thereafter C<λ stays separated from λ after any fixed post-turn time and P→−∞; its lower terminal scale is the unique root H(c)=J in (0,λ). Positivity of a′ everywhere is a sufficient source-aligned assumption used by the corrected statement.

### Counterexample under the original weaker hypothesis

Let L(s)=1/(1+e^(−s)), choose any a0∈(1,2), and let b=log((a0−1)/(2−a0)). Define

a(r)=1+L(r³+b), J=(2/a0)^p.

This a is C∞ and strictly increasing, with limits 1 and 2 and a′(0)=0. Its central expansion is a(r)=a0+B r³+O(r⁶), where B=(a0−1)(2−a0)>0. At P*=0, J a0^p=2^p=H(λ). Along the upper branch as P↑0,

H(λ)−H(C) ∼ [H(λ)q/(2λ²(1−q))](C−λ)²,

H(λ)−J a(εP)^p ∼ Jp a0^(p−1)B ε³(−P)³.

Therefore C−λ∼K(−P)^(3/2) with K>0. The arrival-time integral diverges as ∫_0^δ s^(−3/2)ds. The orbit approaches the finite equilibrium (λ,0) as t→∞ and does not reflect. Smooth uniqueness also prohibits reaching that equilibrium at a finite time from a distinct point. Taking a0→2 makes J→1+, so the failure occurs arbitrarily near the critical invariant. This example violates the source's a′>0 hypothesis; it refutes only the original overbroad authored statement, not the source theorem.

With the repair, the squared terminal-speed perturbation coefficient 2λ²(1−q)/q is correct. Finite initialization at C0=1 gives J=a(εP0)^(−p)<1, so the reduced orbit transmits even when λ=λ̃. Expanding 1−J∼p(a(εP0)−1) gives the stated finite-start coefficient. The source's finite-start orbit therefore cannot be identified with the exactly incoming critical normalization. The final uncertainty timescale is an asymptotic comparison of ODE velocity magnitudes under the exact-tail assumption, not a uniform numerical theorem or PDE prediction.

## Independent controls and packet integrity

The original 43 algebra controls and three deliberate wrong-identity rejections were independently replayed. Its verifier succeeded in ordinary and optimized Python. Because that verifier launches its child using −B without forwarding −O, the audit separately ran check_algebra.py directly in both modes and compared its bytes. Both results agree with the frozen CHECK_RESULTS.json.

The independent script reconstructs the invariant through integer powers G(C)/a(εP)^4, solves the Pohozaev linear system, directly differentiates the explicit soliton, and checks threshold, energy, tail, flat-turning, and constant-distribution controls. It passes 78 exact controls and rejects 9 deliberately wrong mathematical controls in both ordinary and optimized Python, with identical output. Explicit exceptions enforce failures; optimization does not remove checks. These finite checks support but do not replace the written infinite-time and functional-analytic proofs.

Independent relocation and mutation tests verify the original packet's inventory, payload hashes, and recorded replay. Changing the proof, adding an extra file, deleting the recorded result, replacing a payload by a symlink, or altering the frozen replay is rejected. Recomputing the manifest after a proof alteration illustrates an important limit: the original verifier then accepts its own new manifest. It is a consistency checker, not an authenticated trust root. This audit pins the original manifest digest externally and rejects that substitution. The audit verifier likewise requires its own published manifest hash for authenticated use.

The complete public corpus files were independently hashed and counted, and exactly one problem 30001591 was matched. Its public code is OWR-4429-002; that code is absent as a research-result key. Both corpus hashes match the metadata. The recorded revision is retained as supplied provenance, with the distinction that matching local bytes alone does not authenticate a remote revision. No raw corpus records, source PDFs, copied source text, screenshots, or private coordination files are in the audit bundle.

The five ledger entries describe five mathematically distinct approaches and are compatible with the artifact contents. Their historical first-write timestamps are author-recorded chronology, not independently established by hashes or by this audit. No reading, replay, packaging, or correction step is counted as an extra approach.

## Exact remaining gap

What remains unavailable is a fixed-ε, all-late-time analysis of the actual critical PDE solution that supplies a usable modulation/radiation decomposition, controls its accumulated signed parameter error through the degenerate threshold, and proves the relevant tail or asymptotic compactness properties. The reduced orbit, conservation identities, stationary exclusion, and finite controls do not supply that bridge.

There is consequently no accepted proof here of PDE transmission, reflection, logarithmic PDE escape, a nonzero stationary limiting state, an ε-dependent shifted threshold, or critical radiation size. Taking an endpoint in an off-threshold theorem whose constants or escape times degenerate does not repair the gap. The accepted disposition is **unsolved 5/5**, with the corrected partial results retained.
