# Independent adversarial audit: 30001408 / OWR-4199-001

Date: 2026-10-05 UTC. Rank: 696. Target: invariant homogeneous extended-valued valuations on origin-interior convex bodies.

## Verdict

**PASS WITH REQUIRED MATHEMATICAL CORRECTION, for an unsolved / five-approach research packet only.** The frozen source packet is not correct without the correction. Its Section 5 omits the right-limit-at-zero hypothesis in one claimed implication. `CORRECTION.md` supplies the controlling replacement, a complete counterexample to the original inference, and every downstream dependency. With that replacement authoritative, the retained partial results withstand this audit. No complete classification, mixed-infinity example, global openness claim, or historical novelty claim is certified.

The author's seven manifest-bound files and the manifest itself remain byte-for-byte unchanged. The original manifest hash is `938d14791569ca0c77c9f19b13a71bd33219df81395d778c86e6703300c9bb34`. The author controls reproduce exactly: 15,200 assertions. The separate audit controls pass 28,270 checks, including ten deliberately false mathematical alternatives and eight in-memory tamper cases. These finite checks are supplementary evidence, not proofs of a statement about every convex body.

This is a fresh review by a separate AI reviewer, without helper agents or remote writes. It is not human peer review or formal theorem-prover certification.

## 1. Scope, binding, and source inspection

The review read the entire frozen `RESULT.md`, `APPROACH_LOG.md`, `SOURCE_VERIFICATION.md`, README, manifest, and both Python scripts; replayed the supplied controls; and wrote independent controls rather than merely trusting the author's output. The bound defect location is the Section 5 paragraph on line 127 of `RESULT.md`; its exact text hash is in `BINDING.json` and `CORRECTION.md`.

All four public PDFs cited below were freshly retrieved independently of the author's local copies. Their byte counts and SHA-256 hashes match the author's recorded metadata. Text inspection was supplemented by locally rendered visual inspection of OWR printed p.149, Annals printed pp.1221 and 1262, and Ludwig manuscript p.14. The web tool's PDF screenshot route returned cache errors; local rendering of the successful fresh downloads supplied the visual evidence instead. Only bibliographic details, public URLs, hashes, sizes, inspection history, and authored analysis are included in this audit packet. PDFs, extracts, rendered images, dataset contents, and private coordination material are excluded.

Primary inspected sources:

- Reitzner, *Affine invariant notions of surface area*, in *Mini-Workshop: Valuations and Integral Geometry*, Oberwolfach Reports 7 (2010), 141-178; relevant contribution pp.147-150. DOI: https://doi.org/10.4171/OWR/2010/04 . PDF: https://ems.press/content/serial-article-files/46262?nt=1 . Inspected the contribution and its references, with visual confirmation of p.149.
- Ludwig and Reitzner, *A classification of SL(n) invariant valuations*, Annals of Mathematics 172 (2010), 1219-1267. DOI: https://doi.org/10.4007/annals.2010.172.1219 . PDF: https://annals.math.princeton.edu/wp-content/uploads/annals-v172-n2-p09-p.pdf . Inspected definitions, Theorems 3-5, the discussion of dissection/extension obstacles, and Section 5's use of Theorems 26 and 5. The complete long proof of Theorem 5 and the older polytopal theorem were not re-proved.
- Ludwig, *General affine surface areas*, Advances in Mathematics 224 (2010), 2346-2360. DOI: https://doi.org/10.1016/j.aim.2010.02.004 . Author PDF: https://dmg.tuwien.ac.at/ludwig/gasa.pdf . Inspected the relevant family definitions, Theorems 6 and 9, Corollaries 7 and 11, equations (10), (16), (17), and Section 6 conjectures. Its full semicontinuity proofs were not independently reconstructed.
- Ludwig, *Geometric valuation theory*. Author PDF: https://dmg.tuwien.ac.at/ludwig/GeoVal.pdf . Inspected the finite scalar-valued affine classifications and their codomains, notably Theorems 2.4 and 2.7. This does not provide an extended-valued completion.

