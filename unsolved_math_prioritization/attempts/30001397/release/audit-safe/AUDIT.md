# Independent adversarial audit: elliptic conformal Hausdorff gauges

Problem ID 30001397, rank 669, OWR-4137-017. Audit date: 2026-10-04 UTC.

## Verdict

**Accept the disposition UNSOLVED, 5/5 approaches exhausted, with a minor verification-count correction and a metric-normalization clarification.** No proof or counterexample to the full exact-gauge question has been established. No fatal defect was found in the retained mathematical partials under the packet's explicit basin-attraction interpretation and stated conformal-measure hypotheses. This is an independent AI-assisted audit, not human peer review or a certification that no later resolution exists.

The fixed audit input is the 22,392-byte author ZIP with SHA-256 `5286fc55fc2227f1c10cd03742ab4a6e4d5d261a56888c8b736a5ba031a48919`. It contains 14 ZIP entries: 13 manifest-listed payloads and the manifest itself. Every payload matches its recorded byte count and digest. The original packet and all original files were preserved.

The authored verifier reproduces its saved output and passes all actual assertions. Its reported total of 8,700 is incorrect: an instrumented replay executes **7,580 assert statements**. The exponent loop visits 1,120 accepted triples and contains five assertions per triple, but adds six to its counter. Its family count must be 5,600 rather than 6,720. This is a reporting defect, not a failed identity. Independently authored checks add 87,730 exact predicate checks, all passing; these finite controls do not prove an elliptic theorem.

## 1. Primary sources and scope

The exact target was checked visually at printed p.2961 of the primary Oberwolfach report. It concerns an elliptic meromorphic map, the full Julia set, and equality with a gauge Hausdorff measure. The neighboring exponential/radial-Julia problem is separate. The source's codomain is the Riemann sphere; text extraction can lose its bar. The 2004 author's version explicitly makes its principal geometric-measure assertions in the spherical metric.

The following primary inputs were inspected directly:

- The Oberwolfach report, printed p.2961. An independent fresh EMS download matches the frozen source hash exactly.
- Kotus and Urbański, *Ergodic Theory, Geometric Measure Theory, Conformal Measures and the Dynamics of Elliptic Functions*, arXiv:2007.13235v1. An independent version-pinned fresh PDF download matches the frozen source hash exactly. Checked the critical-point convention, metric conversion, local parabolic law, regularity of the parabolic class, dimension bound, pole estimates, uniqueness/atomlessness/transitivity, vanishing Hausdorff mass, and invariant-measure finiteness criterion. Printed pp.455, 595, 601, and 609 were also checked visually.
- The author-hosted 2004 PostScript and locally converted PDF: cached bytes and hashes rechecked; the spherical-metric convention was read in its introduction. No independent journal-typeset PDF identity is asserted.
- Simmons, *On interpreting Patterson-Sullivan measures of geometrically finite groups as Hausdorff and packing measures*, arXiv:1408.4664v3. A fresh version-pinned PDF matches the frozen hash. Checked Theorem 1.1's log-gauge assumptions, Corollary 1.5, and Lemma 4.3.

Public source URLs and exact inspection locations are recorded in AUDIT_SOURCE_CHECKS.json. No source PDF, PostScript, extracted source text, screenshot, or dataset is included in the audit deliverable.

