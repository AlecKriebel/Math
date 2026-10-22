# Independent audit: segment mirrors, 5500031

Date: 5 October 2026 UTC. Rank 776; AMR-054-0031; TOPP Problem 31.

## Verdict

**The scoped mathematical results pass this independent audit. The unrestricted problem remains unsolved, with five of five approaches used.** No fatal proof defect was found. The accompanying addendum records one related-catalog completeness correction and two computational reporting clarifications. None changes the mathematical disposition. This is an independent AI audit, not human peer review, journal acceptance, or a novelty certification.

The original ten-file author freeze was not edited. Its ZIP SHA-256 is `7112c0fff3aaf9cbbd429af541d1e08b30677a380155382e5b96095e02ff57dd`; its manifest SHA-256 is `ed99d8e8d377db851e03a09bc1b30c9e94ed2b8cc17f5b0cb7c73827506a10fe`. All nine listed file digests and all ten archive members match. A replay from a newly extracted temporary directory reproduced the frozen 20,012-assertion result byte-for-byte.

An independently written normal-equation/Householder implementation passes **58,598 exact rational assertions**. It does not import the author's verifier. These are finite controls; the universal claims below were assessed from their proofs, not inferred from test density.

## Mathematical findings

### 1. Model, endpoints, and collision time

The proof distinguishes disjoint **closed segment pieces** from their supporting lines. Supporting lines may meet; in the concurrent theorem they all meet. The examples' closed segments are disjoint, independently checked using exact segment distances. For the four-mirror example, the minimum separation is 1/10.

For a nondegenerate transverse reflection on one straight segment, the outgoing line cannot encounter that same segment again before another reflection. Thus successive effective collisions involve different mirrors. With finitely many pairwise-disjoint compact closures, their minimum separation delta is positive. At unit speed, the kth collision time is at least (k-1)delta, not necessarily k delta: the first flight from the source can be arbitrarily short. This establishes the absence of finite-time collision accumulation. The n=0 and n=1 cases are immediate and do not require defining a minimum inter-mirror separation.

For a source in the closed convex hull, each finite leg between collisions stays in that hull. An infinite regular trajectory is therefore trapped, while a finite-reflection trajectory has an unbounded final straight tail. The equivalence is sound under the stated regularity and source-position hypotheses. A source already outside the hull cannot satisfy the proposed trapping requirement.

The regular-source proofs assume the source avoids all mirror closures. They do not silently discard possible endpoint sources from the original target. Endpoint hits are transparent in the authored target convention. The concurrent all-ray extension separately stipulates straight continuation of collinear grazing; it is not a conclusion for endpoint absorption. These qualifications must remain attached to publication.

### 2. Direct shadows and the four-mirror certificate

A compact segment separated from the source has its directions contained in a strictly smaller-than-semicircle closed arc. The sum-of-shadow-lengths criterion, and consequently direct escape for at most two mirrors, are correct in the source-clear setting.

The four-mirror arrangement blocks every initial direction. Below absolute slope 2 a vertical mirror is reached in its interior unless an earlier horizontal hit occurs. At or above absolute slope 2, the horizontal intercept has absolute x-coordinate at most 3/4, strictly within its half-length 9/10. This handles the vertical-mirror endpoint slope without treating an endpoint as reflective.

For 15/31 < m < 15/29, the first two collisions are exactly (1,m) and (-1,3m), and the outgoing direction again has slope m. The first collision lies below the top horizontal support, the second is strictly inside the left vertical mirror, and the next right-support crossing has height 5m>2. The only relevant top-support crossing has x-coordinate 2-3/(2m) on the middle leg, or 3/(2m)-4 on the final leg. Multiplying by positive 10m reduces the required gap inequalities to 15-29m>0 and 31m-15>0. At m=1/2 the top support is crossed at x=-1. All bottom mirrors are avoided. This is an analytic open interval of regular two-bounce escapes, not just a rational sample.

The independent certificate exactly matches the author certificate: direction (2,1), collisions (1,1/2) and (-1,3/2), followed by escape with outgoing velocity (2,1). The interval's two boundary slopes also escape in the transparent-endpoint convention, but encounter a horizontal endpoint and hence are not regular. This extra endpoint check is a control, not an enlargement of the authored open-interval claim.

