# Boundary blow-up and local completeness of planar conformal metrics

Problem 30000704 / OWR-1460-010. Author's research note, 2026-10-04.

## Status and exact scope

**PARTIAL RESULT; the full minimum-regularity classification is not resolved.**
The source problem asks which boundary-set hypotheses make density blow-up
and local metric completeness equivalent. The 2007 source gives an open free
C² boundary subarc as a sufficient hypothesis. This note proves a broader
sufficient result for an explicitly defined one-sided free Jordan boundary
arc, with no differentiability assumption. Its forward implication has a
more general local componentwise regular-open formulation. Explicit
constant-curvature counterexamples exclude arbitrary boundary sets, even
singletons on an analytic ambient boundary. None of this proves a necessary
and sufficient criterion for general boundary sets. No novelty or priority
claim is made. The proof is provisional pending independent mathematical
review.

## 1. Definitions, conventions, and the exact source problem

Let Ω be a connected open subset of C. A regular conformal metric is
λ(z)|dz| with λ:Ω→(0,∞) of class C². Curvature and distance are

    κ_λ = -Δ log λ / λ²,
    d_λ(p,q) = inf_γ ∫_γ λ(z)|dz|,

where the infimum is over piecewise C¹ paths joining p to q in Ω.
We use the curvature -4 normalization

    h_D(z) = 1/(1-|z|²).

Thus κ_λ≥-4 means Δ log λ≤4λ². The direction of this inequality is
important: most ordinary Schwarz-Ahlfors upper estimates assume the
OPPOSITE curvature inequality.

For Γ⊂∂Ω, write

- (B) λ(z)→∞ as z∈Ω tends to ξ, for every ξ∈Γ.
- (C) d_λ(z₀,z)→∞ as z∈Ω tends to ξ, for every ξ∈Γ.

These are unrestricted Euclidean approach limits, not just radial,
nontangential, or almost-everywhere limits. The choice of z₀∈Ω in (C)
does not matter, by the triangle inequality. Neither condition asserts
completeness at boundary points outside Γ or at infinity.

The original source is Oliver Roth's problem-session contribution in
*Normal Families and Complex Dynamics*, Oberwolfach Report 9/2007,
printed p.529, Problem 2, DOI 10.4171/owr/2007/09. It follows a corollary
assuming Γ is an open free C² subarc and κ_λ≥-4. The adjacent Problem 1
is about boundary behavior of a holomorphic disk map and is a different
question. The catalogue is a reasonable broad question rather than a theorem
for arbitrary Γ; its shorthand must not be read as deleting openness and
freeness from the known positive result.

For clarity, the free-Jordan hypothesis used HERE is the following explicit
one-sided local condition:

(J) For every ξ∈Γ there are ε>0 and a bounded Jordan domain P⊂Ω such that
Ω∩B(ξ,ε)=P∩B(ξ,ε), and a relatively open subarc J of ∂P containing ξ
with J⊂Γ. In addition, Γ is relatively open in ∂Ω.

This formulation rules out hidden other approach components. It holds for
ordinary one-sided free Jordan boundary arcs, including nonsmooth ones.
It is enough to require the corresponding local condition at each point;
no global simple connectivity or boundedness of Ω is assumed.

An open set G is *regular-open* if G=int(cl G), where closure and interior
are taken in the Euclidean plane. This is a topological condition; it is
not Wiener regularity, smoothness, or regularity of the metric. A Jordan
domain is regular-open. A punctured disk is not.

## 2. Results proved in this note

**Theorem A (global outward approximation).** If G is a bounded connected
regular-open plane domain, λ is a positive C² density on G with
κ_λ≥-4, and λ→∞ at EVERY point of ∂G, then

    λ(z) ≥ h_G(z)  for all z∈G.

Here h_G is the hyperbolic density with curvature -4.

**Theorem B (local componentwise regular-open sufficiency).** Let λ be a
regular conformal metric on Ω with κ_λ≥-4 and assume (B) on Γ. Suppose
that for every ξ∈Γ there is R>0 such that

    ∂Ω ∩ cl B(ξ,R) ⊂ Γ,

