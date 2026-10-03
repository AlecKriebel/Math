# Independent covering and topological-boundary audit

Frozen PR382 / problem6600013 head: `421c6aa90eace49c8659f9a96e83c24fe1b5b901`.

**Assigned-scope conclusion:** Turns4-5 are mathematically supported when read together with the existing `final_review/TOPOLOGICAL_CLARIFICATION.md`. No mandatory mathematical correction was found in this family. The finite cyclic covers are admissible examples with finite Betti numbers `(1,4,q+3)`. The inverse 2-adic tower has countably infinite rational second Cech cohomology, but its specified transversal action has no continuous finite-alphabet generator, and its direct full-state unit-square decoration fails FLC. These findings do not resolve the original arbitrary higher-dimensional implication. This is an independent AI-assisted family audit, not novelty, external peer-review, merge, or full-resolution certification.

Audit completion: 100% of this family's assigned checks. Original-problem resolution estimate: 0%. The five author turns remain exhausted; no sixth author search was conducted.

## Independence, provenance, and scope

The original problem and Julien conventions were downloaded independently before candidate proof conclusions were read. Their PDF hashes agree with the frozen source metadata. Original arXiv1604.06280 printed p8 and Julien2017 printed p546 were visually checked. Julien0804.0145v1 Section5 was read, including Theorem5.10, Lemma5.14, and Proposition5.16, with the published/arXiv renumbering distinguished. Sources:

