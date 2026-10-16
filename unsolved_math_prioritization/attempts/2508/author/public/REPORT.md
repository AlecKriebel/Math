# Prior solution audit for robust polynomial interpolation

## Verdict and attribution

**The exact target has a complete prior proof, verified here relative to the established Bernstein interpolation density theorem and the standard analytic compactness facts listed below. No unresolved mathematical gap was found in the April 29, 2026 candidate. Zero new solution approaches were undertaken.**

The proof being audited is the draft *A Bernstein-density proof of Erdős’s robust interpolation obstruction*, dated April 29, 2026, publicly linked by Przemek Chojecki with GPT-5.5 Pro assistance. The PDF itself has no named author on its title page. This report attributes the argument through that public posting; it makes no new-discovery or priority claim. Its independently written verification is not a claim of journal acceptance, human expert certification, or proof-assistant formalization. The last available AI-contributions wiki snapshot still calls the work a candidate and says its updates ended June 30, 2026. That status label was not used as mathematical evidence.

## Exact target and source gate

For each positive real number C, the assertion requires constants ε>0 and n₀ depending only on C. Given any integer n≥n₀ and any indexed list of n nodes from [-1,1], labels from [-1,1] must be chosen so that every polynomial of degree below (1+ε)n and norm at most C agrees with strictly fewer than (1−ε)n labels. Agreement is counted by index, including repeated nodes. This is the contrapositive of the requested strict norm conclusion.

The original question on printed page 72 of Erdős’s survey has the same degree slack, fraction of matches, and order of quantifiers, with distinct ordered nodes. The database formulation permits repetitions; the candidate handles that stronger interpretation. The scan's first page is dated 1968, while the archive filename and some bibliographic records use 1967. This date discrepancy changes no mathematical assumption.

The selected database record is 2508 / EP-1133, rank 1037. The research-results corpus contains no EP-1133 entry. The provided bounded prior-work screen found only literature triage in the campaign and explicitly identified the April candidate for inspection. No substantive inherited campaign proof was found. The candidate author's separate public repository contains earlier finite interpolation experiments, but those are external work and do not supply the proof. In particular, fitting a subset does not force a polynomial of larger permitted degree to equal its minimal-degree Lagrange interpolant.

## Imported results and their exact roles

1. **Bernstein interpolation density, necessity only.** Let Bτ be the entire functions of exponential type at most τ bounded on the real line. If a separated real set Λ allows interpolation of every bounded complex sequence by an element of Bτ, then its upper uniform counting density is strictly less than τ/π. This is the real-line specialization of Ortega-Cerdà and Seip, Theorem 1. The theorem and its definitions were inspected in the original accepted manuscript, pages 1–2, including the strict inequality; the necessity argument is on pages 3–5. The theorem is imported, not reproved or formally certified here.

   The specialization is exact: their separation distance becomes |s−t|/(1+|s−t|), equivalent to an ordinary positive minimum gap; their Carleson sum vanishes for real points; their strip density reduces to the ordinary interval density. Open versus closed interval endpoints change counts by at most two and leave the limiting density unchanged. The bandwidth convention is exponential type τ, so the critical density is τ/π, with no missing factor of two.

2. **Growth bound.** For f∈Bτ, |f(x+iy)|≤‖f‖∞ exp(τ|y|). This Phragmén–Lindelöf consequence appears on page 1 of the same primary source. It yields compactness of norm-bounded families by Montel and preservation of exponential type in their limits.

3. **Standard compactness and measure theory.** Montel's theorem; vague compactness of uniformly separated counting measures; weak compactness of probability measures on a compact metrizable space; the Portmanteau theorem; Fubini's theorem; and uniqueness of a locally finite translation-invariant measure on the line. These standard facts are imported explicitly. Their hypotheses and applications are checked below.

4. **Standard ergodic theory in the candidate's presentation.** Ergodic decomposition of an invariant probability measure for a continuous real action on a compact metrizable space, and the continuous-parameter Birkhoff theorem for a bounded observable. The candidate uses these to extract a positive-density configuration. The verification below supplies a reverse-Fatou alternative, so the audit's deduction does not need either ergodic theorem.

5. **Derivative bound.** The candidate uses the classical Bernstein inequality ‖f′‖∞≤τ‖f‖∞. Only a uniform positive separation is needed. The verification below obtains a weaker sufficient bound from Cauchy's formula and item 2, avoiding a separate derivative-theorem import.

The statement that the manuscript uses one external theorem should therefore be read as one specialized interpolation theorem. It also uses ordinary analysis and ergodic theory. These are neither hidden hypotheses nor computationally established facts.

## Verification of the local obstruction

