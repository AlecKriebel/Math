# Proof-first publication audit of the primary literature for T3-2

**Audit date:** 2026-08-12 PDT.

**Status of this note:** publication and priority audit only.  It does not
certify the internal proof and does not alter any theorem file.  All substantive
claims below were checked against a paper, an arXiv record, or an official
publisher/author project page.  No secondary source is used as authority.

## 1. Prospective result being audited

The prospective classwise statement is the following.

Let every complex of a finite stochastic mass-action network have total
molecularity at most two, and let every linkage class be weakly reversible.
Fix a closed irreducible population class \(\Gamma\).  Delete coordinates that
are constant on \(\Gamma\), delete linkages having no source enabled anywhere
on \(\Gamma\), and merge projected linkages that share a projected complex,
retaining parallel labelled reaction channels.  If the resulting exact
fixed-class network has at most three dynamic species and at most two active
linkage classes, then the CTMC restricted to \(\Gamma\) is nonexplosive and
positive recurrent for every choice of positive rate constants.

Here "binary" must mean that **every complex**, source or target, has total
degree at most two.  The fixed-class reduction and the meanings of "active"
and "merge" are part of the proposed theorem, not conventions supplied by the
papers below.

## 2. Bottom-line literature verdict

As of the audit date, I located no posted manuscript or refereed paper whose
stated theorem subsumes the entire prospective T3-2 result.  I also located no
published or posted counterexample to positive recurrence of a weakly
reversible stochastic mass-action network in the T3-2 class.

The main established overlaps are:

1. complex-balanced systems, and hence weakly reversible deficiency-zero
   systems, by Anderson--Craciun--Kurtz (2010) together with the later
   nonexplosion theorem;
2. the Anderson--Kim (2018) top-S-tier descending-source criterion;
3. the Anderson--Cappelletti--Kim (2020) one-linkage binary theorem when every
   species occurs as \(S\) or \(2S\), and their broader proper-tier criterion;
4. every one-dimensional stoichiometric system in the weakly reversible class,
   by Wiuf--Xu (arXiv v3, 2023);
5. fully open or suitably dissipatively augmented strongly endotactic systems,
   by Anderson--Cappelletti--Kim--Nguyen (2020).

The important priority caveat is an independent five-author work entitled
*A proof of the chemical recurrence conjecture in two dimensions*.  On
2026-08-12 the authors' project page still placed it under **"In preparation"**,
and an exact-title arXiv search returned no record.  No theorem statement or
proof was available to audit.  It is therefore an announcement and novelty
caveat, not an established result that can be invoked in a proof.

The defensible publication claim is consequently not "the first proof" of an
unqualified three-species assertion.  A safer description is that the result
extends posted/refereed parameter-independent recurrence guarantees into the
restricted regime of three dynamic species and two active linkage classes.

## 3. Anderson--Kim (2018): exact tier criterion and numbering

### Bibliographic record

