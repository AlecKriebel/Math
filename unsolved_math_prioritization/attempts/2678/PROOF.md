# Separating-sphere twists detected by knots: scoped prior-result audit

Audit date: 11 October 2026. Target: K3 Problem 1.19, dataset record 2678.

## Finding

The affirmative answer follows, for **closed, connected, oriented smooth 3-manifolds**, from established theorem statements and the argument below. This is a prior-result audit, not a claim of a new solution or of priority. An explicit public treatment is Alper Ferudun's unrefereed October 2026 note, version 1.1 [F]. The argument required for the target has no gap identified in this audit when the cited classical theorems are used as dependencies.

There are two distinct historical records. Aceto–Bregman–Davis–Park–Ray, arXiv:2007.05796v3, p. 6, records an Etnyre–Margalit proof extending its Theorem 1.1 to non-prime manifolds, with no written proof supplied there [A]. Ferudun's version 1.1 reports an October 2026 personal communication that their paper is forthcoming and their argument differs from his. That second statement is Ferudun's public report; this audit did not contact either mathematician. The announcement is not being substituted for an inspected proof.

## Exact scope

K3 p. 28 asks about a specified twist around the separating sphere in Y1#Y2, with neither summand S3 and with the twist nontrivial up to isotopy. It asks for **ambient-isotopy** detection by a knot. The smooth-knot convention is explicit on p. 11. Page 28 does not explicitly say closed or oriented, and no blanket closed/oriented convention was located in the inspected preceding pages. The related article [A] explicitly works with smooth closed oriented manifolds. We establish that formulation, and do **not** certify a variant allowing boundary, noncompact manifolds, or nonorientable manifolds.

Knots may be regarded as unoriented embedded circles. Detecting this weaker, setwise equivalence also detects the oriented parametrized knots of [A]. Equivalence by arbitrary ambient diffeomorphism is automatic for K and Phi(K) and is not the conclusion. There is no prime-summand assumption in the proof.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty, priority, or new-solution claim is made. The broader literal K3 scope is not certified.

The complete core argument and its exact classical dependencies are retained. This is not a computational reproduction package: copied source documents, source images, executable code, dataset contents, and raw certificates are not distributed. Classical theorem statements and applicability were audited; their historical proofs were not independently re-proved. Edition preparation performed editorial and byte-integrity checks only, with no new mathematical execution, scholarly-source retrieval, or visual source inspection.

## Precise dependencies

The following are established results invoked as black boxes; their entire historical proofs have not been re-proved here.

1. **Asymmetric-knot existence.** Kawauchi's Main Theorem [K], pp. 300–301, applied to a knot L in a closed connected oriented Y, supplies a knot K in the **same Y** whose exterior has complete finite-volume hyperbolic interior and trivial full isometry group. The good-pair boundary condition on p. 299 is vacuous when Y is closed. The local diffeomorphism condition in Section 2, pp. 309–310, preserves the number of components, so K is one knot, not just a link. The finite bound on volume gives finite volume. The assertion concerning the trivial isometry group is explicit in part (2). No inference from merely hyperbolic-knot existence is needed.
2. **Mostow–Prasad rigidity.** For a complete finite-volume hyperbolic 3-manifold M, every element of Out(pi1 M) is induced by a unique isometry. In particular, if Isom(M) is trivial, Out(pi1 M) is trivial. See [T], Theorem 5.7.2 and Corollary 5.7.4. Only this consequence is needed.
3. **Waldhausen, in the pointed formulation.** Hatcher–Wahl [HW], Proposition 2.1, pp. 7–8 of arXiv v4, says that the homomorphism from the pointed orientation-preserving mapping class group to Aut(pi1) is injective for compact connected orientable irreducible 3-manifolds with incompressible boundary. Its isotopies are not required to fix the boundary. The orientation-preserving and pointed qualifications must be retained.
4. **The solid-torus and smoothing facts.** Hatcher [H], Appendix, printed pp. 605–606, statements (3) and (9), gives the smooth/topological comparison (including its TOP form) and contractibility of Diff(S1xD2 rel boundary). Consequently Homeo(S1xD2 rel boundary) is path-connected, and two diffeomorphisms of a closed 3-manifold that are topologically isotopic are smoothly isotopic.
5. Standard smooth isotopy extension and uniqueness of tubular neighborhoods are used to normalize a knot-preserving map. Standard elementary hyperbolic topology says a compact exterior with complete finite-volume hyperbolic interior is irreducible with incompressible torus boundary. These background facts are used, not established by finite computations.

## Proof of the target in the stated scope

We prove a stronger statement sufficient for every quantified instance: there is one knot K in each such Y that is moved by every nonidentity orientation-preserving mapping class of Y.

Choose K by dependency 1 and let N be a closed tubular neighborhood of K. Write X=Y\int(N) and T=boundary X=boundary N. Its interior M is a one-cusped finite-volume hyperbolic manifold, and X is irreducible with incompressible boundary.

Suppose f:Y->Y is orientation-preserving and f(K) is ambiently isotopic to K. Choose h isotopic to the identity with h(f(K))=K. Tubular-neighborhood uniqueness, followed by isotopy extension, supplies rho isotopic to the identity such that g=rho h f preserves N. Thus g preserves X and is isotopic to f. This step does not require the original f to fix K pointwise or to preserve any framing.

Let u=g|X. Since Isom(M) is trivial, dependency 2 implies that the induced outer automorphism of pi1(X) is trivial. We next justify carefully why this implies an isotopy of u to the identity, without erroneously using a closed-irreducible theorem on Y.

