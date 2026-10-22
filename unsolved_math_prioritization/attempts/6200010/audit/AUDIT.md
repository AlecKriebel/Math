# Independent adversarial audit: Coxeter boundaries, problem 6200010

## Verdict

**PASS for the stated partial results; the original existence problem remains unresolved after 5/5 author approaches.** There is no accepted general construction, no general nonexistence theorem, and no novelty claim. The review found no blocking mathematical error.

One reproducible packaging weakness in the frozen author verifier is corrected by the separate audit verifier: the original inventory scan overlooks unexpected nested files named `MANIFEST.json`. This does not affect any file actually present in the reviewed freeze or any mathematical conclusion. Use `verify_audit.py` for the reviewed package. The author files are preserved unchanged in `author/`.

This is an independent AI-assisted mathematical audit, not external human peer review, formal proof-assistant certification, or a complete survey establishing worldwide open status. The audit reconstructs the arguments and source hypotheses and adds independently implemented finite controls.

## 1. Exact reviewed object and source identity

The immutable author ZIP has 20,470 bytes and SHA-256

`a2fc0e27b9bd81dca28450f20cdbbda139b2e50933126bd6b9db577662cc0dcf`.

Its ten members match the submitted public directory byte-for-byte. Its 1,453-byte manifest has SHA-256

`b8f24c4403ad0c93be653da10572689ecb683741e4e387b97996ebb05a717609`.

All three complete input corpora were independently read and hashed. The unique catalogue and problem records identify rank 807, ID 6200010, code AMR-061-0010. The full problem record together with its actual report, serialized by the specified canonical review procedure, reproduces review hash

`a7ba968e284b4b4b467dcb2029da7bc249bc87135f05c936fadf91551909160d`.

The statement hash also matches. The imported report is an OPEN-TRIAGE literature/desk assessment with no direct verification; it supplies no mathematical proof attempt. `IDENTITY_RECHECK.json` contains only hashes, byte counts, and match metadata, not corpus records or contents.

