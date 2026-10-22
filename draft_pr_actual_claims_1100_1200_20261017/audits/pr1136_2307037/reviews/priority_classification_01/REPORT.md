# Independent priority-classification audit: PR1136 / 2307037

Audit date: 2026-10-17 UTC. Source PR created 2026-10-10; supplied exact source head `cbbe7826cca914588018c840ba99c6b7a59fa7f5`. This is a bounded independent audit, not a historical first-priority certificate. No other current priority report was read. No outside person was contacted. No repository reference, index, PR, tracker, manuscript, or release was changed by this auditor.

## Finding and recommendation

**The submitted exact-target deduction passes this independent bridge check. The inspected EH1995 and LP2009 statements are generic inputs; neither inspected body records the full fixed-area/all-radii squared-pole assertion. Their conjunction is logically sufficient after the explicit exterior-field and localization deductions below. That logical implication does not, by itself, establish that a full-target solution was historically recorded before the source PR.**

A bounded recommendation is therefore possible: treat this as a correct, fully attributed deduction/application of established results, with historical novelty and first priority unresolved. Do not label it an independently established new sharp operator estimate or a new quadrature-existence theorem. Conversely, do not label it an identified older full-target solution merely because its ingredients predate it. A classifier using `prior_full` to mean *a recorded earlier full target theorem or a recorded complete target criterion and bridge* has no such witness from this audit. If a classifier instead defines `prior_full` to include every previously unrecorded elementary corollary of old theorems, the EH+LP implication below qualifies under that broader definition; that is a definition of classification, not evidence of historical recognition.

The word **additional** is justified for the target-specific bridge. The word **historically new** is not established. Search failure and the historical open-problem label are not used as novelty proofs.

## Exact claim and success criteria

For every finite list of arbitrary complex points, including repetitions, and positive real weights of sum one, let

\[
g(z)=\sum_j\lambda_j(z-z_j)^{-2}.
\]

The quantifiers are

\[
\exists C<\infty\ \forall g\ \exists S(g),\ |S(g)|=\pi\ \forall R>1:
\quad\int_{D_R\setminus S(g)}|g|\,dA\le 2\pi\log R+C.
\]

The same set must serve all real radii. It must have exact area, with no restriction on pole placement or pole separation. A proof for each radius with a separately chosen set, a result only for poles in a bounded disk, or an unspecified constant depending on the poles fails this test. The submitted deduction achieves the stronger compact-set conclusion and the universal constant \(C=\pi(\log 2+e^{-1})\).

