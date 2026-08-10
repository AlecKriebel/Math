# Publication-candidate v1 literature and proof-positioning audit

**Paper:** *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*

**Audit date:** 9 August 2026 (America/Los_Angeles)

**Scope:** literature metadata, theorem/proof positioning, and publication-safe comparison language.

**Source rule used:** publisher pages, publisher PDFs/front matter, arXiv records/PDFs, and official conference/project pages only. No external contact was made.

## Executive verdict

The manuscript can make a strong and defensible novelty claim, but the claim should be made at the level of the **proof mechanism and removed hypothesis**, not at the level of entropy growth alone.

The classical line is:

1. Horn--Jackson introduced the complex-balanced free-energy/pseudo-Helmholtz framework in deterministic mass-action kinetics.
2. Anderson--Craciun--Gopalkrishnan--Wiuf identified that deterministic Lyapunov function as the large-volume limit of a stochastic non-equilibrium potential for complex-balanced systems.
3. Anderson--Cappelletti--Kim used the ordinary entropy-like function in an $n$-step embedded-chain proof, under the additional assumption that every species appears as a pure complex $S$ or $2S$.

The new paper's defensible advance is different: it subtracts the **actual carried target**, obtains an **exact** falling-factorial increment, makes target-following jumps have zero reward, and propagates restoring drift along a directed target-following path. That mechanism removes the pure-species hypothesis from the 2020 theorem.

There are two release-critical bibliographic cautions:

- The current official title of arXiv:2409.05340 is **“On the Regulary of Reaction Systems”**. “Regulary” is the spelling on the official record. The title “Non-explosivity of Endotactic Stochastic Reaction Systems” is not the current arXiv title and must not be used.
- The public two-dimensional recurrence result should be described as an **announced/in-preparation result**, with each statement attributed to the source that actually supports it. The 2022 conference page names four collaborators; the 2025 SIAM abstract lists only Andrea Agazzi; the current ConStRAINeD project page lists five authors and “in preparation.” No matching public manuscript was located on arXiv in this audit.

## Priority audit

### P0 — statements that must be exact before submission

1. **Locate the 2020 hypothesis precisely.** Do not say vaguely that Anderson--Cappelletti--Kim's method “needed pure species.” The hypothesis is used in the last case of the proof of Theorem 4.1, in Section 6.1, arXiv v2 PDF pages 17--18, to establish their tier condition (11). It is not used in their general tier/Foster theorem, Theorem 6.1, or in Lemmas 6.2--6.5.
2. **State what the new method replaces.** It replaces the disabled-mixed-complex-to-enabled-pure-complex bridge in that final structural reduction. It does not merely “improve an estimate” in the old proof.
3. **Use Xu's current official title and version.** The verified record is arXiv:2409.05340v2, revised 9 May 2026.
4. **Calibrate the Agazzi status statement.** Use “we did not locate a public manuscript as of 9 August 2026,” not “there is no manuscript.” Do not infer the five-author list from the 2025 abstract; it comes from the ConStRAINeD project page.

### P1 — positioning needed for credibility and impact

1. Describe the residual log-factorial potential as a **discrete, target-shifted analogue** of the Horn--Jackson/pseudo-Helmholtz family, not as the Horn--Jackson function itself.
2. Separate deterministic boundedness/permanence from stochastic positive recurrence. Anderson (2011) and Boros--Hofbauer (2020) motivate the conjecture but do not imply the stochastic result.
3. State that the present theorem **recovers the 2020 theorem as a special case at the assumption level**: every network satisfying the 2020 binary/single-linkage/pure-complex assumptions satisfies the present binary/single-linkage assumptions.
4. Treat the two-dimensional announced theorem as complementary: it is dimension-restricted but structurally broader in the public descriptions, whereas the present theorem allows arbitrary finite species dimension but assumes bimolecularity and one linkage class.

### P2 — citation hygiene

1. Cite standard Markov-chain books by chapter/section unless the exact theorem text has been checked. In particular, do not introduce an unverified “Meyn--Tweedie Theorem 11.3.15.”
2. Preserve capitalization in BibTeX for `{Markov}`, `{Foster--Lyapunov}`, `{2d}`, and chemical-reaction-network acronyms where the bibliography style would otherwise downcase them.
3. Cite the published 2015 title as “... for Reaction Networks,” not the earlier arXiv wording “... for Chemical Reaction Networks.”

## 1. Classical entropy and stochastic non-equilibrium potential

### Horn and Jackson (1972)

**Verified metadata.** F. Horn and R. Jackson, “General mass action kinetics,” *Archive for Rational Mechanics and Analysis* **47**(2), 81--116 (1972), DOI 10.1007/BF00251225. The Springer record gives January 1972 and explicitly describes the decreasing free-energy property and the class called complex-balanced kinetics.