Fix C≥1. We show that some positive η and integer L have the following property: every indexed L-tuple with diameter at most π(1+η)L admits real unit-bounded data that cannot all be fitted by a function in B₁ of norm at most C. For C<1, one node labeled 1 already suffices.

Suppose no such η,L exist. Set Lk=k+2 and ηk=1/k. For each k choose a corresponding universally C-interpolable Lk-tuple. It cannot repeat a point: the two labels +1 and −1 would be incompatible. Translate its distinct points to a set Uk contained in [0,Tk], with both endpoints included and Tk≤π(1+1/k)Lk.

The growth estimate and Cauchy's formula on a radius-one circle about a real point give |f′(x)|≤eC. Assigning +1 and −1 at any two nodes and integrating f′ along the intervening real interval gives a distance at least δ=2/(eC). Thus all Uk are uniformly δ-separated and Tk≥δ(Lk−1)→∞. The candidate's stronger δ=2/C follows from its Bernstein inequality and is also valid; sharpness is irrelevant.

Let Xδ be the space of δ-separated closed subsets of the line, including the empty set, represented by counting measures with vague convergence. A compact interval of length r contains at most 1+r/δ points. Diagonal compactness on an exhausting family of compact intervals therefore gives a vaguely convergent subsequence; limits still have unit atoms separated by δ, with atoms allowed to escape to infinity. Xδ is compact and metrizable. Translation TtΛ=Λ−t is continuous. For every continuous compactly supported φ, the observable Nφ(Λ)=Σλ∈Λ φ(λ) is continuous and bounded.

Average translates of Uk over t∈[0,Tk] to obtain probability measures νk on Xδ. Extract a weak limit ν. Shifting the averaging interval by a fixed s changes any bounded-observable integral by at most 2|s|‖F‖∞/Tk. Hence ν is translation invariant. Its first-moment measure is a locally finite translation-invariant measure and therefore equals I times Lebesgue measure for some I≥0.

For φ≥0 supported in [-R,R], Fubini gives

    ∫ Nφ dνk = (1/Tk) Σu∈Uk ∫₀^Tk φ(u−t) dt.

Every node in [R,Tk−R] contributes ∫φ. The total number of nodes in the two end intervals is at most 2(1+R/δ), independently of k. It follows that

    I ∫φ = lim ∫ Nφ dνk ≥ liminf (Lk/Tk) ∫φ ≥ (1/π)∫φ.

Taking a nonzero φ proves I≥1/π. Boundary truncation has not lost macroscopic mass, precisely because uniform separation bounded the endpoint contribution.

Next fix Λ in the support of ν, a finite subset {λ₁,…,λr} of Λ, and real data b₁,…,br in [-1,1]. Portmanteau and a shrinking countable neighborhood basis provide indices kj→∞ and translates Ukj−tj converging vaguely to Λ. Separation supplies distinct points wj,i in those translates with wj,i→λi. Assign bi to the corresponding original nodes, extend the labels arbitrarily to the remaining nodes, and take norm-C interpolants hj. The functions fj(z)=hj(z+tj) have the same norm and type, and satisfy fj(wj,i)=bi.

The strip bound supplies local uniform boundedness in the complex plane. A Montel subsequence converges locally uniformly to f, with |f(x+iy)|≤C exp(|y|), hence f∈B₁ and ‖f‖∞≤C. Local uniform convergence together with wj,i→λi gives f(λi)=bi. This proves the finite interpolation property for every configuration in supp ν, not merely almost every configuration and not for one predetermined label pattern.

Every separated configuration is countable. For any fixed bounded real label sequence on an infinite Λ, interpolate its first r entries and take another Montel subsequence as r→∞. Each fixed entry is eventually imposed, so the limit interpolates every entry with norm at most C after normalization. For complex labels aλ, interpolate their real and imaginary parts separately and add the results as f+ig; the norm is at most 2C‖a‖∞. The component interpolants themselves need not be real-valued. This construction proves exactly the complex-data interpolation hypothesis needed by the density theorem.

Here is a direct check of the last density contradiction which does not require choosing an ergodic component. For every Λ in supp ν, put

    H(Λ) = limsup over positive integers r of #(Λ∩[0,r))/r.

For finite Λ this is zero. For infinite Λ, the imported strict density theorem gives H(Λ)≤D⁺(Λ)<1/π. The counting functions are measurable, uniformly bounded by 1+1/δ for r≥1, and their ν-expectations are exactly I, by stationarity of the first-moment measure. Applying Fatou to a common upper bound minus these functions gives

    I ≤ ∫ H dν < 1/π.

The last inequality is strict: 1/π−H is positive almost surely, and a positive measurable function on a probability space has positive integral. This contradicts I≥1/π. Thus the required η,L exist. This is an alternative verification of one standard-measure-theory step within the candidate's argument, not a new solution strategy.

