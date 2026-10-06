# Independent geometric and h-principle audit of original PR 32

**Family verdict: PASS for the geometric reduction, existence theorem, and compatible formal-space model in original CANDIDATE §§3–5.** No mandatory mathematical correction was identified in this family. The integral component-counting calculation in §§6–8 needs its separate topology audit; this report does not turn its legacy PASS, symbolic checks, or this family PASS into a full-target solved disposition. Historical novelty, publication, and the neighboring real-form orbit question are outside this audit.

Audit completed against original head `a92af24e2e6015893787e0c55cd4618f7098917e`, actual research base `01358d66fc67d1c462bddf31c0d4ee5b120e6737`. PR metadata instead names `c6975ca76f9f667f1250ba403d0e6da2aafe14d0` as its comparison base. The candidate SHA-256 is `501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050`. The original 15 numeric-folder files and all 16 diff blocks were read and checked against the frozen manifest; every numeric-file addition in the diff equals its snapshot byte content. Both original programs were read in full before unchanged isolated reproduction. The original ledger records one substantive attempt out of five; this audit adds no full-target proof-search attempt.

## 1. Independent target seal and conventions

The first source operation freshly retrieved the complete [university TeX of the Morgan–Pansu list](https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex). The web tool could not read that URL, but direct download from the university succeeded. Its SHA-256 is `33d853a6de512584aeedfaf5b491bcc7f0cf02d2964e8b1f1be67a5b3b97c48e`. The second question under “Manifolds modelled on flag manifolds” is question-environment ordinal 7. It asks for the homotopy classification of totally real immersions of real three-manifolds into the complex full flag manifold and immediately invokes Gromov's h-principle. The first question about orbits of real forms is separate.

Only this fresh source, the applicable AGENTS instructions, and the frozen CANDIDATE were read before `EARLY_SEAL.json` at `2026-10-02T01:12:16.919584+00:00`. No old review, author code/results, readiness, source audit, root audit, or sibling family was read before this seal. The seal and its hash receipt are preserved.

The exact tested theorem uses a fixed connected smooth second-countable **boundaryless** real 3-manifold M, the **ordered integrable complex** flag F = SL(3,C)/B_upper, and homotopies **through totally real immersions**. Neither maps nor homotopies need be proper. Orientability and compactness are not assumed. The source's bare word “homotopy” is not by itself a proof of a unique convention; this report adopts the candidate's explicit regular-homotopy convention. Ordinary underlying-map homotopy identifies more objects: on S3 the extra formal-derivative integer is invisible to it. Embeddings, images modulo source diffeomorphisms, and real-form uniformization therefore cannot be substituted into the target.

The candidate hypothesis is the following. With A = H^1(M;Z), B = H^2(M;Z), C = H^3(M;Z), and delta = beta(w1(TM)), indices are pairs (x,y) in B² with -4x-2y = delta. Its fiber formula is a torsor for C direct sum coker D_xy, where

    D_xy(p,q) = (-4p-2q, (2x+y) cup p + (x+2y) cup q).

The success criteria sealed before reviewing the old PASS included the entire parametric h-principle, every principal slice, simultaneous compatibility of the two bundle paths, infinite-CW bundle classification, genuine nonorientable controls, and actual realization of every admissible index.

## 2. Universal linear-algebra reduction

Let V be a real vector space of dimension 3 and W a complex vector space of complex dimension 3. A real-linear L:V→W is an injective totally real map precisely when its complex-linear extension L_C:V⊗C→W is an isomorphism.

If L is injective and L(V) intersects iL(V) only at zero, the equation L(v)+iL(w)=0 forces L(v)=L(w)=0 and then v=w=0. Thus L_C is injective, hence bijective in equal complex dimensions. Conversely an isomorphism L_C restricts to an injective real map; an element of L(V) intersecting iL(V) yields a nonzero kernel of L_C unless that element is zero. This proof is pointwise and requires no orientation, metric, Lagrangian condition, or trivialization of TM.

Consequently a formal solution is exactly a map f:M→F and a complex bundle isomorphism TM⊗C→f*TF. Restricting any such isomorphism to the real TM gives the required formal derivative. This is an equivalence of the formal data, not merely a necessary characteristic-class test.

## 3. Every principal affine slice is ample

Fix a point (m,z) and any real hyperplane H⊂T_mM. Choose a real basis v1,v2 of H and a complementary v3. A principal affine slice fixes L|H and varies L(v3) in T_zF ≅ C³.