**Safe mathematical role.** This is the foundational deterministic complex-balance/free-energy reference. It supports calling

$$
G_c(r)=\sum_i\left[r_i\bigl(\log(r_i/c_i)-1\bigr)+c_i\right]
$$

the Horn--Jackson or pseudo-Helmholtz family in the reaction-network literature. It does not contain the target mark, residual subtraction, or exact falling-factorial identity used in the present paper.

### Anderson, Craciun, Gopalkrishnan, and Wiuf (2015)

**Verified metadata.** “Lyapunov Functions, Stationary Distributions, and Non-equilibrium Potential for Reaction Networks,” *Bulletin of Mathematical Biology* **77**(9), 1744--1767 (2015), DOI 10.1007/s11538-015-0102-8.

**Exact positioning in the author version.** In arXiv:1410.4820:

- formula (2), PDF page 2, is the pseudo-Helmholtz function
  $$
  V(x)=\sum_i\left[x_i(\log x_i-\log c_i-1)+c_i\right];
  $$
- Theorem 7, PDF page 8, gives the scaled product-Poisson stationary distribution for a complex-balanced system;
- Theorem 8, beginning on PDF page 8, proves that the scaled stochastic non-equilibrium potential converges to $V$, which is a deterministic Lyapunov function.

**Safe comparison.** This paper establishes the stochastic-to-deterministic large-volume interpretation of the classical entropy for complex-balanced systems. The present residual factorial is related through Stirling asymptotics, but its exact finite-state identity comes from subtracting the carried target, which is not part of the 2015 construction.

### Anderson, Cappelletti, Koyama, and Kurtz (2018)

**Verified metadata.** “Non-explosivity of Stochastically Modeled Reaction Networks that are Complex Balanced,” *Bulletin of Mathematical Biology* **80**(10), 2561--2579 (2018), DOI 10.1007/s11538-018-0473-8.

**Exact positioning in the author version.** In arXiv:1708.09356:

- Theorem 2, PDF page 12, proves nonexplosion from a stationary solution $\pi$ of the forward equation plus the integrability condition $\sum_x\pi(x)q(x)<\infty$;
- Remark 1, PDF pages 12--13, identifies that condition with positive recurrence of the embedded jump chain after weighting by the total jump rate;
- Corollary 1, PDF page 13, specializes the criterion to reaction networks;
- Theorem 3, PDF page 13, concludes nonexplosion for all complex-balanced stochastic mass-action systems.

**Safe comparison.** This is a classical nonexplosion/stationary-integrability reference. It does not provide the marked-target drift argument and should not be presented as a prior positive-recurrence theorem for all weakly reversible bimolecular networks.

**Citation placement.** Horn--Jackson (1972) and Anderson--Craciun--Gopalkrishnan--Wiuf (2015) are the direct citations for the entropy/non-equilibrium-potential sentence. Anderson--Cappelletti--Koyama--Kurtz (2018) is better placed in the separate nonexplosion/complex-balance comparison. A three-reference citation after the entropy formula is not false, but it obscures what the 2018 paper specifically contributes.

### Exact asymptotic relation to the present potential

For residual $r=x-t\in\mathbb N_0^d$, Stirling's formula gives

$$
\sum_i\log(r_i!)
=\sum_i(r_i\log r_i-r_i)
+O\!\left(\sum_i\log(r_i+1)\right).
$$

Thus its leading term agrees with $G_{\mathbf 1}(r)$ up to an additive constant and the stated lower-order term. For general $c$, $G_c$ also contains the linear term $-\sum_i r_i\log c_i$. The publication-safe conclusion is:

> The residual log-factorial potential is a discrete, target-shifted analogue of the classical Horn--Jackson entropy, not that entropy itself. Its new feature is the subtraction of the complex actually produced by the preceding reaction, which yields the exact increment
> $$
> V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}
> $$
> and makes a reaction sourced at the carried target have exactly zero increment.

This is sharper and more defensible than claiming novelty for “an entropy Lyapunov function.”

## 2. Deterministic single-linkage results

### Anderson (2011): boundedness

**Verified metadata.** David F. Anderson, “Boundedness of trajectories for weakly reversible, single linkage class reaction systems,” *Journal of Mathematical Chemistry* **49**(10), 2275--2290 (2011), DOI 10.1007/s10910-011-9886-4.

**Exact result.** Theorem 3.12, arXiv:1104.4992 PDF page 16, states that every weakly reversible, single-linkage, non-autonomous mass-action system with bounded kinetics has bounded trajectories. The proof uses decrease of an entropy-like function outside a sufficiently large set. The paper itself notes immediately afterward that this estimate alone does not establish permanence.