Three targeted current web searches were also performed for extended-valued SL(n) valuations, the exact upper-semicontinuity/infinite-value combination, and the cited conjecture. They did not produce a verified resolution of the literal target. This limited search does not establish global open status. The audit did not independently repeat the author's repository, catalogue, or prior-attempt searches; those remain author-reported provenance rather than mathematical evidence. No uninspected upstream dataset is represented as byte-verified.

## 2. Exact target and neighboring-source mismatch

The OWR p.149 target really uses upper semicontinuity. Its codomain notation is R^+ together with infinity; a nearby displayed definition on the same page uses R_0^+. The printed distinction is visible. Thus the packet correctly avoids silently deciding whether zero is admitted and gives both interpretations. Strict positivity may be the intended reading, but the audit does not turn that notational inference into a settled editorial correction.

The target's final sentence does not separately restate a dimension lower bound or explicitly name a degree variable. The surrounding domain is K_0^n, with the origin in the interior. The packet's n>=2 analysis is its higher-dimensional scope, and it separately proves the n=1 classification. It does not apply the higher-dimensional finite-valued list to dimension one. The neighboring Annals definition specifies q real and dilation parameter t>0, which is the convention used here. No t=0 case, empty-set value, or body with origin merely on the boundary is imported.

The Ludwig conjectures visually inspected on manuscript p.14 use lower semicontinuity. They also have a different extended codomain and, in the homogeneous conjecture, explicitly concern degrees outside [-n,n]. Its negative-p constructions in the two stated parameter ranges are infinite on polytopes and finite on balls. This precludes upper semicontinuity along origin-interior polytopes approaching a ball. The mismatch is real; no evidence inspected authorizes changing the OWR word to lower or treating the lower-semicontinuity conjectures as resolved.

SL(n) invariance and q-homogeneity imply GL^+(n) covariance: for A with positive determinant, write A=tS with t=(det A)^(1/n)>0 and S in SL(n). Then Phi(AK)=t^q Phi(K). This preserves infinite versus finite values because t^q is finite and strictly positive. Reflection invariance is not assumed. In particular SL(1) is trivial, and one-sided endpoint formulas must remain possible in dimension one.

## 3. Finite-valued boundary and extended arithmetic

The Section 2 finite list agrees with Annals Theorem 4 under the stated higher-dimensional scope. The real-valued theorem gives the nonnegative affine-surface-area coefficient. At degree zero evaluation on a polytope forces the constant term nonnegative. At degrees +/-n positive volume forces its coefficient nonnegative. Under strict positivity, a positive constant at degree zero or a positive volume coefficient at +/-n is necessary; intermediate positive-p affine surface areas vanish on polytopes. Degrees outside [-n,n] have only the zero finite valuation, disallowed by a strictly positive codomain.

Everywhere infinity is admissible under the literal extended-semigroup interpretation and every real degree: both sides of each valuation identity are infinity, homogeneity uses only positive finite multipliers, and upper semicontinuity at infinity is automatic. There is no properness condition in the inspected target line. If a later authority supplies such a condition, this degenerate case must be reconsidered; none is silently added here.

No infinity subtraction or zero-times-infinity is used in a retained proof. Cancellation from infinity+x=infinity+y would be invalid and is explicitly rejected by the audit controls. Even when the Boolean support condition holds for an all-finite quadruple, its numerical valuation identity is an additional requirement; the reconstruction proposition correctly includes it.

The finite theorem cannot by itself classify mixed finite/infinite maps. Its proof begins with a real-valued polytopal classification and subtracts finite elementary terms before invoking a real-valued representation theorem. Those hypotheses are absent for a general mixed map. Truncation fails even for length: the valid values 4,4,6,2 become 4,4,4,2 at cutoff 4. Products with a fixed origin-interior factor preserve this witness in higher dimensions. This rejection is exact and not dependent on asymptotics.

## 4. Infinite support and finite-locus reconstruction

Let X=K_0^n, I={Phi=infinity}, F=X minus I. For upper semicontinuity in the Hausdorff metric, each strict finite sublevel {Phi<m} is open. Their union is F. Therefore F is open and I is closed in X, not necessarily in an enlarged space that also contains degenerate bodies. At a finite K choose a finite M>Phi(K); this same sublevel gives an actual locally bounded-above neighborhood. Density of polytopes then supplies finite polytopes in that neighborhood. It does not show that all polytopes, or all bodies, are finite.

