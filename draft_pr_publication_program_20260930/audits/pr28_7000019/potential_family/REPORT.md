# Potential/PDE adversarial audit of PR28

**Verdict: PASS for the original scoped partial theorem. No mandatory mathematical repair identified.** The full one-width convex-surface target remains unresolved. This audit is independent AI analysis, not external peer review or a priority certification.

Target: 7000019 / AMR-069-0019. Original head: `90a81313f3f65a7914fb6d5a9950fa087ea7467e`. Frozen original proof SHA-256: `147b64bc267744e83ede73f7e89200c21931585f91e3e639cf0efc7bd7de5e46`.

## Independence and exact input

Before reading any original mathematical artifact, old review/script, sibling-family artifact, or history, I reconstructed the source quantifiers and the entire potential route in EARLY_INDEPENDENT_RECONSTRUCTION.md. Its sealed SHA-256 is `3b44e662a84376d5f9fb989476d8813c70e486eb602116123e64ad40536dcaf7`. Later clarifications are separate.

I read all 17 frozen original files. inventory_receipts.json independently recomputes their lengths, SHA-256 digests, and Git blob IDs and matches each byte-for-byte to the exact original Git head. It also checks the 18 changed paths: those 17 plus QUEUE.md. The queue row moves from queued 0/5 to unsolved 2/5. attempt.json and the original research log agree on two substantive attempts out of five; this verifies the recorded ledger, not unobservable historical model turns. The shared queue, canonical attempt, Git state, PR, and frozen source bytes were not mutated by this family.

