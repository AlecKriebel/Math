# PR316: current classical priority obstruction (provisional)

Original intake: PR316, submitted head `c96a3b2019ed3d6aabe0612b31491161dcb275e8`, submitted status `claimed_solved`, author 1/5. This is a research audit record, not a preprint or a claim of historical firstness. Root's mathematical acceptance of the submitted lacunary construction remains valid. Priority and publication acceptance remain false.

## Claim and boundary cases

For iid positive finite-a.s. renewal increments, zero initial delay, let `S_0=0`, `N(t)=max{k:S_k<=t}`, `D_t=S_{N(t)+1}-S_{N(t)}`, and `U(t)=sum_{k>=0}P(S_k<=t)`. With any slowly varying tail `r(t)=P(X>t)` tending to zero, the classical renewal asymptotic `U(t)r(t)->1` yields the following exact consequence: every proper finite weak limit of `D_t/phi(t)`, for an arbitrary eventually finite positive deterministic scale, is the point mass at zero. In particular no increasing positive scale gives a proper nondegenerate limit. This is stronger than failure of the scale t and includes mixed distributions with an atom at zero and oscillating scales.

## Root derivation, subject to fresh adversarial adjudication

For `x>=t`, the event `{D_t>x}` is the disjoint union over `k>=0` of `{S_k<=t, X_{k+1}>x}`. Each such jump passes strictly beyond t, even when its start equals t, and therefore is the unique straddling interval under the stated strict-next-renewal convention. Independence and Tonelli give the exact identity `P(D_t>x)=U(t)r(x)`. The expectation U is finite on bounded intervals for positive finite-a.s. iid increments; the explicit law below even has X>=1.

For any fixed M>=1, slow variation and the classical asymptotic give `P(D_t>Mt)->1`; thus `D_t/t->infinity` in probability. Suppose `D_t/phi(t)=>Y` is proper finite. If `phi(t)/t` does not tend to infinity, some t_n->infinity and finite C satisfy `phi(t_n)<=Ct_n`. Along this sequence `D_t/phi(t)>=D_t/(Ct)->infinity` in probability, contradicting tightness. Hence `phi(t)/t->infinity`, and eventually `a phi(t)>t` for every fixed a>0. For any positive a,b,

`P(D_t>a phi(t)) / P(D_t>b phi(t)) = r(a phi(t))/r(b phi(t)) -> 1`.

The denominator probability is at most one, so the difference of these two survival probabilities tends to zero. At positive continuity points of Y their limits agree. Properness implies survival probabilities along arbitrarily large such points tend to zero; consequently all positive continuity-point survival probabilities vanish. Since Y is nonnegative, `Y=0` almost surely. No moment assumption on Y or monotonicity of phi was used.

## Elementary explicit law, independently checkable without a Tauberian theorem

Take X with continuous survival `r(t)=1` for 0<=t<=1 and `r(t)=1/(1+log t)` for t>=1, with density `1/[x(1+log x)^2]` on x>1. This is a probability distribution, strictly positive, finite almost surely, non-lattice and of infinite mean. For t>=1 its truncated expectation M(t) satisfies

`M(t)=integral_1^t dx/(1+log x)^2 <= sqrt(t)+t/(1+(log t)/2)^2`.

Therefore `M(t)/(t r(t))->0`. Let K be the first increment strictly exceeding t and T its renewal start. Independence and Tonelli give `E T=M(t)/r(t)` (the law is continuous, so <= versus < in M is immaterial). Markov's inequality implies `P(T>t)->0`. On T<=t, that jump is the straddling interval and exceeds t. Thus `P(D_t>t)->1`, which, with the exact identity at x=t, establishes `U(t)r(t)->1` for this explicit law. The all-scale argument above applies for all real t tending to infinity. This elementary route verifies the negative answer, but by itself establishes no earlier publication of that answer.

## Authenticated classical premise and read scope

Erickson, *Strong renewal theorems with infinite mean*, Transactions of the AMS 151 (September 1970), pp263–291, DOI https://doi.org/10.1090/S0002-9947-1970-0268976-9. Root read extracted text of printed pp263–266, then visually read the complete rendered pp265–266. Theorem5 on p265 explicitly covers 0<=alpha<=1 and gives `U(t) ~ t / [Gamma(alpha+1)Gamma(2-alpha)m(t)]`. Equation2.2 on p266 gives the equivalent expression for alpha!=1 and explicitly assigns the alpha=0 constant its value1. Together with the definition `1-F(t)=t^{-alpha}L(t)` and `m(t)=integral_0^t(1-F)` on pp263–264, alpha=0 yields precisely `U(t)r(t)->1`. The assumptions allow the continuous explicit law above.

The primary article was obtained by the priority reviewer from a public mirror after the official AMS endpoint returned403. Root independently read the article binary's relevant content; it is original article content with AMS publication identifiers, but mirror provenance remains disclosed. Private PDF and scans are retained as evidence and excluded from this public checkpoint. Root has not read the entire 29-page article and does not claim a historical author explicitly stated the all-scale conclusion in it.

Earlier primary sources read by root: complete three-page Bingham–Goldie–Teugels ratio preprint; Lamperti's 1961 Stanford technical-report scan, all19 pages as OCR aid and decisive scan pp4/9 visually; semistable and random-inspection papers' main hypotheses and theorem statements only. These conditional ratio, regular-variation or inspection theorems must not be substituted for the exact arbitrary-scale conclusion. Original Thorisson Problem1.2/hypotheses were checked in indexed institutional primary text; full original PDF binary/visual access remains unavailable after recorded failures. No full published/preprint comparison is claimed.

## Status, novelty and remaining gap

The full general negative answer is a short checkable corollary of a primary theorem published in 1970. This is a substantial priority concern for marketing the existential negative answer as a new discovery. No primary source has yet been authenticated as explicitly announcing an answer to Thorisson's later Problem1.2, and exact priority of the particular irregular lacunary construction remains unestablished. An old premise, a newly articulated consequence, and a prior explicit answer are distinct evidence categories. A fresh adversarial reviewer is independently testing the consequence and its historical implications before root adjudication. No paper, merge, Zenodo upload or tracker append is currently approved for PR316.

Checkpoint estimate: submitted mathematics100%; current PR workflow35%; priority obstruction adjudication pending. No outside individual contacted. Persistent goal remains active and its current intake filter accepts only submitted `claimed_solved` PRs.