David F. Anderson and Jinsu Kim, *Some Network Conditions for Positive
Recurrence of Stochastically Modeled Reaction Networks*, **SIAM Journal on
Applied Mathematics** 78(5) (2018), 2692--2713,
[DOI 10.1137/17M1161427](https://epubs.siam.org/doi/10.1137/17M1161427).
The publisher records submission on 2017-12-15, acceptance on 2018-08-16,
and online publication on 2018-10-16.  The open preprint is
[arXiv:1710.11263v3](https://arxiv.org/abs/1710.11263).

### Published Theorem 9

For a tier sequence \(\{x_n\}\), let
\(T^{S,1}_{\{x_n\}}\) be its top stochastic, or S-type, tier and let
\(D_{\{x_n\}}\) be the source complexes of reactions that descend between
D-type tiers.  The exact hypothesis is

\[
 T^{S,1}_{\{x_n\}}\cap D_{\{x_n\}}\ne\varnothing
 \quad\text{for every tier sequence }\{x_n\}.             \tag{AK}
\]

Under (AK), for every positive choice of rate constants, the stochastic
mass-action process has both conclusions:

1. each state in each closed irreducible component is positive recurrent;
2. from every initial state, the expected entrance time into the union of the
   closed irreducible components is finite.

Published Corollary 10 replaces (AK) by the stronger convenient condition
that descending sources are nonempty and the top D-tier equals the top
S-tier along every tier sequence.

This is a sufficient criterion, not a theorem that weak reversibility by
itself implies recurrence.  In particular, a T3-2 seam can have a globally
top enabled S-tier whose reactions are D-neutral while all descending sources
are in a lower-rate linkage.  The theorem is silent there.

### Journal versus arXiv numbering

The final journal article numbers the result **Theorem 9** and its corollary
**Corollary 10**.  The text of arXiv v3 uses section numbering: the same result
is **Theorem 4.2**, followed by **Corollary 4.3**.  The general Foster theorem
is journal Theorem 3 but arXiv Theorem 3.1.

Publication recommendation: cite the version of record as
"Anderson--Kim [journal reference, Theorem 9]."  If the arXiv locator is also
given for access, add a parenthetical note once -- "Theorem 4.2 in arXiv v3"
-- rather than using the arXiv number as though it were the journal number.

### Fixed-class use of Theorem 9

The published statement assumes (AK) for all tier sequences in the ambient
state space; it is not stated as a fixed-class theorem.  Its proof, however,
is a Foster contradiction that localizes cleanly to a closed class.

Indeed, with the entropy potential \(V\), failure of a uniform negative drift
outside a finite subset produces a sequence \(x_n\) with
\(|x_n|\to\infty\) and \({\cal A}V(x_n)>-1\).  A tier subsequence is extracted,
and (AK) forces \({\cal A}V(x_n)\to-\infty\), a contradiction.  If the chain is
restricted to a closed irreducible class \(\Gamma\), the same argument starts
with \(x_n\in\Gamma\), and the restricted generator is the same on \(\Gamma\).
Thus the proof needs (AK) only for tier sequences contained in \(\Gamma\).

This class-local variant is an immediate proof adaptation, **not a separately
stated Anderson--Kim theorem**.  Any T3-2 branch using it should include the
short restriction corollary explicitly.  It should not cite published
Theorem 9 as if that theorem literally had the weaker class-local premise.

## 4. Anderson--Cappelletti--Kim (2020): one linkage

### Bibliographic record

David F. Anderson, Daniele Cappelletti, and Jinsu Kim, *Stochastically Modeled
Weakly Reversible Reaction Networks with a Single Linkage Class*, **Journal of
Applied Probability** 57(3) (2020), 792--810,
[DOI 10.1017/jpr.2020.28](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/stochastically-modeled-weakly-reversible-reaction-networks-with-a-single-linkage-class/5E9F7DAE999525F8D4A3392F80B3F0C9),
published online 2020-09-04.  Open preprint:
[arXiv:1904.08967v2](https://arxiv.org/abs/1904.08967).

### Theorem 4.1: exact structural scope

Theorem 4.1 assumes all of the following:

- stochastic mass-action kinetics;
- weak reversibility;
- a single linkage class;
- binary complexes;
- for every species \(S\), at least one of \(S\) and \(2S\) is a complex:
  \(\{S,2S\}\cap\mathcal C\ne\varnothing\).

It concludes that the associated continuous-time Markov chain is positive
recurrent.  The statement is parameter-independent: \(\kappa\) is an arbitrary
positive rate vector.  The proof treats an absorbing initial state separately
and otherwise works on the reachable state space from the fixed initial state,
using an \(n\)-step embedded chain and then journal Theorem 3.1 to recover
nonexplosive positive recurrence in physical time.

In a binary network, the phrase "a multiple of every species" therefore means
precisely \(S\) or \(2S\); it does not mean that the zero complex or a mixed
complex containing \(S\) suffices.

### Theorem 6.1: broader analytic scope

Theorem 6.1 does not assume binary complexes or pure multiples.  It fixes a
weakly reversible mass-action system with one linkage class and an initial
state \(x_0\).  If every proper tier sequence of the reachable chain satisfies

\[
 T^{S,1}_{\{z_n\}}\subseteq T^{D,1}_{\{z_n\}},             \tag{ACK}
\]

then the chain is positive recurrent.  The paper prints \(\subset\); the proof
uses inclusion, not a strict-subset requirement.

Theorem 4.1 proves (ACK) from binarity plus the pure-multiple hypothesis.  It
does **not** establish all weakly reversible one-linkage binary systems.  For
example, the support \(\{0,B,2B,A+B\}\) lacks a pure multiple for \(A\), and
on the face \((A,B)=(n,0)\) its disabled mixed source can obstruct (ACK).
Such supports require an additional argument in T3-2.

## 5. Anderson--Craciun--Kurtz product form, and nonexplosion

### Product-form paper

David F. Anderson, Gheorghe Craciun, and Thomas G. Kurtz, *Product-Form
Stationary Distributions for Deficiency Zero Chemical Reaction Networks*,
**Bulletin of Mathematical Biology** 72 (2010), 1947--1970,
[DOI 10.1007/s11538-010-9517-4](https://link.springer.com/article/10.1007/s11538-010-9517-4),
published online 2010-03-20; open version
[arXiv:0803.3042](https://arxiv.org/abs/0803.3042).

Published Theorem 4.1 says that if the deterministic mass-action system with
the chosen rates is complex balanced at \(c\in\mathbb R^d_{>0}\), then the
stochastic system has the full-lattice Poisson product stationary law

\[
 \pi(x)=\prod_{i=1}^d e^{-c_i}\frac{c_i^{x_i}}{x_i!}.
\]

On each closed irreducible component \(\Gamma\), the stationary law is its
normalized restriction,

\[
 \pi_\Gamma(x)=M_\Gamma\prod_{i=1}^d\frac{c_i^{x_i}}{x_i!}
 \quad(x\in\Gamma),
\]

and is zero off \(\Gamma\).

Published Theorem 4.2 combines this with the deterministic deficiency-zero
theorem: if the network is weakly reversible and has deficiency zero, then for
every positive rate vector it has the product-form stationary distributions
above.

### Why the 2018 nonexplosion citation should accompany it

The 2010 theorem constructs stationary/invariant probabilities.  In an
infinite-state CTMC, a formal stationary solution alone should not silently be
used to rule out explosion.  The clean companion citation is:

David F. Anderson, Daniele Cappelletti, Masanori Koyama, and Thomas G. Kurtz,
*Non-explosivity of Stochastically Modeled Reaction Networks that are Complex
Balanced*, **Bulletin of Mathematical Biology** 80 (2018), 2561--2579,
[DOI 10.1007/s11538-018-0473-8](https://link.springer.com/article/10.1007/s11538-018-0473-8),
published 2018-08-16; open version
[arXiv:1708.09356v2](https://arxiv.org/abs/1708.09356).

Its Theorem 3 states that complex-balanced stochastic mass-action systems are
nonexplosive for every initial distribution.  Combining that theorem with the
normalizable class-restricted product form gives positive recurrence on each
closed irreducible class by standard irreducible CTMC theory.

For T3-2, nonexplosion can also be proved directly: a binary-source reaction
cannot increase total population because its target is binary, so every
population-increasing channel has source degree at most one and aggregate
positive-jump rate \(O(1+|x|)\).  That independent argument avoids relying on
complex balance outside the deficiency-zero branches.

### Application warning after projection

Deficiency is to be computed for the exact reduced network after constant
coordinates are removed and projected linkage graphs are merged.  Deficiency,
linkage count, and complex balance can change under projection.  The 2010
theorem does not itself prove that the project's fixed-class reduction is a
CTMC conjugacy or that weak reversibility survives it; those are separate
lemmas the manuscript must retain.

## 6. Later established partial results screened through 2026

### One-dimensional stoichiometric systems

Carsten Wiuf and Chuang Xu, *Classification and Threshold Dynamics of
Stochastic Reaction Networks*,
[arXiv:2012.07954v3](https://arxiv.org/abs/2012.07954), revised 2023-01-24.
No journal reference is shown on the arXiv record as of the audit date.

Their Corollary 4.10 treats weakly reversible mass-action systems under
\(\dim S=1\) (hypothesis H2) and nontrivial reactions in both directions
(H3).  It gives positive recurrence on every positive irreducible component
and an exponentially ergodic stationary distribution.  The paper treats the
remaining finite/trivial class issues in its one-dimensional classification.
This subsumes all genuinely one-dimensional T3-2 branches, without a binary
restriction, but says nothing about the rank-two or rank-three branches.

### Strongly endotactic networks

David F. Anderson, Daniele Cappelletti, Jinsu Kim, and Tung Nguyen, *Tier
Structure of Strongly Endotactic Reaction Networks*, **Stochastic Processes
and their Applications** 130(12) (2020), 7218--7259,
[DOI 10.1016/j.spa.2020.07.012](https://www.sciencedirect.com/science/article/pii/S0304414920303239),
open version [arXiv:1808.05328v2](https://arxiv.org/abs/1808.05328).

Theorem 4.2 characterizes strong endotacticity by deterministic tier
descent.  It is not a universal stochastic recurrence theorem.  Corollary 7.1
does give positive recurrence for a binary strongly endotactic network after
adding every species outflow and an arbitrary subset of inflows.  Theorem 7.2
is a higher-order dissipative augmentation theorem.  Neither supplies the
missing undrained one- or two-linkage T3-2 cases.

Examples 3.1 and 3.2 are, respectively, transient and explosive strongly
endotactic stochastic systems.  They are directed non-weakly-reversible
networks and contain complexes of molecularity greater than two.  They are
therefore warnings against substituting deterministic tier geometry for a
stochastic proof, but they are not counterexamples to T3-2.

Andrea Agazzi and Jonathan C. Mattingly, *Seemingly Stable Chemical Kinetics
Can Be Stable, Marginally Stable, or Unstable*, **Communications in
Mathematical Sciences** 18(6) (2020), 1605--1642,
[publisher PDF](https://archive.intlpress.com/site/pub/files/_fulltext/journals/cms/2020/0018/0006/CMS-2020-0018-0006-a005.pdf),
likewise exhibits positive, null, and transient stochastic behavior for
networks with nearly identical stable fluid limits.  Its displayed networks
are not weakly reversible and use high-molecularity complexes.  It does not
contradict T3-2; it reinforces the boundary-risk warning.

### Stationary measure is not stationary probability

Carsten Wiuf and Chuang Xu, *Any Stochastic Reaction Network Has a Stationary
Measure*, [arXiv:2312.07590v1](https://arxiv.org/abs/2312.07590), posted
2023-12-11.  Theorem 3.1 gives a stationary **measure** on any closed
irreducible component.  The paper explicitly notes that positive recurrence
is still needed to normalize that measure to a distribution.  This result
does not settle T3-2.

### Ergodicity and reduction papers that do not prove recurrence here

David F. Anderson, Daniele Cappelletti, Wai-Tong Louis Fan, and Jinsu Kim,
*A New Path Method for Exponential Ergodicity of Markov Processes on
\(\mathbb Z^d\), with Applications to Stochastic Reaction Networks*, **SIAM
Journal on Applied Dynamical Systems** 24(2) (2025), 1668--1710,
[DOI 10.1137/24M1665933](https://epubs.siam.org/doi/10.1137/24M1665933),
[arXiv:2309.06970v2](https://arxiv.org/abs/2309.06970).  The general path
method starts from an ergodic chain with a stationary distribution and proves
spectral-gap conclusions under extra path/rate hypotheses.  Corollary 3.3
applies it to open complex-balanced networks.  It does not establish the
existence of a stationary probability for arbitrary weakly reversible T3-2
systems.

Linard Hoessly, Carsten Wiuf, and Panqiu Xia, *Asymptotic Analysis for
Stationary Distributions of Multiscaled Reaction Networks*, **Advances in
Applied Probability**, First View (2025), 1--31,
[DOI 10.1017/apr.2025.10040](https://www.cambridge.org/core/journals/advances-in-applied-probability/article/asymptotic-analysis-for-stationary-distributions-of-multiscaled-reaction-networks/7551C68BD723A93B1D707B7A0F4226D2),
published online 2025-12-11.  Its reduction eliminates fast non-interacting
species in a scaling limit, principally from complex-balanced systems.  Its
positive-recurrence conclusions are conditional on inherited stationary
distributions.  This is not the exact deletion of coordinates constant on a
fixed class and does not imply T3-2.

Minjun Kim, Seokhwan Moon, and Jinsu Kim, *Long-Term Behavior of Markov Chains
on Non-negative Integer Grids and Its Application*, **SIAM Journal on Applied
Mathematics** 86(4) (2026), 1463--1488,
[DOI 10.1137/25M1814074](https://epubs.siam.org/doi/abs/10.1137/25M1814074),
published online 2026-07-02.  It gives one-dimensional CTMC criteria with
arbitrary transition rates and classifies broad rational-rate models; the
high-dimensional reaction-network use is via one-dimensional approximation.
It does not supply a multidimensional weak-reversibility theorem.

Lucie Laurence and Philippe Robert, *Scaling Methods for Stochastic Chemical
Reaction Networks*, [arXiv:2310.01949v3](https://arxiv.org/abs/2310.01949),
revised 2025-12-17 and marked "to appear" in *Stochastic Processes and their
Applications*, develops scaling and stopping-time stability methods and works
through model classes.  It contains no stated universal theorem for weakly
reversible binary networks with three species or two linkages.

## 7. Unavailable two-dimensional work: priority caveat only

The author-run
[ConStRAINeD results and publications page](https://constrained.polito.it/publications/)
was checked on 2026-08-12.  Item 16, under the heading **"In preparation"**,
is:

Andrea Agazzi, David F. Anderson, Daniele Cappelletti, Lucie Laurence, and
Jonathan C. Mattingly, *A proof of the chemical recurrence conjecture in two
dimensions*.

The surrounding project prose announces a complete two-dimensional proof and
glosses it as covering weakly reversible stochastic reaction networks with two
species for arbitrary rates.  However:

- the page itself classifies the work as in preparation;
- no paper, DOI, theorem number, or proof is linked;
- the exact-title arXiv search returned no results on 2026-08-12;
- the precise meaning of "two dimensions" cannot be checked from a manuscript.

Consequently this item must not be cited as an established theorem or used to
close a proof branch.  It does create real priority overlap for all T3-2 cases
with at most two dynamic species.  It might also overlap three-species systems
of stoichiometric rank two, depending on the unavailable definition of
dimension.  The genuinely three-dimensional part of T3-2 is the safest
novelty emphasis until that manuscript becomes public and can be compared.

Safe disclosure language for a manuscript is:

> As of 12 August 2026, an independent five-author proof of the
> two-dimensional chemical recurrence conjecture was publicly listed as in
> preparation, but no manuscript was available for comparison.  We therefore
> do not rely on that announcement as a theorem and make no priority claim for
> the overlapping two-dimensional cases.

## 8. Counterexample and scope-risk register

### No located weakly reversible counterexample

The primary-source search located transient, null-recurrent, and explosive
stochastic reaction networks, but none that is both weakly reversible and in
the binary T3-2 class.  This is evidence against an obvious contradiction,
not proof that no counterexample exists.

### Main technical risks to a publication claim

1. **Class-local tier premise.**  Published Anderson--Kim Theorem 9 is global.
   A branch checking only tier sequences in \(\Gamma\) must state and prove the
   restriction corollary.
2. **Projection is not supplied by the literature.**  The paper must prove
   exact conjugacy on \(\Gamma\), including absorption of constant falling-
   factorial factors, deletion of truly inactive linkages, preservation of
   parallel channels, and merging of projected linkages that share a complex.
3. **Recompute graph invariants after projection.**  Linkage number and
   deficiency used in a black-box theorem must be those of the reduced graph.
4. **Pure-multiple hypothesis is literal.**  Anderson--Cappelletti--Kim
   Theorem 4.1 requires \(S\) or \(2S\) for every dynamic species; a mixed
   complex containing \(S\) is insufficient.
5. **Stationary measure versus probability.**  A sigma-finite invariant
   measure does not establish positive recurrence.  Product-form branches
   need normalizability and nonexplosion.
6. **Deterministic stability is insufficient.**  Strong endotacticity and
   stable fluid limits alone admit null, transient, and explosive stochastic
   examples outside weak reversibility.
7. **Rate and orientation quantifiers.**  A headline claim must say that all
   retained reaction channels have arbitrary positive rates and that the
   result is independent of the strongly connected orientation within each
   linkage.  A proof for selected cycles or reversible pairs is narrower.
8. **Finite classes are trivial.**  Novelty language should concern infinite
   closed classes; finite projected classes do not require the new recurrence
   machinery.
9. **In-preparation overlap may move.**  The two-dimensional status should be
   rechecked immediately before submission and again at proof stage.

## 9. Recommended citation and novelty language

For the core citations, use the journal theorem numbers:

- Anderson--Kim (2018), Theorem 9; optionally note "Theorem 4.2 in arXiv v3";
- Anderson--Cappelletti--Kim (2020), Theorems 4.1 and 6.1;
- Anderson--Craciun--Kurtz (2010), Theorems 4.1 and 4.2;
- Anderson--Cappelletti--Koyama--Kurtz (2018), Theorem 3;
- Wiuf--Xu (arXiv v3, 2023), Corollary 4.10;
- Anderson--Cappelletti--Kim--Nguyen (2020), Corollary 7.1 and Theorem 7.2.

A defensible literature paragraph is:

> Published parameter-independent recurrence results cover complex-balanced
> systems, weakly reversible deficiency-zero systems, one-dimensional
> stoichiometric systems, fully open strongly endotactic systems, and certain
> one-linkage binary networks satisfying a pure-multiple or proper-tier
> condition.  We did not locate a posted or refereed theorem that covers every
> weakly reversible binary network after exact fixed-class reduction to at
> most three dynamic species and at most two active linkage classes.  An
> independent two-dimensional proof is publicly announced but was still
> listed as in preparation, with no manuscript available, on 12 August 2026.

Avoid "first," "settles the three-species conjecture," or "the two-dimensional
case was open" unless the search is repeated at submission and the resulting
manuscript's exact rank/species scope is compared with the then-current
two-dimensional work.

## 10. Search boundary and reproducibility

The audit checked the official journal pages and full primary texts for the
three core papers and the complex-balance nonexplosion companion.  It then
searched arXiv and official publisher pages for combinations of
"weakly reversible," "positive recurrence," "chemical recurrence conjecture,"
"three species," "two dimensions," and "two linkage classes," and followed
the primary citation trails through publications posted online by
2026-08-12.  Exact-title and combined-author searches were run for the
announced two-dimensional paper.

A negative literature search is not a mathematical proof of novelty.  The
conclusion here is deliberately phrased as "no posted/refereed source located
in this audit," not as an absolute claim that no overlapping result exists.
