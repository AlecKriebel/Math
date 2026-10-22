# Independent PR1350 / problem10400168 audit

22 October2026UTC. Pinned head `3d765aeead02d6ae70874c38023ef4263fb24ff0`. Family: original source, independent mathematical falsification and bounded priority. Parent sweep80%. This is an AI research audit; no conventional human peer review or proof-assistant verification is claimed.

## Decision

The strongest verified result is the full inclusion-dependent **oriented(3,2) defect-interface answer** for complete finite spherical Barrett–Westbury data over C and every compatible based restriction with its inherited pivotal/spherical structure. No fatal gap was found in the restricted-regular bimodule, the two partial-trace requirements, the published defect-functor application, the orientation conventions, or the per-bulk and boundary normalizations.

This is an existing-result application. Carqueville–Müller's published *Orbifold Completion of 3-Categories*, DOI[10.1007/s00220-025-05434-y](https://doi.org/10.1007/s00220-025-05434-y), actually supplies the required defect construction, not merely an abstract suggestion. The source record and version-of-record first page authenticate online publication6December2025, CMP407,article8(2026). CRS's actual proof supplies the ordinary bulk identification with its coloring-dependent boundary rescaling. The elementary restricted-trace verification below specializes those results to the supplied inclusion. A qualified existing-result ledger row is justified and proposed locally; nothing was written to the ledger or any external service.

The original question is qualitative, leaving the kind of relation unspecified. The interface is a substantive answer under the declared categorical BW/based-restriction interpretation: its distinguished action recovers the specified inclusion, both ordinary bulk theories are identified, and mixed bordisms have state spaces/maps obeying sewing. This is not merely the assertion that each theory has a center. The original source does not require an invertible wall, equivalence, an ordinary natural transformation of the two bulk functors, or a fully extended theory down to points. Requiring one would manufacture a stronger target.

The exact coverage boundary remains visible: the historical exposition does not provide a complete numerical axiom list. No reconstruction from an arbitrary algebra subspace or an arbitrary array satisfying unspecified named equations is proved. This is a limitation of what those phrases specify, not a residual theorem silently solved here. Actual BEK and KO inclusions are covered under the precise hypotheses below. No universal formula for singular braided doubles, no automatic trace for arbitrary module categories, no new general theory and no firstness claim is made.

## Original request and model identification

The fresh publisher primary is Ohtsuki(ed.), *Problems on invariants of knots and3-manifolds*, Geometry & Topology Monographs4(2002), printed506–510/PDF134–138. Full source4731008bytes,SHA256 `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd`; selected pages retained privately. Problem9.4,p510/PDF138 was visually checked. Its closing request is “What relation do we have for these TQFT's?” The two inputs are ambient fusion/6j-data and a subsystem with restricted symbols. The following remark highlights alpha-induction and singular S; it does not impose modularity. [Primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=138).

The nearby isomorphic-theory question is9.3, a different problem. Equation48,p509 gives an individual label-system normalization w^(-v), w=sum_i mu_i². The exposition describes simple labels, full multiplicity spaces and associator-coordinate changes. It does not write every numerical coherence/duality equation; positivity enters conditionally in a subfactor-realization discussion. The categorical interpretation uses the complete spherical state-sum input cited there.

Barrett–Westbury's actual Definitions2.5/2.8/2.10–2.13 and Theorem5.1 authenticate that interpretation: finite semisimple spherical input of nonzero dimension, without a positivity requirement. Over C it is the usual fusion-category model, or its additive/idempotent completion if the starting presentation supplies only simples. Turaev–Virelizier's trace conventions and sphere computation also match the pinned formulae. No arbitrary monoidal category is asserted spherical.

One source discrepancy is real and already disclosed by the PR: p510 describes the untwisted finite-group state sum as an unweighted count of conjugacy classes. The normalized Equation48 instead gives |Hom(pi_1(M),G)|/|G| for connected closed M, hence1/|G| on S³. The defining state sum and normalized TVBW theory govern this audit. Keeping the prose unweighted count would contradict that normalization; it is not an additional condition on the requested interface.

## Independent categorical derivation

### 1. Complete input and the based restriction

