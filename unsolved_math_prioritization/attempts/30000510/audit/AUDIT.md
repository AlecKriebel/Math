# Independent adversarial audit: Baby Teichmüller space

## Decision

PASS for the explicitly stated scope: connected components and ordinary singular homology/cohomology with a constant abelian coefficient group, for every integer n >= 3. No blocking mathematical defect was found. The frozen reconstruction correctly verifies an attributed prior result, rather than establishing novelty. The recommended disposition is **already_solved / prior result verified, singular scope**, with **one substantive approach out of a maximum five**. This audit does not create four additional attempts.

The original problem leaves the cohomology theory unspecified. Consequently this decision must not be promoted into a certification of every interpretation of that word. It is not a certification of the entire prior preprint, human peer review, formal proof checking, or historical priority.

## Immutable object audited

- Problem: rank 657, ID 30000510, code OWR-1275-010.
- Author manifest SHA-256: 37cf18bd16178ae4c8cc7aefc84712dff2bed750cb5e91e10fdd8a4c556007f1.
- Author archive SHA-256: 9aeff19fabf35423f3e8a169212ebf47e56e306d7a55bd323cce1eca7628251e.
- All ten listed author files match their declared sizes and hashes. The eleven archive entries comprise precisely that manifest and those ten files; their decompressed bytes match, with no extraneous members.
- The original files were read without alteration. Audit artifacts are separately bound by AUDIT_MANIFEST.json.

## 1. Source statement, interpretation, and prior credit

The original source is *Teichmüller Space (Classical and Quantum)*, Oberwolfach Reports 3 (2006), Problem 6 on printed page 1607, posed by Volodya Fock. Both its text and page image were inspected. The definition uses maps on a cyclically indexed finite set, prohibits equal adjacent values, requires at least three image points, and takes the quotient by SL(2,R). It does not require all values to be distinct. It does not quotient labels or reflections. It gives no explicit lower bound on n and specifies neither a cohomology theory nor coefficients. For positive n, the at-least-three condition makes n >= 3 exactly the nonempty range; n = 1 and n = 2 are empty. No claim is made about n = 0, which is outside the finite-cycle convention.

The reconstruction explicitly uses the product topology on configurations and quotient topology on the orbit space. This is a clear and natural interpretation, rather than an assertion that the source supplied additional topological wording. The EMS publisher page confirms report year 2006 and publication date 31 March 2007.

The relevant prior result is Alper Ferudun, *Components and Cohomology of Fock's Baby Teichmüller Space*, version 1.0, publication date 1 October 2026, DOI 10.5281/zenodo.23071801. The reading PDF, not merely the abstract or a verification report, was inspected. Theorem 1.1(iv) explicitly includes arbitrary abelian coefficients and singular homology as well as cohomology. The proof dependencies needed here are Lemma 2.1, Lemma 3.2, Proposition 3.3(b), and Proposition 3.4, with Lemma 3.1 supplying a second local-chart route. The complete relevant argument on PDF pages 2–4 was checked, including visual inspection of pages 3–4.

The public deposit and PDF identify the work as unrefereed; the deposit discloses AI-assisted preparation. Independent fresh retrieval of the PDF matched its frozen SHA-256 and size. The deposit is evidence of an accessible attributed prior manuscript, not of peer review. The source archive and third-party verification report were hash-checked, but their code was not executed and their assertions were not substituted for proof.

## 2. Universal reconstruction checked

### 2.1 Winding levels and the precise excluded locus

Regard RP1 as an oriented circle of circumference one. For each adjacent pair of different values there is a unique positive increment a_i in (0,1). The sum is an integer k in {1,...,n-1}. The starting circle value and the increments recover the full configuration continuously, with a continuous inverse. Branch discontinuities occur only when adjacent values meet, and those points are outside the domain.

The sum is invariant under PSL(2,R): this group is connected, and moving a fixed configuration through its action gives a continuous integer-valued winding function. SL(2,R) has the same orbits because its central kernel acts trivially. Passing instead to PGL(2,R) would merge k and n-k and would be a different problem.

Adjacent inequality permits a configuration with fewer than three values precisely when n is even and it alternates between two different points. In increment coordinates this is (t,1-t,...,t,1-t), with k = n/2. Thus no nonmiddle level is punctured, and there is exactly one removed alternating family in the even middle level. This checks the crucial distinction between allowing nonadjacent coincidences and requiring every point to be distinct.

### 2.2 Pair normalization is a homeomorphism of quotients

