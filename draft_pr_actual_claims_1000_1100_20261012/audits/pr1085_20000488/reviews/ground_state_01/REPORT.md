# PR1085 / 20000488: independent ground-state adversarial review

**Verdict: accept the full mathematical claims at PR head `5e23f0c801d23976830657d2eef2b32bdc7da05a`. No P0, P1, P2, or P3 defect identified. No mathematical repair required.** This is an independent AI review, not human peer review or a novelty certificate. It neither merges the PR nor publishes a release.

The exact strongest verified result is: every nontrivial connected C∞ domain with bounded symmetric difference from an upper half-space binds below the attractive Robin threshold for every coupling in ambient dimensions two and three, including overhangs and compact additional boundary components; every compact W¹,∞ graph in ambient dimensions at least four has no spectrum below the threshold at sufficiently weak coupling; and the nonzero smooth graph f=h/100 has spectrum [−1,∞) at β=1 in R⁴. The last statement is an explicit counterexample to the dimension-unrestricted universal question. Equal spectral and essential-spectral sets do not exclude embedded eigenvalues.

## Independence, custody, and full submitted scope

The complete MATHEMATICAL_REPORT was the first substantive submission read. The reconstruction in [INDEPENDENT_DERIVATION.md](INDEPENDENT_DERIVATION.md) was written before reading the inherited audit, status, README, source metadata, or manifest. Afterwards, all five remaining files and the locally captured PR body were read completely. The reviewer used only this dedicated folder; there were no candidate edits, Git mutations, service writes, external communications, or interactions with other review shards.

All six submitted files were first frozen byte-for-byte. Read-only `git show` then authenticated them against the actual candidate commit, rather than current main. [PR_BLOB_AUTHENTICATION.json](PR_BLOB_AUTHENTICATION.json) records every Git object ID, SHA256, byte count, declared pin, and equality check. In particular the full report has 14,666 bytes and SHA256 `9db488c626bad1367229603fc45eeff92be5f613c79418f0249dd25032ffe3e5`.

The actual workspace main HEAD at capture was `fa24428a4fa6930fd3df9dc1b2feb0f7c72885c9`; it is distinct from the PR head and was already dirty. [ACTUAL_GIT_CAPTURE.json](ACTUAL_GIT_CAPTURE.json) preserves the actual branch, HEAD, global status, and diff summaries without changing any Git state. Comparing the PR’s recorded base `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc` with its head gives exactly six additions under the stated attempt directory, with no other changed paths. Thus the candidate does not change QUEUE.md or unrelated entries. Those six attempt files are absent from the current main tree. [GLOBAL_CANDIDATE_COMPARISON.json](GLOBAL_CANDIDATE_COMPARISON.json) records this whole-candidate comparison. No current-main file was substituted for a PR blob.

The mathematical scope matches across the report, audit, README, STATUS, and captured PR body. MANIFEST correctly lists six members and hashes the other five; the captured body independently pins the manifest and all six files. SOURCE_METADATA contains bibliographic/provenance data and limits, with no full source bodies. The Git delta consists only of the six authored text files, so the claimed exclusion of programs, checker outputs, source copies, and images is borne out. This review creates new independent controls in its own audit folder; it does not replay undistributed author code or convert omitted numerical evidence into a proof premise. Historical accounting and human-peer-review claims are correctly limited by the text; this review does not independently reconstruct historical attempt counts.

## Original target, sign, and quantifiers

