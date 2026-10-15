Current administrative status as of 2026-10-06T06:45:26.412290+00:00: published preprint 10.5281/zenodo.23180194 (https://zenodo.org/records/23180194); actual tracker 1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20 / sheet 1254632077 (Math Puzzles), row 30, range 'Math Puzzles'!A30:D30, read back and ROOT-accepted. Two sequential whole-preprint reviews are completed for immutable candidate03 content. The administrative successor requires separate ROOT ancestry/parity and source-guard acceptance; native merge is not certified here. Exact22 public payloads and all mathematics are unchanged; unrefereed, extensive AI assistance, no human peer review or formal machine proof.

The entire retained candidate03 text below is historical as of its frozen preparation03 checkpoint, including earlier pending, DOI-none, review-request and workflow statements. Frozen original/rejection/checkpoint records remain historical evidence.

---

# Turn 2: abstract measure-only Markov theorem and separately scoped background-retaining Cox matchings

**Corrected author version; ROOT accepted the exact mathematical scopes of A and B, and bounded priority for precise formal A is accepted with disclosed gaps; fresh global preprint review remains pending.** A proves the formal all-Markov theorem on the arbitrary ambient flow. B proves only the specified canonical intensity-background Cox matching theorem. The original claim that B closes Last's full narrower OWR allocation question is withdrawn. Read SCOPE_AND_CREDIT.md for source selection, credit, unrefereed/AI disclosure and remaining gap. The original two substantive author turns remain 2/5; one joint turn-3 repair campaign brings the current total to 3/5.

## 1. Statements and conventions

Throughout G is a locally compact second countable Hausdorff Abelian group. Its Radon-measure space M is standard Borel. Set θ_sµ(B)=µ(B+s). On an arbitrary measurable space (Ω,F), let (θ_s) be a jointly measurable group action, ξ:Ω→M measurable and covariant, and Q σ-finite with Q(ξ(G)=0)=0. A transport kernel is Markov, covariant as in Last–Thorisson (2009), (3.1), and preserves ξ pointwise. The invariance assumption is

    E_Q ∫f(θ_tω)K(ξ(ω),0,dt)=E_Q f(ω)                (I)

for all nonnegative measurable f and every invariant ξ-preserving kernel depending only on ξ and the starting location. This is the precise measure-only test restriction in Annals Problem 7.3. Ω need not be countably generated, and the image Q∘ξ⁻¹ need not be σ-finite.

**Theorem A.** Condition (I) is equivalent to mass-stationarity of Q for ξ. In particular it yields the full joint-state Mecke equation, with arbitrary measurable tests on Ω×G.

**Theorem B.** For a σ-finite law Q on the canonical space M\{0}, it already suffices to require invariance under the Cox-derived kernels of the singleton matching family in Section 6. These are genuine deterministic invariant matchings of the locally finite counting measure ζ+δ_s, allowing the original µ as background. They work for arbitrary atomic, diffuse or mixed µ. This is an intensity-background canonical matching characterization, corresponding to the diagonal X=ξ specialization of the published 2011 projected formulation. It does not establish the intensity-erased/prescribed-X formulation or identify this family with the exact smaller class intended in Last's closing OWR paragraph.

These are affirmative transport characterizations under the source's nonzero, locally finite and Abelian assumptions. A zero measure, a bounded non-Markov weighted transport, or an unproved identification of the auxiliary state with ξ is not substituted.

## 2. Off-base-diagonal reversal lemma

This lemma avoids countable separation of Ω and avoids disintegration over ξ.

Let a(µ;s,t)≥0 be measurable, symmetric in s,t and covariant, with row integral r(µ,s)=∫a(µ;s,t)µ(dt)≤1. Let

    R_0(µ,t)=(θ_tµ,−t),       R(ω,t)=(θ_tω,−t).

For every Borel R_0-invariant indicator b on M×G, form

    a_b(µ;s,t)=a(µ;s,t)b(θ_sµ,t−s),
    K_b(µ,s,dt)=a_b(µ;s,t)µ(dt)+(1−r_b(µ,s))δ_s(dt).

Symmetry and Tonelli show K_b is invariant, Markov and µ-preserving, exactly as in Turn 1. Assume (I) for all these K_b. Define the σ-finite measure

    m(dω,dt)=Q(dω)a(ξ(ω);0,t)ξ(ω,dt),

whose first marginal is bounded by Q. Put

    J={(ω,t): θ_tξ(ω)=ξ(ω)}.

Then **m and R_*m agree on Jᶜ**.

### Proof

For any nonnegative f with Q(f)<∞, (I) permits subtraction of the finite holding contribution and gives

    ∫[f(θ_tω)−f(ω)] b(ξ(ω),t) m(dω,dt)=0.            (2.1)

Both nonnegative terms are finite: the outgoing term is bounded by Q(f), and the incoming term is bounded by the full K_b expectation Q(f). No global signed difference of two infinite measures is needed.

Fix a Borel set A⊂M and set

    F_A={(µ,t):µ∈A, θ_tµ∉A}.

For an arbitrary Borel B⊂G take F=F_A∩(M×B). The sets F and R_0F are disjoint. Hence b=1_F+1_(R_0F) is an allowed symmetric indicator. Let D∈F have Q(D)<∞ and use f(ω)=1_D(ω)1_A(ξ(ω)) in (2.1). On F the incoming f vanishes, and on R_0F the outgoing f vanishes. Therefore

    m((D×B)∩ρ⁻¹F_A)=R_*m((D×B)∩ρ⁻¹F_A),            (2.2)

where ρ(ω,t)=(ξ(ω),t). This uses only a measure-dependent gate; the arbitrary state information occurs solely in the permitted test function 1_D.

A countable partition of Ω into finite-Q sets makes both restricted measures in (2.2) σ-finite, since with B=G their masses on each partition piece agree and are finite. Uniqueness of measures on the product σ-field extends (2.2) from rectangles to all measurable subsets of ρ⁻¹F_A.

Choose a countable family (A_j) separating the points of M, closed under complements. If θ_tξ(ω)≠ξ(ω), some A_j contains the first measure and not the second. Thus Jᶜ=∪_jρ⁻¹F_(A_j). Equality on each piece, followed by a disjoint refinement, proves the lemma. Only M, not Ω, needs a countable separating family. ∎

## 3. Apply the lemma to positive local Markov transports

For each symmetric compact neighborhood C of zero put

    a_C(µ;s,t)=1_C(t−s)/[(1+µ(s+C))(1+µ(t+C))].

Its row integral is at most µ(s+C)/(1+µ(s+C))≤1. The associated gated lazy kernels are ξ-only and admissible. Section 2 shows m_C=R_*m_C on Jᶜ. The weight a_C(µ;0,t) is R_0-invariant and strictly positive when t∈C. Deweighting gives equality of

    c(dω,dt)=Q(dω)ξ(ω,dt)

and R_*c on Jᶜ∩(Ω×C). An increasing symmetric compact exhaustion of G gives equality on all Jᶜ. Deweighting is legitimate for σ-finite positive measures: integrate min(k,1/a_C) and pass monotonically to the limit. The Campbell measure is σ-finite, since sets

    {ω∈D_j:ξ(ω,C_n)≤k}×C_n

give a countable finite-mass cover, for a finite-Q partition (D_j) and a compact exhaustion (C_n).

The remaining set J cannot be discarded: the measure may be unchanged by a displacement while an auxiliary state changes. It is handled by additional ξ-only Markov kernels, rather than by identifying the two states.

## 4. Explicit transports along the period subgroup

For µ∈M let H_µ={t:θ_tµ=µ}. It is a closed subgroup: the translation action on Radon measures is continuous in the vague topology. H_(θ_sµ)=H_µ because G is Abelian. For a relatively compact Borel B⊂G put

    w_B(µ)=µ(H_µ∩B),
    κ_B(µ,dt)=1_(H_µ∩B)(t)µ(dt)/w_B(µ) if w_B(µ)>0,
                δ_0(dt)                              if w_B(µ)=0.

The graph {(µ,t):t∈H_µ} is Borel; parameter integration makes w_B and κ_B measurable. The denominator is finite by local finiteness. No measurable choice of Haar measures or orbit representatives is used in this definition. Set

    K_B(µ,s,A)=κ_B(θ_sµ,A−s).                         (4.1)

This is automatically a covariant, µ-measurable Markov kernel. We now prove that it preserves µ.

Fix µ and write H=H_µ. For every s, the restriction (θ_sµ)|_H is an invariant locally finite measure on H, hence either zero or c_sλ_H for some Haar measure λ_H and finite c_s≥0. This is a pointwise argument for the fixed µ, so an arbitrary normalization of λ_H suffices.

If λ_H(B∩H)=0, all w_B(θ_sµ) vanish and K_B is the identity. Otherwise λ_H(B∩H) is positive and finite. Let E={s:w_B(θ_sµ)>0}. On E, κ_B(θ_sµ) is the same probability ρ_B=λ_H(·∩B)/λ_H(B), independent of s; off E it is δ_0. The set E is H-invariant, since θ_(s+h)µ=θ_sµ for h∈H. Therefore µ|_E is H-invariant. Convolution with the H-supported probability ρ_B preserves µ|_E; the complement is fixed. This proves µK_B=µ. In particular (4.1) is among the kernels in (I).

## 5. Recover reversal on J, and finish Theorem A

The measure ξ is unchanged by every shift in the support of K_B(ξ,0,·), including the zero shift in the denominator-zero case. Thus w_B(ξ) is invariant under these shifts. Applying (I) to w_B(ξ)f for arbitrary nonnegative measurable f gives

    E_Q∫_(H_ξ∩B) f(θ_tω)ξ(dt)=E_Q[f(ω)w_B(ξ)].      (5.1)

There is no integrability requirement or subtraction here; both sides are nonnegative integrals, and w_B is finite pointwise. On a closed Abelian subgroup, Haar measure is invariant under inversion. Hence ξ(H_ξ∩(−B))=ξ(H_ξ∩B). Apply (5.1) with −B to obtain

    E_Q∫1_(H_ξ)(t)1_B(−t)f(θ_tω)ξ(dt)
      =E_Q∫1_(H_ξ)(t)1_B(t)f(ω)ξ(dt).                (5.2)

This is c|_J=R_*(c|_J), first on product tests and then on the full product σ-field. For the uniqueness step, use the same finite-mass product cover as in Section 3; (5.2) ensures the reversed measure is finite on that cover as well.

Combining with the off-J identity proves c=R_*c, or

    E_Q∫g(θ_tω,−t)ξ(dt)=E_Q∫g(ω,t)ξ(dt)

for every nonnegative measurable g. The established Mecke characterization, Last–Thorisson (2009), equation (2.7), gives a stationary σ-finite measure P with Q=P_ξ. Theorem 6.3 of that paper identifies this with mass-stationarity. Its Theorem 4.1 supplies the converse implication. This proves Theorem A without a standard-Borel hypothesis on Ω or a σ-finite marginal law of ξ. In particular it closes precisely the abstract-state issue that Turn 1 left open.

## 6. An actual Cox-derived matching family

This construction proves the canonical intensity-background Theorem B directly. It does not settle the full strict count-only deterministic Cox allocation question.

By Struble's theorem, G admits a compatible proper translation-invariant metric d. Write B̄(s,r) for its closed balls; these are compact. For s≠t define

    U(s,t)=B̄(s,d(s,t)) ∪ B̄(t,d(s,t)).

Let η be a locally finite integer-valued counting measure, allowing multiple points, and let µ be a nonzero locally finite Radon measure retained as background. First pair s and t only if

    s≠t,   η{s}=η{t}=1,   η(U(s,t))=2.               (6.1)

Each point has at most one partner. Indeed if s had two distinct partners, the nearer one would lie in the closed ball used for the farther pair, giving at least three points there. Equal-distance ties also give at least three and are rejected. Condition (6.1) is symmetric, so it defines disjoint transpositions; leave all other locations fixed.

For any Borel R_0-invariant indicator b(µ,t), retain a pair (s,t) only when b(θ_sµ,t−s)=1. That condition is symmetric in the endpoints. Denote the resulting matching by τ_b(µ,η,s). It is an involution and preserves the entire counting measure η: only singleton atoms of equal unit mass are transposed, and all multiple atoms are fixed. It is translation-covariant. Its measurability follows from the explicit test (6.1) and integration against the locally finite counting kernel: the potential partner is unique, and its point-mass kernel is given by the measurable sum over t of the pairing indicator. Thus no nonmeasurable selection or global ordering of the group is required.

Given µ, let ζ be a Poisson random measure of intensity µ. For each starting point s add one point δ_s, and average the allocation:

    K_b^Cox(µ,s,A)=E_µ[1_A(τ_b(µ,ζ+δ_s,s))].         (6.2)

This is a Cox-derived transport obtained by applying an invariant matching with original µ retained as background. Published 2011 Remark 4.8 permits inside T to observe prescribed auxiliary w and the rooted counting measure; choosing X=ξ admits these µ gates. Choosing constant X removes that intensity observation and gives a smaller class, for which this argument supplies no sufficiency theorem. No independent labels, marks, grids or extra stationary background are introduced.

### Exact density, including atoms

The Poisson Campbell–Mecke formula applied to a possible distinct partner t yields

    K_b^Cox(µ,s,dt)
      =1_{t≠s} b(θ_sµ,t−s) exp[−µ(U(s,t))] µ(dt)
         +(1−r_b(µ,s))δ_s(dt),                       (6.3)

where r_b is the integral of the off-diagonal term. To check the formula, after inserting δ_s and the candidate δ_t, (6.1) holds exactly when the original ζ has no point in U(s,t). This void probability is exp[−µ(U(s,t))]. The compactness of U makes it finite and strictly positive for every distinct s,t.

This argument works when µ has atoms. In that case the void event includes the requirements that there were no original Cox points at s or t. Omitting these atom factors would be an error. Multiple Cox points at either endpoint preclude the transposition, precisely as encoded by the void event. A candidate t=s is excluded and belongs to the holding mass; it is not double-counted as a partner.

The Poisson Campbell–Mecke identity used here is the ordinary intensity-µ identity, valid also for atomic µ. It can be obtained for finite µ by expanding the Poisson series and choosing one of its points, and for σ-finite locally finite µ by monotone exhaustion. Thus its use does not presuppose mass-stationarity of Q or any Palm characterization being proved.

Since (6.2) is a probability kernel, r_b≤1. The off-diagonal density is symmetric in s,t and covariant. Consequently (6.3) preserves µ by Tonelli and cancellation with its holding term. The averaged Cox construction is a genuine preserving **Markov** transport, not only a weighted transport.

## 7. Cox matching tests imply canonical mass-stationarity

Assume now Ω=M\{0}, ξ(µ)=µ, and Q is σ-finite. Suppose its distribution is invariant under all kernels (6.2) in the displayed family.

Apply the off-base-diagonal lemma of Section 2 with

    a(µ;s,t)=1_{s≠t}exp[−µ(U(s,t))].

Every gate required in that proof is one of the indicator gates in Section 6. The row bound follows from the matching construction with b=1. Hence m=R_*m off the set J={(µ,t):θ_tµ=µ}.

On J, R fixes µ and reverses t. The restriction µ|_(H_µ) is either zero or a multiple of Haar measure on H_µ. Further, a(µ;0,t)=a(θ_tµ;0,−t)=a(µ;0,−t) for t∈H_µ. Thus the conditional weighted measure on H_µ is invariant under t↦−t. Integration with respect to Q proves m|_J=R_*(m|_J). This remains a pointwise Haar argument and uses no measurable Haar normalization.

Therefore m=R_*m everywhere. Its weight a(µ;0,t) is strictly positive for t≠0, so deweighting gives the full canonical Campbell reversal identity away from t=0. At t=0, R is the identity, so the missing diagonal equality is automatic even if µ has an atom at zero. This proves the full Mecke identity and mass-stationarity. Necessity follows from transport invariance because every kernel (6.2) was proved preserving and Markov. Theorem B follows.

## 8. Exact source scope, attribution and remaining gap

Theorem A proves formal Last–Thorisson (2009) Problem 7.3 under its σ-finite arbitrary-flow setting and answers the literal imported all-Markov question. Thorisson also poses the general Markov converse in OWR47/2008, printed pp.2692/2694. The import contains no Cox/allocation restriction. This is a transparent formalization of the literal target, without asserting resolution of every question in the cited whole report.

Theorem B separately proves a σ-finite canonical measure-law criterion using genuine singleton matchings that inspect µ as background. Last's closing OWR paragraph, printed p.2673, discusses allocation-derived Cox transports and does not explicitly identify their allowed intensity observation. The final published 2011 paper, Remark 4.8 on printed p.263, writes T′(w,α,s,·)=∫T(w,ν+δ_s,s,·)Π_α(dν). Inside T observes prescribed w and rooted counting ν, not α separately. B matches the diagonal X=ξ specialization; replacing constant X by ξ enlarges the observations and is not a reduction proving the smaller premise.

The complete final 2011 paper was subsequently acquired and checked by the source-scope family at SHA256 67ba5a5c0943ac3cfaecdadcfadaf8ffd0e9cc0fe52f114b507218710a6a5744 (203,382 bytes). Original failed access is historical evidence, not a present unread limitation. The complete operative OWR contributions and formal Annals source were checked. The verified later construction edition is arXiv:1405.7566v2, revised 17 July 2015; its Section 9 retains a historical Markov gap and distinguishes weighted kernels. The complete final SPA 2015 publisher body was not authenticated, and neither that historical statement nor a bounded search certifies 2026 openness or novelty.

TURN_3 records already verified, distinct count-only extensions: C for canonical probability laws with preserving Markov tests, and D for countable discrete Abelian groups with σ-finite canonical laws and allocation tests. Neither supplies the full non-discrete deterministic allocation converse, arbitrary-X strict Cox theorem, or general σ-finite strict Cox Markov extension. The Markov family cannot be silently identified with allocation mixtures in the presence of unequal multiplicities.

Classical Mecke/Palm characterization and transport invariance are credited Last–Thorisson inputs. Struble's metric theorem, pointwise Haar uniqueness and ordinary Poisson Campbell–Mecke are used with their displayed assumptions. Nonzeroness, local finiteness, σ-finiteness and lcsc Hausdorff Abelian G are retained. No non-Abelian, non-locally-finite, finite-intensity-only or standard-Borel-Ω substitution is made. Bounded priority for the precise formal A claim is accepted by ROOT with the six disclosed edition/audiovisual/coverage gaps; this is not worldwide priority certification. Human refereeing, machine formal verification and publication clearance remain absent. The integrated main preprint contains A only; B/C/D remain ancillary attempt results.

### Appendix: Poisson identity used in (6.3)

For a finite measure µ with mass m, the Poisson law is the mixture of n independent points with weights e^(−m)/n!, interpreted as integration against µ^n. Therefore, for nonnegative measurable F,

    E∫F(ζ,t)ζ(dt)
      = e^(−m)Σ_(n≥1) (1/n!)∫Σ_(i=1)^n F(Σ_jδ_(x_j),x_i) µ^n(d(x_1,…,x_n))
      = ∫µ(dt) e^(−m)Σ_(k≥0) (1/k!)∫F(δ_t+Σ_jδ_(x_j),t) µ^k(d(x_1,…,x_k))
      = ∫E[F(ζ+δ_t,t)]µ(dt).

Coincident points are allowed in these product integrals, so the derivation includes atoms. For the partner formula with fixed s and t restricted to B̄(s,R), the void event depends only on ζ in B̄(s,2R), where µ is finite. Apply the finite identity there and then let R increase. Tonelli and monotone convergence justify the passage to arbitrary locally finite µ. This establishes exactly the Campbell–Mecke use made in (6.3), without an assumption on the law Q of µ.
