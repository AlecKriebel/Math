# Étale maps of Green and Tambara functors: source and proof gate

Audit date: 21 October 2026. Scope: the original question “What is an étale map of Green or Tambara functors?”, and the lifting-versus-flatness question in the public AIM workshop report, §4, p. 3. This is an independently authored mathematical audit, not a claim of new priority or a resolution of the whole equivariant geometry programme.

## Outcome

There is an established discrete definition: flatness for the relative Mackey box product, vanishing of the relevant differentials, and finite presentation. Hill supplies the genuine Tambara differential framework; Wisdom explicitly uses the finite-presentation refinement. This definition must not be confused with the unique-lifting condition alone.

Ferudun's 18 October 2026 unrefereed preprint gives a valid scoped negative answer to lifting-implies-flatness. We independently checked the construction and proof below. The construction is a known ghost map, credited to Chan–Mehrle–Quigley–Spitz–Van Niel, not a new construction of this audit. The claimed finite computational test count in the preprint has not been reproduced and is not used here.

An apparent remaining gap concerning preservation of finite presentation by constantization is NOT an open target: Schuchardt–Spitz–Wisdom, Theorem C / Theorem 4.29, already proves preservation of compact morphisms. Combining that result with the elementary arguments below gives the full constant-functor test in every characteristic. No novelty is claimed for this combination.

## 1. Exact category and example

Fix a nonzero commutative ring k with 2=0 and G=C2. Write top for G/G and bottom for G/e. Let C=c_G(k), with restriction the identity, transfer zero, trivial Weyl action, and norm a↦a². Define S by top ring k×k, bottom ring k, restriction (a,b)↦a, zero transfer, trivial Weyl action, and norm a↦(a²,a²). The structural map C→S is diagonal at top and identity at bottom.

All C2 Tambara-pair identities hold. Restriction after transfer is zero, equal to the Weyl trace because 2=0. Restriction after norm is squaring, the Weyl product. Norm multiplicativity follows from multiplication in k. The additive norm reciprocity formula reduces to (a+b)²=a²+b² since transfer is zero. Frobenius reciprocity is immediate. Norms preserve zero and one. Thus this is a complete Tambara map, not merely a Green map with an informal candidate norm.

## 2. Presentation and lifting audit

For any commutative Green C-algebra U, a C-algebra morphism from S is determined by the image u of (0,1). The necessary and sufficient conditions are u²=u and res(u)=0. Given u, the top component is

f(a,b)=α(a)+(α(b)-α(a))u,

where α is the base map; the bottom component is forced by α. Orthogonal idempotents u and 1-u establish multiplicativity. Restriction compatibility follows from res(u)=0, and transfer compatibility follows because all bottom elements in S come from the base.

For Tambara targets, no additional equation is missing: every bottom element a is a base element, so its target norm is already α(a²), which is the image of the diagonal pair (a²,a²). This proves the same representing property in the complete Tambara category. A single top generator and the two displayed equations yield finite presentation; equivalently, the represented functor commutes with filtered colimits computed orbitwise.

Now let U→V be a levelwise surjection with square-zero kernel, and let v be the idempotent describing a morphism S→V. Choose a top lift x. The element x²-x lies in the kernel, so x⁴-x²=(x²-x)²=0. Consequently x² is an idempotent lifting v. Its restriction is an idempotent in a square-zero ideal and is therefore zero. If two idempotent lifts differ by j in the kernel, then (u+j)²=u² in characteristic two, forcing j=0. This proves existence and uniqueness in both categories. The argument even works for a nilpotent kernel, using a sufficiently large 2-power.

This is an ordinary, algebraic lifting assertion about the stated surjections. It is not a theorem identifying a spectral cotangent complex or every conceivable derived square-zero notion.

## 3. Nonflatness audit on all Mackey modules

For a k-module Q, let D(Q) be the C-module supported only at top, with value Q there. Set D=D(k). Let E have value k at both levels, zero restriction, identity transfer, and trivial Weyl action. Both are valid C-modules: the Mackey trace relation is zero in characteristic two, and the C-module cohomological relation tr res=2 also holds. The map j:D→E is the identity at top and zero at bottom, hence a monomorphism.

For every C-module M, balanced Mackey pairings out of D and M have zero bottom component. Their top component is a k-linear map out of M_top; the transfer relation forces it to kill tr(M_bottom), and restriction forces its image to have zero restriction. Conversely these conditions give a balanced pairing. Therefore the universal property yields

D box_C M = D(M_top / tr(M_bottom)).

In particular D box_C D=D and D box_C E=0. The underlying C-module of S is C⊕D, by separating (a,b) into (a,a)+(0,b-a). Tensoring j with S is consequently the map

D⊕D → E,  (d1,d2) ↦ j(d1).

Its kernel is the nonzero second D. Thus S is not C-flat. This obstruction tests genuine nonconstant modules; evaluating ordinary orbit rings could not detect it.

The C⊕D splitting is only a module splitting. D is not asserted to be a nonzero top-supported unital Tambara factor. In particular, norms of the bottom unit would forbid such a factor.

## 4. Differentials and limitations

Every C-relative Green derivation on S vanishes at bottom, where the map is the base map. At top it vanishes on the diagonal and on the idempotent: d(u)=d(u²)=2u d(u)=0. Thus the Green differential module vanishes. Genuine Tambara differentials are a quotient and also vanish. The orbit maps are the identity and k→k×k, both finite étale ordinary ring maps.

