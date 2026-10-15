# Independent duality and algebra derivation, before candidate exposure

Scope read so far: literal source_snapshot_v2/source_record.json, whose statement is “Are homotopy types of 2-knot complements determined by their homotopy 2-types?” No candidate OBSTRUCTION, review, result, verifier, or old-helper body has been opened. This note reconstructs consequences from the question and standard topology; primary-source checking follows.

## Exact claim and hypotheses

Let X be the exterior of a smooth or locally flat PL embedding S^2 in S^4. The open complement deformation retracts onto X. X is a compact connected orientable 4-manifold with boundary S^2 x S^1; H_*(X;Z)=H_*(S^1;Z). A meridian t generates H_1(X;Z) and has infinite order in G=pi_1(X). The question asks whether an isomorphism of full unmarked Postnikov 2-types (G,A=pi_2(X),k in H^3(G;A)), including the compatible group and module isomorphisms carrying k, implies a homotopy equivalence of the entire spaces. Boundary pairs, meridian-preserving equivalence, and knot isotopy are stronger or differently marked conclusions, and no pair structure is supplied by the stated invariant.

## Independent consequences and falsifiers

1. A compact 4-manifold with nonempty boundary has a finite CW model of dimension at most 3 (e.g. a handle decomposition without 4-handles). Its simply connected universal cover has H_4=0 and H_1=0. A homology-S^1 conclusion for X does not imply H_3 of its cover vanishes.

2. Take Lambda=ZG with its left regular action and retained commuting right action. C^*(X;Lambda)=Hom_Lambda(C_*(tilde X),Lambda) is naturally a right-Lambda complex. Poincare-Lefschetz duality converts its right modules to left modules using the involution g -> g^(-1); orientation twisting is trivial because X is orientable. In degree 1 the simply connected cover identifies H^1(X;Lambda) with H^1(G;Lambda). Boundary inclusion corresponds to H=<t> <= G and H^1(boundary X;Lambda)=H^1(H;Lambda), since the S^2 factor contributes no degree-1 cohomology. Both H^0(X;Lambda) and H^0(boundary X;Lambda) are zero: finite-support elements of ZG invariant under an infinite subgroup vanish. The relative cohomology long exact sequence therefore gives

  H^1(X,boundary X;Lambda) = ker[H^1(G;Lambda) -> H^1(<t>;Lambda)].

After applying the involution this is H_3(tilde X) as a left-Lambda module. Equivalently, compact-support duality on tilde X uses H_c^1(tilde X,boundary tilde X), not ordinary H^1(tilde X,boundary tilde X). Losing compact supports is a serious possible falsifier.

3. A left-module calculation for the infinite cyclic subgroup gives H^1(<t>;Lambda)=Lambda/(t-1)Lambda; this is a right-Lambda quotient, because (t-1)Lambda is a right ideal. If a text calls this a left module without applying the involution or switching convention, the sidedness must be repaired. Multiplication by t-1 is not a unit in the integral group ring; augmentation maps it to 0. Formal geometric series cannot be used in ZG unless they are finite, so telescoping purportedly supported on an infinite orbit is invalid.

4. For finitely generated infinite G, H^1(G;ZG) detects ends; one-ended groups have zero such cohomology. Thus one-ended actual knot groups yield H_3(tilde X)=0. Infinite ends do not by themselves prove that the meridian restriction has a nonzero kernel. Normal generation of G by t is not a proof of injectivity or noninjectivity of restriction: a derivation can vanish on t without vanishing on every conjugate of t. Specifically, if d(t)=0, then d(a t a^(-1))=(1-a t a^(-1))d(a), which may be nonzero. For finite-group splittings, geometric realization as an actual 2-knot exterior and the specific meridian must be checked separately from group presentation and normal generation.

5. The simply connected Whitehead exact sequence for a 3-dimensional CW model has 0 -> Gamma(A) -> pi_3(X) -> H_3(tilde X) -> 0. Additional higher information can therefore occur through H_3 and the module extension. This observation does not produce a counterexample within the class of actual knot exteriors. Wedge-S^3 examples among arbitrary CW complexes are outside the question's success criterion.

6. A full 2-type isomorphism supplies an equivalence of P_2 X and P_2 Y. Since X has dimension at most 3, ordinary obstruction theory suggests an absolute map X -> Y inducing it (first obstruction to lifting to Y lies in degree 4). This does not supply a boundary map, meridian preservation, relative fundamental-class degree 1, or a homotopy equivalence. Those are separate exact gaps; no assumption of pair-map degree 1 may be smuggled into an argument for the unmarked question.

7. A valid negative answer requires two actual smooth/locally flat PL 2-knot complements with isomorphic full (G,A,k) and provably different homotopy types. A valid positive answer requires all such exteriors, including non-quasi-aspherical cases, without extra peripheral markings or an unproved degree-1 pair-map premise. An audit may validly certify a restricted theorem or computational identity while leaving the original question unsolved.

## Initial checkpoints

Initial mathematical reconstruction: approximately 20% of this audit complete. The deductions above are independently written from the literal question; source validation and candidate comparison remain. The strongest anticipated check is the exact relative duality kernel with explicit coefficient sidedness. No solution of the original problem is claimed.
