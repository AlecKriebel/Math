# Independent review: constant-area strips at small fixed width

## Verdict

**PASS for the stated partial theorem.** For a compact convex body in three dimensions with $C^{2,\alpha}$ boundary, the one-width strip hypothesis implies that the body is a ball when the prescribed width $h$ satisfies $h<2r_{\mathrm{in}}$. The averaging, analytic continuation, and application of Reichel's electrostatic theorem are valid. No required mathematical correction was found.

**The full source problem remains unresolved by this package.** Neither the large-width regime $h\ge2r_{\mathrm{in}}$ nor arbitrary nonsmooth convex boundaries is covered. The disconnected nested-sphere example is a scope diagnostic, not a counterexample to the intended convex problem. No novelty or external-peer-review claim is certified.

- Target: **7000019 / AMR-069-0019**.
- Frozen artifact: `PROOF.md`.
- SHA-256: `acd8d7f8d98d7500cb2c09cb724bdceb187993634b76579aff4febf7715015d7`.
- Review date: 2026-09-30 UTC.
- Separate reviewer: `gpt-6-astra`, effort `xhigh`.

## 1. Exact original scope

[Ghomi's survey](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), Problem 4.3 on printed p. 12, concerns one fixed positive separation of parallel planes, below the diameter. It does not provide a family of widths tending to zero. The question occurs in the convex-surfaces section. More decisively, [Ghomi's own 2017 formulation](https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere) explicitly defines the surface as the boundary of a compact convex set with nonempty interior. The candidate preserves that intended scope and clearly labels its two additional hypotheses.

The theorem's strip condition uses a single constant across all admissible positions and directions, not one direction-dependent constant. Its bounding planes may be tangent because they are required to intersect the surface. The proof and its width lemma use that stated convention. The main averaging argument uses strictly interior plane levels and therefore has no tangency ambiguity.

Kim–Kim's [Proposition 2 and Theorem 3](https://arxiv.org/abs/1208.5361) concern cap-area functions over varying sufficiently small heights. They cannot be substituted for the single fixed-width hypothesis. The candidate treats them only as related work.

## 2. Centered slabs really are admissible

Set $a=h/2$. The inradius assumption supplies a point of the open set

$$E=\{x\in\operatorname{int}K:\operatorname{dist}(x,\partial K)>a\}.$$

A ball of radius strictly greater than $a$ about each $x\in E$ lies in $K$. Hence each of the planes $u\cdot(y-x)=\pm a$ passes through the interior of $K$. Its section with the bounded convex body is a nonempty planar convex set with relative interior; its relative boundary lies on $\partial K$. Thus both planes intersect the surface, as required. Merely showing intersection with the solid would be insufficient without this last observation; the candidate includes it.

The set $E$ is open by continuity of the distance function. Only its nonemptiness is needed; connectedness is required later for the whole interior of $K$, which follows from convexity.

## 3. Averaging and normalization

For any $z$ with $|z|>a$, the orientation condition $|u\cdot z|\le a$ selects a spherical zone. In longitude and vertical-coordinate variables, ordinary unit-sphere area is $d\theta\,ds$, so its area is exactly

$$4\pi a/|z|.$$

This is an integral over the **unit sphere of directions**, not a solid-angle normalization with total mass one. Every boundary point $y$ satisfies $|y-x|>a$ when $x\in E$. Tonelli's theorem therefore gives

$$4\pi C=4\pi a\int_{\partial K}|x-y|^{-1}\,dA(y).$$

The resulting potential is $U=C/a=2C/h$. Both factors of two and $4\pi$ are correct. On a sphere of radius $R$, the area is $C=2\pi Rh$ and the unnormalized interior potential is $4\pi R$, providing a consistent control.

No conditional integral or limiting interchange is present. The surface is compact with finite area, and the kernel stays a positive distance from its singularity on each compact interior subset.

## 4. Harmonic continuation and the imported rigidity theorem

Differentiating the Newtonian kernel under the surface integral on an interior compact set is justified by its positive separation from the boundary. The kernel is harmonic away from the source point, so $U$ is harmonic in the interior. Harmonic functions are real analytic. A harmonic function that agrees with a constant on a nonempty open set agrees with that constant throughout the connected interior. This is a valid unique-continuation application; knowing only one interior value would not suffice.

