# Approach 3: extension across a general nondegenerate moving free boundary

**Problem:** 30004633. **Author continuation:** approach 3. **Status:** candidate conditional theorem, awaiting independent review. This approach removes the radial/quadratic Barenblatt restriction by constructing a signed-pressure certificate across arbitrary smooth moving free boundaries. It does not solve arbitrary irregular weak solutions or wall contact.

## 1. A geometric pressure class

Fix m>1 and a finite time interval I=[a,b]. Let Ω be a bounded Lipschitz domain. Suppose D(t) is a smoothly moving, bounded open set whose closures lie in Ω, at a uniform positive distance from its physical boundary. Multiple components are allowed. Assume:

1. The spacetime family ∂D(t) is smooth, with a uniform two-sided tubular radius. Equivalently for present purposes, the normal-coordinate maps (ξ,s)↦ξ+s n(t,ξ), |s|<s0, are smooth diffeomorphisms onto collars, with uniformly bounded derivatives of the finite orders used below.
2. A pressure p(t,x)>0 is smooth up to the moving closure of D(t), p=0 on ∂D(t), and satisfies inside D(t)
   \[
   p_t=(m-1)p\Delta p+|\nabla p|^2.
   \tag{1.1}
   \]
   Smoothness here can be read literally as C∞ on the moving closure; the proof needs only bounded finite jets sufficient for a C¹-in-time, C³-in-space extension with bounded mixed gradient ∇p_t. This deliberately convenient formulation makes no sharp-regularity claim.
3. The outward normal derivative is uniformly nondegenerate:
   \[
   -\partial_n p(t,\xi)\ge c_0>0\quad(\xi\in\partial D(t)).
   \tag{1.2}
   \]
4. The density
   \[
   \rho(t,x)=\left({m-1\over m}p(t,x)\right)^{1/(m-1)}\mathbf1_{D(t)}(x)
   \tag{1.3}
   \]
   has mass one initially.

These hypotheses allow density vacuum and a nonzero interior limiting force at its boundary. For example every positive-time Barenblatt profile with fixed physical-wall clearance belongs to this class. They exclude waiting-time degeneracy, topology changes, loss of a uniform collar, and contact with the physical wall.

## 2. Signed extension lemma

There exists q on I×Rᵈ with the following properties:

- q=p on D(t), q<0 outside its closure, and q_+=p 1_D;
- q is C¹ in time and C³ in space, with bounded ∇q, D²q, D³q, q_t, and ∇q_t;
- u=−∇q is supported in a fixed compact subset of Ω;
- for
  \[
  \mathcal R=q_t-|\nabla q|^2+(m-1)q\operatorname{div}(-\nabla q),
  \]
  there is a uniform C_R such that
  \[
  |\mathcal R(t,x)|\le C_R(-q(t,x))\mathbf1_{\{q<0\}}.
  \tag{2.1}
  \]

### Proof

Use exterior tubular coordinates x=ξ+s n(t,ξ), s≥0. The outward normal derivatives below mean derivatives along the straight normal ray, evaluated from the interior at ξ. Define for sufficiently small s≥0

\[
q_{ext}(t,\xi+s n)=\sum_{j=1}^{4}{s^j\over j!}\partial_n^j p(t,\xi).
\tag{2.2}
\]

Keep q=p inside D(t). Taylor's formula in the same normal coordinates shows matching of spatial derivatives through order four at s=0; tangential derivatives match by differentiating the boundary jets. The smooth time dependence of the boundary and jets gives the stated mixed time regularity. Thus this piecewise definition has more regularity than is needed for the estimate.

From (1.2) and uniform bounds on the remaining coefficients, after decreasing the collar width δ>0 if necessary,

\[
q_{ext}(t,\xi+s n)\le -\tfrac12 c_0 s
\quad(0<s\le\delta).
\tag{2.3}
\]

Choose a smooth function χ(s) equal to one on [0,δ/3], zero on [2δ/3,∞), and between zero and one. For an arbitrary κ>0 replace (2.2) in the exterior collar by

\[
q=\chi(s)q_{ext}-(1-\chi(s))\kappa,
\tag{2.4}
\]

and set q=−κ outside the exterior collar. Keep q=p inside. Since the cutoff is constant near both ends, this glues with the asserted regularity. The uniform physical-wall clearance makes the support of ∇q a fixed compact subset of Ω.

It remains to prove (2.1), the substantive point. Inside D(t), R=0 by (1.1). By taking the interior boundary trace of (1.1), p=0 implies

\[
p_t=|\nabla p|^2\quad\text{on }\partial D(t).
\tag{2.5}
\]

