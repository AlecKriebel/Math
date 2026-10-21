# Actual-outcome gate, PRs #1100–#1150

Recorded at 2026-10-17T16:35:19.261516+00:00. Outcome-gate completion estimate: **100%**. This estimate applies only to identifying the recorded outcome, not to the overall mathematical review/publication program.

All 51 pinned PR records were examined. QUEUE.md was not used. No mathematical or priority audit, repair, PR mutation, external comment, merge or publication was performed.

Explicit full-solution claims forwarded for later review: **#1102, #1108, #1114, #1118, #1119, #1121, #1129, #1135, #1136, #1141, #1142, #1150**.

Counts: 12 explicit full-solution claims; 28 partial/unsolved; 11 explicitly credited prior full resolutions; 0 unresolved outcome records.

A full claim is a claim to be rigorously audited, not an endorsement. Existing foundational ingredients and generic no-novelty language do not by themselves make a complete theorem ineligible. Explicit attribution of the full result to prior work does.

The important boundary cases are #1114 (full construction, directly relevant prior B3 realization; priority remains for later audit), #1129 (published first clause and complete authored deduction for second clause), #1136 (complete deduction from credited ingredients), #1141 (complete exact two-polynomial result from credited ingredients), #1142 (negative answer as stated with two boundary components), and #1148 (explicitly framed as a credited prior-result implication).

The nonempty saved PR bodies at #1138, #1140, #1141 and #1142 agree with the pinned outcome records retained here; both are quoted below. Pinned outcome records for #1114 and #1148 are also retained. See FETCH_PROVENANCE.json for exact hashes and absent-path records.

## PR #1100 — partial_or_unsolved

Problem 3000029; head `1a3bcb164bc2a7a6708283c02aa2ca676c7f6b05`.

The actual outcome expressly leaves the general minimum-rigidity-cut complexity target unresolved.

Outcome evidence: `evidence/pr1100/PR_BODY.md` lines 1–1.

> ## Accepted partial results; general complexity unresolved

Outcome evidence: `evidence/pr1100/PR_BODY.md` lines 3–6.

> Target: 3000029 / AMR-029-0029, minimum edge deletion destroying generic local
> rigidity in the Euclidean plane for finite simple rigid graphs on a fixed
> vertex set. Abstract topological planarity is not assumed. No arbitrary-input
> polynomial algorithm, valid hardness reduction, novelty or priority claim is made.

## PR #1101 — partial_or_unsolved

Problem 3000044; head `812b0b128705aa3de27c322910f086f60e2cc918`.

Structural overlap hypotheses cover a proper subcase and the general conjecture is expressly unresolved.

Outcome evidence: `evidence/pr1101/PR_BODY.md` lines 1–1.

> ## Accepted structural partial; general conjecture unresolved

Outcome evidence: `evidence/pr1101/PR_BODY.md` lines 3–8.

> For finite loopless acyclic directed multigraphs with prescribed convex sets,
> terminalwise simultaneous independent paths, the stated local bipartite
> matchings, and coherent independent prescribed-set out-arborescences are
> equivalent if each different-root overlap has at most one directed
> vertex-sequence path between any ordered pair after parallel arcs are
> collapsed. Same-root overlaps are unrestricted.

## PR #1102 — explicit_full_solution_claim

Problem 30006658; head `860cd93b8fb3ce5e9c7dc9109fc1e7cc83c9347a`.

The PR claims the full prime/field/compact-Lie theorem answering the originating target; related credited results are explicitly narrower.

Boundary/ambiguity: No-novelty boilerplate is not an outcome exclusion; mathematical validity and priority require the later audit.

Outcome evidence: `evidence/pr1102/PR_BODY.md` lines 1–1.

> ## Accepted complete theorem

Outcome evidence: `evidence/pr1102/PR_BODY.md` lines 3–9.

> For every prime p, every field k of characteristic p, and every compact Lie
> group G whose finite component group is not p-nilpotent, the canonical
> k-cellularization map Gamma_k R -> R induces zero in every homotopy degree,
> where R = C_*(Omega((BG)^p-completed); k). Target: 30006658 / OWR-14299915-021.
> Completion precedes looping. No adjoint-orientability, nilpotent-action or
> spectral-sequence-collapse assumption is imposed. This is zero on homotopy;
> nullity of the morphism in the derived category is not asserted.

## PR #1103 — partial_or_unsolved

Problem 3100062; head `912f49c5c1a080217781266e51195e7b67cac05e`.

The fixed-arity Rado target is expressly unresolved.

Outcome evidence: `evidence/pr1103/PR_BODY.md` lines 15–23.

> The target 3100062 / AMR-030-0062 is shared with 153 / GREEN-065 and
> remains unresolved here. No novelty or bibliographic priority is claimed.
> Public sources include:
> https://people.math.sc.edu/cooper/combprob.html
> https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf
> https://arxiv.org/abs/0812.1314
> https://arxiv.org/abs/1404.3384
> The Fox–Kleitman three-variable bound is credited through Green;
> its full paper was not inspected. Recorded retrieval failures remain distinct.

## PR #1104 — partial_or_unsolved

Problem 3400; head `1d7b60bec48940d9aca08a0fe3e16ef32a805fed`.

The unconditional general circuit-size target remains unresolved; the stronger conclusion is conjecture-dependent.

Outcome evidence: `evidence/pr1104/PR_BODY.md` lines 1–1.

> ## Accepted partial; general linear-size question unresolved

Outcome evidence: `evidence/pr1104/PR_BODY.md` lines 3–7.

> Preserves the explicit Boolean O(n log n) rank-parity construction, full gate
> accounting and O(log^2 n) depth, linear-overhead all-terminal fan-out
> conversion, threshold/count gadgets, ordinary and balanced bit-shift
> restrictions, and balanced-promise equivalence with the required output mask.
> Unconditionally the gap remains Omega(n) versus O(n log n).

## PR #1105 — partial_or_unsolved

Problem 5500040; head `975536365cfb1cc27d42132042da9863e668d1ea`.

The universal per-set counting inequality is not proved; the claimed injection has an explicit extra hypothesis.

Outcome evidence: `evidence/pr1105/PR_BODY.md` lines 10–15.

> A six-point coordinate wheel has no contained pointed pseudotriangulation.
> It refutes universal containment-only maps and Hall arguments on that
> relation. It does not refute the requested counting inequality: the audit
> independently proves t=11 and ppt=25 analytically.
> The one-interior fiber identity and general weighted-refinement identity
> remain in full. The necessary global compensation inequality is unproved.

## PR #1106 — partial_or_unsolved

Problem 9700022; head `05d35145a75c652a432eba6578f113cac19cec9b`.

No finite upper hegemony-time bound or counterexample is claimed for a full-plane start.