and every connected component G of Ω∩B(ξ,R) is regular-open. Then (C)
holds on Γ. More explicitly, there is c=c(ξ,R,λ)>0 such that

    λ(z) ≥ c/[|z-ξ| log(R/|z-ξ|)]

whenever z∈Ω and 0<|z-ξ|<R/2. Hence distances to ξ have a quantitative
lower bound of log-log type. This estimate is a sufficient barrier, not a
claim that the true boundary growth must be this slow.

**Theorem C (free-Jordan equivalence).** Under (J), (B) and (C) are
equivalent. No differentiability of J is needed. The forward implication
is Theorem B. The reverse uses the known localized disk Schwarz estimate
stated in the original report, transported to P. This dependency is explicit
in Section 6; it is not claimed as a new theorem here.

**Counterexamples.**

1. For every 0<a<1 the density

       λ_a(z)=a|z|^(a-1)/(1-|z|^(2a))  on 0<|z|<1

   has constant curvature -4 and diverges at EVERY boundary point, but has
   finite distance to the puncture.
2. Even on the analytic-boundary domain Ω=D, the density

       η_a(z)=a 2^(-a) |1-z|^(a-1) /
              [1-2^(-2a)|1-z|^(2a)]

   is positive and real analytic, has constant curvature -4, diverges as
   z→1, and gives finite distance to 1. Thus a singleton Γ={1} cannot
   replace an open boundary arc merely because the ambient boundary is
   smooth.

These do not refute Theorem C: the first has a non-regular-open puncture,
and the second lacks a relatively open Γ.

## 3. Hyperbolic facts used, and an outward convergence proof

We use three standard hyperbolic facts, obtainable from planar uniformization
and Schwarz-Pick:

(i) Every bounded domain G has a universal covering π:D→G, normalized at
any p∈G by π(0)=p and π'(0)>0. Its density satisfies
h_G(p)π'(0)=1.

(ii) If f:D→G is holomorphic, h_G(f(0))|f'(0)|≤1. In particular, if
G⊂H, then h_G≥h_H.

(iii) On the punctured disk 0<|z-ξ|<R,

    h_*(z)=1/[2|z-ξ| log(R/|z-ξ|)].                         (3.1)

The formula is checked directly by Δ log h_*=4h_*², or by a covering
from a half-plane. Its radial length to ξ is infinite.

The following argument supplies the particular kernel-convergence fact
needed here instead of hiding it in a broad convergence citation.

Let G be bounded, connected, and regular-open, and put

    G_n={z:dist(z,cl G)<1/n}.

Each G_n is a bounded connected domain: it is a union of balls centered
on the connected set cl G. The domains decrease, contain cl G compactly,
and G⊂G_n. Fix p∈G. Monotonicity gives h_Gn(p) increasing to a finite
L≤h_G(p), with L>0 because all G_n lie in a fixed large disk. Choose
normalized universal coverings f_n:D→G_n at p. They are uniformly
bounded and have f_n'(0)=1/h_Gn(p). Montel's theorem supplies a subsequence
converging locally uniformly to a holomorphic f with f(0)=p and f'(0)=1/L>0.

For every fixed w∈D, f(w) belongs to cl G: the distance of f_n(w) to cl G
is less than 1/n. Since f is nonconstant, f(D) is open. Therefore

    f(D)⊂int(cl G)=G.

Schwarz-Pick now gives h_G(p)/L≤1. Combining this with L≤h_G(p)
proves

    h_Gn(p) ↑ h_G(p).                                      (3.2)

This proof explains exactly why a filled slit or puncture is a problem:
without regular-openness the limiting holomorphic disk need only land in
int(cl G), which can be strictly larger than G. No arbitrary-domain
kernel-convergence assertion is being used.

## 4. Proof of Theorem A

Fix n and let μ=h_Gn. Since cl G is compact in G_n, μ is bounded and
positive on cl G. Set w=log μ-log λ on G. Since λ tends to infinity at
every boundary point, w tends to -∞ at every boundary point. Compactness
of ∂G upgrades this pointwise statement enough to conclude that any positive
supremum of w is attained in the interior of G: for any fixed positive
level, its superlevel set stays away from the boundary and is bounded.

At an interior positive maximum p, μ(p)>λ(p), and

    Δw(p)=4μ(p)²-Δlog λ(p)
          ≥4[μ(p)²-λ(p)²]>0.