Fix a spherical fusion category C over C and a full strong monoidal inclusion i:D->C. The pivotal structure on D is the restriction of that on C. A complete numerical version has finite simple labels I, a unit0, duals i*, multiplicity spaces H_ij^k, invertible recoupling maps satisfying pentagon/triangle, coherent evaluation/coevaluation satisfying snakes, and coherent pivotal data with equal left/right traces. The edge weights are those traces and the tetrahedral tensors use those same duality pairings and associator gauges.

To reconstruct, take finite I-graded vector spaces X=(X_i) with componentwise morphisms and

    (X tensor Y)_k = direct_sum_(i,j) X_i tensor Y_j tensor H_ij^k.

The specified recoupling maps give the associator, the specified unit spaces give unitors, and their identities are exactly monoidal coherence. The supplied duality and pivotal maps extend over finite sums; the snake and pivotal identities remain true. Equality of traces on simple blocks extends to every endomorphism by ordinary matrix trace. This constructs precisely a spherical fusion category with the supplied data, rather than another categorification of the fusion ring.

Let J contain0, be closed under duals, and retain every k with H_ij^k nonzero for i,j in J. Retain entire multiplicity spaces and structural maps. The full subcategory on J-supported objects is closed under tensor products, duals, sums and summands. Fullness places every restricted structural map inside it, and every coherence identity is the ambient identity. No intermediate associator label is omitted. Its trace is computed by the same diagram, so i is spherical and its simple dimensions agree. Conversely every full replete inherited fusion subcategory arises in this way. This is the required exact translation for a compatible **based** subsystem.

A mere linear subalgebra does not do this. In C[Z/3], s=g+g² satisfies s²=2+s, so span{1,s} is an algebra but not a subset of the original simple basis. The object represented by s is g direct_sum g², with a two-dimensional endomorphism algebra. Calling it a new self-dual simple would also violate the coefficient1 of the tensor unit in x tensor x*. This is a concrete boundary counterexample, not a new condition on the actual based restriction.

### 2. The particular bimodule and its trace

Let M be the underlying category C, with

    d acts on m acts on c = i(d) tensor m tensor c,
    t_m(f) = tr_C(f).

Its left, right and mixed associators/unitors are the ambient ones, with i's tensorator inserted for a nonliteral inclusion. Each module/mixed pentagon is an instance of the ambient pentagon and i's strong-monoidal coherence. Finite semisimplicity makes the actions exact. M is therefore a finite semisimple(D,C)-bimodule. It is indecomposable as a right module: a summand containing the simple unit contains1 tensor c for every c.

For a simple s, d_s=tr_C(id_s) is nonzero. Rigidity identifies Hom(1,s* tensor s) with End(s)=C, so the unit appears with multiplicity one. Evaluation and pivotal coevaluation are nonzero by the snake identities. In a semisimple category the resulting nonzero projection/inclusion for that unique simple summand have nonzero composite, equal to d_s. For m=direct_sum_s s tensor V_s,

    t_m(f) = sum_s d_s Tr(f_s).

This is basis independent. Rectangular matrix cyclicity gives t_m(gf)=t_n(fg). Opposite matrix units pair every nonzero morphism block with nonzero weight d_s, proving nondegeneracy on all Hom(m,n) x Hom(n,m). A nonsimple object can have dimension zero without its trace pairing becoming degenerate. Positivity and absolute values have not been used.

Use left evaluation ev_x:x* tensor x->1 and coev_x:1->x tensor x*, together with pivotal right evaluation tilde_ev_x:x tensor x*->1 and tilde_coev_x:1->x* tensor x. Define

    ptr_L,x(F)=(ev_x tensor1)(1_x* tensor F)(tilde_coev_x tensor1),
    ptr_R,c(G)=(1 tensor tilde_ev_c)(G tensor1_c*)(1 tensor coev_c).

Expanding the left trace of F on x tensor m as nested evaluation/coevaluation gives

    tr_L,xm(F)=tr_L,m(ptr_L,x(F)).

Expanding the right trace on m tensor c gives

    tr_R,mc(G)=tr_R,m(ptr_R,c(G)).

Sphericity identifies the two whole-category traces with t. The maps for x=i(d) are exactly the restricted maps from D. Thus both left and right module-trace equations hold for **every** endomorphism, not just identities or decomposable tensors. On i(d) tensor m tensor c the disjoint outer closures commute by interchange/coherence. Their composite is the partial trace for D boxtimes C^(reverse tensor); additivity extends this to the whole Deligne product. The action functor's Calabi–Yau compatibility likewise follows on tensor-product morphism blocks and hence by linearity. These are exactly the two diagrams of CM Definition5.16/Equation5.13, visually checked in the published PDF.

