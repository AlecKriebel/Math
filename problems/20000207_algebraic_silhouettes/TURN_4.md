# Turn 4: finite epipolar ambiguity among actual smooth fixed-degree realizations

AI-assisted proof candidate; independent review pending. Fourth author turn. This uses the local smooth-primal theorem of Turn3 to prove a global finite statement for actual realizations in the same fixed-degree parameter family. It does not assert that all solutions of the necessary Kruppa equations are realized in that family.

## 1. Algebraic parameter and data spaces

Fix d>=3 over C. Let T be the irreducible open parameter space of triples (f,P1,P2), where f is a degree-d homogeneous equation defining a smooth surface in P3, P_i are full-rank 3-by-4 projective camera matrices with distinct centers outside the surface, and the two full apparent contours have their generic degrees and ordinary behavior. If needed shrink further to a nonempty open on which their equations depend regularly on the parameters. This is permissible for a generic theorem; no assertion is made for discarded degenerate records.

There is a rational algebraic map D assigning the pair of full contour equations, regarded as points of the appropriate projective coefficient spaces. One algebraic construction is to eliminate the space coordinates from f and the directional polar equation together with the linear projection equations. On the nonempty open where the reduced image is a plane curve of fixed degree d(d-1), its principal equation is unique up to scalar. Its coefficient line therefore varies rationally: over the function field of T perform elimination, choose a nonzero normalization coefficient and clear denominators. The resulting identity specializes correctly on a nonempty open; further shrink excludes vanishing leading coefficients and degree drops. This gives the asserted regular map on an irreducible open. This is algebraic contour data, with no clipping or metric fitting.

There is also a regular map F:T -> P8 on this open, assigning the rank-two fundamental matrix up to scalar. The matrix follows rationally from the camera matrices by linear algebra; denominator-nonzero charts cover the generic case.

Let Y be the closure of D(T) and Z the closure of (D,F)(T) in the product of the contour coefficient space and P8. Both are irreducible. Projection p:Z -> Y is dominant.

## 2. Relative differential criterion

For completeness, the algebraic principle used here is the following.

**Lemma (characteristic-zero finite-image criterion).** Let T be an irreducible complex variety and D:T -> Y, F:T -> W be morphisms. Suppose at a general smooth point t of T every tangent vector v with dD_t(v)=0 also satisfies dF_t(v)=0. Then dim closure((D,F)(T))=dim closure(D(T)). Consequently the projection between these image closures is generically finite. For general y in the data image, only finitely many F-values occur among all t in T with D(t)=y.

Proof. In characteristic zero the generic rank of a morphism's differential equals the dimension of its image, since the induced extension of function fields is separable. Linear algebra gives rank(dD,dF)=rank dD exactly when ker dD is contained in ker dF. Applying the generic-rank equality to the two maps yields equality of image dimensions. The dominant projection of irreducible image closures therefore has relative dimension zero. The fiber-dimension theorem supplies a nonempty open U in the base where fibers are zero-dimensional or empty. Each such fiber is a finite-type zero-dimensional algebraic set and has finitely many points. Every actual (D(t),F(t)) lies in the image closure, so all actual F-values over y in U lie in that finite fiber. This includes exceptional t lying over that general y, as long as t belongs to the chosen domain T. No assertion that a single isolated solution implies a globally finite fiber is used.

## 3. Apply the frontier theorem

At a general t in this smooth-primal degree-d family, Turn3 proves that the true fundamental matrix has zero projective tangent space in the extended-Kruppa compatibility locus for its two fixed contours. For any v in ker dD_t, the contours are fixed to first order. The family of actual surfaces/cameras satisfies the contour compatibility equations identically, so its first-order F variation belongs to precisely that tangent space. It is therefore zero. This verifies ker dD_t subset ker dF_t on a dense open of T.

The lemma now proves:

**Theorem.** For every d>=3, a general pair of full algebraic contours arising from a smooth degree-d complex surface with two admissible general cameras admits only finitely many rank-two fundamental matrices among all explanations by triples in the fixed-degree admissible smooth family T. The unknown surface is allowed to vary with the cameras.

This is global finiteness of realizable epipolar geometries, not merely local uniqueness at the generating triple. It concerns a general point in the image Y; it does not assume the pair consists of two independently general plane curves. The whole fiber of surface reconstructions may still have positive dimension. The theorem bounds only its image under the F-map.

## 4. Exact scope and remaining questions

The closure Z is a stronger realizability condition than the necessary extended-Kruppa equations alone. Turn3 controls the true solution at a general smooth realization, and the image argument propagates finiteness to all realizations in the stated family over general data. It does not rule out positive-dimensional components of formally compatible matrices with no such realization. It does not compute the finite number of realizable matrices or prove that number is one. It also excludes different degrees, singular primal surfaces, degree-drop data and nongeneric contour maps outside T. The unrestricted smooth-dual family of Turn2 is a different parameter family and its uniqueness theorem cannot simply be transplanted here.

A finite algebraic fiber does not select the physically correct real camera motion; cheirality, visibility and numerical conditioning remain separate. A fixed smooth degree-d surface family is essential to this theorem, while the source itself asks a broader informal recovery question. The general source remains unresolved in this packet pending a final scope review.

## 5. Credit and controls

The mechanism combines the credited Kruppa deformation criterion with standard algebraic image-dimension and characteristic-zero differential theory. The imported report explicitly left smooth-primal transversality open; Turn3 supplies the local ingredient, and this turn isolates the precise global realizable consequence. No novelty certification is made.

The checker exercises the kernel/rank implication with exact rational linear maps, including nontrivial positive-dimensional kernels and a warning example in which the image map changes along a vertical direction. Such controls verify the finite linear algebra only. The geometric finite-image theorem is proved above, not inferred from a finite scan.