This contradicts Δw(p)≤0 at a C² maximum. Thus λ≥h_Gn. Let n→∞ and
use (3.2) to obtain λ≥h_G. No assumption about existence of geodesics,
completeness of λ, boundary derivatives, or curvature negativity beyond
the stated LOWER bound occurred in this argument.

For a lower bound κ_λ≥-K with K>0, scaling σ=(sqrt K/2)λ reduces to
curvature ≥-4 and gives λ≥(2/sqrt K)h_G. This scaling direction is
also important.

## 5. Proof of Theorem B, including paths that leave the neighborhood

Fix ξ and R as in its hypotheses and abbreviate r=|z-ξ| and
U=Ω∩B(ξ,R). There is m>0 such that λ≥m throughout U. Otherwise choose
z_n∈U with λ(z_n)→0 and pass to a subsequence converging in cl B(ξ,R).
If the limit is in Ω, continuity and positivity contradict λ(z_n)→0.
If it is on ∂Ω, it is in Γ by the closed-ball hypothesis, and (B) gives
the opposite limit λ(z_n)→∞. These exhaust the possibilities.

Define on U

    ρ(z)=λ(z)/(R²-r²),
    K=4R⁴+4R²/m² >0.

The exact differentiation identity

    Δ[-log(R²-r²)]=4R²/(R²-r²)²

gives

    Δlogρ ≤4λ²+4R²/(R²-r²)²
            ≤[4R⁴+4R²/m²]ρ² = Kρ².

Consequently κ_ρ≥-K. Notice that there are no cross-gradient terms
because the modification is MULTIPLICATIVE and we differentiate its
logarithm. A casual addition or maximum of densities would not have the
same property.

For every component G of U, ρ tends to infinity at all points of ∂G.
Indeed, ∂G⊂∂U. At a boundary point inside B(ξ,R), the point lies in
∂Ω∩Γ and λ→∞, while the denominator remains positive. At a point on
∂B(ξ,R), λ≥m and the denominator tends to zero. Positivity of the
metric excludes any missing interior zero issue.

Apply Theorem A to σ=(sqrt K/2)ρ on each regular-open component G. Then

    λ(z) ≥ [2(R²-r²)/sqrt K] h_G(z).                       (5.1)

Every G is contained in the punctured disk 0<|z-ξ|<R, since ξ∉Ω.
By (3.1) and domain monotonicity, for EVERY z∈U, regardless of component,

    λ(z) ≥ (R²-r²)/[sqrt K r log(R/r)].                    (5.2)

In particular, for r<R/2 one may take c=3R²/(4sqrt K) in Theorem B.
The same c works across all components of U, so no finiteness assumption
on their number is hidden here.

It remains to check distances in the ORIGINAL Ω; completeness in a
restricted patch alone would not suffice. Fix z₀∈Ω and choose
0<r₀<min(R/2,|z₀-ξ|). For any path γ from z₀ to z with r(z)<r₀, consider
its portion after the last crossing of the circle r=r₀. On this portion
r≤r₀, and |dr|≤|dz|. Let

    F(r)=log log(R/r),  so |F'(r)|=1/[r log(R/r)].

By (5.2),

    length_λ(γ) ≥ c |F(r(z))-F(r₀)|
               = c log[log(R/r(z))/log(R/r₀)].             (5.3)

The right side tends to infinity as z→ξ. Taking the infimum over all
paths proves (C). Multiple entries into U, remote shortcuts elsewhere in Ω,
and variation among components cannot evade this last-crossing bound.

## 6. Proof of Theorem C and the known disk dependency

For a free-Jordan patch as in (J), the domain is locally regular-open.
Here is a precise reduction. Shrink the ball about ξ so that Ω=P on a
larger neighborhood, its closed ball meets ∂Ω only in Γ, and the ball's
closure lies in that neighborhood. Jordan domains satisfy P=int(cl P),
so U=P∩B(ξ,R) is regular-open, since finite intersections of regular-open
sets are regular-open. Every component G of a regular-open U is regular-open:
if x∈int(cl G), then x∈U; a small ball in the component of U containing x
would be disjoint from G if it were a different component, contradicting
x∈cl G. Thus x lies in G. Theorem B proves (B)⇒(C).