The basin-attraction qualification is important and already present in the packet. The manuscript defines its parabolic elliptic class by absence of derivative-zero critical points from the Julia set, together with existence of parabolic periodic points. The relevant convention is Crit(f) = {z : f'(z)=0}; multiple poles are handled separately. A critical point that lands exactly on a parabolic orbit can belong to the Julia set. Merely knowing convergence of its orbit would therefore not establish the narrower hypothesis. The retained conclusions are accepted in the packet's stated scope; this audit does not silently extend that scope.

Within that scope, the manuscript supports the needed regularity, an atomless unique spherical h-conformal probability, full support, full mass on transitive points, and H_s^h(J)=0. The pole-multiplicity bound makes h>1. A parabolic basin is a nonempty Fatou component, so the manuscript's implication h=2 => J=C gives h<2. The source hypotheses have not been replaced by a numerical h,p,q triple.

## 2. Regular variation and exact Caratheodory transformation

**Proposition 2 and Corollary 2.1 pass.** This is exact equality of measures, conditional on finite positive total mass, rather than a density-comparison assertion.

Here is an independent check of the essential steps. Define the Hausdorff outer measure by infima of sums g(diam U) and let the covering scale tend to zero. For a nondecreasing gauge with g(0)=0, this is a metric outer measure, hence restricts to a countably additive Borel measure. A singleton has measure zero because g(r) tends to zero. No atom is introduced by changing the metric or normalizing a finite total mass.

For fixed L>0, regular variation gives g(Lr)/g(r) -> L^h. The supremum over 0<r<=delta consequently tends to L^h as delta decreases to zero. If a map is L-Lipschitz on A, replace each covering set U by U intersect A before mapping it. Monotonicity of g then proves H^g(F(A)) <= L^h H^g(A). Applying the same argument to the inverse supplies the co-Lipschitz bound.

A C^1 conformal local diffeomorphism has positive continuous metric dilation. On sufficiently small neighborhoods, both Lipschitz constants can be made arbitrarily close to its pointwise dilation. A disjoint countable Borel partition subordinate to those neighborhoods permits addition of the two bounds. On relatively compact charts, the integrand is bounded and its oscillation can be made arbitrarily small. Squeezing, followed by exhaustion, gives

H^g(F(E)) = integral over E of lambda(x)^h dH^g(x).

This argument uses the metric dilation on both the source and target surfaces. Equal Hausdorff dimensions alone would not suffice.

If 0<M=H_s^g(J)<infinity, delete the countable poles and derivative-zero critical points, along with their countable images. These have zero Hausdorff mass. On the remaining points, a disjoint refinement of local injectivity neighborhoods gives conformality for any Borel set on which f is injective. The image pieces are disjoint in precisely that situation. The possible image point at infinity also has zero mass. Uniqueness of the atomless conformal probability therefore yields H_s^g|J = M m_s. Choosing the gauge g/M gives the requested exact normalization. There is no missing constant from the diameter convention because the same convention is used throughout.

This proves no positive finite value of M and says nothing about whether an arbitrary successful gauge must be regularly varying. Those gaps are correctly retained.

## 3. Spherical versus Euclidean measures

The weight is correct: with rho(z)=(1+|z|^2)^(-1), one has dm_e=rho^(-h) dm_s. Substitution into the spherical conformality identity cancels the target rho-factor and produces the Euclidean derivative power. Reversing this weight would be an error; the audit includes a negative control for that reversal and exact checks with nonintegral h obtained from perfect-power rational weights.

For regularly varying g, the same local change-of-metric argument gives dH_s^g=rho^h dH_e^g. Thus the packet correctly avoids comparing a spherical conformal probability to an unweighted Euclidean Hausdorff measure.

One sentence needs a small clarification. Multiplying the metric by c changes H^g by the factor c^h for an index-h regularly varying gauge. For a completely arbitrary gauge, the general exact identity is H^g for the metric c d = H^{g(c dot)} for the metric d. Equivalently, replacing g(r) by g(r/c) preserves the represented measure under the metric change. Existence of some scalar gauge is unchanged, but fixed-gauge behavior is not generally described by a scalar normalization alone. The proposed patch makes this distinction explicit.

## 4. Lattice, pole, and parabolic arguments

**Propositions 3-5 pass under the stated hypotheses.** Translation invariance of m_e follows by applying conformality to a set and its period translate: their images and Euclidean derivative weights agree. The weights are positive away from the countable exceptional set, and atomlessness removes that set. Local finiteness follows from the bounded metric-conversion weight on compact sets. A bounded half-open lattice fundamental cell has finite positive mass; its translates partition the plane. Lattice-cell counting therefore yields Euclidean annular mass comparable to R^2, and summation of weighted annuli gives spherical tail mass comparable to R^(2-2h).

Near a pole of order q, inverse derivatives have order R^(-1-1/q). Integrating over a complete annulus, using all q inverse branches and a finite Borel refinement of angular charts, gives annular pullback mass comparable to R^(2-h(1+1/q)). Sector boundaries need not be assumed null: choose overlapping open charts and assign the overlaps by a Borel partition. The dimension bound makes the exponent negative, so the tail can be summed. Converting R to a radius of order R^(-1/q) gives alpha=(q+1)h-2q, with 0<alpha<h.

The primary local parabolic law, after a local iterate with multiplier one, gives beta=(p+1)h-p. Atomlessness removes the singleton in that law. Local iteration is legitimate here: conformality iterates by the chain rule on the injective neighborhoods used, and no claim that a global transcendental iterate is meromorphic at all prepoles is needed. Since h>1, beta>h.

Consequently beta-alpha=p(h-1)+q(2-h)>0. Comparing balls at one pole and one parabolic periodic point rules out every globally uniform two-sided scalar-gauge ball bound. The fact that the centers belong to countable null sets does not invalidate that global obstruction, but it prevents it from deciding the required almost-everywhere density question.

### Explicit adversarial check of the nonimplication

For an elementary illustration independent of elliptic dynamics, let

E={0} union, for n>=1, [2^(-n), 2^(-n)+4^(-n)/4].

This is a compact set with H^1(E)=1/12. The probability mu=12 H^1|E has full support E and is exactly H^g|E for g(r)=12r. At r=2^(-N), the mass of the ball centered at zero is r^2, whereas at the midpoint 17/32 of the first interval, the ball mass is 24r for N>=6. Their ratio tends to infinity. Thus even full-support exact Hausdorff representation does not require the globally uniform bounds excluded by Proposition 5. This example validates the packet's warning; it is not an elliptic counterexample.

## 5. Invariant measures and recurrence

The source's invariant measure is a sigma-finite measure equivalent to the conformal probability, not the conformal probability itself. Its finiteness criterion for the parabolic class is the stated strict inequality involving the largest parabolic multiplicity. The equality boundary is divergent. No probability recurrence theorem may be substituted without the appropriate finite normalization or inducing argument.

The elementary parabolic model checks correctly distinguish the conformal tail sum from its first moment. The former produces beta, while the latter produces the invariant-mass threshold. The rational map x/(1+x) and its interval images are exact local models; neither a realized elliptic parameter nor the full induced system is certified.

The density obstruction for doubling gauges is valid in the spherical/Euclidean setting used. A disjoint 5r-covering gives cover diameters at most 10r, and the doubling constant absorbs that fixed factor. Countable additivity on the selected disjoint balls and finiteness of the localized measure give the asserted zero Hausdorff mass as the density threshold tends to infinity.

For the transported pole-density estimate, it is useful to state explicitly why the displayed radii tend to zero. The inverse branches in the cited argument exist on a disk of fixed positive radius and their images omit a fixed pole. Koebe's quarter theorem bounds their derivatives at the fixed preimage x from above by a constant depending on x and that pole. Therefore 1/D_j is bounded and d_j/D_j tends to zero. This supplies a short clarification of a step that is compressed in the packet, without providing the missing recurrence rate.

Qualitative d_j -> 0 cannot control the denominator L(D_j/(K d_j)). For example, purely formal sequences d_n=2^(-n), D_n=2^(4^n), gamma=1, and L(t)=log_2(t) give d_n^(-gamma)/L(D_n/d_n)=2^n/(4^n+n) -> 0. These are not asserted to arise from an elliptic map; they show exactly why qualitative recurrence alone does not justify the desired divergence. The packet correctly stops at that missing dynamical estimate.

## 6. Independent Pareto model and analogy limits

**Proposition 6 passes.** In the convergent case, fixed-epsilon exceedance probabilities have the same summability type as the original tail series; the first Borel-Cantelli lemma gives an eventual epsilon bound. A countable intersection over positive rational epsilon gives limsup zero. In the divergent case, independence is used exactly at the second Borel-Cantelli step, for each integer multiplier; another countable intersection gives infinite limsup. Independence is not needed in the convergent half. A fully dependent sequence with the same one-dimensional marginals demonstrates why the divergent conclusion cannot be transferred from marginal tails alone.

Simmons's Theorem 1.1 has explicit eventual differentiability and monotonicity of the log correction, existence of its limiting derivative, and Kleinian-group hypotheses. The packet correctly preserves these restrictions. Its argument is an analogy, not an unrestricted-gauge theorem for elliptic maps. No all-scale elliptic measure formula or appropriate shrinking-target law is supplied, in either finite or infinite invariant-mass regimes.

## 7. Corrections and replay

CORRECTIONS.patch proposes two changes to a working copy of the authored payloads: correct the exponent-loop counter and saved totals, and qualify the metric-normalization sentence. It does not alter any source statement, mathematical status, approach count, or frozen artifact. AUDIT_CORRECTIONS.md records the interpretation and an optional radius-shrinking clarification. The binding distinguishes the original snapshot from any later corrected publication copy.

Replay with:

`python3 audit_verify.py /path/to/author-packet.zip`

The command verifies the exact frozen ZIP, verifies all 13 manifest payloads, reproduces the original result, counts executed assert statements using AST instrumentation, and runs the 87,730 independent exact checks. Output is reproducible as AUDIT_CONTROL_RESULTS.json. Counts are finite test coverage, not measures of proof strength. No Monte Carlo inference, floating-point threshold, or unverified independence assumption is used.

The audit did not refresh repository duplicate-search state or re-download the source datasets; the authored repository gate remains historical evidence. It did freshly re-download three public primary PDFs and verify their fingerprints. No remote write, publication, outreach, or sixth proof-search approach was performed.

The publication-safe scientific conclusion remains: **partial reductions and obstructions only; the arbitrary exact spherical Hausdorff-gauge question is unresolved by this work.**