### Boros and Hofbauer (2020): permanence

**Verified metadata.** Balázs Boros and Josef Hofbauer, “Permanence of Weakly Reversible Mass-Action Systems with a Single Linkage Class,” *SIAM Journal on Applied Dynamical Systems* **19**(1), 352--365 (2020), DOI 10.1137/19M1248431.

**Exact result.** Definition 4.1 and Theorem 4.2, arXiv:1903.03071v2 PDF page 3, state permanence on every positive stoichiometric class for weakly reversible, single-linkage mass-action systems with bounded kinetics; the theorem gives a compact forward-invariant set that every solution enters in finite time.

### Publication-safe deterministic/stochastic distinction

> Deterministically, weak reversibility with one linkage class gives boundedness and, in fact, permanence of positive trajectories (Anderson, 2011; Boros and Hofbauer, 2020). These results motivate the stochastic recurrence conjecture but do not imply it: a countable-state jump process may make arbitrarily large excursions, interact with the boundary, or fail to have finite mean return times even when the corresponding ODE is permanent. The present theorem is therefore a genuinely stochastic recurrence result.

Avoid “the stochastic analogue follows” or any wording suggesting a direct deterministic-to-stochastic implication.

## 3. Full audit of Anderson--Cappelletti--Kim (2020)

### Verified metadata

David F. Anderson, Daniele Cappelletti, and Jinsu Kim, “Stochastically modeled weakly reversible reaction networks with a single linkage class,” *Journal of Applied Probability* **57**(3), 792--810 (2020), DOI 10.1017/jpr.2020.28; arXiv:1904.08967v2.

Their Theorem 4.1, arXiv v2 PDF page 6, assumes:

- weak reversibility;
- binary complexes;
- a single linkage class; and
- for every species $S$, $\{S,2S\}\cap\mathcal C\neq\varnothing$.

It concludes positive recurrence of the associated continuous-time chain.

### Proof dependency map

| Location in arXiv v2 PDF | Role | Uses the pure-species hypothesis? |
|---|---|---:|
| Section 3.3, p. 6, Theorem 3.1 and Lemma 3.2 | Transfer from positive recurrence of the embedded chain to nonexplosion and positive recurrence of the CTMC, using a uniform lower bound on total rate | No |
| Section 4, p. 6, Theorem 4.1 | States the network theorem and its extra hypothesis | In the statement only |
| Section 5, pp. 9--12, Lemmas 5.1--5.6 | Proper tier subsequences, top-tier exit, tier transport after reactions, and intensity/D-tier comparison | No |
| Section 6, p. 12, Theorem 6.1 | General recurrence theorem assuming $T^{S,1}_{\{z_n\}}\subseteq T^{D,1}_{\{z_n\}}$ for every proper tier sequence (condition (11)) | No |
| Section 6, p. 12, Lemma 6.2 | Bounds entropy increments | No |
| Section 6, p. 13, Lemma 6.3 | Bounds path probability times entropy increment and shows convergence to $-\infty$ for a reaction sequence satisfying its top-tier/descending hypotheses | No |
| Section 6, p. 15, Lemma 6.4 | Converts fixed $k$-step path estimates into Foster drift for the $k$-skeleton of the embedded chain | No |
| Section 6, pp. 16--17, Lemma 6.5 | Uses weak reversibility, one linkage class, and condition (11) to build a reaction sequence of length $r=\lvert\mathcal R\rvert$ | No |
| Section 6.1, pp. 17--18, proof of Theorem 4.1 | Proves condition (11) from binary structure plus the pure-species hypothesis | **Yes, only in the final disabled-complex case** |

### The exact place where the hypothesis enters

The proof fixes $y^*\in T^{S,1}$, a top intensity source, and $y^{**}\in T^{D,1}$, a top D-tier complex, and seeks to show $y^*\sim_D y^{**}$, thereby proving condition (11).

The enabled case $y^{**}\notin T^{S,\infty}$ is settled without the extra structural hypothesis by existing tier comparisons; see equation (18) on arXiv PDF page 17.

The hard case begins at equation (19), page 17:

$$
\lambda_{y^{**}}(x_n)=0,
$$

while equation (20), page 18, gives

$$
(x_n\vee1)^{y^{**}}\longrightarrow\infty.
$$

Because the network is binary, these two facts force

$$
y^{**}=S_u+S_v,\qquad x_{n,u}=0,\qquad x_{n,v}\to\infty
$$

after relabeling and passage to the chosen proper sequence. At this exact point the hypothesis supplies either $S_v\in\mathcal C$ or $2S_v\in\mathcal C$.