For an admissible K,L, both contain a ball about zero, so their intersection does too. The union is required to be convex. A sum of two values in [0,infinity] is infinite precisely when one is infinite. Hence the exact condition is

(K in I or L in I) if and only if (K union L in I or K intersection L in I).

Closedness and GL^+ invariance were justified above. This establishes Proposition 3.1 without cancelling anything or assuming monotonicity. A support containing every polytope is all of X by closedness and density. The dual observation for a dense smooth positive-curvature class is equally valid.

Conversely, take any closed GL^+-invariant I satisfying that Boolean equivalence. Assign infinity on I and the constant 1 on F. At points of F an entire neighborhood has value 1; at points of I upper semicontinuity imposes no bound beyond infinity. The valuation identity is either infinity=infinity or 2=2. This proves the degree-zero, strictly positive converse. If zero is allowed, the 0/infinity version works at every real degree because multiplying zero or infinity by a finite positive scalar preserves it.

The qualification “mixed” means I is nonempty and proper. Such an I produces a genuinely mixed degree-zero map; conversely any mixed map supplies such an I. If I is empty the map is the finite constant 1. If I=X the map is everywhere infinity, F is empty, and the finite-part conditions below are vacuous. These edge cases do not invalidate the equivalence, but neither is a mixed example.

For Proposition 3.3, F is invariant under the same transformations and open. Relative upper semicontinuity of a finite f on F is enough for its extension at every point of F, since a sufficiently small ambient neighborhood avoids I. At a point of I the extension is automatically upper semicontinuous. The Boolean condition handles every quadruple that meets I; for an entirely finite quadruple the assumed identity for f is necessary and sufficient. There is no missing boundary-gluing limit condition, because the prescribed boundary value is infinity and the semicontinuity direction is upper. The converse restriction properties follow immediately. This remains valid for F empty and for either positivity convention.

The resulting description is an exact reduction, not a classification: the proper closed invariant Boolean supports and their compatible finite functions have not been determined.

## 5. Every proposed infinity construction

**Origin asymmetry.** For origin-interior K, r(K)=max over unit u of h_K(u)/h_K(-u); the maximum is at least 1 and finite. Support functions vary uniformly under Hausdorff convergence, and their denominators stay uniformly positive near a fixed K. Thus r is continuous. Applying an invertible map preserves the inclusion defining r, giving invariance. The proposed closed supports have the required topology and invariance but fail Boolean compatibility. The two crossed boxes have profiles 2,2,1,1. Their union really is the larger box, since only the first coordinate varies and the common remaining factor is identical. Their intersection is the smaller box, and all contain zero in their interiors. Any threshold in (1,2] gives infinity on the left and finite values on the right.

**Centered ellipsoids.** For 0<a<1 the two opposite caps of B overlap around zero, their union is B, and their intersection is the central slab of B. Each capped body and the slab has a genuine (n-1)-dimensional flat facet; no such body is an ellipsoid for n>=2. Thus neither original body is in the proposed support, but the union is. This fails the reverse implication of the Boolean condition. Origin-interiority and union convexity both hold. No one-dimensional use of this facet argument is allowed.

**Infinity on every polytope.** Since origin-interior polytopes are dense in X, closedness of I forces I=X. In particular a finite ball value cannot coexist with this support in an upper-semicontinuous map.

**Infinity on every smooth strictly positively curved body.** Such bodies are dense among origin-interior convex bodies; smoothing support functions and adding a small positive spherical component gives standard approximants. Closedness again forces I=X. A proposed finite polytope value contradicts this directly.

**Trivial supports.** Both I empty and I=X pass the Boolean condition, as they should. The audit does not mislabel their constructions as mixed or as counterexamples to a dichotomy.

These are counterexamples to construction mechanisms, not to the original request for a classification. The written proofs, rather than the finite coordinate controls, establish their all-dimensional scope.

## 6. Curvature powers, repaired inference, and endpoints

The curvature-density representation is explicitly an additional ansatz. The ball computation is correct: curvature scales as r^(-(n-1)), the support factor as r, the centro-affine curvature as r^(-2n), and total cone measure as n omega_n r^n. Thus q-homogeneity with finite g(1)=c forces g(s)=c s^((n-q)/(2n)) for s>0. It says nothing about the value at zero. This distinction is especially important for c=0.