The normalization t_1(id_1)=1 is fixed. Applying right compatibility with m1 shows any other compatible regular right trace is its scalar multiple; that value fixes the scale. The hypothesis is falsifiable: with underlying Vec_(Z/2) on both sides, put sign spherical structure on D and standard one on C. At the nontrivial g, left compatibility requires t_g=-t_1 and right compatibility requires t_g=t_1. Nondegeneracy forbids t_1=0. Such separately chosen structures need not work; literal inherited restriction does.

Every simple and both global dimensions

    Delta_A=sum_(s in Irr(A))d_s², A=D,C

are nonzero in characteristic0. Nonzero global dimension is the established fusion-category result explicitly invoked in CM Remark5.19; it is not inferred by incorrectly treating complex summands as positive. The module's sum of simple trace-dimension squares is Delta_C. This is not an index or a universal wall-amplitude quotient.

### 3. Inclusion recovery and orientation

For a right-C-linear F:C->C, its module constraint gives F(c) isomorphic to F(1) tensor c. Every right-module natural transformation is f tensor id_c, determined at1. Thus evaluation at1 is a monoidal equivalence

    Fun_C(C_C,C_C) -> C

when tensor product of endofunctors means F composed with G: L_x composed with L_y=L_(x tensor y). The left D action d->L_i(d) returns i(d), including its tensorator, under that equivalence. With the distinguished regular marking, the wall therefore remembers the specified inclusion. Unpointed bimodule equivalence can identify inner-conjugate embeddings; no stronger uniqueness assertion is made.

CM calls a(D,C)-bimodule a categorical1-morphism D->C. The left/right action regions must follow that convention. Meusburger instead depicts a positive normal pointing toward the left-action region; with these names it points C->D. These are compatible distinct conventions, not an orientation reversal of the same unchanged label.

An admissible reverse label is the traced opposite on C^op:

    c acts on m^op acts on d=(i(d)* tensor m tensor c*)^op,
    t#_(m^op)(f^op)=t_m(f).

Covariant dualization m^op->m* identifies it with the regular(C,D)-bimodule, using the pivotal isomorphisms to identify double duals. Spherical trace is invariant under this dualization. Actual Euler-adjusted evaluation/coevaluation and surface-reversal coherence maps are those of the published CM construction. Equality with every map in Meusburger's different model is not asserted.

### 4. The legitimate published import and the full functor

The independent application checked these actual primary locations: CM Definition5.2/Example5.5(pp47–48), Euler construction(p51), Definition5.16/Proposition5.17/Theorem5.18(pp52–54), and construction/Theorem6.4/Example6.5(pp58–63). Proposition5.17's proof compares the two adjoint structures using the traced action; both its premise and the specific regular input above were checked. The general orbifold-coherence theory is an established published import, not a newly asserted lemma hiding the same unresolved task.

For each bulk A choose its own Euler scalar phi_A with phi_A²=Delta_A^(-1), and compatible nonzero simple-dimension square roots. The verified traced M is an admissible1-morphism between those data. Theorems5.18/6.4 and Example6.5 then supply one symmetric monoidal functor Z on oriented compatibly labelled, conically stratified3-bordisms with closed stratified2-manifolds as objects. Use its full permitted label system, or a restriction containing needed identities, adjoints, composites and junctions. A lone surface label is not falsely asserted closed under every operation.

For a surface Sigma and compatible triangulation tau let V_tau be the pre-space. Cylinder maps relate the V_tau and their fixed-triangulation cylinder P_tau is idempotent. The state space is the colimit, isomorphic to im(P_tau). A decorated3-bordism induces its map on those spaces, independent of triangulation, and gluing, disjoint union and identity cylinders hold there. These are the actual constructions in CM6.2, not an extrapolation from equal closed-manifold numbers or fixed-boundary invariance. General conical local models and finite strata are the theorem's domain.

For pure A regions there is a monoidal natural isomorphism J_A between this restriction and ordinary normalized TVBW_A. The resulting relation is the common defect extension, the two J_A and the distinguished M_i. A wall cylinder Sigma x[0,1] gives maps TVBW_D(Sigma)->TVBW_C(Sigma) commuting with diffeomorphisms and disjoint unions and participating in decorated sewing. An ordinary topology-changing bordism need not move the wall from one end to the other. Reversing a wall gives a double wall, not automatic cancellation. This is the full original qualitative interface answer at the specified model level.

