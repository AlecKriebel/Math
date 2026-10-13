# Independent adversarial review: cone, topology, and affine index

## Decision and exact scope

The intrinsic cone/affine mechanism in original PR152 is **not falsified and is proved below**, for the two-polygon translation surface and genus-at-least-two range used by the candidate. However, the original unqualified identification of physical source type with intrinsic index, and its physical reversal statement, **require a folding-orientation sign repair**. An actual four-segment pentagon path falsifies the stronger physical reversal statement. The exact repaired candidate separates the two labels and makes the invariant-weight argument valid. No missing theorem equivalent to the sine-ratio conclusion is hidden in the repaired angular-lift or hyperelliptic steps.

After-repair scoped decision: **PASS**, reviewed exact repaired candidate SHA-256 `e6d40a40032b5af335777abf692e6b0bb45b1582f85d7a02bed192b4984217b9`. Original-submission scoped decision: **REPAIR REQUIRED**, rather than acceptance of every literal source-label assertion.

This is a mathematical review of one mechanism, not a verdict that the entire literal claim is solved. In particular, this review does not independently certify the physical unfolding quotient, its reflected-label transport along arbitrary billiard words, the imported cusp representatives, or the model-direction exhaustion. These are named remaining obligations for a whole-proof verdict, not counterexamples to the cone lemma.

Reviewed original head: `99ef28d28bf380658400886d1f8c2120a5096d97`. Reviewed candidate: `original_submission/files/unsolved_math_prioritization/attempts/5000006/CANDIDATE.md`, especially §§1–3. I read the original verifier only as a claimed-evidence artifact, and wrote a separate checker. I did not consult original reviews/verdicts or other fresh agents' conclusions before forming this assessment. After that independent assessment, the root agent communicated the physical reversal conflict; I derived its sign repair independently and independently traced the concrete example. I then reviewed the exact repaired proof body and its repair note. No outreach, Git operation, publication, or global-file change was performed.

The exact target of this review is: if a short billiard trajectory has the corner data asserted in equation (9), is its canonical sine weight invariant under every affine automorphism required by the reduction, including orientation changes and trajectory reversal? The answer is yes, for the specified surface. The strongest unconditional statement is the intrinsic cone-weight theorem in §4 below. Its comparison with Fuchs requires an initial folding-chart sign: k=sigma*K. The initial-P corner proof establishes sigma=+1; §6 establishes sigma=-1, the physical reversal law and the exact repair. General physical transport remains a separately identified whole-proof dependency.

## 1. Corner cycles, cone orders, genus, and involution

Put `M=n-2` and `delta=M*pi/n`. The gluing is

`P_j P_(j+1) ~ Q_(j+1) Q_j`.

Going around a vertex follows the permutation

`(P,j) -> (Q,j+1) -> (P,j+2)`.

For odd n the permutation has one cycle of length 2n. Its angle is `2n*delta=2*pi*M`, so the zero order is `M-1=n-3`. For even n it has two cycles of length n, distinguished by `P_even,Q_odd` and `P_odd,Q_even`. Each angle is `n*delta=pi*M=2*pi*r`, with `r=M/2`, and each zero order is `r-1=(n-4)/2`.

There are two faces and n glued edges. With V equal to 1 or 2, Euler characteristic is `V-n+2`, hence genus is `(n-V)/2`: `(n-1)/2` for odd n and `(n-2)/2` for even n. These are the exact double-polygon genera; replacing even n by the smaller opposite-side quotient would alter the proof.

The map iota exchanges polygons and acts by `z -> -z`. It is compatible with every glued edge. More explicitly the translation from the P edge to its Q mate is `T(z)=z-P_j-P_(j+1)`. Equality of the iota image with the glued image requires `-z=T(z)`, namely `z=(P_j+P_(j+1))/2`. Thus each of the n glued edges has one regular fixed point. Interior points cannot be fixed because their two polygon interiors are disjoint. The unique odd-n vertex point is fixed; the two even-n vertex points are exchanged. The total is n+1 for odd n and n for even n, in each case `2g+2`.