- If $2S_v\in\mathcal C$, then its D-monomial $x_{n,v}^2$ strictly dominates the D-monomial $x_{n,v}$ of $S_u+S_v$, contradicting $y^{**}\in T^{D,1}$.
- Therefore $2S_v\notin\mathcal C$ along this case and the hypothesis forces $S_v\in\mathcal C$.
- The pure unary complex is enabled and has source intensity
  $$
  \lambda_{S_v}(x_n)=x_{n,v}=(x_n\vee1)^{y^{**}}.
  $$
- Comparing that enabled intensity with the top S-tier source $y^*$ prevents $y^{**}$ from lying strictly above $y^*$ in the D-order. Since $y^{**}$ is already top D-tier, they must be D-equivalent, which establishes (11).

This is the precise obstacle the hypothesis resolves: a **mixed top D-tier complex can be disabled because one coordinate is zero even though its D-monomial diverges through another coordinate**. The proof manufactures an enabled pure unary source with comparable intensity. Calling the hypothesis merely a “technical artifact” would be inaccurate and unnecessarily dismissive; it performs a specific structural job in the proof.

### What the present marked-target argument changes

The present proof does not attempt to prove Anderson--Cappelletti--Kim condition (11). It changes the state and the Lyapunov accounting:

1. the embedded chain records the actual reaction channel that fired and carries its target $t$;
2. the post-jump population automatically contains $t$, so the carried target is enabled without finding a pure complex for any species;
3. subtracting $t$ from the population gives the exact next-step reward $\log((x)_t/(x)_s)$;
4. choosing the next reaction with source $s=t$ gives zero reward exactly;
5. strong connectivity of the single linkage class supplies a finite directed target-following path to a selected terminal source, and scalar propagation converts rare terminal firing into restoring drift.

Thus the new mechanism replaces the pure-source availability bridge in the last paragraph of the 2020 proof. It does not invalidate or supersede their tier/Foster machinery; it provides a different closure that removes their extra network hypothesis.

### Recommended comparison paragraph

> Anderson, Cappelletti, and Kim proved positive recurrence for weakly reversible binary networks with one linkage class under the additional condition that, for each species $S$, at least one of $S$ and $2S$ is a complex. In their proof this condition enters only in the final structural reduction to their general tier criterion: a top D-tier mixed complex $S_u+S_v$ may be disabled because the $u$-coordinate vanishes while the $v$-coordinate diverges, and the hypothesis supplies an enabled pure complex whose intensity can be compared with the divergent D-monomial. The marked-target construction used here resolves that boundary obstruction differently. The target of the preceding reaction is automatically enabled at the post-jump state; subtracting it gives an exact target/source factorial ratio, and a directed target-following path transports zero immediate reward until a restoring terminal source is reached. This removes the pure-complex assumption. Consequently, the present theorem recovers the 2020 theorem as a special case and strictly enlarges its network class at the level of assumptions.

The last sentence is justified because the present hypotheses are the 2020 hypotheses with the per-species pure-complex condition removed. If the final theorem is formulated classwise, keep the recovery statement classwise as well.

## 4. Xu arXiv:2409.05340: current record and role

### Current official metadata

As checked on 9 August 2026, the official arXiv record is:

- Chuang Xu;
- **“On the Regulary of Reaction Systems”**;
- arXiv:2409.05340v2 [q-bio.MN], also classified under math.PR;
- submitted 9 September 2024; last revised 9 May 2026;
- arXiv DOI 10.48550/arXiv.2409.05340.

“Regulary” is not a transcription error in this audit; it is the title displayed on the current official record. Preserve it verbatim in the bibliography unless the arXiv record changes before submission.

### Mathematical role

The abstract says that a simple linear Lyapunov condition proves regularity in both stochastic and deterministic senses; as an application, every second-order endotactic mass-action system is regular, hence every bimolecular weakly reversible mass-action system is regular. In the stochastic usage there, regularity includes nonexplosion.

The current v2 PDF also discusses the recurrence conjecture explicitly on page 18 and states that the bimolecular case “has yet to be closed.” Accordingly, it is accurate to say that the May 2026 revision still records the general bimolecular positive-recurrence problem as open; this is separate from its nonexplosion theorem.

Safe language:

> Nonexplosion also follows from Xu's more general regularity theorem for second-order endotactic systems. We nevertheless prove nonexplosion directly as part of the recurrence argument, keeping the probabilistic closure self-contained.

Do not cite Xu as proving positive recurrence of the present network class; the verified claim is regularity/nonexplosion, not recurrence.

## 5. Agazzi two-dimensional recurrence announcement

### What each official source supports

**2022 University of Geneva conference program.** On 10 June 2022, Andrea Agazzi gave “Weakly reversible chemical reaction networks are recurrent in 2d.” The abstract says the positive-recurrence conjecture is answered affirmatively in two dimensions and identifies joint work with Jonathan Mattingly, David Anderson, and Daniele Cappelletti.