A fresh download of [Kapovich's problem list](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf) matches the author's PDF hash. The auditor independently rendered and visually inspected printed page 4. Section 3 makes the finitely generated Coxeter system and its CAT(0) Davis visual boundary the setting. It does not impose Gromov hyperbolicity. The 2005 workshop date and the PDF's October 24, 2007 date have different meanings and are correctly distinguished.

Problem 10 is the rational-dimension-one boundary question. The preceding examples already cover dimension two. The introduction of [Dranishnikov's 1997 paper](https://doi.org/10.1090/S0002-9939-97-04106-3), inspected through its author-uploaded full text, explicitly identifies the unresolved range beginning at three. Consequently the author has not quietly answered an easier dimension-one or dimension-two question. The live UnsolvedMath page remained inaccessible to the auditor's web request, so its current rendered content and status are not certified.

## 2. Imported dimension formulas and induced-subcomplex maxima

Write D_R(L) for the highest reduced cohomology degree of any full vertex-complement of a simplex of L, including the empty simplex. The geometric deletion convention is correct: a point outside the closed simplex has positive total barycentric coordinate on vertices outside it. Normalizing those coordinates gives a deformation onto the relevant full subcomplex while staying in the same carrier simplex. Removing an open simplex instead would be a different operation.

The Coxeter compact-support computation and virtual-dimension formula in [Davis, second edition, Section 8.5](https://people.math.osu.edu/davis.12/second_edition.pdf) give vcd_R(W)=D_R(L)+1 in the coefficients used here. The rational coefficient passage is valid for the finite-type torsion-free finite-index subgroup and is also illustrated by Davis's Example 8.5.8. Dranishnikov's 1997 Theorem 5 states the coefficient-sensitive boundary shift in the Coxeter CAT(0) setting. Its ensuing definition uses relative Cech cohomology; finite-dimensional integral cohomological dimension agrees with covering dimension. The audit imports these published theorems, rather than claiming to recertify all their original proofs.

The author's Proposition 1 is valid. A full subcomplex L|U is the nerve of the special subgroup W_U. If Gamma is torsion-free of finite index in W, then Gamma intersect W_U has finite index in W_U. Restriction of projectives is legitimate because the ambient group ring is free over the subgroup ring. Thus virtual cohomological dimension cannot increase. A nonzero degree-j class of L|U, viewed as its empty puncture, supplies the reverse inequality required for equality of the two maxima.

There is independent published support stronger than needed here: [Constantinescu-Kahle-Varbaro, Theorem 5.2, equation (8)](https://arxiv.org/abs/1705.01802), establishes the maximal-degree identity combinatorially for arbitrary finite simplicial complexes. The audit checked the surrounding argument, not merely an abstract. The positive-degree use avoids reduced-degree edge cases; the usual degree-minus-one convention handles simplices/finite groups.

The integral-to-field maximum also has the correct direction. Each finite cochain complex has finitely generated integral cohomology. Its top nonzero degree is detected over Q or some F_p by universal coefficients, and no field contributes above the highest integral degree. Together with Hochster's formula this justifies rational regularity 2 and maximal field regularity n+1 as the coefficient-specific search target. High regularity alone does not suffice.

The earlier [6200004 draft PR](https://github.com/AlecKriebel/Math/pull/390), verified at commit `e0c20cc0546247ef8c7a4f97345cc8e65e3941e5`, contains an overbroad sentence saying arbitrary vertex deletion changes the invariant. It changes individual puncture data, but not the maximum. The present correction is necessary and correct; the earlier concrete deleted-simplex computations and closed-manifold exclusions remain valid. A four-cycle is a small distinguishing example: deleting opposite vertices leaves two points, a degree-zero reduced class that no simplex deletion produces, while both maxima still equal one. The independent checker verifies this example.

## 3. Surface-link theorem: full proof audit

Let L be a finite three-dimensional simplicial complex whose every vertex link is a closed connected triangulated surface. The rational obstruction is actually a statement about the puncture invariant for such complexes before a Coxeter realization is imposed.

### Orientable link

For a vertex v, the pair (L,L-v) has the relative cohomology of (cone(lk v),lk v). This is a simplicial pair computation; the link need not be full in L. An orientable closed connected surface link contributes a nonzero relative degree-three class. In the exact sequence

H^2(L-v;Q) -> H^3(L,L-v;Q) -> H^3(L;Q),

both outer groups cannot vanish. The first is a permitted vertex puncture and the second is the empty puncture. Thus D_Q(L)>=2. This argument includes the case where global rational H^2 and H^3 both vanish.

### All links nonorientable

Each triangle has exactly two tetrahedral cofaces: its link incidence at any one of its vertices is an edge incident to two triangles in a closed surface. Hence f_2=2f_3. Double counting link vertices, edges and faces gives

sum_v chi(lk v)=2f_1-3f_2+4f_3,

and therefore chi(L)=f_0-(1/2)sum_v chi(lk v). Connected closed nonorientable surfaces have Euler characteristic at most one. Writing V=f_0, we obtain chi(L)>=V/2.

The top rational homology vanishing requires a separate argument and is not inferred from Euler characteristic alone. Given a rational simplicial three-cycle, restrict its signed incident tetrahedral coefficients to the opposite triangles in any vertex link. The cycle equations at triangles containing that vertex give a two-cycle in the link. A closed nonorientable surface has no nonzero rational two-cycle, since it has no three-simplices and H_2 over Q vanishes. Thus every incident tetrahedral coefficient is zero. Doing this at all vertices annihilates the original cycle, so H_3(L;Q)=0.

For a connected component the Euler identity now gives b_2=chi(L)-1+b_1>=V/2-1+b_1>0. Each component still has dimension three under the link hypothesis, and V>=4 suffices for strict positivity. In a disconnected complex, positive-degree cohomology splits componentwise; deleting a simplex in one component leaves all the others. Thus the connected reduction loses no obstruction. This proves the claimed D_Q>=2, and the boundary consequence follows with the correct dimension shift.

When all links are RP^2, equality chi(L)=V/2 gives the stated formula b_2=V/2-1+b_1 and forces V even. It rules out the extra rational-H^2 vanishing desired in the all-RP^2-link proposal in Dranishnikov's Section 4. It is not a theorem about all singular complexes, disconnected links, or arbitrary boundary realizations.

## 4. Links, PL singularities and flagification

For a simplex sigma in lk_L(v), put X=L-sigma. Then lk_X(v)=lk_L(v)-sigma, and X-v=L-(sigma union {v}). The same relative-pair computation and exact sequence imply that a positive-degree puncture class of lk_L(v) creates a class of that degree or the next in an allowed puncture of L. Both removed sets are actual simplices. This proves D_Q(L)>=D_Q(lk_L(v)) in the degrees used. Iteration gives the face-link version. No assertion that non-right-angled links are induced is necessary.

The higher-dimensional extension is accepted with its stated PL hypothesis understood in the compatible, combinatorial sense: the supplied vertex-link triangulations are PL triangulations of closed PL manifolds. Then the link of an edge of a d-dimensional L is a PL (d-2)-sphere, because it is a vertex link inside one of those (d-1)-manifolds. Thus D_Q(L)>=d-2. In dimensions at least four this excludes rational boundary dimension one. Merely knowing that the underlying vertex-link spaces are topological manifolds would not justify this PL link conclusion in arbitrary dimensions; the report does not make that relaxation.

The barycentric argument is also correct. For a d-simplex tau of K, the vertices of sd K corresponding to the proper nonempty faces of tau induce exactly sd(boundary tau). This is a (d-1)-sphere, regardless of other simplices of K. Since sd K is flag, Proposition 1 applies to its right-angled Coxeter group. For d>=3 the rational dimension is at least two. If D_Q=1, then d<=2, and the Davis complex bounds integral boundary dimension by two. This excludes ordinary barycentric flagification and its iterates; it does not exclude arbitrary flag triangulations of the same underlying space or assume invariance of virtual dimension under subdivision.

## 5. Cone attachments and the imported iteration

If an old complex remains induced in a new Coxeter nerve, every old induced witness remains available. The dimension maximum therefore cannot decrease. In group language take the special subgroup determined by the old vertices; if old edge labels have been changed, its nerve still yields the same dimension invariant, so no unjustified embedding of a differently labelled original group is required.

For a single cone attachment on new apex v, deleting v recovers L exactly. Thus killing a global rational class does not kill the associated puncture obstruction. For several attachments, induced inclusion gives the same conclusion. Surgeries or modifications introducing old-only simplices fall outside the hypothesis and must be investigated anew. The author has not claimed otherwise.

CKV's Lemma 6.6 and Remark 6.7 explicitly give the rational virtual-dimension increment for their k-large flag construction and appropriately displaced torsion-free quotient. The field is characteristic zero; the source cautions against inferring the analogous integral conclusion from that lemma. In the nondegenerate starting setting used by the packet, iteration from q_0=2 gives q_t=2+t, hence rational boundary dimension 1+t. Every positive iteration leaves the target. The audit does not apply this recurrence to a finite/simplex degenerate seed or to a different quotient construction.

The July 2026 [Cashen-Dani-Schreve-Stark publication](https://academic.oup.com/imrn/article/2026/14/rnag144/8729161) concerns conformal dimension and fibering and does not supply the missing fixed-rational-dimension condition. The [August 2026 Ma-Yoon-Zheng manuscript](https://arxiv.org/abs/2608.18163) has Pontryagin-surface boundaries and ambient hyperbolic dimension five; its ambient dimension is not boundary covering dimension five. Current source status and these limited uses were independently checked. No conclusion about the full proofs of those constructions is needed here.

## 6. Independent computations and their limits

The frozen author checker reproduces 32,400 checks in normal and optimized Python. Its main rational-rank certificate is valid: rank over F_101 is a lower bound for rank over Q; the augmentation, chain identities and domain size give matching rational upper bounds in the order claimed. The author does not infer rational ranks from an arbitrary modular match.

The separate `independent_checks.py` imports no author code and uses independently written sparse-column elimination, ternary-coordinate cubical cells and signed boundaries. Its 5,055 checks include:

- Exact Fraction elimination over Q gives cubical boundary ranks (63,129,80) and Betti vector (1,0,31,0), independently of the author's modular certificate.
- The same model over F_2 gives ranks (63,129,79), Betti vector (1,0,32,1); F_3 and F_103 give the rational vector.
- The independent simplicial triangulation has f-vector (64,512,960,480). Every triangle has two tetrahedral cofaces. All 64 vertex links pass purity, connectedness, edge-incidence, circular vertex-link and Euler-characteristic tests, plus exact rational and mod-two homology.
- Simplicial boundary ranks are (63,449,480) over F_103 and (63,449,479) over F_2. Both cubical and simplicial integer boundary compositions vanish.
- Every simplicial complex with exactly vertex set {0,...,n-1}, for 0<=n<=4, is enumerated: 1,1,2,9,114 complexes respectively. For Q, F_2 and F_3, the maxima over all induced subcomplexes agree with the simplex-deletion maxima, and all vertex-link inequalities pass.
- Exact rational suspension, barycentric-boundary and cone controls check the cases where global cohomology alone would miss the obstruction.

There are 127 small complexes and 381 coefficient cases, not 381 different complexes. The test count is the count of explicit checks; it is not coverage of infinite families, a confidence level, or an existence proof. The general accepted claims rest on the arguments and imported theorems above.

## 7. Integrity hardening and final disposition

In the author's verifier, the inventory scan excludes every file whose basename is MANIFEST.json rather than excluding only its designated root manifest. The auditor added an otherwise unlisted `unexpected/MANIFEST.json` to a disposable copy: both normal and -O author verification returned PASS. The actual frozen archive contains no such member, so no false content is being accepted. The supplied `verify_audit.py` uses exact relative paths and explicitly inventories the unchanged author manifest as an ordinary nested file. It rejects this counterexample as well as changed, missing or unexpected files, duplicate entries, traversal/noncanonical paths, symlinks, and wrong problem identity. All failures use exceptions, not optimizable assertions.

The audit ZIP includes authored proofs, code, results, public source metadata and the unchanged safe author packet only. It excludes PDFs, source text extracts, raw catalogue/problem/report records, private coordination material and private working data. The external audit receipt binds the complete ZIP and root manifest hashes. Internal hash checks are tamper detection relative to those trusted bindings, not a digital signature or resistance to an adversary replacing every trusted artifact.

The five approaches are genuine bounded partial work, distinguished from the earlier 6200004 hyperbolic ratio investigation. The correction to that earlier maximum warning is substantive; the broad singular-link, characteristic-sensitive regularity and boundary-realization gaps remain. Accept only the scoped partials and finite controls. Keep the original problem unresolved, with five author approaches used. No remote mutation, publication, merge, release or outreach was performed in this audit.
