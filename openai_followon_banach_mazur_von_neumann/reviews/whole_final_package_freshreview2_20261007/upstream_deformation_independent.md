# Independent upstream and deformation reconstruction, final candidate v2

Reviewer: internal AI agent `upstream_deformation_independent`, with an independently tasked `deformation_attack` agent. This is mathematical source review, not conventional human peer review or a publication authorization.

Checkpoint: 2026-10-07 15:07 UTC. Best-guess completion: **100% of this assigned upstream/deformation audit**, not a percentage of theorem truth, formal verification, or overall publication readiness.

## Finding and exact scope

No substantive mathematical gap or counterexample was identified in the pinned family-295 proof or the manuscript's fixed-algebra deformation mechanism. I reconstructed all five upstream mathematical source sections before reading earlier supporting audits. The resulting input is ordinary bounded complex multilinear Hochschild cohomology, with the original algebra as coefficient bimodule and the **actual image** of the differential. In particular, the input supplies precisely the degree-two and degree-three vanishing required by the follow-on argument.

The strongest intermediate result independently reconstructed is the actual primitive bound `||g|| <= ||f||` for separately normal cocycles on any type-II1 algebra admitting a faithful normal tracial state. The final central homotopy, uniformly bounded assembly, and classical normal reduction extend this to actual bounded primitives on arbitrary von Neumann algebras. The final unrestricted argument does not claim the same norm-one bound for arbitrary ordinary cocycles.

For the follow-on paper I independently checked section 2 in detail, and checked the fixed `P,E` use, full-carrier reconstruction, uniformity quantifiers, and predual step. I additionally checked the exact relevant statements and compression construction in the supplied publisher-formatted Roydor PDF; a full independent audit of all of Roydor's proof machinery belongs to the other assigned geometric reviewer. I have not reproduced a fresh Lean compilation, dependency import, or axiom probe. I do not infer formal verification from the archive's scope statement or an earlier static Lean audit.

Exact remaining mathematical gap within the reconstructed upstream/deformation proofs, using the stated classical structure and cohomology theorems: **none identified**. The limitations are the absence of a fresh kernel reproduction and the use of classical cited results rather than reproving their complete external proofs from first principles. This report is not a clearance decision.

## Frozen objects and source coverage

I read the current `manuscript/main.tex` and the `final_candidate_v2/review_manifest.json`. Current and frozen manuscript SHA-256 both equal

`46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4`.

Current and frozen `publication/upload-kit/source-and-verification.zip` SHA-256 both equal

`4dc0129f59789e279318bc2e1ba53a1c3e414fda8a7ba32c8dd1d7f221aee9fc`.

The archive's upstream provenance specifies full commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. I extracted and read the actual sources in the archive, not merely a theorem ledger or favorable verdict. `build/paper.tex` inputs exactly the five listed mathematical sections, followed by the bibliography. I also read its README, references for the external inputs, and the scope document for the latter's limitations. The extracted section hashes match the archive's pinned-source receipt:

| Actual source section | SHA-256 |
| --- | --- |
| `01-introduction.tex` | `ddec01dc15fa257e3f1e85004b54225dd43df633bbdfa957de98353c069ce4b2` |
| `02-walk.tex` | `3d1015a1c20d2cfc8a4c8991652d93eed756763cd982cbc28a53fd625b7b3314` |
| `03-liouville.tex` | `7782c390e534a15d35d7aee470ff425fcb6823c4073b29886f3dbffbc8d31622` |
| `04-rigidity.tex` | `9cf9cf2b11fc838326321b4c0384904a303ecec43d732cd748c9204059f4ea60` |
| `05-cohomology.tex` | `c6c8e63bac0e543624ac63fd50a046878ba7082a531115111563455682e4d437` |

Scratch sources are confined to `tmp/whole_final_package_freshreview2_20261007/upstream_independent/`. Fresh computation artifacts are preserved in `reviews/whole_final_package_freshreview2_20261007/upstream_deformation_checks/`. I did not read any earlier whole-final-package review or verdict, contact outside individuals, perform Git operations, or publish anything.

## Section 1: claim, coefficient space, and classical inputs

The source explicitly defines `C_b^k(M,M)` as all bounded **complex** multilinear maps with ordinary multilinear norm, `C_b^0=M`, and the standard Hochschild differential with both outer actions and every adjacent merge. Its quotient uses actual coboundaries. Thus there is no substitution of reduced, normal-only, completely bounded, or representation-valued cohomology.

