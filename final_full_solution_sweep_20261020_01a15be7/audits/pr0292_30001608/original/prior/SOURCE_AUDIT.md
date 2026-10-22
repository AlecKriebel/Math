# 30001608: exact source gate

The target is Norros (joint with Reittu), “On the stability of population processes,” OWR48/2010, printed2782–2783, DOI10.4171/OWR/2010/48. The full contribution and question page were read. The imported title says “fluid limits,” but the source uses a **large-system limit scaling the arrival rate as well as the state**, not the fixed-arrival/time-accelerated fluid scaling. These must not be interchanged.

## Correct edition and exact generator

The complete January5,2011 author proof of Norros–Reittu–Eirola, *On the stability of two-chunk file-sharing systems*, is publicly deposited as [HAL00781341](https://hal.science/hal-00781341/document). The publisher metadata gives Queueing Systems67 (2011),183–206, DOI10.1007/s11134-011-9209-2, onlineJanuary26,2011. The accessible PDF is an author proof with its own pages1–24, preceded by a HAL cover; it is not described as a downloaded final Springer PDF. Direct Springer PDF access returned subscription HTML. Model and conjecture occur in Section3.2, proof pages10–12, Figure2 and Conjecture3.6.

State (A,B,X,Y) belongs to Z_+^4. A and B count empty peers committed to acquire chunk0 or1 first, respectively; X and Y hold just the respective chunk. There is one permanent seed with both chunks. Arrival processes into A and B each have rate lambda/2, with fixed lambda>0. Put D=X+Y+1. The six actual state transitions and rates are:

- (A,B,X,Y) -> (A+1,B,X,Y), lambda/2
- -> (A,B+1,X,Y), lambda/2
- -> (A-1,B,X+1,Y), A(X+1)/D
- -> (A,B-1,X,Y+1), B(Y+1)/D
- -> (A,B,X-1,Y), X(Y+1)/D
- -> (A,B,X,Y-1), Y(X+1)/D

Figure2 and the paragraph immediately above it explicitly explain why the denominator excludes A and B: empty waiting-room peers are invisible in the overlay until they acquire a first chunk. This resolves the abbreviated OWR description; replacing D by total population plus one would be a different model. Seed contributions are the +1 factors, including when a chunk is absent. Complete peers leave immediately. “Stable” means irreducible positive recurrence, equivalently a unique stationary probability law, as stated in Section2/proofp5. The conjecture concerns every fixed positive arrival rate; lambda=0 has an absorbing empty state and falls outside that irreducibility convention.

The large-system family changes lambda to N lambda and divides states by N at fixed time. Equation9 is a'=lambda/2-ax/(x+y), b'=lambda/2-by/(x+y), x'=(a-y)x/(x+y), y'=(b-x)y/(x+y). Proposition3.5 establishes an unbounded equilibrium curve and an open set of diverging trajectories. This is a credited known result, not a fresh proof claim. The final Conjecture3.6 asserts stochastic stability and discusses irregular majority-switching simulations. Its simulation footnote uses constant inter-event times; that observation is evidence only, not a recurrence proof or a justification for discarding state-dependent holding times.

## Historical/current distinctions

The sole arXiv version0910.5577v1 (October29,2009) has the same displayed six rates but gives the opposite Conjecture3.4, predicting instability at large lambda. Its conjecture is explicitly superseded by the2011 author proof, which matches the2010 OWR stability conjecture. Neither is a stochastic proof. The later Oguz–Anantharam–Norros2011 paper1107.3166 proves stability of a different, modified majority/common-chunk protocol and discusses Enforced Friedman. It does not resolve this target in the inspected model/protocol sections. Searches for the exact algorithm name, Conjecture3.6, DOI, and later stability literature located no exact resolution. This bounded search is not an exhaustive novelty certificate.

## Prior campaign gate

At October1,2026 before author turn1: all-state repository PR search for30001608/OWR-4530-006/unstable fluid found none; branch search30001608 found none; both candidate attempt paths had no commit history; local all-ref and related-target-group checks found none. The pinned upstream research report is empty. QUEUE rank309 was queued0/5. Source retrieval and edition reconciliation consume zero substantive proof turns.

All full source PDFs, extracts, renders and imported records remain local reading material. Public artifacts contain source URLs/hashes and independently written mathematics only.
