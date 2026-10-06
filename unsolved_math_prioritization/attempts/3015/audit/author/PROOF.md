# Triangulation obstructions in dimension five

## Scope and result

Kirby Problem 5.8 asks for an aspherical, compact, boundaryless topological manifold of dimension five whose underlying space admits no simplicial triangulation. Here, aspherical means that all homotopy groups in degrees at least two vanish. A simplicial triangulation is not required to be a PL triangulation.

**The existence question remains unresolved in this report.** The results below are explicit deductions from established triangulation obstruction theory. They isolate a characteristic-number test, an exact mapping-torus criterion, and obstructions to several natural construction routes. No novelty is claimed for these deductions. In particular, the mapping-torus mechanism already appears in Kronheimer's example recorded by Manolescu [MC, Example 4.5].

Throughout, manifolds are Hausdorff and second countable. All closed manifolds under discussion are connected unless explicitly stated otherwise. Write F2 for Z/2 and let

\[
\Delta(M)\in H^4(M;\mathbf F_2)
\]

be the stable Kirby–Siebenmann class. In dimension at least five, its vanishing characterizes existence of a PL structure. Its nonvanishing alone does **not** characterize failure of simplicial triangulability.

## Established inputs

Let Theta be the smooth oriented integral homology-cobordism group of homology three-spheres, let mu:Theta -> F2 be the Rokhlin homomorphism, and put A=ker(mu). The exact sequence

\[
0\longrightarrow A\longrightarrow\Theta\overset{\mu}{\longrightarrow}
\mathbf F_2\longrightarrow0
\]

defines a connecting map delta. The Galewski–Stern–Matumoto theorem says that a topological manifold M of dimension at least five admits a simplicial triangulation precisely when

\[
\delta\Delta(M)=0\quad\hbox{in }H^5(M;A).
\tag{1}
\]

This includes nonorientable manifolds; these are constant coefficient systems in the cohomology groups. See [MC, Theorem 4.3]. Manolescu proved that there is no y in Theta with mu(y)=1 and 2y=0 [MP, Corollary 1.2]. Neither input assumes that Theta is torsion-free.

We also use Poincare duality with the orientation local system, naturality and stability of the Kirby–Siebenmann class, the integral Bockstein identity rho b=Sq^1, and the degree-one Wu formula. These standard algebraic-topological facts are applied explicitly below.

## The characteristic-number criterion

**Theorem 1.** For a closed connected topological five-manifold M, define

\[
\nu(M)=\left\langle w_1(M)\smile\Delta(M),[M]_2\right\rangle
\in\mathbf F_2.
\]

Then M has no simplicial triangulation if and only if nu(M)=1. Equivalently, M is triangulable if and only if Sq^1 Delta(M)=0.

**Proof.** Choose y in Theta with mu(y)=1. Let

\[
b:H^4(M;\mathbf F_2)\longrightarrow H^5(M;\mathbf Z)
\]

be the connecting map for 0 -> Z --2--> Z -> F2 -> 0. Define j:Z -> A by j(n)=2ny. This is well-defined because mu(2y)=0. The maps j on the left, n -> ny in the middle, and the identity on F2 give a morphism from this integral exact sequence to the sequence defining delta. Naturality gives

\[
\delta x=j_*b(x)\quad\text{for every }x\in H^4(M;\mathbf F_2).
\tag{2}
\]

If M is orientable, Poincare duality identifies H^5(M;Z) with Z. Exactness says that every b(x) is killed by 2, so b(x)=0. Thus delta Delta(M)=0 and M is triangulable by (1). Also w1(M)=0, as required.

Suppose M is nonorientable. For any abelian constant coefficient group B, duality gives

\[
H^5(M;B)\cong H_0(M;B\otimes\mathcal O_M)\cong B/2B.
\tag{3}
\]

Indeed, the monodromy of the orientation system acts on B by a sign. Since M is connected and has an orientation-reversing loop, its coinvariants impose exactly the relations b=-b. Thus H^5(M;Z)=Z/2, and reduction rho to H^5(M;F2)=F2 is an isomorphism. These identifications are natural in B.

