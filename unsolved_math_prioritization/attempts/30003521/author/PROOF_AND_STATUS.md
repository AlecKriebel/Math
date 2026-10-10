# Quadratic graph NLS approximation and two precise obstructions

Problem 30003521, OWR-15437-003. Bounded mathematical investigation dated 6 October 2026.

## Conclusion and scope

This is a partial analysis, not a solution of the open quadratic NLS-approximation problem. It establishes two precise facts on Kirchhoff metric graphs:

1. The domain of the graph Klein–Gordon operator is closed under multiplication, but even infinitely operator-smooth inputs can have a product outside the domain of its square.
2. On an explicitly specified periodic necklace graph, a simple carrier has a genuinely coupled quadratic second-harmonic resonance. Its second-harmonic corrector equation is unsolvable, and the corresponding quadratic normal-form coefficient cannot be defined by division.

These facts locate distinct obstacles. Neither proves that NLS approximation fails for every carrier or every graph. No novelty priority is asserted. In particular, the algebra property is already used in the graph-approximation literature. The counterexample below is an explicit diagnostic in the class of periodic graph Klein–Gordon equations; it is not offered as the answer for an unspecified fixed original system.

## Verified provenance and literature boundary

Schneider's contribution, “The NLS approximation for dispersive systems on graphs,” is on printed pages 1856–1858 of Oberwolfach Report 29/2017. It discusses cubic wave equations and Bloch modulation, then leaves the quadratic graph extension open, mentioning normal forms, nonresonance, and insufficient regularity for an earlier smooth-coefficient argument. It does not state a complete quadratic graph Cauchy problem or the hypotheses of a prospective theorem. [S1]

Gilg–Pelinovsky–Schneider's 2016 result concerns an original NLS equation on a necklace graph, not a proof of the requested quadratic wave problem. [S2] Gilg–Schneider–Uecker's 2022 paper treats cubic Klein–Gordon on graphene-like graphs. Its Remark 7.2(c) explicitly leaves quadratic graph nonlinearities open. Its hypotheses (7.7)–(7.8) concern carrier simplicity and a third harmonic; they cannot simply replace quadratic nonresonance assumptions. [S3]

The 2026 paper by Le Coz–Pelinovsky–Schneider addresses traveling modulating pulses for graph NLS via spatial dynamics, not quadratic Klein–Gordon modulation. [S4] Targeted public searches and the author's publications list located no later result settling the requested problem. This is a search outcome, not a certified assertion that no such theorem exists. [S5]

The requested problem webpage could not be opened by the web tool. The full supplied problem record and inherited report were inspected privately; the inherited report was empty. The supplied corpus and combined-review hashes were verified. Repository searches for the exact ID, problem number, and NLS graph topic returned no matching existing attempt. Search absence is not an exhaustive repository-history proof. No publication was made.

## 1 The exact Kirchhoff operator domain

Let G be a metric graph with finite periodic quotient, all edge lengths positive, and finite vertex degrees. Let

L = -d²/ds² + 1

act edgewise in L²(G). Write ∂ν for the derivative pointing from a vertex into its incident edge. Its domain is

D(L) = {u in the edgewise H² direct sum: u is continuous at every vertex and Σ(e incident to v) ∂νu_e(v) = 0}.

Repeated incident endpoints of a loop are counted separately. Use the norm

||u||²_D = Σ_e ||u_e||²_H²(e),

which is equivalent to the operator graph norm. Periodicity supplies a uniform positive minimum edge length and a finite set of edge lengths; the standard one-dimensional derivative interpolation bound establishes this equivalence.

### Proposition 1 The lowest operator domain is an algebra

There is C, depending only on the finite graph geometry, such that

||uv||_D ≤ C ||u||_D ||v||_D,  u,v in D(L).

Proof. On each of the finitely many edge-length types, the H² multiplication inequality has a uniform constant. Squaring and summing gives

Σ_e ||u_ev_e||²_H² ≤ C² Σ_e ||u_e||²_H² ||v_e||²_H²
≤ C² (Σ_e ||u_e||²_H²)(Σ_e ||v_e||²_H²).

Continuity of uv is immediate. At a vertex v, continuity of the factors gives

Σ_e ∂ν(uv)_e(v)
= u(v) Σ_e ∂νv_e(v) + v(v) Σ_e ∂νu_e(v) = 0.