### 5. Normalization and coloring-dependent comparison

On a closed triangulation in bulk A the normalization is Delta_A^(-v), times that category's edge dimensions and tetrahedral weights. Thus the retained-label part of C's raw sum, still normalized by Delta_C, is not the D theory; D uses Delta_D. The particular Vec subset Vec_(Z/2) has sphere values1 and1/2. These disagree, so a universal monoidal natural transformation between the ordinary theories cannot exist: its empty-surface component is invertible by the monoidal unit condition, and naturality for the closed bordism S³ would equate the two scalars. This obstruction does not undermine a defect extension.

For a pure-bulk boundary graph Gamma with coloring c, CRS4.70 gives

    f_A(Sigma,Gamma;c)=Delta_A^(#complementary_regions/2)
                        product_(edges e) d_(c(e))^(-1/2),
    Z_orb(Y^t)=F_out^(-1) p_TV(Y^t) F_in.

F is diagonal over colorings; it is not generally one scalar. Both nonzero roots and the correct separate Delta_A are essential. The formula conjugates cylinder projectors and gives J_out Z_orb(Y)=TVBW_A(Y) J_in on their images. Complement-region counts add and edge products multiply under disjoint union, so the comparison is monoidal. The actual proof of CRS Theorem4.5,pp38–41,v2, was read; its p41 formula was also visually checked. No formula for arbitrary mixed-phase raw normalizations is inferred from this pure-bulk equation. Consistent root choices suffice for existence; no choice-free entire defect extension is claimed.

## Actual alpha-induced inputs

BEK's original Assumption2.1 fixes a finite-index typeIII subfactor N subset M with finite braided N–N system X, and a subsystem Y containing the dual canonical theta. The extension carries its canonical Q-system; a bare arbitrary object is not enough. No general locality/commutativity or irreducibility/haploidity condition is inserted. The actual p6 inclusions are

    X_M^0 subset X_M^+/- subset X_M^alpha subset X_M,

with the analogous Y rows and their vertical subsystem inclusions. Taking all finite sums, summands and intertwiners gives genuine full finite rigid C*-tensor inclusions. Standard statistical duality/trace is spherical and restricts to the same objects and intertwiners. These are the D subset C inputs; they exist also with degenerate braiding. BEK p5 explicitly gives Hom(lambda,mu) subset Hom(alpha(lambda),alpha(mu)), potentially strictly. Thus alpha itself is not assumed fully faithful. Their degenerate intertwiner results3.9/4.6 remain credited, and product-double corollaries3.10/4.8 retain nondegeneracy. No S inverse appears in the wall construction, even when normalized S itself needs a nonzero Gauss sum.

For KO take finite semisimple ribbon B with simple unit and a commutative connected B-algebra A, rigid in their explicit Definition1.11: epsilon_A m is nondegenerate and dim_B(A) nonzero. Assume theta_A=id. Theorem1.5 gives the tensor product overA and unitA;1.15 gives rigidity and1.17 pivotality, including preservation on local modules. Theorem3.3/Lemma3.4 splits every module off a free module. Free modules on the finitely many B-simples generate, so Rep(A) is finite semisimple; End_A(A)=Hom_B(1,A)=C gives simple unit. Theorem1.18 and Remark1.19 give left and right trace/dimension d_B(X)/d_B(A), hence sphericality. Definition1.8 and Theorems1.10/1.15 give the full sum/summand/dual/tensor-closed local-module inclusion

    Rep^0(A) subset Rep(A)

with that same pivotal structure. These results occur before KO's modularity assumption in Section4. The forgetful Rep(A)->B is not the unit-preserving tensor inclusion, and the free-module functor B->Rep(A) need not be full. This precise nonunitary-capable branch is covered without inverting S. Arbitrary algebra objects outside these hypotheses are not claimed covered.

## Supplementary relative-center claims

The entire pinned RELATIVE_CENTER_INTERFACE was read. Direct evaluation-at1 and the bimodule functor coherence give

    E_i=Fun_(D|C)(C,C) equivalent to Z_D(C),

with relative half-braiding sigma_d:x tensor i(d)->i(d) tensor x and tensor product sigma^(xy)_d=(sigma^x_d tensor1_y)(1_x tensor sigma^y_d). The D-center lift has half-braiding sigma_a^(-1) against an E object, so it reverses the braiding on Z(D); the C-center lift is the original full half-braiding. They centralize because the two mixed crossings are inverse. Thus the canonical central functor is

    overline(Z(D)) boxtimes Z(C) -> Z(E_i).

The actual Kong–Zheng Theorem3.3.7 proof,p23, authenticates that it is a braided equivalence for indecomposable multifusion D,C and nonzero semisimple bimodule M. These hypotheses hold. GNN Definition2.1/Remark2.4 independently authenticates relative-center fusion and FPdim(E_i)=FPdim(D)FPdim(C); its later graded statements are not used without a grading. No pivotal/ribbon compatibility of the braided equivalence is inferred, and FPdim is not substituted for trace normalization.

The additional inner-conjugacy and fusion arguments check by evaluating a right-module equivalence L_u at1, so u is invertible and its left-module constraint is u tensor i(d) isomorphic to j(d) tensor u. Literal trace preservation requires d_u=1; spherical invertibles can instead have d_u=-1. Balanced tensor products give M_i boxtimes_C N_i equivalent to D C D and composition of nested regular restrictions, but no trace-normalized cancellation follows. Invertibility of the original wall forces its action D->Fun_C(C,C) equivalent to C to be a tensor equivalence, hence i essentially surjective. These are consistent supplementary algebraic facts, not a substitute for CM's oriented functor.

## Falsification controls and limits

No author program was executed. The independently written standard-Python diagnostics check every grade-preserving matrix unit on a27-dimensional triple tensor basis in signed Vec_(Z/2), left/right/mixed partial traces and rectangular nondegenerate pairings, including a zero-dimensional nonsimple object. They check coloring-dependent conjugation, projector intertwining and sewing by exact rational matrices; these matrices are diagnostic linear algebra, not claimed actual TV matrices. Every flat labeling determined by rooted vertex data on the boundary of a4-simplex is enumerated for groups of orders2,3,6; all triangle equations and the converse are checked, giving normalized S³ values1/2,1/3,1/6. The distinguished subgroup action recovers the inclusion, and the false linear-subalgebra restriction is tested.

Outputs match under normal,-O,-OO Python. Nine deliberately corrupted variants—discarding pivotal signs, reversing the boundary conjugation, or changing the vertex normalization, each in three modes—are rejected. These finite checks support the explicit derivations; they do not verify every orbifold coherence theorem numerically or provide a formal proof.

## Priority and proposed disposition

The fresh GWS read at12:50:22.727976Z preceded mathematics:191rows,13 broad keyword hits, all read and distinct. Extra hits include “diffusion” containing “fusion” and unrelated proof/physical defects. No same-target ledger record was found. Parent's lead file contains11 generic hits/deposit records, not authenticated target coverage.

The primary CM version of record and actual relevant proof/construction—not its title/abstract alone—supply the full declared relation. CRS2020 establishes its normalized ordinary bulk comparison. Earlier Kitaev–Kong2012 Section5 already constructs bimodule walls for unitary Levin–Wen models; its outlook explicitly declines a general topological-invariance claim. Fuchs–Schweigert–Valentino2013 gives the central/Witt description of surface defects, and GNN2009/Kong–Zheng2018 supply general algebraic center structure. These are material antecedents. This audit does not call CM the earliest historical answer or present an old construction as new. The explicit full oriented defect functor, all spherical inputs and checked normalization make CM the authenticated DOI chosen for the qualified existing-result row.

`PROPOSED_LEDGER_ROW.json` contains exactly four literal cells; B is blank and C is the proper CM DOI. D states the categorical BW/based scope, exact theorem chain, original source, inclusion dependence, normalization, alpha-model hypotheses, prior attribution and limits, with PR1350 provenance. It records an existing-result answer rather than a new publication or an assertion that CM invented or addressed every historical numerical convention. No row/service/PR/Git/publication write occurred.

The remaining uncertainty is historical earliest priority and unformalized numerical source readings. Full older papers and all general theorem dependencies were not re-proved; precise versions/pages/read limits are in SOURCE_INDEX.md. These are not unclosed hypotheses in the stated categorical interface. The result should retain its qualification instead of either claiming an unrestricted reconstruction theorem or labeling this full declared interface merely partial because stronger unasked outputs fail.
