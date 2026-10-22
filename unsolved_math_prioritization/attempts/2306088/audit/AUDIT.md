# Independent adversarial audit: Function Theory 6.88

Audit date: 2026-10-04 UTC. Catalogue ID 2306088 / AMR-022-6088, rank 589.

## Verdict

**PASS at the explicitly stated published/classical-theorem dependency level.** The frozen packet correctly deduces the sharp area constant `sqrt(27*pi/8)` and a sufficient positive perimeter constant `pi*sqrt(27/2)`. The map `q(z)=z+z^2/2` proves optimality of the area constant. No mathematical correction is required for the original finite-area question or its perimeter-existence addendum.

This is an attributed known result and catalogue-status correction, with discovery count zero. It is not an independent new solution of the minimum-area theorem, a formal proof certificate, an authenticated-image review of the 2006 paper, or a solution of the sharp-perimeter problem.

The reviewed `FROZEN_MANIFEST.json` SHA-256 is `6c8b21e1fedfbde37339716d8bfd8a57ec5aed6c703c6cb0732b8155adf0331c`. All eight frozen entries, their byte counts, and the `SHA256SUMS` fingerprint and entries match before and after the audit. No frozen file or remote repository state was modified.

## 1. Original statement and exact scope

I read the complete supplied dataset record and prior AI report, and independently inspected the page image of [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), printed p. 148, PDF leaf 149. The question starts with a normalized univalent map whose image has finite area, and asks for the best constant in the second-coefficient area sharpening. Its next sentence conjectures the existence of an analogous perimeter bound; it does not expressly ask for the largest perimeter constant.

Thus the prior AI report's residual description of “sharp constants” strengthens the perimeter request. The packet correctly distinguishes those scopes. The 2018 update is a report of information received by that source, not evidence that the earlier published theorem is absent. The supplied immutable-source fingerprints agree with the four local source files named in `SOURCE_MANIFEST.json`; I did not independently redownload or authenticate the complete dataset corpus.

## 2. Published input: hypotheses and normalization