The example therefore rules out each implication “unique infinitesimal lifting implies box-flatness” and “orbitwise finite étale implies box-flatness,” even with finite presentation and complete norms. It does NOT contradict a definition that already requires flatness. It does NOT settle the workshop's separate diagonal question, general étale sites, or the spectral comparison problem. Extending the SAME counterexample from Green to complete Tambara works for the concrete base-element reason above; it does not justify extending arbitrary Green counterexamples by merely declaring norms.

## 5. Constant-functor test, with the missing prior theorem restored

For a finite group G and ring map A→B, let c_G denote the constant cohomological Tambara functor. As Mackey modules it preserves sums, cokernels, and filtered colimits. Applying a free A-module presentation proves

c_G(M) box_{c_G(A)} c_G(N) = c_G(M tensor_A N).

In fact the same argument gives c_G(M) box_{c_G(A)} X orbitwise M tensor_A X(G/H), with the induced Mackey structure, for any c_G(A)-module X. Taking M=B and using Lazard's filtered-free characterization shows that A-flatness of B implies box-flatness of c_G(B). The converse follows by testing injections between constant modules and evaluating at G/e. This uses no inversion of |G|.

The relative product of two constant algebras is c_G(B tensor_A B); the standard constant tensor identity of Lindenstrauss–Richter–Zou also supplies this identification. Put J=ker(B tensor_A B→B). The Green differential quotient is the constant J/J². Genuine decomposables contain the pointwise product ideal; their value at the free orbit is exactly J², since there is no proper subgroup below e and restrictions of higher norm decomposables are products of at least two ideal elements. Thus ordinary, Green, and genuine Tambara differential vanishing are equivalent for these constant maps.

Finite presentation is reflected: constantization is fully faithful and preserves filtered colimits, so compactness of c_G(B) among c_G(A)-algebras implies compactness of B among A-algebras. Preservation, which cannot be inferred just from orbitwise finite presentation, is supplied by the already existing Schuchardt–Spitz–Wisdom theorem. Consequently

c_G(A)→c_G(B) is Tambara-étale if and only if A→B is classically étale.

Here both notions include finite presentation and flatness. Without finite presentation, the equivalence is instead between Hill's flat-plus-zero-differentials condition and ordinary flatness plus zero differentials. For example, c_G(F_p)→c_G(algebraic closure of F_p) meets that condition but is not finitely presented, since an algebraic field extension of finite type is finite. This elementary boundary example is not assigned novelty.

## 6. Residual-target gate

Five distinct mathematical checks were completed: (1) the precise definitions and their hypotheses; (2) the represented-point lifting argument; (3) the tensor obstruction on nonconstant modules; (4) constant flatness and differential detection; and (5) finite-presentation preservation and reflection. These are audit routes, not five new discoveries or five invented substitutes for the original problem.

The original question is broad and definitional. The public report contains several separate geometric questions, but the lifting implication is now answered negatively by existing work, while the constant finite-presentation gap is already answered by older literature. No single additional unsolved theorem is specified by the original question. It would be inappropriate to silently replace it with an arbitrary general spectral equivalence or diagonal theorem and claim to have completed five approaches to that replacement. The appropriate gate is: established discrete answer plus independently checked prior scoped counterexample; no certified new solution of the broader programme. Further work needs an explicitly selected residual statement and precise definitions.

## Public sources and inspected metadata

- AIM, Equivariant derived algebraic geometry, public workshop report, §4, pp. 3–4: https://aimath.org/pastworkshops/equideralggeomrep.pdf . Inspected local PDF: 112321 bytes, SHA256 4cbf3d072269bdfb8327051686cb50d44255029e975480180f3db8ed7c529c54.
- Alper Ferudun, Infinitesimal Lifting Does Not Imply Flatness for Green Functors, 18 October 2026, explicitly unrefereed: https://eulersolve.org/papers/aim-algebraic-geometry-0162/ . Inspected PDF: 75304 bytes, SHA256 ff5da79fd9cb915a8fe04358eb451bd6198df067be0d417900eaf3f9b3339c8d. Public search indexing confirmed the scoped claim on 21 October; direct web opening failed, so no fresh successful download is claimed.
- Michael A. Hill, On the André–Quillen homology of Tambara functors: https://arxiv.org/abs/1701.06219 .
- Ayelet Lindenstrauss, Birgit Richter, Foling Zou, Examples of étale extensions of Green functors: https://arxiv.org/abs/2304.01656 .
- Noah Wisdom, Affine étale group schemes over Tambara fields, version 2, Definitions 2.10 and 2.13: https://arxiv.org/html/2508.09365v2 . Theorem 5.4 has additional hypotheses; it is not a blanket orbitwise criterion.
- Jason Schuchardt, Ben Spitz, Noah Wisdom, Algebraically Closed Fields in Equivariant Algebra, Theorem C / 4.29: https://arxiv.org/abs/2505.05539 . The May 2025 author PDF was inspected, including theorem and proof on printed p. 24: https://www.math.ucla.edu/~jasonsch/pdfs/Schuchardt,%20Spitz,%20Wisdom%20-%20Algebraically%20Closed%20Fields%20in%20Equivariant%20Algebra.pdf .
- David Chan, David Mehrle, J. D. Quigley, Ben Spitz, David Van Niel, On the Tambara Affine Line: https://arxiv.org/abs/2410.23052 . This is the credited source of the ghost construction, not a priority claim for this audit.

This report includes authored mathematical reasoning and public bibliographic metadata only. It does not distribute third-party source PDFs or private records. The verification is a human-readable mathematical audit, not proof-assistant certification.
