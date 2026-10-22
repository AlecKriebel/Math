# PR1348 /10000037: second new independent whole-package adversarial review

**Scientific verdict: PASS for the exact unchanged publication_preparation_01 package and its explicitly declared scope. No remaining substantive mathematical,computational,bibliographic,reproducibility or presentation repair is required by this review.** This is an independent AI review,not independent human peer review,formal certification,root adoption or authorization of a live action. The original source's missing probability quantifier and bounded priority/access coverage are retained limitations,not resolved by this verdict.

Assigned review completion100%; overall sweep estimate80%. All new work is confined to publication_whole_review02. Earlier whole review01's PASS was disclosed in the assignment but was not used as an independent derivation. I reconstructed the proof and source interpretation,authored different finite attacks,read the full final paper and all 18 scientific members,and replayed the supplied package separately. No manuscript edits were made.

## Exact reviewed object

- Preparation MANIFEST.json SHA256 **542496a557c992dd2c14418f2cb1bf8695955bf5022cefe6d445f3586d382ce3**; all 115 listed members and the manifest itself checked,3,065,270 total bytes. Exact closure,not merely selected hashes,was verified. The supplied verify_closed_seal.py also passes read-only.
- Main TeX SHA256 **6b5a8b008f43d2cdd22641889b67d63b6c635e2997378ccca66246b7902666af**. The source copy and note/main.tex are byte-identical.
- Five-page PDF SHA256 **4a83d0519b0d3987f8f79daed7d030793bfaeb94c88c0bcfa339c936d81ebcde**,67,272 bytes.
-18-member scientific source/verification ZIP SHA256 **4fccb467a29f4676d8fcecf933404eab0586a853a351179b9cc2b19b11284589**.
-5-member upload kit SHA256 **e2306f26c017354bd5d6137d07f4f1d86ff368b976644068cdba3899fee6a52b**.

Read all of main.tex,README,related-work note,SOURCE_PROVENANCE,CODE_PROVENANCE,both licenses,both build/visual receipts,PUBLIC_MANIFEST,reproduce.py,build_package.py,exact_checks.py,EXPECTED,UPLOAD_README,metadata and deposit proposal. Every metadata field equals the matching deposit's metadata. Read the entire preserved14,070-byte construction proof and10,629-byte source adjudication as historical inputs,not mathematical authorities or executable code. No claimant/prior-review mathematical program was imported or executed; the published supplementary checker was replayed with attribution after independent reasoning.

## Original problem and exact success criterion

The original is Benjamini's30October2013 author manuscript,Problem9.6,page64. I independently rehashed the entire1,101,523-byte,115-page primary PDF (aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe),read actual selected pages1,5,9,32–33,63–65,and visually inspected new renders of9/63/64. Full-book reading is not claimed. Page9 explicitly permits multiplicative plus additive rough-isometry distortion and a strict C-net. Pages32–33 define ordinary common-p independent bond percolation and rooted pc on connected graphs. Page63 discusses p>pc. Nearby theorems impose transitivity explicitly; that does not become an implicit hypothesis of the separate question. The Problem9.6 sentence omits p.

The manuscript declares its target before refuting it: every admissible graph,each fixed pc(G)<p<=1,almost-sure uniqueness. A dimension-two example with positive-probability at least two infinite clusters at one strictly supercritical parameter is the full logical negation needed. The paper does not infer the source author's unique intent or a simultaneous-in-p statement. A near-one assertion is weaker and is not refuted; critical multiplicity,almost-sure multiplicity,exact cluster count and dimension-one multiplicity are not claimed. These qualifications appear in the abstract,first section,related-work discussion,README,upload README and full metadata. They must survive root's later public framing. An unqualified statement that every possible interpretation of the historical question has been settled would not be supported.

The live author-PDF access timed out in this review. The exact cached primary copy supplies actual source evidence. Current Springer chapter metadata has2013-10-14 and pages69–84; the subscription chapter body was not read or equated bytewise with the later manuscript. These are disclosed access/version limits.

## Independent reconstruction and deliberate proof attacks

### Graph admissibility and all-vertex metric quantifiers

Take the ordinary nearest-neighbor square lattice. Keep bonds internal to A={x,y>=1} or B={x,y<=-1}; replace every other edge by a private100-edge chain. Each original has four incidences,each new vertex two,and no loops or parallel edges arise. Countability,connectedness and simplicity follow directly. The definition is global and deterministic; no randomly chosen environment or location-dependent length enters.

