# CTDT interface: complete finite-configuration repair and verification

Audit date: 2026-10-10 (UTC).

## Verdict and scope

**The application of Last–Peccati–Yogeshwaran (LPY), Corollary 4.1, to the finite-box exploration in Bérard–Dembin–Marêché (BDM), §§3.1 and 3.3, is valid after making the all-configuration convention explicit as below. No obstruction remains at this interface.** The argument below proves all the required stopping-set, measurability, continuity, increment, and determination hypotheses. It does not assume that a merely almost-sure algorithm automatically extends to a stopping set on every configuration.

BDM footnote 9 leaves two details implicit: its arbitrary tie order should be chosen Borel, and simultaneous atoms at different sites need a specified update convention. The synchronous, pre-time-state convention below is compatible with the displayed update rule and makes their exploration correct for every finite counting measure. It agrees with the usual graphical construction almost surely. No discretization or weaker substitute for LPY is needed.

This report verifies this interface and its revealment estimate, not unrelated parts of the IPS proof.

## Sources inspected

- Jean Bérard, Barbara Dembin, Laure Marêché, *Sharpness for monotone absorbing Interacting Particle Systems*, [arXiv:2510.11424v2](https://arxiv.org/abs/2510.11424v2), 24 November 2025, especially printed pp. 6, 11–15. The p. 14 exploration and footnotes were also visually inspected in the PDF.
- Günter Last, Giovanni Peccati, D. Yogeshwaran, *Phase transitions and noise sensitivity on the Poisson space via stopping sets and decision trees*, [arXiv:2101.07180v3](https://arxiv.org/abs/2101.07180v3), especially §1.5, §2, (3.2)–(3.5), Corollary 4.1 and Appendix A (A.1).

Inspected PDF integrity:

- BDM: 294584 bytes; SHA-256 `ae1411968b797f149f050b553dd035225707d29a7739e003c26213b73878fd2d`.
- LPY: 793484 bytes; SHA-256 `dceb9e19a634d8cf93b55a6ec048346f69ee1654579bbbe35beaa81de0301269`.

## 1. Finite ambient space and an all-configuration graphical model

Fix a finite box V = Λ_m containing the origin, a horizon T > 0, and the finite neighborhood N = Λ_R containing 0. States outside V are fixed at zero. Use the conventional local configuration centered at x, namely ξ_x(y) = ξ(x+y). This removes the separate sign-convention typo in the source's definition of spatial shifts.

Let K = [0,M] × {A,B}, with M > 0 as in the source, and let

    X = V × [0,T] × K.

Take B_n = X for every n. Then the LPY configuration space consists of **all finite integer-valued measures** on X, including measures with multiplicities, same-time atoms, and atoms on the time and mark boundaries. The intensity λ_h is the source's restriction to X. It is finite, with total mass M|V|T, and diffuse because its time marginal has a Lebesgue factor, also when h is 0 or 1. Thus the diffuse-intensity assumption retained in LPY §4 is satisfied in this application.

For every finite counting measure μ, define the graphical trajectory from an initial time a ∈ [0,T] and an initial configuration ξ as follows.

1. Ignore atoms with time ≤ a. In particular, a trajectory starting at a has value ξ at a and uses clocks strictly after a.
2. Ignore atoms of the form (x,t,M,A). This exceptional A-mark could otherwise create a 1 from a zero neighborhood because of the closed upper interval in the displayed source update rule. It has zero λ_h-measure.
3. At each fixed pair (x,t), choose one distinct remaining mark, if any, by the fixed lexicographic Borel order on (u,1{w=A}). Multiplicities have no further effect. The particular Borel order is immaterial.
4. Process the finitely many distinct times in increasing order. At a given time t, update all sites having selected marks **simultaneously**, using the single pre-time state X_{t-} in each local update. Other sites retain their states.

The local A- and B-update maps are the maps in BDM §2.1.1. On the retained A-marks u<M, they are increasing functions of the configuration and output zero when the entire relevant neighborhood is zero. B-updates output zero. For completeness, the A-map has thresholds α(ξ)=c_0(ξ), β(ξ)=M-c_1(ξ), with α≤β and both thresholds nonincreasing as ξ increases. If the output for ξ is 1, either u≥β(ξ), in which case u≥β(η) for η≥ξ, or ξ(x)=1 and u≥α(ξ), in which case η(x)=1 and u≥α(η). Hence the output for η is also 1. Absorption follows from c_1(0)=0 and u<M. Simultaneous application to any chosen subset of sites is therefore also monotone and zero-preserving.

Denote by X_t^a[μ], a≤t≤T, this trajectory started from all 1 on V at time a. All these maps, jointly in (a,t,μ), are measurable. One explicit justification is to use a Borel enumeration of a finite counting measure on the standard Borel space X, sort its finitely many time coordinates, select each site's minimum valid mark by Borel comparisons, and perform a finite recursion. On each stratum μ(X)=n every operation is Borel; the result is independent of the enumeration. The same argument applies when an arbitrary initial state is supplied.

Define the target function

    f(μ) = X_T^0[μ](0) ∈ {0,1}.

It is measurable and agrees almost surely with the intended finite-volume IPS observable. This convention also defines it on configurations having measure zero under the Poisson law.

## 2. One-pass exploration and the replay lemma

For a≤t≤T put

    A_t^a(μ) = {x∈V : some y∈(x+N)∩V has X_t^a[μ](y)=1}.

For 0≤r≤T-a define the revealed set

    E_r^a(μ) = {(x,t,u,w)∈X : a<t≤a+r and x∈A_{t-}^a(μ)}.

The formula reveals the **whole mark fiber** at any queried site-time, including ignored marks and all multiplicities. This matters: the atom-selection rule at a queried site-time must be determined entirely by the data in that fiber. It also gives E_0^a=∅. The definition is the source's moving-slab exploration, expressed without an implicit recursive event-time convention.

### Replay lemma

If ν is any finite counting measure agreeing with μ on E_r^a(μ), then

    X_t^a[ν] = X_t^a[μ] for every a≤t≤a+r,
    E_r^a(ν) = E_r^a(μ).

Here agreement means ν restricted to E_r^a(μ) equals μ restricted to E_r^a(μ); outside that set ν is unrestricted.

Proof. List the finitely many time coordinates of the union of the supports of μ and ν in (a,a+r]. Induct over this common ordered list. Initially the two states are identical. Suppose they agree just before time t. Their active site sets then agree. At each active site x, the entire fiber {x}×{t}×K lies in E_r^a(μ), so both measures supply exactly the same selected mark or no mark. At an inactive site, every state in its relevant neighborhood is zero, including the site's own state because 0∈N. Any selected update leaves that site zero, and absence of an update also leaves it zero. Thus the two simultaneous post-time states agree. This proves the trajectory assertion, and the formula defining E gives the set assertion.

Consequently, taking ν=μ_{E_r^a(μ)}+ψ_{E_r^a(μ)^c} proves LPY's full stopping-set identity (A.1) for **every μ,ψ**, not just Poisson-almost surely. The same argument proves that E_r^a determines the whole explored trajectory.

Graph measurability is immediate from the preceding measurable trajectory construction and the formula for E: the map (a,r,μ,x,t,u,w)↦1{(x,t,u,w)∈E_r^a(μ)} is measurable. In particular, joint dependence on the random cut time is legitimate.

## 3. Two-pass randomized CTDT

For each deterministic a∈[0,T] let L_a=T-a and

    B_a(μ) = f_a(μ) = X_T^a[μ](0).

The replay lemma shows that B_a is determined by E_{L_a}^a. For exploration time r≥0, define

    Z_r^a(μ) = E_r^a(μ),                                      0≤r≤L_a;
    Z_r^a(μ) = E_{L_a}^a(μ),                                  r>L_a, B_a(μ)=0;
    Z_r^a(μ) = E_{L_a}^a(μ) ∪ E_{min(r-L_a,T)}^0(μ),           r>L_a, B_a(μ)=1.

The sets are constant by time L_a+T≤2T. This formula also covers a=0 and a=T: when a=T the first pass is empty and B_a=1, so the second pass starts at r=0 with E_0^0=∅. Let S be independent and uniform on [0,T], and take Z_r=Z_r^S.

### Stopping-set identity for the concatenation

Fix a and r and replace μ outside Z_r^a(μ) by an arbitrary ψ. For r≤L_a, the replay lemma applies directly. For r>L_a, the first terminal set E_{L_a}^a(μ) is a subset of Z_r^a(μ); therefore its full trajectory and terminal value B_a are unchanged. If B_a=0 the claim follows. If B_a=1, the replacement also preserves μ on E_{min(r-L_a,T)}^0(μ); the replay lemma preserves this second revealed set as well. The union is therefore unchanged. This is exactly (A.1).

Graph measurability, including joint measurability in a, follows from that of E and B_a. Every revealed set lies in X=B_1, so the localizing-ring condition is automatic.

## 4. Continuity and instantaneous increments

### Increasing and right-continuous sets

For a fixed a and μ the one-pass sets increase in r, and

    E_r^a(μ) = intersection over q>r of E_q^a(μ),

within the horizon, with constant continuation after it. Indeed membership of a fixed point (x,t,u,w) is the conjunction of the fixed condition x∈A_{t-}^a(μ), the strict condition t>a, and the closed inequality t≤a+r. The starting slice t=a is never included. Thus right continuity holds at r=0 as well. At the two-pass switching time r=L_a the added set is E_0^0=∅, and its decreasing right limit is also empty. Union with the fixed first terminal set therefore preserves right continuity. The continuation after the second pass is constant. All these assertions hold for every finite μ, including simultaneous-time configurations.

### Initial intensity and λ-continuity

Z_0^a(μ)=∅ for every μ and a. Hence E[λ_h(Z_0^a(η))]=0.

For r>0 a one-pass increment satisfies

    E_r^a(μ) \ (union over q<r of E_q^a(μ))
       ⊂ V × {a+r} × K.

In the first CTDT phase, each instantaneous increment lies in the physical-time slice a+r. In the second phase, it lies in the physical-time slice r-L_a, after subtracting any already revealed points. At the phase switch no new set is added. A fixed physical-time slice has λ_h-measure zero. Thus LPY (3.4), equivalently BDM (14), holds for **all μ and all r**, not merely almost surely.

### At most one Poisson atom in every increment

The projection of the finite Poisson process η onto physical time has intensity M|V| times Lebesgue measure. It is almost surely simple: all atoms of η have distinct physical times, simultaneously over the entire finite configuration. Every CTDT increment is contained in one physical-time slice, and the switching time adds no slice of a second physical time. Therefore

    P(η(Z_r^a(η) \ Z_{r-}^a(η))≤1 for all r≥0)=1.

This proves LPY (3.5), equivalently BDM (15). The one-null-set argument uses simplicity of the whole time projection, not a union over uncountably many individual zero-probability events. It works for every a, hence certainly for almost every cut-time parameter.

## 5. Determination on every configuration and hybrid convergence

Let Z^a=Z_∞^a and ν=μ_{Z^a(μ)}.

If B_a(μ)=1, the terminal revealed set contains E_T^0(μ). The replay lemma for the second pass yields f(ν)=f(μ).

If B_a(μ)=0, the replay lemma yields X_T^a[ν](0)=X_T^a[μ](0)=0. For either driving measure κ=μ or κ=ν, the trajectory started at time 0 has a configuration at time a bounded by all 1. By monotonicity, using the same post-a clocks,

    X_t^0[κ] ≤ X_t^a[κ] for every t≥a.

The inequality also holds when κ has atoms exactly at a: the lower trajectory has already processed them, whereas the upper trajectory starts from the maximal configuration at a and ignores those clocks. Hence f(μ)=f(ν)=0. This proves LPY (3.2) for every μ and every a.

The remaining determining condition, LPY (3.3), is stronger than needed here but immediate without a limiting argument. For every r≥2T, Z_r^a=Z_∞^a. Consequently the source's hybrid configuration is exactly

    ζ_r = η_{Z_∞^a(η)\Z_r^a(η)} + η'_{Z_r^a(η)} + η'_{X\Z_∞^a(η)}
         = η'.

Thus f(ζ_r)=f(η') from that deterministic time onward. The condition for g=f in Corollary 4.1 is identical and holds automatically.

## 6. The same revealment bound and applicability

The repaired construction agrees almost surely with BDM's exploration for each fixed cut time a. The only conventions added concern configurations with a boundary mark, repeated physical times, multiple atoms at the same location, or clocks exactly at a. Each is a null event under the relevant Poisson law. In particular, the source's law, variance, and integrated absolute add-one cost remain unchanged. More generally, if two bounded versions agree Poisson-almost surely, Mecke's formula implies that they agree also for (P⊗λ_h)-almost every add-one configuration; changes of null-set versions therefore do not alter the OSSS integral.

For a fixed queried point z=(x,t,u,w), excluding the null event S=t, membership in Z_∞^S implies either that the auxiliary trajectory survived at the origin at T, or that S<t and its relevant neighborhood was occupied just before t. Therefore

    P_h(z∈Z_∞^S)
      ≤ (1/T) ∫_0^T [P_h(X_{T-a}^m(0)=1)
          + 1{a<t} Σ_{y∈(x+N)∩V} P_h(X_{t-a-}^m(y)=1)] da.

A finite-rate finite-state chain has no jump at a deterministic time almost surely, so its one-site probabilities are continuous and the left-limit symbol can be removed. Each integral is bounded by the integral over [0,T] of the largest finite-box density. This gives BDM (19):

    P_h(z∈Z_∞^S)
      ≤ (|N|+1)/T ∫_0^T max_{y∈V} P_h(X_s^m(y)=1) ds.

Monotone domination by the process on y+Λ_{2m}, started from all 1 **on that translated box**, gives max_y P_h(X_s^m(y)=1)≤θ_s^{2m}(h), and hence BDM (20). The translated initial condition is the harmless separate typo already identified in the source.

We have now checked: standard Borel ambient space; finite diffuse intensity; measurable bounded f; independent randomization; jointly graph-measurable stopping sets on every finite counting measure; boundedness; monotonicity in exploration time; right continuity including phase endpoints; zero initial intensity; zero-intensity increments for every configuration; at most one Poisson atom per increment almost surely; pointwise determination; and the hybrid convergence condition. LPY Corollary 4.1 therefore gives exactly

    Var_h(f) ≤ 2 ∫_X P_h(z∈Z_∞^S) E_h|f(η+δ_z)-f(η)| λ_h(dz).

**Conclusion:** this CTDT/OSSS interface is independently discharged, with an explicit null-configuration completion. The source's brief assertion is not being accepted without proof; the argument above supplies the missing details.
