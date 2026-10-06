# A smooth degenerate conductivity with no ordinary correction potential

**Verified credited exposition of a preexisting ordinary-potential counterexample.** See [PRIORITY_CORRECTION.md](PRIORITY_CORRECTION.md): Ferudun (2026) Theorem 1.2 already gives the same negative answer; this packet makes no new-resolution claim. The distinction between an actual gradient in the source's solution space and an abstract conductivity-weighted completion is essential.

## 1. Exact claim

The source constructs a linear map A↦∇φ_A satisfying

(1) div(σ(A+∇φ_A))=0 in distributions on R³,

with an ordinary unweighted L² curl-free correction, hence with A+∇φ_A in its W(curl) space. The map is intended, in particular, for divergence-free A in the vector Beppo–Levi space W¹_diamond. The foundational published Lemma3.1 actually has the larger input space L²_rho(R³)^3. See `SOURCE_GATE.md` for the exact definitions.

**Theorem.** There exist a scalar σ in C_c^∞(R³), σ>=0, and a divergence-free A in C_c^∞(R³)^3, such that there is **no** φ in H¹_loc(R³) satisfying (1). In particular there is no correction in the source's scalar Beppo–Levi class, no correction having an ordinary locally L² distributional gradient, and no extension of its gradient-valued map to all nonnegative bounded σ with its stated output.

The conductor can be taken to be a bounded connected Lipschitz domain with connected exterior, with σ positive almost everywhere there. Its only interior degeneracy is a meridional surface of measure zero. Thus failure is not caused by an irregular conductor boundary, a positive-volume interior insulating region, or irregular input A. The domain is not simply connected; the source does not require the conductor to be simply connected.

This is a negative answer for the original ordinary-potential formulation. Section6 gives the always-defined weighted projection and explains precisely why it is a different output. No claim about the impossibility of every generalized eddy-current formulation is made.

## 2. Explicit smooth coefficient and solenoidal field

Write x=(x1,x2,z), q=x1²+x2² and r=sqrt(q). Let

Omega={1<r<2, -1<z<1}.

This annular cylinder is a bounded connected Lipschitz domain. Its complement outside the closure is connected: the inner cylindrical passage connects to the outer region through either end. It is a solid-torus-type domain and is not simply connected.

Let b(t)=exp(-1/t) for t>0 and b(t)=0 for t<=0. Define

eta(q,z)=b(q-1)b(4-q)b(1-z²).

Thus eta is smooth, nonnegative, positive exactly on Omega, and flat on its boundary. Choose a smooth compactly supported function chi(q,z) that is identically1 on a neighborhood of [1,4]×[-1,1], vanishes for q<=1/4, and is supported where q<9 and |z|<2. Standard one-dimensional smooth cutoffs and their product give such a chi.

Define, with zero extension near the axis,

A(x)=chi(q,z)(-x2/q, x1/q, 0),
sigma(x)=eta(q,z)(r-x1).

Both definitions are smooth on all of R³ because their prefactors vanish on a neighborhood of the singular axis. They have compact support. The conductivity is nonnegative since r>=x1, bounded (in fact sigma<=4), and positive almost everywhere on Omega. Its interior zero set is

{ x2=0, x1>0, 1<x1<2, |z|<1 },

a single meridional cut, which has three-dimensional measure zero. Its topological support is the closure of Omega; the conductor and support are identified up to their boundary in the source convention.

A is divergence-free. Indeed, A0=(-x2/q,x1/q,0)=∇theta locally has divergence zero, and the gradient of chi(q,z) is orthogonal to A0. Consequently A lies in the source divergence-free W¹_diamond and in L²_rho, with no regularity issue. On Omega, A=A0.

If the workshop report's displayed inner-ball inclusion is retained literally rather than the foundational paper's outer-ball bound, translate the whole construction by -(3/2,0,0). The translated conductor contains B_(1/4)(0), remains bounded, and all arguments below are translation invariant. The example therefore does not depend on exploiting that notation discrepancy.

## 3. The circulation lies in the weighted closure of gradients

Use the angle theta in [-pi,pi] with endpoints identified. For 0<epsilon<1 define the continuous periodic piecewise-linear function

h_epsilon(theta)=
  -theta-pi,                         -pi<=theta<=-epsilon;
  (pi/epsilon-1)theta,                -epsilon<=theta<=epsilon;
  -theta+pi,                         epsilon<=theta<=pi.

The values agree at ±epsilon and at the identified endpoints, so this is a Lipschitz function on the circle. Its derivative almost everywhere is

h'_epsilon=-1+(pi/epsilon) 1_(|theta|<epsilon).

In particular the derivative integrates to zero around the circle, as required of a single-valued potential. Set

v_epsilon(x)=chi(q,z)h_epsilon(theta).

This is a single-valued, compactly supported H¹ function on R³, with support away from the axis. On Omega, where chi=1,

A+∇v_epsilon = (pi/epsilon)1_(|theta|<epsilon) A0.

Write the positive finite constant

C_eta = integral_(r=1)^2 integral_(z=-1)^1 eta(r²,z) dz dr.

Since sigma=eta*r*(1-cos(theta)), |A0|²=r^-2 and dx=r dr dtheta dz, direct cylindrical integration gives

||sqrt(sigma)(A+∇v_epsilon)||²₂
 = (pi²/epsilon²) C_eta integral_(-epsilon)^epsilon (1-cos(theta)) dtheta
 = (2pi² C_eta/epsilon²)(epsilon-sin(epsilon))
 <= (pi² C_eta/3) epsilon,