Under (3), j_* sends the generator of Z/2 to the class of 2y in A/2A. This class is nonzero: if 2y=2a for some a in A, then z=y-a would have mu(z)=1 and 2z=0, contradicting Manolescu's theorem. Consequently j_* is injective on H^5(M;Z). Equation (2), the isomorphism rho, and rho b=Sq^1 now imply

\[
\delta x=0\quad\Longleftrightarrow\quad b(x)=0
\quad\Longleftrightarrow\quad\operatorname{Sq}^1x=0.
\tag{4}
\]

For x=Delta(M), the degree-one Wu formula gives

\[
\left\langle\operatorname{Sq}^1\Delta(M),[M]_2\right\rangle
=\left\langle w_1(M)\smile\Delta(M),[M]_2\right\rangle.
\]

Evaluation on [M]2 identifies the top mod-two cohomology with F2. Combining this fact with (1) and (4) proves the result. Notice that the Wu identity is used in top degree, not as an identity for arbitrary cohomology classes in arbitrary degrees. QED.

**Interpretation for Problem 5.8.** A positive solution is equivalent to constructing a closed aspherical five-manifold with nu=1. Proving nu=0 for every such manifold would give a negative solution. Neither assertion is established here.

## Products and covers

**Corollary 2.** If X is any closed connected topological four-manifold, including a nonorientable one, then X x S1 admits a simplicial triangulation.

**Proof.** For the projection p:X x S1 -> X, stability and the tangent-microbundle product formula give Delta(X x S1)=p*Delta(X) and w1(X x S1)=p*w1(X). Their product is the pullback of a class in H^5(X;F2), which vanishes by dimension. Theorem 1 applies. Equivalently, naturality makes delta Delta(X x S1) the pullback of a class in H^5(X;A)=0. QED.

Thus multiplying a nontriangulable aspherical four-manifold by a circle cannot solve the five-dimensional question. The product may still fail to be PL.

**Corollary 3.** Let p:N -> M be a connected finite covering of degree d between closed connected topological five-manifolds. Then

\[
\nu(N)=(d\bmod2)\nu(M).
\tag{5}
\]

In particular, every even-degree such cover is triangulable. An odd-degree cover is triangulable if and only if its base is triangulable.

**Proof.** A covering map identifies the stable tangent microbundle upstairs with the pullback of the one downstairs. Hence both characteristic classes in nu pull back. The mod-two fundamental classes satisfy p_*[N]2=(d mod 2)[M]2, proving (5). Apply Theorem 1. QED.

Asphericity passes to finite covers. Therefore a hypothetical example in Problem 5.8 necessarily has triangulable even-degree covers, including its orientation double cover. This does not construct the example or an action producing it. Nor does this proof imply that even-degree covers in dimensions at least six must be triangulable: Theorem 1 uses the top-degree cohomology of a five-manifold.

## An exact mapping-torus criterion

Let X be a closed connected **orientable** topological four-manifold and f:X -> X a homeomorphism. Let Tf=(X x [0,1])/((x,1)~(f(x),0)), and write epsilon(f)=0 or 1 according as f preserves or reverses orientation. Set ks(X)=<Delta(X),[X]2>.

**Theorem 4.** The mapping torus Tf satisfies

\[
\nu(T_f)=\epsilon(f)\operatorname{ks}(X).
\tag{6}
\]

It is aspherical if and only if X is aspherical. Consequently this construction answers Problem 5.8 positively exactly when X is aspherical, ks(X)=1, and f reverses orientation.

**Proof.** Let q:Tf -> S1 be the bundle projection, let u generate H^1(S1;F2), and let i:X -> Tf include a fiber. Orientability of X means that the total space's orientation character vanishes on fiber loops and has value epsilon(f) on a loop once around the base. Thus w1(Tf)=epsilon(f)q*u. The fiber is locally flat with trivial normal line; hence i*Delta(Tf)=Delta(X). Since q*u is mod-two Poincare dual to the fiber,