**2025 SIAM AG25 abstract book.** The official abstract book, current 17 June 2025 for the 7--11 July 2025 conference, contains MS111, “Weakly Reversible Chemical Reaction Networks Are Recurrent in 2d,” on PDF page 79. Its abstract says that the CTMCs modeling weakly reversible mass-action networks are positive recurrent. It lists Andrea Agazzi as the speaker and does **not** list collaborators.

**Current ConStRAINeD project page.** The project page says that every weakly reversible stochastic reaction network with two species is positive recurrent regardless of rate constants and that the arbitrary-dimensional conjecture remains open. Under “In preparation,” item 16 lists A. Agazzi, D. F. Anderson, D. Cappelletti, L. Laurence, and J. C. Mattingly, “A proof of the chemical recurrence conjecture in two dimensions.” This is the source that supports the current five-author/in-preparation description.

**Public manuscript search.** Exact-title, phrase, and author-combination searches of the official arXiv interface did not locate a matching public manuscript on 9 August 2026. This is a time-stamped search result, not proof that no manuscript exists elsewhere. Recheck immediately before submission.

### Publication-safe status paragraph

> A complementary two-species result has been announced in conference abstracts since 2022. The current ConStRAINeD project page lists a five-author proof of the two-dimensional chemical recurrence conjecture as in preparation and describes positive recurrence for every weakly reversible two-species stochastic reaction network. We did not locate a public manuscript as of 9 August 2026. The announced result and the theorem proved here are therefore differently scoped: the former is dimension-restricted but is described without the present single-linkage and bimolecular restrictions, while the latter treats an arbitrary finite number of species under bimolecularity and a single linkage class.

This paragraph makes no priority claim over an unavailable proof and does not imply that the present theorem subsumes the announced two-dimensional result.

### Citation practice

- Cite the 2022 talk only for the 2022 announcement and four-person collaboration disclosed there.
- Cite the 2025 abstract only for the 2025 talk and its one-paragraph claim.
- Cite or footnote the ConStRAINeD page for the current five-author/in-preparation status.
- Do not create a normal journal/preprint citation for an unpublished manuscript that was not located.

## 6. Standard Markov, Foster, and regenerative references

### J. R. Norris, *Markov Chains* (1997)

**Verified metadata.** Cambridge University Press, Cambridge Series in Statistical and Probabilistic Mathematics 2, 1997; DOI 10.1017/CBO9780511810633; print ISBN 978-0-521-63396-3.

**Recommended use.** The official contents place invariant distributions in Section 1.7, jump chains/holding times/explosion in Chapter 2, and recurrence, invariant distributions, and the ergodic theorem in Sections 3.4, 3.5, and 3.8. This is the natural citation for embedded-chain/continuous-time conversion and elementary irreducible-chain facts.

The 2020 Anderson--Cappelletti--Kim paper says its embedded-chain transfer theorem can be inferred from Norris, Theorem 3.5.1. Because this audit did not obtain the theorem text itself from the publisher preview, the present manuscript should cite Norris broadly and retain its own proof rather than repeat that theorem number as independently verified.

### Meyn and Tweedie, *Markov Chains and Stochastic Stability* (2009)

**Verified metadata.** Second edition, Cambridge University Press, 2009; DOI 10.1017/CBO9780511626630; print ISBN 978-0-521-73182-9.

**Recommended use.** The official contents give:

- Section 8.4, “Classification using drift criteria”;
- Chapter 10, “The existence of $\pi$”;
- Chapter 11, “Drift and regularity,” especially Section 11.3;
- Section 13.2, “Renewal and regeneration”;
- Sections 19.1--19.3, state-dependent, history-dependent, and mixed drift criteria.

The present finite random-time Foster lemma is most naturally described as a countable-state specialization of standard Foster/drift theory, with the paper's self-contained proof carrying the exact burden. Cite Chapters 11 and 19 or the book as a whole. Do not cite an unchecked theorem number.

### Meyn and Tweedie (1993), continuous-time Foster theory

**Verified metadata.** Sean P. Meyn and R. L. Tweedie, “Stability of Markovian processes III: Foster--Lyapunov criteria for continuous-time processes,” *Advances in Applied Probability* **25**(3), 518--548 (1993), DOI 10.2307/1427522.

This is an appropriate background citation for generator-based continuous-time Foster criteria. It should not be represented as the exact source of the manuscript's stopped, finite random-time episode lemma unless a theorem is matched line by line.

### Asmussen, *Applied Probability and Queues* (2003)

**Verified metadata.** Søren Asmussen, second edition, Springer, New York, 2003, Stochastic Modelling and Applied Probability 51, DOI 10.1007/b97236. The publisher contents list “Regenerative Processes,” pp. 168--185, with chapter DOI 10.1007/0-387-21525-5_6.