Let C be the configurations with first pair (infinity,0), and let D be their stabilizer in PSL(2,R). The stabilizer consists exactly of positive dilations. Negative dilations reverse projective orientation and are excluded. Every orbit meets C, and two points of C in the same full-group orbit differ by D.

The nontrivial step is topology, not this orbit bijection. On an open neighborhood of any ordered pair, choose one fixed third projective point outside both entries. The unique orientation-compatible projectivity from the reference triple depends continuously on the pair. After applying its inverse to a configuration, take the D-orbit in C. Different local choices differ by a projectivity fixing the first pair, hence by an element of D. The maps therefore agree on overlaps. For a full-group transformation h, the two local normalizers differ after inserting h by an element of D as well, proving invariance of the glued map. Its continuous descent to the original quotient is inverse to the map induced by C's inclusion. This establishes the required homeomorphism without properness or a separation axiom.

### 2.3 Local products establish a genuine bundle

For any index i >= 2, let C_i be the configurations in C whose i-th value is finite and nonzero. These invariant open sets cover C because a third distinct value exists. The map sending x to the pair consisting of |x_i| and the configuration divided by |x_i| has continuous inverse (r,y) -> r y. Its second factor has i-th coordinate +1 or -1. Positive dilation acts only on the first factor.

A group quotient map is open: the saturation of an open set is a union of open translates. Consequently each C_i/D is an open subset of the base, is homeomorphic to the second factor, and the restriction over it is its product with R_{>0}. Thus C -> B_n is an actual locally trivial bundle with contractible fiber, rather than a map whose fibers merely happen to be contractible. No global section, proper action, or numerability is presumed.

### 2.4 Why the non-Hausdorff base does not invalidate the singular argument

The applicable results are Hatcher, *Algebraic Topology*, Proposition 4.48 (printed pages 379–380), Theorem 4.41 (page 376), and Proposition 4.21 (pages 356–357). Their relevant proofs were inspected, with page images checked for Proposition 4.48.

For lifting a disk homotopy, pull back a trivializing open cover to its compact cubical domain. A sufficiently fine finite subdivision lies in individual trivializations. Extend successively using the retraction of a cube onto its bottom and sides; finite closed-domain pasting gives continuity. This uses compactness and metrizability of the domain, not Hausdorffness or paracompactness of the base. Hence the bundle is a Serre fibration. Its homotopy exact sequence and path lifting, with connected contractible fibers, yield a weak equivalence including the path-component bijection.

Weak equivalences induce singular homology isomorphisms for arbitrary spaces: finite singular cycles are represented by finite complexes, so the argument needs no separation property of the target. Universal coefficients supply cohomology. These facts do not imply a homotopy equivalence here; Whitehead's theorem cannot simply be applied to an unverified CW target.

### 2.5 Slice geometry and component count

Fixing the first pair fixes the initial angular coordinate and sets a_0 = 1/2. The winding-k slice is therefore the relatively open convex set

Y_k = {a in (0,1)^n : a_0 = 1/2, sum(a_i) = k},

of dimension n-2. It is nonempty: the remaining coordinates can all equal (k-1/2)/(n-1), strictly between zero and one for each allowed k. In the even middle slice the alternating family meets the constraint in exactly c = (1/2,...,1/2); that single point is removed. In other slices nothing is removed.

For the punctured middle slice put V = {v : v_0 = 0, sum(v_i) = 0}. For nonzero v with c+v in Y, let M be its sup norm. The homotopy

c+v -> c + ((1-t) + t/(4M))v

stays within Y: its norm is (1-t)M+t/4, lying strictly between zero and 1/2. It never reaches the removed point, ends on the radius-1/4 norm sphere, and fixes that sphere throughout. This is a strong deformation retraction of the slice, whose sphere has dimension (n-2)-1 = n-3. The strong assertion is made only for this ordinary slice, not for B_n.

For even n >= 4 that sphere has dimension at least one, so the punctured slice is path connected. The other slices are convex and path connected. Their images under the quotient are path connected, nonempty, and separated by the continuous discrete winding invariant. There are exactly n-1 connected as well as path components. Each nonmiddle component is weakly contractible; the middle component is weakly equivalent to S^(n-3).

### 2.6 Constant coefficients, homology, and the ring

For every abelian group A, the result is H^0(B_n;A) = A^(n-1), one additional A in degree n-3 when n is even, and zero in every remaining positive degree. Ordinary singular homology has the same degree pattern. There are finitely many components, so no infinite-product/direct-sum ambiguity occurs. A means a constant coefficient group; no statement about arbitrary twisted local systems is intended.

