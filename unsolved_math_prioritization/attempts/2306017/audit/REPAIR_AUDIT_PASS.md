# Narrow independent audit of the ordinary-radius repair

Audit date: 2026-10-03 UTC.

## Verdict

**PASS at the stated classical-theorem dependency level.** The revised argument establishes the full normalized-univalent-class minimum and supplies explicit attaining maps. The replacement comparison does not use the disputed biangle inequality or the unavailable 1999 coefficient lemma.

This verdict is specific to the revised packet. The original packet's unresolved source-sign discrepancy remains unresolved; it has been bypassed by a valid argument using a different invariant. This is not a formal proof-assistant certificate, a claim to have read the original 1999 proof, or an independent verification of full-class uniqueness in the nontrivial range.

The reviewed repair manifest has SHA-256 `0b2b338232706ec644a5dc5df6aa42b1ea2eb6c4ecd2d7dd610d4854f31ab9b8`. All eleven frozen repair entries and all eight original frozen entries match. The actual eight-file change set exactly matches OLD_TO_NEW.diff. The additional source fingerprints also match. Neither frozen packet was edited.

## 1. Authoritative source and its exact applicability

I independently inspected the supplied page images of [Dubinin (1994)](https://www.mathnet.ru/eng/rm1153), printed pp. 11–13 and 19–20. The source PDF has SHA-256 `ef1f9fa876488f0c408a0a571e0aafe2cd30de8e4f111cb34b91d320f6e53083`.

On pp. 19–20, the circular-symmetrization definition uses a strict angular inequality for an open set. The angular parameter is its actual angular measure when its intersection with a circle is nonempty and proper; the value is set to positive infinity only for an entire circle. Thus a circle missing a single point, although still of angular measure 2 pi, becomes a circle missing its negative point. The repair's use of this convention is correct.

For one interior marked point at zero and the function psi(r)=r, (1.17) reads M(V,0)<=M(V*,0). Equation (1.8) identifies this M with log R/(2 pi); p. 12 identifies the inner radius with conformal radius in the simply connected setting. Hence R(V,0)<=R(V*,0), with exactly the sign and hypotheses required here. This is an interior conformal invariant. There is no appeal to the disputed boundary-biangle invariant.

The ordinary-radius inequality remains a stated classical external theorem. Its application and normalization have been checked; no claim is made to reprove all capacity results underlying the survey.

## 2. Domain topology and preservation of punctures

For the initial reduction, f extends univalently past the closed disk, so its image Omega is a bounded Jordan domain containing zero. The later radial approximation justifies making this assumption.

The radial image of a connected domain containing zero is an interval starting at zero. Every nonempty circle section of its circular symmetrization contains the positive radial point, and is joined to it by a centered open arc or a complete circle. This proves connectedness of the rearranged set. Its openness is also consistent with the source definition: for an open original set, compact subarcs persist under small radial changes; an entire contained circle persists on a nearby annulus.

Let delta be the distance from zero to the complement of Omega. That complement is connected and unbounded, so its set of radii contains every s>=delta. Therefore every such original circle is missing at least one point. In the rearrangement, all corresponding complementary arcs or singleton points include -s. These sets attach to the connected ray (-infinity,-delta]. The rearranged complement is consequently connected. The rearranged domain is bounded, connected, and has connected complement, so it is simply connected.

A terminal negative slit merely lengthens this connected complementary ray. It does not disconnect the domain: all remaining circle sections still join the positive radial segment. The same reasoning applies to E_x and E_x*, since E_x is a conformal image of the simply connected slit disk and remains bounded. In particular, no puncture is filled silently and no disconnected component is discarded.

## 3. Restoring conformal radius one

For C=Omega*, its negative real portion is precisely (-delta,0). The sets C_t=C minus (-infinity,-t], 0<t<=delta, are simply connected domains containing zero. At t=delta no extra point of C is removed, so R(C_delta,0)>=R(Omega,0)=1.

Their distance from zero to the boundary is exactly t. Koebe's quarter theorem therefore gives R(C_t,0)<=4t, which tends to zero at the other end of the parameter interval. At any positive parameter t0, compact subsets of C_t0 are contained in C_t for all sufficiently close t, while no open neighborhood crossing the limiting slit can enter the kernel. Hence the kernel limit is exactly C_t0, from either direction. The standard kernel theorem gives continuity of conformal radius. The intermediate value theorem supplies t with R(C_t,0)=1.

Only the weak symmetrization inequality is needed. This construction also covers the case R(C,0)=1, by taking t=delta. It requires no strictness or equality classification for the symmetrization theorem.

## 4. Negative-slit inclusion and strict contradiction

Fix x in (0,1), and put U_x=disk minus [-1,-x], c=|f(-x)| and T=-G(-x), where G is the normalized map onto C_t.

Symmetry and injectivity make G and its inverse real-symmetric. G' is real and nonzero on the real interval, and has positive sign there because G'(0)=1. The interval (-1,0) therefore maps monotonically onto (-t,0). In particular, 0<T<t<=delta, and removal of (-1,-x] removes exactly (-t,-T]. Thus

G(U_x)=C minus (-infinity,-T].

The complement of E_x=f(U_x) contains f([-1,-x]) joined to the unbounded complement of Omega at f(-1). This connected set contains f(-x) and points of arbitrarily large modulus. Continuity of modulus implies that it meets every circle of radius s>=c. The symmetrization convention verified above therefore excludes -s from E_x* for every such s. Monotonicity of rearrangement under set inclusion also gives E_x* subset C. Together,

E_x* subset C minus (-infinity,-c].

Suppose c<T. Since T<delta, every -s with c<s<T belongs to C and to G(U_x), but is absent from E_x*. Therefore E_x* is a proper subdomain of G(U_x). Both domains are simply connected and contain zero.

Strict conformal-radius monotonicity applies to this proper inclusion. One may prove the strictness directly: compose the two normalized Riemann maps to obtain a disk self-map fixing zero; equality of radii would force a rotation by Schwarz's lemma and thus equality of the image domains. No boundary regularity or equality case of the symmetrization theorem is needed.

Conformal covariance and f'(0)=G'(0)=1 now give

R(U_x,0)=R(E_x,0)<=R(E_x*,0)<R(G(U_x),0)=R(U_x,0),

which is impossible. Consequently -G(-x)<=|f(-x)|. The inclusion, strictness, and direction of this comparison all check.

## 5. Coefficient consequence, area and exhaustion

Choose the rotation of f with a2=a>=0, and write G(z)=z+bz^2+..., where b is real. The negative-ray expansions are

-G(-x)=x-bx^2+O(x^3), and |f(-x)|=x-ax^2+O(x^3).

The preceding comparison yields b>=a. The sign is correct: reversing the slit direction without changing this Taylor calculation would not be harmless.

Real symmetry and injectivity imply that G is typically real: a nonreal point with a real image would collide with its conjugate, and the imaginary-part sign in the upper half disk is determined near zero. G is bounded and normalized; the second-coefficient theorem and its equality case give b<2. Thus for a>1/2 the already-checked typically-real energy estimate applies to G. Since G is univalent, its energy equals ordinary area. Circular rearrangement and removal of a line segment preserve area, yielding

A(f)=A(G)>=M(b)>=M(a).

The coefficient range a<=1/2 has its separate direct proof. For arbitrary f in S, f(rho z)/rho is univalent in a neighborhood of the closed disk whenever rho<1. Its area is the monotonically increasing coefficient sum in the packet, tending to A(f), possibly infinity. Its second coefficient tends to the prescribed one. Continuity of M on [0,2) therefore proves the asserted bound for all S. No convergence of the rearranged domains as rho tends to one is required.

## 6. Scope corrections and checks

The changes correctly distinguish Dirichlet energy from ordinary image area for nonunivalent typically-real functions. They retain full-S uniqueness in the range 1/2<a<2 as an attributed published result, rather than an independently proved conclusion. They explicitly retain the original biangle-source conflict as unresolved and unused. No unsupported stronger equality assertion was introduced elsewhere in the revised files.

The explicit extremal and the typically-real calculation are unchanged apart from the necessary energy notation, so the earlier successful checks of those parts continue to apply. The revised author's script passes all 16 exact checks, including the two new Taylor-direction identities. Its fresh output agrees exactly with the recorded verification.json. These algebra results support the calculation but are not substitutes for the geometric reasoning above.

`audit_repair.py` and `audit_repair.json` provide reproducible integrity, actual-diff, source-fingerprint, scope, and script-rerun controls. This narrow audit supplies no new theorem or priority claim and does not resolve the old source discrepancy.
