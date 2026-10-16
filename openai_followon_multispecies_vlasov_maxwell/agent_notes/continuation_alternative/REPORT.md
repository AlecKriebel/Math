# Independent continuation and aggregate-energy family

Audit timestamp: 2026-10-07T04:23:32Z (2026-10-06, America/Los_Angeles).
Agent: continuation_alternative. No external individual contacted. No Git mutation or publication performed.

## Finding and status

The standard local/continuation machinery supports a finite-species formulation, but does not produce the required a priori simultaneous momentum bound. Aggregate positivity and a discrete species label preserve energy; they do **not** convert opposite charges into one scalar positive Vlasov equation. This approach is blocked as a route to the full target unless a genuinely new characteristic-force estimate is supplied.

Strongest independently derived results: exact mass-normalized equations, positive energy and null flux, local Sobolev uniqueness/construction, and a scalar reduction when all nonempty charged species have one common charge-to-mass ratio. The last reduction is conditional on a valid one-species global theorem; it is an elementary structural reduction, not a novelty claim. It does not include the equal-mass ±1 case.

Best-guess progress for this approach family: mathematical full target 8%; publication package 0%. These numbers are judgments, not evidence.

## Normalization and conservation, proved directly

Use rationalized units c=1 and Maxwell equations E_t−curl B=−j, B_t+curl E=0, div E=ρ, div B=0. In physical momentum P, the species velocity is P/sqrt(m_a²+|P|²), and force is e_a(E+v_a×B). Put p=P/m_a, q=sqrt(1+|p|²), u=p/q, F_a(t,x,p)=m_a³ f_a(t,x,m_a p), and κ_a=e_a/m_a. The Jacobian is essential: F_a dp=f_a dP. Then

    S F_a + κ_a K·∇p F_a=0,
    S=∂t+u·∇x, K=E+u×B,
    ρ=Σ_a e_a ∫F_a dp, j=Σ_a e_a ∫u F_a dp.

Because ∇p u is symmetric, div_p(u×B)=0. Every species flow preserves phase volume, nonnegativity and its particle number; F_a is constant on its own flow. For every finite closed classical time slab, |u|<1 gives spatial support |x|≤R0+t, and continuity of fields on that compact cylinder bounds force there. Its momentum support therefore stays compact on each such slab. This statement does not bound momentum uniformly up to a possible finite maximal time.

Integrating each transport equation in p gives ∂tρ+div j=0. Maxwell then propagates both constraints; no total-charge cancellation enters this argument.

Set

    k(t,x)=Σ_a m_a ∫q F_a dp,
    h(t,x)=Σ_a m_a ∫p F_a dp,
    e(t,x)=k+(|E|²+|B|²)/2,
    z(t,x)=h+E×B.

Multiplying transport by m_a q and integrating by parts gives k_t+div h=j·E. The magnetic contribution vanishes because u·(u×B)=0 and m_aκ_a=e_a, including negative e_a. Maxwell gives the opposite −j·E. Thus e_t+div z=0. Since |p|≤q and |E×B|≤(|E|²+|B|²)/2, |z|≤e. With finite energy and standard cutoffs, total energy is conserved. The null-boundary flux e+z·ω is nonnegative. In particular its kinetic part is Σ_a m_a ∫q(1+u·ω)F_a dp≥0. The charge signs are absent from the positive energy and null flux. Mass dependence remains positive, fixed, and cannot be discarded:

    Σ_a ∫q F_a dp ≤ k/min_a m_a,
    |ρ|, |j| ≤ max_a(|e_a|/m_a) k.

These bounds are uniform for fixed positive masses, not uniformly as a mass tends to zero. They are integrable/energy bounds, not pointwise field or momentum-support bounds.

## Why aggregate scalar reduction fails

For equal masses m=1 and charges ±1 put h=F_++F_- and g=F_+−F_-. Exactly,

    S h + K·∇p g=0,
    S g + K·∇p h=0,
    ρ=∫g dp, j=∫u g dp, h≥|g|.

Neither h nor g obeys the scalar unit-charge Vlasov equation except in special invariant situations. For example, Sg+K·∇p g=−2K·∇p F_-, generally nonzero. Replacing signed g by positive h changes Maxwell sources. Assuming h obeys the one-species equation therefore assumes away the coupled difficulty.

More generally, write G_r=Σ_a e_a κ_a^r F_a. Then SG_r+K·∇p G_(r+1)=0. If the distinct κ_a are κ_1,…,κ_d, their minimal polynomial closes this into d transport equations; diagonalizing returns the original acceleration groups. A species label or finite moment hierarchy is an equivalent reformulation, not a new estimate. A common field cannot be rescaled differently for each receiver species.

A valid special reduction is available if κ_a=κ≠0 for every nonempty charged species. Neutral species may be included: they transport freely and do not contribute to Maxwell sources. Define

    G=κ Σ_a e_a F_a=κ² Σ_a m_a F_a≥0,
    E'=κE, B'=κB.

Then G,E',B' satisfy precisely unit-mass/unit-charge scalar VM, with the same normalized velocity u. Conversely, after solving scalar VM, each F_a is reconstructed from its initial value by the common characteristic flow driven by E',B'; their weighted sum is G by transport uniqueness. The energy of the transformed scalar system is κ² times the original energy. The reduction works for κ<0 as well. κ=0 means all species are neutral and gives free transport plus vacuum Maxwell directly. Identical species can also be merged within each common κ group. This does not reduce the number of distinct charge-to-mass groups.

