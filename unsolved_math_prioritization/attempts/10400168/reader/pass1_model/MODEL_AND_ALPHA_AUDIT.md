# PASS1 model and α-induction coverage

Date: 14 October 2026 UTC. This is one lane of the shared PASS1. No publication or repository action was performed.

## Result in brief

1. A compatible **based restriction of complete spherical state-sum data** gives exactly a full spherical fusion-subcategory inclusion over C, with the original associator, duality, pivotal structure and retained simple dimensions. This statement is proved below without positivity, C*-realizability, pseudo-unitarity, braiding or modularity.
2. The historical exposition itself is not a complete list of numerical axioms. Its categorical Barrett–Westbury interpretation is covered. It is not legitimate to infer a spherical categorification from a fusion multiplication table plus the names of three unspecified equations, or from an arbitrary linear subalgebra. This is a source-interpretation boundary, not a newly identified open mathematical problem.
3. The actual BEK systems supply full spherical inclusions: ambichiral into chiral, chiral into the full α-system, the full α-system into the M–M system, and the corresponding subsystem inclusions. These are covered even with degenerate braiding. The α-induction functor from the original N–N category is generally **not** fully faithful and is not the inclusion to which the restricted-regular-interface theorem should be applied.
4. The cited Kirillov–Ostrik model supplies a nonunitary branch: for their rigid commutative algebra A of trivial twist in a finite semisimple ribbon category B, the inclusion Rep^0(A) → Rep(A) is full spherical, with dimensions d_A(X)=d_B(X)/d_B(A). This uses no invertible S-matrix.
5. A universal inclusion-dependent interface supplies a uniform defect-functor relation for these specified inclusions. It does not compute their centers, identify their modular data, make α fully faithful, prove a product formula for a singular braided category, or supersede BEK's or Sato's more explicit results.

## 1. What the historical source does and does not specify

Ohtsuki, Sections 9.1–9.2, printed pp. 506–510 (PDF pp. 134–138), works over C with finitely many simple labels, multiplicity spaces H_ij^k, recoupling matrices, dimensions μ_i, and a state sum with one factor w^{-1} per vertex, where w=Σ_i μ_i². The fusion algebra is the complex span of the **specified simple-object basis**. The recoupling entries compare the two decompositions of Hom(V_l,V_i⊗V_j⊗V_k).

The exposition calls 6j-symbols solutions of tetrahedral-symmetry, unitarity and pentagon equations, but does not write those equations, supply their complete orientation conventions, or separately list the unit, duality and pivotal axioms. It refers to monoidal categories with additional properties and to the Barrett–Westbury construction [41]. Positivity appears as a conditional hypothesis for realizing numerical data by subfactors on p. 507. It is therefore not a universal hypothesis of Problem 9.4.

The sound coverage statement is:

> We use the finite semisimple spherical, oriented Barrett–Westbury interpretation of the admissible state-sum input cited by the source, and retain all of its numerical and pivotal data. Every compatible based restriction of such data is covered. No claim is made about arbitrary bare arrays that satisfy an unspecified subset of the historical equations.

This does not restrict the theorem to unitary categories. Barrett–Westbury's categorical input is spherical and need not be braided. For quantum-group constructions that use a negligible-morphism quotient, C is the finite semisimple spherical category on which the given state sum is actually defined, not the entire unreduced representation category. The label restriction is taken in that same category; no different quotient or associator is substituted. Turaev–Virelizier's Appendix exhibits oriented tetrahedral 6j-tensors with the Biedenharn–Elliott and orthonormality identities for spherical categories. An algebraic orthonormality identity must not silently be replaced by positivity of a Hermitian form. Conversely, this audit does not assert that every spherical category has a choice of scalar symbols satisfying every possible literal convention intended by the word “unitarity.” The relevant comparison is through the complete oriented spherical state-sum data, including duality pairings and gauge conventions.

