# PR384: induced-endotrivial family and analytic completion review

Reviewed target: frozen PR head `682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6`, particularly Turn 5 and its Turn 2 prerequisites. All 52 files in `../snapshot_manifest.json` match their recorded lengths and SHA-256 hashes. This report is an additive verification artifact; it does not modify the candidate, its historical review, a queue, or a publication disposition.

**Scoped result:** the Turn 5 theorem reconstructs correctly for every nontrivial elementary abelian p-group and every module field of characteristic p. The completed induced-endotrivial subalgebra and its projective extension are symmetric. No required mathematical repair has been found. The original universal symmetry question remains unsolved at five of five author turns. This is not novelty certification or merge-readiness certification; the parent audit controls the PR385-before-PR384 gate.

## Exact original target

The complete Benson contribution in OWR 14/2019, printed pages 847–849, was retrieved and visually inspected, including the conjugation bars on page 849. The objects are finite-dimensional modules over an arbitrary field k of characteristic p, for a finite group G. The split Green ring has indecomposable module classes as its free integral basis; its additive relations concern direct sums. Its complexification uses C for analysis while retaining k for the representations. For x=sum c_M[M], the norm is sum |c_M|dim_k(M), and the involution conjugates c_M and takes the contragredient dual of M. The full completion is a commutative unital Banach *-algebra. The question asks whether its x*x spectra are always nonnegative real, equivalently whether every dimension-bounded species respects duality and complex conjugation. The stable projective quotient, maximal quotient and further C*-completion are separate objects. [Official OWR source](https://ems.press/journals/owr/articles/16776).

The Turn 5 result addresses a specific closed subalgebra of the actual stable completion for E, and then its corresponding full-completion span. It does not assert a universal theorem or an actual-group nonsymmetry example.

## Primary inputs and exact access limits

The controlling accessible Benson text is [arXiv:2008.13155v2](https://arxiv.org/pdf/2008.13155v2), dated 30 April 2022. Printed page 69/PDF page 69 was inspected visually: Proposition 4.4.6 supplies the elementary abelian endotrivial classification, Lemma 4.4.7 supplies syzygy growth, and Theorem 4.4.8 supplies endotrivial gamma equal to one. Corollary 4.3.8 supplies invariance under field extension. Sections 4.1–4.2 use a field of characteristic p without imposing algebraic closure; Section 4.10 supplies the induction/restriction and Mackey identities. The relevant nontrivial p-groups ensure p divides their orders. The published 2024 Memoirs edition is separately identified by the [AMS publication listing](https://www.ams.org/journals/notices/202408/202408FullIssue-optimized.pdf), Volume 298, No. 1488; its full PDF was not retrieved and the accepted manuscript is not asserted byte-identical to it.

The author-hosted primary [Benson–Symonds preprint](https://personalpages.manchester.ac.uk/staff/peter.symonds/preprints/bs1.pdf), *The non-projective part of the tensor powers of a module*, independently confirms the inherited input: its introduction permits arbitrary k, Lemma 2.11 preserves gamma under scalar extension, and Theorem 7.5 gives endotrivial gamma one. Printed pages 4–5 and 11–12 were visually inspected. Theorem 7.1 credits Carlson's restriction dimension bound; Proposition 7.4 credits Dade's classification. Their exact original proof PDFs were not directly obtained here. Thus those are credited dependencies through an accessible primary theorem, not claimed independently re-proved original classification theorems.

[Carlson–Thévenaz, Annals 162 (2005)](https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p05.pdf), printed pages 823–824, also explains unique indecomposable endotrivial cores, injectivity of scalar extension on T(G), the reduction to algebraic closure, Dade's noncyclic abelian classification, and the cyclic boundary cases. Its subsequent algebraic-closure convention is explicitly qualified; it is not silently applied to arbitrary-field modules. The [Dade II publisher metadata](https://annals.math.princeton.edu/1978/180-2/p05) was located, but an attempted publisher PDF returned 404. The Carlson 1981 DOI `10.1016/0021-8693(81)90129-0` was located, but its full original proof was inaccessible through the tool. `SOURCE_MANIFEST.json` records downloaded source hashes and these access limits. Raw PDFs, extracted text and rendered source pages are in the locally ignored `sources/` folder.

## Actual module injection before the formal algebra

An endotrivial stable class has a unique indecomposable nonprojective core M_t. The stable tensor inverse makes tensoring by that object an equivalence, and the stable unit k has endomorphism algebra k and is indecomposable. Krull–Schmidt then supplies uniqueness of the actual nonprojective core. Restriction to a nontrivial subgroup preserves stable endotriviality because restriction preserves projectives.

For E=H×K, the actual induced module is M_t tensor kK. Its endomorphism algebra is

    D = End_(kH)(M_t) tensor_k (kK)^op.

The first factor D_0 is local. The ideals rad(D_0) tensor kK and D_0 tensor aug(kK) are nilpotent; their products commute as ideals, and their sum is nilpotent. The quotient is D_0/rad(D_0), a division algebra. Hence D is local and the induced module is indecomposable. No step assumes that tensor products of arbitrary local k-algebras are local: the crucial special property is that kK/aug(kK)=k. This removes a possible nonclosed-field counterexample.

For a subgroup C of order p contained in H, restriction gives [E:H] copies of Res_C M_t. Endotriviality gives (dim M_t)^2 congruent to 1 modulo p, so this restriction is not projective. If C is not contained in H, C∩H=1 and Mackey expresses the restriction as free kC modules. The nonprojective ordinary cyclic restrictions therefore recover exactly the lines of H, which determine H. In particular the induced module is nonprojective. For a fixed H, restricting back to H gives [E:H] copies of M_t, so Krull–Schmidt also recovers t. This proves all symbols I(H,t) are different actual indecomposable coordinates before invoking a lattice algebra.

As a further arbitrary-field check, for an endotrivial core the stable endomorphism algebra is k. The ideal of maps factoring through projectives is contained in the radical of its local endomorphism algebra: a unit factoring through a projective would make the core projective. Its quotient is k, so this ideal equals the radical. After any field extension its tensor extension is still nilpotent with field quotient, proving absolute indecomposability of this core. This is a verification of the field boundary, not an added assumption in the induction proof. The directly credited gamma theorem already supports the required field generality.

## Multiplication, duality and completion

The tensor induction identity and abelian Mackey decomposition give [E:HK] copies of induction from L=H∩K of the restricted tensor product. If L is nontrivial, its core has class res_L(t)res_L(s); the other terms induce to E-projectives. If L=1, the entire induced term is projective. Writing a_H=[E:H] and b_(H,t)=[I(H,t)]/a_H, the equality

    [E:HK][E:L]=[E:H][E:K]

gives coefficient one in the stable multiplication. Induction commutes with finite-group duality, and duality inverts t. The norm of a sum of b-coordinates is exactly sum |c_(H,t)|w_H(t), w_H(t)=dim M_t, because actual injectivity has already been proved.

For e_H=b_(H,1), e_1=0 and e_H e_K=e_(H∩K). The finite nontrivial-subgroup zeta matrix is injective on their coordinate span. Möbius inversion produces self-adjoint, orthogonal, nonzero p_H summing to the unit. It follows that p_H b_(K,s) is zero unless H≤K, and otherwise equals p_H b_(H,res_H(s)). This is an exact statement inside the actual coordinate algebra.

For the block map Phi_H(delta_t)=p_H b_(H,t), expansion gives

    Phi_H(delta_t)=sum_(1!=L<=H) mu(L,H)b_(L,res_L(t)).

The leading H-coordinate is precisely delta_t. Therefore, on finite supports,

    ||f||_(l1(w_H)) <= ||Phi_H f|| <= C_H ||f||_(l1(w_H)),
    C_H=sum_(1!=L<=H)|mu(L,H)|.

The upper bound uses w_L(res_L(t))≤w_H(t); restricting keeps the vector-space dimension and taking the endotrivial core can only remove summands. Lower-level collisions reduce a triangle-inequality upper bound and cannot touch the leading coordinates. This is the decisive norm check. Extension to the weighted l1 completion is bounded below and has closed range. Projected generators lie in the range and are dense in p_H B, so the closed range is all of p_H B. The inverse has norm at most one on that block. Combining the finitely many blocks yields a Banach *-isomorphism, with forward norm at most max C_H and inverse norm at most sum C_H. There is no passage from an algebraic bijection to an unjustified completed bijection.

## Characters, symmetry and the full factor

For every t, the credited gamma theorem gives w_H(t^n)^(1/n)→1, including t inverse. A character of the completed weighted group algebra has |chi(t)|^n≤w_H(t^n); positive and inverse powers force |chi(t)|=1. Conversely any unitary group homomorphism extends by absolutely convergent Fourier sums since all weights are at least one. This argument does not require finite generation of T(H) or character extension from a subalgebra. Every character is Hermitian; evaluating x*x gives |s(x)|² and hence nonnegative spectrum. The finite product is symmetric. Its character on b_(K,t) vanishes unless H≤K and otherwise equals chi(res_H(t)); on I(K,t) it is multiplied by a_K. The normalization is essential to the dimension bound.

For the full p-group completion, e=[kE]/|E| is a self-adjoint norm-one idempotent; e[M]=dim(M)e. The projective ideal is exactly Ce because kE is local and every finite projective is free. The stable inverse is Jx=(1-e)x=x-D(x)e for the canonical nonprojective representative. Disjoint supports give the exact norm ||Jx||=||x||+|D(x)|, between ||x|| and 2||x||. D on the stable coordinate space is merely bounded linear; it is not multiplicative. The factor units are e and 1-e. Thus the specified full coordinate span is Ce×J(B), proving its intrinsic symmetry. No equality of its spectra with ambient subalgebra spectra is asserted.

## Proper-family witness and boundary cases

The F8 module for E=C2³ is a genuine two-dimensional representation: the three generator actions are 1+J, 1+zJ, 1+z²J, with J²=0. All nonidentity group elements have nonzero coefficient of J because 1,z,z² are independent over F2. Each ordinary C2 restriction is therefore free. Its endomorphism algebra is the local algebra F8[J], so it is indecomposable, while dimension two excludes free projectivity over the local algebra kE of dimension eight. Every induced-endotrivial coordinate has at least one nonprojective ordinary cyclic restriction. Hence this module is absent, with no unnoticed coincidence or multiplicity. An absent basis coordinate has distance exactly two from the closed span in the full Green norm.

Being free on ordinary cyclic subgroups is weaker than Dade's shifted-cyclic projectivity criterion. Here (g_2-1)+z(g_1-1) acts as zero, displaying an omitted shifted direction. This checks consistency rather than producing a non-Hermitian species. For rank one, T(C2) is trivial and T(Cp) has order two for p odd; the formulas retain the correct finite group algebra. The trivial group is excluded from the Turn 5 premise, so the empty nontrivial-subgroup lattice must not be assigned a unit. Uncountable indexing sets cause no analytic problem: weighted l1 elements have countable support and finite sums are dense.

## Reproducibility and independence

The verifier was read before execution and copied into ignored `sources/private_B/`. The Turn 5 author receipt reproduced byte for byte: 51,028 assertions and SHA-256 `c197801636a64210283f727c7be972bd28268230ac1b4f858be1a8d3eae1be95`. That replay is preserved in `AUTHOR_TURN5_REPLAY.json` and bound in `AUTHOR_REPLAY_BINDING.json`.

`independent_controls.py` imports no candidate or historical-review code. Its 176,934 exact assertions pass. Distinct controls include canonical RREF subgroup enumeration and the closed Gaussian-lattice Möbius formula; p=2,3,5,7 and rank-zero/rank-one edges; actual syzygy endotrivial classes with line restrictions that collapse Z to trivial or Z/2, using nonconstant actual syzygy dimensions; finite-support signed rational block lower/upper bounds and both inverse directions; 23 actual matrix inductions of cyclic endotrivial cores; direct cyclic tensor Jordan-rank and projective-multiplicity checks; exact unitary species with normalization-sensitive dimension bounds; a separately coded F8 construction using x³+x²+1; and F8→F64 scalar extension. The `full_stable_norm` controls check the coordinate norm/triangle bound, not multiplicativity of J. The latter is the idempotent-splitting deduction proved above.

The control labels for actual syzygy groups and weights depend on the credited classification and standard minimal resolutions. They are not a numerical proof of classification. Matrix cases check actual module actions and cyclic restrictions; they are not exhaustive tests of module categories. The infinite completed-range proof, all-field representation injection, and character classification are supplied by the written argument above. The independent reconstruction was saved before reading the historical review verdict; incidental PR metadata appeared during an earlier file search and is explicitly not treated as evidence. The later historical-review comparison reveals no disagreement about the scoped claim.

The syzygy dimensions used in the controls are independently checkable. For rank r, tensor the r cyclic resolutions, whose maps alternate x and x^(p-1) (both x for p=2). All maps lie in the augmentation ideal, so the resulting resolution is minimal. Its n-th free rank is beta_n=binomial(n+r-1,r-1). With d_0=1, exactness gives d_(n+1)=p^r beta_n-d_n. Duality gives d_(-n)=d_n. These are the `syzygy_dim` weights. In rank one they reduce to the expected periodic dimensions 1 and p-1, with p=2 giving only 1. This derivation supports the finite dimension controls without importing the author's constant-functor model.

The alternate F8 cubic is also explicitly related to the candidate's field: if z satisfies z³+z²+1=0, then b=z^(-1) satisfies b³+b+1=0. Thus the candidate's coefficient root can map to b. The two coefficient triples (1,z,z²) and (1,b,b²) are F2 bases and differ by a change of generators in GL3(F2). This group automorphism preserves the all-subgroups induced-endotrivial family. The separate cubic controls therefore verify the same invariant proper-family mechanism; the exact candidate actions are checked in the written argument rather than claimed a byte-identical recoding.

A separate adversarial subagent saved its own reconstruction before reading this one, then checked the field inputs, proof, code and control boundaries. It found no mandatory mathematical or wording repair. Its independent 54-assertion control checks cyclic tensor Jordan ranks for p=3,5,7, actual full Green multiplication, the distinct orthogonal factor units, multiplicativity of J on signed rational inputs and its exact norm. These remain finite controls supplementing the written factor proof. See `adversary/INDEPENDENT_RECONSTRUCTION.md`, `adversary/full_split_controls.py` and `adversary/FULL_SPLIT_CONTROLS.json`.

## Mandatory repairs and exact remaining gap

No mandatory mathematical repair is identified for the frozen Turn 5 theorem or its verifier. The source-access qualification is essential: retain the accepted-manuscript qualification, credit the external growth/classification inputs, and do not claim direct inspection of the unavailable Dade 1978/Carlson 1981 original proofs or the final 2024 publisher PDF.

The strongest verified claim is intrinsic symmetry of the actual induced-endotrivial closed span for all elementary abelian E over arbitrary characteristic-p k, with a bounded completed Möbius decomposition and its full/projective extension. The exact original gap is control of bounded species on the other actual indecomposable directions. The F8 example proves this family can be proper. Hermitian restrictions to it do not establish that an ambient species is Hermitian everywhere, and the example itself does not exhibit a non-Hermitian species. No new author turn, original-problem solution, or novelty claim is added.

Final audit checkpoint UTC: 2026-10-03T02:19:04.061192+00:00. Completion estimate: 100% of this verification family; no additional universal-discovery completion certified. Reproduce bindings and both fresh control receipts with `python3 verify_review.py` from this folder. The separate final adversarial report is `adversary/REPORT.md`.
