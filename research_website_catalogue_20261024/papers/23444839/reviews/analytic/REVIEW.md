# Independent analytic review: Zenodo 23444839

**Verdict: PASS at the exact stated hypotheses.** I found no substantive mathematical error or unresolved load-bearing proof gap in the five-page v1.0.0 manuscript, *A negative answer to Nevo's homology-sphere decomposition question*, dated 17 October 2026. This is an AI mathematical review, not external human peer review, a formal proof certificate, or a novelty/priority certification.

## Frozen inputs and independence

The operative PDF is `sources/spherefree-doubly-cm.pdf`, SHA256 `0f3bd7b0b576188794376e5a6428f7049bd19a1e778b68ad5c63b696a73c3a01` (83,093 bytes). The support ZIP is `spherefree-doubly-cm-source-and-verification.zip`, SHA256 `7919adebe0119f34df35e905ebe3665b1d66e79477fa36a06c30801bbe736a5b` (392,255 bytes). Fresh acquisition receipt SHA256 is `9734c4468dbbec154b84c2d6317e6da880209815b9dcac656b47ebba48ee7985`; public metadata SHA256 is `d2de5b40d398e0ee555c43aaf7143bea1e5c006494130e44259a2314a539ff2b`. The embedded main PDF is byte-identical. All 120 extracted files, both public assets, and every ZIP member's CRC and SHA256 were checked against the fresh receipt without modifying originals.

I read all five PDF pages through text extraction and the complete matching `main.tex`, including the proof, references, and disclosure. I reconstructed the universal argument and wrote and ran `independent_controls.py` before inspecting packaged helper code. I then read the current verification programs and executed them unmodified in a disposable private copy. No sibling mathematical findings or dedicated historical assessment bodies were read. Incidental exposure: the paper's own final disclosure reports historical AI audits and priority searches; source inventory/receipt metadata lists historical filenames and hashes; current helper code names and hashes archived audit records. The default verifier mechanically hashes those records and parses a historical PDF/source custody JSON. None of those prior opinions was adopted as mathematical evidence. Packaging self-tests copy an older finite diagnostic as opaque bytes; they do not use a historical mathematical verdict.

## Exact claim and question match

The theorem is existential: one finite pure **two-dimensional abstract simplicial complex** K is doubly Cohen–Macaulay over **every characteristic-zero field** and contains **no two-dimensional homology-sphere subcomplex over any field**. The sphere convention requires the sphere homology in every face link, including the empty face; it is not merely a condition on the total homology of the complex. The forbidden subcomplex need not be induced. There is no claim about all finite building quotients, all residue orders, all coefficient characteristics, subdivisions, immersed spheres, or larger ambient complexes.

Nevo's original OWR 17/2005 contribution, printed pp.960–961, gives Theorem7 for d-dimensional 2-CM complexes over a field, d≥1, with minimal d-cycle pieces, overlaps containing a d-face, and the stated reordering property. Problem8 asks for homology-sphere pieces. The published paper, Section3, Definition3.1, Theorem3.4 and Problem3.7 (printed pp.414–417), has the same domain and quantifiers. I read that theorem's full proof as well as its statement. Swartz's `g-elements`, Section4, explicitly gives the local-link homology-sphere/Gorenstein-star convention in this decomposition setting. Consequently an example over Q in d=2 answers the universal question negatively; showing that no permitted piece exists is stronger than failing the overlap or reordering conditions.

Neither a PL assumption nor classification of topological surfaces is imported. The local-link hypotheses themselves force the two-dimensional sphere candidate to have two triangles on every edge and a cycle at every vertex. The Euler contradiction then works over every field without an orientability argument. In contrast, the positive 2-CM assertion is restricted to characteristic zero, which is essential to the proof's scalar-extension step.

## Proof reconstruction and critical interfaces

### 1. The finite quotient really exists with the asserted links