[Reichel 1996](https://ems.press/content/serial-article-files/34877), Section 2, printed p. 622, was inspected in both text and typeset form. It explicitly starts with a bounded $C^{2,\alpha}$ domain with connected exterior and defines an equilibrium charge by constancy of its single-layer potential in the body. It states the corresponding constant-density rigidity result and reduces it to the exterior overdetermined problem proved in Section 4.

The match is exact here: take the interior of $K$, whose exterior is connected; the density is the positive constant one; and the boundary has the assumed regularity. Reichel's kernel is $1/(4\pi r)$, while the candidate uses $1/r$, a harmless global scaling. Equivalently, the normalized exterior potential has constant Dirichlet data and constant negative normal derivative by the jump relation, tends to zero at infinity, and satisfies the exterior harmonic rigidity hypotheses. No unmentioned star-shapedness, strict convexity, or analytic-boundary hypothesis is needed.

## 5. Width lemma and the actual remaining gap

The directional width is continuous on the connected sphere of directions and its maximum is the Euclidean diameter. If some width is at most $h$ while the diameter is greater than $h$, an intermediate direction has width exactly $h$. The slab between its two supporting planes contains the entire surface, so the common strip area equals total area. A direction of width greater than $h$ has an admissible strictly interior strip which excludes a nonempty relatively open surface cap of positive area. That contradiction proves the necessary bound $\min w>h$ under the stated intersection convention.

It does not establish $h<2r_{\mathrm{in}}$. The tetrahedron control is correct. Its edge differences give $w(u)=2(a+b)$, where $a\ge b\ge c\ge0$ are the absolute direction coordinates. Since $2ab\ge c^2$, the minimum unit-direction width is two, attained on a coordinate axis. Its four face planes have distance $1/\sqrt3$ from the origin. Their inward normals sum to zero, so the smallest face distance from any interior point cannot exceed their common centered value; this also confirms the inradius exactly. Thus $h=3/2$ lies strictly between $2r_{\mathrm{in}}$ and the minimum width.

That tetrahedron is not asserted to have constant strip areas. It only blocks a general geometric shortcut. At $h\ge2r_{\mathrm{in}}$, the particular open set $E$ is empty, so there is no open set of constant Newtonian potential from which to continue. The candidate does not conceal this failure.

The one-dimensional density diagnostic is also correct: an $h$-periodic positive nonconstant density has the same integral over every length-$h$ interval. A fixed-width sliding integral gives periodicity of a derivative where it exists, not constancy. The missing all-direction compatibility is not supplied by that diagnostic.

## 6. Disconnected-surface control

For concentric spheres of radii two and one-half, with width three, both planes meet the union exactly when the lower offset lies in $[-2,-1]$. Every such slab contains the entire inner sphere. The outer spherical strip has area $12\pi$ and the inner sphere contributes $\pi$, so the total is $13\pi$, independent of direction and position. The union is not the boundary of a convex body. Its use as a warning is valid; using it as a solution of Ghomi's intended convex question would not be.

## 7. Reproduction and disposition

The submitted checker was copied and replayed without changing the author's files. All **1,056 exact controls passed**. A separately written checker, importing no candidate code, passed **266 exact controls** under SymPy 1.14.0. It checks the spherical coordinate area element, the angular integral, Newton-kernel harmonicity, the sphere normalization, the tetrahedron support and inradius controls, the periodic-density example, and the complete admissible offset interval of the nested spheres.

From this review directory:

```sh
python3 submitted_verify.py > verification.json
python3 independent_checks.py
```

The independent script writes `independent_results.json`. Finite algebraic controls do not prove the potential-theoretic rigidity theorem; its exact published scope was checked separately above.

**Final disposition:** suitable for a draft PR as a reviewed, explicitly scoped partial theorem, with no full-source solved claim. Retain the strict inradius inequality, the boundary regularity, the intended convex-body assumption, and the priority disclaimer.

## Final status-header snapshot

The author subsequently changed only the status line to record this completed review. Replacing that single line with its previous text reproduces the original reviewed SHA-256 exactly, so the mathematical content is unchanged. The PASS verdict also covers final `PROOF.md` SHA-256 `147b64bc267744e83ede73f7e89200c21931585f91e3e639cf0efc7bd7de5e46`. The full source problem remains unresolved.
