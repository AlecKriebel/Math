# Independent priority audit: PR 615 / problem 4200010

Reviewer: independent priority adversary subagent `pr615_priority_adversary`.
Date: 12 October 2026, America/Los_Angeles (13 October 2026 UTC).
Input: the frozen candidate under `native/unsolved_math_prioritization/attempts/4200010/submission/FULL_PROOF.md`.

## Verdict

The construction can honestly be presented as **a self-contained explicit answer to the existential question in Knill's unrestricted printed formulation**. It cannot honestly be advertised as the discovery of a new zero-exponent Hamiltonian phenomenon, the first solution of a currently unresolved problem, or a resolution of the source's genericity/weak-mixing guess.

This conclusion has positive historical evidence. The exact skew shift and its continuous-spectrum mechanism occur in Anzai (1951), Section 6, Theorem 6 and its Corollary, pp. 91-92 [S02]. The symplectic extension of a cosymplectic manifold and realization of its Reeb field as a Hamiltonian vector field are explicitly in de Leon and Saralegi (1993), Lemma 3.2, p. 5036, and Section 6.1, p. 5042 [S04]. These ingredients give the printed unrestricted existential conclusion by the short deduction below. The compact ambient topology is the classical unipotent torus bundle used by Thurston (1976), p. 467 [S03]. Thus, absent an additional original contribution, the strongest defensible publication is an elementary explanatory research note applying classical constructions.

No inspected source was found explicitly labeling Knill's item 10 solved by this particular formula. That bounded negative finding does **not** establish priority. Conversely, the elementary classical deduction below is enough to refute a broad claim that the Hamiltonian behavior itself is new. I do not independently change the queue status: the parent must distinguish an explicit prior statement from a consequence of old theorems when recording its outcome. If `claimed_solved` is intended to certify novel resolution of a still-open problem, this audit supplies a material priority concern that must be resolved before publication with that characterization.

## Exact source question and scope

Knill's 19 October 2000 problem list, item 10, asks for a Hamiltonian example with positive Liouville measure outside the almost-periodic invariant region and the positive-exponent region [S01]. The printed question does not state Euclidean phase space, standard cotangent symplectic form, analyticity, a mechanical kinetic-plus-potential Hamiltonian, contact-type energies, robustness, or genericity. Its subsequent guess about weak mixing and generic occurrence is distinct.

The candidate addresses this unrestricted smooth symplectic interpretation. Its constant-roof suspension has clock eigenfunctions and is not weakly mixing. Its failure of almost periodicity on every connected band energy component, and on every positive-volume invariant subset of the band, is stronger than merely averaging continuously varying integrable frequencies across energies. That distinction is essential: the source's later spectral-integrability discussion explicitly emphasizes ergodic invariant measures [S07], and his 2023 discussion distinguishes mixed spectral behavior from a purely singular-continuous class [S08]. Neither later source adds a requirement to the 2000 printed existence question.

The original source is a personal problem list dated 2000. It is not evidence that the question remained unresolved as of 2026. An unsolved-problem catalogue entry is also not such evidence.

## Checkable classical deduction: the full-volume issue

This is an authored deduction, not a quotation of a theorem allegedly printed in an earlier source.

Take Anzai's map with irrational rotation parameter and cocycle x,

`F(x,y)=(x+a,y+x)` on the area torus.

Its iterates have derivative `[[1,0],[n,1]]`; its character `exp(2*pi*i*y)` has orthogonal integer translates. Anzai's Theorem 6 and Corollary describe the corresponding continuous-spectrum complement [S02]. The map is ergodic.

Form its constant-roof mapping torus N, carrying the descended closed forms beta and tau from the torus area and the clock differential. The vertical suspension field R satisfies `i_R beta=0`, `tau(R)=1`, and preserves `nu=beta wedge tau`. This is the standard cosymplectic suspension. It is also a classical Heisenberg nilflow: in the notation of Avila-Forni-Ulcigrai, Section 2.2, Lemma 1, choose lattice integer E=1, `w_y=1`, `w_x=a`, and `w_z=-a/2`; the return time is 1 and the return map is exactly F [S05]. Their description explicitly recalls this as a known construction, rather than presenting it as their mixing theorem.

Now apply the symplectic extension in de Leon-Saralegi [S04]:

`M=N x R_E`, `omega=beta+tau wedge dE`, `H=E`.

Their Section 6.1 identifies the Hamiltonian field of the added coordinate with R. Hence any nonempty finite interval I defines an invariant band `N x I`, with positive finite full four-dimensional Liouville measure `|I|`. In product coordinates the flow is `(q,E)->(psi_s(q),E)`; the transverse energy derivative is the identity. Constant-roof suspension of F has at most linear tangent growth, and the inverse has the same bound, so all four exponents vanish.

For any positive-volume invariant subset C of the band, Fubini, invariance at rational times, strong continuity, and ergodicity on N give `C=N x J` modulo null sets, for a positive-length measurable J. The suspension of the character above has orthogonal integer translates on C. Thus C is not almost periodic. This is the full-phase-volume conclusion, not a statement on one measure-zero energy surface.

This deduction is valid on the noncompact M with a global real Hamiltonian; the printed source does not require compactness. The candidate's second energy circle and smooth cutoff provide a compact version. The cutoff removes the global error of calling an angular coordinate a real Hamiltonian, but it adds no new dynamical mechanism. Compact thickening itself is standard: see Thurston's particular torus-bundle construction [S03], the product extension discussion [S10], and the exact circle form in Miranda-Nicolas (2026), Proposition 4.1 [S11]. The latter predates the frozen candidate, but is not needed to place the underlying Hamiltonian extension before 2000.