## Explicit limitation of the energy route

Choose nonnegative smooth compactly supported unit-integral φ(x), h0(p), and hR(p)=h0(p−R e1). Let A0=∫q h0 and AR=∫q hR. Fix A*>A0 and for R sufficiently large put εR=(A*−A0)/(AR−A0)∈(0,1). Define

    F_R(x,p)=φ(x)[(1−εR)h0(p)+εR hR(p)].

Every F_R has the same particle number 1, the same kinetic energy A*, fixed spatial support, uniformly bounded L∞ norm, and uniformly bounded derivatives of every fixed order; its momentum support tends to infinity. The formula εR~(A*−A0)/R is enough to check all assertions. Put F_+=F_-=F_R and E0=B0=0. All Maxwell constraints hold, total energy is exactly 2A*, and an actual global solution is free transport with F_+=F_-=F_R(x−tu(p),p), E=B=0. Hence even fixed particle numbers, energy, spatial radius and uniform smooth norms do not determine momentum radius without the initial momentum radius. This is **not** a counterexample to the target global theorem or to a datum-dependent growth bound; it falsifies only a direct energy-to-support inequality. To prove growth control from fixed initial support requires dynamical information absent from aggregate energy.

## Local class and conventional continuation: precise dependency scope

A convenient independently constructible class is F_a0∈C_c∞(R⁶), E0,B0∈⋂_(k≥0)H^k(R³), satisfying the signed Gauss constraints. For k≥6 define Yk=Σ_a||F_a||H^k+||(E,B)||H^k. With momentum supports in |p|≤R, phase-space integration by parts, integer tame-product estimates, and Cauchy–Schwarz in p give

    Yk(t) ≤ Yk(0)+C∫_0^t [1+||(E,B)||W^(1,∞)+Σ_a||∇_(x,p)F_a||∞]Yk(s) ds,

where C depends on k,R,N and the fixed e_a,κ_a. In the force commutators use a momentum cutoff equal to 1 on |p|≤R; no cutoff alters the leading divergence-free transport. The current estimate is ||j||H^k≤|B_R|^(1/2)Σ_a|e_a| ||F_a||H^k. Linear transport/Maxwell iteration gives a common H^6 lifespan and keeps radius at most R_initial+1 after taking it sufficiently short. L² difference energies contract because derivatives of each iterate are bounded by H^6 embedding. Higher tame bounds preserve every H^k and positivity. This directly verifies local existence and uniqueness; it does not prove bounded-momentum continuation by itself because the displayed coefficient contains first derivatives.

The stronger bounded-momentum criterion is established machinery. Glassey's book states the finite-species formulation, and its final proof discussion explains species-dependent streaming plus signed source sums. However its printed theorem includes neutrality in the preceding assumptions. Luk–Strain's H^5 theorem has no neutrality assumption and explicitly notes multispecies extension, with details omitted. A follow-on manuscript should supply this adaptation or cite a precise finite-species theorem, rather than silently drop the book's neutral-data clause.

On a hypothesized uniformly bounded radius R, the Bouchut–Golse–Pallard division lemma has denominators bounded away from zero by 1−R/sqrt(1+R²)>0. Its kernels depend on u, not on κ_a. Transport substitution contributes κ_a; Maxwell averages contribute e_a; signs are removed by absolute values. Summing the finitely many wave-average bounds yields a finite field bound. Summing its second-derivative estimates yields

    ||(E,B)(t)||W^(1,∞) ≤ C[1+log(2+N(t))],
    N(t)=max_(s≤t) Σ_a||∇_(x,p)F_a(s)||∞,
    N(t) ≤ N(0)+C∫_0^t [1+log(2+N(s))]N(s) ds.

This closes by the logarithmic Gronwall/Osgood integral, once the adapted kernel estimates are supplied; finite species signs do not obstruct that step. The cited proof's Sections 4 and 5 were read, not merely its abstract. The zero-charge species contribute no field term and have free transport, so cannot produce a continuation obstruction. This standard bounded-radius mechanism is different from proving a priori R<∞; the constants depend on R and cannot be sent to infinity to solve the target.

For the wider upstream field class C_b∞∩L², the finite-horizon Coulomb/vector-potential modification in upstream continuation.tex can be repeated using signed smooth compact ρ0. Its Coulomb field is in every H^k in dimension 3 even when total charge is nonzero (Fourier size O(|ξ|^−1) near ξ=0 is square integrable). The removed divergence-free vacuum field vanishes in the particle cone. This validates that neutrality is not forced by finite energy. It does not show that arbitrary smooth finite-energy fields with unbounded derivatives fit the proof, and no such claim is made.

## Exact remaining gap

To establish the user target, one must bound the joint normalized support Q(t)=max_a max_(z∈supp F_a0) q(V_a(t,z)) independently of the compact prefix time below T_max. No aggregate-energy argument above provides the requested species-pair signed impulse estimate, angular occupation bound, selected-range coefficient estimate, or uniform strict improvement of a simultaneous bootstrap. In the equal-mass ±1 case, the aggregate system already retains two coupled accelerations. No claim of completion, novelty or publication readiness is justified.
