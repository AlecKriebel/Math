# Independent analytic and source-scope derivations

## Complete norm/length interface

For either prescribed matrix norm, left and right multiplication by unitaries are isometries, and ||B E C||_nu <= ||B||_op ||E||_nu ||C||_op. For HS this follows by summing Euclidean column bounds (and applying the same inequality to the adjoint for right multiplication); for op it is submultiplicativity. The resulting intrinsic metric is bi-invariant. Any absolutely continuous matrix curve has norm-length integral of its derivative. On the unitary submanifold the induced Finsler length has the same integral: one inequality follows by ambient chord bounds and partitions; the reverse follows in local charts from the first-order tangent norm, then subdivision. This is the standard finite-dimensional curve-length fact used by the manuscript, with no change to a chordal target metric.

Every minimizing sphere geodesic has Lipschitz image of intrinsic length <=L times its domain length. The normalized image lies in Re W>=0 because an eigenvector detects principal-angle distance at most the ambient intrinsic distance, and the unit-round diameter is pi. Differentiating the rational transform along that absolutely continuous image gives the exact norm-speed bound q_t=(1-t^2)/(1+t^2). The transformed image curve supplies an admissible target path. The argument is valid even if the semicircle subset is not target-geodesically convex. It also does not require smoothness of the input map.

## Matrix algebra and continuity

D*=I+tW* gives D*D=(1+t^2)I+t(W+W*) >=(1+t^2)I. Hence D is uniformly invertible, including t=1. The numerator N=W+tI satisfies N*N=D*D, so F=N D^-1 is unitary. The exact difference identity keeps the order D_U^-1 (U-V) D_V^-1; moving U-V to the right generally fails for noncommuting matrices. Differentiation yields (1-t^2)D^-1 E D^-1 for arbitrary perturbation E, without commuting E with W. Both endpoints and identity-fixed property are exact.

For two maps the anchor variation costs one delta and normalized variation costs two delta, yielding a uniform 3 delta map-space continuity estimate in either matrix norm. Uniform t continuity follows from compact [0,1]xS and the inverse lower bound. Intrinsic and chordal uniform topologies coincide on compact finite-dimensional U(N). The formula therefore defines the requested strong deformation retraction, rather than merely individual null homotopies. Since evaluation at p remains A at every time, the based subspace contracts to I. Constant maps throughout the entire copy of U(N) remain fixed; that copy itself is not contracted to one preferred point.

For arbitrary topological parameter space Y, a continuous map on Y x S^(n-1) substituted into the rational formula gives a continuous map on [0,1]xYxS^(n-1). Compactness of the sphere also identifies this with a continuous map into the uniform function space, without a metrizability assumption on Y. A global fixed domain basepoint is available for this product family. No argument for a nontrivial sphere bundle, or equivariance under changing the domain basepoint, is asserted.

## Boundary distances on the two-point sphere

For op, the principal-angle maximum distance formula follows directly: the eigenvector lower bound applies to every path; the path exp(i s Theta) attains max|theta_j|. For HS, the unnormalized trace metric is a complete bi-invariant Riemannian metric. Its geodesics through I are exp(s X), since Ad-invariance gives Levi-Civita connection one half the Lie bracket. Compactness supplies a minimizing geodesic. Every skew-Hermitian logarithm of W has angles theta_j+2pi k_j, and minimizing its Euclidean eigenangle norm gives sqrt(sum theta_j^2). Thus the manuscript's S0 extension uses the correct intrinsic distances, not ambient chord norms.

The scalar transformed angle g_t(theta)=2 arctan(((1-t)/(1+t))tan(theta/2)) satisfies g_t(0)=0 and g_t'(theta)=(1-t^2)/(1+t^2+2t cos theta). For |theta|<=pi/2 its absolute derivative is <=q_t, so |g_t(theta)|<=q_t |theta|. Applying this coordinatewise proves both principal-angle norm estimates on S0 with assigned interpoint distance pi. It does not assign a finite intrinsic path metric to a disconnected Riemannian zero-sphere.

At t=0 the map is unchanged; at t=1 its denominator remains invertible and the output is exactly constant. The strict sublevel stays strict because q_t<=1. At eigenangles +/-pi/2 the norm bound still holds with equality for the differential envelope. Outside the semicircle, W=-I has scalar angular derivative 3 at t=1/2 whereas q_t=3/5, and t=1 is singular. Hence removing the domain bound is not permitted.

The scalar family Phi(x)=exp(i d(p,x)/2) on a positive-dimensional unit-round sphere has Lipschitz constant 1/2 and reaches angle pi/2 at the antipode. One-sided local ratios there approach q_t. This diagnoses an erroneous smaller universal coefficient (1-t)/(1+t), without claiming a new research theorem or opening a follow-up programme.

## Monotonicity along time

The printed estimate is relative to the input. The actual formula also implies ordinary time monotonicity if the title is read that way. Rational functional calculus gives F_u(F_s(W))=F_((s+u)/(1+su))(W). The anchor remains A, so H_u(H_s(Phi)) has the same composition law. For 0<=s<=t<=1 and s<1, set u=(t-s)/(1-st) in [0,1]. Then Lip(H_t Phi)<=q_u Lip(H_s Phi)<=Lip(H_s Phi). The terminal case is constant. This is a check of the displayed construction, not an asserted literature novelty.

## Exact primary interpretation

Gromov's actual printed pages35–36 confirm the literal continuous-deformation question and its metric context. The manuscript stays within its explicit HS/op metrics; neither the nearby Lip<1 argument nor nontrivial sphere fibrations are included in its theorem.

The Neretin 2011 author-hosted book was read at printed page42, section1.7.9/Theorem7.5 (actual page54). Its Cayley chart gives the classical unitary/self-adjoint correspondence, with invertibility of I+W understood in that chart. On the present semicircle domain the chart is safe. Substituting the displayed F_t gives C(F_t(W))=((1-t)/(1+t))C(W). This confirms the classical attribution and does not transfer originality of the chart to this manuscript.

No priority assertion is inferred from a bounded search or from the deposited author audit. The new focused search was limited to the stated catalog identifier and the Gromov/Lipschitz/unitary assertion; it did not establish priority. The AMR catalog identifier in package metadata is treated as bookkeeping, while the exact mathematical assertion was verified against Gromov's own PDF. No public follow-up question or worldwide-openness claim is supported or proposed.
