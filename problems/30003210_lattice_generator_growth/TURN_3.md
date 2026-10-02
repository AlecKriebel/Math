# Turn 3: a non-effective growing-cover window

AI-assisted proof attempt; independent review pending. Original unresolved.

Fix G as in the gate. Write v(H)=vol(G/H) with the fixed Haar normalization. For t sufficiently large define
R(t)=sup{(d(H)−1)/v(H): H torsion-free lattice, v(H)≥t},
with supremum0 for an empty class. Gelander's linear rank bound makes R finite, and the prior FMW theorem implies R(t)→0: otherwise choose a violating H at each increasing t, contradicting its sequential assertion. This is uniformization of an existing theorem; it supplies no effective rate.

Put h(t)=min(sqrt(t),R(t)^(-1/2)), interpreting the second term as infinity if R(t)=0. Then h(t)→infinity. Suppose Γ_i has volume v_i→infinity and a torsion-free subgroup H_i of index m_i≤h(v_i). Normality is unnecessary. Starting with H_i, repeatedly adjoin an element outside the generated subgroup until reaching Γ_i. Every enlargement at least doubles the index over H_i, so at most floor(log_2 m_i) elements suffice. Thus
(d(Γ_i)−1)/v_i ≤ m_i R(v_i)+floor(log_2 m_i)/v_i
≤ sqrt(R(v_i)) + (log_2 v_i)/(2v_i) →0.
The zero-R case follows directly from the first inequality.

Consequently the bounded-degree family in turn2 extends non-effectively to unbounded field degrees D_i with 3^(N² D_i)≤h(v_i). There is some diverging allowable degree window, but no explicit logarithmic or polylogarithmic degree window follows from this proof. No uniform computation of h is claimed.

## Exact conditional rate thresholds
More generally retain the actual cover volume w=mv and the inequality
(d(Γ)−1)/v ≤ m R(mv)+log_2(m)/v.
If the torsion-free ratio is at most C w^(−α), 0<α≤1, and m≤v^a, then the first term is ≤C v^(a(1−α)−α). This tends to0 precisely under the sufficient strict condition α>a/(a+1). At equality, the power estimate alone is O(1); a further little-o or logarithmic improvement is needed. This is an exact qualification of this calculation, not a blanket criticism of any source theorem.
If m≤C_0(log v)^a and R(w)≤C(log w)^(−b), then the first term tends to0 for b>a. Equality b=a again does not suffice on this information alone. These are conditional transfer statements, not newly established rates. Gelander–Slutsky §5 already introduces the transfer strategy and is credited.

## Why qualitative sublinearity plus polylog covers is insufficient
Take the scalar profile R(t)=1/loglog(t+e^e) and m(v)=ceil(log v). Then R→0 but m(v)R(m(v)v) diverges. This is a counterexample only to the numerical inference from the two upper bounds; it does not construct a lattice with large rank. Similarly R(t)=t^(−a/(a+1)) and m(v)=v^a give a constant product at the critical exponent. No finite test or scalar model is evidence against the original conjecture.