This is the clean reference for the regenerative occupation formula: stationary mass equals expected occupation during a return cycle divided by expected cycle length. Cite the chapter broadly unless the exact theorem number is checked from the full text.

### Suggested division of citation labor

| Manuscript step | Best standard citation | What the manuscript should still prove |
|---|---|---|
| Embedded jump chain, holding times, explosion | Norris, Chapters 2--3 | The exact lower-bound/return argument used here |
| Random-time Foster drift | Meyn--Tweedie (2009), Chapters 11 and 19 | The finite stopped-episode lemma in the manuscript's notation |
| Continuous-time Foster context | Meyn--Tweedie (1993) | Any specialization actually invoked |
| Return-cycle invariant law and mean occupation | Asmussen (2003), “Regenerative Processes” | Finiteness of the cycle quantities for this chain |
| Elementary invariant/irreducible chain facts | Norris, Sections 1.7 and 3.5 | Class-specific hypotheses and projections |

## 7. Publication-ready comparison paragraphs

### Entropy lineage and novelty

> Entropy growth is classical in reaction network theory. Horn and Jackson introduced the pseudo-Helmholtz free-energy family for complex-balanced deterministic mass-action systems, and Anderson, Craciun, Gopalkrishnan, and Wiuf later recovered it as the large-volume limit of the stochastic non-equilibrium potential of complex-balanced systems. By Stirling's formula, the residual potential used here has the same leading growth when evaluated at the residual population $r=x-t$. It is not, however, the Horn--Jackson function itself. The new ingredient is the target shift: subtracting the complex produced by the preceding reaction yields an exact falling-factorial increment and makes every target-following jump have zero reward.

### Relation to the 2018 complex-balance nonexplosion theorem

> Anderson, Cappelletti, Koyama, and Kurtz proved nonexplosion of complex-balanced stochastic mass-action systems by combining a stationary solution of the forward equation with integrability of the total jump rate. The present argument neither assumes complex balance nor relies on a product-form stationary law; it derives nonexplosion together with positive recurrence from the marked-target Foster construction.

### Relation to deterministic permanence

> Anderson proved boundedness, and Boros and Hofbauer proved permanence, for deterministic weakly reversible single-linkage mass-action systems. Those results provide the deterministic motivation for the stochastic conjecture but do not control stochastic excursions or mean return times. The recurrence theorem here addresses that probabilistic obstruction directly.

### Relation to Anderson--Cappelletti--Kim (2020)

> The closest predecessor is Anderson, Cappelletti, and Kim's positive-recurrence theorem for binary weakly reversible one-linkage networks under the additional condition that each species occurs as $S$ or $2S$. Their hypothesis enters in the final proof that a top intensity tier lies in the top D-tier, specifically when a mixed top D-tier complex is disabled on the boundary. The marked-target construction avoids that comparison: the carried target is enabled automatically, target-following motion has zero exact reward, and strong connectivity propagates the drift to a restoring terminal source. This removes the pure-complex hypothesis and recovers the 2020 theorem as a special case.

### Relation to current nonexplosion and two-dimensional work

> Xu's current arXiv manuscript proves nonexplosion more generally for second-order endotactic stochastic reaction systems. Separately, a full positive-recurrence theorem for weakly reversible two-species systems has been announced and is listed by the ConStRAINeD project as in preparation; no public manuscript was located in our search as of 9 August 2026. These developments are complementary to the present arbitrary-dimension, bimolecular, single-linkage theorem.

## 8. Publication-ready BibTeX

The following entries use final publisher metadata where available. The Agazzi entries intentionally list the speaker, not inferred manuscript authors. For regeneration, choose either the Asmussen book entry or the more specific chapter entry rather than citing both at the same point.

