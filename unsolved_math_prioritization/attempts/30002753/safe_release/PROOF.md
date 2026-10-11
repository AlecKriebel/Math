# Random-transposition entropic curvature: five approaches and exact gaps

Problem 30002753, OWR-13359-003. Research date: 5 October 2026.
Disposition: unresolved after five investigative approaches. No novelty or priority claim.

## 0. Statement, conventions, and scope

The inspected primary problem is Jan Maas's contribution in *Variational Methods for Evolution*, Oberwolfach Report 57/2014, pp. 3227–3229, specifically the paragraph after Theorem 3. It asks for the correct asymptotic order of the optimal entropy-geodesic-convexity constant for random transpositions. The source gives a lower bound 4/[n(n−1)] and upper bound 2/(n−1). The exact UnsolvedMath URL was inaccessible; correspondence is based on the catalog identifier, title, DOI and the primary paragraph, not a verified byte-for-byte website statement. The website might impose a stronger exact-constant formulation; neither formulation is solved here.

Let n≥2, d=n(n−1)/2, q=1/d, X=S_n and μ=1/n!. Connect σ and τσ for every transposition τ of two distinct labels. Use continuous time with

L f(σ)=q Σ_τ [f(τσ)−f(σ)].

Thus the total jump rate is 1. The stationary measure is uniform. A density ρ is positive and has μ-average 1. Write θ(a,b)=(a−b)/(log a−log b), with θ(a,a)=a, for the logarithmic mean. Set g_xy=ψ(y)−ψ(x), and

A(ρ,ψ)=μq Σ_{unordered edges {x,y}} θ(ρ_x,ρ_y) g_xy²,

B(ρ,ψ)=μq Σ_{unordered edges {x,y}} {½[θ_1(ρ_x,ρ_y)Lρ_x+θ_2(ρ_x,ρ_y)Lρ_y]g_xy² − θ(ρ_x,ρ_y)g_xy[Lψ_y−Lψ_x]}.

The established entropy-Hessian criterion identifies the optimal entropic curvature as

κ_n=inf_{ρ>0, ψ nonconstant} B(ρ,ψ)/A(ρ,ψ).

We use this criterion from Erbar–Maas–Tetali (2015), Theorem 2.2, as a background theorem; we do not reprove the Riemannian equivalence here. Positivity of A follows from connectedness. Homogeneity of θ implies A(cρ,ψ)=cA(ρ,ψ), B(cρ,ψ)=cB(ρ,ψ), so unnormalized positive test densities give legitimate quotients after normalization.

This curvature uses the logarithmic-mean transport metric on probability densities. It is not the ordinary W_1 Ollivier curvature of the Cayley distance, a sectional-curvature condition, or a log-Sobolev constant. The Cayley distance specifies adjacency only. Classical W_2 on this finite metric space is not the metric used here.

If rates are multiplied by c>0, A becomes cA and B becomes c²B, so κ becomes cκ. For the lazy kernel P_α=(1−α)I+αP with 0<α≤1, the associated generator P_α−I is αL and its entropic curvature is ακ_n. If two labels are independently selected from [n], allowing identity moves, its generator has rate 2/n² per nonidentity transposition and curvature (n−1)κ_n/n. In unnormalized rate-one-per-transposition time the curvature is dκ_n. None of these are statements that discrete-time entropy itself has a continuous geodesic second derivative. At n=1 the state space is a singleton and the positive-dimensional Rayleigh quotient is absent; no finite κ_1 is assigned.

## 1. Uniform-density spectral approach

At ρ≡1, Lρ=0 and θ=1. Reversibility gives

A(1,ψ)=−⟨ψ,Lψ⟩_μ,  B(1,ψ)=⟨Lψ,Lψ⟩_μ.

Indeed, the second formula follows by summation by parts in −⟨∇ψ,∇Lψ⟩. Let f(σ)=1_{σ(1)=1}−1/n. If σ(1)=1 then precisely n−1 transpositions move this label away; otherwise exactly one moves it to 1. Thus