The main theorem is all complex von Neumann algebras, all `k>=2`, actual bounded primitives. The zero algebra is harmless. Degree-one innerness is an external theorem and is not required to prove higher-degree vanishing, although it is used in an optional consequence discussed by the older audit.

The only external cohomological reductions are: an ordinary cocycle is cohomologous through a bounded cochain to a separately normal cocycle; and algebras without a type-II1 central summand have ordinary vanishing. I checked [Johnson–Kadison–Ringrose III, Lemma 5.4 and Theorem 5.6](https://www.numdam.org/item/10.24033/bsmf.1731.pdf), including the surrounding description of the natural map between normal and ordinary cohomology. The self-module is a dual normal bimodule, so the stated specialization applies. The theorem concerns actual coboundaries.

I checked [Christensen–Pop–Sinclair–Smith, equation (1.1) and section 2](https://arxiv.org/pdf/math/0107078). Its ordinary-cohomology vanishing formulation and differential agree; a zero type-II1 part is included. The new proof does not assume property Gamma or use a completely bounded replacement for ordinary cochains.

## Section 2: finite free tests and the single random walk

The Popa specialization was tested directly against [Popa, Theorem 0.1(a), sections 1.5–1.6](https://arxiv.org/pdf/1308.3982). Set each ambient factor and each full coordinate subalgebra equal to `P`. A diffuse factor corner cannot intertwine into the scalar relative commutant or a finite matrix amplification; the full ultraproduct is a factor. Taking the centered part of the separable coefficient algebra as `X` gives scalar-trace freeness. This uses case (a), so no amenability of the coefficient algebra is imposed. Finite iterative adjunction yields all needed Haar generators in the same ultrapower.

For the distinguished-letter lemma, write each path as `A_i u_{h_i}^{epsilon_i} B_i` over the algebra generated by nondistinguished letters. In a reduced word in the paths, the distinguished-letter string remains reduced: a potential adjacent inverse would already contradict reduction of the path-generator word. Expanding coefficient factors into scalar plus centered parts joins only contiguous subwords of that reduced string. Each such Haar block is nonempty and centered, so every resulting alternating centered product has trace zero. This avoids any requirement that the entire list of path coefficients have vanishing trace.

The factor finite-test argument lifts all finitely many ultrapower unitaries to unitary representatives and chooses one coordinate satisfying every test. For a center, the source applies the factor argument fiberwise only within the separable-predual stage. The countable measurable unitary sections obtained by exponentiating self-adjoint rational polynomials are fiberwise 2-norm dense. The test inequalities are open by telescoping unitary products; taking the first successful candidate is measurable. Integration then supplies the strict global tolerance. No global nonseparable direct-integral claim is made here.

The hierarchy is fixed before any harmonic map: `p_l=2^{-2^l}`, `n_l=p_l^{-3/2}`, `K_l=l n_l`, `d_l=K_l^4`. Every test family is finite, although very large. The four bad events respectively have bounds tending to zero: later levels `O(l sqrt(p_l))`, omitted base atoms `K_l^{-1}`, same-level label collisions `O(K_l^{-2})`, and a path missing the new level `l exp(-p_l^{-1/2})`. Labels are sampled before their values are interpreted, so possible equality between actual unitary values does not invalidate those probability estimates. The measure retains a positive dense base component. Its conclusion is moment convergence in probability, not norm convergence of sampled polynomials.

## Section 3: harmonicity, endpoint selection, and the first ultrapower

The bounded-ball 2-continuity condition is equivalent to a uniform modulus on each fixed operator-norm ball, by a sequence selected from any failed modulus. This modulus preserves the tracial ideal and passes to the coordinatewise lifted bounded linear map on an ultrapower. A representative bounded by `r+1`, with a halved tolerance, supplies the transferred modulus without assuming quotient infima are attained.

For `D(g)=T(g)g*`, harmonicity gives the Hilbert-space martingale `Z_n=D(U_1...U_n)`. The norm bound makes squared martingale increments summable; hence `Z_n` converges in Hilbert-valued `L^2`. The operator-norm ball is closed in tracial `L^2`, so the limit and its support points are elements of `M`, rather than merely unbounded affiliated operators.

The deterministic-limit case forces the same multiplier at every positive-mass atom; bounded-ball continuity and the dense atoms extend that multiplier to every unitary, then to the complex span of unitaries.

In the nondeterministic case, distinct support points `a,b` lie in the bounded ball. Independent prefixes from the two disjoint halves of a path give a positive probability of a forward endpoint near `a` and a reverse-inverse endpoint near `b`; martingale replacement errors tend to zero. The argument never asserts independence of `G` and `G^{-1}`. Concatenation is correctly restricted to **distinct unsigned block indices**, which makes the signed blocks independent walks. At each fixed finite stage, the positive conditioning mass is fixed first, and a later walk time is selected with total failure probability below half that mass. Shrinking conditioning masses therefore cause no uniform-selection gap.

The first ultrapower turns the finite selected moment inequalities into an exact countable free Haar family and turns the first-letter multiplier inequalities into exact identities on signed words with pairwise distinct unsigned indices. Freeness from `a,b` is neither asserted nor required. The second ultrapower used next has a different purpose and index.

## Section 4: distinct-index rigidity and finite-trace spectral forcing

The proof of the free-group length estimate separates exact boundary cancellation numbers. For each cancellation number the input and output basis decompositions have uniquely determined suffixes, and each matrix block has Hilbert–Schmidt norm bounded by the coefficient `ell^2` norm. Summing over the `q+1` cancellation numbers gives the stated estimate. Equal faithful trace moments of `(p* p)^m` determine its norm, so this estimate transfers to scalar word polynomials in the exact free Haar family.

For `s_r=r^{-1/2} sum g_j`, the length estimate gives the uniform operator bound `2`, before constructing the second ultrapower. Each block `z(z* z)^d` reduces to a nonempty word with positive endpoint signs. Block boundaries join positive signs and cannot cancel. For a fixed surviving word of length `q`, noncrossing cancellation records give coefficient `O_L(r^{-q/2})`. Repeated **surviving** unsigned indices have only `O_q(r^{q-1})` possible words. Their 2-norm error is `O_L(r^{-1/2})`; the homogeneous length bound upgrades this to operator norm. Canceled repetitions correctly remain within retained coefficients. No scalar term is lost because the block sign excess forbids one.

The alternating moment calculation counts the leading assignments with exactly `d` labels by Catalan noncrossing perfect matchings and `(r)_d`; assignments with fewer labels are lower order. The compactly supported Marchenko–Pastur density with those moments has no atom at zero. Faithfulness therefore gives zero kernel, and the finite trace upgrades the polar isometry to a unitary. Polynomial approximation is applied for fixed regularization, and bounded-ball continuity is used only afterward to remove regularization. Powers are expanded as literal ordered products; no commutation of the polar unitary with its modulus is assumed.

The final spectral lemma is the decisive forcing mechanism. Uniform sine sums bound `(a-b)X_{m,lambda}`. On a short spectral arc, the real part of the harmonic sum is at least `cos(1) h_m`. Multiplying on the **right** by its inverse on that arc bounds `(a-b)e`. Trace-weighted squared compression bounds sum without a factor for the number of arcs, forcing `||a-b||_2=0`. No commutation of `a,b` with the spectral algebra is needed. The source's bilateral-shift example in `B(ell^2(Z))` is a valid counterexample when the finite trace is removed, so the boundary condition is material and correctly retained.

## Section 5: normality, actual primitives, and all scope removals

The direct normal-map continuity proof truncates inputs to small two-sided supports, then chooses a subsequence with summable support traces. Tail joins decrease to zero. Normality transfers ultraweak convergence of annular compressions through the map, and lower semicontinuity lets the image 2-norm stay bounded below on a sequence of disjoint annular supports. Random signs keep the input operator norm bounded while the squared output 2-norm expectation grows linearly. This contradicts boundedness and supplies the needed modulus for an arbitrary normal linear map, with no positivity or complete-boundedness hypothesis.

Cesaro averaging in the last cochain variable is a contraction. Product ultraweak compactness preserves bounded complex multilinearity. Countable averaging is continuous on the common cochain norm ball by truncation with a uniform tail estimate, so the limit is harmonic. The fixed last-variable normal slice has a modulus uniform under right-unitary translation; that modulus survives averaging and the ultraweak limit. Thus the limit need not be normal. Liouville identifies it as a right module map in the last variable.

Expanding **the original** equation `df=0` at `(a_1,...,a_k,v)` and averaging after right multiplication by `v*` gives `dh=(-1)^k f`, hence the actual primitive `g=(-1)^k h` with `||g||<=||f||`. The proof does not require the averaging operator to commute with the Hochschild differential.

To remove separability in a tracial algebra, each finite input set is placed, together with its finitely many cocycle outputs, inside an independently chosen countably generated subalgebra containing unital matrix systems of every size. A nonzero finite homogeneous type-I summand would inherit each such system and cannot contain one larger than its finite degree; hence the subalgebra is type II1. Conditional expectation gives a separately normal cocycle there. Pulling its uniformly bounded primitive back solves the equation exactly on the selected finite set. A cofinal subnet eventually contains every fixed tuple, giving exact equality after compactness. Nestedness of the chosen subalgebras is unnecessary.

The final central decomposition does not assume a global scalar trace or countability of the partition. A maximal family of supports of normal states on the abelian center covers the type-II1 part. Faithful center-valued trace then supplies faithful normal scalar traces on each piece. The no-II1 complementary algebra is treated as one piece, whose primitive may have its own finite norm.

Crucially, central restriction alone solves only the cut cocycle. The source defines the explicit homotopy `J_z` and proves `dJ_z+J_zd=id-cut_z`, including degrees zero and one. On a colored tuple, its one nonzero insertion is immediately before the first complementary input. Every other differential term cancels or vanishes by central orthogonality. Thus `H_i=tilde b_i+J_{z_i}(z_i f)` satisfies `dH_i=z_i f` on **all** input tuples, with `||H_i||<=k||f||` uniformly over the tracial pieces. The bounded central product assembles a cochain valued in `M`; adding the normal-reduction cochain yields an actual primitive for the original ordinary cocycle. This is the mechanism removing type, separability, global trace, and central mixed-input restrictions; it is not an unsupported reformulation of the original problem.

## Manuscript deformation and fixed-source use

At `main.tex:131–139`, closed kernels and actual-image `H_b^3=0` give a Banach-space bijection `C_b^2/Z^2 -> Z^3`; `H_b^2=0` similarly gives the primitive quotient bijection. Strictly enlarged quotient inverse bounds produce actual representatives despite nonattained infima. Zero right sides are handled exactly. A bounded linear choice or complemented kernel is never used.

At `main.tex:141–149`, unsigned star reversal satisfies `dR_n=(-1)^{n+1}R_{n+1}d`. The displayed signs turn this into `dS_n=S_{n+1}d`. Although `S_n` is conjugate-linear in its cochain, it maps complex multilinear cochains to complex multilinear cochains. Real averaging is therefore sufficient. Average the approximate cocycle first, then choose and average its primitive; this preserves the stated primitive bound.

At `main.tex:151–171`, the associator gives exactly the displayed quadratic formula. Expanding `g mu(u,v)-(gu)(gv)` gives `Delta-dh+hDelta-m(h.,h.)`, without a missing product-norm factor or sign. With `||h||<=2L delta`, `||g^{-1}||<=2`, the bound is `D delta^2`, `D=8K+8L+16L^2`.

At `main.tex:173–184`, the chosen threshold implies every preceding smallness condition, geometric defect decay, and `sum ||h_n||<=1/4`. For the transport convention, the left ordered composition `g_{n-1}...g_0` is correct. Summable corrections imply norm convergence and `||Phi-id||<=exp(1/4)-1<1/2`; hence the limit is invertible, complex linear, and star preserving. The finite-stage conjugacy passes to the limit. If the original product has unit 1, surjectivity makes its image the unique unit of the original multiplication. Intermediate corrections need not fix 1. The independent `deformation_attack` agent separately reconstructed every one of these steps and found no counterexample or gap.

At `main.tex:219–233`, central opposite multiplication is associative, unital, involution-compatible, and has the same C-star norm. Roydor's Lemma 3.1 gives unital star-preserving compressed block maps, so the pullback is unital. The bilinear defect estimate has no missing `||F||^2`: the published block defects already quantify unit-ball source inputs. There is one deformation on the original fixed algebra, not one on each moving central corner.

At `main.tex:239–316`, the full-carrier inequality uses `||k-c_D(k)||<=1` in the approximate-order bound; its error tends to zero. Compressing by the complementary central projection forces the projection `h(1-z)` to vanish once that error is below one. Both source corners have full carrier, and unitality gives the complement closeness. A full abelian target corner forces type I. The center identification from the exact Jordan corner map preserves joins because it is an order isomorphism. On each degree `n`, the `n-1` abelian equivalent summands of the large corner and the full abelian complement have the same carrier, so finite matrix degree is reconstructed by equivalence of abelian projections with equal carrier. There is no cancellation of infinite cardinal dimensions. The classical full-corner and type-I structure facts remain explicit external inputs.

At `main.tex:321–354`, `P` and `E=eOe` are at most two fixed source von Neumann algebras. Universal upstream vanishing applies to each in its own right; cohomology of the noncentral corner `E` is not inferred by central restriction. Infinite type-I and type-II/III components enter the halving source `P`; the odd finite degrees enter one fixed product corner `E`. All remaining near-isometry/compression errors are uniform functions of initial distortion tending to zero. A finite set of threshold requirements therefore gives `forall M exists epsilon_M forall N`. It does not give a universal epsilon. Strict Banach–Mazur inequality supplies an actual comparison map without requiring attainment of the infimum.

At `main.tex:356–368`, adjoint norms and inverse norms give the distance inequality in the correct direction. Exact Jordan star isomorphisms are normal order isomorphisms and yield isometric canonical predual maps. Surjective predual isometries adjoint to algebra isometries, whose unitary factor can be removed in Kadison's theorem to obtain Jordan structure. The zero-algebra convention is handled separately and consistently.

## Fresh falsification artifacts

Reproduction command:

`python3 reviews/whole_final_package_freshreview2_20261007/upstream_deformation_checks/mechanism_checks.py`

The independently written script and JSON record have no imports from earlier audit code. Script SHA-256 is `23b26030b4c34ea2c698200ccaf22a7337d7dcf41eacdb62d434230b8319cb6b`.

It checked the homotopy with arbitrary formal cochain outputs and **noncommuting** variable words in each of the two central colors: every one of the 1,022 input-color patterns in degrees 1 through 9 canceled exactly. The proof's degree-zero convention is immediate because `cut` is identity and `J` is zero. It also exhaustively reduced eight ordered block products at three labels, including internal cancellations and multiple blocks, and verified nonempty positive endpoint signs. Leading alternating identity-word label counts for moments `d=1,...,5` equal `Catalan(d) d!`: `1,4,30,336,5040`.

These are finite mechanism checks supplementary to the mathematical reconstruction. They do not prove infinite-dimensional Hochschild vanishing or authenticate Lean.

## Assessment of archived supporting audits, read afterward

After completing the independent reconstruction and fresh checks, at the parent's request I read the archive's complete `reviews/cohomology_adversary.md` and `research/involutive_deformation_adversary_20261007.md`.

The cohomology audit's mathematical mechanism claims agree with the actual sources and the reconstruction above, including the essential distinctions between the two ultrapower indices, moments and norms, disjoint-half independence and path/inverse dependence, canceled and surviving repeated labels, fixed-stage conditioning, retained 2-continuity and lost normality, and central cuts and mixed inputs. Its derived estimate `dist(T,InnDer(M))<=||dT||` for a normal map on a tracial II1 algebra follows from the norm-one normal cocycle primitive and the classical inner-derivation theorem; it is not claimed for all arbitrary coefficient modules. I found no contradiction in that optional consequence. Its warning against inferring a universal Banach–Mazur threshold is justified.

Its old finite checks on `C direct-sum C` alone would not test noncommuting outer actions; the present formal-word check addresses those actions, while the written all-degree cancellation remains the proof. The archived audit's claims about actual Lean declaration inspection and a no-`sorry` search are **static evidence**. The current ZIP contains a scope document but no Lean source tree or clean build of the declaration closure. Those statements cannot supply fresh kernel evidence, audit all imports, or establish semantic fidelity of the formal theorem. Its own limitation paragraph correctly says as much. Its 95% checkpoint estimate describes that audit's work and conveys no theorem confidence or readiness score.

The deformation audit proves a somewhat broader, possibly nonunital conditional lemma; the manuscript uses only its unital specialization. Its enlarged selection constants, conjugate-linear averaging, correction identity, and ordered-product convergence are all substantiated by direct calculation. Its sample threshold differs from the current manuscript threshold; the manuscript's `1/(16L)` bound independently yields the required strict near-identity estimate at the non-strict endpoint. Neither audit certifies the ordinary cohomology input by itself, a geometric bridge, novelty, or publication readiness. The manuscript correctly limits reliance to attributed mathematical proof and explicitly disclaims a reproduced formal build.

Final checkpoint, 2026-10-07 15:07 UTC: assigned source/deformation reconstruction complete; **100% scoped completion**; no substantive issue found requiring a manuscript repair in this assigned scope. No Git, push, release, deposit, or external communication was performed.