For (C)⇒(B), fix a bounded Jordan patch P from (J), a basepoint p∈P, and
a Riemann map φ:D→P. Carathéodory's theorem extends φ to a homeomorphism
of closures. A subarc J'⊂J about ξ corresponds to an open unit-circle
arc A. Define the positive C² pullback density

    ν(w)=λ(φ(w))|φ'(w)|.

Conformal invariance gives κ_ν≥-4. For any η∈A,

    d_ν(w₀,w)=d_(λ|P)^P(p,φ(w)) ≥ d_λ^Ω(p,φ(w)) →∞

as w→η. Here superscripts emphasize which domain contains admissible
paths. The inequality is in the correct direction because restricting
paths increases their infimum. It is enough to take p=φ(w₀).

We now invoke precisely the established disk result stated on p.529 of the
2007 primary report: for a positive regular metric of curvature ≥-4,
local completeness along an open circle arc implies

    liminf_(w→η) ν(w)/h_D(w) ≥1.                           (6.1)

The report attributes this direction to Yau and Bland and to the detailed
Kraus-Roth-Ruscheweyh treatment. Its proof is not re-proved in this note.
This statement, rather than a general assertion about complete metrics on
arbitrary rough domains, is the only localized completeness theorem used.

Conformal invariance of the hyperbolic density yields

    ν(w)/h_D(w)=λ(φ(w))/h_P(φ(w)).

The homeomorphic boundary extension gives

    liminf_(z→ξ, z∈P) λ(z)/h_P(z) ≥1.                     (6.2)

There was no need to bound φ' above or below: it cancels in the quotient.
Take a disk B(ξ,S) containing P. By monotonicity and (3.1),

    h_P(z)≥1/[2|z-ξ| log(S/|z-ξ|)]→∞.

Thus λ→∞ as z∈P tends to ξ. Since Ω and P agree near ξ, this is the
required unrestricted limit in Ω. This finishes the equivalence.

The conclusion is qualitative. In the rough case we do not claim the
sharp ratio liminf λ/h_Ω≥1 from density blow-up, or Euclidean-distance
asymptotics, derivative bounds, a reflection principle, or C¹ boundary
extension of φ.

## 7. Exact counterexamples and curvature-sign controls

### 7.1 Isolated boundary, even with constant negative curvature

On the punctured unit disk define λ_a as in Section 2, with 0<a<1.
Writing r=|z| and q=r^(2a), direct differentiation gives

    r (log λ_a)' = a-1+2a q/(1-q),
    Δlog λ_a = 4a² q/[r²(1-q)²] = 4λ_a².

Hence κ=-4. At r→0, λ_a∼a r^(a-1)→∞; at r→1 it is asymptotic to
1/[2(1-r)] and also tends to infinity. But a radial segment from 0 to
r₀ has total length

    ∫_0^r₀ a r^(a-1)/(1-r^(2a)) dr = artanh(r₀^a)<∞.

Consequently d_λ(r₀,r) stays bounded as r→0. This is a GLOBAL density
blow-up example that is globally incomplete. It shows why one cannot
silently replace an open free arc by all boundary sets, or drop the
regular-open premise from Theorem A. The classical conical/cuspidal
classification also explains the example: for negative Hölder curvature,
orders below 1 can blow up but remain incomplete; order 1 has the cusp
logarithm and is complete. The latter general classification needs its
extra curvature regularity and is not assumed for our target class.

The flat model λ=r^(-b), 0<b<1, gives the same simpler obstruction with
κ=0 and radial length r₀^(1-b)/(1-b). It is not the only obstruction,
because λ_a already has κ=-4 everywhere.

### 7.2 Smooth ambient boundary but a singleton distinguished set

For Ω=D, use the principal holomorphic branch

    f_a(z)=((1-z)/2)^a,  0<a<1.

The values of 1-z lie in the right half-plane, so the branch is defined,
f_a' never vanishes, and |f_a|<1. Its pullback f_a^*h_D is exactly η_a
from Section 2 and has curvature -4. It tends to infinity at ξ=1 because
its denominator tends to 1 and its numerator is a positive constant times
|1-z|^(a-1). Along z=1-r, 0<r≤1,

    ∫_0^1 η_a(1-r)dr = artanh(2^(-a))<∞.

