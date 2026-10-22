# Components and singular cohomology of baby Teichmuller space

## Status and attribution

This is an authored verification and reconstruction of a prior result, not a new solution or priority claim. Alper Ferudun's unrefereed preprint, *Components and Cohomology of Fock's Baby Teichmüller Space* (1 October 2026), Theorem 1.1 and especially Lemma 3.2 and Propositions 3.3(b), 3.4, already gives the answer below. Its archived reading copy is DOI https://doi.org/10.5281/zenodo.23071801. The preprint declares CC BY 4.0. We inspected its PDF, not merely an abstract. Our reconstruction changes the angular normalization to circumference one and uses an explicit sup-norm retraction for exact arithmetic. It has not undergone human peer review. Independent audit of this packet is still required.

## Problem and conventions

The primary source is the Oberwolfach Report *Teichmüller Space (Classical and Quantum)*, volume 3 (2006), pages 1537–1614, Problem 6 on printed page 1607, posed by Volodya Fock. DOI: https://doi.org/10.4171/OWR/2006/26. The report was published on 31 March 2007, but the workshop and problem session were in 2006.

For every integer n >= 3, set

X_n^* = { (x_0,...,x_{n-1}) in (RP^1)^n : x_i != x_{i+1} for every i modulo n, and |{x_0,...,x_{n-1}}| >= 3 }.

We take the product topology on configurations and the quotient topology on B_n = X_n^*/SL_2(R). The action is simultaneous projective postcomposition, labels are retained, and nonadjacent coincidences are allowed. Neither relabeling nor orientation-reversing projective transformations are quotiented out. The central matrices +/-I act trivially, so the effective group is G = PSL_2(R). For positive n < 3 the admissible set is empty.

The primary question does not specify a cohomology theory or coefficient group. Our verified conclusion is about ordinary singular homology and cohomology with any abelian coefficient group A. We do not silently identify these with de Rham or Cech cohomology of this potentially non-Hausdorff quotient.

## Theorem

For n >= 3 there are exactly n-1 connected components of B_n. They are open, closed and path-connected, indexed by k = 1,...,n-1. For every abelian group A and every integer q >= 0,

- H^0(B_n; A) = A^(n-1).
- If n is even, H^(n-3)(B_n; A) = A.
- All other positive-degree singular cohomology groups vanish.

The identical degree formula holds for singular homology, with H_0 in place of H^0. More precisely, each component with 2k != n is weakly contractible, and the middle component for even n is weakly homotopy equivalent to S^(n-3). The word 'weakly' is essential.

For integral coefficients this also determines the ring: the degree-zero ring is Z^(n-1), and for even n there is one additional generator u of degree n-3, with u^2=0 and (a_1,...,a_{n-1})u = a_(n/2)u. For odd n all positive degrees vanish.

## 1 Winding coordinates

Choose the orientation and circumference-one coordinate omega([cos(pi t):sin(pi t)]) = t modulo 1 on RP^1. This coordinate sends infinity to 0 and the affine point 0 to 1/2, using affine coordinate x = v_1/v_2. For adjacent distinct points, let a_i be the unique number in (0,1) congruent to omega(x_{i+1})-omega(x_i). Then

k(x) = sum_i a_i

is an integer in {1,...,n-1}. Conversely, choosing omega(x_0) in R/Z and numbers 0<a_i<1 with integral sum reconstructs a unique closed configuration by successive addition. These constructions are mutually inverse continuous maps. The continuity of the positive increment follows because the diagonal, on which its branch would jump, has been removed.

The integer k is locally constant. It is also G-invariant: for fixed x, the map g -> k(gx) is a continuous integer-valued map on the connected group G. Thus k descends continuously to B_n.

A configuration satisfying adjacent inequality has at most two values precisely when n is even and it alternates between two distinct values. In winding coordinates this is the line of vectors (t,1-t,...,t,1-t), 0<t<1, and k=n/2. Removing configurations with at most two values therefore removes nothing from any other winding level.

## 2 Fixing the first two values preserves the actual quotient