Outcome evidence: `evidence/pr1106/PR_BODY.md` lines 17–25.

> No finite upper bound on hegemony time or counterexample is proved for any
> named full-plane start. A contour-uniform summable bound for the actual
> process remains missing. No novelty or bibliographic priority is claimed.
> Public sources include:
> https://www.stat.berkeley.edu/~aldous/Papers/me123.pdf
> https://doi.org/10.1088/1751-8113/43/2/025001
> https://www.stat.berkeley.edu/~aldous/Research/OP/empires.html
> https://arxiv.org/html/math/0410359v3
> The 2017 Poissonian-coloring dynamics is explicitly distinguished.

## PR #1107 — partial_or_unsolved

Problem 5500029; head `6ac8bfdcd47511d728e8e0b04bb33d5c2feeb8ec`.

The unrestricted no-Steiner Hamiltonian-path tetrahedralization problem is expressly unresolved.

Outcome evidence: `evidence/pr1107/PR_BODY.md` lines 14–17.

> The exact target is a convex 3-polytope on its original extreme vertices,
> no Steiner points, positive-volume face-to-face tetrahedra and a
> Hamiltonian path in triangular-face adjacency. Coplanarity is allowed.
> The unrestricted problem remains unresolved here. No novelty is claimed.

## PR #1108 — explicit_full_solution_claim

Problem 30003439; head `148130ab93ab46a3459d7bc98a11a1ca79052d65`.

The recorded result explicitly claims to affirmatively answer the original existential question, with a specified cone and barrier.

Boundary/ambiguity: The cone is credited prior work; the complete original-target construction remains an explicit claim. The broader every-cone question is distinct.

Outcome evidence: `evidence/pr1108/PR_BODY.md` lines 3–11.

> This affirmatively answers the original existential question.
> The exact one-sided cone K = {(x,y,z) in R^3: x,y,z >= 0, xy^2 >= z^3}
> has the 100-normal barrier F = -25 log[z(xy^2-z^3)], with negative
> third-derivative curvature for every cone direction. No homogeneous
> polynomial in the original three-dimensional space has this K as its
> hyperbolicity cone. The complete analytic proof and mathematical audit
> are preserved, with the audit's optional mixed self-concordance bridge
> and explicit endpoint PSD decomposition incorporated into the proof.
> No mathematical correction was required.

## PR #1109 — partial_or_unsolved

Problem 30003308; head `24d3193c47d3585c70bdbda11c701a3d317017c2`.

The original non-complete-intersection classification is expressly unresolved.

Outcome evidence: `evidence/pr1109/PR_BODY.md` lines 1–1.

> ## OPEN/PARTIAL: original non-CI classification unresolved

Outcome evidence: `evidence/pr1109/PR_BODY.md` lines 3–6.

> Preserves the full analytic same-singleton-principal-matrix obstruction for
> two minimal primitive five-tuples, with types seven and one. The Gorenstein
> member is a complete intersection; no impossibility theorem for the original
> non-CI class is claimed. Collective gcd one is not pairwise coprimality.

## PR #1110 — partial_or_unsolved

Problem 30003033; head `a33f7d11d2901299979efb10a864070d1e524c63`.

The recorded result explicitly does not solve the original unrestricted principal-series connection question.

Outcome evidence: `evidence/pr1110/PR_BODY.md` lines 3–10.

> This does not solve the original unrestricted principal-series connection
> question. For the chamberwise rational-isotropic orthogonal-pair theta
> family, the full cyclic infinitesimal module is the specified tensor
> oscillator extension with trivial residual sl2 and a simple essential
> Hermite socle. That socle injects infinitesimally into the normalized
> Jacobi principal series at parameter -1; its Schwartz globalization has
> the group injection. For r>0 the full extension has zero Hom into every
> specified ordinary smooth or distribution-vector principal series.

## PR #1111 — partial_or_unsolved

Problem 30003421; head `e27ed810a53e7ade92f3a893dd94926f064e5f29`.

The A1/A2/B2 block theorem excludes G2 and arbitrary higher rank, leaving the original conjecture unresolved.

Outcome evidence: `evidence/pr1111/PR_BODY.md` lines 9–13.

> The arbitrary symmetrizable-Cartan conjecture remains unresolved by this
> work. G2 and arbitrary higher rank are not covered. The analogous
> full-constructible-function-algebra assertion is false and is excluded.
> The dimension convention is d=Dr with ordinary G(d), and the support
> inequality is strict. Nonmaximal components are allowed.

## PR #1112 — partial_or_unsolved

Problem 30003590; head `1473df9577fb840e6def0360cc78efa7450073ea`.

The singular-ambient counterexample is outside the original smooth-ambient problem, which remains unresolved.

Outcome evidence: `evidence/pr1112/PR_BODY.md` lines 17–23.

> The original OWR introduction uses smooth subvarieties of complex
> projective manifolds. This example refutes a broader singular-projective
> formulation, and does not solve the original smooth-ambient problem or
> a version separately requiring codimension at least two. No novelty,
> priority or worldwide current-status claim is made.
> Original problem, OWR 43/2017, Problem 1(1), printed p. 2633:
> https://doi.org/10.4171/OWR/2017/43

## PR #1113 — partial_or_unsolved

Problem 4500001; head `51cd6a64061a42bfc70b40980751b4fe15005d0a`.

The general irrational dependent arithmetic classification is expressly unresolved.

Outcome evidence: `evidence/pr1113/PR_BODY.md` lines 3–10.

> The complete authored proof and independent mathematical audit are retained.
> The results include exact weighted direction-retaining coding, a complete
> rational-pair region/period algorithm, the full quarter-rotation line, the
> rational-outer/irrational-inner periodicity threshold and whole periodic set,
> a complete irrational-capable 14/4 band, generic minimality/nonperiodicity,
> and an all-period visit obstruction. The general word certificate is exact
> but unbounded. The general irrational dependent arithmetic region
> classification remains unresolved; this is not a full solution.

## PR #1114 — explicit_full_solution_claim

Problem 30003952; head `e1a11feef98ed0fde22375c983e30b72b268d265`.

The pinned STATUS and ACCEPTANCE explicitly say full_resolution=true; the stated construction answers all original regularity questions.

Boundary/ambiguity: Relevant Mann–Tshishiku smooth B3 realization on a three-marked disk is expressly credited. The records still claim a complete prescribed-surface construction, so the priority relationship must be decided by the later priority audit rather than excluded at the outcome gate.

Outcome evidence: `evidence/pr1114/PR_BODY.md` lines 1–1.

> ## Complete smooth construction

Outcome evidence: `evidence/pr1114/PR_BODY.md` lines 3–8.