This count is exact, including n=5, n=6, n=7 and n=8. For n=3 and n=4 the marked vertex points are regular and g=1; the genus-at-least-two uniqueness argument is not available. The candidate treats those cases separately. The cone proof itself applies to odd n>=5 and even n>=6, although the candidate also treats n=6 separately.

## 2. Hyperelliptic uniqueness and affine/anti-affine conjugation

In translation charts iota has complex-linear derivative -I. It is holomorphic away from zeros and extends holomorphically over them. A local justification is useful: if the translation coordinate near a cone point is `z=w^r`, and a map with derivative -I sends that point to another cone point, then in centered coordinates `(w')^r=-w^r`. On a connected punctured neighborhood this gives `w'=c*w`, with `c^r=-1`; hence the map extends holomorphically across the zero. This explicitly handles any sheet rotation at a cone point.

For a holomorphic involution with B fixed points, Riemann–Hurwitz gives

`B=2g+2-4h`,

where h is the quotient genus. With `B=2g+2`, the quotient has genus zero, so iota is hyperelliptic.

Now let f be any affine automorphism, allowing either sign of determinant. It is not necessary, and would be false in general, to assume f itself is holomorphic. Instead `h=f*iota*f^(-1)` has derivative `A*(-I)*A^(-1)=-I`. Therefore h is holomorphic in the original translation complex structure, including at the zeros by the local argument above. It is topologically conjugate to iota, so is an involution with `2g+2` fixed points. Its quotient is again a sphere. Uniqueness of the hyperelliptic involution for g>=2 gives `h=iota`, hence `f*iota=iota*f`.

This remains valid when f reverses orientation: the conjugate is still orientation preserving and has complex-linear derivative -I. It does not rely on f being antiholomorphic.

The exact uniqueness theorem was independently checked in the primary paper E. Tyszkowska, *On p-hyperelliptic Involutions of Riemann Surfaces*, Theorem 3.1 (printed p.583): set p=0 in its hypothesis `g>4p+1`. [Full primary paper](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2tys.pdf).

There is also a short independent reason for uniqueness. If two distinct degree-two maps to the sphere existed, their meromorphic function fields would generate the full curve field, because each is a subfield of index two and they differ. The resulting map to `P^1 x P^1` is birational onto a curve of bidegree (2,2), whose arithmetic genus is one. Its normalization cannot have genus at least two. Thus the sphere-cover involution is unique. This argument is explanatory; the cited theorem suffices.

## 3. Angular lifts and sheet offsets

A cone of angle `2*pi*r` has a germ circle `R/(2*pi*r Z)`. Projecting its angular coordinate to the ordinary direction circle amounts to reducing modulo `2*pi`.

Let `epsilon=sign(det A)`. The ordinary direction map induced by an invertible real-linear A has a continuous angular lift G satisfying

`G(theta+pi)=G(theta)+epsilon*pi` and `G(theta+2*pi)=G(theta)+epsilon*2*pi`.

Proof: `A(-v)=-A(v)` says that the first difference is an odd multiple of pi; continuity makes that multiple constant. Applying it twice and using the degree epsilon of the direction map forces that multiple to equal epsilon. Iteration gives the same identity for every integer multiple of pi.

The germ map of an affine automorphism at a cone is a lift of this ordinary direction map. Any two such lifts differ by a constant `2*pi*c`, c integer. It is a constant because the difference is continuous and integer valued. Thus a sheet offset cancels whenever two germs are compared at the same source point. In particular, for any integer m,

`F(theta+(1-e)*pi+2*pi*m)-F(theta)`

`=epsilon*((1-e)*pi+2*pi*m)`.

Nonconformal distortion of the other angles is irrelevant: the only differences used are integer multiples of pi. This is a proved local fact for arbitrary invertible A, rather than an assumption that affine maps preserve ordinary corner angles.

## 4. Intrinsic index theorem, endpoint cases, and reversal