Fresh retrieval of the [canonical AIM Robin section](http://aimpl.org/shapesurface/1/) succeeded over its plain-HTTP URL. The complete visible section was read, including the introduction immediately before Problem 1.4, and the selected subsection was rendered locally from these same bytes and visually inspected. The source treats a negative boundary parameter and asks for binding below −α²; it supplies no ambient-dimension or boundary-topology restriction for Problem 1.4. Other problems in the section explicitly give dimensions when relevant. The selected question’s dimension-unrestricted reading is supported by the actual source wording; no hypothetical fixed-dimension version was silently substituted.

The standard attractive convention ∂νu+αu=0, α<0, is equivalent to ∂νu=βu, β=−α>0, and the H¹ form ∫|∇u|²−β∫∂Ω|u|². This convention gives the exact flat threshold −β². The source does not itself write out a boundary condition in the selected subsection; the review independently checks the report’s convention by integration by parts and the flat exponential mode. This avoids inferring a Robin sign merely from a parameter name.

An R⁴ counterexample at β=1 suffices to refute the unrestricted universal claim. For each prescribed β*>0 a suitably small nonzero graph supplies another counterexample. This is a geometry depending on β*, not one geometry with absence for all β. The positive fixed-n=3 theorem is additional verified scope. The candidate does not promise an arbitrary nongraph n≥4 classification, large-coupling absence, removal of embedded eigenvalues, or novelty, and those absent conclusions are not gaps in the unrestricted negative answer.

## Form realization and complete essential spectrum

The local smooth/Lipschitz trace inequality on finitely many charts covering the compact modified part, plus the flat trace inequality on the rest, gives an infinitesimally form-bounded boundary term. Therefore q is closed and semibounded, with form domain H¹. The smooth closure core is dense; Lipschitz graphs use bi-Lipschitz flattening. No Robin operator condition is placed on variational trial functions.

On H, the completed square is QH[u]=∥∇x u∥²+∥∂y u+βu∥². For the perturbed domain choose an IMS partition whose exterior factor vanishes on a neighborhood of every geometric change. Its exterior product extends to H¹(H) without a jump. Semiboundedness of the interior factor gives QΩ[u]≥−C∫K|u|². Any weakly null operator Weyl sequence at λ<−β² has bounded H¹ norm by trace coercivity. Local Rellich then forces its compact mass to zero, contradicting its negative limiting shifted energy. This excludes essential spectrum below the threshold.

For the reverse inclusion, horizontally translated and dilated tangential wave packets are supported on full unchanged vertical fibers. Multiplying by the normalized mode √(2β)e^(−βy) gives norm one and the exact Robin condition on their supported flat boundary. They are in the operator domain: integration by parts against every form test yields the weak operator equation with L² Laplacian. This supplies a rigorous alternative to assuming a global H² operator-domain characterization on all smooth domains. At λ=|k|²−β² the residual is O(R⁻¹)+O(R⁻²), and horizontal escape gives weak convergence to zero. These packets cover all [−β²,∞), including its endpoint. Thus σess=[−β²,∞); strictly lower spectrum is discrete with finite multiplicity.

## Nongraph mechanism and strict defect positivity

The independently derived identity for φ=e^(−βy) is

Q[φv]=∫Ωφ²|∇v|²−β∫∂Ω(1+ν_y)φ²|v|².

Its sign is correct: Δφ=β²φ and ∂νφ=−βν_yφ. The coefficient 1+ν_y is nonnegative for every unit normal, is zero on the unmodified lower plane, and is positive on appropriate parts of any obstacle boundary. An overhang need not have a graph parametrization for this conclusion.

The total defect Bβ is finite because its support lies in the compact altered boundary. If Bβ vanished, nonnegativity and continuity would force every outward normal to equal −e_y. Each connected boundary component would be locally a horizontal plane, globally contained in one such plane, open in that plane, and closed in ambient space. It must therefore be the entire plane. Compact agreement with H excludes every plane except y=0, and agreement at infinity plus connectedness forces Ω=H. This contradicts nontriviality, so Bβ>0. The proof correctly handles multiple boundary components; no compact closed component can have the required constant normal.

For ψ equal to one over the deformation’s projection and with gradient outside that projection, u=e^(−βy)ψ belongs to H¹: Ω is bounded below, and its upper tail is exponentially integrable. Vertical truncation beyond the changed region has vanishing error. On gradient support the fiber is exactly (0,∞), giving

Q[u]=(1/(2β))∫|∇ψ|²−βBβ.

The tangential energy tends to zero via linear cutoffs in m=1 and logarithmic cutoffs in m=2. This produces Q[u]<0 for every β>0. Combined with the independently verified essential spectrum, it gives a discrete eigenvalue for the full smooth compact-perturbation class in n=2,3.

[NEW_NONGRAPH_CONTROL.md](NEW_NONGRAPH_CONTROL.md) adds a direct analytic obstacle test: remove a ball lying entirely above the flat plane. Its outward-domain normal points into the ball, and its lower hemisphere gives Bβ≥2πa²e^(−2βc)>0 in n=3. The logarithmic trial has an explicit finite cutoff range making Q<0. Under the ball, vertical fibers have two intervals, so this test would expose a covert whole-domain graph assumption. It also gives the corresponding planar disk control.

## Graph capacity and all-function absence

For a graph the normal and surface Jacobian give (1+ν_y)dS=(√(1+|∇f|²)−1)dx. The graph transverse-mode trial identity and its capacity condition follow exactly. That condition is sufficient only; failure supplies no absence conclusion. Nonzero compact Lipschitz f has nonzero gradient on positive measure, hence a positive total graph defect.

The weak-coupling result controls all form functions. After flattening y=t+f(x), the core identity has bulk |∇xw−∇f wt|²+|wt|² and the negative trace defect. Tangential Hardy in m≥3 gives local weighted mass ≤A E_x with A=4R²/(m−2)². Vertical integration then gives T_K≤(2βA+√A)(E_x+E_t). The elementary vector inequality yields c(G)=1/[2(1+G²)] for the bulk. Upper and lower exponential bounds give

Q[u]≥[e^(−2βM)c(G)−βe^(2βM)D(2βA+√A)]E.

Hence βD e^(4βM)(2βA+√A)≤c(G) is a sufficient full-form absence criterion. It holds for all sufficiently small β for every fixed compact W¹,∞ graph. Passing to the full H¹ domain uses compact-support core density and form continuity, not globally bounded multiplication by e^(βy). This is the decisive distinction from a separable-trial-only calculation. The Hardy restriction m≥3 is respected and does not conflict with low-dimensional capacity zero.

For h=e^(−1/(1−r²)) on the unit ball, extended by zero, flatness at the support sphere gives C∞ smoothness. The bound |∇h|≤8/e²<2 gives M<1/100, G<1/50, D<1/5000 for f=h/100. At β=1 and m≥3, A≤4. The report’s absence side is <1/250 while its coercivity is >1/3. Independently, the power-series inequality e^(1/25)<25/24 gives absence side <1/480 and coercivity >1250/2501, leaving the exact positive margin 597499/1200480. No spectral discretization or numerical extrapolation is required. The flattening diffeomorphism verifies connectedness of Ω and its boundary, and the symmetric difference is bounded.

## Primary literature interfaces and provenance limits

The fresh source custody in [SOURCE_CUSTODY.json](SOURCE_CUSTODY.json) records URLs, timestamps, HTTP status, actual bytes, and hashes. AIM HTML, Exner–Minakov v1, Pankrashkin–Popoff v2, and the Trier slides exactly reproduce the submitted metadata’s retained hashes. Raw source bodies and rendered images stay in a locally ignored private directory. This fresh review does not retrofit a new retrieval claim into the historical edition, and plain-HTTP AIM provenance remains weaker than authenticated HTTPS. The web tool’s automatic HTTPS attempt returned a 502; direct canonical HTTP retrieval succeeded without bypassing certificates.

In [Exner–Minakov](https://arxiv.org/abs/1406.7624), the visually inspected PDF pages 16,17,20 show the single C⁴ boundary curve, nontrivial same-line compact-deformation hypothesis, essential threshold in Theorem 5.1, and all-coupling binding in Theorem 5.2. The report appropriately credits this standard planar precedent. The cited concave/wedge alternatives have different asymptotics and do not refute the compact same-line result. These relevant theorem pages were checked; this is not a full independent review of their entire paper.

In [Pankrashkin–Popoff](https://arxiv.org/abs/1502.00877), visually inspected PDF pages 2–4 give admissibility, bounded-curvature conditions, K∞<Kmax, and Corollary 1.6’s sufficiently-large-parameter quantifier. This is compatible with the weak-coupling graph theorem. The primary abstract currently identifies v2 and the preliminary-version comment; journal metadata does not certify equality of preprint and published bytes.

In [Lotoreichik’s 2017 talk](https://aamp.fjfi.cvut.cz/lotoreichik/Trier2017.pdf), the visually inspected physical pages 7 and 12 correspond to printed slides 9 and 15. The former makes β a graph deformation amplitude at fixed δ-interaction coupling α. The latter separates a higher-dimensional δ-interaction expectation from a Robin half-space expectation. Neither is a proved Robin theorem, and the Robin block does not restate a dimension. The candidate’s historical qualification is accurate.

The fresh primary [Barseghyan–Schneider–Zhang abstract](https://arxiv.org/abs/2609.03783) expressly adds a compactly supported magnetic field to a planar Robin operator. It does not establish the unmagnetized higher-dimensional result. Only its abstract/version metadata were checked, not its PDF or full proof.

The bounded search and these primary checks are enough to validate source interfaces and avoid obvious misattribution. They do not certify priority, novelty, current open status, or exhaustive coverage of later papers. No mathematical acceptance conclusion depends on an unverified novelty claim.

## Runnable controls and remaining gap

Run `python3 check_controls.py` from this review folder. It authenticates all six frozen candidate blobs using read-only Git, checks manifest and scope flags, proves the rational constant margin by exact fractions, probes the normal/Jacobian signs, checks linear and logarithmic trial signs, and performs 125 exact rational coercivity probes. It rejects altered report bytes, a missing member, and a fully repinned status/manifest mutation asserting embedded-eigenvalue exclusion. The finite probes guard common errors; they are not a replacement for the analytic proof. [CONTROL_RESULTS.json](CONTROL_RESULTS.json) records PASS; an optimized `python3 -O` run gives identical output, so validation does not vanish when assertions are disabled.

No required mathematical gap remains in the submitted full claim scope. No edits to the candidate are requested. The remaining limits are stated nonclaims: nongraph higher-dimensional classification, all-coupling graph absence, embedded-spectrum structure, and historical novelty. A minor descriptive observation is that the boundary identity uses the half-space’s preferred vertical direction; calling it coordinate-free means that it needs no graph or boundary chart, not that the distinguished half-space direction disappears. This does not affect any conclusion or require repair.

Completion estimate: 100% of this independent review’s assigned scope. Broader publication or priority decisions remain with the parent review and human user.