\[
\left\langle q^*u\smile\Delta(T_f),[T_f]_2\right\rangle
=\left\langle i^*\Delta(T_f),[X]_2\right\rangle
=\operatorname{ks}(X).
\]

This proves (6). The homotopy exact sequence of the fiber bundle over S1 identifies pi_k(Tf) with pi_k(X) for each k>=2. The final conclusion follows from Theorem 1. QED.

No claim is made that every example sought by Problem 5.8 must fiber over S1. The theorem characterizes this particular construction route.

**Corollary 5.** If X is spin as well as orientable, every mapping torus of a self-homeomorphism of X is triangulable.

**Proof.** The orientation-preserving case follows from Theorem 4. In the orientation-reversing case, the signature obeys sigma(X)=-sigma(X), so sigma(X)=0. The topological spin identity ks(X)=sigma(X)/8 mod 2, recalled in [T, p. 757], gives ks(X)=0. Theorem 4 again applies. The homeomorphism need not preserve a chosen spin structure. QED.

In fact any fiber satisfying the positive criterion of Theorem 4 must be nonspin and have signature zero. The criterion does not supply such an aspherical fiber with the required homeomorphism. The simply connected fiber in the established Kronheimer example [MC] is not aspherical: its nonzero second homology gives nonzero pi2 by Hurewicz.

## The hyperbolization barrier

The primary DFL paper constructs examples in dimensions at least six. Its Section 3 identifies the missing five-dimensional step: obtain a PL structure on the resolved four-dimensional boundary after hyperbolization. It explains that the original resolved boundary has zero Kirby–Siebenmann class but is nevertheless not PL. Making a pre-hyperbolization resolution PL does not establish this property after hyperbolization. Thus replacing the needed PL assertion by the equation Delta=0 in dimension four is invalid. Relative hyperbolization cannot fill this missing hypothesis by itself. [DFL, pp. 798–800.]

Lafont and Ruffoni's later Theorem 5.12 supplies hyperbolic virtually compact special fundamental groups for the higher-dimensional examples. Its range is still n>=6. It provides no five-dimensional example or repair of that boundary step. [LR, Section 5.3.]

The five routes examined therefore end with proved reductions and exclusions, not a closed aspherical five-manifold with nu=1 and not a universal vanishing theorem. The secondary question in K3 about virtually triangulable aspherical four-manifolds is also left unanswered.

## References

- [K3] R. I. Baykur, R. C. Kirby, and D. Ruberman, *K3 – A New Problem List in Low-Dimensional Topology*, author's preliminary AMS version, Problem 5.8, printed p. 306. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [DFL] M. W. Davis, J. Fowler, and J.-F. Lafont, *Aspherical manifolds that cannot be triangulated*, Algebraic & Geometric Topology 14 (2014), 795–803. https://msp.org/agt/2014/14-2/agt-v14-n2-p06-p.pdf
- [MC] C. Manolescu, *The Conley index, gauge theory, and triangulations*, author's updated PDF, Section 4, especially Theorem 4.3 and Example 4.5. The journal publication is Journal of Fixed Point Theory and Applications 13 (2013), 431–457. https://web.stanford.edu/~cm5/conley.pdf
- [MP] C. Manolescu, *Pin(2)-equivariant Seiberg–Witten Floer homology and the Triangulation Conjecture*, Corollary 1.2. Journal of the American Mathematical Society 29 (2016), 147–176. https://arxiv.org/abs/1303.2354
- [T] P. Teichner, *On the signature of four-manifolds with universal covering spin*, Mathematische Annalen 295 (1993), 745–759, especially p. 757. https://math.berkeley.edu/~teichner/Papers/Signature.pdf
- [LR] J.-F. Lafont and L. Ruffoni, with an appendix by D. Groves and J. Manning, *Relative cubulation of relative strict hyperbolization*, Journal of the London Mathematical Society 111 (2025), no. 4. Inspected version: arXiv:2304.14946v2, revised 2 April 2025, Theorem 5.12 and Remark 5.13. https://arxiv.org/abs/2304.14946v2 ; https://doi.org/10.1112/jlms.70093