For any actual vertex x choose its nearest original endpoint f(x),fixing originals. Every actual edge maps either to a point or a lattice edge,including the single switch across a chain midpoint. Hence d_lattice(fx,fy)<=d_G(x,y) for arbitrary x,y,not only originals. Also d_G(x,fx)<=50. Lift any lattice geodesic from fx to fy; its cost is at most100 times its length. Thus

`d_lattice(fx,fy) <= d_G(x,y) <= 100*d_lattice(fx,fy)+100`.

The source lower bound with C=100 follows from the stronger left inequality; f is onto,so the strict100-net is immediate. Both midpoint tie choices work. These arguments quantify over every vertex and all positions; they do not extrapolate from a patch. I attacked far endpoint choices,midpoint ties,remote coordinates and the hidden substitution of unbounded chain lengths. The stated nearest-endpoint map and fixed length resist those attacks. C100 would fail for arbitrarily long chains,but the paper never uses those.

### Exact model and infinite component correspondence

Coarse strong edges use one actual bond; weak edges use disjoint sets of100 actual bonds. Their states are independent with marginals p and p^100. Shared endpoint vertices do not create dependence in bond variables. This is a derivation from one homogeneous iid model on G,not a different requested percolation law.

An actual simple path between originals cannot leave a replacement chain internally: every internal vertex has degree2 and no external attachment. Therefore it traverses the entire chain. Compressing paths gives exactly coarse connectivity of originals; conversely,expand coarse-open edges. An actual component without an original lies inside one finite chain. If it has k finite originals,it is contained in those vertices and their finitely many incident finite chains,so cannot be infinite. Thus an infinite actual component has infinitely many originals and induces exactly one infinite coarse component; distinct coarse components cannot join through partial chain stubs. Conversely each infinite coarse component lifts into one infinite actual component. This is a component-label bijection,not an assertion that partial-chain stubs vanish. The paper explicitly retains them. Finite exact partition attacks confirm the local mechanism but do not replace this universal argument.

### Quadrant dual parity without an exterior-tour assumption

For any finite D in N0² containing the corner,form the finite dual graph crossing the Q-edge boundary. Every interior dual vertex has even degree by cyclic membership transitions around its square,including degree4 at diagonal contacts. Boundary endpoints on the bottom/left have degree at most1. Along the infinite primal bottom ray,membership starts1 and eventually0; there are an odd number of bottom endpoints. Some dual component has an odd number of them. Handshaking forces an odd number of left endpoints in that same component,since there are no other odd-degree vertices. A simple path within the component joins a bottom to a left endpoint. Boundary degree1 prevents internal boundary visits. Endpoints (i+1/2,-1/2),(-1/2,j+1/2) require m>=i+j+2>=2 unit dual edges.

This derivation covers holes,disconnected D and degree4 vertices; neither a canonical outer face nor a simple boundary tour is needed. Applying it to a finite open corner cluster makes every crossed primal bond closed. Each simple eligible dual path crosses distinct existing Q-bonds. At length m there are at most m bottom starts,then at most4*3^(m-1) paths per start. Counting ineligible paths increases the combinatorial bound only; no closed-bond probability is assigned outside Q. For z=3(1-t)<1,the finite-cluster probability is at most

`(4/3) * sum_(m>=2) m*z^m = (4/3)*z²*(2-z)/(1-z)²`.

At t=.9 this equals102/245,so corner survival is at least143/245. I tried parity counterexamples using thin strips,triangular domains,detached annuli,holes and far satellites. None breaks the universal parity argument. The removed-corner and zero-start variants do fail,as expected; the actual paper keeps the necessary hypotheses.

### Every root survives; no uniformity or uniqueness monotonicity shortcut

For an arbitrary actual root o,choose a finite deterministic path F to the strong corner v. Conditional on its bonds being open,the increasing event {v survives} has probability at least its unconditioned probability: couple the other bonds identically. Hence

`P(o survives) >= p^|F| P(v survives) > 0`.

F may overlap bonds determining v's survival; independence between those two events is not assumed. Conditioning monotonicity resolves that overlap. This establishes the same critical threshold at every actual root,including chain interiors,without a location-uniform survival bound. Consequently pc(G)<=.9. Coupling all bonds with independent uniforms makes quadrant survival increasing at the larger p=.95. It says nothing about monotonicity of uniqueness,which is not used. A finite forcing proxy independently checks the conditioning inclusion and positive margin; it is not a finite proof of infinite survival.

### Every weak bridge,all starts,and all lengths

Any finite coarse connection from A to B can be stopped at its first B vertex and begun at its last earlier A vertex. Internal vertices then lie outside both sets,so each retained edge is weak. Loop erasure keeps this property. Using the first A would be wrong: a real walk can use strong edges,leave A and return before its final exit. I constructed that failure explicitly. The paper uses the correct last-A/first-B rule.