Lf=q(1−n1_{σ(1)=1})=−nqf.

It follows directly that B(1,f)/A(1,f)=nq=2/(n−1), reproducing the primary upper bound without requiring a full representation-theoretic spectral-gap calculation.

Exact gap: the infimum defining κ_n ranges over all positive densities. A lower bound at ρ=1, or a diagonalization of L in irreducible representations, is not a lower bound for the density-dependent Hessian. In fact Approach 2 gives a strictly smaller value for n≥3. Thus uniform-density minimization cannot yield the desired global constant.

## 2. Nonuniform one-card quotient and an asymptotic upper bound

Let z(σ)=σ(1). A function depending only on z sees the generator

\bar Lh(i)=q Σ_{j≠i}[h(j)−h(i)],

with uniform stationary measure on [n]. Exactly one label transposition moves i to any fixed j≠i. Consequently A and B of lifted density/potential pairs agree exactly with the quotient A and B: collect the full edge sums by z-values; all within-fiber differences vanish, and L of a lifted function is the lift of \bar L. This is a direct calculation, not an assumption about arbitrary lifted geodesics.

Take ρ(1)=t>0, ρ(i)=1 for i≠1, and ψ(i)=1_{i=1}. Write ℓ=log t and t≠1. Only crossing edges contribute. Their potential-gradient Laplacian difference is −nq times the potential gradient. Also

\bar Lρ(1)=q(n−1)(1−t),  \bar Lρ(i)=q(t−1) for i≠1.

For θ=θ(t,1),

θ=(t−1)/ℓ,
θ_1=(ℓ−1+1/t)/ℓ²,
θ_2=(t−1−ℓ)/ℓ².

Therefore the quotient of the two forms is

R_n(t)=nq + q(t−1)[θ_2−(n−1)θ_1]/(2θ)
      = q/2 [n+(t+n−2−(n−1)/t)/log t].                 (2.1)

This proves κ_n≤R_n(t) for every t>0, t≠1. The continuous value at t=1 is nq. Writing h=t−1, Taylor expansion of the displayed elementary expression gives

R_n(1+h)=nq + q(2−n)h/4 + O(h²).

For n≥3, sufficiently small h>0 proves the strict inequality κ_n<2/(n−1). This is not an exact formula for κ_n.

Taking t=√n in (2.1), and using q/2=1/[n(n−1)], gives

nR_n(√n)=n/(n−1) + [√n+n−2−(n−1)/√n]/[(n−1)(½log n)] → 1.

Hence limsup_{n→∞} nκ_n≤1. This improves the constant in a test-family upper bound; no claim is made that this elementary deduction is new. The bounds still leave a factor of order n between known lower and upper scales.

Exact gap: one-card tests provide upper bounds. They cannot prove κ_n≥c/n, nor κ_n=Θ(n⁻²), nor even that the one-card family attains the full infimum. Arbitrary potentials and densities retain correlations between cards.

## 3. Coarse-graining, parity, and the failed reverse comparison

A general finite equitable quotient has a surjection z:X→Y such that Σ_{y:z(y)=j}Q(x,y) depends only on z(x) and j. For positive densities and potentials lifted from Y, the same grouping argument as in Approach 2 proves exact agreement of A and B with the quotient, using its pushforward stationary measure. Therefore

κ_X≤κ_Y.

The inequality has this direction because the full infimum includes more tests. A lower bound for the quotient supplies no lower bound for the original chain.

The parity quotient is especially decisive. Each transposition switches parity; the quotient has two states, uniform stationary measure, and rate 1 in each direction. Put density a on even permutations and b on odd permutations, and take any nonconstant parity-constant potential. Direct substitution gives

B/A=2+(b−a)[θ_1(a,b)−θ_2(a,b)]/[2θ(a,b)].             (3.1)

The last term is nonnegative. To check this without a curvature theorem, note

