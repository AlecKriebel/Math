# E-6322 pass 2: the a.e. inverse is a Sobolev map with the full inverse trace

Checked 16 October 2026 against the frozen target and pass-1 adversarial audit. This strengthens the established baseline for **every finite-energy competitor**, without minimality. It does not assert a homeomorphism, a positive essential Jacobian lower bound, or equivalence with an unconstrained inverse minimization problem.

## 1. The applicable primary theorem

Marco Bresciani, Elisa Davoli and Martin Kružík, *Existence results in large-strain magnetoelasticity*, Ann. Inst. H. Poincaré ANL 40 (2023), 557–592, DOI 10.4171/AIHPC/51:

https://ems.press/content/serial-article-files/28047?nt=1

The relevant result is Proposition 2.5, pp.566–567 (PDF pp.10–11). Section 2, pp.562–563 supplies the standing assumptions: a bounded Lipschitz domain in dimension three and Sobolev exponent p>3. Proposition 2.5 assumes positive determinant and almost-everywhere injectivity, and proves that the almost-everywhere inverse belongs to W^{1,1}, with weak derivative equal to the inverse gradient composed with the inverse. Its proof uses the Piola identity, Sobolev composition and the change-of-variables formula. It does not assume homeomorphism.

The inverse is defined on the open set Ω^y=y(Ω)\y(∂Ω). Lemma 2.1 and Remark 2.3, pp.563–565, identify this set with the topological image. The precise inverse definition is equation (2.1), p.565. Proposition 2.5 was checked in extracted full text and visually on printed p.566. Its theorem is used independently of the paper's magnetoelastic energies or later higher-gradient regularization.

## 2. Application to the entire frozen class

Write D=G(Ω), F=Dy, C=cof F and J=det F. Pass 1 already established that every E-6322 competitor is continuous on the closure, has J>0 a.e., is a.e. injective, and satisfies the area formula. The full trace gives

\[
\deg(y;\Omega;z)=\deg(G;\Omega;z)=1\quad(z\in D),
\]

and zero off G(closure Ω), for z away from the boundary image. Thus Ω^y=D exactly. This remains valid for domains with holes.

Proposition 2.5 now gives a genuine weak derivative, not merely an algebraically defined measurable matrix field:

\[
v=y^{-1}\in W^{1,1}(D;\mathbb R^3),\qquad
Dv(z)=F(v(z))^{-1}\quad\text{a.e.},\qquad
K(z):=\det Dv(z)=J(v(z))^{-1}>0.
\]

The inverse is an equivalence class defined almost everywhere. Exceptional fibers of y may be non-singletons; no choice on a target null set upgrades this result automatically to a continuous inverse.

## 3. Actual Sobolev and minor estimates

The algebraic estimates of pass 1 now apply to the weak derivative. Change variables z=y(x) and use Hölder:

\[
\begin{aligned}
\int_D|Dv|^{9/5}\,dz
 &=\int_\Omega |C|^{9/5}J^{-4/5}\,dx\\
 &\le\left(\int_\Omega|C|^3\right)^{3/5}
       \left(\int_\Omega J^{-2}\right)^{2/5},\\
\int_D|\operatorname{cof}Dv|^{9/4}\,dz
 &=\int_\Omega |F|^{9/4}J^{-5/4}\,dx\\
 &\le\left(\int_\Omega|F|^6\right)^{3/8}
       \left(\int_\Omega J^{-2}\right)^{5/8},\\
\int_D K^3\,dz&=\int_\Omega J^{-2}\,dx.
\end{aligned}
\]

As v takes values in bounded Ω a.e., v belongs to every finite L^q and in particular

\[
\boxed{v\in W^{1,9/5}(D),\quad\operatorname{cof}Dv\in L^{9/4}(D),\quad\det Dv\in L^3(D).}
\]

The transformation of the complete energy is consequently an identity involving weak derivatives:

\[
I(y)=\int_D\left[
 a\frac{|\operatorname{cof}Dv|^6}{K^5}
+b\frac{|Dv|^3}{K^2}
+\frac cK+dK^3\right]dz.
\]

This fills the weak-inverse-derivative gap explicitly left open in the pass-1 variational audit. It is an application of established inverse regularity plus direct algebra, with no novelty claim.

## 4. The full inverse boundary trace

The boundary claim below is a deduction for the frozen smooth data; it is not a quoted extra conclusion of Proposition 2.5.

Choose a sufficiently small smooth outward parallel domain Ω̃ with closure Ω compactly contained in Ω̃ and closure Ω̃ contained in U. Such a choice exists by the smooth compact boundary and its tubular neighborhood, also when Ω has holes. Glue

\[
Y=y\quad\text{on }\Omega,\qquad Y=G\quad\text{on }\widetilde\Omega\setminus\overline\Omega.
\]

Matched traces give Y∈W^{1,6}(Ω̃), while positivity and finite energy hold on both pieces. The full outer trace is G. Applying the same degree argument and Proposition 2.5 gives an inverse V∈W^{1,9/5}(G(Ω̃)). On D it equals v a.e.; on G(Ω̃)\closure D it equals G^{-1} a.e. This follows from a.e. injectivity of Y and the fact that its prescribed collar map is G.

The smooth hypersurface ∂D lies strictly inside G(Ω̃). Uniqueness of Sobolev traces from the two sides therefore yields

\[
\boxed{\operatorname{Tr}_{\partial D}v=G^{-1}|_{\partial D}.}
\]

This is a full-boundary Sobolev trace statement. No pointwise extension of v or trace of Dv is asserted.

## 5. Limits of the improvement

- The derivative exponent 9/5 is below dimension three, so this result does not yield inverse continuity by Sobolev embedding.
- The determinant is in L^3, not L^∞. The desired primal lower bound is precisely the missing upper bound for K after this change of variables.
- The inverse variational comparison class remains the set of genuine a.e. inverses of admitted primal competitors. A generic W^{1,9/5} map with the displayed minor integrability and inverse boundary trace has not been proved to be in that class. Thus global minimality for the transformed energy over every finite-energy Sobolev map must not be asserted.
- The admissible collapsed-segment example from pass 1 is compatible with this theorem: its inverse can have a discontinuity on an exceptional target set while remaining Sobolev.

Independent review checked the primary theorem's hypotheses and the collar trace argument during this pass. The target's unconditional positivity claim remains unresolved.