```bibtex
@article{HornJackson1972,
  author  = {Horn, Friedrich J. M. and Jackson, Roy},
  title   = {General Mass Action Kinetics},
  journal = {Archive for Rational Mechanics and Analysis},
  year    = {1972},
  volume  = {47},
  number  = {2},
  pages   = {81--116},
  doi     = {10.1007/BF00251225}
}

@article{AndersonCraciunGopalkrishnanWiuf2015,
  author  = {Anderson, David F. and Craciun, Gheorghe and
             Gopalkrishnan, Manoj and Wiuf, Carsten},
  title   = {Lyapunov Functions, Stationary Distributions, and
             Non-equilibrium Potential for Reaction Networks},
  journal = {Bulletin of Mathematical Biology},
  year    = {2015},
  volume  = {77},
  number  = {9},
  pages   = {1744--1767},
  doi     = {10.1007/s11538-015-0102-8}
}

@article{AndersonCappellettiKoyamaKurtz2018,
  author  = {Anderson, David F. and Cappelletti, Daniele and
             Koyama, Masanori and Kurtz, Thomas G.},
  title   = {Non-explosivity of Stochastically Modeled Reaction Networks
             that are Complex Balanced},
  journal = {Bulletin of Mathematical Biology},
  year    = {2018},
  volume  = {80},
  number  = {10},
  pages   = {2561--2579},
  doi     = {10.1007/s11538-018-0473-8}
}

@article{Anderson2011Boundedness,
  author  = {Anderson, David F.},
  title   = {Boundedness of Trajectories for Weakly Reversible,
             Single Linkage Class Reaction Systems},
  journal = {Journal of Mathematical Chemistry},
  year    = {2011},
  volume  = {49},
  number  = {10},
  pages   = {2275--2290},
  doi     = {10.1007/s10910-011-9886-4}
}

@article{BorosHofbauer2020,
  author  = {Boros, Bal{\'a}zs and Hofbauer, Josef},
  title   = {Permanence of Weakly Reversible Mass-Action Systems with a
             Single Linkage Class},
  journal = {SIAM Journal on Applied Dynamical Systems},
  year    = {2020},
  volume  = {19},
  number  = {1},
  pages   = {352--365},
  doi     = {10.1137/19M1248431}
}

@article{AndersonCappellettiKim2020,
  author  = {Anderson, David F. and Cappelletti, Daniele and Kim, Jinsu},
  title   = {Stochastically Modeled Weakly Reversible Reaction Networks
             with a Single Linkage Class},
  journal = {Journal of Applied Probability},
  year    = {2020},
  volume  = {57},
  number  = {3},
  pages   = {792--810},
  doi     = {10.1017/jpr.2020.28}
}

@book{Norris1997,
  author    = {Norris, J. R.},
  title     = {{Markov Chains}},
  series    = {Cambridge Series in Statistical and Probabilistic Mathematics},
  number    = {2},
  publisher = {Cambridge University Press},
  year      = {1997},
  isbn      = {978-0-521-63396-3},
  doi       = {10.1017/CBO9780511810633}
}

@book{MeynTweedie2009,
  author    = {Meyn, Sean P. and Tweedie, Richard L.},
  title     = {{Markov Chains and Stochastic Stability}},
  edition   = {2},
  publisher = {Cambridge University Press},
  year      = {2009},
  isbn      = {978-0-521-73182-9},
  doi       = {10.1017/CBO9780511626630}
}

@article{MeynTweedie1993,
  author  = {Meyn, Sean P. and Tweedie, R. L.},
  title   = {Stability of {Markovian} Processes {III}:
             {Foster--Lyapunov} Criteria for Continuous-Time Processes},
  journal = {Advances in Applied Probability},
  year    = {1993},
  volume  = {25},
  number  = {3},
  pages   = {518--548},
  doi     = {10.2307/1427522}
}

@book{Asmussen2003,
  author    = {Asmussen, S{\o}ren},
  title     = {Applied Probability and Queues},
  edition   = {2},
  series    = {Stochastic Modelling and Applied Probability},
  volume    = {51},
  publisher = {Springer},
  address   = {New York},
  year      = {2003},
  isbn      = {978-0-387-00211-8},
  doi       = {10.1007/b97236}
}

@incollection{Asmussen2003Regenerative,
  author    = {Asmussen, S{\o}ren},
  title     = {Regenerative Processes},
  booktitle = {Applied Probability and Queues},
  edition   = {2},
  series    = {Stochastic Modelling and Applied Probability},
  volume    = {51},
  publisher = {Springer},
  address   = {New York},
  year      = {2003},
  pages     = {168--185},
  doi       = {10.1007/0-387-21525-5_6}
}

@misc{Xu2026,
  author        = {Xu, Chuang},
  title         = {On the Regulary of Reaction Systems},
  year          = {2026},
  eprint        = {2409.05340},
  archivePrefix = {arXiv},
  primaryClass  = {q-bio.MN},
  doi           = {10.48550/arXiv.2409.05340},
  note          = {Version 2, revised 9 May 2026},
  url           = {https://arxiv.org/abs/2409.05340}
}

@misc{Agazzi2022Talk,
  author       = {Agazzi, Andrea},
  title        = {Weakly Reversible Chemical Reaction Networks Are
                  Recurrent in {2d}},
  year         = {2022},
  howpublished = {Jean-Pierre Eckmann 75 Conference, University of Geneva},
  note         = {Talk on 10 June 2022; the official program identifies
                  joint work with Jonathan Mattingly, David Anderson, and
                  Daniele Cappelletti},
  url          = {https://www.unige.ch/jpe75conference/program.html}
}

@misc{Agazzi2025Talk,
  author       = {Agazzi, Andrea},
  title        = {Weakly Reversible Chemical Reaction Networks Are
                  Recurrent in {2d}},
  year         = {2025},
  howpublished = {Abstract MS111, SIAM Conference on Applied Algebraic
                  Geometry (AG25)},
  note         = {Official abstract book, p. 79; conference held
                  7--11 July 2025},
  url          = {https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf}
}

@misc{ConStRAINeDResults,
  author       = {{ConStRAINeD project}},
  title        = {Results and Publications},
  year         = {2026},
  howpublished = {PRIN 2022 project website},
  note         = {Access year; accessed 9 August 2026. Item 16 lists the
                  two-dimensional chemical recurrence proof as in preparation},
  url          = {https://constrained.polito.it/publications/}
}
```