Let gamma be an oriented saddle connection in X_n, with start germ u and backwards end germ v. Its developed directions are antipodal.

For coincident endpoints, define m modulo r by

`angle(u,v)=pi+2*pi*m mod 2*pi*r`.

The equality of developed directions up to a half turn makes m well defined. The angular-lift law gives m'=m for an orientation-preserving affine map and `m'=-m-1` for an orientation-reversing affine map.

For even n and different endpoints, iota exchanges those endpoints. Its derivative -I makes the direction of `iota(v)` agree with that of u. Define m by

`angle(u,iota(v))=2*pi*m mod 2*pi*r`.

After applying f the compared germs are `f(u)` and `iota(f(v))=f(iota(v))`. Both now come from the same starting cone, so their sheet offsets cancel. Thus m'=m for det A>0 and m'=-m for det A<0. The indicator e of different endpoints is preserved because f is a bijection.

Define an intrinsic residue K modulo M by `K=2m+1-e`, using e=0 for odd n. For odd n, r=M and M is odd, so m -> K is a bijection of residues. For even n, r=M/2: e=0 yields the M/2 odd residues, and e=1 yields the M/2 even residues. No extra residue is lost and no incompatible endpoint parity is introduced.

All orientation-preserving affine maps preserve K. All orientation-reversing affine maps send K to -K. Indeed the formulas above give this immediately in both e cases.

Reversing the orientation of gamma gives the same transformation. For e=0, swapping u and v negates their angle difference, hence `m'=-m-1`. For e=1, apply iota to the old comparison: the angle from `iota(u)` to v equals the angle from u to `iota(v)`; swapping the comparison negates it, giving `m'=-m`. This uses iota being an orientation-preserving isometry and `iota^2=id`, not an arbitrary comparison of different cone lifts.

For canonical `K in {0,...,M-1}`, set `W(K)=sin((K+1)*pi/n)`. If K=0 its inverse residue is zero. If K>0, the inverse residue is `M-K` and

`sin((M-K+1)*pi/n)=sin((n-1-K)*pi/n)=sin((K+1)*pi/n)`.

Therefore W is preserved by every affine automorphism and by reversing the saddle connection. The representative convention is indispensable: W is a function on canonical residues, not the sine expression evaluated at arbitrary integer lifts. For example for n=5, K=1 has W=sin(2*pi/5), whereas the congruent integer 4 gives sin(pi)=0 if used without canonical reduction.

This proves the strongest unconditional statement of this review: **the intrinsic cone weight W is invariant under every affine automorphism of the specified X_n in genus at least two and under trajectory reversal.** The proof does not transfer this conclusion to an unsupported equivalent assertion.

The required dihedral isometries are included in this statement. Polygon rotations and reflections take the translation edge-pairing to itself. For odd n=2h+1, the additional rotation by pi/n exchanges the copies and maps both P_j to Q_(j+h) and Q_j to P_(j+h), with indices modulo n. It takes the edge pairing to the same pairing with the copies exchanged, so it is also an actual affine self-map of X_n. Its determinant is positive, so K itself is preserved. This verifies the extra odd-n half-step used to align unoriented Fuchs directions.

## 5. Fuchs definition and residue comparison

I downloaded the full 25-page primary Fuchs PDF and visually inspected printed pp.502-505, including Fig.8, Definition 2.1 and both type tables. Its preceding convention assigns the sum relation to odd segment count and the difference relation to even segment count. Its type parameter is a residue modulo n-2, with the boundary duplicate `A_(n-2)=A_0`. The literal odd first-clause bound is `m+1`; its extra indices are infeasible for nonnegative alpha. [Fuchs primary PDF](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf).

Write angles in units of pi here. The physical ranges from the figure are

`0<=alpha<=M/n` and `2/n<=beta<=1`.

For odd segment count, `s=n*(alpha+beta)/2` is an integer and the parity-selected source residue is `k=n-1-s mod M`. For even segment count, `s=n*(beta-alpha)/2` is an integer and `k=s-1 mod M`.

Here is an exhaustive analytical boundary check of those residue formulas. In the sum case `1<=s<=n-1`; the unreduced label `n-1-s` lies in `[0,M]`. The range on beta becomes

`max(0,(n-2k-2)/n)<=alpha<=min(M/n,2*(n-k-2)/n)`.

For small k the upper restriction is automatic; for large k the lower restriction is automatic. These are the two sum branches, with the two boundary-side representatives 0 and M agreeing.

In the difference case `2-n/2<=s<=n/2`. For even n=2h, integer s has range `[2-h,h]`. Positive s yields `k=s-1` in `[0,h-1]`, with `alpha<=1-2s/n`. Nonpositive s yields `k=s-1+M` in `[h-1,M-1]`, with `alpha>=2/n-2s/n`. These are its two difference branches; the overlap at k=h-1 is only the two endpoint boundary configurations. For odd n=2h+1, integer s has range `[2-h,h]`; the two label intervals are `[0,h-1]` and `[h,M-1]`. The literal first-clause extension to h+1 allows no extra nonnegative alpha because its upper bound is negative.

A useful adversarial example is the direct pentagon diagonal j=2, with `alpha=2/5`, `beta=4/5`. Without segment parity the displayed conditions admit residues 0 and 1. With its actual one-segment parity the type is 1. This is not a counterexample to the candidate: it explicitly retains the preceding convention. It warns against claiming that the four displayed angle clauses alone are unambiguous.

It remains to compare the source residue with K. This step is exact once the candidate's corner/parity transport is supplied. Start at P_0 with lower boundary angle zero. For odd n the start cone cycle has terminal P at t even and terminal Q at t odd. For even n, transport a different endpoint by iota before measuring it in the start cone. Terminal P then has `t=2a+e`; terminal Q has `t=2a+1-e`.

A terminal P backward germ has offset `1-beta`. A terminal Q corner, whose physical reflected orientation is reversed, has offset `delta/pi-(1-beta)=beta-2/n`. Hence, with integer q accounting for any full-cone lift,

`(1-e)+2m = t*M/n + 1-(alpha+beta) + 2r*q` (terminal P),

`(1-e)+2m = t*M/n + (beta-alpha)-2/n + 2r*q` (terminal Q).

In the first case the exact integer relation is

`n*m = a*M + e*(n-1)-s + n*r*q`.

In the second it is

`n*m = a*M + s+e-2 + n*r*q`.

For odd n use e=0 and r=M. For even n `r=M/2`, and n is even. Thus `n*r` is a multiple of M in both cases. Reducing, and using `n=2 mod M`, gives

`2m=k+e-1 mod M`, hence `k=2m+1-e mod M`.

This explicitly verifies that full-cone lifts cannot alter the residue, including even n where r differs from M. It also shows why the different-endpoint correction e is necessary.

The displayed endpoint relation has a checkable local mechanism: crossing to a reflected polygon reverses the physical interior offset, while translation-side gluing leaves its developed direction unchanged. I have checked the resulting cone algebra and source definitions. A whole-proof review must still independently check that this relation applies to every actual unfolded billiard word with exactly the stated P/Q parity; this report does not substitute an algebraic consistency check for that physical verification.

## 6. Falsification attempts and repairs

| Approach | Mechanism tested | Evidence | Status and exact gap |
| --- | --- | --- | --- |
| Topological mismatch | Wrong double-polygon genus or cone cycle | Explicit corner permutation, Euler calculation, edge-midpoint equation; checks n=3..80 | No mismatch; genus-one uniqueness intentionally excluded |
| Noncentral affine symmetry | Conjugation might change hyperelliptic involution | Conjugate derivative -I, extension over zeros, fixed-point count, independent primary uniqueness theorem | Ruled out for g>=2, including det A<0 |
| Sheet-offset counterexample | Distinct lifts might shift the type | Lift difference is constant 2*pi*c; different endpoints first compared using commuting iota | Ruled out for the actual intrinsic index |
| Nonconformal angle distortion | A shear might change m | Integer-pi difference law proved for every invertible A; numerical shear/reflection/negative-angle probes | Ruled out locally; numerical probes are not evidence of global map existence |
| Type congruence or parity error | Source branches may disagree with m | Exact source-angle truth-pattern partitions and all corner/full-sheet congruences n=3..80 | No error under stated corner transport; arbitrary physical billiard words outside this checker |
| Representative sine error | A modular congruence might be fed directly into sine | Canonical inversion identity proved; explicit n=5 noncanonical warning | Candidate correctly uses canonical representatives |
| Direction/trajectory reversal | Same/different endpoint cases and physical chart changes | Separate m transformations, direct source-angle reversal and physical example | Intrinsic K reverses to -K; physical even-N source k is preserved; repaired weight invariant |
| Boundary cases | Side wraps, middle type, minimal genus | Exact endpoints, midpoint truth-pattern partitions, direct chords, n=3,4,5,6,8 | No false boundary step in scope |

No repair of the intrinsic cone mechanism is necessary, but the physical-source sign repair below is required. Two further modest clarifications would make the proof more readily checkable: write the local holomorphic extension at zeros rather than leaving it implicit; and write `epsilon=sign(det A)` in the angular-lift law before discussing orientation reversal. The candidate already contains the needed hypotheses, genus exclusions, parity selection and canonical sine convention.

## 6A. Exact physical sign repair and after-repair review

The intrinsic statement `K_rev=-K` is correct. The original sentence treating that as physical `k_rev=-k` for every path is false. Directly from the source endpoint convention, reversing a physical path gives

`alpha_rev=1-beta`, `beta_rev=1-alpha`.

For odd N, the sum integer changes to `n-s`, giving `k_rev=-k`. For even N, the difference integer stays s, giving `k_rev=k`. Thus the exact physical law is

`k_rev=(-1)^N*k mod M`.

This is an actual issue, rather than only a formal admissible-angle example. In a side-one regular pentagon, starting at vertex 0 with alpha=pi/2 gives side word `[1,3,1]`, all three hits in side interiors, and returns to vertex 0 after four segments. The segment directions are exactly `pi/2,-pi/10,9*pi/10,-pi/2`. Side 1 has line angle pi/5 and side 3 has line angle -3*pi/5, so the successive reflection formulas are exact. The normal incidence at side 3 retraces the path. Both source endpoint angles are pi/2, so its source type and the type of its identical physical reverse are 2 modulo 3. The intrinsic reversed connection has K=1. `physical_reversal_example.py` independently computes the side-interior hit fractions and produces the receipt in `physical_reversal_example.json`.

The repair introduces the folding-chart orientation sign sigma. A physical realization beginning in an orientation-preserving P chart has `k=K`, as proved above. An initial physical Q fold has negative orientation and gives `k=-K`. This is not an arbitrary relabeling: choose H to be a polygon reflection in a center-to-side-midpoint symmetry axis. The actual side-reflection representative Q -> P is `H composed with iota`: since iota is a half turn, its composition with the normal-axis reflection is reflection in a line parallel to the side. Adding the relevant translation makes it the physical side reflection. Other physical Q folds differ by an orientation-preserving polygon rotation.

The path folded using H is the polygon reflection of the path normalized by iota alone. Polygon reflection changes endpoint angles to

`alpha'=M/n-alpha`, `beta'=1+2/n-beta`.

The sum integer becomes n-s, and the difference integer becomes 2-s. Both source-label formulas therefore give `k'=-k`. Since iota preserves intrinsic K, the physical Q chart has `k=-K`. In general,