using 1-cos(theta)<=theta²/2. Therefore

(2) sqrt(sigma)∇v_epsilon → -sqrt(sigma)A strongly in L²(R³)^3.

Every v_epsilon is in H¹ with compact support and can be approximated in H¹ by C_c^∞ functions. Boundedness of sigma makes the corresponding weighted gradients converge. Thus (2) also places -sqrt(sigma)A in the closure of gradients of smooth compactly supported single-valued potentials. There is no use of a multivalued theta as an admissible scalar potential.

For contrast, the unweighted gradients of these approximants diverge. On Omega their squared norm is exactly

2 log(2) [2pi²/epsilon-2pi],

which tends to infinity. This observation alone would not prove nonexistence; the next section does.

## 4. Any ordinary solution would cancel the circulation exactly

Suppose φ in H¹_loc(R³) solved (1). The field sigma(A+∇φ) is L² and compactly supported. The distributional equation therefore extends by H¹ approximation from smooth compactly supported tests to every compactly supported H¹ test.

Choose a smooth cutoff kappa equal1 on a neighborhood of supp(sigma). Testing with kappa φ is legitimate, and gives

(3) integral sigma(A+∇φ)·∇φ=0.

The extra derivative of kappa vanishes wherever sigma is nonzero. Testing also with v_epsilon gives

integral sigma(A+∇φ)·∇v_epsilon=0.

Let R=sqrt(sigma)(A+∇φ), F=sqrt(sigma)A and G=sqrt(sigma)∇φ. These are L² because the support is compact. By (2), the last identities imply <R,F>=0. Equation(3) gives <R,G>=0. Since R=F+G, it follows that

||R||²₂=<R,F+G>=0.

Hence sqrt(sigma)(A+∇φ)=0 almost everywhere. Because sigma>0 almost everywhere on Omega,

(4) ∇φ=-A0 almost everywhere on Omega.

No uniqueness theorem for degenerate elliptic equations has been assumed. This conclusion follows directly from the actual weak equation and the explicit weighted approximation.

## 5. A compactly supported divergence-free test gives the contradiction

Define

B(x)=eta(q,z) A0(x),

again with zero extension near the axis. It is a smooth compactly supported vector field, vanishes outside the closure of Omega, and has divergence zero by the same radial calculation as for A. It is nonzero in Omega.

Since φ is H¹_loc and B is smooth and compactly supported,

integral_(R³) ∇φ·B = -integral_(R³) φ div(B)=0.

But (4) gives

integral_(R³) ∇φ·B
 = -integral_Omega eta(q,z)|A0|² dx < 0.

The integral is finite because r>=1 on the support, and strictly positive before its minus sign because eta is positive in Omega. This contradiction proves the theorem.

In particular an ordinary distributional gradient belonging to L²_loc cannot solve the equation: such a scalar distribution has an H¹_loc representative, up to constants, by the standard local Sobolev characterization. The source asks for an even stronger globally L² correction, so the obstruction applies to that target directly. It is not merely a failure of one normalization or of boundedness of a chosen solution operator.

## 6. What remains valid in a weighted completion

For any bounded nonnegative sigma and any A with sqrt(sigma)A in L², define

V_sigma = closure in L²(R³)^3 of {sqrt(sigma)∇v : v in C_c^∞(R³)},
G_A = -P_(V_sigma)(sqrt(sigma)A).

This is a well-defined bounded linear weighted correction. In the source's compact-support setting it is a continuous map from L²_rho to L², since the weight is bounded and compactly supported. Its flux

j_A = sqrt(sigma)(sqrt(sigma)A+G_A)

has zero distributional divergence by the defining orthogonality. The associated projected mass form is nonnegative and symmetric.

In the compact-support setting, if an ordinary H¹-local correction exists, a cutoff and H¹ approximation show its weighted gradient belongs to V_sigma. Its divergence equation then forces that weighted gradient to equal G_A. For the counterexample above, G_A=-sqrt(sigma)A and j_A=0, yet Section5 proves that no ordinary H¹-local potential represents it. Calling the abstract completion element “φ_A” is possible as notation, but it no longer supplies the Sobolev scalar potential or W(curl) reconstruction required in the original formulation. The theorem also does not exclude a discontinuous or distributional scalar whose gradient contains a singular term on the cut; that gradient is outside the source solution space.

This packet does not claim that every generalized variational formulation is impossible, or that the weighted projection lacks meaning. It also does not infer a separate theorem about existence for every forcing J_t in the full time-dependent problem. The exact target addressed is the ordinary correction map used to define that formulation.

## 7. Credit, checks and disposition

The source spaces and known positive-conductivity construction are credited to Arnold–Harrach2012. Hilbert-space projection, H¹ density and the standard circulation/gradient obstruction are classical. The explicit coefficient and approximation are written out so their hypotheses can be independently checked. The exact negative answer was already given by Ferudun (2026), Theorem 1.2; see PRIORITY_CORRECTION.md. No novelty of this particular proof detail or exhaustive oldest priority is certified.

The accompanying checker verifies the algebraic divergence and cylindrical identities, the single-valued piecewise potential, its exact angular energy, and scope controls. These finite symbolic checks do not replace the H¹ approximation or distributional-testing proof.

This completes substantive author turn1, with four turns remaining if the independent audit identifies a genuine gap or a source-scope mismatch. No final status promotion or PR before that full audit and the separate publication gate.