Let C_n be the subspace of X_n^* where x_0=infinity and x_1=0. G acts transitively on ordered pairs of distinct points. The stabilizer of (infinity,0) is

D = {x -> lambda*x : lambda>0},

which is isomorphic to the additive group R via log(lambda). Every G-orbit meets C_n, and two elements of C_n lie in the same G-orbit precisely when they lie in the same D-orbit. The resulting continuous bijection C_n/D -> B_n is a homeomorphism, as follows.

Locally on the ordered-pair space choose a third projective point z distinct from both entries. There is a unique element s of G sending (infinity,0,+1) or (infinity,0,-1) to the ordered triple consisting of the two entries and z, with the sign chosen to match cyclic orientation. On each such neighborhood the sign is constant and the normalized transformation varies continuously (it is the familiar rational three-point projective normalization). The D-orbit of s^-1 x is independent of this auxiliary choice. These locally defined continuous maps glue and are G-invariant. They descend to a continuous inverse B_n -> C_n/D. Thus no properness or Hausdorff hypothesis was used to replace the quotient.

For each i in {2,...,n-1}, let C_(n,i) be the invariant open subset where x_i is finite and nonzero. These sets cover C_n because at least three distinct values are present. If

S_(n,i) = {x in C_(n,i) : x_i in {+1,-1}},

then the explicit map

C_(n,i) -> (0,infinity) x S_(n,i),
x -> (|x_i|, (1/|x_i|) x)

is a homeomorphism with inverse (r,y) -> r y. It intertwines the D action with multiplication on the first coordinate. The orbit map is open, since the saturation of an open set under a group action is open. Consequently C_n -> C_n/D = B_n is a locally trivial bundle with fiber (0,infinity), or equivalently R. In particular it is not merely a set-theoretic quotient with contractible orbits.

## 3 Why the bundle gives the correct singular theory

A locally trivial bundle with contractible fiber is a weak homotopy equivalence, including when its base is not Hausdorff. The relevant lifting theorem is Hatcher, *Algebraic Topology*, Proposition 4.48, printed pages 379–380, followed by the homotopy exact sequence (Theorem 4.41). Its proof only pulls back an open trivializing cover along a map from a compact cube, subdivides the cube finely, and extends the fiber coordinate using a retraction of a cube onto its bottom and sides. No separation or paracompactness property of the base enters. The usual stronger assertion about a Hurewicz fibration is unnecessary here.

The long exact homotopy sequence, together with path lifting and connected contractible fibers, gives isomorphisms on all based homotopy groups and a bijection on path components. Hatcher Proposition 4.21, printed pages 356–357, then gives isomorphisms on singular homology and cohomology with every abelian coefficient group. Its finite singular-complex argument also does not require a Hausdorff target. Thus C_n -> B_n, and its restriction to each winding level, has exactly the properties needed here. We do not assert that it has a global section or is a homotopy equivalence.

## 4 The normalized slice is convex or once punctured

In the winding coordinates of Section 1, x_0=infinity fixes omega(x_0)=0, and x_1=0 fixes a_0=1/2. Put

Y_(n,k) = { a in (0,1)^n : a_0=1/2, sum_i a_i=k }.

This is a nonempty open convex subset of an affine space of dimension n-2. For example it contains the vector whose zeroth entry is 1/2 and whose other entries are (k-1/2)/(n-1); these lie strictly between 0 and 1 for every 1<=k<=n-1.

For 2k!=n the winding-k part of C_n is exactly Y_(n,k). For n even and k=n/2 it is Y_(n,n/2) minus the single point c=(1/2,...,1/2). This follows from the alternating-vector characterization: imposing a_0=1/2 leaves just this point on the removed line.

For nonmiddle k, Y_(n,k) is contractible. In the middle case set

V_n = {v in R^n : v_0=0, sum_i v_i=0}.

Then Y_(n,n/2) is the part of c+V_n with every coordinate strictly between 0 and 1. For v!=0 write M=||v||_infinity and define

F_t(c+v) = c + [(1-t)+t/(4M)] v,  0<=t<=1.