I independently reopened the [public author-posted 2006 text](https://www.academia.edu/31230874/Minimal_area_problems_for_functions_with_integral_representation), and read its normalization on pp. 83–84 and Section 4, pp. 105–109. It defines S by univalence in the unit disk, f(0)=0, f'(0)=1, fixes the second Taylor coefficient a, and identifies its Dirichlet integral with image area when the map is univalent. Theorem 3 gives the typically-real estimate; Theorem 4 expressly transfers it to S for 0<a<2. The inverse-Koebe parameter is tau=2(2-a)/3. There is no additional convexity, omitted-area, or point-value hypothesis in that transfer.

Rotation preserves normalization and area, and sends a2 to exp(i theta)a2, so a prescribed nonnegative real coefficient suffices for |a2|. The a=0 endpoint does not have to be forced into Theorem 4: the packet proves the entire interval 0<=a<=1/2 directly.

The accessible display is OCR, with damaged typography in places. It is not a verified page-image transcription. Its factor 27*pi/8 and the explicit extremal are mutually consistent and are independently normalized below. Theorem 4 imports its coefficient-comparison lemma from the 1999 paper; that original proof has not been read in this audit. Treating Theorem 4 as an explicitly identified published theorem is legitimate and is exactly the packet's stated dependency level.

I also reopened the [1999 publisher abstract](https://link.springer.com/article/10.1007/BF02791132). It claims resolution of the normalized prescribed-second-coefficient area problem but displays denominator 7. The explicit a=1 construction gives a smaller area and disproves that displayed stronger numerical lower bound. The packet correctly declines to use the corrupted formula. This is not evidence that the underlying 1999 theorem is false. The supplied 1974 announcement states denominator 8 only under additional topological assumptions; it is correctly treated as historical corroboration.

## 3. Universal area inequality and endpoints

Put a=|a2|. Bieberbach's second-coefficient theorem gives a<=2; its equality case is a Koebe rotation with infinite area. Therefore the finite-area hypothesis implies a<2. The area identity gives A>=pi>0. Squaring `(2-a)*sqrt(A)>=sqrt(27*pi/8)` is consequently reversible, without an unnoticed sign condition.

For a>1/2, the stated published minimum immediately gives `(2-a)^2*A>=27*pi/8`. For 0<=a<=1/2, integrating |f'|^2 on smaller disks and taking an increasing limit gives A>=pi*(1+2*a^2). I independently expanded the exact identity

`(2-a)^2*(1+2*a^2)-27/8 = (1-2*a)^3*(5-2*a)/8`.

Both factors on the right are nonnegative on the required interval. The result includes a=0 and a=1/2. As an additional check, the derivative of the expression before subtracting 27/8 is `-2*(2-a)*(2*a-1)^2`, confirming the endpoint minimum on that interval.

The original problem excludes A=infinity. If the inequality is extended with infinity^(-1/2)=0, it is just Bieberbach's inequality there; the packet does not need to multiply an indeterminate expression involving a=2 and infinite area.

## 4. Sharpness, branches, and explicit maps

For q(z)=z+z^2/2, equality q(z)=q(w) factors as `(z-w)*(1+(z+w)/2)=0`. In the open disk, |z+w|<2; hence distinct points cannot collide. The vanishing derivative at the boundary point -1 creates no interior failure of univalence. The map is normalized and bounded, a=1/2, A=3*pi/2, and `(2-a)^2*A=27*pi/8`. A larger proposed constant fails for this one map. No equality-case classification is needed.

I also checked the optional family independently. For 0<tau<1,

`tau*k(D) = C minus (-infinity,-tau/4]`

is a subset of `k(D)=C minus (-infinity,-1/4]`. Thus the branch of k^(-1) taking zero to zero is defined throughout the required image. Its range is D with the negative terminal slit removed, whose interior endpoint is -r with `r/(1+r)^2=tau/4`, 0<r<1. This gives an injective p_tau, and composing with the already injective q and a nonzero dilation gives an injective F_tau.

The defining equation yields p_tau'(0)=tau and second coefficient 2*tau*(1-tau). Hence F_tau'(0)=1 and its second coefficient is 2-3*tau/2=a. The deleted segment is one-dimensional; its polynomial image has planar measure zero. Injectivity then gives exactly

`A(F_tau)=A(q)/tau^2=27*pi/[8*(2-a)^2]`.

The endpoint tau=1 is q; as tau decreases to zero, a increases to two and the area diverges. These checks rule out a wrong inverse branch, a missing dilation square, and the abstract's denominator 7. They establish attainment and normalization, not the lower bound by themselves.

## 5. Perimeter: direction, boundary convention, and infinite cases

For finite area and finite topological boundary length ell=H^1(partial Omega), the finite-perimeter form of planar isoperimetry gives `4*pi*A<=P(Omega)^2<=ell^2`. The second inequality is important for slit boundaries: the measure-theoretic perimeter and topological boundary length need not be equal.

As independent checks on those classical inputs, [Lahti's Federer-characterization paper](https://arxiv.org/abs/1804.11216) states the finite-boundary-measure criterion, and [Figalli–Indrei, Theorem 2.2](https://people.math.ethz.ch/~afigalli/papers-pdf/A-sharp-stability-result-for-the-relative-isoperimetric-inequality-inside-convex-cones.pdf) gives the isoperimetric inequality for finite-perimeter sets. Specializing the latter to C=R^2 yields `2*sqrt(pi*A)<=P(Omega)`. The measure-theoretic boundary is contained in the topological boundary, giving the stated comparison. Neither source imposes a Jordan-boundary assumption for this use.

The reciprocal inequality points the correct way: `A<=ell^2/(4*pi)` implies `1/sqrt(A)>=2*sqrt(pi)/ell`. Therefore the area result implies `(2-a)*ell>=pi*sqrt(27/2)`. A conformal boundary trace that counts slit sides with multiplicity has no smaller length, so the same sufficient bound remains valid. It is not legitimate to infer optimality of the perimeter constant from this chain, and the packet does not do so.

If ell=infinity, interpret 1/ell=0 and apply Bieberbach directly. No isoperimetric division by infinity is necessary.

For completeness, even if the perimeter assertion is read without the original finite-area assumption, finite ell forces a univalent image to be bounded. Here is an elementary justification. If the proper simply connected image Omega containing zero were unbounded, it would meet every circle about zero. For every R>dist(0,partial Omega), that circle cannot be wholly in Omega: a simple closed curve in a simply connected planar domain encloses only points of that domain, while an omitted point exists at smaller modulus. Since the circle meets both Omega and its complement, it meets partial Omega. The 1-Lipschitz radius map therefore sends partial Omega onto an unbounded interval, forcing H^1(partial Omega)=infinity. This contradiction proves boundedness and finite area. Thus no unhandled infinite-area/finite-length exception spoils the perimeter conclusion.

## 6. Related prior work and audit boundaries

I read the supplied PR 503 proof, source gate, complete original non-passing audit, and repaired passing audit. The earlier failed biangle-source comparison remains a recorded historical defect. The repaired proof uses ordinary conformal radius and a negative slit, and its Taylor comparison has the correct direction. This packet cites the repaired proof but does not revive the disputed biangle argument or independently assert full-class uniqueness.

This audit does not count the prior audit as its own verification of a foundational theorem. The current result follows from the explicitly attributed published theorem plus the independent elementary argument above. The stronger prescribed-coefficient result in [PR 503](https://github.com/AlecKriebel/Math/pull/503) is the same decisive mathematical input. Discovery count zero and the proposed `already_solved`, `1/5` disposition are appropriate for the original scope.

## 7. Reproducibility and nonblocking clarifications

`audit_controls.py` runs 89 integrity and exact-rational checks, including an independent degree-nine formal-series computation for five Pick parameters, slit endpoint checks, factorization/monotonicity, normalization, and wrong-formula controls. It also reruns the author's 21 checks and compares the complete JSON with the frozen recording. All pass. The frozen manifest and inputs remain unchanged.

These counts include integrity checks and sampled formal-series controls; they are not an exhaustive functional search or proofs of univalence, topology, symmetrization, or isoperimetry. Those analytic steps are addressed separately above.

No required mathematical correction was found. Optional editorial improvements are recorded in `CORRECTIONS.md`: make the infinite-area convention explicit, add an exact finite-perimeter reference, and describe the author's last negative control as only an arithmetic direction sanity check. These do not block the current verdict. Full source PDFs/OCR, dataset records, and private retrieval material are excluded from the audit deliverable.