A weak path starts on A's inner boundary,(1,n) or (n,1),n>=1. Its L1 distance to B is n+3. A specified self-avoiding weak path with m edges uses m distinct independent weak coarse bonds and has probability q^m,where q=(19/20)^100. Counting at most4*3^(m-1) paths per start and double-counting the corner gives

`P(W) <= (8/3) * sum_(n>=1) sum_(m>=n+3) r^m = (8/3)*r^4/(1-r)²`, r=3q.

I independently sum by length: for m>=4 there are exactly m-3 eligible n values in the overcount,so the same series is (8/3)sum_(m>=4)(m-3)r^m. This confirms both the fourth power and the second denominator. Nonnegative terms justify exchanging summations. Every start and length is included; no finite barrier or asymptotic “at infinity” connection is assumed. I tested actual walks with excursions and starts through n=10,000,and exact positive tails after multiple cutoffs. These disprove finite-window coverage as a proof method.

Bernoulli's inequality gives(20/19)^20>=1+20/19>2,so q<1/32 and r<3/32. The positive series is strictly increasing,therefore P(W)<27/107648. The cap is deliberately loose but enough. A geometric estimate that merely assumed q small without proving it would be incomplete; the paper proves this bound exactly.

### Infinite sigma-fields and the strict conclusion

S_A depends on internal-A bonds,S_B on internal-B bonds,and W on weak-chain bonds. These three countable bond families are disjoint. Cylinder independence extends to their generated sigma-fields by a monotone-class argument. Quadrant survival is a countable intersection of finite-distance connection events on a locally finite graph; W is a countable union of finite path events. Thus the required infinite events are measurable and independent. Shared vertices do not invalidate this bond independence. No independence of arbitrary overlapping cluster events is asserted.

On S_A intersect S_B intersect W-complement,two infinite strong components survive and cannot belong to one actual component,since a graph connection between their vertices always means a finite path,and such a path would force W. Hence

`P_.95(N_infinity>=2) > (143/245)²*(107621/107648) = 2200741829/6461571200 > 1/3`.

The difference from1/3 is140654287/19384713600>0. Strictness comes from the strictly bounded bridge probability; survival lower bounds may be non-strict. At .95 the parameter is strictly above pc<=.9. Positive-probability nonuniqueness is exactly enough to contradict almost-sure uniqueness. No ergodic0/1/infinity law,exact cluster count,transitivity,quasi-transitivity,WSF transfer or uniqueness-monotonicity theorem is needed.

## Independent finite attacks and supplied replay

independent_controls.py was newly written here without reading/importing another review's code. Its face-based dual enumeration uses triangular and2-by8 strip supports,plus16 detached annuli:49,168 sets,45,863 disconnected,1,632 with holes,29,455 degree4 cases. The longest selected witness is17. This differs from the publication checker's3-by4 primal-neighbor enumeration. A square-plus-diagonal gadget with two subdivided edges has128 actual bond worlds,32 coarse states,512 exact original-component partition comparisons,64 interior-only component occurrences and an exact forcing margin9020160/1977326743. All joint coarse probabilities equal the independent product law at p=3/7. Eight excursion walks validate extraction through coordinate10,000. Four remote chains with both midpoint ties give81,608 exact same-chain pair controls; the proof above,not these pairs,supplies the cross-chain global quantifier. Five exact diagonal-series tail identities are checked. Nine false constraints are rejected with explicit finite witnesses or rational calculations. No numerical Monte Carlo evidence is promoted to proof.

Own normal/-O/-OO outputs agree exactly (dc012e7d612a4444a194e6e88e5d716cce374775b634662706076b4806f4da4d). The first normal run also passed,but its weak conceptual negative controls were sharpened into actual finite witnesses; that initial output is preserved honestly. No publication-package repair followed from this review.

Read the entire supplied checker before executing it. In a new safe extraction,reproduce.py passes all prescribed normal/-O/-OO modes against exact EXPECTED. Both ZIPs have unique safe relative regular member paths,no traversal or symlink,valid CRC and exact source bytes:18 scientific,5 kit members. The extracted builder recreates all 6 release files byte-identically. Six isolated corruptions (expected output,TeX,PDF,metadata,checker bytes and an extra nested member) are rejected,and restored extraction passes. Receipts retain rejection diagnostics; no rejection was waived. ARCHIVE_REPLAY.json binds outputs and every archive/rebuilt-release member. Source/kit content contains no credentials,raw spreadsheet,third-party source bodies,old acceptance corpus or provider/operations driver. The kit names exactly PDF plus scientific ZIP for upload.