The primary target was freshly checked at printed pp.171-172 (PDF pp.172-173) of [HL v2](https://arxiv.org/pdf/1809.07200v2). HL credits Baernstein and says the assertion would imply its preceding area-distortion problem. The neighboring update credits EH for the preceding problem; it is not an assertion that the squared-pole problem is equivalent to that problem. The update's report of no communicated progress is historical testimony, not a mathematical or priority inference.

## What the old primary statements supply

**EH1995.** The displayed consequence following Theorem 1, printed p.2794, gives

\[
\int_{\Delta\setminus E}|T1_E|\,dA\le |E|\log(\pi/|E|)
\]

for measurable \(E\subset\Delta\), with ambient compact set \(\Delta\) of capacity one and \(T=-\pi^{-1}\mathrm{pv}\int(\cdot)/(w-z)^2\,dA(w)\). The disk is allowed. Its proof concludes on p.2797. This was visually verified in the scanned original. The theorem estimates an already chosen indicator; it neither assigns the target poles an area-\(\pi\) set nor treats an arbitrary far-away portion of that set within a small observation disk. [EH primary PDF](https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf).

**LP2009.** Definition (4), Proposition 2.12, Corollary 2.13, Lemma 2.15 and Lemma 6.1 supply bounded smash sums containing the input disks, null boundary, additive area and associativity. Proposition 6.6 on printed p.58 supplies the superharmonic quadrature inequality for balls of arbitrary positive volumes at arbitrary specified points. Applying it to both signs of a harmonic test gives equality. The proof on p.59 cites Sakai's obstacle result. No connectedness or disjointness hypothesis is present. This constructs the target measure's area representation; it provides no absolute-value Beurling integral estimate or logarithmic all-radii bound. [LP May 1, 2009 primary manuscript](https://lionellevine.github.io/scalinglimit.pdf). The same Proposition 6.6 was freshly checked in the [versioned v2 body](https://arxiv.org/pdf/0712.3378v2); [arXiv metadata](https://arxiv.org/abs/0712.3378v2) dates that version to 2009-05-02, so the by-2009 logical-sufficiency claim does not depend only on an undated current author URL.

Neither primary body contains a recorded squared-pole target application in its theorem statements or inspected proof context. Full-text searches of the downloaded bodies for the target names/phrases support, but do not independently prove, that reading. EH's sharp indicator estimate and LP's quadrature-domain theory deserve their existing attribution. Earlier partial-balayage antecedents make it especially unsafe to attribute the construction to this PR.

## Independent complete bridge

This derivation is included to distinguish actual sufficiency from a vague claim that an old theorem ought to apply.

### 1. Fix the set before choosing a radius

Combine any equal poles by adding their positive weights. For each distinct pole let \(B_j\) be the open disk of area \(\pi\lambda_j\) centered at \(z_j\), and let \(\Omega\) be their iterated smash sum. For the relevant indicator sums, the density is bounded and compactly supported, continuous off a null boundary, and takes only nonnegative integer values. Thus LP's density gap holds with any fixed \(0<\eta<1\). The regularity and mass propositions may be iterated. Consequently

\[
B_j\subset\Omega,\qquad \Omega\text{ bounded and open},\qquad
|\partial\Omega|=0,\qquad |\Omega|=\sum_j\pi\lambda_j=\pi.
\]

Set \(S=\overline\Omega\). This is compact, has area exactly \(\pi\), contains a neighborhood of every pole, and is independent of \(R\).

For any \(z\notin S\), the complex-valued function \(h_z(w)=(w-z)^{-2}\) is holomorphic on a neighborhood of \(\overline\Omega\) and bounded there. Its real and imaginary parts are integrable harmonic tests. Applying both-sign quadrature to each part gives

\[
\int_\Omega (w-z)^{-2}\,dA(w)
=\pi\sum_j\lambda_j(z_j-z)^{-2}=\pi g(z).
\]

Therefore \(T1_\Omega(z)=-g(z)\). This holds on every component of \(\mathbb C\setminus S\): the test's only singularity is at the external point \(z\), regardless of whether that point lies in a bounded hole. At each such point all integrals are ordinary absolutely convergent integrals. No differentiating across the boundary or appealing only to an expansion at infinity is needed.

### 2. Localize without moving the fixed set

For measurable \(E\subset D_L\) with \(a=|E|\), change variables \(z=L\zeta\) in EH. The kernel's degree minus two cancels its input-area scaling, and the output integral contributes \(L^2\). Hence

\[
\int_{D_L\setminus E}|T1_E|\,dA\le a\log(\pi L^2/a).
\tag{A}
\]

Choose an arbitrary real \(R>1\), put \(L=\sqrt2 R\), \(E=\Omega\cap D_L\), \(F=\Omega\setminus D_L\), and \(a=|E|\in[0,\pi]\). The first part of the field obeys

\[
\int_{D_R\setminus S}|T1_E|\,dA\le a\log(2\pi R^2/a),
\tag{B}
\]

because \(D_R\setminus S\subset D_L\setminus E\). The estimate is compatible with the ordinary exterior values: the standard \(L^2\) transform and the kernel integral agree off the closed support. Null sets do not affect the area integral.

For \(w\) with \(\rho=|w|>R\), rotation followed by the Poisson-kernel angular integral yields

\[
\begin{aligned}
\int_{D_R}|z-w|^{-2}\,dA(z)
&=\int_0^R\frac{2\pi r}{\rho^2-r^2}\,dr\\
&=\pi\log\frac{\rho^2}{\rho^2-R^2}.
\end{aligned}
\tag{C}
\]

For \(w\in F\), \(\rho\ge\sqrt2R\), so this is at most \(\pi\log2\). The positive separation \(L-R\) justifies the kernel integral for \(T1_F\) throughout \(D_R\); Tonelli applies to its nonnegative absolute majorant. Therefore

\[
\int_{D_R\setminus S}|T1_F|\,dA
\le\pi^{-1}\int_F\int_{D_R}|z-w|^{-2}\,dA(z)\,dA(w)
\le(\pi-a)\log2.
\tag{D}
\]

Linearity off \(S\), the triangle inequality, (B) and (D) now give

\[
\begin{aligned}
\int_{D_R\setminus S}|g|\,dA
&\le a\log(2\pi R^2/a)+(\pi-a)\log2\\
&=2a\log R+\pi\log2+a\log(\pi/a)\\
&\le2\pi\log R+\pi\log2+\pi/e.
\end{aligned}
\]

The final inequality uses \(a\le\pi\), \(\log R>0\), and \(t\log(1/t)\le1/e\) for \(0\le t\le1\). At \(a=0\), use the continuous entropy value zero; no division by zero remains. At \(a=\pi\), the far term vanishes. Because \(R\) was arbitrary and \(S\) was fixed first, every radius is covered by one set. Arbitrarily distant poles are covered by the far estimate; colliding poles are covered by the initial merging. This completes all quantifiers and proves finiteness.

### 3. Boundary and coefficient check

For the single pole \(g(z)=z^{-2}\), every area-\(\pi\) set leaves at least \(2\pi\log R\) of integral in \(D_R\): the radial decreasing integrand is minimized by removing \(D_1\). This can be checked directly by exchanging any removed area outside \(D_1\) with unremoved area inside it. The inside values are at least one; outside values are at most one. Thus the leading coefficient cannot decrease with any finite absolute additive constant. The submitted proof's additive constant is an explicit adequate value; no optimality of it follows.

## Mechanism and priority interpretation

The substantive old ingredients are: sharp indicator entropy control and positive-mass quadrature construction. The additional bridge consists of testing the harmonic identity with the squared Cauchy kernel, and splitting a fixed quadrature set at \(\sqrt2R\) to apply the indicator estimate locally while bounding distant mass directly. The latter localization actually applies to every bounded area-\(\pi\) set; its use in the atomic rational-function problem is the target-specific application.

This mechanism does not transfer the central difficulty to an unproved theorem: all invoked hypotheses and the complete remaining deduction are displayed above. It also shows that the target is a logical consequence of established pre-PR mathematics by 2009 at the latest. **Logical availability by 2009 and a recorded historical solution by 2009 are different claims.** The proof establishes the former; this bounded literature audit does not establish the latter or its negation. The shortness of a new application does not prove it was known, and failure to locate that application does not prove it was new.

## Search findings and exact remaining gap

The actual 40-query ledger and direct primary-source opens are in `QUERY_LEDGER.json`. General-web and domain-limited queries covered the problem number, Baernstein attribution, squared-pole wording, fixed-area wording, the EH/LP combination, quadrature plus exceptional-set language, and Fuchs-Macintyre's cited title. Most exact-target searches returned only the problem text or irrelevant matches. No pre-2026-10-10 primary theorem with every target quantifier was identified.

The cited Fuchs-Macintyre DOI was located, but its original full body was not successfully opened here; it is an explicit coverage limitation, not an inspected negative result. The primary 2006 Anderson-Eiderman body was opened as a forward-citation lead: its stated theorems concern first-order Cauchy sums and Hausdorff-content level sets, not the target's second-order area integral. It is not a full-target witness. The author-hosted Eremenko publication list was opened as a discovery index; that is not a complete citation search. A 1992 meeting-program hit for Leung's *On a fixed area problem* is only a title-level lead; no mathematical identification of that talk with this target was obtained here. These leads should remain separate from verified prior art.

No claim about unseen paywalled papers, informal knowledge, unindexed records, all citations of EH/LP, all quadrature literature, or an exhaustive pre-cutoff corpus is supported. A historical `prior_full` conclusion would require a dated primary theorem/criterion and a checkable bridge covering unrestricted positive weights, repeated complex poles, exact area, one set, all real \(R>1\), and an absolute constant. A certified first-priority conclusion would require substantially stronger historical coverage than this audit supplies.

The route 'HL says open, therefore this is novel' is rejected. The route 'the old ingredients imply it, therefore an earlier full solution was recorded' is also rejected. Both omit the historical fact at issue.

## Checkpoint and handoff

Strongest verified result: the complete exact-target bridge above, with the stated constant and all boundary cases. Mathematical gap found: none in this bridge. Historical gap: whether this bridge or another full-target solution was recorded before 2026-10-10. Completion of this scoped independent classification audit: 100%; completion of global historical priority certification: not estimable from this bounded search.
