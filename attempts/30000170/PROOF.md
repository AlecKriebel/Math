# A quadratic complex-coefficient obstruction to unique nearest stable projection

**First substantive-turn candidate. Source/proof review is required before classifying the original target.** No novelty claim is made. The theorem concerns the complex coefficient convention of the cited polynomial variational theory, and the whole-epigraph set notion; it does not settle a real-only variant or the finite-subgradient function conjecture.

## 1. Precise statements

Identify the monic complex quadratics

    p(z)=z²+a z+b

with (a,b)∈C²=R⁴, with coefficient order (Re a,Im a,Re b,Im b). Let

    S={p: every root has real part at most zero}.

Let alpha(p) be the largest real part of a root. The following are the claims.

**Theorem A.** S is not prox-regular at p0(z)=z². For every neighborhood of p0 in coefficient space there is a polynomial having at least two distinct nearest stable monic quadratics. This holds for the standard Euclidean coefficient norm and for every fixed positive-definite real coefficient inner product.

**Theorem B.** The same local nonuniqueness conclusion holds when all exact-degree complex quadratics are allowed, including their leading coefficient near 1. The proof is in the full ambient coefficient space, rather than an inference from a monic slice.

**Theorem C.** The epigraph of alpha, as a set, is not prox-regular at (p0,0), both in the monic and full exact-degree complex frameworks. The obstructing normalized normals converge to a horizontal normal. This conclusion does not refute function prox-regularity at a fixed finite subgradient, since the unscaled gradients used below diverge.

“Stable” is the closed-left-half-plane convention explicitly stated in OWR 2/2005. All nearest points here are sought in coefficient space, not in a root-matching metric.

## 2. A necessary uniform support inequality

For a closed subset C of a finite-dimensional Euclidean space, prox-regularity at x0 implies that, near x0, bounded normal vectors satisfy a uniform quadratic support estimate. In particular, if

    x_t,y_t∈C,   x_t,y_t→x0,
    n_t∈N_C(x_t),   n_t→n0∈N_C(x0),

then for some fixed rho and all sufficiently small t,

    <n_t,y_t-x_t> ≤ (rho/2)||y_t-x_t||².             (1)

This is the elementary distance expansion in the definition of prox-regularity for the normal n0; see Poliquin–Rockafellar–Thibault (2000), Definition 1.1 and Proposition 1.2. If x_t is the nearest point to x_t+n_t/rho, comparison with y_t and expansion of squared distances gives (1).

We will use actual proximal normals at smooth boundary points. Their limits are limiting normals at x0. A violation of every fixed rho therefore disproves set prox-regularity. Theorem 1.3(a),(k) of the same primary paper then identifies the consequence for locally single-valued projections in finite dimension.

## 3. Explicit stable points and their full ambient normals

For t>0 define

    p_t(z)=z²+t² z+t²+i t³
          =(z+i t)(z+t²-i t).                     (2)

Its roots are -it and -t²+it. The first is simple and active, with real part zero; the other has strictly negative real part. Thus p_t lies on a smooth stable boundary. The active root remains simple and strictly dominates the other root locally, so alpha is smooth near p_t and the stable set is locally {alpha≤0}.

Implicit differentiation at the active root lambda=-it gives

    d lambda = -(lambda d a+d b)/(t²-2it).

Taking real parts in all four independent real coefficient directions yields

    grad alpha(p_t)
      = 2/[t(t²+4)] · n_t,
    n_t=(-t,-t²/2,-t/2,1).                         (3)

This is a full R⁴ gradient, including the imaginary linear-coefficient direction. It is not a normal computed only after imposing Im a=0. Its last component is nonzero. The positive multiple n_t of the smooth outward gradient is a proximal normal of S at p_t. For example, a local Taylor bound for alpha supplies the quadratic support inequality at this fixed point, with a constant allowed to depend on t.

The normal vectors are bounded and converge to

    n0=(0,0,0,1).

Since the p_t approach p0, n0 belongs to the limiting normal cone N_S(p0).

As a separate check of the boundary, write a=x+iy and b=u+iv. Shifting the variable by -iy/2 produces the polynomial

    z²+xz+(u+y²/4)+i(v-xy/2).

In the chart x>0, u+y²/4>0 its stability is equivalent to

    |v-xy/2| ≤ x sqrt(u+y²/4).

At p_t the upper inequality is active and the lower one is strict. The gradient of

    v-xy/2-x sqrt(u+y²/4)

is exactly n_t. This confirms the ambient normal and its outward sign without relying on an informal drawing of a coefficient slice.

## 4. Exact failure of the quadratic support bound

The comparison point is the equally explicit stable polynomial p_(sqrt(2)t). Its coefficient displacement from p_t is

    Delta_t=(t²,0,t²,(2sqrt(2)-1)t³).

Direct computation gives

    <n_t,Delta_t>=(2sqrt(2)-5/2)t³,                 (4)
    ||Delta_t||²=2t⁴+(2sqrt(2)-1)²t⁶.              (5)

The constant in (4) is positive: 2sqrt(2)>5/2. Thus

    <n_t,Delta_t>/||Delta_t||² → +infinity          (6)

at rate 1/t. Equations (2)–(6) contradict (1) for every fixed rho. This proves the set statement in Theorem A.