Choose an interior point x of X. Compose u with a diffeomorphism d isotopic to the identity, supported away from T, taking u(x) to x. Such a d is obtained by moving a small ball along an interior path. The automorphism (du)* of pi1(X,x) is inner. Point-pushing x around a suitable interior loop gives a diffeomorphism d' isotopic to the identity in the unpointed diffeomorphism group, fixing x at its endpoint, whose induced inner automorphism is the inverse of (du)*. Therefore v=d'du fixes x and induces the identity automorphism. The point-push exists by extending the motion of the point along the loop to an ambient isotopy. Dependency 3 applies to v and shows that v is isotopic to the identity. Hence u is isotopic to the identity in Diff(X), with boundary allowed to move. Choose such an isotopy u_t with u_0=id and u_1=u.

It remains essential to extend this conclusion over the filling solid torus; it is not legitimate simply to assert that an isotopy on X is relative to T. Here is an explicit topological collar construction that handles this issue.

Take a collar c:T x [0,1]->N, with c(x,0)=x. For 0<=t<=1, define lambda_t:N->N on the collar by

lambda_t(c(x,s)) = c((u_{t+(1-t)s}|T)(u_1|T)^{-1}(x), s),

and define it to be the identity off the collar. At s=1 the displayed expression is c(x,1), so the definitions agree. Each lambda_t is a homeomorphism: it keeps s fixed and acts by a homeomorphism of T on every level; the inverse is the corresponding levelwise inverse and is continuous. It depends continuously on t. We have lambda_1=id and lambda_t|T=(u_t|T)(u_1|T)^{-1}.

Define kappa_t:Y->Y by kappa_t=u_t on X and kappa_t=lambda_t g on N. The definitions agree on T because g|T=u_1|T. They therefore give an isotopy through homeomorphisms. Its terminal map is g, and kappa_0 fixes X pointwise. The restriction kappa_0|N fixes T pointwise, so dependency 4 gives an isotopy to the identity in Homeo(N rel T). Extend that isotopy by the identity on X. We have proved that g, and hence f, is topologically isotopic to the identity. Dependency 4 upgrades this to a smooth isotopy.

Contrapositively, if [f] is nontrivial then f(K) is not ambiently isotopic to K. A twist Phi about an embedded separating sphere is orientation-preserving. Applying this result to each Y=Y1#Y2 and each specified nontrivial [Phi] proves the affirmative answer in the stated scope. Neither the number nor the prime types of the summands are restricted.

## Verification boundary and historical status

The conclusion is one asymmetric hyperbolic knot detecting every nonidentity orientation-preserving mapping class of a closed, connected, oriented smooth 3-manifold. The separating-sphere target follows by applying that statement to the specified nontrivial twist. The optional claim about every hyperbolic knot, its finite-order extension route, and any classification of sphere twists are not included or certified by this edition.

AUDIT.md preserves the independent focused check of the asymmetric-knot existence statement, finite-volume rigidity, pointed-to-unpointed conversion, continuous collar gluing, relative solid-torus kernel, and return to the smooth category. Those complete written arguments supply the conclusion subject to the expressly declared classical dependencies. Finite calculations do not replace their continuous or universal steps.

SOURCES.json records the exact retained PDF identities and the historical source-inspection scope. Ferudun's entire 11-page version 1.1 was text-read in the original audit; his verification report and claimed reviews are not independent evidence for acceptance. The focused audit checked the applicable statements and original scans, rather than re-proving the complete classical sources.

Aceto–Bregman–Davis–Park–Ray's May 2026 p. 6 announcement of an Etnyre–Margalit prior proof was inspected; the announced proof itself was not inspected. A bounded public proof-access search did not locate the joint written proof. This does not establish that none exists. Ferudun's October 2026 statement that their paper is forthcoming is his publicly stated manuscript status, not private author confirmation by this work. No author was contacted.

**Classification:** scoped prior result, with a complete argument using cited classical theorems. Boundary, noncompact, and nonorientable variants remain outside the accepted scope.

## References

[F] A. Ferudun, *Asymmetric Hyperbolic Knots Detect Mapping Classes of 3-Manifolds: A Written Proof for a Problem of the K3 List*, version 1.1, 5 October 2026; unrefereed. https://doi.org/10.5281/zenodo.23165876 . Landing page: https://eulersolve.org/papers/kp-1-19/ .

[A] P. Aceto, C. Bregman, C. W. Davis, J. Park, A. Ray, *Isotopy and equivalence of knots in 3-manifolds*, arXiv:2007.05796v3 (19 May 2026). https://arxiv.org/abs/2007.05796v3 . Journal version: https://doi.org/10.1112/jlms.70600 .

[K] A. Kawauchi, *Almost identical imitations of (3,1)-dimensional manifold pairs and the branched coverings*, Osaka J. Math. 29 (1992), 299–327. https://doi.org/10.18910/4930 .

[HW] A. Hatcher, N. Wahl, *Stabilization for mapping class groups of 3-manifolds*, Duke Math. J. 155 (2010), 205–269. https://arxiv.org/abs/0709.2173 .

[H] A. Hatcher, *A proof of the Smale conjecture, Diff(S3) approximately O(4)*, Ann. Math. 117 (1983), 553–607. https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf .

[T] W. Thurston, *The Geometry and Topology of Three-Manifolds*, Chapter 5. https://library.slmath.org/books/gt3m/PDF/5.pdf .

[K3] R. I. Baykur, R. C. Kirby, D. Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, AMS, 2026, Problem 1.19. https://doi.org/10.1090/surv/295 .