Sources: [historical model and target](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=134); [Barrett–Westbury, Definitions 2.1–2.13 and Theorem 5.1](https://arxiv.org/pdf/hep-th/9311155v3); [Turaev–Virelizier, §§1–5 and Appendix](https://arxiv.org/pdf/1006.3501v5).

## 2. Exact reconstruction and restriction proposition

### 2.1 Complete numerical input

A concrete sufficient formulation of the complete data is:

- A finite set I, a distinguished tensor-unit label 0, a dual-label involution i↦i*, and finite-dimensional complex multiplicity spaces H_ij^k.
- Unit multiplicities H_0i^k and H_i0^k identified with C for k=i and zero otherwise. Distinct labels represent nonisomorphic absolutely simple objects.
- Invertible recoupling maps between ⊕_m H_ij^m⊗H_mk^l and ⊕_n H_jk^n⊗H_in^l, with compatible unitors, satisfying the pentagon and triangle identities. If the supplied W-symbols are normalized tetrahedral weights rather than raw associator entries, the specified duality pairings and normalization convert between them; one must use that specified conversion.
- Evaluation and coevaluation maps for i and i*, compatible with the recoupling data and satisfying both snake identities.
- Compatible pivotal data, equivalently compatible left/right dualities, whose left and right categorical traces agree. The edge weight μ_i is the resulting spherical dimension d_i, and tetrahedral weights are those obtained from these same data.

These requirements make explicit what “complete spherical state-sum data” means. They are not quotations of an axiom list printed in the problem. One cannot omit the last two bullets and claim a proof that every finite semisimple monoidal category has the needed spherical structure.

### 2.2 Reconstruction

Let C be the category of finite I-graded complex vector spaces X=(X_i), with

Hom_C(X,Y)=⊕_i Hom_C(X_i,Y_i),

and define

(X⊗Y)_k=⊕_{i,j} X_i⊗Y_j⊗H_ij^k.

The given recoupling maps define the associator, extended by linearity and the ordinary vector-space tensor identifications. Their pentagon and unit identities are precisely the coherence identities for C. The object supported at 0 with value C is the tensor unit. The objects supported at a single i with value C form the simple objects. Every object is a finite sum of these, all morphism spaces are finite dimensional, and the unit is simple.

Extend the supplied dualities and pivotal maps to direct sums and tensor products using their given coherence. The snake identities make C rigid; the pivotal compatibility makes it pivotal; equality of traces on simples gives equality of traces on all endomorphisms by block decomposition. Thus C is spherical fusion. By construction its H-spaces, associator matrices, duality/pivotal data, and W-symbols in the chosen gauges are the original ones. This construction does not replace the associator by a different categorification of the same ring.

If the data originally came from a spherical fusion category rather than a chosen skeleton, the functor (X_i)↦⊕_i X_i⊗V_i, with the given decompositions V_i⊗V_j≅⊕_k H_ij^k⊗V_k, is a spherical monoidal equivalence. The displayed construction is then merely a choice of coordinates.

### 2.3 Based restriction

Let J⊆I satisfy:

- 0∈J;
- i∈J implies i*∈J;
- i,j∈J and H_ij^k≠0 imply k∈J.

Retain the **entire** spaces H_ij^k for i,j,k∈J and the original recoupling, duality and pivotal data on them. Let D be the full subcategory of C consisting of objects whose support is contained in J.

Then D is closed under finite sums and summands, has the same tensor unit, and is closed under tensor products and duals. The associator, unitors, evaluations, coevaluations and pivotal isomorphisms have their sources and targets in D and are morphisms of D because it is full. All their identities remain true. The trace of any D-endomorphism is calculated by exactly the same diagram in D and C, so D is spherical and the inclusion preserves the spherical structure. Every simple of D is one of the retained simples of C; no simple is split or replaced by a linear combination.

In associator coordinates, every intermediate label for a tensor product of retained labels is again in J. Consequently the original recoupling maps restrict to full isomorphisms, and their coherence equations have no missing summands. Tetrahedral weights are the restricted weights. Conversely, every replete full fusion subcategory with the inherited spherical structure is obtained in this way by taking its simple labels. This proves the exact correspondence at the stated level of data.

### 2.4 Why an arbitrary algebra subspace is not enough

In K_0(Vec_{Z/3})⊗C=C[g]/(g³−1), the subspace span_C{1,g+g²} is a unital algebra: if s=g+g², then s²=2+s. It is not spanned by a subset of the original three simple labels. Treating s as a retained simple would replace the object g⊕g², whose endomorphism algebra is C⊕C, by a fictitious simple. Moreover the coefficient of 1 in s² is 2, incompatible with a self-dual simple in a fusion category. Thus this subalgebra does not define the proposed restriction of the original simple-label 6j-data.

Similarly, restricting to a proper subspace of a retained multiplicity space is not the full-subcategory construction. Such an operation needs additional tensor-category data and coherence checks; none is inferred merely from multiplication closure of a vector subspace.

## 3. Dimensions, pairings and original normalization

For every simple i of a pivotal fusion category, d_l(i) and d_r(i) are nonzero. One elementary reason is that Hom(i*⊗i,1) and Hom(1,i*⊗i) are one dimensional, and their nonzero evaluation/coevaluation maps are nonzero scalar multiples of a projection/inclusion for the unit summand. Their composite is therefore nonzero. Turaev–Virelizier Lemma 4.1 proves this precisely and also proves nondegeneracy of the categorical pairings.

Over the algebraically closed field C of characteristic zero, the global dimension is nonzero: Turaev–Virelizier §4.2 invokes the ENO theorem for dim(C)=Σ_i d_l(i)d_r(i); for a spherical category this is Σ_i d_i². Apply the same theorem separately to D. Thus neither nonzero simple dimensions nor nonzero global dimension impose an extra positivity/unitarity restriction in the declared model. The sum Σ_i d_i² is the categorical global dimension, not an arbitrarily substituted Frobenius–Perron dimension.

The two theories use

w_C=Σ_{i∈I}d_i²,   w_D=Σ_{j∈J}d_j²,

respectively. The edge dimensions of retained labels agree, while the vertex factors differ. The D state sum is the sum over retained labelings with w_D^{-v}; it is not simply the retained-label portion of the C state sum with w_C^{-v}. Boundary normalizations and cylinder-projector images must likewise be taken from the relevant theory. The interface does not turn the raw inclusion of labeling spaces into an asserted inclusion of physical state spaces.

**Source normalization discrepancy.** Ohtsuki p. 510 describes the untwisted finite-group invariant as the number of conjugacy classes of representations. The normalized state sum with w=|G| instead gives |Hom(π_1(M),G)|/|G| for connected closed M. For example on S³ the two expressions are 1 and 1/|G|. The defining state sum and the modern TVBW normalization must govern the comparison; the prose sentence cannot be used to require the incompatible unweighted count. This is an identified source discrepancy, not an adjustment hidden in the comparison theorem.

## 4. Actual α-induction input and inclusions

### 4.1 BEK's operator-algebraic model

Use BEK's original notation to avoid confusing three different categories. Assumption 2.1 fixes a type III subfactor N⊂M, a finite braided N–N system X_N, and a subsystem Y_N⊆X_N such that the dual canonical endomorphism θ=bar(ι)ι belongs to the finite-sum closure of Y_N. Here ι:N→M is the inclusion. The actual extra object is the canonical **Q-system** on θ supplied by this extension, not θ as a bare object.

In categorical language, a Q-system is a special C*-Frobenius algebra (A,m,u): m is associative and unital, Δ=m* and ε=u*, the Frobenius identities hold, and mm* is a positive scalar multiple of id_A. The standard choice is determined by standard solutions of the conjugate equations. This is the positive operator-algebraic branch; its positivity is supplied by this branch, not assumed for the general problem. Commutativity/locality is additional and is not required in BEK's general setup. A haploid/connected Q-system corresponds to an irreducible inclusion; Assumption 2.1 does not explicitly impose irreducibility, so haploidity must not be silently added here.

The induced endomorphisms are

α^±_λ=bar(ι)^{-1} Ad(ε^±(λ,θ)) λ bar(ι).

They preserve products and the unit, and have d(α^±_λ)=d(λ). BEK p. 5 nevertheless gives only the chain

Hom(λ,μ)⊆Hom(α^±_λ,α^±_μ)⊆Hom(ιλ,ιμ).

The first inclusion need not be equality. Simple inputs may split or become equivalent after induction. Therefore α^± is not, in general, the embedding of the original braided category into a fusion subcategory.

BEK p. 6 defines:

- X_M: the irreducible subsectors of ι λ bar(ι), for λ∈X_N;
- X_M^±: the irreducible subsectors of α^±_λ;
- X_M^α: the irreducible subsectors of α^+_λ α^-_μ;
- X_M^0=X_M^+∩X_M^-: the ambichiral system.

The precise chains are

X_M^0⊆X_M^±⊆X_M^α⊆X_M,

and the analogous Y-system chains, together with Y_M^s⊆X_M^s for s=0,+,−,α and for the whole M–M system. Take finite direct sums, subobjects and all intertwiners to obtain the associated full tensor categories. BEK p. 15 explicitly identifies such finite systems with rigid C*-tensor categories. Their standard statistical trace supplies the spherical structure; subcategories retain the same dimensions and standard trace. Every displayed inclusion therefore satisfies the model proposition.

For any selected inclusion D⊆C among these, the candidate interface is the bimodule _D C_C: its underlying category is C, its left D action is tensor product along D→C, and its right C action is the regular tensor-product action, equipped with the trace from C. This matches the shared convention in which it labels the arrow D→C; restricting the other action gives the opposite-direction candidate instead. No inverse S-matrix is involved in selecting this interface. The notation C here names the chosen ambient induced-system category, not automatically the original N–N category.

Sources: [BEK, Assumption 2.1 and pp. 4–6, 15](https://arxiv.org/pdf/math/0002154v1). For the exact modern Q-system terminology and the distinction between haploid and general Q-systems, see [Carpi–Gaudio–Giorgetti–Hillier, Definitions 2.5, 2.7, 2.12, 2.16–2.18](https://doi.org/10.1007/s00220-023-04722-9). Kawahigashi's [2023 paper, §2](https://arxiv.org/pdf/2302.05577v3) independently identifies the same input and explicitly permits local and nonlocal Q-systems and degenerate braiding.

### 4.2 Kirillov–Ostrik's categorical model, without unitarity

Let B be a finite semisimple ribbon category over C with simple unit. In [222], a B-algebra A has associative multiplication and unit, is commutative relative to B's braiding, and satisfies dim Hom_B(1,A)=1 (Definition 1.1). It is “rigid” in their terminology when the pairing e_A=ε_A m is nondegenerate and dim_B(A)≠0, where ε_Au=id_1 (Definition 1.11). Retain the hypothesis θ_A=id_A.

Theorem 1.5 gives a tensor product over A with unit A; Theorem 1.15 gives rigidity; Theorem 1.17 gives the pivotal structure and inherited ribbon structure on local modules; Theorem 3.3 gives semisimplicity. Finiteness follows from Lemma 3.4: every module is a summand of a free module F(V), and there are only finitely many simple V in B. The unit A is simple since End_A(A)≅Hom_B(1,A)=C. Hence Rep(A) is a fusion category.

Theorem 1.18 and Remark 1.19 supply the spherical trace and

d_Rep(A)(X)=d_B(X)/d_B(A).

The local-module category Rep^0(A) is a full tensor subcategory of Rep(A) (Definition 1.8 and Theorem 1.10); its rigidity and pivotal data are inherited by the cited results. It is closed under direct sums and summands, and thus is a full spherical fusion subcategory. These claims occur before the modularity section and do not need nondegeneracy of B's S-matrix.

The required inclusion is therefore

D=Rep^0(A) → C=Rep(A).

It compares the local and all-module TVBW theories, with the above module-category dimensions. It is **not** a literal inclusion Rep(A)⊆B: its tensor product is ⊗_A and its unit is A, so the forgetful functor is not the asserted unit-preserving tensor inclusion into B. Nor is the free-module functor F:B→Rep(A) generally fully faithful. In the local Q-system specializations one can compare these categories with chiral/ambichiral sectors; that identification requires the chosen operator-algebraic/algebra-object correspondence. This report does not conflate the two models merely because both use α-induction terminology.

The special Frobenius description of A is available from its nondegenerate pairing, but the exact hypotheses used here are KO's own rigidity, commutativity, connectedness and trivial-twist hypotheses. No dagger or unitarization is introduced.

Source: [Kirillov–Ostrik, Definitions 1.1/1.8/1.11, Theorems 1.5/1.10/1.15/1.17/1.18/3.3 and Remark 1.19](https://arxiv.org/pdf/math/0101219v3). Their Theorem 4.5, which additionally assumes B modular, proves Rep^0(A) modular. That later assumption is unnecessary for the present inclusion-dependent TVBW interface.

## 5. Singular S and exact prior-art boundary

### BEK

The introduction expressly allows degenerate braiding. Theorem 3.9 gives intertwiner multiplicities for η-extensions associated with the full α-system, using the relative permutant and degenerate subsystem. Theorem 4.6 does the corresponding work for chiral systems and ambichiral branching data. Degeneracy can identify candidates and split fixed points. These theorems are already relevant in singular-S settings.

Corollary 3.10 imposes nondegeneracy of X_N to identify the double of the full M–M system with the product of the original system and its opposite; in this case X_M^α=X_M. Corollary 4.8 similarly identifies the chiral double with the original system times the opposite ambichiral system. They must not be extended by deleting their nondegeneracy hypotheses. A singular S-matrix also must not be assumed invertible in intermediate calculations, and even the normalized S,T notation may require a nonzero Gauss sum in BEK p. 6.

The defect theorem answers a different, weaker-in-information but more uniform, question: what inclusion-dependent topological interface can be attached to any of the specified fusion inclusions? It neither refutes nor replaces the product descriptions and intertwiner formulae. It adds no claim that those product descriptions persist with singular S.

### Sato

The inspected source is arXiv:math/0404509v1, whose file displays a later typesetting date. Its degenerate symmetric center is assumed even, hence identified with Rep(G). Section 4 assumes a minimal nondegenerate extension DeltaHat⊇Delta, with DeltaHat∩Delta'=Delta^d. Proposition 4.2 and Theorem 4.3 impose G abelian. Under these conditions the double is described by a centralizer in DeltaHat⊗DeltaHat^op followed by a categorical crossed product; Section 5 applies this to a surgery formula. Remark 5.4 explicitly distinguishes the proved case from a more general nonabelian claim attributed to Ocneanu.

The inclusion Delta⊆DeltaHat, where supplied, is another spherical inclusion to which the interface construction applies, independently of using Sato's formula. However the interface theorem does not produce a minimal modular extension, prove the even-center or abelian conditions unnecessary for Sato's formula, or calculate the crossed-product double. No version-of-record proof verification is claimed for Sato beyond the previously inspected preprint and journal record.

Sources: [BEK, pp. 15–16 and 19–21](https://arxiv.org/pdf/math/0002154v1); [Sato, pp. 5, 13–17](https://arxiv.org/pdf/math/0404509v1); [Sato journal record](https://doi.org/10.1007/s00220-005-1292-y).

## 6. Precisely usable conclusion for the shared theorem

The source-model part may be accepted in the following form:

> For every admissible finite spherical Barrett–Westbury input over C, and every compatible based restriction retaining the unit, duals, all simple summands and the full multiplicity spaces, let D→C be its reconstructed full spherical inclusion. The restricted regular bimodule construction uses exactly the original data. It covers all BEK full/chiral/ambichiral/subsystem inclusions above and the KO local-module inclusion under the explicit cited hypotheses, without requiring an invertible S-matrix.

The full defect-functor conclusion then depends on the other PASS1 lanes verifying the restricted trace and the application of Carqueville–Müller Theorems 5.18/6.4 and Example 6.5, including normalization and orientation. This lane does not independently certify their proofs.

This is an application of existing categorical constructions. It is a meaningful proposed answer to the qualitative source question under the declared spherical/based interpretation. The source does not specify a unique comparison arrow or demand equivalence, injectivity, or a numerical ratio, and this report introduces no such extra demand. The historical phrase “an object satisfying certain axioms” is implemented by the two actual cited frameworks above, not by a claim that every arbitrary Frobenius object or every linear fusion-algebra subspace automatically defines the same inclusion problem.