S is nonempty and closed, by continuous dependence of the roots of a monic fixed-degree polynomial on its coefficients. In finite-dimensional Euclidean space every point has a nearest point in a nonempty closed set. If all sufficiently nearby polynomials had unique nearest stable polynomials, Theorem 1.3(k) of Poliquin–Rockafellar–Thibault would imply prox-regularity at p0, contradicting (6). Therefore every neighborhood contains a polynomial with at least two nearest stable polynomials. Such a polynomial is necessarily outside S, since a point of S has itself as its unique distance-zero projection.

This is an existence proof of arbitrarily close nonunique projections. It does not claim that either p_t or p_(sqrt(2)t) is the unstable input or that those two particular boundary points are an explicitly identified nearest-point pair.

## 5. Other fixed coefficient inner products

Let G be any positive-definite real symmetric matrix defining the coefficient inner product. The covector in (3) represents the G-normal vector G^-1 n_t. These vectors remain bounded and converge, and

    <G^-1 n_t,Delta_t>_G=<n_t,Delta_t>.

There is a fixed constant M with ||Delta_t||_G²≤M||Delta_t||². Hence the support quotient for this metric still diverges by (4)–(5). The projection characterization applies in this finite-dimensional Hilbert metric as well.

This addresses fixed weighted Euclidean coefficient conventions. It does not claim that local unique projections are preserved merely because two arbitrary norms are equivalent, nor does it substitute a root-distance metric.

## 6. Exact degree without monic normalization

Write a full quadratic as l z²+a z+b with l near 1. The smooth normalization map is

    (l,a,b) ↦ (a/l,b/l).

The active root and abscissa depend on these normalized coefficients. At the monic point p_t, the full six-real-dimensional gradient is a positive multiple of

    N_t=(t³/2,-t², -t,-t²/2, -t/2,1),             (7)

where the first two entries are the real and imaginary leading-coefficient directions. This follows either by differentiating the normalization map or by the direct root formula

    d lambda = -(lambda² d l+lambda d a+d b)/(t²-2it).

The remaining four coordinates are exactly (3). Thus N_t is a genuine full ambient proximal normal, bounded and converging to the imaginary-constant direction.

The two comparison polynomials have the same leading coefficient, so their leading-coordinate displacement is zero. Consequently (4)–(6) hold unchanged with N_t. This proves failure of local prox-regularity in the full exact-degree setting, rather than relying on the potentially invalid inference from a non-prox-regular slice.

For projection existence and locality, choose a small closed coefficient ball C0 around z² on which every leading coefficient is nonzero. Let C be its intersection with the stable set. It is a nonempty compact set, and all p_t used above eventually lie in the interior of C0. Their local normals are unchanged, so C is not prox-regular at z².

For a polynomial q sufficiently close to z², every stable polynomial outside C0 is farther from q than z² itself, by the triangle inequality. Therefore nearest points in C and in the full exact-degree stable set agree. Theorem 1.3(k) applied to C supplies nonunique projections arbitrarily close to z², which are also nonunique nearest full exact-degree stable polynomials. The same localization works for any fixed positive-definite coefficient metric. This proves Theorem B.

## 7. The abscissa epigraph as a set

Let E=epi(alpha) in the monic coefficient space times R. At (p_t,0), the epigraph is locally the smooth sublevel alpha(p)-r≤0. From (3), a positive multiple of its outward gradient is

    v_t=(n_t,-t(t²+4)/2).                          (8)

It is bounded and converges to the horizontal vector (n0,0). Both (p_t,0) and (p_(sqrt(2)t),0) belong to E. Their height displacement is zero, so (4)–(6) give exactly the same support violation for (8). Thus E is not prox-regular at (z²,0).

Using N_t in place of n_t proves the full exact-degree version, with the same small closed localization if needed. Fixed positive-definite inner products are handled as in §5.

These are direct epigraph-set counterarguments. No unproved general equivalence between stable sublevel sets and epigraphs is used.

## 8. What the argument does and does not resolve

Under the complex-coefficient convention explicitly used by the source's cited variational theory, Theorems A and B give a negative answer to the literal nearest-stable-polynomial question already in degree two. Theorem C separately addresses the whole-epigraph projection description in the report.

However, the short report does not repeat its coefficient field or metric, while its opening control example uses real polynomials. The real-only variant is a distinct question: for monic real quadratics, stability is exactly a≥0 and b≥0, a convex set with unique projections. The complex construction is not a counterexample to that restriction.

Further, standard function prox-regularity at a fixed finite subgradient restricts attention to nearby finite subgradients and function values. The gradients in (3) diverge as t decreases, while the bounded epigraph normals in (8) converge horizontally. Therefore the present construction alone does not settle that finite-subgradient function question. Poliquin–Rockafellar (2010), p. 205, explicitly characterize function prox-regularity relative to v by epigraph prox-regularity relative to the normal (v,-1); the horizontal limiting normals here are outside that finite-v normalization. The broader 2005 roots-paper conjecture cited by Rockafellar–Wets Definition 13.27 is not claimed false here.

The imported clean statement's “equivalently” must not erase these distinctions. Independent source review must decide whether the original campaign target is exhausted by the literal complex projection statement or retains an additional real/function scope. If it retains the latter, this remains a first-turn partial result and the remaining substantive turns are still required. No novelty or historical-openness assertion is made.