`k=sigma*K mod M`.

There is also a direct negative-chart corner calculation. Normalize an initial Q corner to P using the positive-orientation iota. Its initial abstract offset is `M/n-alpha`. For odd physical N its terminal corner is now P and its backwards offset is `beta-2/n`; for even physical N its terminal corner is now Q and its backwards offset is `1-beta`. Substitution gives respectively

`n*m=a*M+e*(n-1)+s-n` and `n*m=a*M+e-s`,

up to full-cone lift multiples. Each reduces to `K=-k mod M`. These are included in the independent checker, so the negative-chart rule is tested separately from simply asserting reflection invariance.

For an affine map with determinant sign epsilon, and old/new physical chart signs sigma and sigma', the exact physical type transformation is

`k'=sigma'*epsilon*sigma*k mod M`.

It can preserve or negate k; it always preserves its canonical sine weight. Under physical reversal the initial chart sign changes by `sigma_rev=(-1)^(N-1)*sigma`, while the intrinsic connection reverses K to -K, recovering `k_rev=(-1)^N*k`.

This distinction also makes the reduction explicit. Every model connection has `L=2R*w(K)`, including connections beginning in Q. All connections in one direction get the same derivative length factor under the same affine map. Original physical paths start in P and have k=K; model physical normalization may have either sign, but `w(k)=w(K)` in both cases. Consequently the labelled ratio uses the correctly invariant weight throughout. There is no need to assert invariant physical labels.

