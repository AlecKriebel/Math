# Five substantive approaches and the exact remaining gap

The preliminary source recovery and duplicate screening are not counted as mathematical approaches. The bound below is five actual routes applied to the recovered equation. None resolves the original assertion.

## 1. Induction directly through the exact renormalized recurrence

Derived the triangular coefficient recurrence, including G/G(0,a), M−L−ay, and the N(a,b)−N(a,0) difference. Reconstructed g₁, evaluated L₁,M₁,N₁,y₁, and recovered g₂ as a rational symbolic identity. Origin boundary normalization follows conditionally by induction. This identifies a viable induction structure, but it does not prove closure of the coefficient space or existence of all integrals. Writing every expression as an operation-labelled syntax tree would be automatic and would not prove the source's particular rooted-kernel assertion.

## 2. Closure under the Cauchy divided difference

Proved D(KF)=K(I_leaf F)+∫I_leaf F/u, for every source-kernel forest F. This gives exact closure on every single rooted tree, with explicit all-size star-tree constants (m+1)!ζ(m+2). The remaining issue is D applied to arbitrary products multiplied by mixed rational coefficients in a,b. The actual N operator contains these expressions; the single-tree lemma does not cover all of them.

## 3. Conversion to harmonic polylogarithms and reverse-span testing

Proved that all rooted trees and their periods lie in the 0/1 harmonic-polylogarithm/MZV algebra. Derived the exact K word transformations. Tested the reverse leading-word spanning question exhaustively through weight 9, with full rank in each weight. An all-weight reverse-span proof is still absent, and broader hyperlogarithm closure would not by itself give the exact polynomial ring in a,b,A,B. Neither the weight-9 computation nor the source's third-order expansion has been promoted to an all-order claim.

## 4. Endpoint-preserving coefficient space

Tested whether the whole proposed generator ring, together with the mass/wavefunction conditions at the origin, is a sufficient induction domain. It is not. The symmetric polynomial f(a,b)=a²+b² has f(0,0)=0 and both first partial derivatives zero at the origin, but

L[f](a)=a²∫₀¹ dr/(1−r)

diverges for a≠0. This is a counterexample to an overly broad operator-closure lemma, **not** a counterexample to the conjecture about actual coefficients of G.

For g₁ the endpoint difference factors exactly by (1−r); for g₂ the verifier proves its rational symbolic endpoint cancellation, and the available logarithmic bounds then give convergence. The required missing invariant is an all-order endpoint-cancellation/divisibility statement for the actual recursion, strong enough also for y and repeated rational kernels. The fact that individual ring elements fail is why general polynomial-ring membership alone is not a valid induction hypothesis.

There is a second precision issue in the source's shorthand: the full 2009 paper explicitly includes multiple-zeta values in its conjectured coefficient ring, whereas the brief OWR statement suppresses them even though ζ(2) already appears in its displayed second-order coefficient. The 2009 paper also notes the divided function (I(a)−a)/a in a third-order footnote. This packet does not exploit shorthand omissions as counterexamples, and it does not silently enlarge the target ring to all rational functions.

## 5. Modern exact solution and renormalization bridge

Panzer–Wulkenhaar, arXiv:1807.02945v2, proves a Lambert-W answer in two dimensions. Its I_λ(a) derivative expansion is therefore related background, not a solution or duplicate of the present 4D rooted-tree problem.

Grosse–Hock–Wulkenhaar, arXiv:1908.04543v1 / JHEP 01 (2020) 081, gives the 4D Fredholm solution

J(x)=x·₂F₁(c,1−c;2;−x/μ²),    c=arcsin(πλ)/π,

for the auxiliary equation

J(x)=x−λx²∫₀^∞ J(t)/[(t+μ²)²(t+μ²+x)]dt.

Its all-order alternating-letter hyperlogarithm expansion concerns this auxiliary function. The two-point function is then reconstructed through a two-variable integral representation (Theorem 1). Matching its finite renormalization to ribbon-graph Taylor subtraction uses μ²=c(1−c)/λ with the removable value 1 at λ=0. Thus a free choice μ²=1 cannot simply be substituted at nonzero λ when identifying perturbative coefficients in the source normalization.

The current general quartic-model paper, arXiv:1906.04600v4 (6 August 2025), now published in Advances in Mathematics 481 (2025), 110551, is the version to cite. Its earlier v1 had a dimension-4 problem subsequently corrected. The current exact-solution theorem and its D=4 Taylor-subtraction discussion are credited; no independent reproof of those nonperturbative results is claimed.

Neither inspected modern statement supplies the required reduction of every reconstructed G coefficient to the source's precise a,b,A,B rooted-tree polynomial ring, with the stated subtraction and finite renormalization. A verified bridge of that kind could resolve the conjecture, but merely naming the hypergeometric solution does not. This is a bounded literature assessment, not certification that nobody has proved the missing bridge elsewhere.

## Final unresolved obligation

Starting with g₀=1 and the exact recursion, prove simultaneously for every n that:

1. its coefficientwise endpoint integrals and origin limit exist with the source subtraction prescription;
2. g_n has the source's restricted joint rational-prefactor/rooted-integral form, with the intended period convention;
3. all operations that introduce derivatives, removable quotients or products reduce back into that same form, rather than a larger rational or decorated-tree algebra.

Alternatively produce an actual coefficient of the normalized 4D G outside the intended class, with a proof of nonmembership. No such counterexample is present here. Status remains **unresolved, scoped partial results only**.
