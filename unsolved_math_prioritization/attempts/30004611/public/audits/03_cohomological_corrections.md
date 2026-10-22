# Independent audit of the cohomological corrections

14 October 2026 UTC. Row 1775 / 30004611, the same shared mathematical pass 2. This is an independent proof check of the frozen authored component, not an additional mathematical approach, a novelty certificate, or a full solution of the source problem. The audited source file was not modified.

## 1. Frozen artifact and verdict

Audited artifact: `cohomological_corrections.md`.

- Bytes: 8,680.
- SHA-256: `abff68797e812d7f3969abdd51628c12dda74fd89ad5d5ff0ff0ac3d27adf505`.

**Qualified mathematical acceptance.** No correction is required to the splitting criterion, normal-sequence cohomology comparison, defect-support vanishing bound, high-degree image/target comparison, or center-punctured coloop-deletion product formula. The stated exclusions are essential: these results neither make the two restriction maps universally surjective nor give an unrestricted addition-deletion or freeness criterion. In particular no independent mathematical acceptance of the source paper's other comparison or freeness theorems is implied.

The audit read the accepted pass-1 common-poset construction, its independent audit, the full restriction-defect report, and the source-verification record. The essential/nonessential deletion convention and the one-dimensional restriction boundary were checked against those definitions. The cohomological proofs below use only finite-poset sheaf theory, the explicitly proved rank-two restriction calculation, and elementary arrangement algebra.

## 2. Splitting of normal evaluation

Let P be the nonzero flats of the essential arrangement A, with inclusion order; write Q for its flats lying in H=ker(alpha), and I for the ideal-valued functor equal to alpha S on Q and S elsewhere. The normal sequence is

0 -> E -> D -> I -> 0.

At the top flat V, a sheaf splitting gives theta=sigma_V(1) with theta(alpha)=1. Every deletion hyperplane L is a nonzero flat outside H: distinct hyperplanes cannot contain one another, and dim V>=2 ensures L is retained in P. Naturality along L -> V therefore forces this same theta to belong to D(A_L), hence to be tangent to L. Intersecting these conditions gives theta in D(A').

Taking coefficient-degree zero is valid over any field because all logarithmic divisibility conditions are homogeneous. The resulting constant vector v lies in every deletion hyperplane, and alpha(v)=1. Essentiality gives T' intersect H=0, so the nonzero deletion center T' is a line. This is exactly the marked-coloop condition.

Conversely, for v in T' normalized by alpha(v)=1, the map f -> f partial_v is logarithmic away from H, and on Q the ideal membership f in alpha S supplies tangency to H. It is compatible with all arrows because the same polynomial derivation is used everywhere. Evaluation sends it back to f. This proves the claimed equivalence even for ungraded splittings; the constructed coloop splitting also preserves coefficient degree.

The distinction from local Euler splittings is correct. The latter exist on Q but supply no global sheaf splitting in the non-coloop case.

## 3. Acyclicity and the positive-degree comparison

The exact sequence 0 -> I -> S_P -> i_*R_Q -> 0 uses constant functors and the closed lower-ideal inclusion i:Q -> P. Both P and Q have maxima, so their order complexes are cones. Consequently the constant-functor cohomologies are S and R in degree zero and zero above degree zero. This is a claim about constant coefficients, not a claim that a maximum makes every sheaf acyclic.

For the closed inclusion, extension by zero is exact and preserves cohomology. The global map S -> R is the ordinary surjective quotient. Thus the long exact sequence gives Gamma(I)=alpha S and H^k(P,I)=0 for k>0.

The global Euler derivation is present at every stalk. Sending alpha f to f times Euler splits Gamma(D) -> alpha S. The possible connecting map Gamma(I) -> H^1(E) is therefore zero. Hence E -> D induces an isomorphism in degree one as well as in every higher degree. Omitting this global surjectivity check would not justify the degree-one assertion; the frozen proof includes it correctly. The global splitting preserves coefficient grading and is not confused with a sheaf splitting.

## 4. Defect support and the exact range

The pass-1 rank-two calculation establishes both ordinary and Ziegler surjectivity at every localization of rank at most two, over every field. Since rank(A_X)=codim_V(X), either defect vanishes outside

W={X in Q: 1<=dim X<=ell-3}.

This is a lower ideal of P. A chain in W has at most ell-3 vertices, hence dimension at most ell-4. For ell<=3, W is empty and the defects are zero.

For a covariant functor F, the normalized finite-poset cochain complex computing derived global sections is

C^n(P,F)= product over x_0<...<x_n of F(x_n).

With a conventional alternating-sign choice, its differential on a chain x_0<...<x_(n+1) is the sum of the omitted-vertex values for vertices 0 through n, followed by (-1)^(n+1) times the transition F(x_n -> x_(n+1)) applied to the value on x_0<...<x_n. In degree zero it imposes precisely the section compatibility equation. Thus the last-vertex convention in the frozen proof is correct.

If F vanishes off W, a nonzero cochain summand must end in W. Lower-closedness then places every vertex in W. Consequently this is exactly the cochain complex of F restricted to W, and it has no terms above ell-4. This verifies H^k(P,C)=0 for k>ell-4 for either defect C. The argument concerns poset-chain dimension; no module-codimension estimate is substituted for it.

For 0 -> J -> Tbar -> C -> 0, the exact segment is

H^(k-1)(C) -> H^k(J) -> H^k(Tbar) -> H^k(C).

It yields a surjection at k=ell-3 and an isomorphism at k>=ell-2. The frozen report correctly preserves the possible boundary contribution H^(ell-4)(C) -> H^(ell-3)(J), rather than claiming an unjustified restriction-valued connecting map in that degree. At ell=4 the defects are on discrete one-dimensional flats; positive defect cohomology vanishes, while degree-zero defects can remain. All indices agree with the companion tangency-complex report.

## 5. The actual center-punctured deletion

For a marked coloop, V=H direct-sum T', dim T'=1, and restriction gives a bijection from deletion hyperplanes to the hyperplanes of B=A^H. Two distinct deletion hyperplanes cannot acquire the same restriction, since each is the direct sum of that restriction and T'. Their intersections give the intrinsic poset isomorphism

Q -> L(A') minus {T'},  Y -> Y direct-sum T'.

After choosing v in T' with alpha(v)=1, all deletion equations are independent of alpha and S=R[alpha]. At the corresponding stalk, coefficient expansion in alpha identifies the derivations tangent to these equations with

(S tensor_R D(B_Y)) direct-sum S partial_v.

This identification commutes with the derivation inclusions. Scalar extension commutes with the finite cochain products, and it is flat, so it commutes with cohomology. The second summand is constant on Q and acyclic in positive degree. The displayed degree-zero and positive-degree cohomology formulas are therefore correct. The poset identification is intrinsic; the direct-sum expression uses the chosen product coordinate, as the frozen report explicitly says.

The retained-center deletion poset instead has a minimum and is acyclic for every sheaf, because global sections are evaluation at that minimum. It is not silently identified with the center-punctured source convention.

For ell=2, Q has the single point H and the restriction's removed zero flat carries the missing logarithmic condition. Thus Gamma(Q,D_B)=Der_K(R), generally not the full module D(B). The frozen formula and its explicit boundary qualification remain valid.

## 6. Acceptance limits

The artifact's four substantive conclusions are accepted in the stated category over arbitrary fields. Its normal-sequence positive-degree comparison can be used to express the companion Ziegler construction in terms of actual arrangement-sheaf cohomology. Its support bound justifies the companion's high-degree exact tail. Neither result removes lower-degree defect corrections.