Thus (B) does not imply (C) on Γ={1}, even though ∂Ω is analytic and
κ is the same constant as the hyperbolic metric. The regularity of the
ambient boundary and relative openness of the distinguished set are
separate issues. This is not a counterexample on an open arc.

### 7.3 Why the lower curvature bound is essential

For 0<a<1 on D set τ_a=(1-|z|²)^(-a). It diverges on the whole circle
and has finite radial boundary length, since (1-r²)^(-a)≤(1-r)^(-a).
But

    κ_τ = -4a(1-r²)^(2a-2)→-∞.

Thus this familiar example does NOT satisfy the target hypotheses. It is
included as a negative control against a reversed-curvature argument.

## 8. What the five approaches establish, and the remaining obstruction

1. **Radial curvature ODE:** identifies conical versus cusp growth and
   supplies a constant-negative-curvature obstruction at a puncture.
2. **Boundary-coordinate regularity:** nonvanishing continuous derivative
   of a conformal chart, available under Dini-smoothness, transfers density
   blow-up directly to the disk. This gives a familiar sufficient class but
   is not a necessity theorem. If φ' tends to zero, λ∘φ→∞ alone says
   nothing about their product, so this argument does not prove arbitrary
   Jordan sufficiency.
3. **Outward approximation and circular cutoff:** avoids that derivative
   bottleneck altogether, proving Theorems A and B. Its exact limit-set
   requirement is regular-openness of local components. For a punctured or
   slit domain whose local component fills in under int(cl·), the proof
   only compares to the filled domain and can lose the singularity.
4. **Topological transport of completeness:** the distance inequality and
   cancellation in (6.2) prove the reverse implication for free-Jordan
   patches, combining with approach 3 to give Theorem C.
5. **Distinguished-set and singularity stress test:** the disk singleton
   construction shows smoothness of ∂Ω alone cannot be the desired
   criterion. The isolated-point classification under negative Hölder
   curvature does not extend to the entire class κ≥-4 without additional
   work. A sharp potential-theoretic or topological criterion for general
   Γ is not obtained.

The local componentwise regular-open condition is a sufficient condition,
not asserted necessary. For example, it can hold on interior points of a
straight slit after a small disk splits the domain into upper and lower
components, although the unsplit ambient domain is not regular-open.
At slit endpoints or more complicated thin closed sets, neither this
observation nor a smoothness scale determines the answer. We have not
classified such boundary sets or proved a weakest possible hypothesis.

The terms “minimal regularity” require a specified class of boundary sets
and ordering of hypotheses. Within the explicitly one-sided free-Jordan
class, differentiability is unnecessary. This substantial weakening is not
presented as the complete arbitrary-Γ classification requested by the
catalogue. The fifth approach ends with this precise unresolved scope;
there is no sixth proof search hidden in verification.

## 9. Source and verification limitations

- Primary report p.529 was read as extracted text and visually checked.
- The KRR 2007 publisher page and bibliographic metadata were checked;
  its attempted PDF URL returned subscription-preview HTML, not a PDF.
  The full KRR article was therefore NOT inspected. The disk implication
  (6.1) is verified as explicitly stated in the primary report.
- Kraus-Roth's isolated-singularity paper was inspected at Theorems 1.1,
  1.2, 1.4, the extended comparison discussion, and §3.5. Its stronger
  curvature hypotheses are not silently imported into the target.
- The current Bracci-Kraus-Roth boundary-rigidity paper was inspected at
  Theorems 2.1–2.4 and proofs §§4.1 and 4.4. It assumes the opposite
  curvature inequality in its strong Schwarz result and asks for a sharp
  ratio rate. It does not verify the present minimum-regularity question.
- A publicly available 2013 thesis was inspected as a cross-check of the
  chart method. It has transcription errors in some displayed metric
  labels; it is not relied on as the authority for (6.1).
- The controls verify explicit differential identities, lengths, and
  normalization algebra. They do not certify Montel compactness, topology,
  the cited disk theorem, or the full analytic proof. Those require review.
