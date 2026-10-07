# Current theorem target and verified scope

Status: hypotheses under audit, not an unconditional resolution.

For H={0,...,h−1}, h≥2, let Σ_h be all binary relations on H, compose in path order, and let L_h={R_1...R_k: R_1...R_k≠∅}, with empty product I_H. Let E_h concatenate the row-major h²-bit adjacency matrices. Define B_h=E_h(L_h) as a language over {0,1}*: every word whose length is not divisible by h² is excluded, including all proper partial blocks; ε is included.

Core target 1: construct a polynomial-in-h one-way NFA for B_h and prove every equivalent s-state two-way DFA has s≥2^{Ω(h)}/poly(h), hence 2^{n^{Ω(1)}} in the source-state parameter n. Preserve quantitative source expansion; do not claim 2^{Ω(n)}.

Core target 2: construct a polynomial-in-h binary two-way NFA (one-way suffices if proven) for B_h and prove every s-state two-way NFA recognizing {0,1}*\B_h has s≥2^{Ω(h)}/poly(h). Complement universe is all binary words. Pullback only uses valid E_h(w), and E_h^{-1}({0,1}*\B_h)=Σ_h*\L_h must be proved.

Conventions: one initial state, distinct endmarkers, initial head on left marker; left/right/stay moves, partial transitions, disabled outward boundary moves, acceptance by a finite run reaching an accepting state (including zero steps). All states counted. Infinite nonaccepting runs reject. Ordinary 1NFA right-only formulation and conversion overhead must be explicitly stated.

Proposed pivotal inputs requiring independent audit:
- Determinization: 2^{floor((h−2)/31)}≤4(s+2)² (source has h+3 states; stronger s+1 variant under zero-step acceptance).
- Complementation: 2^{floor((h−2)/127)}≤2(s+1) for a complementing 2NFA; source h+2 states.

Success requires both unconditional core claims, valid pivotal dependencies, attribution/priority, two full-package reviewers including a fresh reviewer of final version, compiled/exported/inspected PDF, production publication and verified tracker insertion. No L≠NL or stronger uniform complexity claim follows here.