Thus uv satisfies the same Kirchhoff conditions. The same reasoning covers complex conjugation. This elementary proof is consistent with the known algebra property used in [S2, S3]; it is not claimed as a new result. ∎

### Proposition 2 Exact higher-domain obstruction

For u,v in D(L²), their product belongs to D(L²) if and only if the quantities

∂νu_e(v) ∂νv_e(v)

are independent of the incident endpoint e at each vertex v.

Proof. D(L²) consists of edgewise H⁴ functions for which u and Lu satisfy Kirchhoff conditions. In outgoing edge coordinates, this is equivalent to continuity of u and u'', together with Σu' = Σu''' = 0 at each vertex. For uv, the only possibly noncommon term in

(uv)'' = u''v + 2u'v' + uv''

is 2u'v'. The third derivative satisfies

Σ(uv)''' = v Σu''' + 3u'' Σv' + 3v'' Σu' + u Σv''' = 0,

because u'', v'', u, v have common vertex traces. Edgewise H⁴ multiplication and the same direct-sum estimate justify the regularity. Proposition 1 gives the remaining conditions. ∎

### Corollary A loss even for infinitely operator-smooth inputs

At any vertex of degree at least three, choose outgoing slopes (1,-1,0) on three incident endpoints and zero on all others. On short disjoint endpoint segments put

u_e(s) = a_e s χ(s),

where χ is smooth, equals one near s = 0, and vanishes before reaching any other endpoint. Extend by zero elsewhere. All supports may be chosen disjoint even for loops.

This function is edgewise smooth, has common value zero, and its outgoing slopes sum to zero. Near the chosen vertex, every L^m u equals u. All conditions at other vertices are zero. Therefore u belongs to D(L^m) for every positive integer m.

However, near the vertex u²_e(s) = a_e²s², so the vertex traces of L(u²) are -2a_e². They include -2,-2,0 and are not continuous. Hence u² is not in D(L²).

This does not obstruct local quadratic evolution in D(L). It invalidates a proof step that assumes arbitrary operator-domain powers remain multiplication algebras merely because the inputs are edgewise smooth.

## 2 Quadratic normal forms and the required resonance information

To make the issue precise, consider the specified representative system

u_tt + Lu = ηu² + ζu³,  η ≠ 0,

with the Kirchhoff conditions above. This model is introduced for the analysis; the OWR question does not prescribe these particular coefficients or geometry.

Let Ω = sqrt(L) and z_σ = (u - σ i Ω^(-1)u_t)/2, for σ = +1 or -1. Direct differentiation yields

(z_σ)_t = σ i Ω z_σ - σ i η Ω^(-1)(z_+ + z_-)²/2 + cubic terms.

For a periodic graph, let θ denote the Floquet phase, and let f_n(θ), ω_n(θ)² be normalized eigenpairs of L(θ). In a quasiperiodic-fiber convention the product of modes at θ₁ and θ₂ belongs to the fiber θ₁+θ₂, modulo 2π. Define

c_(jmn)(θ₁,θ₂) = <f_j(θ₁+θ₂), f_m(θ₁)f_n(θ₂)>.

For the component mapping signs σ₁,σ₂ to σ, the homological divisor is

Φ = σ₁ω_m(θ₁) + σ₂ω_n(θ₂) - σω_j(θ₁+θ₂).

For w = z + B(z,z), the quadratic cancellation equation on finite spectral sums reads

iΦ b = -q,  q = -σ i η c_(jmn)/(2ω_j).

Thus, when Φ ≠ 0,

b = σ η c_(jmn)/(2ω_j Φ).

If Φ = 0 and the coupling is nonzero, cancellation is impossible for that component. If a denominator vanishes but the coupling also vanishes, division is still not automatically legitimate: one needs a controlled extension and estimates near the vanishing set.

For a carrier f with frequency ω at phase θ, the order-two second-harmonic and mean corrector equations have the form

[L(2θ)-4ω²]h₂ = η f²,
L(0)h₀ = 2η|f|².

The second equation is invertible here because L ≥ 1. The first requires the Fredholm compatibility condition

P_ker[L(2θ)-4ω²](f²) = 0.

Even its solvability does not prove long-time stability. The normal-form analysis of the error also encounters interactions between the carrier and all error modes, with all relevant signs. A proof needs summable, domain-respecting estimates for the resulting bilinear operators, and their parameter derivatives or an alternative energy argument. Merely checking the finitely many carrier-generated harmonics does not establish these estimates. Nor is nonvanishing of individual denominators by itself a uniform bound in infinitely many band indices.

## 3 An explicit coupled resonance with a simple carrier

Here the graph and all lengths are specified exactly. This is a periodic necklace: e₀ connects A_n to B_n, and parallel edges e_+,e_- connect B_n to A_(n+1). Each edge has length ℓ. All edges are oriented in that order. A Bloch field is e^(inθ) times a cell profile.

On a cell the conditions are

f₀(ℓ) = f_+(0) = f_-(0),
f₀'(ℓ) = f_+'(0) + f_-'(0),
f_+(ℓ) = f_-(ℓ) = e^(iθ) f₀(0),
f_+'(ℓ) + f_-'(ℓ) = e^(iθ) f₀'(0).

Set

a = arccos(1/3),   ℓ = sqrt((π²-4a²)/3),   q = a/ℓ,   b = π/ℓ.

Since 0 < a < π/2, ℓ is positive. The mass term remains exactly +1 in L. Only the graph's common edge length has been chosen; no discrete or smooth-coefficient surrogate is used.

At antiperiodic phase θ = π define the real cell profile

f₀(s) = cos(qs) - sqrt(2) sin(qs),
f_+(s) = f_-(s) = -cos(qs) - sin(qs)/sqrt(2).

Since cos(a) = 1/3 and sin(a) = 2sqrt(2)/3, the link endpoint values are 1,-1 and the arc endpoint values are -1,-1. The link endpoint derivatives are both -sqrt(2)q; each arc has derivatives -q/sqrt(2),+q/sqrt(2). These verify every displayed vertex condition at θ = π. Thus

L(π)f = (1+q²)f = ω² f.

The carrier is simple in the full fiber. To see this, split into components symmetric and antisymmetric under exchanging e_+ and e_-. Any nonzero antisymmetric mode has a zero link and Dirichlet arcs, hence qℓ is an integer multiple of π; our a is not. In the symmetric sector use state (value, total outgoing-forward flux/q). Propagation through a link and then a double arc has matrices

T₁ = [[c,s],[-s,c]],   T₂ = [[c,s/2],[-2s,c]],

where c = cos(qℓ), s = sin(qℓ). Their product has determinant 1 and trace 2c²-(5/2)s². At qℓ = a, the trace is -2 and its upper-left entry is -1/3, so it is not -I. Consequently the eigenspace for the multiplier -1 has dimension one. The compact self-adjoint Floquet operator has a one-dimensional eigenspace, proving simplicity.

At periodic phase 0 define

g₀(s) = sin(bs),
g_+(s) = g_-(s) = -(1/2) sin(bs).

All vertex values are zero. The link derivatives are b,-b and each arc's derivatives are -b/2,+b/2, so Kirchhoff conditions hold. Therefore

L(0)g = (1+b²)g = 4ω²g,

where the last equality follows from 3ℓ² = π²-4a². Since 2π is equivalent to phase 0, this is precisely a 1:2 Floquet resonance from f to g.

Crucially, its coupling does not vanish. The cell inner product, counting both parallel edges, is

I = <g,f²> = ∫₀^ℓ [f₀(s)² - f_+(s)²] sin(πs/ℓ) ds.

Write y = s/ℓ-1/2. Elementary trigonometry gives

f₀(s) = -sqrt(3) sin(ay),
f_+(s) = -sqrt(3/2) cos(ay),
f₀(s)²-f_+(s)² = 3/4-(9/4)cos(2ay).

For |y|<1/2, cos(2ay)>cos(a)=1/3, and cos(πy)>0. Hence I<0 directly. Integrating also gives the exact value

I = -6ℓa²/[π(π²-4a²)] = -2a²/(πℓ) ≠ 0.

Now suppose h in D(L(0)) solved the second-harmonic corrector equation. Self-adjointness would give

0 = <[L(0)-4ω²]g,h> = <g,ηf²> = ηI,

a contradiction. The equation has no solution. Equivalently, the corresponding homological equation has a zero divisor and a nonzero numerator.

This proof concerns exact Bloch fibers. It does not claim that a nonlocalized Bloch wave is an L² wave packet on the infinite graph, nor does it provide a nonlinear long-time counterexample for localized data. It proves the exact spectral and corrector obstruction, even though the carrier is simple. The chosen ℓ is not the conventional edge length π; nothing here claims that this same pair resonates on the fixed π-length graph.

## 4 What a successful nonresonant proof still needs

A possible closure mechanism is a bounded quadratic change of variables in a Banach space X adapted to small wave packets. Suppose a verified transformation reduces the system to

w_t = Aw + F(w),

where the linear group is bounded by M and

||F(w)-F(v)||_X ≤ K (||w||_X+||v||_X)² ||w-v||_X

in a fixed neighborhood of zero. Suppose a constructed approximation w_a satisfies

||w_a||_X ≤ C_a ε,
||(w_a)_t-Aw_a-F(w_a)||_X ≤ C_r ε^(p+2),
||w(0)-w_a(0)||_X ≤ C_i ε^p,

for 0≤t≤T/ε² and some p>1.

Then standard continuation and the variation-of-constants formula yield

sup_(0≤t≤T/ε²) ||w(t)-w_a(t)||_X ≤ C_T ε^p.

Indeed, on the bootstrap ||w-w_a||≤ε the cubic Lipschitz bound is at most K(2C_a+1)²ε² times the error. Gronwall gives

||w-w_a|| ≤ M(C_i+C_rT) ε^p exp(MK(2C_a+1)²T),

which improves the bootstrap for sufficiently small ε because p>1. This is only a conditional stability lemma. Local well-posedness and continuation in X, invertibility of the change of variables, and every displayed hypothesis must first be proved for the actual graph problem.

For extended packets, an unscaled L²-based H² norm need not be O(ε); its size depends on the spatial dimension and packet width. A proof must use an appropriate Bloch L¹-type control norm together with its error norm, or carry the scaling losses explicitly. Replacing this requirement by a naive H² smallness assumption would prove a different statement.

The unresolved work is therefore concrete: specify the original quadratic system and admissible graph/carrier class; identify compatible resonances; establish the infinite-band bilinear estimates with the correct vertex domains; construct and estimate a sufficiently accurate packet; and close stability on the NLS time scale. The present report stops without those results.

## Research budget and verification scope

Five substantive approaches were used: source and prior-result reconciliation; Kirchhoff domain multiplication; quadratic homological equations; an exact resonant Bloch construction; and the conditional long-time stability test. No full solution or verified earlier full solution emerged.

The supplementary checker only verifies finite rational endpoint, flux, monodromy, and formal resonance identities. The mathematical proofs above do not depend on numerical simulation, unverified root finding, band truncation, or the checker. It does not test or prove the open nonlinear approximation theorem. Integrity is checked externally before this checker is executed in an isolated Python process.

## Public references

[S1] Guido Schneider, “The NLS approximation for dispersive systems on graphs,” in Nonlinear Partial Differential Equations on Graphs, Oberwolfach Reports 14 (2017), contribution pp. 1856–1858; report pp. 1805–1868. DOI: https://doi.org/10.4171/owr/2017/29 . Publisher PDF: https://ems.press/content/serial-article-files/46690 .

[S2] Steffen Gilg, Dmitry Pelinovsky, Guido Schneider, “Validity of the NLS approximation for periodic quantum graphs,” Nonlinear Differential Equations and Applications NoDEA 23 (2016), article 63. https://doi.org/10.1007/s00030-016-0417-7 . Publisher page: https://link.springer.com/article/10.1007/s00030-016-0417-7 .

[S3] Steffen Gilg, Guido Schneider, Hannes Uecker, “Nonlinear dynamics of modulated waves on graphene like quantum graphs,” Mathematische Nachrichten 295 (2022), 2147–2170. https://doi.org/10.1002/mana.202100009 . Publisher full text: https://onlinelibrary.wiley.com/doi/10.1002/mana.202100009 . Author preprint: https://pde2path.uol.de/hu/pre/070-graphene.pdf .

[S4] Stefan Le Coz, Dmitry E. Pelinovsky, Guido Schneider, “Traveling Waves in Periodic Metric Graphs Via Spatial Dynamics,” Journal of Dynamics and Differential Equations (2026), published 2 February 2026. https://doi.org/10.1007/s10884-026-10490-6 .

[S5] Guido Schneider, public publication list, inspected 6 October 2026. https://www.iadm.uni-stuttgart.de/dokumente/schneider_publ.pdf .