θ(a,b)=∫_0^1 a^s b^{1−s} ds.

Each integrand is concave and homogeneous of degree one: its Hessian quadratic form is −s(1−s)a^s b^{1−s}(u/a−v/b)². Integrating proves concavity of θ. Apply the monotonicity of the gradient of a differentiable concave function to (a,b) and (b,a), and use symmetry, to obtain

(a−b)[θ_1(a,b)−θ_2(a,b)]≤0.

This proves (3.1)≥2, with equality at a=b. The parity-restricted infimum is exactly 2 for every n≥2. For n=2 this is the full chain, so κ_2=2 exactly. For n≥3, Approach 1 gives κ_n≤2/(n−1)<2. Thus a positive quotient curvature, even an exact one, cannot be pulled back as a full-chain lower bound.

Exact gap: conditional entropy decompositions and good curvature on label or parity quotients do not control mixed directions in the full density-dependent Hessian. No monotone reverse comparison has been proved; the parity example disproves that comparison in its unrestricted form. This blocks an induction that simply imports a quotient lower bound while discarding inter-fiber terms.

## 4. Local Bochner-square approach and its sharp obstruction

We record the diagonal term obtained by allowing, in Lρ and Lψ for an edge, only that same edge's jump:

B_on=μq² Σ_{edges} g² {2θ(a,b)+½(b−a)[θ_1(a,b)−θ_2(a,b)]}.

By the concavity argument above, B_on≥2qA. The remaining interactions concern two distinct adjacent edges. Erbar–Maas–Tetali's square decomposition proves their total is nonnegative for the transposition graph, yielding κ_n≥2q=4/[n(n−1)]. We retain this as a credited established theorem, not as a new proof. Its combinatorial counting distinguishes disjoint transpositions, which lie in one appropriate square, and overlapping transpositions, which lie in two and receive half weight. The source's full theorem, including this decomposition, was inspected.

Could the overlapping S_3 pieces contribute an additional multiple of A of order n? The known obstruction in their Lemma 5.2 says there is no strictly positive universal local coefficient. We independently evaluate the obstruction in full, including the diagonal term.

The transposition graph of S_3 is K_{3,3}, because each even permutation has all three odd permutations as neighbors. Denote its parts U={u_1,u_2,u_3}, V={v_1,v_2,v_3}. For 0<ε<1 take

ρ(u_i)=ε;   (ρ(v_1),ρ(v_2),ρ(v_3))=(1,ε²,ε²),
ψ(u_i)=1;   (ψ(v_1),ψ(v_2),ψ(v_3))=(0,2,2).

These are the published local test, with labels specified explicitly. Set M=−log ε. Every edge has squared potential difference 1. Rates are q=1/3 and μ=1/6. Direct evaluation uses

Lρ(u_i)=(1+2ε²−3ε)/3,
Lρ(v_1)=ε−1,  Lρ(v_2)=Lρ(v_3)=ε−ε²,
Lψ(u_i)=1/3,  Lψ(v_1)=1,  Lψ(v_2)=Lψ(v_3)=−1.

The two logarithmic means are (1−ε)/M and ε(1−ε)/M. Substitution into the definitions gives

A=(1−ε)(1+2ε)/(6M),
B_on/A=(1+2εM−ε²)/(6εM),
B_off/A=(1+2εM−ε²)/[3M(1+2ε)],
B/A=(1+4ε)(1+2εM−ε²)/[6εM(1+2ε)].                (4.1)

These identities can be checked by inserting θ_1(a,b)=[log(a/b)−1+b/a]/log²(a/b) and θ_2(a,b)=[−log(a/b)−1+a/b]/log²(a/b) in the nine edges; the portable checker independently does exactly that using rational Laurent polynomials.

As ε↓0, εM→0 and M→∞. Thus B_off/A→0, but B_on/A∼1/(6εM)→∞ and B/A→∞. The local obstruction therefore cannot itself be a minimizing sequence for the full entropic curvature.