The cached Tectonic0.17.0 binary independently hashes to b52b5a730e2b0b33087304f7720f649603953f270a6b1c88bb031e1ae01f7f9c. A new compilation runs with --only-cached,--untrusted,--keep-logs,network denied and all writes denied outside this assigned recompile folder and/dev/null. No installation or download occurs. It succeeds; its entire extracted text equals the frozen PDF's. PDF bytes differ,which is permitted and explicitly not claimed reproducible by TeX recompilation. Frozen-PDF archive reproducibility is a separate claim and passed exactly. All 5frozen PDF pages were newly rendered and individually visually read; no clipping,overlap,missing glyph or unreadable equation was found. The actual original source definition/context/question renders were also individually read. VISUAL_QA and RECOMPILE record hashes/commands and actual limits.

## Priority,coverage,attribution and presentation

PRIORITY_LOG.md records20fresh queries,actual primary comparison statements and precise read limits. I read the relevant original source and primary models/theorems for the hyperbolic-sector example,near-one uniqueness,the critical product example,Teixeira,Candellero–Teixeira,Hutchcroft–Tointon,and the2026 annealed stretched-lattice paper. I additionally checked the sprinkling model. None of the inspected statements is an authenticated earlier exact Euclidean-coarse all-supercritical counterexample or a theorem invalidating this one. Standard series reduction and planar/counting mechanisms are correctly credited. The claims do not pretend to be a new general probabilistic mechanism. Full proofs of comparison papers,uninspected editions,unindexed/folklore/unpublished work and current worldwide status remain outside coverage. The manuscript accurately preserves those limits and claims no exclusive firstness. Its self-contained proof imports no comparison theorem.

Fresh coverage checks preceded mathematical work. At15:37UTC,the full43-column numeric GWS tab had208populated rows; raw typed value/formula views matched and full metadata stayed stable. All semantic leads were actually read and distinguished,then authenticated against native Zenodo record metadata. The three are dependent internal-threshold percolation,oriented flow,and designed-tree traffic. The numeric public hit is curriculum research.244 local state files yielded no matching state. No solution DOI,existing partially completed candidate upload or duplicate publication was authenticated. No owned-account private-deposit inventory is claimed. These are point-in-time observations; root must repeat live sheet/DOI/local/owned-account checks immediately before any publication and row write.

Title,Alec Kriebel identity,ORCID0009-0001-9320-500X,date2026-10-22,version1.0.0 and preprint type agree across PDF/source/metadata/deposit. All-phase extensive AI use includes exploration,proof development/reconstruction,computation,literature,writing and adversarial checking. Unrefereed status and absence of conventional independent human peer review,journal acceptance and formal proof-assistant certification are explicit. AI review is not mislabeled human review. CC BY4.0 prose and MIT code agree with the supplied licenses; citations do not relicense third-party bodies. Source/question/dependency DOIs are only references,not this paper's solution DOI. No reserved DOI is inserted. These observations support scientific packaging,not a provider action.

## Preservation,failures and remaining action gates

INPUT_BASELINE records exact files/dirs,bytes/hashes,modes and nanosecond mtimes for the preparation,first whole review and earlier source/math review. Final preservation is rechecked by the closing verifier. Original primary PDF and compiler identity are separately recorded and rechecked from the point they were introduced. No Git/index/ref,STATE,QUEUE,CASE,shared branch,draft,spreadsheet,Zenodo or other service mutation occurred. Communications were limited to this reviewer and its parent. No external individual or unrelated agent was contacted. All owned writes,extractions,logs,renders,receipts and seal stay here. Own allocation remains below 8MiB and actual free space above the 150MiB reserve; observed closing guard values are in RESOURCE.json.

A local report-edit patch also failed an exact context match, made no partial edit, and was corrected against the observed text. One read-only shell glob lookup initially failed because it addressed a nonexistent private receipt pattern; a direct observed receipt path fixed the lookup. This was not a mathematical failure. The first own control output remains retained after strengthening its witness quality. No failed mathematical test or package rejection was hidden or converted to a pass. No substantive issue remains unresolved within the declared scientific scope.

This PASS applies only to the exact package hashes above. Root adoption and all live publication/merge/deduplication gates remain separate. In particular,do not convert the missing-p interpretation into a claimed resolution of a near-one statement or into recovered author intent; do not convert bounded priority searches into exclusive novelty. If root changes the scientific package,the changed bytes need appropriate fresh review. This review performs no publication or operational approval.