> For any prescribed essential pair meeting once on an oriented smooth surface,
> actual orientation-preserving C∞ diffeomorphisms A,B represent the prescribed
> right Dehn-twist classes and satisfy ABA = BAB as maps. The construction gives
> C∞ inverses, compact support inside a regular neighborhood and identity on a
> boundary collar. It answers the original homeomorphism, C1 and every finite Cr
> questions affirmatively, including the negative-Euler-characteristic cases.

Outcome evidence: `gate_reviews/lower/pr1114/STATUS.json` lines 6–15.

>   "classification": "COMPLETE_SOLUTION_ACCEPTED",
>   "full_resolution": true,
>   "mathematical_answer": "yes",
>   "review_status": "Complete smooth construction accepted by the accompanying independent AI-assisted mathematical audit; unrefereed",
>   "accepted_claims": [
>     "For any prescribed essential pair meeting once on an oriented smooth surface, actual orientation-preserving C∞ diffeomorphisms A,B represent the prescribed right Dehn twists and satisfy ABA=BAB as maps.",
>     "The maps and their inverses are C∞, so the homeomorphism, C1 and every finite Cr question is answered affirmatively.",
>     "The maps have compact support in the interior of any sufficiently small compact regular neighborhood of the pair, with identity on a boundary collar.",
>     "The construction fixes existing boundary, marked points and punctures by choosing the neighborhood disjoint from them.",
>     "The construction lifts the specified B3→Mod(S) homomorphism; it need not split its image when ambient relations are added."

Outcome evidence: `gate_reviews/lower/pr1114/README.md` lines 15–18.

> Mann–Tshishiku's Theorem 4.1 already supplies smooth B3 realization on a
> three-marked disk. This directly relevant positive prior work is prominently
> credited; no novelty or priority is claimed.
> [Prior realization](https://arxiv.org/abs/1802.00490).

## PR #1115 — partial_or_unsolved

Problem 30003863; head `cc69ca2d80d85a7a6fcbb07d70e431efca66bb34`.

The full cylinder-free/all-automorphism-extension equivalence is expressly unsolved.

Outcome evidence: `evidence/pr1115/PR_BODY.md` lines 3–5.

> The full cylinder-free versus all-automorphism-extension equivalence remains
> unsolved here. This proof-only edition preserves the complete bounded proof
> and independent mathematical audit, with no mathematical correction required.

## PR #1116 — explicitly_prior_full_resolution

Problem 30004007; head `fd88f8034d1850e5848ede0ebf47d451461e2fd2`.

The decisive budget-2 counterexample and its non-MRS property are explicitly credited to Dughmi–Roughgarden–Yan (2011); this edition adds representation and reconstruction.

Boundary/ambiguity: The all-field representation is supplied here, but the body explicitly identifies the decisive counterexample as prior mathematics; the prior manuscript did not explicitly address the later OWR question.

Outcome evidence: `evidence/pr1116/PR_BODY.md` lines 5–5.

> The principal budget-2 counterexample and its non-MRS property are explicitly credited to Dughmi–Roughgarden–Yan (2011), full author manuscript §D.2; Definition 2.1 allows nonnegative real weights. The edition supplies the explicit all-field representation and complete direct and separating-functional proofs. No novelty or priority is claimed. The prior manuscript is not claimed to address the later OWR question explicitly.

## PR #1117 — partial_or_unsolved

Problem 30003993; head `e9b0c073fa22d19914cd55433b2618fd1babad9b`.

The original constant-versus-unbounded directed linear k-cut gap question remains open.

Outcome evidence: `evidence/pr1117/PR_BODY.md` lines 3–9.

> For every k>=2, an explicit polynomial-size finite simple directed graph
> with k distinct ordered terminals and unit edge costs has integral optimum
> C_k-k^2 and an original edge path-distance LP vector of cost C_k/3, where
> C_k = sum_{l=1}^k (k-l+1) floor(k/l). The lower bounds 3(1-k^2/C_k)
> tend to 3; the actual gaps have liminf at least 3. Convergence of the actual
> gaps to 3, exact LP optima, unbounded gaps and a universal constant upper bound
> are not proved. The original constant-versus-unbounded question remains OPEN.

## PR #1118 — explicit_full_solution_claim

Problem 30004231; head `8592fb7297d3c4973f2778c47cfa8972cba896a6`.

The PR explicitly claims counterexamples resolving both printed assertions.

Boundary/ambiguity: Alternative definitions or general-position variants are excluded; exact-target interpretation remains for later audit.

Outcome evidence: `evidence/pr1118/PR_BODY.md` lines 1–1.

> ## Complete negative resolution of both printed assertions

Outcome evidence: `evidence/pr1118/PR_BODY.md` lines 3–9.

> For the standard four-simplex D and I=[0,1], the full-dimensional lattice
> polytopes D×I and (−D)×I in R5 have a totally mixed face order complex that is
> a disjoint union of two connected pure graphs, each with 50 vertices and
> 60 edges. Its rational Betti numbers are (2,22,0,0,…). This disproves both
> shellability and the claimed rational homology of a wedge of three-spheres.
> The separate R3 six-point control refutes only the homology assertion and
> is shellable in dimension zero.

## PR #1119 — explicit_full_solution_claim

Problem 30004127; head `786fff9ba06951209e8c1e3bc6114efbfa2c9d16`.

The PR explicitly claims a full negative answer to the original testing-complexity comparison.

Boundary/ambiguity: The recorded query model distinctions must be checked in the later audit.

Outcome evidence: `evidence/pr1119/PR_BODY.md` lines 1–1.

> ## Accepted complete negative answer

Outcome evidence: `evidence/pr1119/PR_BODY.md` lines 3–7.

> For the fixed hereditary, extendable, edge-monotone property of K4-free
> graphs that become 3-colorable after deletion of at most one vertex, the
> classical canonical sample complexity is O(epsilon^-6 log(1/epsilon)) for
> all finite sizes without knowing n. Its full induced adjacency cost is
> quadratic; no polynomial runtime is claimed.

## PR #1120 — partial_or_unsolved

Problem 30004196; head `b94c626bfadcfc6dbc653c7ad3654f3e053b0f18`.

The original broader initial-surface, fixed-flow oval-limit question remains open.

Outcome evidence: `evidence/pr1120/PR_BODY.md` lines 12–18.

> The original question allows a broader initial-surface class and asks for a
> later-time oval limit in one fixed flow. It remains OPEN. No single-flow
> realization, complete original-class exclusion, novelty or priority is claimed.
> The full infinite C^{1,1} twice-differentiable scalar construction is not an
> arrival-time PDE solution. The audit preserves its explicit regular transition
> point with arrival operator 4229/18 and residual 4247/18. The varying-flow peanut
> and initially singular Miura examples retain their precise limitations.

## PR #1121 — explicit_full_solution_claim

Problem 30004311; head `f86b108ac1bc024302648eee9f47f74e26c810ec`.

The PR expressly claims a complete finite-brace counterexample answering Cedó Problem 9 negatively.

Boundary/ambiguity: No historical-novelty claim is made; this generic disclaimer does not remove the explicit full-solution claim.

Outcome evidence: `evidence/pr1121/PR_BODY.md` lines 3–7.

> The explicit brace B of order 20,000 is nontrivial and simple, with additive
> group C5^4 x C2^5 and multiplicative group (C5^3 semidirect C2) x
> (C2^4 semidirect C5). The multiplicative group is metabelian and every
> multiplicative Sylow subgroup is abelian, yet B is not an asymmetric product
> of two trivial braces. This answers Cedó’s original Problem 9 negatively.

## PR #1122 — partial_or_unsolved

Problem 30004513; head `27d3c93ebaec0438c3499829b7fede5701db6fc2`.

The star theorem is source credited and the original three-question bundle expressly remains partial.

Boundary/ambiguity: Partial classification takes precedence over the prior-credit label because the full original bundle is unresolved.

Outcome evidence: `evidence/pr1122/PR_BODY.md` lines 18–25.

> The credited clique upper bound is p(K_n,b)<=sum_{j=0}^{n-1}b^j. The Ramsey
> lower bound concerns arbitrary b-iatlon graphs and need not be realizable by
> planar closures; the directly checked closure lower bound is (n-1)b+1.
> The original three-question bundle remains PARTIAL: exact general clique
> thresholds and the nontrivial higher homology/homotopy question are unanswered
> here. No novel theorem, proof novelty or priority is claimed. Unsupported
> computational values and unaudited Radon/Helly or topological claims are
> excluded from acceptance.

## PR #1123 — partial_or_unsolved

Problem 20000225; head `aa02b7055349e96f9aa91a60c7c2e952d5d618f0`.

The construction-route obstruction leaves the actual irreducible-complex proper-point Harbourne target open.

Outcome evidence: `evidence/pr1123/PR_BODY.md` lines 10–14.

> The original irreducible complex proper-point h<-2 existence question
> remains OPEN. The result does not rule out all degree-26 curves with
> 30 ordinary quintuple points, decide the asymmetric n=4 graph case,
> or resolve the earlier degree-21 necessary patterns. No converse reducing
> all such curves to the graph-pair construction is claimed.

## PR #1124 — partial_or_unsolved

Problem 30004486; head `8002ca837b98803d37fea53910a5e3d0f58b4e4c`.

The original skyrmion non-staticity/quantitative-energy target remains open.

Outcome evidence: `evidence/pr1124/PR_BODY.md` lines 12–15.

> The original non-staticity/quantitative-energy target remains OPEN. No frequency nonvanishing/sign/lower bound, global range,
> endpoint energy law, uniform endpoint constants, minimizer uniqueness or
> smoothness of all weak minimizers is claimed. Zero between the extremal
> corner slopes need not be an attained multiplier.

## PR #1125 — partial_or_unsolved

Problem 20000822; head `e90c101a3046c517a1924abca5c119f1561b556e`.

Neither an example nor a full impossibility theorem is claimed for the fat connected Hilbert-component target.

Outcome evidence: `evidence/pr1125/PR_BODY.md` lines 3–5.

> AIM Problem 21 asks whether a polynomial-ring multigraded Hilbert scheme
> with a fixed full Hilbert function has a connected component that is a fat point.
> This proof-only edition supplies no example and no full impossibility theorem.

## PR #1126 — explicitly_prior_full_resolution

Problem 10400072; head `47aff7d85965c7493b9b6af006acb8c73071f03a`.

The exact Laurent-polynomial negative resolution is explicitly credited to Patureau-Mirand Theorem 4 (2012).

Outcome evidence: `evidence/pr1126/PR_BODY.md` lines 3–8.

> Ohtsuki Conjecture 3.22 is false in its exact Laurent-polynomial case:
> map (30), equivalently map (29) at the admissible choice A(t)=1.
> Credit belongs to Bertrand Patureau-Mirand, Noninjectivity of the “hair” map,
> Algebraic & Geometric Topology 12 (2012), 415–420, Theorem 4.
> Published source: https://msp.org/agt/2012/12-1/p16.xhtml
> Original statement: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf

## PR #1127 — explicitly_prior_full_resolution

Problem 30005263; head `a1b8857a49dc6e4761c27952930ba2a133b372f6`.

The exact Gaussian target is explicitly credited to Gwóźdź arXiv:2609.04052v1 rather than a new solution.

Boundary/ambiguity: The credited source is an unrefereed preprint; prior-credit classification does not certify its validity.

Outcome evidence: `evidence/pr1127/PR_BODY.md` lines 9–17.

> Credit: Maja Gwóźdź, Caffarelli Estimates under Lipschitz Perturbations,
> arXiv:2609.04052v1, submitted September 3, 2026 at 16:24:45 UTC.
> https://arxiv.org/abs/2609.04052
> https://arxiv.org/pdf/2609.04052v1
> The inspected public record establishes a September 2026 preprint, not
> journal acceptance or peer review. No new proof, novelty or priority is claimed.
> Original conjecture: Max Fathi, joint work with Dan Mikulincer and Yair
> Shenfeld, Oberwolfach Report 49/2022, Conjecture 1, printed page 2845.
> https://ems.press/content/serial-article-files/46987

## PR #1128 — partial_or_unsolved

Problem 30005275; head `db6b28477c2bcd4302fcf9fef2d4a86fa17b4d98`.

The exact low-degree classifications leave the full arbitrary-degree target open in both prime regimes.

Outcome evidence: `evidence/pr1128/PR_BODY.md` lines 15–21.

> The full arbitrary-degree target remains OPEN in both prime regimes.
> X^2 versus X^6 obstructs universal affine rigidity at arbitrarily large
> primes 2 modulo 3, but not at all sufficiently large primes. X^4 versus
> -4X^4 agrees at every odd prime and obstructs rational input-affine rigidity
> with output sign restricted to +/-1, while remaining complex-affine.
> The p=5 complementary-fiber example is a boundary control; no sharpness
> of the sufficient p>=11 bound is claimed.

## PR #1129 — explicit_full_solution_claim

Problem 30005461; head `26fed29c1130e539ba018a37200f133870f0e036`.

The PR explicitly claims both original clauses, including the all-c<3 Motzkin odd-power conclusion and threshold limit.

Boundary/ambiguity: One clause is expressly a published Blekherman–Kozhasov–Reznick theorem; the Motzkin clause is presented as a complete authored deduction from a broader Scheiderer input. The whole target is not expressly attributed as an existing prior resolution.

Outcome evidence: `evidence/pr1129/PR_BODY.md` lines 1–1.

> ## Full two-clause mathematical resolution

Outcome evidence: `evidence/pr1129/PR_BODY.md` lines 3–8.

> For arbitrary real polynomials p,q, if p^(2i+1) and q^(2j+1) are sums
> of squares, then (p+q)^(2i+2j+1) is a sum of squares. This is the
> published Blekherman–Kozhasov–Reznick theorem, with the truncated-binomial
> ingredient credited to Iosif Pinelis. The full credited proof, both source
> index/display corrections, arbitrary-degree reduction and edge cases are
> included.

## PR #1130 — partial_or_unsolved

Problem 30005298; head `589b5f81c3bdcfca08597a7c3714483e148f3f54`.

The complete P3 dimension table and other regimes leave the all-parameter Weddle problem open.

Outcome evidence: `evidence/pr1130/PR_BODY.md` lines 10–10.

> These are statements about the reduced closure of the outside-Z jumping locus. All quantifiers, generic-fiber arguments, projective nonemptiness and boundary-center exclusion, common-factor occupancy bounds, determinantal lower bounds and monotonicity qualifications remain in full. The all-parameter problem remains OPEN. The conservative residual is n>=4,d>=2,d+2<=r<=N-2 except values otherwise settled, without claiming every residual value is independently open. No entire determinantal-scheme, ACM, multiplicity, irreducibility, full component or general degree conclusion is added.

## PR #1131 — partial_or_unsolved

Problem 30005455; head `bacae693a1f2a33c89565b0bd716620885831289`.

The equal-rate whisker interval 4/3<alpha<17/4 remains unresolved, so the original bundled target is partial.

Outcome evidence: `evidence/pr1131/PR_BODY.md` lines 7–7.

> The full bundled target remains OPEN: the equal-rate whisker interval 4/3<alpha<17/4 is unresolved. The exact stable unequal-rate diameter-four path at alpha=2 is a scope control, not a counterexample to that equal-rate target. No infinite-graph or loop/multigraph extension is asserted.

## PR #1132 — explicitly_prior_full_resolution

Problem 30005952; head `bab329be46faab9d04bf1664a7183712239f88b2`.

The complete counterexample, module decomposition and computer-assisted argument are explicitly credited to Ferudun.

Outcome evidence: `evidence/pr1132/PR_BODY.md` lines 3–3.

> Alper Ferudun's September 30, 2026 Theorem 1.3 supplies Sigma(30,47,83): its total ungraded F2[U] HF-minus module has torsion length 16 and no length-15 cyclic direct summand, for both orientations. It is an integral homology sphere with one Spin-c structure. Credit for the example, decomposition and computer-assisted argument belongs to Ferudun.

## PR #1133 — explicitly_prior_full_resolution

Problem 30006113; head `22be679fda3e2e4c87fb79458d7ade2df07f5b1c`.

The original strong-density target is explicitly recorded as resolved by Chandrasekaran–Chekuri–Kulkarni; this is their source-credit audit and corrections.

Outcome evidence: `evidence/pr1133/PR_BODY.md` lines 3–3.

> The original strong-density extreme-point statement is resolved by Chandrasekaran, Chekuri and Kulkarni, arXiv:2609.04414v1, Theorem 1, with the explicit elementary corrections and bounded-to-original bridge in this authored audit. IDs 30004905 and 30006114 concern the same underlying Fiorini question.

## PR #1134 — explicitly_prior_full_resolution

Problem 30005752; head `51f6f84bebaaa365ec501b9b3c937fd4eeda306d`.

Tang is explicitly credited with the proof of the full original divisibility conjecture.

Outcome evidence: `evidence/pr1134/PR_BODY.md` lines 3–4.

> Qiyue Tang's September 26, 2026 arXiv v1 preprint, *A Note on Universal Positivity of Rank-Two Quantum Greedy Elements*, supplies the proof of the full divisibility case of Lee–Li–Rupel–Zelevinsky's Conjecture 1.10. Credit belongs to Tang:
> https://arxiv.org/abs/2609.37452v1

## PR #1135 — explicit_full_solution_claim

Problem 30000052; head `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`.

The PR explicitly claims analytic counterexamples resolving the universal expected p-th-power comparison negatively.

Boundary/ambiguity: The expectation-of-norm variant is expressly distinct; the later audit must verify exact original-target matching.

Outcome evidence: `evidence/pr1135/PR_BODY.md` lines 3–3.

> The universal continuous-generator expected-moment comparison in problem 30000052 / OWR-723-005 is false. The full standalone elementary proof and complete substantive independent internal AI-assisted audit are included.

## PR #1136 — explicit_full_solution_claim

Problem 2307037; head `cbbe7826cca914588018c840ba99c6b7a59fa7f5`.

The PR claims a complete affirmative result for the named Hayman–Lingham problem with simultaneous all-R control.

Boundary/ambiguity: Existing sharp Beurling and quadrature theorems are credited inputs, not an explicit attribution of the full original-target answer to prior work.

Outcome evidence: `evidence/pr1136/PR_BODY.md` lines 1–1.

> ## Complete affirmative deduction

Outcome evidence: `evidence/pr1136/PR_BODY.md` lines 3–3.

> Adds the complete authored proof and independent AI-assisted audit for Hayman–Lingham Problem 7.37 / 2307037 / AMR-022-7037.

## PR #1137 — partial_or_unsolved

Problem 30000515; head `43b9eb289661b75ad7b8a718e3355febe5e3265d`.

The full Godeaux fundamental-group target remains unresolved despite finite-cover deductions.

Outcome evidence: `evidence/pr1137/PR_BODY.md` lines 3–3.

> Problem 30000515 / OWR-1276-008 remains unresolved by this work. The complete authored partial proof and full substantive independent internal AI-assisted mathematical audit are included. No full-resolution, counterexample, novelty or priority claim is made.

## PR #1138 — explicitly_prior_full_resolution

Problem 2302066; head `dfbabfe13ef4fd7f4dfb8766ffc74839d3db0e77`.

The saved PR body preserves historical Hinkkanen credit, and the pinned README says the 2018 edition already reports independence; this is an authored reconstruction of that known outcome.

Boundary/ambiguity: Historical unpublished proof is not recovered, but the saved PR body and pinned outcome records explicitly agree on the prior outcome; no mathematics was audited.

Outcome evidence: `evidence/pr1138/PR_BODY.md` lines 1–9.

> ## Exact source-credit resolution
> 
> Adds the full authored reconstruction and AI-assisted mathematical audit for Hayman–Lingham Problem 2.66 / 2302066 / AMR-022-2066.
> 
> ZFC proves that the full omega_1-indexed strictly maximum-modulus-ratio cofinal hierarchy exists iff d=aleph_1. Every limit is over all real radii tending to infinity. Assuming Con(ZFC), both the hierarchy and its negation are relatively consistent.
> 
> Preserves Hayman–Lingham’s historical credit to Hinkkanen (unpublished), uses Blass–Shelah’s published 1987 Theorem 5.2(a),(d) for the negative model, and Gödel’s constructibility metatheorem for positive consistency. The complete elementary majorant, shifted all-radii estimate, countable upper bounds, and omega_1 recursion remain in AUDIT.md. No novelty or priority claim is made. The reconstruction and AI-assisted audit are unrefereed and are not external human peer review or formal machine proof.
> 
> The full Hechler spectrum, precise later-book attribution, independence over ZFC+not CH, and equivalence with or disposition of Problem 7.62 are explicitly excluded. All substantive source limitations remain. The mathematical proof has no hidden computational dependency.

Outcome evidence: `gate_reviews/lower/pr1138/README.md` lines 7–16.

> The exact accepted result is:
> 
>     ZFC proves H iff d=aleph_1.
>     Con(ZFC) implies Con(ZFC+H) and Con(ZFC+not H).
> 
> The complete authored transfer and source audit are in AUDIT.md. The proof supplies explicit entire majorants, the shifted all-radii estimate, countable strict upper bounds, and transfinite recursion through all countable ordinals. It then applies established positive and negative relative-consistency theorems. No computational result is needed for the mathematical deduction.
> 
> ## Credit and status
> 
> Hayman–Lingham’s 2018 edition already reports independence and credits Hinkkanen’s unpublished work. That credit is preserved; the unpublished argument was not recovered. The published negative model used here is Blass–Shelah (1987), Theorem 5.2(a),(d). The positive consistency input is Gödel’s constructibility metatheorem. The explicit elementary transfer is an authored reconstruction, with no attribution of its formulas to those sources and no novelty or priority claim.

## PR #1139 — partial_or_unsolved

Problem 30000374; head `9adbe5b79c1df2c417982f55989fc2f96cf1e208`.

The ordinal-colored preorder target expressly remains unresolved.

Outcome evidence: `evidence/pr1139/PR_BODY.md` lines 3–3.

> Problem 30000374 / OWR-1116-002 remains unresolved by this work. This edition includes the complete authored proof and full substantive independent internal AI mathematical audit. No mathematical correction was required; the proof is byte-identical to its accepted frozen original.

## PR #1140 — explicitly_prior_full_resolution

Problem 30002450; head `35e9a328dfe7d5e188f59239d2e161d150da91e8`.

The saved PR body, pinned STATUS and pinned README expressly label the full original outcome a prior published resolution by Geuenich–Labardini-Fragoso–Miranda-Olvera.

Boundary/ambiguity: Saved PR body and pinned outcome records agree on the exact prior published resolution.

Outcome evidence: `evidence/pr1140/PR_BODY.md` lines 1–7.

> ## Exact prior published resolution
> 
> Adds the complete authored mathematical audit and explicit local formula corrections for problem 30002450 / OWR-12732-002.
> 
> The prior published result is due to Jan Geuenich, Daniel Labardini-Fragoso and José Luis Miranda-Olvera, Séminaire Lotharingien de Combinatoire 84 (2022), Article B84c, Theorems 1.1(2) and 4.1. The [official journal record](https://www.mat.univie.ac.at/~slc/wpapers/s84geuen.html) records the accepted and final version on February 8, 2022.
> 
> The exact scope is every compact connected oriented closed surface of genus g >= 1 with exactly two punctures, all tagged triangulations and every algebraically closed field of arbitrary characteristic. Its quiver admits a nondegenerate completed potential, and all its nondegenerate potentials form exactly one weak right-equivalence class.

Outcome evidence: `gate_reviews/lower/pr1140/README.md` lines 3–9.

> Problem 30002450 / OWR-12732-002 has a prior published positive resolution by Jan Geuenich, Daniel Labardini-Fragoso and José Luis Miranda-Olvera, in [Séminaire Lotharingien de Combinatoire 84 (2022), Article B84c](https://www.mat.univie.ac.at/~slc/wpapers/s84geuen.html), Theorems 1.1(2) and 4.1.
> 
> For every compact connected oriented closed surface of every genus g >= 1 with exactly two punctures, every tagged triangulation has a quiver admitting a nondegenerate potential. All its nondegenerate potentials in the completed path algebra form exactly one weak right-equivalence class over every algebraically closed field, in arbitrary characteristic.
> 
> AUDIT.md contains the complete authored proof audit. PROOF_CORRECTIONS.md makes the local source-formula corrections explicit, including the Proposition 4.4 mate indices, formal splitting, positive-characteristic checks, absent-series identities and convergent complete-algebra automorphisms. The mathematical reasoning is fully presented in those documents, with published theorem dependencies identified in SOURCE_DEPENDENCIES.json. Finite regression checks are supplementary.
> 
> The source theorem is published. This AI-assisted authored audit and its local corrections are unrefereed and do not claim external human peer review. No author-issued erratum, new solution, novelty, priority or formal machine proof is claimed.

Outcome evidence: `gate_reviews/lower/pr1140/STATUS.json` lines 5–15.

>   "status": "ACCEPT_FULL_PRIOR_PUBLISHED_POSITIVE_RESOLUTION_WITH_EXPLICIT_LOCAL_FORMULA_CORRECTIONS",
>   "accepted_scope": {
>     "surface": "compact connected oriented closed surface",
>     "genus": "every integer g >= 1",
>     "punctures": 2,
>     "triangulations": "all tagged triangulations",
>     "field": "every algebraically closed field",
>     "characteristic_restriction": null,
>     "potentials": "completed path algebra modulo closed cyclic differences",
>     "existence": true,
>     "uniqueness": "one weak right-equivalence class of nondegenerate potentials"

## PR #1141 — explicit_full_solution_claim

Problem 30006210; head `b1d6bc6ceb66e9c9c98cfae229ee86e5720799e2`.

The saved PR body and pinned README expressly claim a complete affirmative proof for the exact two-polynomial Boolean-cube question.

Boundary/ambiguity: Source-credit is to a separator lemma and other proof ingredients; it is not an explicit attribution of the complete original target as a previously resolved theorem.

Outcome evidence: `evidence/pr1141/PR_BODY.md` lines 1–9.

> ## Exact affirmative result
> 
> Adds the complete authored proof and substantive independent internal mathematical audit for problem 30006210 / OWR-14299088-012.
> 
> For every pair of positive integers n,d and every pair of nonzero real multilinear polynomials f,g on {-1,1}^n of degree at most d, all relative coordinate influences at most 1/(4096d^8) imply intersecting supports. Relative influence uses the full squared L2 norm, including the constant coefficient. Thus c=1/4096 and C=8 suffice. The proof establishes the stronger lower bound 1/(1024d^8) for the maximum influence under disjointness.
> 
> The essential prior separator is credited prominently to Longcheng Li, Qian Li, Xingjian Li and Qipeng Liu, [arXiv:2608.03824v1, Lemma 3.5](https://arxiv.org/abs/2608.03824v1). Its proof is reconstructed with depth 16d^4. The Markov/Bernoulli input is credited to [Kothari, Kovacs-Deak, Wang and Yang, arXiv:2601.08727v3](https://arxiv.org/abs/2601.08727v3). The adaptive covariance bridge and square-influence estimate are fully proved.
> 
> The frozen proof's pending-audit header is explicitly updated to its accepted internal mathematical status. All mathematics, source credit and substantive limitations are preserved; original and distributed proof hashes are distinguished. The proof and audit are AI-assisted and unrefereed. No external human peer review, journal acceptance of this proof, formal machine proof, novelty or priority is claimed. No general distribution-formulation, other-group or approximate-support extension is claimed.

Outcome evidence: `gate_reviews/lower/pr1141/README.md` lines 3–9.

> Problem 30006210 / OWR-14299088-012 has a complete affirmative proof for the exact two-polynomial Boolean-cube question, accepted by an independent internal mathematical audit.
> 
> For every pair of positive integers n,d and every pair of nonzero real multilinear polynomials f,g on {-1,1}^n of degree at most d, the bounds RelInf_i(f), RelInf_i(g) <= 1/(4096 d^8) for every coordinate imply that f and g are simultaneously nonzero at some vertex. Relative influence uses the full squared L2 norm, including the constant coefficient. Thus c=1/4096 and C=8 suffice. The proof establishes the stronger necessary lower bound 1/(1024 d^8) on the maximum relative influence for disjoint supports.
> 
> The essential separator is prior work of Longcheng Li, Qian Li, Xingjian Li and Qipeng Liu, [arXiv:2608.03824v1, Lemma 3.5](https://arxiv.org/abs/2608.03824v1). PROOF.md reconstructs it with the explicit depth 16d^4, includes the classical Markov/Bernoulli argument credited to [Kothari, Kovacs-Deak, Wang and Yang, arXiv:2601.08727v3](https://arxiv.org/abs/2601.08727v3), and supplies the complete adaptive covariance and square-influence arguments.
> 
> The AI-assisted proof and independent internal audit are unrefereed. Internal acceptance does not claim external human peer review, journal acceptance, formal machine certification, novelty or priority. The result concerns the exact two-polynomial question; no general distribution-formulation, other-group or approximate-support extension is claimed.

## PR #1142 — explicit_full_solution_claim

Problem 30002112; head `c29139d2c2a98f1a0284d0dc794c88f51c680a0c`.

The saved PR body and pinned README claim a negative answer for the stated original class using connected domains with two boundary components.

Boundary/ambiguity: The connected-boundary variant remains unclaimed; the later audit must verify the original target allows disconnected boundary. STATUS records acceptance as stated.

Outcome evidence: `evidence/pr1142/PR_BODY.md` lines 1–9.

> ## Exact negative result
> 
> Adds the complete authored proof and substantive independent internal AI mathematical audit for problem 30002112 / OWR-12005-004.
> 
> For every fixed integer m>=2, bounded connected smooth domains in R^(m+1) with exactly two connected boundary components defeat every finite pair of dimension-only constants in the additive estimate
> 
> lambda_k(boundary Omega) |boundary Omega|^(2/m) <= A_m I(Omega)^(1+2/m) + B_m k^(2/m).
> 
> Here I(Omega)=|boundary Omega|/|Omega|^(m/(m+1)); the spectrum is intrinsic Laplace-Beltrami for the induced boundary metric and includes all zero modes and multiplicities, indexed from 1. The quotient with the sum of the two unweighted target terms tends to infinity. The domain itself is connected. No connected-boundary or m=1 result is claimed.

Outcome evidence: `gate_reviews/lower/pr1142/README.md` lines 3–17.

> Problem 30002112 / OWR-12005-004.
> 
> For every fixed integer m >= 2, the complete proof constructs bounded connected smooth domains in R^(m+1), each with exactly two connected boundary components, for which
> 
> lambda_k(boundary Omega) |boundary Omega|^(2/m) / (I(Omega)^(1+2/m) + k^(2/m)) tends to infinity,
> 
> where I(Omega)=|boundary Omega|/|Omega|^(m/(m+1)). Thus no finite pair of dimension-only constants satisfies the proposed additive estimate for the stated class. The spectrum is intrinsic Laplace-Beltrami on the induced boundary metric; all zero modes and multiplicities are counted from index 1.
> 
> The domain is connected. This construction makes no claim for connected boundaries or for m=1. In dimension 2 the cavity genus may vary; in dimensions at least 3 it may be a sphere. The final domains and boundaries are smooth.
> 
> ## Credit and review status
> 
> The argument uses the established Colbois-Dryden-El Soufi large-normalized-eigenvalue theorem, the C0-dense Nash-Kuiper isometric-embedding theorem, standard smooth approximation and generalized Jordan-Brouwer separation. It supplies the quantitative metric comparison, small-ball/exact-area construction, connected-domain verification, exact spherical spectral rank and limiting contradiction. Source credit and precise inspection limits appear in PROOF.md, AUDIT.md, SOURCE_DEPENDENCIES.json and SOURCE_METADATA.json.
> 
> The AI-assisted proof has been accepted by an independent internal AI mathematical audit. The proof and audit are unrefereed. No external human peer review, journal acceptance, formal machine proof, novelty or priority is claimed. Internal acceptance applies only to the exact two-component-boundary scope above.

Outcome evidence: `gate_reviews/lower/pr1142/STATUS.json` lines 5–15.

>   "status": "ACCEPT_AS_STATED_BOUNDARY_MAY_BE_DISCONNECTED",
>   "review_status": "AI-assisted authored proof and independent AI mathematical audit; internally accepted and unrefereed; no external human peer review claimed.",
>   "exact_result": "For every fixed integer m>=2, connected bounded smooth Euclidean domains with exactly two boundary components disprove all finite dimension-only constants in the additive boundary Laplace-Beltrami estimate.",
>   "inequality_disproved": "lambda_k(boundary Omega) |boundary Omega|^(2/m) <= A_m I(Omega)^(1+2/m) + B_m k^(2/m)",
>   "isoperimetric_ratio": "I(Omega)=|boundary Omega|/|Omega|^(m/(m+1))",
>   "all_fixed_integers_m_at_least_2": true,
>   "domain_connected": true,
>   "boundary_connected_components": 2,
>   "connected_boundary_result_claim": false,
>   "dimension_one_result_claim": false,
>   "all_zero_modes_counted": true,

## PR #1143 — partial_or_unsolved

Problem 30001611; head `e0a78df4ccef8a6f08b8d80a5aad391fbc90dfa0`.

The full endpoint cyclicity question is expressly unresolved; a proper cutoff ideal is not the target counterexample.

Outcome evidence: `evidence/pr1143/PR_BODY.md` lines 9–9.

> Crucially, the Banach defect quotient is cyclic. A proper cutoff ideal and a noncyclic displayed vector do not establish operator noncyclicity. Cyclicity of both full endpoint models remains undetermined by this work; the original problem remains unresolved by this submission.

## PR #1144 — partial_or_unsolved

Problem 30002009; head `1635e8e2aa8c46f507835704fff57fafa5c55b15`.

Generic computability does not provide the structural higher-rank target and the original problem expressly remains partial.

Outcome evidence: `evidence/pr1144/PR_BODY.md` lines 9–9.

> This is generic computability using classical topology. It is not a structural higher-rank resolution, practical triangulation implementation, root-combinatorial matrix formula, canonical or minimal model, or novelty claim. No higher-rank general triangulation search was executed. The original problem remains PARTIAL. No novelty, priority, exhaustive literature search, or present global-open-status claim is made.

## PR #1145 — explicitly_prior_full_resolution

Problem 30002714; head `c7e122e5324074939ca5ff2b5b5a93e241e15c76`.

The original unrestricted negative answer is explicitly a prior published counterexample with a reconstruction.

Outcome evidence: `evidence/pr1145/PR_BODY.md` lines 3–3.

> Adds the complete elementary reconstruction and substantive independent internal mathematical audit for problem 30002714 / OWR-13351-013. This is a prior published counterexample, with no new theorem, novelty, or historical-priority claim.

## PR #1146 — explicitly_prior_full_resolution

Problem 30002482; head `e7bdf5c63d4a6d99eed071c3a05afeb83650dbb8`.

The historical characteristic-zero ladder assertion is explicitly credited to the published Mitra–Offen–Sayag theorem.

Boundary/ambiguity: Unqualified field ambiguity and unclaimed positive-characteristic extensions are explicit. The accepted historical target is prior resolved.

Outcome evidence: `evidence/pr1146/PR_BODY.md` lines 1–1.

> ## Accepted historical characteristic-zero prior resolution

Outcome evidence: `evidence/pr1146/PR_BODY.md` lines 3–3.

> Adds the complete substantive source-credit audit and proof reconstruction for 30002482 / OWR-12863-001. Credit belongs to Arnab Mitra, Omer Offen and Eitan Sayag, [Klyachko Models for Ladder Representations](https://ems.press/journals/dm/articles/8965505), Documenta Mathematica 22 (2017), 611–657, Theorem 10.3 / Theorem 1.2, [DOI 10.4171/DM/574](https://doi.org/10.4171/DM/574).

## PR #1147 — partial_or_unsolved

Problem 30002326; head `6c9ec263988e86425af39ead0a0132aa127c39ce`.

The global homometric sublinearity question is expressly unresolved; exact flower-class bounds are partial.

Outcome evidence: `evidence/pr1147/PR_BODY.md` lines 7–7.

> The proof retains all construction details, odd-clique domination, both cone root states, the j=0 boundary and exact integer rounding. The entire flower class has asymptotic minimum ratio 1/4. This is PARTIAL: neither direction of the global sublinearity question is resolved, and no global positive linear lower bound is claimed. Necessary degree, diameter and two-distance restrictions are retained.

## PR #1148 — explicitly_prior_full_resolution

Problem 30002562; head `b8b29d9c86f4413d6b27b339c4e89c72592d4a72`.

The edition explicitly presents the exact all-degree threshold as a credited prior-result implication of BDIM Theorem 4.5; pinned README confirms that attribution.

Boundary/ambiguity: The authored bridge is accepted, but the title and README frame the target as a consequence of credited prior work, not a new full original-target solution.

Outcome evidence: `evidence/pr1148/PR_BODY.md` lines 3–3.

> For problem 30002562, this exposition proves alpha(k) >= k^2 + 1 for every integer k >= 3 as a consequence of Theorem 4.5 of Erwan Brugallé, Alex Degtyarev, Ilia Itenberg and Frédéric Mangolte, [Real algebraic curves with large finite number of real points](https://doi.org/10.1007/s40879-019-00324-9), European Journal of Mathematics 5 (2019), 686-711. The existence construction and patchworking foundations are credited prior mathematics. No novelty is claimed.

Outcome evidence: `gate_reviews/lower/pr1148/README.md` lines 7–9.

> For every integer k >= 3, the specified threshold satisfies alpha(k) >= k^2 + 1. Here alpha(k) is the least integer A such that every real positive semidefinite homogeneous ternary form of degree 2k with more than A distinct zeros in RP^2 has an indefinite square factor.
> 
> The existence input is Theorem 4.5 of Erwan Brugallé, Alex Degtyarev, Ilia Itenberg and Frédéric Mangolte, *Real algebraic curves with large finite number of real points*, European Journal of Mathematics 5 (2019), 686-711, [DOI 10.1007/s40879-019-00324-9](https://doi.org/10.1007/s40879-019-00324-9). This is a credited consequence of prior work, with a complete authored bridge from finite real curves to the threshold. No novelty is claimed.

## PR #1149 — partial_or_unsolved

Problem 30002668; head `862ead0f219817db0bbb306b19aa98b731110b89`.

The uniform quadratic-length single face-simple dual-path target remains unresolved; disjoint cycle packing is partial.

Outcome evidence: `evidence/pr1149/PR_BODY.md` lines 7–7.

> This is PARTIAL. The original uniform quadratic-length SINGLE face-simple properly colored dual-path target remains unresolved. Aggregate length across disjoint cycles is not a single-path bound. No counterfamily to the exact balanced three-color target is accepted. The justified single-path bound remains the source-derived 3n edges, obtained by coarsening colors and using Aichholzer et al., Theorem 3.2. A supporting geometric line may be crossed more than once; only faces must be distinct. No periodic RGB word is required.

## PR #1150 — explicit_full_solution_claim

Problem 30003045; head `99f43020e142374629848e97113d354b43fd9f8e`.

The PR explicitly claims a full negative answer under the original arbitrary finite purely inseparable hypothesis at an allowed index.

Boundary/ambiguity: The n=0 equality and exponent-one predecessor are separate boundaries; later audit must verify the original binary-quadric convention.

Outcome evidence: `evidence/pr1150/PR_BODY.md` lines 3–3.

> Problem 30003045, Question 2 in Ahmed Laghribi's contribution (joint with Roberto Aravire and Manuel O'Ryan) to [Oberwolfach Report 5/2016](https://ems.press/content/serial-article-files/46609), asks whether a mixed Kato kernel is always the sum of three individual kernels. This edition gives a full counterexample under the original arbitrary finite purely inseparable hypothesis, at the allowed index n = 1. The original n = 0 equality is proved separately to hold. No failure at every index or every field is claimed.