For F=F_11((y)), the affine building of PGL_3(F) consists of homothety classes of full O-lattices with lattice-chain faces. In a vertex link, proper nonzero subspaces of F_11^3 are its points and lines, and a link edge is inclusion. Thus the link is the incidence graph G of PG(2,11), with 133 vertices on each side and degree12.

The load-bearing external import is Lubotzky–Samuels–Vishne, arXiv math/0406217v2, Sections2–4. These sections were read from the full primary PDF, not inferred from an abstract. Section3 defines the cyclic algebra over F_11(y), its center and its splitting over F, and the injective adjoint representation after quotienting central scalars. Its polynomial ring R0=F_q[1/y] does **not** support the original algebra construction in the same way as R; LSV explicitly defines G′(R0) using the adjoint embedding into GL_(d²)(R0). The submission follows this distinction correctly.

LSV Equation(9) on manuscript p.13 has entries of degree at most one in t=1/y for Ad(b_u). Definition4.7 and Proposition4.8 place the whole group, including inverses, in GL_9(F_11[t]) and prove simple transitivity on building vertices. Corollary4.6 gives a positive-generator product of length equal to the lattice index exponent. A neighbor has index11 or11², so **both undirected neighbor types** are represented by one or two positive generators. This avoids incorrectly assigning degree one to every undirected step or assuming that an inverse generator has degree one.

For an additional independent algebra check, put b=1−z^−1 with z³=1+y and φ(a)=a^11. Then b^−1=1+t(1+z+z²). Direct multiplication gives

Ad(b)(a z^k)=a z^k+(a−φ^−1(a))(Σ_(i<k)z^i+tΣ_(i<3)z^i), for k=0,1,2.

Conjugation by u is a constant block-diagonal linear map, so the same degree-one property holds for every b_u=ubu^−1. The field extension is separable and the cyclic algebra's center is the base field; the kernel of its conjugation action is central. Projectivizing therefore makes this representation faithful. No claim from LSV's later global Ramanujan spectral construction is required. In particular, the historical status comment about that later theory in LSV's introduction is outside the dependency chain here.

The reduction kernel Γ9 modulo t^9 is normal and finite index, since its matrix target over the finite ring is finite. A path of length≤4 from o to γo yields at most eight positive generators: use simple transitivity successively to translate each neighbor step to the base vertex. The resulting matrix has degree≤8. If γ∈Γ9, each entry of ρ(γ)−I is divisible by t^9, hence is zero. Faithfulness gives γ=1. Normality and vertex transitivity give the same displacement bound at every building vertex. The use of the nonreduced ring F_11[t]/(t^9) introduces no additional hypothesis: reduction of a polynomial matrix with a polynomial inverse is still invertible. The proof does not invoke Lubotzky–Meshulam's irreducible-polynomial quotient theorem with incompatible parameters.

The quotient K is the complex of orbit images of actual building faces. It is finite, connected and pure2D. No face folds, and no two neighbors of x have the same orbit: their mutual distance is≤2, contrary to the displacement bound. Every quotient triangle or edge incident to [x] has a translate lifting it incident to x. Its other lifted vertices are unique neighbors of x. These observations establish a bijection on both vertices and edges of the link, hence lk_K([x])≅G. They do not depend on completing cliques, assuming an induced quotient, or requiring the action to preserve building colors.

### 2. Every deletion has the required normalized spectral gap

The exact point–line identity MMᵀ=11I+J yields the adjacency spectrum ±12 and ±√11 and ordinary gap12−√11. This uses the constant singular direction and its orthogonal complement; bipartiteness does not create a smaller positive Laplacian gap. G is connected and has no cycle of length below six.

For H=G−w, extend an unweighted-mean-zero x by zero at w. The extended function is still mean-zero on G. The deleted incident-edge energy is Σ_(v∼w)x(v)²≤||x||². Therefore E_H(x)≥(11−√11)||x||². Positivity also proves H connected, rather than presupposing this in the variational step.

For arbitrary nonconstant f, set x=f−its unweighted mean. The degree-weighted variance is at most12||x||² because all degrees in H are11 or12; this is an **upper** bound for the denominator. It follows that