As a separate algebraic cross-check, the integral homology in these degrees is free. In universal coefficients all Ext and Tor correction terms therefore vanish, so torsion, divisible, and infinitely generated choices of A introduce no missing groups. For even n the degree n-3 is positive; thus the extra group never conflicts with H^0 in the stated range.

For integral cohomology the degree-zero idempotents act by restricting to their components. The sole positive generator belongs to the middle component. Its square vanishes because degree 2(n-3) is a zero group, not merely because its degree is odd. This verifies the stated ring consequence.

## 3. Adversarial boundary and scope checks

- **n = 1,2:** the admissible space is empty. The positive-range restriction prevents an invalid negative-degree sphere or spurious H^0 term.
- **n = 3:** all three values must be distinct. There are exactly two oriented triple orbits, each a point. This gives A^2 in degree zero and no positive cohomology.
- **n = 4:** the middle normalized slice is a punctured two-dimensional convex set, giving weak circle type and H^1 = A; two other components contribute only degree zero. There is no middle S^0 case within the theorem.
- **All even n >= 4:** the author's common-orbit sequence has different admissible limits. In one limit even coordinates are constant and odd coordinates are not; the opposite holds in the other. Equality patterns are preserved by every projectivity, so the limits are distinct orbits. Adjacent inequalities, the third-value condition, and the final-to-first adjacency all hold. This verifies non-Hausdorffness and the need for caution about strong conclusions.
- **Free action alone / contractible orbits alone:** neither was accepted as a substitute for the explicit local products.
- **Connected versus path connected:** the winding-level proof verifies both, rather than inferring component count solely from H^0.
- **Other cohomology theories:** no Cech, sheaf, de Rham, compact-support, or orbifold/stack comparison is certified. The prior paper makes additional claims, but they are not needed here.
- **Scope of novelty:** the inspected prior theorem already supplies the claimed singular result with the same coefficient generality. Attribution and the one-approach early stop are appropriate. The audit does not independently certify repository search completeness or corpus-wide priority.

Two optional wording refinements are nonblocking: the source's n bound is inferred from its definition rather than explicitly printed; and the n=4 phrase “singular homotopy type” would be clearer as “weak homotopy type.” The surrounding frozen text already gives both qualifications correctly. No replacement author packet is necessary for the approved scope.

## 4. Reproduction and finite controls

The author control script and its manifest verifier were read before execution. Their imports and operations are local; no downloaded research code was executed. The manifest verifier passes for ten files. Running the author controls produces exactly the frozen 742-byte CONTROL_RESULTS.json, byte for byte.

A newly written independent control program does not import the author program. It tests a rational matrix implementation of pair/triple normalization, obtains the same small-n winding counts by exhaustive words instead of set partitions, exhausts binary words for the excluded locus, and probes the radial homotopy very close to the center and boundary with exact fractions. It passes:

- 210 distinct projective triples;
- 1,260 projective orbit and winding checks;
- 840 positive-dilation normalization checks;
- all 8,190 binary words of lengths 1 through 12, with exactly 12 adjacent-distinct words, all even alternating cases;
- 5,700 near-boundary radial checks;
- independently identical cyclic-order counts for n = 3,4,5,6.

Finite tests are auxiliary controls. The universal quotient, bundle, lifting, deformation, and coefficient arguments above are the basis of the decision. Neither executable enumerates or certifies all real configurations.

## 5. Artifact and release boundary

The audit contains this newly authored analysis, deterministic local code and results, public-source verification metadata, and content hashes. It contains no scholarly PDF, source transcription, third-party code archive, dataset content, credentials, or private coordination. No remote write, publication, or DOI creation was performed. A future draft-PR publication must retain the singular-scope qualifier, prior attribution, unrefereed status, and one-approach count.

## Public references

1. [Original problem report and bibliographic metadata](https://ems.press/journals/owr/articles/1275), DOI [10.4171/OWR/2006/26](https://doi.org/10.4171/OWR/2006/26), Problem 6, printed p.1607.
2. [Ferudun's archived preprint](https://doi.org/10.5281/zenodo.23071801), Theorem 1.1(iv), Lemmas 2.1 and 3.2, Propositions 3.3(b) and 3.4; version 1.0, 1 October 2026, unrefereed.
3. [Hatcher, Algebraic Topology, author-hosted edition](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf), Propositions 4.21 and 4.48, Theorem 4.41.