Its endpoint c+v/(4M) lies in Y, since every coordinate displacement has absolute value at most 1/4. Convexity keeps the whole segment in Y. Its displacement is a strictly positive multiple of v, so it never meets c. If M=1/4 it is stationary. Therefore F is a strong deformation retraction of Y minus c onto the sup-norm sphere {c+v : v in V_n, ||v||_infinity=1/4}. Radial comparison with a Euclidean norm makes this sphere homeomorphic to S^(dim V_n-1)=S^(n-3).

For even n>=4 the dimension n-3 is at least one. Hence this punctured slice is path-connected and nonempty, as are all the other convex slices. Their images in B_n are path-connected. Since the winding number is continuous and takes exactly n-1 values, these images are nonempty disjoint open-and-closed subsets and are exactly the connected components. The bundle result now gives the stated weak types and singular groups. Standard cohomology of a sphere completes the computation. Products with the degree-zero idempotents and the absence of degree 2(n-3) give the asserted integral ring.

## 5 Boundary and separation controls

For n=3 a configuration is an ordered triple of distinct points. There are two G-orbits, distinguished by cyclic orientation, agreeing with the two components and no higher cohomology. For n=4 the middle slice is a punctured two-dimensional convex region; its quotient therefore has the singular homotopy type of a circle, while the two extreme components are weakly contractible.

The quotient really can be non-Hausdorff, so suppressing the adjective 'weakly' would be unjustified. For every even n>=4, choose affine numbers a_0=0,a_1=1 and, if needed, a_j=0 for j>=2. Choose b_0=infinity,b_1=1 and, if needed, b_j=infinity for j>=2. For m>=2 let

f_m = (m^2 b_0,a_0,m^2 b_1,a_1,...),
g_m(x)=x/m^2.

All adjacent values of f_m are different and at least three values occur. In the limit, f_m approaches f=(infinity,a_0,infinity,a_1,...), while g_m f_m approaches h=(b_0,0,b_1,0,...). Both limits are admissible. The first is constant on even positions and not on odd positions; the second has the opposite property, so they are in distinct G-orbits. Yet q(f_m)=q(g_m f_m) tends to both. The quotient is locally Euclidean by three-point charts; the same sequence thus illustrates concretely why standard Hausdorff/CW upgrades should not be assumed on the middle component. This witness is also prior mathematics: compare Ferudun Lemma 4.1.

## Verification boundaries

The theorem is supported by the universal arguments above, not by finite testing. The accompanying exact-rational script checks winding invariance under projective matrices, the distinction between PSL and PGL, the excluded alternating locus, rational slice witnesses, the explicit deformation and the non-Hausdorff sequences on finite controls. It cannot certify the bundle lifting theorem or establish a universal result by enumeration.

We do not certify the entire preprint. In particular its stronger separation classification, constant-sheaf comparison, Cech comparison, de Rham result, frieze variants and claims about strong homotopy type are not needed for the theorem here. We read them to identify the scope and avoid overstatement. The original problem's unqualified word 'cohomology' remains convention-sensitive. The conclusion is a prior-result verification complete for ordinary singular cohomology and component count, not a resolution of all possible cohomology theories or proof of historical priority.

## References

1. S. Morita, A. Papadopoulos and R. C. Penner (organizers), *Teichmüller Space (Classical and Quantum)*, Oberwolfach Reports 3 (2006), 1537–1614, Problem 6, p.1607. https://doi.org/10.4171/OWR/2006/26
2. A. Ferudun, *Components and Cohomology of Fock's Baby Teichmüller Space*, unrefereed preprint, 1 October 2026, Theorem 1.1, Lemmas 2.1, 3.1–3.2 and Propositions 3.3–3.4. https://doi.org/10.5281/zenodo.23071801
3. A. Hatcher, *Algebraic Topology*, Cambridge University Press, 2002, Propositions 4.21 and 4.48, Theorem 4.41. Author-hosted edition inspected: https://pi.math.cornell.edu/~hatcher/AT/AT.pdf