Exact gap: a local S_3 lower bound B_off≥cA with c>0 is false. On the other hand, its failure does not prove κ_n has order n⁻², since the large compensating diagonal term cannot be dropped in an upper bound. A genuinely global estimate trading off these terms, or a full-Hessian low-curvature sequence, is still missing.

## 5. Full finite Hessian search and an exact S_3 witness

For a fixed strictly positive density, A and B are quadratic forms in ψ. Choose an orientation of the edges and its incidence matrix E, and let W=diag(θ(ρ_x,ρ_y)), H=diag(θ_1Lρ_x+θ_2Lρ_y). Apart from the common positive factor μq,

A_matrix=E^T W E,
B_matrix=½E^T H E − ½(A_matrix L+L A_matrix).

Here L is symmetric because the chain is uniform and reversible. Removing one row/column represents potentials modulo constants, and A_matrix is positive definite there. Its lowest generalized eigenvalue is precisely inf_ψ B/A for this fixed density. Searching over log densities then supplies upper-bound candidates, but a local numerical optimizer cannot certify the global infimum in density.

An exploratory search of all density coordinates for n=3 and n=4 was performed, with deterministic random seed and retained code/output. Its approximate values are not used as mathematical conclusions. The n=3 search suggested a simple rational witness, which we now prove exactly without optimization.

List S_3 lexicographically in one-line notation:

(012),(021),(102),(120),(201),(210).

Take unnormalized density (1,1,16,16,1,1) and potential (5,−5,8,−8,5,−5). With ℓ=log 2, exact edge summation yields

A=(4496ℓ+135)/(18ℓ),
B=(251392ℓ²+480ℓ+6075)/(1152ℓ²).

Consequently

(9/10)A−B=(37888ℓ²+36480ℓ−30375)/(5760ℓ²)>0.

For a fully rational sign proof, log 2=2∫_0^{1/3}(1−x²)^{-1}dx>2/3. The numerator is strictly increasing for positive ℓ, and at ℓ=2/3 it equals 97057/9>0. Therefore

κ_3≤B/A<9/10.

The exact ratio is approximately 0.88181537; only the strict rational bound is needed. The stated density divided by its mean 6 has μ-average 1, leaving the ratio unchanged. This is an explicit finite upper bound, not a determination of κ_3. It also provides a concrete negative control against the incorrect assertion that uniform-density spectral minimization is globally sharp.

Exact gap: neither this single witness nor finitely many optimized n establish an all-n asymptotic order. A finite-dimensional LP for W_1 would concern a different curvature. The entropic problem here is a nonlinear optimization in the density and a quadratic-form comparison in the potential, not a single all-density linear program.

## Conclusion

The five approaches retain: the correct continuous-time convention; the spectral upper test; the one-card family and limsup nκ_n≤1; the exact n=2 value; the direction and failure of reverse quotient comparison; an explicit evaluation of the known local off-diagonal obstruction; and a rigorous κ_3<9/10 test. The general asymptotic order remains unresolved in this investigation. No prior resolution was located in the bounded literature search. This is not a claim of global openness as of October 2026.

## Sources

- Jan Maas's report contribution, pp. 3227–3229: https://doi.org/10.4171/OWR/2014/57 ; publisher PDF https://ems.press/content/serial-article-files/46544
- Erbar, Maas, Tetali, *Discrete Ricci curvature bounds for Bernoulli–Laplace and random transposition models* (2015): https://doi.org/10.5802/afst.1464 ; inspected author preprint https://www.janmaas.org/papers/slices.pdf
- Fathi, Maas, *Entropic Ricci curvature bounds for discrete interacting systems* (2016), Theorem 4.9 in the published version (4.8 in the earlier preprint): https://doi.org/10.1214/15-AAP1133

Later-source scope checks and exact retrieval metadata are recorded separately. The source PDFs and extracts are not included in this packet.