### 3. Countability and finite-prefix control

The endpoint argument fixes a finite reflection word and one terminal endpoint. Unfolding supplies one endpoint image. A positive-length straight ray from the fixed source has at most one direction toward it; an image equal to the source gives none. Countably many words and finitely many endpoints give a countable exceptional set. Collinear first contacts must first traverse an endpoint. Absence of finite collision accumulation justifies using a finite prefix before any positive-time first singular contact.

For periodic trajectories, reversibility takes eventual periodicity back to the original state. A full return word yields one affine image of the source. Its nonzero displacement fixes the original direction; zero displacement cannot represent a positive-length unfolded return. The proof correctly permits repeated mirror labels, rather than counting only permutations.

For common k-label prefixes, the two unfolded kth hit points occupy a segment of length at most L. The identity

    ||t v-r w||^2 = (t-r)^2 + tr ||v-w||^2

for unit vectors, together with t,r >= (k-1)delta, proves the stated L/((k-1)delta) bound. Same infinite itinerary implies same direction. It does not bound the number of infinite itineraries. The uncountable-itinerary obstruction is correctly retained; finite tests and a vanishing diameter for each cylinder set cannot replace control of the union over all cylinders.

### 4. Concurrent and parallel supports

For concurrence at c, a collision point q has q-c tangent to the reflecting support, so its scalar product with velocity has no reflection jump. During free flight its derivative is 1 at unit speed. With no finite-time accumulation, integrating over finitely many collisions on each bounded time interval gives the claimed global radial-square polynomial. Its quadratic growth forces escape. The disk exit-time bound follows from the positive root of that polynomial, and the collision-count bound then follows from delta. No rational-angle restriction is needed.

The all-ray extension is valid when omitted endpoints and collinear grazing leave velocity unchanged. At those events the same invariant still has no jump. This extension uses the explicit convention, not the regular-source countability lemma.

For parallel mirrors, the tangential component of velocity is conserved. Every nonzero such component forces unbounded tangential position. Only the two normal directions remain possible traps. On the source's normal line, the open-mirror intersection points are a finite ordered set: bracketing adjacent points create a periodic two-mirror path, and an unbracketed source escapes after at most one reflection. Endpoint intersections are omitted. The independent controls include both behaviors.

### 5. Rational approximation and the quadratic obstruction

Finite regular escape is stable under small changes of the source-clear legal configuration: each collision has interior and transverse margins; after finitely many collisions the ray can be continued outside a containing disk with outward velocity. Compactness supplies positive nonincident-mirror margins on the finite portion. Rational-angle configurations are dense by small direction perturbations that preserve the closed-segment and source clearances. With the cited rational-angle theorem, this gives an open dense regular-escape set in the source-clear configuration space. It does not prove that the complement is empty or null. The author correctly leaves the uniform-time/clearance gap open.

For V(q)=q^T A q+2b^Tq+d, the reflected derivative jump equals -2(n.v)(gradient V(q).n). Both signs of incident normal velocity are locally admissible for a two-sided mirror, forcing gradient V(q).n=0. Its coefficients along the open segment give n^T A u=0 and n^T(Aa+b)=0. In the plane, symmetry makes n an eigenvector; positive definiteness makes its eigenvalue nonzero. Substitution of c=-A^{-1}b therefore puts c on every support. Conversely the centered squared norm works for any concurrent family. The three-line obstruction has a five-by-five full-rank constraint system on the five nonconstant coefficients, independently checked by rational row reduction. This only rules out the specified globally monotone positive-definite quadratics; it says nothing against other escape methods.

## Literature and status