- [Original problem collection](https://arxiv.org/pdf/1604.06280), Problem2.5.1.
- [Julien's available 2008 arXiv version](https://arxiv.org/pdf/0804.0145), Section5.
- [Julien2017 conventions](https://www.numdam.org/item/10.5802/aif.3091.pdf), Section2.

`SOURCE_RECEIPT.json` records the download hashes and lengths. Raw foreign PDFs, extracts, and renders are ignored in `private_sources/`. I do not separately certify the cut-and-project literature correction, which belongs to the source family.

`INDEPENDENT_PRE_CANDIDATE.md` and `PRE_CANDIDATE_SEAL.json` sealed the mechanisms at 02:40:32 UTC before TURN4, TURN5, RESULT, candidate code, roof clarification, and substantive old verdict were read. All five candidate proof files and all executable Python files were subsequently read. The new controls import no author code. `NEW_CONTROL_SEAL.json` and `INDEPENDENT_RESULTS_SEAL.json` bind the new code and its results before reading the substantive old `ADVERSARIAL_REVIEW.md`. An incidental verdict string in `REVIEW_MANIFEST.json` was exposed during integrity-code reading before the new code seal; this contamination is recorded explicitly, rather than misdescribed as complete blindness to every old status label. The independent mechanism reconstruction was already sealed at that point.

`FROZEN_BINDING.json` verifies every one of the 58 snapshot paths byte-for-byte against `git show` at the frozen head and against the snapshot SHA256 hashes. Its workspace-head field is the audit's actual workspace head, not a substitution for the frozen candidate head. No shared candidate, queue, Git index, branch, service, or remote was modified. Only this family's folder was written.

## Exact target hypotheses

The target's rational coefficient field is essential. The integral Thue-Morse example in the original source does not provide a rational counterexample. The intended hull is translational, and aperiodicity means no nonzero translation period, following Julien2017. Repetitivity plus FLC gives a compact minimal translation action. Finite-alphabet unit-cube systems satisfy FLC automatically. Fixed pointing and norm conventions preserve the polynomial exponent after bounded scale/constants; they need not preserve a numerical complexity coefficient. Every coefficient below concerns the stated symbolic n-box language.

## 1. Finite-stage covering theorem

Let the base be a product of d minimal aperiodic one-dimensional subshift suspensions, and let a D-sheet cover be pulled back from one specified finite product of Rauzy graphs. At independently chosen cofinal word lengths, assume graph i has first Betti number at most M_i. Each connected graph can be collapsed to a rose with at most M_i loops. Its product has a CW model with at most `product(1+M_i)` cells in total, including one vertex and all product cells.

A finite cover pulled back across a homotopy equivalence is homotopy equivalent to the original cover: lift the inverse and the two base homotopies. Thus its total rational cohomology rank is at most `D product(1+M_i)` at every selected cofinal stage. Compatible inverse-limit coordinates identify the pullback limit with the cover of the base hull. Cech continuity and the cofinal finite-dimensional bound then prove the asserted finite total rank. This proof neither assumes injective arbitrary bonding maps nor confuses a finite-to-one factor with an unbranched covering.

For a local permutation decoration, the finite values of each continuous fixed-radius transport are well-defined at a sufficiently large product-pattern approximant. The square equations close each lifted square. Cube boundaries introduce no further obstruction: in a cubical product every change in ordering of coordinate transports is generated by adjacent coordinate interchanges, already governed by square flatness. The result is an actual D-sheet covering. Minimality is not automatic here; the general cover theorem only asserts finite cohomology. The specific cyclic family separately proves minimality.

For the full extension, the distinguished vertex's D states give D distinct decorations of every base pattern. One state and an expanded base patch determine the whole decoration by transport. Hence

`D P(n) <= P_lift(n) <= D P(n+2R+c)`.

The liminf coefficient equality follows by a fixed integer shift of the same sequence: `P(n+a)/n^d = [P(n+a)/(n+a)^d] [(n+a)/n]^d`, and the second factor tends to 1. No regular-variation assumption is necessary. The lower bound requires the full D-sheet system; it need not hold after selecting one invariant component. Candidate wording preserves that qualification.

The factorwise graph rank bound used in Turn4 also follows: if `c_i=liminf p_i(n)/n`, infinitely many integer increments satisfy `p_i(n+1)-p_i(n)<=floor(c_i)`, giving `M_i=floor(c_i)+1`. Since `c_i>=1`, `1+M_i<=3c_i`. Finite products of the factor liminfs do not exceed the liminf product. The numerical conclusion is therefore valid for the declared box convention.

## 2. Proper substitution and the roof bridge

For `tau(a)=aab, tau(b)=ab`, every b ends a supertile and each preceding a-run has length one or two. The runs partition a legal bi-infinite word uniquely into ab/aab, and the resulting preimage stays in the substitution language by cropping an occurrence in a higher iterate. Iterating gives recognizability. Both images begin with a and end with b; their increasing common expanded prefixes/suffixes determine arbitrarily large neighborhoods even at a graph vertex. This supplies the border information needed for the two-loop inverse-limit model.

The substitution matrix is unimodular. The free-group map has explicit inverse `a=A B^-1`, `b=B A^-1 B` for `A=aab,B=ab`. Thus the graph map is a homotopy equivalence. The candidate's primitive-block frequency and length arguments establish minimality, irrational a-frequency, aperiodicity, and `p_tau(n)<=24n`; no exact Sturmian complexity identity is required for this family.

A constant-expansion stationary metric graph requires PF lengths, not two unit edges. Write `phi=(1+sqrt(5))/2`, choose lengths `(phi,1)`, and expansion `lambda=phi+1`. The two checks are

`2phi+1=lambda phi`, and `phi+1=lambda`.

The supplied roof clarification makes this convention explicit. For the symbolic subshift X and locally constant positive roof `ell(x_0)`, the tilewise map from unit roof to PF roof is

`[x,t] -> [x,t ell(x_0)]`, `0<=t<=1`.

It respects endpoint identifications and has a continuous inverse dividing by the roof. Thus it is a homeomorphism and orbit reparameterization. For an interior a-tile, a unit-time displacement delta becomes PF displacement phi times delta under this displayed map; the map does not conjugate the actions while preserving time. Keeping the fiber state makes it lift to every cyclic decorated suspension, and reducing fiber states commutes with it. This justifies transfer of cohomology and connectedness without transferring a numerical language coefficient through a geometric rescaling.

**Packaging dependency:** retain the existing `TOPOLOGICAL_CLARIFICATION.md` and its bindings when promoting these scoped results. Removing it would reopen the unit-edge stationary-model ambiguity. No additional correction is presently required.

## 3. Actual cyclic covering cochains and changing substitution monodromy

The degree-q cover of the product of two two-loop roses has vertices g in Z/q, horizontal edges `(g,a),(g,b)`, and vertical analogues. With increment pair `(u,v)` in both factors, the directed square at g with labels i,j has boundary

`X_i(g) + Y_j(g+s_i) - X_i(g+s_j) - Y_j(g)`.

The new code constructs these incidence matrices from the actual paths, with q vertices, 4q edges, and 4q faces. It does not infer Betti numbers from covering degree alone. For `h=gcd(q,u,v)` there are h components; Fourier decomposition gives

`(beta0,beta1,beta2)=(h,4h,q+3h)`.

Indeed, a character for which both `zeta^u,zeta^v` equal 1 contributes the untwisted `(1,4,4)` tuple. Every other character has nonzero map `C->C^2` in both graph factors, so it contributes a single degree-two dimension. There are h trivial-on-monodromy characters. At the initial `(u,v)=(1,0)`, h=1 and the claimed tuple is `(1,4,q+3)`. Scalar extension preserves ranks of these finite rational matrices.

The substitution does not keep the initial monodromy `(1,0)` fixed: its pullback changes `(u,v)` to `(2u+v,u+v)`. Because this transformation has determinant 1, surjectivity modulo q persists. A hidden substitution error here would not be detected merely by recomputing one static cover. The new controls build the actual lifted maps between these changing covers. An a-edge maps to the aab path, a b-edge to ab; a source square maps to the rectangular product grid of the corresponding two words. The target sheet of each small square is g plus its two prefix increments. The controls verify both chain identities and compute the induced homology image ranks `(1,4,q+3)` at four stages for q in `{1,2,3,4,5,6,8,12}`. These actual maps are consistent with the all-level covering-homotopy proof that the lifted maps are homotopy equivalences.

Connectedness and minimality are both justified. Surjective pulled-back monodromy gives connected approximants and hence the connected covering hull. If M is a minimal closed invariant subset of its finite-fiber transversal, its projection to the minimal base is onto. The fiber cardinality is an invariant upper-semicontinuous integer function. Its closed superlevel sets are invariant, so base minimality makes it constant. Excluding the finitely many missing local states shows M is open as well as closed. Its suspension is therefore clopen in the connected covering hull, forcing it to equal the whole hull. Periods project to periods of the base and are zero. Thus the full finite cyclic covers are repetitive, FLC, and fully aperiodic. Their exact full-decoration box complexity is `q p_tau(n)^2`.

Adversarial boundary controls retain the role of hypotheses: zero monodromy over a minimal base splits into q components and has tuple `(q,4q,4q)`; monodromy `(2,0)` at q=4 has tuple `(2,8,10)`. Neither supports the connected/minimal tuple asserted for `(1,0)`.

## 4. Infinite cohomology and the finite-generator obstruction

Fiber reduction defines genuine two-sheet covers from degree 2q to degree q. On cellular cochains, pullback repeats a cell value on its two lifts and transfer sums those values. Both commute with differentials, and transfer after pullback is exactly 2 times the identity. Over Q this yields a left inverse, so cohomology pullback is injective. The new controls check those equations at the initial and two later monodromies and compute the full H2 image rank q+3. Naturality through the lifted substitution models supplies the same conclusion for the suspensions.

The inverse-limit transversal is `X_tau x X_tau x Z_2` with its specified additive cocycle. Basic open sets are finite-level cylinders, so finite-level minimality proves inverse-limit minimality. Stabilizers project to base stabilizers and vanish. All suspension projections keep the same fractional unit-square position; compatibility of both configurations and seam identifications gives a continuous bijection between suspension-of-limit and limit-of-suspensions. Compactness makes it a homeomorphism.

Cech continuity now gives a countable direct limit of injectively nested H2 spaces with dimensions `2^k+3`. Consequently H2 has countably infinite rational dimension. H1 has dimension4, H0 has dimension1, and higher groups vanish. Unbounded raw approximant ranks alone would not justify this inference; it depends on transfer injectivity.

For nonexpansiveness, two distinct points with the same base and fiber difference `h=2^k` remain at 2-adic distance `2^-k` under every lattice translate: identical base points receive identical cocycle increments. Arbitrarily large k defeats every expansivity constant. A finite-alphabet subshift is expansive because moving a differing site to the origin separates configurations uniformly. Hence the specified action is not conjugate to any finite-alphabet `Z^2` subshift.

The stronger finite-observation proof has the required universal quantifier. Let F map the compact transversal continuously to a finite discrete alphabet. Around every point choose a product cylinder on which F is constant. A finite subcover has a maximum base-window radius R and fiber residue level k. Refining to common R,k shows F depends only on that finite window and the fiber modulo `2^k`. The whole orbit code therefore factors through that finite level, since reduction commutes with every skew shift. Two points over one base with a nonzero difference divisible by `2^k` have identical entire codes. No such F is a generator.

The new action controls implement signed transports on actual substitution words, including negative shifts, inverses, the cocycle law, and quotient compatibility. They support the construction; the compactness proof above, rather than this finite scan, proves the assertion for every F and every shift.

Each individual finite observation has `O(n^2)` code complexity, with its own level/window-dependent constant. That does not supply one finite generating alphabet. The full-state unit-square construction records uncountably many one-site fiber states and fails FLC. Moreover `P_q(n)>=q(n+1)^2` shows that the canonical finite-level coefficients diverge. The candidate carefully does not infer a cohomology bound for arbitrary factor images and does not claim that every possible different geometric realization or action has been ruled out. Those qualifications are necessary and are retained.

## Reproducibility and strongest verified result

All source/snapshot bindings and commands are recorded in this folder. `independent_controls.py` passes **58,258 exact assertions** with zero stderr; its full JSON stdout records the actual cover tuples, changing monodromies and image ranks, transfer ranks, and finite-observation controls. Every new assertion and matrix is independently constructed with Python's standard library. `INDEPENDENT_REPLAY_RECEIPT.json` records the explicit exit code and output hash.

The untouched private candidate copy reproduces `verify_turn4.py`, `verify_turn5.py`, and old `final_review/independent_checks.py` with byte-identical frozen stdout: 1,077, 2,374, and 22,728 assertions respectively. The additive `verify_review.py` entry point also exits0, replaying all 5,367 author assertions, 173 internal author manifest entries, and 44 raw author blobs. The complete stdout/stderr for each assigned replay and `REPLAY_RECEIPT.json` are retained. Its source-PDF count is0 because that portable command was not supplied sources; independent primary-source validation of the three assigned PDFs is recorded separately and must not be misreported as that command validating four PDFs.

**Strongest result in this family:** an actual finite-stage local-cover positive theorem for product hulls; explicit minimal FLC fully aperiodic cyclic finite covers with `(1,4,q+3)`; and a rigorously infinite-rank 2-adic suspension whose proposed finite-local generating description fails. The exact remaining gap is either a persistent-rank bound for arbitrary admissible low-complexity tilings or an admissible construction retaining infinitely many rational classes with one finite local generator and one `O(n^d)` coefficient. Neither is supplied by this family or by the finite tower. Keeping the packet's original disposition unsolved5/5 is consistent with these verified statements.
