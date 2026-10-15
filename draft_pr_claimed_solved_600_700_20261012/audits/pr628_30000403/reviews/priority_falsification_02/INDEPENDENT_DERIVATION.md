# Independent derivation checkpoint

Recorded UTC: 2026-10-15T03:36:53.824544+00:00
Completion estimate toward this falsification audit: 65%.

No other subagent report has been read. The candidate root derivation and required input packet were read; the derivation below was reconstructed from the source statements and the quotient construction.

Let H=PGL2 and let F be the reduced fiber of the geometric quotient at a k-point x. Characteristic zero makes k perfect, so F remains reduced over the algebraic closure. Its geometric underlying set is one orbit. The reduced orbit is H/E, smooth because E is finite etale. Thus F is a smooth H-homogeneous variety and [F/H] is an etale gerbe geometrically BE.

The associated representable projective-line family U=[(F x P1)/H] has coarse space Y. Geometrically U=[P1/E] and Y=P1/E=P1, so Y is a smooth projective genus-zero k-curve. On the complement of finitely many geometric points the E-action is free, and U agrees with Y on a nonempty open Y0. Pulling the resulting map Y0 -> [F/H] back along a geometric section of the gerbe gives an open subset of P1; its geometric fibers are irreducible of genus zero.

A y in Y0(K) is an H-torsor T with equivariant maps to F and P1. The latter map is a K-point of the associated conic C_T. Such a conic is split, so the corresponding class in H1(K,H) is trivial; a trivialization of T produces an element of F(K). This removes the strongest possible twist-versus-split objection.

A nonempty open of a conic over an infinite field has a closed point of degree <=2, by a k-line avoiding the boundary and the dual tangent conic. This yields the universal quadratic bound for every finite E, without needing a neutrality statement for the gerbe.

If E is noncyclic, Bresciani 2211.03438v1 Proposition 2 applies contrapositive to Y -> [F/H] and forces Y(k) nonempty. Then Y0(k) nonempty and F(k) nonempty. Every hypothesis is checked above. In particular E=V4 gives degree one. Independently, tame Riemann-Hurwitz gives three branch values for noncyclic finite E; their descended odd-degree divisor on Y forces Y to split.

Both cited Bresciani PDFs were independently fetched with matching SHA256. The exact Hurwitz theorem is not explicitly stated in them. The homogeneous-orbit construction and split-torsor argument are additional deductions, but short and formal. Source-sharpness and the precise reasonable-salvage assessment remain to be finalized.