All these jets are preserved by the extension; thus R=0 at s=0. Its spatial Lipschitz norm in the small collar is bounded, so |R(t,ξ+s n)|≤C s. Together with (2.3), this proves |R|≤(2C/c0)(−q) on 0<s≤δ/3. In the cutoff region s≥δ/3, both q_ext and −κ are bounded above by a fixed negative constant. Their convex combination has the same property, and boundedness of R then proves (2.1). Outside the collar q is a fixed negative constant and R=0. This proves the lemma.

The construction uses the equation only in the positive-density region and its boundary trace. It does not require the signed extension to solve the pressure equation in vacuum.

## 3. Kinematic and conservation identities

Since p(t,ξ(t))=0 along a boundary trajectory and tangential derivatives of p vanish there, (2.5) implies its outward normal speed

\[
V_n=-p_t/\partial_n p=-\partial_n p=u\cdot n.
\tag{3.1}
\]

Hence the globally Lipschitz flow of u maps D(a) onto D(t). In the interior, (1.1) implies

\[
\rho_t+\operatorname{div}(\rho u)=0.
\tag{3.2}
\]

There is no interface measure in (3.2): ρ is continuous to zero at the interface, and its normal flux ρu has zero trace. More explicitly, in a collar ρ=O(s^{1/(m−1)}), while its interior first derivatives have the locally integrable size O(s^{1/(m−1)−1}). Integration by parts on sets with distance at least h from the boundary has boundary terms O(h^{1/(m−1)}), which vanish as h↓0. The same argument, or change of variables under the smooth flow, proves preservation of mass and the material pushforward identity.

For P(t)=∫ρᵐ, the pressure power relation and (3.2) give

\[
P'=\int\rho q_t=-(m-1)\int\rho^m\operatorname{div}u.
\tag{3.3}
\]

Differentiation of the first expression is justified because r↦(r_+)^{m/(m−1)} is C¹. For the second identity one may apply the ordinary chain rule in the positive region and send the collar thickness to zero; its boundary terms vanish even faster, like h^{m/(m−1)}. Thus the reference identities used by the discrete estimate hold without assuming the density itself is smooth across the free boundary.

## 4. Convergence theorem for the original scheme

Use exactly the Hilbert space, particle partition, compact-domain energy, and frozen-proximal scheme defined in Approach 2, with ρ0=ρ(a). Let X(t,·) be the flow of u with X(a)=Id. Put δ_N²=||Π_NId−Id||²_{L²(ρ0)}. For 0<ε≤1 and τ≤ε,

\[
\sup_{a\le t\le b}\|X_N(t)-X(t)\|_{L^2(\rho_0)}^2
 +\int_a^b\|\dot X_N(t)-\dot X(t)\|_{L^2(\rho_0)}^2dt
 \le C\left({\delta_N^2\over\varepsilon}+\varepsilon+{\tau\over\varepsilon}\right).
\tag{4.1}
\]

Here C depends on the fixed smooth reference solution and its collar/clearance constants. As before, this is a material-velocity estimate, not a quantitative evaluation theorem for the discontinuous zero-extended physical velocity at particle positions.

### Proof

For any reconstructed density r, the signed relative energy

\[
e(t,x,r)={r^m\over m-1}-q(t,x)r+\rho(t,x)^m
\]

is nonnegative and dominates (−q)r in vacuum. The extension lemma gives |∫rR|≤C_R∫e. Compact support of u inside Ω makes its positive and negative perturbations admissible in the proximal minimization. The variation identity is therefore

\[
\varepsilon^{-1}\langle Y_n-X_N(t_n),u(t,Y_n)\rangle
 =\int r_n^m\operatorname{div}u.
\]

Define the same frozen modulated energy Z_n as in Approach 2. Identities (3.3) and the residual definition give exactly the same cancellation

\[
-\int r_n^m\operatorname{div}u+\int r_n(|u|^2-q_t)+P'
 =-(m-1)\int e\operatorname{div}u-\int r_nR.
\]

The bounded gradient of |u|²−q_t supplies the evaluation commutator, bounded ∇u controls the spatial commutator, and the frozen-step defect is bounded by (Δ_n+τ||u||∞²)/(2ε). All estimates and node jumps in Approach 2 §§5–7 now apply verbatim, with no use of the radial formula after these reference identities have been established. This proves (4.1).

## 5. What is and is not gained

The new mathematical content is the collar construction and residual divisibility estimate (2.1) for a general moving hypersurface. It yields convergence for a nonradial free-boundary class with genuinely nonsmooth zero-extended density/velocity. The proof is conditional on regularity and nondegeneracy of the exact pressure geometry, and does not establish those hypotheses for arbitrary porous-medium initial data. In particular it cannot presently be used across waiting-time interfaces, merging supports, singular interfaces, or physical-wall contact. This is a substantive extension of Approach 2, not a claim that all irregular porous-medium solutions are settled.