## Identification of the compact topology

The affine translation in F does not produce a new underlying manifold. On the cover define

`u=x+a*t`, `v=y-(a/2)*t*(t+1)`.

For the candidate gluing `(x,y,t)->(x+a,y+x,t-1)`, these coordinates transform as

`(u,v,t)->(u,v+u,t-1)`.

The coordinate change is well-defined in the torus coordinates for each real t and has a smooth inverse. Thus the mapping torus is smoothly the usual unipotent torus mapping torus; its product with a circle is the Kodaira-Thurston manifold (after exchanging the torus coordinates if using Thurston's upper-triangular matrix). This establishes a topology identification, not a claim that every choice of symplectic form is identical to Thurston's original form.

## Closest alternatives and why they are not exact prior matches by themselves

| Family | Verified content | Exact remaining mismatch or conclusion |
| --- | --- | --- |
| Anzai / Heisenberg nilflow | The same skew shift, continuous spectrum, and constant-roof nilflow model are classical [S02, S05]. | A discrete map alone has no full Hamiltonian phase volume. The standard extension [S04] closes this gap. |
| Symplectic / cosymplectic extension | The added-coordinate symplectic form and Hamiltonian/Reeb identity are explicit in 1993 [S04]. | Together with the first row, they imply the unrestricted target on a positive band. A compact cutoff is the candidate's elementary presentation choice. |
| Anosov-Katok | Weakly mixing smooth area maps with zero entropy are classical; modern primary authors recall the disk/sphere constructions [S12-S14]. | A discrete map alone is not a flow answer. The same mapping-torus extension produces a second existence route. Topological entropy zero alone is not a pointwise exponent proof; smooth invariant volume and the entropy formula, or rigidity, must be used. This route is not needed by the candidate. |
| Knill 1999 | Theorem 3.3, pp. 87-88, gives weakly mixing invariant tori through Hamiltonian perturbation [S06]. | An individual torus is null for ambient Liouville volume. It does not by itself solve item 10. |
| Fayad 2002 | Corollary 2, p. 442, yields mixing invariant tori on a distinguished energy surface [S09]. | An uncountable dense family is not automatically a positive-measure family. That energy surface is also null for full phase volume. |
| Katok 1973 | Abstract: ergodicity on each constant-energy manifold; the related oscillator example has discrete spectrum according to the primary retrospective [S15]. | Ergodicity is not failure of almost periodicity. Full text retrieval failed; no exact ugly-set priority theorem is inferred from the abstract. |
| Mixing time changes of nilflows | Explicit mixing roofs occur in [S05], Theorem 4 and examples, p. 381. | The candidate uses constant roof and does not claim mixing. Nonconstant-roof time changes require a compatible Hamiltonian realization argument; no such theorem is silently assumed here. |
| Locally Hamiltonian surface flows | Classical parabolic examples and extensive modern literature. | A multivalued Hamiltonian / locally Hamiltonian field is not automatically a global autonomous real Hamiltonian. This broad family is background, not a direct priority verdict. |

## Required publication changes

1. Cite Anzai (1951), Section 6/Theorem 6/Corollary, for the skew shift and its spectral mechanism. A generic attribution only to 'classical skew shifts' is inadequate after locating this exact source.
2. Cite de Leon-Saralegi (1993), Lemma 3.2 and Section 6.1, for the Hamiltonian extension. Describe the proof as an explicit application of the standard cosymplectic construction.
3. Cite Thurston (1976), p. 467, for the compact torus-bundle topology/construction; [S05] can be added for the classical nilflow identification. Do not claim a new compact symplectic manifold.
4. Explicitly say that the printed unrestricted existence question has this elementary answer, while historical first priority and contemporary openness are not established. Remove language such as 'first', 'long-standing open problem solved', 'previously unresolved in general', 'novel chaotic Hamiltonian mechanism', or genericity/weak-mixing conclusions.
5. Preserve the exact limitations already in the proof: unrestricted smooth symplectic category, no positive-volume weak-mixing conclusion, and no prescribed standard phase space or mechanical Hamiltonian.

Suggested scope sentence for a paper:

> We give a self-contained elementary construction answering the positive-volume existence question in item 10 of Knill's 2000 list, interpreted in the unrestricted smooth symplectic category. The construction combines the classical Anzai skew shift with its standard cosymplectic suspension and Hamiltonian extension; we make no claim of historical first priority.

This formulation is honest. The words 'answering the question' concern the mathematical implication proved here; they should not be coupled elsewhere with a claim that the phenomenon is newly discovered or was still open immediately before this work.

## Limits and exact gaps

- A bounded priority audit cannot prove absence of any earlier explicit presentation. No such presentation of this exact compact cutoff / measure 1/4 example was located.
- There is positive evidence for all central classical mechanisms. There is no unsupported mathematical gap in the classical deduction above; novelty of a particular exposition is a different issue.
- The source author's unstated intentions cannot be certified from published wording. This note does not resolve versions imposing standard Euclidean/cotangent geometry, natural Hamiltonians, contact type, or genericity.
- Katok's 1973 full text could not be acquired through the attempted source. Its abstract and primary retrospective were checked, and no conclusion exceeding them is credited to it.
- Green (1961) and Auslander-Green-Hahn (1963) are historical pointers cited in [S05]; their full theorem proofs were not directly inspected. The priority conclusion uses directly inspected Anzai and de Leon-Saralegi instead.

All third-party documents and rendered source pages are confined to ignored `sources.private/`. No outreach, PR comments, merges, publishing, branch change, or git mutation was performed by this reviewer.