## 9. Primary-source ledger

All records below were checked during this audit.

- Horn--Jackson publisher record: <https://link.springer.com/article/10.1007/BF00251225>
- Anderson--Craciun--Gopalkrishnan--Wiuf publisher record: <https://link.springer.com/article/10.1007/s11538-015-0102-8>
- Anderson--Craciun--Gopalkrishnan--Wiuf author version: <https://arxiv.org/abs/1410.4820>
- Anderson--Cappelletti--Koyama--Kurtz publisher record: <https://link.springer.com/article/10.1007/s11538-018-0473-8>
- Anderson--Cappelletti--Koyama--Kurtz author version: <https://arxiv.org/abs/1708.09356>
- Anderson boundedness publisher record: <https://link.springer.com/article/10.1007/s10910-011-9886-4>
- Anderson boundedness author version: <https://arxiv.org/abs/1104.4992>
- Boros--Hofbauer publisher record: <https://epubs.siam.org/doi/10.1137/19M1248431>
- Boros--Hofbauer author version: <https://arxiv.org/abs/1903.03071>
- Anderson--Cappelletti--Kim publisher record: <https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/stochastically-modeled-weakly-reversible-reaction-networks-with-a-single-linkage-class/5E9F7DAE999525F8D4A3392F80B3F0C9>
- Anderson--Cappelletti--Kim author version: <https://arxiv.org/abs/1904.08967>
- Xu current arXiv record: <https://arxiv.org/abs/2409.05340>
- Agazzi 2022 official conference program: <https://www.unige.ch/jpe75conference/program.html>
- Agazzi 2025 official SIAM abstract book: <https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf>
- ConStRAINeD current results/publications page: <https://constrained.polito.it/publications/>
- Official arXiv exact-title search used for the in-preparation record: <https://arxiv.org/search/?query=%22A+proof+of+the+chemical+recurrence+conjecture+in+two+dimensions%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50>
- Norris publisher record: <https://www.cambridge.org/core/books/markov-chains/A3F966B10633A32C8F06F37158031739>
- Norris official table of contents: <https://assets.cambridge.org/97805216/33963/toc/9780521633963_toc.pdf>
- Meyn--Tweedie book publisher record: <https://www.cambridge.org/core/books/markov-chains-and-stochastic-stability/E2B82BFB409CD2F7D67AFC5390C565EC>
- Meyn--Tweedie continuous-time article: <https://www.cambridge.org/core/journals/advances-in-applied-probability/article/abs/stability-of-markovian-processes-iii-fosterlyapunov-criteria-for-continuoustime-processes/9B9CB13CED7CFD00C846EBB83B7706AD>
- Asmussen publisher record: <https://link.springer.com/book/10.1007/b97236>
- Asmussen regenerative-process chapter: <https://link.springer.com/chapter/10.1007/0-387-21525-5_6>

## Submission-day checklist for this literature slice

- [ ] Recheck Xu's official title and version immediately before submission; this audit and the candidate bibliography use the official record as displayed on 9 August 2026.
- [x] Include Horn--Jackson, Anderson--Craciun--Gopalkrishnan--Wiuf, Anderson--Cappelletti--Koyama--Kurtz, Anderson (2011), and Boros--Hofbauer in the final bibliography where the corresponding comparison sentences remain.
- [x] In the Anderson--Cappelletti--Kim comparison, identify Section 6.1/equations (19)--(20) and the disabled mixed-complex case.
- [x] Say the present theorem recovers the 2020 result as a special case; do not say their assumption was an “artifact.”
- [x] Keep deterministic permanence and stochastic recurrence logically separate.
- [x] Attribute the Agazzi author/status statements to the correct public sources and time-stamp the no-public-manuscript search.
- [ ] Recheck arXiv and the ConStRAINeD page immediately before journal upload.
- [x] Use broad chapter/section citations for standard Markov theory unless exact theorem text is independently checked.