There is one required repair. Concavity, an assigned value g(0)=0, and sublinear growth at infinity do not imply that alpha>0. The step function equal to c>0 on the positive half-line and zero at zero is a complete counterexample. `CORRECTION.md` restores the separate right-limit-at-zero condition from the source, proves the repaired iff statement, and has controlling precedence over the frozen paragraph. The proof now excludes alpha=0 for an actual reason. It does not extend any finite-valued representation theorem to the mixed setting.

For 0<alpha<1, Holder gives

integral kappa_0^alpha dmu <= (mu(boundary K))^(1-alpha) (integral kappa_0 dmu)^alpha.

The two finite factors are bounded by n V_n(K) and n V_n(K*) respectively. The latter measure inequality is explicitly present in Ludwig equation (17), with equations (10) and (16) explaining the full measure and its absolutely continuous part. Both volumes are finite because K is compact and contains a ball about zero. Multiplication by c preserves the claimed bound. This argument cannot produce a mixed-infinity member in that range.

For alpha>=1 with g(0)=0, the rounded-cube test is geometrically valid. On a fixed spherical patch E strictly inside a vertex normal cone, x=v+epsilon u lies on P+epsilon B, its area element is epsilon^(n-1) d sigma, and its Gaussian curvature is epsilon^(-(n-1)). The support factor v dot u+epsilon is bounded above and bounded away from zero uniformly for 0<epsilon<=1. The patch contribution is therefore bounded below by a positive constant times epsilon^((n-1)(1-alpha)). For n>=2 this diverges when alpha>1 and remains positive when alpha=1. The cube integral is zero. The sequence converges in Hausdorff distance, so upper semicontinuity fails. The argument does not require the entire rounded cube to have positive curvature or to be globally smooth.

For negative powers with g(0)=infinity, polytopes have infinite values and balls have finite ones, giving the independently valid density obstruction. The packet does not establish an exhaustive classification of all conceivable discontinuous zero assignments or arbitrary extended densities; it correctly retains its representation gap. No such broader conclusion is certified by the audit.

For alpha=0 with g(0)=c the functional is c n V_n. With g(0)=0 it is the jump-density case discussed in the correction, and the superellipsoid sequence supplies a separate, complete upper-semicontinuity counterexample. The boundary is smooth because its defining polynomial has nonzero gradient on the level set; away from coordinate-zero sections its Hessian is positive definite, giving positive Gaussian curvature. The exceptional sections have surface measure zero. The explicit cube inclusions establish volume convergence, so there is no unsupported interchange of a singular curvature limit and integration.

At alpha=1, the absolutely continuous curvature integral alone is not polar volume. Polytope facets have zero Gaussian curvature almost everywhere while polar volume is positive. The source's full measure includes a singular part, resolving this endpoint distinction. The correction does not change it.

## 7. Dissection propagation and domain traps

The Boolean equivalence also says that K and L are both finite exactly when their admissible union and intersection are both finite. It does not imply that a finite union alone bounds both pieces, nor does one finite summand allow cancellation of infinity on the opposite side.

Cuts through zero leave the domain because zero lies on the new facets and the intersection is lower-dimensional. Offset cuts can preserve origin-interiority but introduce a full-dimensional intersection whose finiteness still needs proof. These are valid reasons that the proposed propagation proof is incomplete. The audit does not assert that no different propagation argument could work.

For a deliberate domain-negative control, two crossed rectangles in R^2 have a nonconvex union. A midpoint of a point in each rectangle lies in neither. Replacing this union by its convex hull changes the volume identity: the sum of the two areas is 16, while convex-hull plus intersection area is 18. Such a hull substitution is not a legal repair of admissibility.

The phrase about dense finite polytopes at the end of frozen Section 6 must not be read as an established global density theorem for its unknown finite locus. What Section 3 proves is local boundedness and local finite polytopes near a finite body; that is sufficient for the stated obstruction discussion, not for global finiteness. No downstream proof in the packet relies on the stronger reading.

## 8. Complete one-dimensional theorem