The maintained [TOPP Problem 31 page](https://topp.openproblem.net/p31) was retrieved afresh and still states the general conjecture. Its HTML statement, with emphasis markup removed, exactly matches the selected imported statement hash. A bounded fresh search using the title, mirrors, Milovich, solution, and 2025/2026 terms found no general resolution. That negative search is not an exhaustive literature certificate.

The [2001 O'Rourke-Petrovici manuscript](https://www.cccg.ca/proceedings/2001/orourke-13443.ps.gz) was independently re-retrieved; its digest matches the author record. The full converted text and the image of internal page 3 were inspected. Its stronger aperiodic-cardinality conjectures are distinct from the all-light conjecture. Its periodic-direction argument is properly credited. The five-page retrieved manuscript is not confused with the four-page proceedings citation.

[Milovich's 2004 manuscript](https://www.tamiu.edu/~dmilovich/mirrors4.pdf) was re-retrieved with the same 289,897-byte digest. Definitions, relevant general statements, Corollary 3-8, the opening of Section 4, and the final theorem/corollary were inspected, with pages 1 and 28 checked visually. The rationality assumption concerns angles between supports, not rational Cartesian coordinates. Endpoint absorption only strengthens the escape conclusion needed here: a ray escaping that model avoids endpoints. The audit does not independently reconstruct all 28 pages or their dependencies.

The [Mitchell-Simon-Zhao 2012 article](https://msp.org/involve/2012/5-1/involve-v5-n1-p02-p.pdf) was re-retrieved with the same 659,557-byte digest. All six article pages were read; printed pages 9 and 11 were checked visually. The proved constructions establish one aperiodically trapped ray and any prescribed finite number of selected distinct rays. The stronger arbitrary-prescribed-directions statement is only outlined there and is not needed by this package. No all-direction trap is claimed. Its nondegenerate rays survive endpoint transparency. Countably many exceptional directions in a fixed rational-angle configuration are entirely compatible with these aperiodic examples and with choosing larger configurations for larger finite ray counts.

The UnsolvedMath page again returned HTTP 403. Live rendered access is not claimed. Original article binaries, extracts, and images are excluded from this audit package.

## Dataset and actual prior-attempt provenance

The complete 68,931,837-byte problems file and 80,334,822-byte prior-report file were read and independently hashed. Both match the pinned repository manifest and the freshly retrieved [Hugging Face descriptor at revision 37e53eabe540fb458758e198be61634bd02ee008](https://huggingface.co/api/datasets/ulamai/UnsolvedMath/revision/37e53eabe540fb458758e198be61634bd02ee008?blobs=true), including its LFS SHA-256 values and sizes. Their counts are 15,458 problem records and 6,701 prior reports. Exactly one selected numeric-ID record was found. The complete keyed prior report was read as triage, not accepted as proof.

The complete catalog has 15,458 records. Its SHA-256 and Git blob hash agree with the frozen metadata. The selected identity, rank 776, statement digest, and baseline queued 0/5 status agree with the catalog and exact queue blob. The campaign tree and complete 62-entry attempts tree were independently reconstructed as Git tree objects and their hashes verified. There is no target attempt directory at the author's baseline commit.

During this audit, main had advanced to `cb8091dcfa69ed41defad72963836f5f8920648f`; its campaign and attempts tree hashes remained identical. Fresh public PR searches by numeric ID, code, and title phrase, plus commit searches by ID and title phrase, each returned zero results with incomplete_results=false. Eight branch-list pages covered 796 distinct visible branch names; none matched the numeric ID or mirror/trapping-light terms. The first page of a general PR listing was not used as an absence certificate. No new independent authenticated code search was performed, so the author's original code-search claim is not promoted into a separately reproduced audit result. Deleted, private, and unindexed work remain outside this bounded check.

The related-target addendum identifies both 3900009 and 3100011 as separate polygonal-room illumination targets. Neither is settled by these partial escape results; their current literature status was not audited here. The convex-body illumination entries are different topics. No further proof-search approach was expended on adjacent targets.

## Reproduction, boundaries, and release scope

`independent_verify.py` and its recorded result are self-contained standard-library controls. `verify_artifacts.py` checks the author freeze, relocates its replay, compares the independently reconstructed certificate, and optionally verifies complete public provenance inputs. `verification_metadata.json` supplies source/retrieval hashes and search scopes without source text or raw repository responses.

The safe package includes only this authored review, the correction/clarification addendum, independent code and results, public verification metadata, reproduction instructions, and its manifest. It excludes source binaries, extracts, rendered images, imported datasets, complete catalog records, raw repository/API responses, and coordination materials. The audit performed no remote writes.

**Recommended publication wording:** unsolved partial-results attempt, five approaches exhausted; independently audited scoped elementary proofs and exact finite controls. Do not label it a solution of TOPP 31, a proof of the unrestricted conjecture, a new discovery, or human-reviewed work.
