# Independent transport and measure audit of PR 284

**ACCEPT the original submitted Theorem A and Theorem B in their stated setting.** No mandatory mathematical correction was found. This verdict binds original head 391cb662b1599ef564ff15b63cd8ed73c7d1f125. The baseline was frozen before author mathematics; the independent mathematical finding was frozen before the historical review was read. Prior PASS was not used as a certificate.

The accepted setting is a locally compact second countable Hausdorff Abelian group G, locally finite Radon measures, a jointly measurable action on an arbitrary measurable state space, a covariant random measure ξ, and sigma-finite Q with Q(ξ(G)=0)=0. Theorem A retains arbitrary auxiliary state and permits a non-sigma-finite ξ-marginal. Theorem B is a canonical sigma-finite measure-law theorem; its Cox matching observes the original measure as background.

## Exact claim and credited inputs

For every covariant, ξ-preserving, measure-only Markov kernel K and every nonnegative measurable f, the hypothesis is

    ∫Q(dω)∫K(ξω,0,dt)f(θtω)=∫Q(dω)f(ω).

The conclusion is Campbell reversal c=R*c, where

    c(dω,dt)=Q(dω)ξω(dt),  R(ω,t)=(θtω,−t).

This is the full joint-state Mecke identity. The [2009 primary paper](https://arxiv.org/pdf/0906.2062v1), equation (2.7), supplies the Mecke/Palm equivalence on the same measurable setting, Theorem 6.3 supplies Palm/mass-stationarity equivalence, and Theorem 4.1 gives invariance under preserving transports. These are established inputs; their converse narrowing to Markov kernels is the submitted deduction. Its Problem 7.3 restricts kernels to ξ-measurability while testing the full state law.

The [OWR contribution](https://ems.press/content/serial-article-files/46189), printed p.2673, motivates its Cox question through the joint intensity and inserted-Cox object. The [2015 author edition](https://arxiv.org/pdf/1405.7566v2), Section 9, distinguishes its weighted kernels from Markov kernels. This is attribution, not a proof or current novelty clearance. [Struble's theorem](https://www.numdam.org/item/CM_1974__28_3_217_0.pdf), printed p.217, supplies the proper compatible invariant metric. No unread 2011 theorem is used as a proof premise.

## Admissibility of the local gates

For symmetric compact C define

    aC(µ;s,t)=1C(t−s)/[(1+µ(s+C))(1+µ(t+C))].

Local finiteness makes denominators finite. The row rate is at most µ(s+C)/(1+µ(s+C))≤1. If b(µ,t) is a Borel indicator invariant under R0(µ,t)=(θtµ,−t), then

    ab(µ;s,t)=aC(µ;s,t)b(θsµ,t−s)

is symmetric, covariant and has row rate rb≤1. Therefore

    Kb(µ,s,dt)=ab(µ;s,t)µ(dt)+(1−rb(µ,s))δs(dt)

is a probability kernel. Symmetry and Tonelli give, for nonnegative φ,

    ∫∫φ(t)ab(µ;s,t)µ(ds)µ(dt)=∫φ(t)rb(µ,t)µ(dt).

The holding term supplies the remainder, proving exact spatial preservation. This uses no finite total mass, and the kernel depends only on µ and s.

## Off-measure-diagonal reversal, without finite marginal law

Let m=aC(ξ;0,t)c, ρ(ω,t)=(ξω,t), and J={(ω,t):θtξω=ξω}. For Q(f)<∞, subtracting the finite holding integral from invariance gives

    ∫b(ξω,t)[f(θtω)−f(ω)]m(dω,dt)=0.

Both jump integrals are finite: outgoing is bounded by Q(f), incoming by the full invariant kernel expectation Q(f). No infinity is subtracted.

For Borel measure-state A and displacement B put

    FA={(µ,t):µ∈A,θtµ∉A}, F=FA∩(M×B).

F and R0F are disjoint, hence b=1F+1R0F is an allowed indicator. Use f=1D1A(ξ), Q(D)<∞. Incoming f vanishes on F; outgoing f vanishes on R0F. Reversal of the incoming term gives exactly

    m((D×B)∩ρ⁻¹FA)=R*m((D×B)∩ρ⁻¹FA).

Taking B=G and a countable finite-Q partition Dj produces a common finite cover for both restricted measures. Sum over D∩Dj to obtain arbitrary D, then use rectangle uniqueness on the product sigma-field. This uniqueness requires sigma-finiteness of the measures, not countable generation of the auxiliary state space.

A countable separating family on the standard Borel Radon-measure space, closed under complements, makes the oriented FA pieces cover J-complement. A disjoint refinement gives m=R*m there. The symmetric density is positive for t∈C, so integrating min(k,1/aC) deweights. A symmetric compact exhaustion gives c=R*c on J-complement.

The Campbell measure is sigma-finite on

    {ω∈Dj:ξω(Cn)≤k}×Cn,

whose mass is at most kQ(Dj). Reversal has the same finite masses wherever equality is established. No conditioning on the possibly non-sigma-finite ξ-marginal occurs.

## The period kernel preserves ξ and retains hidden states

For fixed µ the period group Hµ={t:θtµ=µ} is closed, because translations act continuously in the vague topology. Its graph is Borel, and Hθsµ=Hµ by commutativity.

For relatively compact Borel B put wB(µ)=µ(Hµ∩B). Normalize the restricted measure on Hµ∩B when wB>0 and use δ0 otherwise. Parameter integration proves measurability; local finiteness proves the denominator finite. Translating this row from θsµ by s proves covariance.

For fixed µ,s, the restriction (θsµ)|H is a locally finite H-invariant measure, hence csλH with finite cs≥0. If λH(B∩H)=0 every row holds. Otherwise E={s:cs>0} is H-invariant and all rows on E have the same displacement probability ρB=λH|B/λH(B∩H). Since µ|E is H-invariant,

    ∫EρB(A−s)µ(ds)
      =∫ρB(dh)µ(E∩(A−h))=µ(E∩A).

The complement holds. Thus the submitted kernel preserves µ pointwise. The coefficient may vary between cosets; the proof correctly permits this. No measurable family of Haar normalizations is selected.

All supported displacements fix ξ and therefore wB(ξ). Applying invariance to the nonnegative test wB(ξ)f gives

    ∫Q(dω)∫Hξ∩B f(θtω)ξω(dt)=∫Q(dω)f(ω)wB(ξω).

There is no subtraction, so infinite expectations cause no gap. Apply this identity to −B and use Haar inversion on the Abelian subgroup to obtain Campbell reversal on J. The same local finite-mass cover extends product tests to the full product sigma-field. Together with the preceding locus, this proves full joint Mecke reversal and Theorem A.

## Turn 1 and the separate Cox construction

Turn 1 is valid in its stated canonical scope. Positive integrable h(µ) makes a finite test measure. Symmetric gates make each state difference annihilate the antisymmetric reversal defect; countable canonical-state separation kills it off the stabilizer, and conditional Haar symmetry kills it on the stabilizer. The proof correctly records that this alone cannot identify hidden auxiliary states. Turn 2 closes that gap through the period kernels, without silently identifying state and measure.

For Theorem B, the proper invariant metric gives compact

    U(s,t)=closed_ball(s,d(s,t))∪closed_ball(t,d(s,t)).

Pair only distinct singleton endpoints with exactly two counting points in this union. Two partners for s are impossible: the nearer one appears in the farther pair's s-ball. Ties fail identically. A symmetric measure gate retains both orientations together. Multiple atoms stay fixed. The allocation is an equivariant involution preserving the full counting measure.

Measurability follows by integrating the unique partner indicator against the counting kernel. Its value is zero or a unit atom; on standard Borel G it determines a measurable partner, with holding elsewhere.

Insert δs into a Poisson measure of intensity µ. Campbell–Mecke applied to candidate t inserts δt. The pair condition is exactly that the original Poisson measure vanish on U(s,t). Hence the off-diagonal jump density is

    1s≠t b(θsµ,t−s) exp(−µ(U(s,t))) µ(dt).

The exponent includes atom masses at BOTH endpoints. The diagonal stays in the holding mass. Actual partner uniqueness proves the row bound. Endpoint symmetry and Tonelli prove preservation. Compactness makes this density strictly positive at all distinct pairs. The Poisson-series calculation allows repeated locations; partners at distance ≤R need information only in the compact radius-2R ball, validating exhaustion.

The required oriented gates are actual members of this matching family. They recover reversal off canonical periods. On periods, reversal fixes µ and Haar symmetry handles the even density. Deweighting works for t≠0; at t=0 reversal is the identity. This proves canonical Cox sufficiency independently of Theorem A.

## Adversarial boundaries

- Zero measure: a canonical zero-state law passes all origin shift tests trivially, but fails the nonzero mass-stationarity convention. Its explicit exclusion is essential and matches the formal source.
- Unsupported root: Campbell reversal concentrates the rooted state on support, because its reversed representation roots at a ξ-point. On an unsupported-root event the Campbell mass vanishes; nonzeroness and a countable compact exhaustion imply its Q-mass vanishes. Root support is a conclusion, not a missing premise.
- Non-sigma-finite marginal: let G=Z/2, ξ be constant counting measure, Ω=N×G, and Q=counting_N×δ0. Q is sigma-finite, but its ξ-marginal puts infinite mass on one canonical state. Translation by the nonzero period is a preserving measure-only kernel and fails invariance on a single-fiber test. The period argument detects this, while replacing the state by ξ would lose it.
- Infinite totals/intensity: the proof uses nonnegative spatial integrals, local compact mass bounds and finite-Q state tests. Q(Ω), ξ(G) and Palm intensity may all be infinite. The canonical law of δ0 on R is also covered: its root stays fixed and Campbell reversal is trivial, while stationary unrooting is an infinite measure.
- Atomic/diffuse/mixed/periodic: local denominators, subgroup zero branches, discrete periods, vanishing subgroup restriction and constant measures are included. The Cox endpoint factors and zero-displacement holding term are explicit.
- Source boundary: Theorem A answers the imported all-Markov statement and formal Annals Problem 7.3. Theorem B accepts ξ as background, consistent with OWR's joint object. A stricter Cox-realization-only rule and a full joint-state Cox characterization are not established. Non-Abelian, non-second-countable or non-locally-finite extensions are outside the result. The unread 2011 final text is not a missing proof lemma; its exact stricter conventions remain unverified.

## Native evidence and exact remaining gap

All 21 attempt files plus the full original QUEUE match every snapshot hash and byte count, with mode 0444. Four reacquired PDFs match author source hashes. The superseded 2007 PDF was not reacquired; its hash is an original manifest assertion only.

Default and bundled Python each lack SymPy. All eight failures remain. Workspace Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0 replay the unchanged two author scripts and historical reviewer script byte-for-byte: 18,814, 75,172 and 186,869 assertions. Stderr is empty and every exit code is zero. Actual child PIDs are 82655, 82675, 82694. The owning driver reaps all children with Popen.wait. Prelaunch argv, cwd, executable/source hashes, PIDs, streams, statuses and post-source hashes are preserved in native/. Dependency source hashes and replay comparisons are separately cataloged. No wait status is inferred from a tool-session ID.

The finite controls support gate rank, preservation, atom factors, ties, multiplicities, period kernels and hidden marks. They do not imply an infinite theorem; the analytic argument above supplies that conclusion. Historical review was read only after the independent finding, for consistency and replay.

**Strongest accepted result:** full joint Mecke reversal from all measure-only preserving Markov transports in the stated sigma-finite setting, plus the separate canonical Cox matching characterization with intensity background.

**Exact remaining mathematical gap in these stated claims:** none found. **Unassessed:** historical novelty, priority, exhaustive current literature, community acceptance and publication clearance. No additional author proof attempt or wider unstated theorem is introduced.