I read the exact `repaired_proof_v1/CANDIDATE.md`, verified its SHA-256 `e6d40a40032b5af335777abf692e6b0bb45b1582f85d7a02bed192b4984217b9`, and read the case-level `PROOF_SIGN_REPAIR.md`. The repaired body implements the sign qualification in index identification, physical reflection, physical reversal and the model-length argument. Its formulas agree with the derivations above. The H composed with iota choice is a valid representative; uniqueness of that physical fold is neither needed nor asserted as an input to the invariant weight.

After repair, no remaining gap exists within this review's cone/affine/source-definition mechanism. The general unfolding and cusp dependencies remain outside the certification scope. The counterexample falsifies an original overstrong intermediate claim, not the target sine-ratio theorem, and the repair does not rely on an unproved equivalent claim.

## 7. Checkable artifacts and limits

`check_cone_affine.py` is independent of the submission verifier. Running `python3 check_cone_affine.py` from this review directory produces `checks.json`. The successful run made 5,749,203 assertions. It covered n=3 through 80, 246,597 exact endpoint/midpoint source-angle truth-pattern samples, all corresponding affine-linear source boundaries for each tested n, 1,247,610 corner/full-sheet integrality checks and the same number of residue checks for each chart sign. It also checks physical reversal on all 246,597 source-angle samples. Local GL probes include positive and negative determinants, arbitrary integer sheet offsets, negative angles and multiple turns.