λ_norm(H)≥(11−√11)/12>7/12>1/2.

The replacement of an ordinary mean by a weighted variance is handled in the correct direction. No regularity assumption is made on the deleted link. The strict comparison uses √11<4, so no numerical eigenvalue approximation bears the proof.

### 3. Weighted cocycles give all the needed homology vanishing

For a finite pure2D complex X, let m(e)>0 count incident triangles. In a fixed real cohomology class, choose the edge cocycle a orthogonal to coboundaries for the weighted inner product Σ_e m(e)a(e)². Finite-dimensional orthogonal projection ensures existence. Variation at a vertex v gives Σ_u m(vu)a(vu)=0. Since the degree of u in lk_X(v) is precisely m(vu), the local function f_v(u)=a(vu) is **degree-weighted mean-zero**.

The triangle cocycle equation identifies f_v(u)−f_v(w) with −a(uw). Summing local edge energies counts each edge once for each triangle through it, and therefore gives E(a), not 2E(a) or3E(a). Summing local weighted norms counts the two endpoints of each edge and gives2E(a). With λ the minimum of the finitely many link gaps, the inequality is E(a)≥2λE(a). Strict λ>1/2 forces a=0. This proves the finite lemma directly; it is not a numerical test and does not require X simply connected or contractible.

For K−z, each surviving edge loses at most the unique possible triangle containing z, so its former twelve incident triangles become at least eleven. Every surviving vertex retains at least265 neighbors. It follows that the deletion is nonempty and pure of dimension2. A path through z can be replaced by a path in its connected link, so the deletion remains connected. A surviving vertex link is exactly G or G−w, according to adjacency to z. Thus the lemma applies to K and **every** single-vertex deletion, not merely one orbit representative or a sampled deletion.

Real H¹ vanishing gives real H_1 vanishing by finite-dimensional duality. The finite simplicial boundary matrices have integer entries; their ranks over Q, R and any characteristic-zero field coincide because their nonzero integer minors remain nonzero. This transfers H_1 vanishing to all such fields, without assuming every field embeds into R. All Reisner conditions are then checked: empty-face connectedness and H_1; nonempty connected vertex links; nonempty zero-dimensional edge links; and the facet-link convention {∅}. The same dimension is preserved after deletion. Therefore K is 2-CM over each characteristic-zero field.

### 4. The sphere obstruction covers every allowed piece

Let S be a two-dimensional local-link homology sphere over any field and a subcomplex of K. Its edge link is zero-dimensional and has reduced H_0 dimension1, so it has exactly two vertices; each edge lies in exactly two triangles. Every vertex link is connected and its vertices all have degree2, hence it is a simple cycle. Because it is a subgraph of G, its length is≥6. This remains true for non-induced S; missing extra ambient edges cannot create a shorter cycle.

Thus 2f1≥6f0 and3f2=2f1. They imply χ(S)=f0−f1/3≤0, while global sphere homology implies χ(S)=2 over every field. The contradiction rules out all such subcomplexes. It neither assumes that every homology sphere is presented as a standard triangulated topological sphere nor uses the classification of surfaces. Since K contains no allowed piece at all, no decomposition with the further overlap/reordering requirements can exist.

## Independent exact controls, completed before helper inspection

`independent_controls.py` is a fresh standard-library implementation. Its 22,766 explicit checks passed. The main mechanisms are distinct from merely rerunning the package:

- It independently constructs projective points/dual lines over F_11, verifies all17,689 Gram entries, and checks all266 deletions. Each deleted link has12 vertices of degree11 and253 of degree12, with1,584 edges, and is connected.
- It uses E=F_11[a]/(a³+4a+1), whose cubic irreducibility follows from checking absence of a root, and the power basis rather than relying on a saved matrix table. It builds Ad(b) as B0+tB1. The determinant has degree≤9, and its values at all11 elements of F_11 are exactly1; the polynomial root bound therefore certifies determinant≡1 and a polynomial inverse. This is an exact identity certificate, not interpolation beyond its valid degree range.
- It checks every one of the133 projective conjugators and compares3,591 columns with direct multiplication in the cyclic algebra at y=1,2,9. Those finite specialized checks corroborate the separately derived universal formula; they alone do not certify a rational-function identity. All133 generator matrices are distinct. An intentionally changed coefficient is detected. A separate I+t^9 E12 control shows why an omitted degree restriction would invalidate a congruence-to-identity inference.
- It computes exact simplicial homology over Q,F2,F3 for the tetrahedral sphere, a separately constructed9-vertex18-triangle torus, the6-vertex real projective plane, and a sphere with an attached triangle. The projective plane has Betti numbers(1,0,0) over Q and(1,1,1) over F2, demonstrating why the characteristic-zero transfer must not be extended casually. The attached-triangle example has sphere homology globally but fails the local edge condition, demonstrating the distinction in the question's sphere convention.
- The9-vertex torus has C6 links and H_1 dimension2. A nonexact weighted-harmonic cocycle has E=36, summed local energy36 and summed local norm72. It realizes equality at gap1/2 and detects both a missing factor2 and replacing strictness by a nonstrict inequality. This control differs from the package's7-vertex torus/coboundary calculation.

These checks are corroboration for the proof and exact primary imports. They do **not** enumerate the enormous finite quotient Γ/Γ9, exhaust arbitrary group words, or prove 2-CM by checking the homology matrix of K. Those universal conclusions rest on the argument above.

## Unmodified replays and source custody

After independent reconstruction I read all current mathematical verification code, its common authentication module, the packaging self-test and builder. The code was copied byte-for-byte into a private replay folder; originals were never executed in a mode that writes beside them. `replay-receipts.json` records commands, times, exit codes and stdout/stderr hashes.

The default verifier passed in normal and optimized Python with identical full output. Each run includes two exact positive calculations and six expected failures from actual corrupted incidence, triangle or edge-weight constructions. The packaging self-test passed all40 checks in normal and optimized modes with identical output. It verifies path/input custody and mutation detection, not additional mathematical theorems. Optional matrix diagnostics passed under the available NumPy runtime, including both polynomial inverse identities,266 distinct positive/inverse generators, and the local incidence matrix. Its floating eigenvalues are diagnostic only. Optimized Python correctly rejected that optional program because it uses substantive assertions. The final original-asset/member rehash and CRC check passed.

## Primary attribution, remaining limits, and disposition

`primary-source-checks.json` binds seven primary PDFs/texts with exact reading ranges and explains each dependency. LSV Sections2–4 supply the central construction. Nevo and Swartz establish the exact target/convention. Lubotzky–Meshulam Section3 supplies antecedent method and clarifies the different irreducible-polynomial hypotheses. Ballmann–Świątkowski Theorem1 and Section2 give the classical normalized-gap vanishing framework, but the submission supplies the particular finite proof. Januszkiewicz–Świątkowski Example1.8(5), pp.11–12, records the classical sphere-curvature obstruction; their more general systolic theorems are not imported.

No unresolved central mathematical gap remains in this review. The standard building and central-simple-algebra results used within LSV were checked at their stated primary interfaces rather than recursively re-proving all background theory. I did not certify the completeness of the manuscript's historical priority search, examine the packaged old priority assessments, or resolve its acknowledged literature access gaps. I did not independently certify the contextual nonpriority statement about every later paper cited. None is a premise of this theorem. There is no formal proof-assistant verification and no new human referee input.

The strongest supported disposition is **PASS for the exact existential finite abstract2D theorem and its negative answer to Nevo's published question under the standard local-link sphere convention**. Preserve the characteristic-zero restriction for 2-CM, the all-fields quantifier only for sphere exclusion, the lack of quotient enumeration, classical attribution and unrefereed/AI status. No repair was made or proposed, and no publication action was performed.
