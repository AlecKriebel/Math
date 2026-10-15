# Independent analytic falsification review

Review checkpoint: 2026-10-06 21:41 PDT (2026-10-07 04:41 UTC).

Reviewed input: `/Users/alec/Desktop/math`, HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, read-only. The review concerns the mixed-K3 manuscript's analytic realization dependency, not the entire rational-Hodge argument or a publication package. Best-guess completion of this assigned analytic audit: 100%; this is not a percentage of resolution of the global Hodge conjecture or of publication readiness.

## Verdict and exact scope

**The particular relative interior-rooted construction passes this audit.** Its tree normalization, fixed ordinary outputs, reciprocal switches, empty external word, stable constant roots, relative chart extension, CF extension, Stokes identity, deformation identity, and filtration can be rederived from the supplied argument and the cited source machinery. There is a checkable finite relative adaptation of the quasi-component construction; it is stronger than an assertion that two combinatorial trees happen to agree. I found no specific unproved condition or counterexample in that adaptation. The product/category completion also passes the checks described below, conditional on the stated ordinary factor HMS and generation inputs.

This verdict **does not independently certify** the topology/surgery input, ordinary quartic or torus HMS, all the graph-image/generation assertions, semiregularity/Hodge deformation in `cohomology.tex`, exact universal Kuga–Satake algebraicity, or the downstream Hodge theorem. Those are different pivotal dependencies. It does not say that the analysis is formalized in Lean. No PDE build can verify a Kuranishi proof. It accepts the published/chart-source results enumerated below as mathematical inputs and checks the application and the additional relative argument.

The audit began with the original project request and primary sources rather than with a favorable verdict. A separately delegated narrow reviewer rederived the corner construction; its report is `checks/analytic_falsification/corner_rederive.md`. Its final assessment agrees with the relative-extension argument below. That assessment is supporting evidence, not the proof.

## Reviewed artifacts and source provenance

The four pinned manuscript SHA-256 hashes are:

| File | SHA-256 |
|---|---|
| `build/manuscript/curvature.tex` | `5eb8d9656ceeab8aa4dfdceb10566b61ed9d44a23113188ceae11c39dc880f49` |
| `build/manuscript/topology.tex` | `153d29eed2f02aa956ac8898dbf01fd5b13c4e4e69999a5f67bdbf501d921864` |
| `build/manuscript/comparison.tex` | `f6e817648b5866991cff23b7e90643c00d8924f85f8d5e0128643f90ae148be2` |
| `build/manuscript/realization.tex` | `338c65d26d9cade6acffc202127697f51af84853a19a2506daf1489080f9ef8d` |

Read supporting portions of `setup.tex`, `references.bib`, and the repository README as well. The repository explicitly describes the manuscripts as AI-produced results at different verification stages; the presence of this argument in a release is not treated as validation.

Primary texts retained solely as local research sources under `checks/analytic_falsification/`:

| Source | Version/download | SHA-256 of source file |
|---|---|---|
| [AFOOO, Quantum cohomology and split generation](https://arxiv.org/html/2606.12257v1) | v1, fresh HTML retrieval; readable text copied from project source cache and cross-checked against the HTML | `b29fe9b8ee8fbdc3bf9bc61665ae27a16ebda90aa0bf6f6861c7fa5fbceac050` |
| [FOOO Charts I](https://arxiv.org/pdf/1710.01459) | downloaded arXiv PDF | `118cc46d5339ac34c9a123448c148564c2f63482b6d5244be728169bff4952fe` |
| [FOOO Charts II](https://arxiv.org/pdf/1808.06106v2) | v2, February 2024 | `4b4ff7ec0b86cc84a26376489ca15d187a0e3daa88b672a3f62d9c34ad5e4068` |
| [Charts I corrigendum](https://arxiv.org/pdf/2403.19683) | arXiv PDF | `ba9557c9500b74ea7948f6077e673b7ca577f39b909b0631b3f2e516a797c52e` |
| [FOOO exponential gluing](https://arxiv.org/pdf/1603.07026v2) | v2, as explicitly cited upstream | `5b65330bb4dc427e20028b892bbea23fe15bb32413e2e6c94b3fa1c1839c5d6f` |
| [Akaho–Joyce](https://people.maths.ox.ac.uk/joyce/AkahoJoyce.pdf) | authors' JDG paper PDF | `988f1146e9aa6cb1caa553fb70dd28cbb98c6dc2048a3c894b3f29582b27fc05` |

These are research-cache copies; their third-party redistribution rights have not been audited and they should not automatically enter a publication upload kit. Plain-text conversions were made with `pdftotext -layout`. No upstream files were changed, no git operations were performed, and no external person was contacted.

## Claim being checked

Let $i:L\to D$ be a closed graded spin Lagrangian immersion into the compact symplectic $2n$-manifold in the manuscript. Assume transverse double points, no triple points, zero spin background/bulk class, integer grading, all branch generators of odd degree, and the prescribed fixed split $J_0$ with no nonconstant spheres. Include a finite collection of the embedded test branes, each with no nonconstant self-disks at $J_0$. Accept for this review the topological injection

\[
i_*:H_{n-2}(L;\mathbb Q)\longrightarrow H_{n-2}(D;\mathbb Q)
\]

and the stated description of $H^2(L)$.

The proposed analytic conclusion is that the fixed finite cyclic immersed disk system can be supplemented, through any sufficient finite cutoff, with scalar interior-rooted integrations $p_k^\eta$, $\eta\in\Omega^{n-2}_{\mathrm{closed}}(D)$, such that

\[
p_1^\eta(m_0)=0,
\qquad p_{1,0}^\eta(c)=\pm\int_L c\wedge i^*\eta,
\]

and, for every positive-valuation degree-one boundary insertion $b$,

\[
\sum_{r\ge0}p_{r+1}^\eta(m_0^b,b,\ldots,b)=0.
\]

This makes the first curvature coefficient exact. Canonical transfer then removes curvature and bounds the degree-two self-Hom by $b_2(L)$. The remaining category comparison/projector realizes a perfect complex with the prescribed Euler data and this Ext² bound.

## Exact source-hypothesis map

| External input | Actual hypotheses/obligations needed here | Supplied argument and disposition |
|---|---|---|
| AFOOO Theorems 9.3, 9.6 | finite closed spin immersed collection in compact symplectic target; transverse off-diagonal sectors; compatible relative spin/background and bulk data; filtered coefficients | `curvature.tex` 17–88 fixes finite collections, transverse copies, grading, spin, and zero background/bulk. Source gives curved cyclic category and homotopy units, **not** automatic unobstructedness. Unobstructedness is proved separately. Pass under stated geometric setup. |
| AFOOO Propositions 9.18, 9.20 | ordinary boundary charts and CF perturbations compatible with normalized boundary products; output/diagonal evaluation weakly and strongly submersive; cyclic ordinary system | Their statements explicitly provide the needed ordinary data. `curvature.tex` 196–201 fixes this geometric system before adding roots. The proof uses child output submersivity, not joint submersivity of all parent evaluations. Pass. |
| Charts I Theorem 7.1 | actual obstruction bundle data: local support, smooth transport, augmented regularity, semicontinuity, invariance/effectivity, compatible neighborhood germs | `curvature.tex` 311–394 supplies compact-core sections, finite-group saturation, faithful augmented directions when needed, nested quasi-index neighborhoods, and inclusions. The relative extension proof below verifies the root/ordinary coloring preserves these properties. Stable constant roots require the constant-case clarification below. Pass. |
| Charts I Condition 7.11/Lemma 7.12 | evaluation restricted to the augmented kernel surjects onto $TL$ | Required on ordinary children and supplied by the ordinary system. No condition is imposed at the interior evaluation. At a diagonal match, subtracting a surjective child evaluation is surjective. Pass. |
| Charts II Definition 5.1/Theorems 5.3, 5.4 | disk-component-wise equality of obstruction data on boundary strata; compatible germs of charts, corners, and corner consistency | Direct sum on components, fixed outgoing child flags, and the mixed-root quasi-component extension in `curvature.tex` 262–394. Theorem 5.4 is not directly a theorem about this new two-type system; its constructive proof is adapted below. Pass of that adaptation. |
| Charts II Conditions 8.12–8.15 and Props 8.17–8.18 | open quasi-choice family; containing proper closed family; invariance; boundary union by vertex; direct sum; augmented regularity and effectivity; compatible stabilization/trivialization and shrinking constants | The manuscript's proper/open inherited family and off-collar compact-core additions are precisely the proof's mechanisms. Root type is preserved under contracted subtrees, giving Lemmas 8.19–8.20 for both types. Generic additions are made only outside the retained smaller collar. Detailed check below. Pass. |
| FOOO gluing Assumption 3.12 | augmented component operators surjective; difference of nodal evaluations surjective | At diagonal nodes, child output submersivity suffices. The tree's recursive variation construction gives all equations together. At switches, target matching is a point, and the fixed-jump operator is used instead of falsely requiring an $L$-diagonal match. Pass. |
| FOOO Theorems 3.13, 6.4, 8.16–8.17 | stabilized domains, compact-core obstruction transports, preceding regularity/matching, sufficiently small neighborhoods; family gluing including domain parameters and exponential derivatives | Auxiliary stabilization, support away from nodes/ends, transport and shrinking appear in `curvature.tex` 311–366. No angular interior-node gluing is needed because there are no sphere components. Family version accommodates the root mark. Pass using the fixed-jump immersed gluing input at switches. |
| Akaho–Joyce §§4–5, AFOOO immersed construction | compactness with lifted boundary arcs and reciprocal labels; fixed-jump Fredholm/capping problem; orientations from spin data; reciprocal cap dualities | Full sectors are retained. Reciprocal labels are not discarded before composition. The constant strip contraction uses the same determinant duality as ordinary gluing. Pass. |
| Charts I corrigendum Lemma 2 | corrected smooth corner coordinates; double-log/admissible profile when needed | `curvature.tex` 63–66 and 288–302 explicitly adopt corrected conventions and the admissible category. No claim that exponential plumbing or ordinary forgetting is globally smooth. Pass. |
| AFOOO §14.3, Definition 14.9/Prop 14.10 | admissible data; compatible forgetful obstruction system; bi-collared versions when pulling back outer-collar CF data | Root construction retains the interior mark, has no requirement to forget its external inputs, and auxiliary forgetting is local stabilization. Ordinary factors already carry source-admissible data. Chain contraction has total neck length $T=\sum T_i$; admissible pullbacks suffice. Pass; ordinary smoothness would be false. |
| AFOOO Prop 14.8/Remark 14.7 | compatible **collared** charts and CF representatives on boundary factors; agreement on iterated normalized corners; then a neighborhood CF perturbation exists | Verified by the direct-sum quasi-component construction and common normalized-tree factor systems. Outer collar is supplied before invoking Prop 14.5. Tree agreement alone would be insufficient, but it is not the entire argument supplied. Pass. |
| AFOOO Prop 14.5 | oriented obstruction-data Kuranishi space; strongly smooth weakly submersive map $f$; compact prescribed $K$; existing transverse CF system strongly submersive near $K$; allow compatible thickening | Choose $f$ to a point, so map conditions are automatic. The smaller closed corner neighborhood is compact at a cutoff and its CF system was constructed by collaring. Compatible thickening retains its virtual integrations near that set. Pass; this proposition is not used as an initial chart-existence theorem. |
| AFOOO Props 16.3, 16.14 | distinguished interior mark; mixed root $\mathfrak p$/ordinary-bubble $\mathfrak q$ system; orientations and cyclic action; boundary decomposition; special weakly stable zero-input constant root when interior evaluation is to be submersive onto $D$ | Sources explicitly construct relative to given ordinary $\mathfrak q$ data and keep those data on bubbles (Remarks 16.5, 16.13). Here only scalar integration is required. Thus the unstable zero-input constant root and its $S^1$ special chart are excluded; stable one-input constants remain. No interior submersivity claim is imported. Pass of the simpler variant, as rederived below. |
| Source Stokes/composition theorems | oriented virtual integrations; closed interior form; strongly submersive child matches; boundary/corner compatibility with weights | All boundary matches are either child-submersive diagonals or points. Signs and dimensions checked below. Pass. |

The source locators in the retained readable AFOOO text are especially useful: Props 14.5/14.8 at lines 7363/7562; admissible forgetting at 7620–7780; Props 16.3/16.14 at 8638/8949; relative-to-given-ordinary-system assertion at 8753–8758; ordinary-bubble distinction at 8911–8937. Charts II Theorems 5.3/5.4 occur at text lines 790/797; Conditions 8.12–8.15 at 1970–2081; full neighborhood extension proof at 2113–2292.

## Checkable relative chart construction

Here is the additional finite construction, independently reorganized so each use of the source proof has a visible hypothesis.

1. There are two types of component problems: ordinary boundary-rooted $Q$, whose data are fixed, and additional interior-rooted $P$. A connected disk subtree has type $P$ precisely if it contains the unique distinguished interior mark; otherwise its unique edge toward that mark gives its ordinary output. Every connected subtree and every partially smoothed tree consequently has a uniquely determined type. This rule is compatible with repeated contractions and never changes an ordinary output.

2. Work in a finite induction order closed under boundary factors. On a $P$ boundary tree prescribe the **actual union** of quasi-component indices on its vertices: the inherited $P$ indices on its root and the fixed $Q$ indices on ordinary vertices. Cores on different components are disjoint. On an iterated boundary, the same compact-core choices, their stabilization data, and their flags are used, whichever edge was normalized first. This supplies the component-wise equality required by Charts II Definition 5.1, with the usual normalized-edge ordering and determinant signs.

3. To check openness, take a sequence of partially smoothed boundary trees approaching a more broken tree. In the proof of Charts II Lemma 8.19, each selected compact-core choice lies on a vertex of the finer tree. Its image vertex in the coarser tree is a connected subtree of the finer tree. It is $P$ if and only if that subtree contains the mark, and $Q$ otherwise. The induction hypothesis on that lower-cost component gives exactly the same inherited quasi-choice in its neighborhood. Thus the proof of openness applies with the two colors; there is no accidental replacement of fixed $Q$ data by $P$ data.

4. The properness proof of Lemma 8.20 has the same check. After fixing the finite tree type and extracting a subsequence, a vertex in a partially smoothed tree converges to a connected subtree. Its inherited compact-core choice converges to a choice on the correctly colored subtree, by the induction hypothesis. The union prescription then gives the required limiting total index. Finite type and compactness at the cutoff are being used here, not the bare statement that every individual fiber contains finitely many choices.

5. Definition 8.21 extends these open/proper choices to a sufficiently small boundary neighborhood, keeping their boundary restriction. It is applicable because both preceding lemmas now hold. On that neighborhood, direct sums, surjectivity and effectivity persist by openness. On the complementary compact part, choose finitely many new compact-core choices, transverse to the inherited ones and their translates, and saturate under finite symmetry groups. Infinite-dimensional spaces of core-supported sections supply room for these finite direct-sum requirements. The additions have support away from a smaller boundary neighborhood. All old ordinary factors remain unchanged there.

6. Compact-core obstruction surjectivity follows from the usual adjoint unique-continuation argument: a cokernel functional annihilating every interior core section vanishes on the open core and hence on the component. Finite saturation does not reduce the span. Faithful augmented directions can be supplied by supported variations on a free finite-group orbit; $D_u\xi$ in the obstruction space makes the pair $(\xi,D_u\xi)$ an augmented-kernel variation. They remain independent modulo reparametrizations because they have localized support. This is a finite-dimensional chart construction, not an assertion that an equivariant single-valued transverse section exists.

7. The same component argument works for **constant stable switching roots**. Such a root already has the interior mark plus at least one boundary flag, hence a stable domain; no immersion-point incidence stabilization is needed. The fixed-jump Fredholm operator is the immersed source operator, and compact-core adjoint unique continuation applies even though $D u=0$. Its finite group can be handled by supported variation representations. The exceptional diagonal one-input constant root is regular and is exactly $L$. The only constant zero-input root is unstable and is excluded. This closes the apparent wording asymmetry in the manuscript's phrase “smooth nonconstant root.”

8. At a diagonal tree edge, augmented matching is surjective because the child's output evaluation is surjective. For simultaneous matching, first choose a root variation, then choose each child's variation with the required output value and recursively choose its descendants. Changes of that child's input evaluations can be compensated only further down the tree. No joint-submersivity assumption at all flags has been smuggled in. A reciprocal-switch match is over a point, so it has no matching tangent constraint.

9. Stabilized gluing transports exactly these obstruction choices from compact cores. Assumption 3.12 and the corresponding fixed-jump immersed gluing are satisfied by steps 6–8. The exponential family estimates and corrected gluing profiles give charts and changes of charts; the quasi-index inclusions give semicontinuity and cocycles. Charts II's proof of Theorem 5.3 then gives boundary/corner consistency at the level of germs. Its Remark 6.1 permits compatible representatives for any finite collection, which is all the finite-cutoff argument uses.

10. Pull back the common normalized-boundary CF representatives by the outer collar projection. Because the preceding charts, indices and their changes actually agree on further normalization, this is the collar step of Prop 14.8, including stabilizer quotients and ordered normal lines. Apply Prop 14.5 with target a point relative to the smaller closed collar. Finite cyclic symmetry can be handled on the finite quotient system, or by the usual group-equivariant CF auxiliary parameter families. Pullback gives cyclic integrations with their stabilizer weights. Compatible thickenings preserve the already prescribed collar integration, so ordinary child counts have not been changed.

This is an existence proof through each cutoff. It does not require compatible analytic choices simultaneously for an infinite object set or all energies, and it does not invoke Prop 14.5 before a Kuranishi/collar system exists.

## Normalized strata, stabilization and boundary cases

The relevant list is exhaustive under the stated fixed-$J_0$ sphere exclusion:

| Configuration | Required treatment | Check |
|---|---|---|
| Boundary node with equal lifts | fiber product over $L$ | child output strong submersivity supplies matching and composition |
| Boundary node with distinct preimages $p,q$ | reciprocal flags ((p,q),(q,p)), product over a point | retain both flags until contraction, even if the external word is empty |
| Any set of several disk nodes | oriented product on a tree rooted at the marked vertex | paths to root and factor types independent of cutting order; normals carry permutation signs |
| Ordinary child carrying a whole external word | ordinary child output remains its attaching node | cyclic rotation of external labels changes positions/linear orders, not this output |
| Automorphism interchanging isomorphic subtrees | finite quotient of the same decorated directed tree | fixes interior mark, preserves output paths, permutes cap/normal lines with determinant signs |
| Constant root with mark and one attaching boundary node | stable $P_1$ factor | retained; diagonal zero-energy sector is regular $L$ |
| Constant root with mark and no boundary flag | unstable disk with $S^1$ automorphisms | excluded; no ambient-evaluation submersivity is requested, so the special source $S^1$ chart is unnecessary |
| Constant ordinary bivalent component after forgetting auxiliaries | contract | two diagonal nodes on one sheet or two reciprocal switches; exactly one switch impossible for a constant lifted boundary arc |
| Chain of such bivalent components | concatenate neck lengths and reciprocal contractions | $T=\sum T_i$ and determinant gluing are associative; ordinary smoothness of forgetting is not claimed |
| Constant stable switching polygon | retain as finite zero-energy type | arity controls its flags, and local fixed-jump charts apply |
| Nonconstant sphere or disk boundary collapse retaining a sphere | absent | fixed $J_0$ has no nonconstant spheres |
| Tree of constant spheres attached at one point, carrying at most the one mark | absent by stability | only two total external special points are available; a tree of stable constant spheres requires at least three |

Cyclic symmetry of $p_k$ does **not** require cyclic symmetry of an ordinary child's $m_s$ in its input positions alone. Its distinguished output is geometrically fixed by the path to the interior mark. Rotating the total external labeling transports the same ordinary problem with that same output. Ordinary cyclicity pertains to the source boundary-rooted system with its pairing; it does not authorize an illicit rerooting of a fixed child in this construction.

## Stokes and curvature removal

For diagonal sectors, $P_{k,\beta}$ has virtual dimension $n+k-1$. With all external inputs equal to degree-one $b$, the integrand $\eta\wedge b^k$ has degree $n+k-2$, exactly one below top degree. Thus Stokes gives an identity on the normalized virtual boundary. At $k=0$, its boundary consists of an interior root with one input attached to an ordinary curvature child. Composition gives $p_1^\eta(m_0)$. Reciprocal-switch children are included first; their curvature outputs then vanish because integer degree two cannot lie in an odd-degree point sector. This is not an assumption that the external empty word has no switching strata.

At zero energy the diagonal $P_1$ constant disk has one boundary mark and one interior mark. The three real marking parameters exhaust disk automorphisms; the constant-map operator is regular. The moduli space is $L$, evaluations are identity and $i$, and its integral is $\pm\int_L c\wedge i^*\eta$. The orientation sign is fixed and nonzero. The removed unstable constant $P_0$ contributes no missing stable boundary term.

For $k>0$, an ordinary child has $s$ consecutive inputs and its root factor has $r=k-s$ remaining external inputs plus that child output. In suspended degrees every $b$ has degree zero and $m_s(b^s)$ has degree one. All cyclic moves past $b$ and all suspended insertion signs therefore have sign (+1). This includes the degree-one branch sectors. There are $k$ normalized labeled placements for every $s$: gaps for $s=0$, starts of the child block for $0<s<k$, and rooted linear orders/attaching gaps for $s=k$. Input differential terms also have $k$ positions. External cyclic labels are not being quotiented, and finite stabilizer weights remain in each term. Dividing by $k$ yields

\[
\sum_{r+s=k}p_{r+1}^\eta(m_s(b^s),b^r)=0.
\]

The separate $k=0$ identity supplies the missing coefficient, giving the claimed deformation identity. Differentiating input forms is the zero-energy de Rham part of $m_1$; $d\eta=0$, and there is no boundary-output differential. These degree and multiplicity checks agree with the cyclic Hochschild-boundary mechanism of AFOOO's interior-rooted operation.

If $c_E$ is the first coefficient of $m_0^b$, the deformed curved $A_\infty$ relation makes $dc_E=0$. Every other term in $R_\eta^b$ has positive valuation, so at this first energy the pairing identity reads

\[
\int_L c_E\wedge i^*\eta=0
\quad\text{for all closed }\eta\in\Omega^{n-2}(D).
\]

By the assumed ambient homology injection and Poincaré duality, ([c_E]=0). This deduction is valid and identifies exactly where the topological input enters.

Canonical transfer has positive-valuation arity-zero part $F_0$, because zero-energy curvature is absent. Its zero-input functor equation is

\[
m_0^{\mathrm{forms},F_0}=F_1(m_0^{\mathrm{can}}).
\]

If canonical curvature had a first nonzero coefficient, its degree-two component lies in $H^2(L)$, since all branch generators are odd. $F_{1,0}$ is the cohomology identification; it therefore gives a nonexact leading form. This contradicts the preceding exactness. The same contradiction can be made through a sufficient finite geometric cutoff after composing with the promotion pseudo-isotopy. The relative $p_k$ need only be built on that representative; they need not be identified under all pseudo-isotopies. There is no circular assumption that a bounding cochain already exists.

## Uniform filtration audit

The energy lemma has a valid lattice argument. The finite union $K$ of brane images has finite homotopy type and arbitrarily small regular neighborhoods. The relative symplectic class can be represented by a form vanishing near $K$: local primitives vanish on every Lagrangian sheet, and at transverse double points the standard radial primitive does so simultaneously. Relative de Rham theory on a deformation-retracting neighborhood supplies the same conclusion. Stokes with transverse-end decay identifies its period with polygon area.

Choose a basis of finite-dimensional $H^2(D,K;\mathbb R)$ represented by such forms. Their pairings with a $J_0$-holomorphic polygon are bounded by constants times its area. Bounded energy therefore bounds every coordinate of its integral relative homology class in a finite-rank lattice modulo torsion. Only finitely many energy values occur below a bound, irrespective of the number of markings. This proves a common positive nonconstant energy gap $\delta$. It does not assert that the entire period group is discrete.

For $0<\varepsilon<\delta$, ordinary-vertex cost is $E+\varepsilon(k-1)$ and root cost is $E+\varepsilon k$. A split into a child with $s$ inputs and a root with $r+1$ inputs satisfies

\[
(E_P+E_Q)+\varepsilon(r+s)
=[E_P+\varepsilon$r+1$]+[E_Q+\varepsilon(s-1)].
\]

Each factor has positive cost: nonconstant ordinary zero-input children cost at least $\delta-\varepsilon$; ordinary zero-energy stable children have at least two inputs; constant one-input roots cost $\varepsilon$; unstable zero-input constant roots and unary constant strips are excluded. Hence each proper boundary factor has strictly lower cost. The finite arity/energy closure has finitely many stable tree types; constant switching polygons are counted by arity. The additive energy monoid is locally finite because a bounded sum has at most $B/\delta$ positive terms.

For a positive-valuation $b$, at most (B/v(b)) insertions contribute below energy (B). The union of the finite supports of the energy system and $b$ below a bound remains locally finite. Thus deformation sums and first-coefficient detection are legitimate. Finite-cutoff promotion at fixed $J_0$ uses the same gap; embedded disk-free objects can retain arity-zero translation zero. On strict words, zero-energy transfer is identity on point complexes and no repeated-label transfer operation is needed.

## Product comparison and the finite-cutoff passage

The following source-to-argument checks were made on `comparison.tex`; ordinary factor HMS itself remains an accepted independent input.

* The Hamiltonian strip data vanish near all transverse intersections, so asymptotes stay fixed. Strip energy equals symplectic area. A constant strip has the transverse invertible operator. Stable strict-word polygons cannot converge to a constant vertex because it would meet at least three distinct labels, forbidden by the no-triple-intersection hypothesis.
* Small Hamiltonian core terms do not create sphere/disk bubbles: they disappear at bubble scale, leaving $J_0$-holomorphic bubbles, which are excluded. Neck curvature is zero for pure strip models, and core curvature has uniform bounds for finitely many words. This makes parametric compactness and positive-area gaps uniform over the small path, including long-neck degeneration.
* Domain-dependent Hamiltonian variations on interior cores suffice for polygon regularity without a simple-map assumption; strip regularity uses the cited regular-point argument and its erratum. Face data have lower-arity independent label tuples. Relative face extension keeps freedom on the remaining open cores. Countably many prescribed chain strata can be included in one Sard–Smale choice.
* In the virtual comparison, Hamiltonian terms are smooth lower-order compact-core terms. Core-supported obstruction sections still kill cokernels. Path projection submersivity follows by solving the augmented equation at a fixed path parameter. At isolated ends there is no matching zero mode. Component augmentation, weighted parametrix, $O(T^{-1})$ cutoff error, exponentially small seam/core errors, Neumann correction and uniform quadratic estimates give the usual gluing. This is the actual adaptation needed to use unforced disk-chart sources with forcing, and it is supplied in the manuscript; a bare unforced citation would not suffice.
* The coefficient-coordinate discussion retains strip-core auxiliary marks when needed. It does not claim that an inverse total-neck length is a smooth function of inverse lengths after a chain has been contracted. Corrected inverse/double-log chart smoothness is distinct from the exponential plumbing coordinates used to describe domain chains.
* Strict directed systems have bounded arity and finitely many finite-dimensional Hom spaces. Thus their functor equations, including inverses of $F_1$, are a finite polynomial system. Finite-cutoff approximate solutions have uniformly nonnegative-valuation coordinates and inverse coordinates. If the equations generated the unit ideal, a fixed Nullstellensatz combination would evaluate to a positive-valuation expression equal to $1$ for a sufficiently accurate solution. This contradiction is valid. It gives an actual solution over a field extension, not a compatible infinite geometric choice.
* The geometric chain complex's inward prism contracts each arity to an interior point, respects ignored-product-factor relations, and gives the acyclicity used for the associahedral operad homotopy. Countability of the generated chain family is enough; no acyclicity of its countable suboperad is assumed.
* At a parameter face one inward parameter may smooth several target nodes: $\lambda_i=t c_i$, $c_i>0$. Fixed-domain indices add at discrete matches. Codimension of the parameter face, rather than the number of these simultaneous nodes, is the dimension loss. The manuscript uses oriented-end coverage for $t>0$, so it does not need an unjustified smooth solution map in exponential coordinates at $t=0$.
* Internal-strip ends occur twice with opposite translation direction and cancel; external breaks give the Hom differential. Grafting uses the same discrete matches. Factor counts on cross-product chains have additive indices, so regular rigid product configurations factor into rigid factors.
* The written determinant parity reduction $b(l+q+r+o)+q(b+q+r+o)+(r+o)(b+q)=bl+q$ is correct mod $2$. Reciprocal normalization absorbs the node term, while direct-sum cap contractions give the graded tensor-evaluation sign. The count normalization $(-1)^{d(d-1)/2}$ removes both composition/cross-product parameter signs and makes boundary counts dg. The final arity-by-arity sign-cocycle rescaling is algebraically correct.
* Along the operadic path, the differential is fixed and arity is bounded. Characteristic-zero arity induction with identity linear part integrates the homotopy. Rectification over the finite product of object fields and tensoring strict quasi-isomorphisms over a field identifies the cellular-diagonal tensor with the ordinary dg tensor. This is the enhanced, rather than merely cohomological, comparison needed later.

No precise analytic hypothesis was found missing in these adaptations. This conclusion relies on the imported ordinary isolated-end/gluing framework, not on a numerical test of elliptic operators. The separate ordinary-HMS/generation assertions can still block the global realization if their dedicated audits fail.

## Category, pairing, field and trace obligations

`realization.tex` does not use a residue-field trace argument. It uses the following different obligations, checked here.

1. **Copy inverses.** Strict pair comparison gives one-dimensional $H^0$ between distinct copies of the same test; comparison for all orders on the *same* full category gives a nonzero binary product on every three distinct copies. If $u:A\to B$, $v:B\to A$, $w:A\to C$ are nonzero and $vu=0$, then $w$vu$=(wv)u$ contradicts these three-copy products. Self degree-zero cohomology has rank at most one; cohomological units then make $vu$, $uv$ nonzero scalar identities. This avoids assuming a directed comparison already identifies repeated-label operations.

2. **Ultraproduct.** Canonical chain ranks and degrees bound every fixed graded Hom. Choose ranks constant on an ultrafilter and pass minimal structures, functors, pairing matrices, units and invertible arrows by finite matrix equations. Nondegeneracy passes by invertible determinant matrices, not by vague preservation of an infinite-dimensional pairing. Each fixed $A_\infty$ equation has finitely many terms. Countable ultraproduct of fields of size at most continuum has size at most continuum and characteristic zero. An abstract embedding into $\mathbb C$ exists by transcendence bases; it need not fix the original coefficient copy of $\mathbb C$. `setup.tex` explicitly defines the resulting complex mirror by scalar extension along this embedding, so this is not illicit convergence/evaluation of Novikov series.

3. **Recovering full Homs.** For an original object $j$, later cofinal copies $j_k$ give a telescope of directed Yoneda modules. At every argument $i$, sufficiently late $j_k$ satisfy $i<j_k$, so strict-arrow comparison identifies the telescope with the restricted full representable. Taking derived Hom from the telescope gives a homotopy limit; transitions are equivalences by copy invertibility. This proves full faithfulness of restricted Yoneda on the full copy category, including higher module structure. It is not a claim that a single finite directed subcategory already contains all full self-Homs.

4. **Generation and projection.** Given the ordinary factor generation theorem, external products generate the product's perfect category. Smooth proper `Perf` is saturated; pointwise finite-total-cohomology modules are pseudoperfect, hence representable in this smooth proper category. The restricted module of $L$ is such a module by properness. Its representing object $\mathcal E\to L$ has right-orthogonal cone $R$.

5. **Cyclic duality.** The original forms/intersection pairing transfers to a nondegenerate finite canonical pairing; with removed curvature it gives Serre shift $[n]$. Its extension to twisted complexes and retracts supplies the same duality on the hull. Therefore right orthogonality of $R$ implies left orthogonality, the connecting morphism vanishes, and $L\simeq\mathcal E\oplus R$. This makes `Ext²(E,E)` a direct summand of `Hom²(L,L)`, proving the required bound. Properness alone would not give this splitting; the cyclic/Serre obligation has been used explicitly.

6. **Euler data.** The transverse Floer chain complex computes Euler characteristic as signed intersection number, unaffected by differential, scalar extension or ultraproduct ranks. Its common sign is set by the same grading convention at every test. $\mathrm{PD}(i_*[L])=\nu a$ then gives one common nonzero rational scalar, and the orthogonal $R$ pairs trivially with every test. This supplies the stated Euler pairings without a trace specialization.

There is a boundary–bulk/Atiyah-class trace used later in `cohomology.tex`. Its semiregularity injectivity and compatibility with Hodge deformations have **not** been independently verified in this review. A residue-field trace used in another family-032 companion must likewise receive a separate audit; it is not a missing line of `realization.tex` and cannot be certified by the category checks here.

## Falsification attempts and reproducible checks

The following possible defects were specifically tested and rejected for the supplied version: restricting an empty external word to diagonal internal nodes; requiring joint parent-evaluation submersivity; contracting the stable one-input constant root; adding the unstable zero-input constant root without an ambient-submersive chart; using ordinary smoothness of auxiliary forgetting; obtaining relative CF extension directly from Prop 14.5 without a collar; changing an ordinary child's output under cyclic relabeling; omitting constant switching roots; ignoring the $s=0$ or $s=k$ multiplicities; equating finite-cutoff approximate solutions to an actual functor without an argument; identifying full self-Homs from one finite directed sector; assuming saturation alone splits the projection; and evaluating Novikov series numerically at complex parameters.

The script `checks/analytic_falsification/check_identities.py` independently checks finite arithmetic/combinatorial portions and writes `identity_results.json`. Result:

* 145 rooted labeled trees through five vertices;
* 2,142 reciprocal/diagonal edge-sector assignments;
* 48,794 normalization orders;
* 1,015 additive-cost checks;
* 461 orientation-normalization parity checks;
* 209 cyclic labeled-placement multiplicity checks.

All passed. These finite tests do not establish analytic gluing, Kuranishi existence, or any Hodge theorem; the general derivations above are the validation for their corresponding identities. No source was edited and no build was run inside the pinned upstream checkout.

**Strongest reviewed result:** assuming the stipulated geometric/topological setup and the source analytic/HMS inputs listed here, the manuscript supplies the relative interior-rooted integration needed to remove curvature, and its category completion transfers the degree-two bound and Euler data to a perfect complex. The previously suspected mixed-root corner/empty-word/cyclic issue is not an identified obstruction in this version. Remaining global proof obligations must be tracked separately rather than converted into an unconditional full-solution verdict.