The source-angle partition is exhaustive for each tested n because all clause inequalities are linear and all possible changes occur at the included breakpoints. The finite n bound does not replace the all-n derivations above. The ordinary-linear numerical checks do not certify the existence of a global affine automorphism; the universal lift identity is proved analytically.

The full Fuchs PDF checksum is `9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d`, independently matching the original source manifest. The primary source PDFs, extracted Fuchs text, and inspected definition-page PNGs are preserved in this directory. `RESULT.json` provides the machine-readable scope decision.

## Final strongest statement and exact remaining gap

For the explicitly glued X_n in the genus-at-least-two range, the canonical intrinsic cone weight is invariant under all affine automorphisms and under saddle-connection reversal. The physical source residue is sigma times the intrinsic residue for the initial folding-chart orientation sigma; the source weight equals the intrinsic weight. The original unconditional source-label/reversal assertion required repair, and the exact repaired body at the hash above now supplies it. None of the repaired hyperelliptic, angular-lift, extra-sheet, or residue algebra steps imports an equivalent unsolved claim.

The only remaining gap before turning this scoped result into a certification of the full literal Fuchs conjecture is external to this mechanism: establish the faithful physical unfolding and source-angle transport for every short billiard trajectory, then verify the classical affine cusp reduction and model connections on the exact surface. This report records that obligation without claiming it has failed or been proved here.