The candidate's original ergodic step is valid as well. An ergodic component of intensity at least 1/π exists because the component intensities average to I. Birkhoff applied to the bounded count in [0,1) gives asymptotic one-sided density equal to that intensity, with a uniformly bounded endpoint error. Such a configuration is infinite and lies in supp ν almost surely, giving the same contradiction.

## Verification of the global robust conclusion

Choose η,L from the local obstruction and write q=(1+η)L. Fix

    0 < ε < min(1/2, η/[2(1+q)]).

Then a=(η−ε)/q−ε is positive. A sufficient explicit threshold once η,L are known is any integer n₀>(1+1/q)/a. This does not give a numerical n₀(C), since the local constants were obtained qualitatively.

For n≥n₀ let D=ceil((1+ε)n). Sort the angular representatives θi=arccos(xi) in [0,π] and divide the indexed list into floor(n/L) disjoint consecutive full blocks of L nodes. At most L−1 indices remain. If hb is a block's angular span, the spans have disjoint interiors and sum to at most π, including zero spans from repeated nodes.

A block is good when D hb≤πq. If B blocks are bad, then B<D/q. Consequently the number G of good blocks satisfies

    G ≥ floor(n/L) − D/q
      ≥ n(η−ε)/q − 1 − 1/q
      > εn.

The strictness follows from the chosen n₀; neither floor nor ceiling has been suppressed. The bound for B is also valid when B=0 since D/q>0.

Inside each good block starting at angle α, scale the nodes to u=D(θ−α). Their diameter is at most πq. Give them the forbidden labels furnished by the local obstruction. Put label zero on the other indices and restore the original index order. All labels depend on C,n and the nodes, never on the polynomial subsequently tested.

Suppose a polynomial P has degree m<(1+ε)n and norm at most C on [-1,1]. Then Q(z)=P(cos z) is an entire trigonometric polynomial of degree at most m, of exponential type at most m, and its real-line supremum equals the interval norm of P. For any block start α,

    F(u)=Q(α+u/D)

has type at most m/D<1 and real-line norm at most C. Thus F∈B₁. Fitting every label in a good block would contradict its forbidden local data. P therefore misses at least one index in each of the G disjoint good blocks, so it misses more than εn indices. This excludes agreement at (1−ε)n or more indices and proves the exact target, including repeated nodes, interval endpoints and complex coefficients.

## What has and has not been established

- Source claim: the April draft claims the complete target. Its existence, date, scope and mathematical dependencies were inspected.
- Checked deduction: the proof above verifies every reduction from the stated imported density theorem and standard analysis. No gap remains in that deduction.
- Imported theorem: the general Bernstein interpolation theorem is accepted here as published mathematics. Its real-line hypothesis matching was checked directly; its full original proof was not reconstructed or formalized.
- Finite evidence: the accompanying standard-library program checks exact block arithmetic, floor/ceiling margins, adversarial finite angular patterns, data-source identities, and artifact integrity. Those checks do not prove an infinite-dimensional compactness theorem and are not presented as a theorem certificate.
- No numerical formula for η(C), L(C), ε(C) or n₀(C) is claimed. Only the last-stage threshold in terms of already-existing η,L is explicit.
- No peer-review acceptance, community consensus, or Lean verification of the April manuscript was established. The appropriate result is a verified prior-solution audit relative to declared imports, with zero new approaches, not a new resolution announcement.

## Public references

1. Candidate draft, *A Bernstein-density proof of Erdős’s robust interpolation obstruction*, April 29, 2026: https://www.ulam.ai/research/erdos1133.pdf
2. Public attribution and discussion: https://www.erdosproblems.com/forum/thread/1133
3. J. Ortega-Cerdà and K. Seip, *Multipliers for entire functions and an interpolation problem of Beurling*, Journal of Functional Analysis 162 (1999), 400–415; DOI https://doi.org/10.1006/jfan.1998.3357 ; accepted manuscript https://diposit.ub.edu/bitstreams/bbe5243b-6094-4096-b939-b6692a19f366/download
4. P. Erdős, *Problems and results on the convergence and divergence properties of the Lagrange interpolation polynomials and some extremal problems*, Mathematica (Cluj) 10 (33), 65–73, printed 1968; original question on page 72: https://users.renyi.hu/~p_erdos/1967-20.pdf
5. Problem tracker: https://www.erdosproblems.com/1133
6. Dated AI-contributions index: https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems
7. Candidate author's separate earlier experiments and public-note link: https://github.com/przchojecki/agentic-erdos/blob/main/notes/ep1133.md

The deliverable contains authored analysis and verification metadata only. It includes no copied source PDFs, source-text extracts, dataset contents, or private coordination material.