If L(v1),L(v2) are **complex** dependent, no choice of the third column can give complex rank three. The allowed slice is empty. Real independence does not suffice: e1 and i e1 are real-independent but complex-dependent; their determinant with every third column vanishes. `controls.py` explicitly tests that negative control.

If those columns are complex-independent, their complex span S is a complex 2-plane and the allowed set is C³\S. A complex linear change of coordinates identifies it with C²×(C\{0}); it is path connected. Its convex hull is all C³. Indeed choose w outside S. For any z in C³ choose a real N≠0 such that neither z+Nw nor z-Nw belongs to S. There are at most two forbidden values of N, so this is always possible. Then z is the midpoint of two allowed vectors. Since the allowed set has one connected component, that component's convex hull is the entire affine slice.

This covers all fixed restrictions and every principal direction, including directions not aligned with a chosen coordinate basis. Empty slices satisfy the usual ample-relation convention vacuously. The determinant condition is open. Thus the totally real immersion relation in J1(M,F) is open and ample. In particular it does not rely on the incorrect assertion that every fixed real-independent pair has a nonempty allowed slice.

## 4. The precise h-principle input and its scope

The complete [Forstnerič author-hosted 1986 scan](https://users.fmf.uni-lj.si/forstneric/papers/1986Expositiones.pdf) was freshly obtained (SHA-256 `233a54e5d06860d06960b701c9cfc4449ed510bd308f449e2f264505e09c2f9e`). Printed pp.244–246 were inspected visually. The initial text extraction returned only form-feed characters and was not treated as a successful read.

The relevant input is Section 2, printed p.246, for a general smooth fiber bundle X→M. An open first-order relation ample in the coordinate directions has its solution space mapping by one-jets to its formal-section space by a weak homotopy equivalence. The statement imposes no open-source, compactness, or orientability assumption. Set X=M×F; its local trivializations give exactly the slices proved in §3. Weak homotopy equivalence supplies both existence and the required bijection on path components. Its parametric/relative content identifies formal paths between holonomic endpoints with paths of genuine totally real immersions.

Forstnerič formulates genuine solutions as C1 sections. Openness gives the usual passage to smooth solutions and smooth parametric families by approximation, fixing smooth endpoints when needed. On a noncompact source one uses approximation with a positive point-dependent tolerance so that the derivative stays in the open relation. This requires no uniform bound at infinity or properness. Smooth sources are paracompact; ordinary compact-open smooth-family homotopies are the convention here.

This use of Section 2 is distinct from Theorem 1.1, which discusses Euclidean targets, and Theorem 1.4, which expressly assumes a **compact orientable** three-manifold. The latter theorem does not prove the candidate's nonorientable existence statement. The former Euclidean theorem alone would not establish the nontrivial target-bundle classification into F.

The complete [Borrelli author PostScript](https://math.univ-lyon1.fr/~borrelli/Articles/IMRN2002.ps) was freshly retrieved (SHA-256 `ec2a73f294b79a5891d4e5e3362e780caed199d3c52b6d35486d4abc36b400e4`) and converted locally for reading. Its introduction defines the totally real condition for maps to a general almost complex W and distinguishes immersion components from embedding components. Section 2.1 is a theorem about improving an embedding isotopy with additional formal data. Those embedding hypotheses are unnecessary for the open ample **immersion** relation and cannot be silently inserted into this result. Borrelli is corroborating context; the general-bundle theorem on Forstnerič p.246 plus §3 supplies the needed universal input.

## 5. The integrable tangent representation

At the standard ordered flag, the holomorphic tangent of SL(3,C)/B_upper is sl3(C)/b_upper. Its three basis classes are E21, E31, E32. For diag(t1,t2,t3), with t1t2t3=1, conjugation multiplies Eji by tj/ti. Therefore the compact torus T² acts with the three complex characters

    L1*⊗L2, L1*⊗L3, L2*⊗L3.

This identifies TF, as a smooth complex bundle, with the associated complex bundle of that representation over SU(3)/T². It does not assert a holomorphic splitting into line bundles. Orthogonal decomposition of a complex flag explains the compact homogeneous model; the ordered quotient lines have first Chern classes x1=x, x2=y, x3=-x-y.

The determinant class is

    (x2-x1)+(x3-x1)+(x3-x2) = 2(x3-x1) = -4x-2y.

The exact adjoint actions on the three matrix entries are tested in `controls.py`. A cyclic-root substitution gives zero determinant class and therefore fails this check. Such a substitution would change the almost complex structure and is inappropriate for the given integrable full flag. There is no Weyl-group quotient: the source names the full ordered flag, and permuting the lines changes the designated primary indices.

## 6. Infinite-CW bundle classification and orientation determinant

A second-countable smooth 3-manifold has a countable locally finite triangulation in its actual dimension. We may work on a CW model of dimension at most three, without requiring finitely many cells. Numerable complex bundles over this paracompact base are classified by maps to BU(3).

The determinant map BU(3)→BU(1)=K(Z,2) has fiber BSU(3). The fibration SU(2)→SU(3)→S5, with SU(2)=S3, gives pi1(SU(3))=pi2(SU(3))=0; thus BSU(3) is 3-connected. For a 3-dimensional CW domain, all obstruction groups for lifting a determinant map lie above its cellular dimension, and all relative obstruction groups for comparing two lifts lie above the dimension of M×I. Equivalently, the 3-type of BU(3) is K(Z,2). Hence c1 gives a bijection between complex rank-three bundles and H^2(M;Z), and every SU(3) bundle on M is trivial.

This cellular argument is valid on infinite CW complexes directly: a nullhomotopy is built cell by cell through the finite number of dimensions. It is not an inference from an inverse limit of classifications on finite subcomplexes and introduces no phantom-map assumption. It uses ordinary, untwisted integral cohomology; the targets' homotopy groups provide constant coefficient systems.

The determinant of TM⊗C is (Λ3_R TM)⊗C. The real orientation line has transition signs (-1)^epsilon. Writing them as exp(pi i epsilon), the obstruction to lifting to continuous logarithms is the integral cocycle obtained by dividing the coboundary of a 0/1 lift of epsilon by two. This is precisely the coefficient Bockstein beta(w1(TM)). Its sign would not matter here because it has order dividing two. Thus c1(TM⊗C)=delta without assuming orientability or real parallelizability.

## 7. Every admissible index has an actual representative

Fix arbitrary x,y∈H^2(M;Z) with -4x-2y=delta. Choose the three universal torus lines with x3=-x-y and their specified product trivialization. Their sum E0 is an SU(3) bundle and therefore has an SU(3) trivialization on this 3-dimensional base. The preceding isotropy representation E_rho has c1=-4x-2y=delta; rank-three bundle classification gives an isomorphism E_rho≅TM⊗C. These two choices make a formal representative. Section 4 deforms it to an actual totally real immersion and preserves its formal component, hence the primary index. This is a universal realization argument for **all** admissible indices, not a finite collection of symbolic examples.

The image of (x,y)↦-4x-2y is precisely 2B: it is contained in 2B, and if delta=2z then x=0,y=-z realizes delta. Coefficient exactness says delta∈2B iff its mod-two reduction vanishes. The Bockstein identity rho2 beta(w1)=Sq1(w1)=w1² then gives

    totally real immersion exists ⇔ beta(w1)∈2H^2(M;Z) ⇔ w1²=0.

Neither beta(w1)=0 nor orientability is required. No division by two inside a torsion group is used.

## 8. Independent genuine nonorientable controls

The interior of a Möbius band times R is a boundaryless noncompact nonorientable 3-manifold homotopy equivalent to S1. Its orientation class is the reduction of an integral circle class, so delta=0. The existence argument applies. The candidate's specialization has A=Z, B=C=0 and gives coker[(p,q)↦-4p-2q]=Z/2. This checks the two regular-homotopy classes in a nonorientable open source with trivial complexified determinant.

RP2×R is another boundaryless noncompact nonorientable source. Here H^2=Z/2, and delta is its nonzero generator. It is not divisible by two and w1²≠0, so no totally real immersion into F exists. This falsifies any accidental rule that every noncompact or every nonorientable source is automatically allowed. The closed RP2×S1 has the same obstruction.

A stronger diagnostic is a closed nonorientable source with delta **nonzero but divisible by two**. It is constructed here independently of the old review's Reid census example. Let

    K = R² / <a(X,Y)=(X+1,-Y), b(X,Y)=(X,Y+1)>

be the Klein bottle. The affine diffeomorphism h(X,Y)=(-X,Y-1/2) satisfies

    h a = (a^-1 b) h,    h b = b h,    h² = b^-1.

Thus h descends to a smooth diffeomorphism f:K→K. Let M_f be its mapping torus. It is a closed smooth connected 3-manifold and is nonorientable because the fiber Klein bottle has trivial normal line and nontrivial orientation class. Its fundamental group has the Klein relation a b a^-1=b^-1 and mapping-torus conjugation relations inducing a↦a^-1 b, b↦b. Abelianization therefore gives

    2b=0,    2a=b,    H_1(M_f;Z)=Z<t>⊕Z/4<a>.

For the mapping-torus convention (p,1)~(f(p),0), one can realize the chosen conjugation presentation on R²×R using the deck transformation T(p,z)=(h(p),z-1). It has orientation sign -1, so w1(T)=1, w1(a)=1, and w1(b)=0. Although h²=b^-1 on the fiber cover, T²(p,z)=(b^-1(p),z-2); **no relation T²=b^-1 is imposed** in the mapping-torus group. An adjusted free H_1 generator t+a has the opposite orientation value; this changes the corresponding nonabelian presentation but not the abelianization or conclusion. Every integral character vanishes on the torsion class a, so w1 has no integral lift. It does lift to a Z/4 character: send a to 1, b to 2, and the displayed T to 1. All relations are satisfied.

For a closed odd-dimensional manifold the Euler characteristic is zero. Here b1=1 and b3=0, so b2=0. Integral universal coefficients consequently give H^2(M_f;Z)=Ext(H_1,Z)=Z/4 (Hom(H_2,Z) vanishes because b2=0). Since w1 has no integral lift, delta≠0. Exactness also gives 2delta=0, hence delta is the unique order-two element 2 of Z/4. It is divisible by two and reduces to zero, so w1²=0. The admissibility equation has exactly eight labels: arbitrary x∈Z/4 and odd y∈Z/4. Every one has an actual immersion representative by §7.

`controls.py` checks the affine equalities, nonzero Jacobian, abelianization Smith form, absence of any integral character lifting w1 on a, the mod-four lift, and all eight labels. The written argument, rather than just a presentation calculation, establishes that this is a genuine manifold and identifies its orientation character. A separate read-only adversarial subagent independently checked the free/proper deck action, inverse normalization, mapping-torus normal forms, integral cohomology versus homology distinction, and cochain Bockstein square identity; its complete verification is preserved in MAPPING_TORUS_ADVERSARY.md. No cup-product table or fiber-group count for this example is inferred merely from its homology.

The separately freshly retrieved [Reid appendix](https://math.rice.edu/~ar99/immersionsFKKT_2.pdf) (SHA-256 recorded in `SOURCE_MANIFEST.json`) supplies an additional prior genuine example with H_1=Z⊕Z/4 and no integral lift of w1. Its proof includes census/computational geometric inputs; those are not re-certified here. The new explicit Klein mapping torus avoids dependence on those numerical orientation and census inputs for this audit's diagnostic.

## 9. Compatibility of the simultaneous formal-space model

Let T=T²⊂G=SU(3), and b0:BT→BG be induced by inclusion. Its homotopy fiber is G/T. One geometric model uses a principal T bundle together with a G trivialization of its induced G bundle; the resulting reduction of the trivial G bundle is a map to G/T. The determinant trivialization is built into T⊂SU(3). A free U(3) trivialization would be different data and could add a determinant invariant.

Let b_rho:BT→BU(3) classify the tangent representation in §5. Restricted to the homotopy fiber of b0, it classifies TF. Therefore the space of formal data is

    Map(M,F) ×^h_Map(M,BU(3)) {tau},

where tau classifies TM⊗C. The homotopy-fiber interpretation of F and associativity of homotopy pullbacks identify this space with

    hofib_(constant,tau)[ Map(M,BT) → Map(M,BG) × Map(M,BU(3)) ],

the candidate's (7). Mapping spaces are understood in the usual compactly generated setting, or replaced by equivalent singular-function-space models; M is locally compact. Derived mapping out of M preserves this homotopy limit.

Both paths have the **same BT base datum**. The first is an SU trivialization of the direct sum of the ordered lines; the second identifies the associated tangent representation with the fixed complexified source tangent bundle. Given the first path, the second is exactly an isomorphism over its resulting flag map. Conversely a flag map and formal derivative produce both paths. Their endpoint identifications and homotopies are retained. There is no additional compatibility obstruction, and the two paths are not free choices of unrelated bundles. Homotopies of the common torus datum account for the shared loop action later computed in §§6–8.

This verifies the actual formal space, not only equality of its apparent characteristic classes. It does not independently replace the later integral loop-coordinate and component-orbit proof; that is the separately assigned topology family.

## 10. Boundary, properness, and disconnected conventions

All stated arguments apply to closed, open, noncompact, orientable and nonorientable sources within the candidate's hypotheses. The source must have its actual dimension at most three and be paracompact for the chosen bundle classification; smooth second countability supplies these requirements. The smooth source has no boundary in the statement. If a different intended convention includes boundary or a prescribed boundary immersion, the statement and relative boundary data must be specified anew; this audit asserts no such classification.

Because F is compact, a proper map M→F would force M compact by taking the inverse image of F. Thus the ordinary/proper distinction is observable: the allowed R3 case cannot have a proper representative. It cannot be settled by an ordinary h-principle while silently imposing properness. No control at infinity appears in the formal data. Ordinary cohomology is therefore appropriate; compactly supported cohomology would create spurious invariants, already visible on R3.

For a disconnected second-countable source, connected components are open and there are at most countably many. Maps, formal data, and homotopies are independent on them. The componentwise extension means the **Cartesian product** of the connected-component classification sets; an empty component factor means no global immersion. It does not mean a disjoint union over components. Infinite-component ordinary cohomology is the corresponding product of cohomology groups. The main theorem only claims a connected source, so the terse componentwise remark does not damage it.

## 11. Computational reproduction, falsifiers, and limits

The initial system-python run failed because SymPy was absent. The subsequent orchestration attempt found that the second isolated program had not been copied after the first early failure. These failures and their available stdout/stderr remain in `reproduction/` and `REPRODUCTION.json`; they were not mathematical failures. Using the existing workspace `.venv/bin/python`, with SymPy 1.14.0, both exact original programs then ran unchanged with empty stderr. Author stdout SHA-256 `78a85bfdf25f6e46b4a7f479ca6bcf252bd65ce6ccf5219fb738c39e6c6ec447` and legacy stdout SHA-256 `7302545150d78712b9ac8bc51568f11eed3b5b7704d835b957ee4dc328b6fb9f` equal their frozen receipts byte for byte. The legacy receipt contains 1,595 assertions. These reproduce algebraic diagnostics only.

The independent family controls use no imports from either frozen checker. They test falsifiable points with actual affine deck transformations and complex matrices, in addition to exact presentation computations. Important controls are real-independent/complex-dependent fixed columns, a non-coordinate principal direction, the direct-sum total-reality condition, explicit allowed midpoints, polygonal paths avoiding the deleted quotient origin, actual isotropy weights, the wrong cyclic-root determinant, obstructed RP2×R, and the new closed mapping torus's nonzero divisible determinant. Their universal conclusions come from the written proofs above, not from the number of checks.

The protected main branch was read from `.git/HEAD`; no Git or GitHub operation was performed by this family. Main's queue still read queued 0/5 and main's state JSON had no 6800007 row at the observation time. The original PR's ledger independently records 1/5. None of the protected main queue/state, original files, PR inputs, or another family was modified. `PROTECTED_STATE_READ.json` records the read-only observation.

Optional clarity repairs, not mathematical requirements for this stated theorem: say “complex-linearly independent” in CANDIDATE §3's fixed-column sentence; cite Forstnerič Section 2 p.246 directly for the general-bundle weak equivalence; spell out “Cartesian product over components” in the disconnected remark. No proposed repair shrinks the source to orientable/compact manifolds or changes the complex structure.

Strongest verified result of this family: every candidate index satisfying -4x-2y=beta(w1) is realized by an actual totally real immersion, the existence criterion beta(w1)∈2H^2 ⇔ w1²=0 holds in the full stated source scope, and (7) correctly models all formal data and their homotopies. The precise remaining dependency for the full classification is the complete integral mapping-space loop and monodromy computation of §§6–8. This family identifies no counterexample to that calculation, but leaves its independent verification to its designated audit. Nothing here proves historical novelty or upgrades a queue/PR disposition.

## Reproduction

From `/Users/alec/Documents/Math`, run the existing workspace interpreter on `hprinciple_family/controls.py`. For exact original receipt reproduction, run the copied `reproduction/verify.py` and `reproduction/review/independent_checks.py` with that same interpreter and compare stdout with `source_snapshot/verification.json` and `source_snapshot/review/independent_results.json`. `REPRODUCTION.json` records hashes, environment choice, and failures. `MANIFEST.json` covers first-party audit files and excludes itself, third-party source/reference copies, tmp, cache, and bytecode. Reference copies are kept locally and ignored to avoid redistributing them in the audit release.