The literal [survey Problem 4.3](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), printed page 12, fixes one plane separation below the diameter. [Ghomi's earlier author formulation](https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere) explicitly makes the surface the boundary of a compact convex body with interior points and requires 0 < h < d. Both planes must meet the surface. The hypothesis is one common area over all admissible positions and directions. The submitted theorem adds C^{2,alpha} boundary, 0 < alpha < 1, and the strict inequality h < 2 r_in. It does not claim these additions from the original hypothesis.

## Universal step verified by proof

Let a = h/2, D = int K, S = boundary K, and E = {x in D: dist(x,S) > a}. The surface measure is finite, from a finite smooth atlas (or compact Lipschitz graph cover for a general convex boundary). The maximum of the continuous distance function on K is the inradius and occurs at an interior point. Since a < r_in, the 1-Lipschitz distance function gives a nonempty open ball in E.

For x in E, a ball of radius greater than a about x lies in D. Each centered plane at u dot x +/- a cuts the interior. Its compact planar section contains a disk, and its relative boundary lies on S. Thus both planes meet S, and the original constant-area hypothesis applies to every centered strip.

For any vector z with |z| > a, rotation to the polar axis gives a longitude-height area element dphi ds on the direction sphere. The allowed height interval is [-a/|z|, a/|z|]. Therefore its direction area is exactly 4 pi a/|z|. The joint strip indicator is Borel, bounded, and nonnegative; Tonelli applies to the finite measures without any conditional integration. Every source point is at distance greater than a from x in E. Hence

    4 pi C = 4 pi a integral_S |x-y|^{-1} dA(y).

The unnormalized potential P is 2C/h throughout E. This is a universal analytic argument, not a sampling inference. It proves the candidate's central step. The actual average at arbitrary center x is integral_S min(1, a/|x-y|) dA(y), with value one for a source at x. Keeping a/|x-y| when the distance is below a is false. Dimension three is essential: the uniform height marginal is special to S^2.

For any compact subset of D, all Newton-kernel derivatives are uniformly bounded against the finite source measure. Differentiation under the integral shows P is harmonic in D. D is connected by convexity. Analytic continuation from the nonempty open set E makes P constant on all of D. This does not continue through S and does not infer constancy from a single interior point.

## Rigidity and full relevant primary proof checked

I read the primary [Reichel paper](https://ems.press/content/serial-article-files/34877), DOI [10.4171/ZAA/719](https://doi.org/10.4171/ZAA/719), Section 2 on printed page 622 and the full relevant Section 4/Appendix 1 on printed pages 624-633, in text and rendered pixels. The paper treats a bounded C^{2,alpha} domain with connected exterior and the kernel 1/(4 pi r). Its applicable case is the Laplacian exterior problem with constant boundary value, constant nonpositive derivative in the body's outward normal, and value zero at infinity. The moving-plane proof uses an exterior reduced half-space, maximum comparison, internal tangency or orthogonal-corner contradictions, and connectedness to establish global reflection symmetry. For the Laplacian its corner-lemma coefficient condition is automatic. No strict convexity, analytic boundary, or extra star-shapedness assumption is being imported.

The independently checked PDE hypothesis bridge is as follows. Put V = P/(4 pi). Positivity is immediate and V is harmonic off S. Its continuous boundary trace is the positive interior constant b. A local graph calculation gives the normalized normal jump -1 for density one. In flat tangent coordinates the singular contribution to the body's normal derivative from the two sides is -sign(t)/2; the remaining graph term has a common principal-value limit because its normal height is O(r^2). Subtracting sides gives -1. The interior derivative is zero, so the exterior derivative is -1. With the unnormalized P it is -4 pi. A normal pointing out of the exterior domain would reverse this sign.

The continuous trace follows by splitting off a small surface patch, where the integrable 1/r singularity contributes O(patch radius). Constant boundary data on a C^{2,alpha} graph then gives the exterior harmonic C^{2,alpha} boundary regularity required in Reichel's case (I). This avoids any stronger regularity claim for arbitrary merely continuous density.

The exterior of a convex body is connected. From an interior center, every exterior point can move radially out to a containing sphere without hitting K; that sphere connects the radial paths. At infinity V tends uniformly to zero, since V(x) <= area(S)/(4 pi (|x|-max_S |y|)). The maximum principle on truncated exterior domains and then the strong maximum principle yield 0 < V < b outside K. Thus all the published hypotheses hold exactly and Reichel forces K to be a ball. The candidate's use of that theorem is valid.

The fetched primary PDF SHA-256 is `611cbd838fe69bde03c1ffe16343d85eba09dc6cab3ca1e46c6014be25b9d4c0`, identical to the original provenance record. Foreign PDF bytes and rendered images remain only under the ignored tmp directory.

## Adversarial controls and verifier limits

The original verify.py and preserved submitted_verify.py each reproduced all 1,056 controls. The original independent checker reproduced all 266 controls and its original JSON exactly. Copies ran under an ignored, isolated tmp directory because the old independent checker writes adjacent output. No installation was needed: /usr/bin/python3 provided SymPy 1.14.0. replay_receipts.json records the exact copied-script hashes and results.

The independently authored new_controls.py imports no submitted or old-review code. Its 20 named controls pass, and 10 explicit mathematical mutants are rejected. They include saturating versus unsaturating the band kernel, dimensions two/five, exact off-center sphere integration, full/half width, direction normalization, normalized/unnormalized jump, body-normal sign, equality at the inradius threshold, and continuation from one point.

The variable-density falsifier is an explicit exterior dipole potential v = 1/r + epsilon t/r^2, t = cos(theta), and its level v = 1. For epsilon = 1/20 the radial boundary is r(t) = (1 + sqrt(1+4 epsilon t))/2 > 9/10. It is smooth, encloses the singularity, and has connected exterior. v decreases radially there, so rho = -partial_nu v = |grad v| is positive. Extending v by the constant one inside the boundary gives distributional -Delta v = rho dA; subtracting the normalized single layer with density rho gives an entire decaying harmonic function, hence zero. The density is directly nonconstant: at the equator rho = sqrt(1+epsilon^2) > 1, whereas at a pole the level equation gives rho = (2r-1)/r^2 = 1-(r-1)^2/r^2 < 1. This nonball therefore has a constant interior potential with a positive variable charge. It is not any sphere: its equatorial radial derivatives are epsilon and -2 epsilon^2, whereas a rotational sphere through equatorial radius one with the required center shift has derivatives epsilon and +epsilon^2. This falsifies dropping uniform density from the general electrostatic statement. It is not a strip-problem counterexample.

A bounded deterministic ellipsoid diagnostic uses axes (3,2,1), h = 0.8, and core points (0,0,0), (0.5,0,0), (0,0,0.5). Their normalized uniform potentials at the finer resolution are approximately 2.1166770382, 2.1079973138, and 2.1340888522: variation 0.0260915384. Doubling quadrature resolution changes values by at most 1.854e-9. This convergence comparison has no rigorous quadrature error bound and proves no universal statement. It only checks that the implementation does not incorrectly assign constant potential to a smooth nonsphere.

Four deliberately corrupted copies of the original proof still pass the original arithmetic verifier: dropping the factor two, replacing the strict core condition by a diameter bound, replacing the open continuation set by one point, and replacing constant density by an arbitrary positive density. This is expected because verify.py never reads PROOF.md. The analytic proof and exact source hypothesis check are the evidence for the universal result; finite assertion counts are not a proof certificate. The original package already says this clearly, so the limitation is not a mandatory repair.

## Remaining gap and disposition

At h >= 2 r_in the particular strict core E is empty, so this mechanism has no open set on which to establish Newton-potential constancy. Even equality supplies no starting set. A smooth ellipsoid of axes (3,2,1) has inradius one and diameter six, so h = 5/2 satisfies h < diameter while the core is empty. It is a width-boundary control, not an alleged strip counterexample. The original tetrahedron control also correctly refutes inferring the inradius bound from minimum width > h. A fresh mechanism would be required to reopen this route toward the full target. Nonsmooth rigidity extensions and historical priority also remain unverified.

All original auxiliary claims read consistently: the one-dimensional periodic-density example does not claim realizability as all-direction surface-area data; the nested spheres are explicitly excluded from convex scope; the minimum-width lemma includes tangent-plane intersection and is valid under that convention. No solved credit, preprint/DOI publication, or release should follow from this partial result.

**Strongest verified result:** the original C^{2,alpha}, h < 2 r_in convex-body theorem, including its universal averaging and continuation steps and exact published rigidity application. **Required repairs:** none in this family's mathematical scope. **Completion estimate:** 100% of this family audit; no new claimed progress toward a full resolution of target 7000019.