Every interval in the domain is [-a,b] with a,b>0, and unions of two such intervals are automatically intervals with zero interior. Suppose [-a0,b0] has finite value. All positive dilates do. For an arbitrary [-a,b], put lambda=a/a0 and mu=b/b0 and use the companion [-mu a0,lambda b0]. The union and intersection have both endpoint coordinates equal to max(lambda,mu) and min(lambda,mu) times those of the initial interval. Thus both have finite values. Their valuation identity forces the arbitrary interval finite. No continuity is needed, and infinity-minus-infinity never appears.

Once finite everywhere, the rectangular modular identity follows by selecting the crossed pair according to the ordering of a versus 1 and b versus 1. In each of the four order patterns, the valuation identity yields F(a,b)+F(1,1)=F(a,1)+F(1,b). Hence F=C+u(a)+v(b), with u(1)=v(1)=0. Homogeneity, compared with the same equation after setting a=1, gives u(ta)=t^q u(a)+u(t). Interchanging a,t and choosing t^q!=1 when q!=0 forces u(a)=A(a^q-1), and likewise for v. Diagonal homogeneity makes C=A+B. Because a^q and b^q vary independently over all positive numbers, nonnegativity forces A,B>=0. Strict positivity is equivalent to A+B>0.

When q=0, u is multiplicatively additive and v=-u. Then F(a,b)=C+u(a/b). Integer powers in either direction make any nonzero value of u produce arbitrarily negative values, contrary to nonnegativity. Thus u=0 and F=C. Strict positivity requires C>0. The converse formulas are valuations since max and min only reorder the endpoint powers. These functions are continuous as a consequence, not as an assumption.

Reflection symmetry would impose A=B, but SL(1) alone does not. The audit explicitly tests an asymmetric endpoint example. The one-dimensional formulas cannot be transplanted into the n>=2 finite list: for example q=2 and F([-a,b])=a^2 is valid in dimension one despite |q|>1. Nor does the crossed-dilate proof generalize automatically, because its higher-dimensional union need not be convex.

## 9. Five approaches and final boundaries

The record supports five distinct mathematical lines, rather than five tool actions:

1. Transfer of the finite-valued classification and failure of truncation.
2. Exact algebraic/topological reduction to invariant infinity supports and finite parts.
3. Construction and rejection of specific geometric supports.
4. Curvature representation/power analysis and genuine geometric semicontinuity tests, with the required zero-endpoint repair.
5. Finiteness propagation through dissection, including a complete independent low-dimensional comparison and explicit higher-dimensional obstacles.

The elapsed-time labels and subjective progress percentages in the author's log are not independently measured or calibrated by this audit. The substantive distinction between the approaches is supported by the written work. Neither documentation nor these checks count as a sixth proof approach. “Unsolved, 5/5 used” accurately describes this attempt after correction; it is not a proof that the problem is globally open today.

The unresolved task is still to classify the proper closed GL^+-invariant supports satisfying the Boolean condition and their compatible finite pieces, or to prove the finite-everywhere/everywhere-infinite dichotomy. None of the review's arguments fills that gap. The partial constructions' historical novelty is not assessed. Publication must preserve the unrefereed, AI-assisted status and include the controlling correction rather than claiming an unconditional audit pass.

## 10. Replay and limitations

Run `python3 audit_controls.py /path/to/original/safe_output`. With the original sibling layout, the argument can be omitted. This uses only Python's standard library, performs no network request, preserves the original bytes, reproduces the author's control output, checks independent algebra/geometry samples, and checks before/after hashes. Its JSON output must match `AUDIT_RESULTS.json` byte-for-byte.

The ten deliberate mathematical negatives cover Boolean AND substitution, omitting finite-part equality, invalid infinity cancellation, forced reflection symmetry, asymmetry and ellipsoid supports, scalar truncation, convex-hull substitution for union, the omitted zero right-limit, and reversed semicontinuity. The separate eight in-memory byte mutations show that the pinned hashes detect changes without modifying the actual source files.

The 28,270 count includes integrity and replay checks as well as mathematical consistency samples. It must not be described as 28,270 independent proofs, random trials, or a probability of correctness. Integer-power interval tests supplement a written proof for every real degree; rational exponent checks supplement a written real-parameter argument. Local geometric proofs and credited curvature-measure facts remain essential. This is the stopping boundary of the audit.
