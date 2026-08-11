# Version 1.1 primary-source literature and metadata audit

**Audit date:** 10 August 2026  
**Scope:** state-space closure citation; Anderson--Cappelletti--Kim (2020)
proof comparison and Example 4.1; MSC 2020; Xu arXiv metadata; the announced
two-species result; and every entry in `manuscript/references.bib`.  
**Source rule:** publisher records, the authors' or repositories' article
copies, official arXiv records, the official MSC 2020 database, and official
conference/project pages. No external contact was made.

## Audit conclusion

The proposed Version 1.1 literature corrections are supported by the primary
sources. In particular:

- weak reversibility makes reachability symmetric at the population-state
  level; this is recorded in the discrete-reaction-network literature and the
  manuscript's elementary lifted-cycle proof is appropriate;
- the requested dependency map for Section 6 of Anderson, Cappelletti, and
  Kim is exact;
- their pure-species assumption first supplies either $S_v$ or $2S_v$,
  but $2S_v$ is then excluded by D-tier maximality, so it is $S_v$ whose
  source propensity supplies the final comparison;
- their Example 4.1 is exactly the five-edge cycle and positive unshifted
  drift stated below;
- arXiv still displays Xu's title as *On the Regulary of Reaction Systems*,
  with Version 2 as the current version;
- the ConStRAINeD page still lists the five-author two-dimensional proof as
  in preparation, although it describes the proof as complete; and
- the requested MSC order and descriptions agree with MSC 2020.

No literature-positioning defect requiring withdrawal of the submission
candidate was found. This audit does not certify any new calculation proposed
for the carried-target treatment of ACK Example 4.1; that calculation should
appear only if its separate exact symbolic verification succeeds.

## 1. Anderson--Cappelletti--Kim (2020): exact Section 6 dependency

### Sources checked

1. David F. Anderson, Daniele Cappelletti, and Jinsu Kim,
   *Stochastically modeled weakly reversible reaction networks with a single
   linkage class*, Journal of Applied Probability 57(3), 792--810 (2020),
   DOI <https://doi.org/10.1017/jpr.2020.28>.
2. The official arXiv record and Version 2 PDF, last revised 16 January 2020:
   <https://arxiv.org/abs/1904.08967> and
   <https://arxiv.org/pdf/1904.08967v2>.
3. The publisher record:
   <https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/stochastically-modeled-weakly-reversible-reaction-networks-with-a-single-linkage-class/5E9F7DAE999525F8D4A3392F80B3F0C9>.

The internal theorem, lemma, equation, and section numbers below agree with
the official arXiv Version 2 and the published citation. Journal page-number
locators are deliberately unnecessary.

### Exact dependency map

| ACK location | Exact role |
|---|---|
| Theorem 6.1 | Reduces positive recurrence to inclusion (11): every top S-tier source lies in the top D-tier along every proper tier sequence. |
| Lemma 6.3(i) | Gives a uniform upper bound for each fixed reaction-word contribution. |
| Lemma 6.3(ii) | If the reaction word lies in the top S-tier and has a strict D-tier descent, its path-probability-weighted Lyapunov contribution tends to $-\infty$. |
| Lemma 6.4 | Sums the finitely many $k$-step reaction-word contributions: all are bounded above and one tends to $-\infty$, contradicting failure of the sampled-chain Foster drift. |
| Lemma 6.5 | Uses weak reversibility, one linkage class, and (11) to construct a reaction word of length $r=|\mathcal R|$ satisfying the hypotheses of Lemma 6.4. |
| Proof of Theorem 6.1 | Applies Lemma 6.5 and then Lemma 6.4 with $k=r$, treating an absorbing initial state separately. |
| Section 6.1, equations (19)--(20) | Verifies (11) from binary structure and the pure-species-complex condition; this is where that extra condition is used. |

The order matters. Lemma 6.5 constructs the finite word. Lemma 6.3(ii)
provides the term tending to minus infinity. Lemma 6.4 assembles those facts
into the sampled-chain argument.

### The $S_v$ versus $2S_v$ point

In the hard case of Section 6.1, a D-top complex $y^{**}$ is disabled:

\[
  \lambda_{y^{**}}(x_n)=0 \tag{19}
\]

while its D-monomial diverges:

\[
  (x_n\vee1)^{y^{**}}\longrightarrow\infty. \tag{20}
\]

Binary structure forces, after relabeling,

\[
  y^{**}=S_u+S_v,\qquad x_{n,u}=0,\qquad x_{n,v}\to\infty.
\]

The additional ACK hypothesis supplies $S_v\in\mathcal C$ or
$2S_v\in\mathcal C$, or both. If $2S_v\in\mathcal C$, then

\[
 \frac{(x_n\vee1)^{S_u+S_v}}{(x_n\vee1)^{2S_v}}
 =\frac{x_{n,v}}{x_{n,v}^2}\longrightarrow0,
\]

so $2S_v\succ_D y^{**}$, contradicting D-tier maximality of $y^{**}$.
Therefore $2S_v\notin\mathcal C$ in this case, and the hypothesis forces
$S_v\in\mathcal C$. Its enabled source propensity satisfies

\[
 \lambda_{S_v}(x_n)=x_{n,v}=(x_n\vee1)^{y^{**}},
\]

which supplies the source-rate comparison used to establish (11).

The accurate summary is therefore:

> The assumption forces $S_v$ to be a complex, after $2S_v$ is excluded
> by D-tier maximality; $S_v$ then supplies the source-rate comparison.

It is inaccurate to say that “$S_v$ or $2S_v$ supplies the comparison.”
The source also does not characterize the hypothesis as an artifact, so the
revised manuscript should not do so.

### Exact recommended replacement paragraph

> Anderson, Cappelletti, and Kim proved positive recurrence for weakly
> reversible binary networks with one linkage class under the additional
> condition that, for every species $S_i$, at least one of $S_i$ and
> $2S_i$ is a complex. Their Theorem 6.1 reduces positive recurrence to the
> tier inclusion (11). Lemma 6.5 constructs the finite reaction word, Lemma
> 6.3(ii) converts its strict D-tier descent into a negative contribution
> tending to minus infinity, and Lemma 6.4 assembles these ingredients into
> the sampled-chain argument. In Section 6.1, equations (19)--(20), the
> additional assumption first supplies $S_v$ or $2S_v$. D-tier maximality
> excludes $2S_v$, so $S_v$ is forced, and its source propensity supplies
> the required comparison. The present marked-target argument replaces that
> boundary comparison without requiring a pure unary or pure-double complex
> for every species.

Use a locator of the form

```tex
\citep[Section~6; Theorem~6.1; Lemmas~6.3--6.5;
Section~6.1, equations~(19)--(20)]{AndersonCappellettiKim2020}
```

and omit journal page-number locators.

### Special-case claim after the closure lemma

The stronger statement remains exact:

> The present theorem contains the binary one-linkage positive-recurrence
> theorem of Anderson, Cappelletti, and Kim as a special case.

Reason: their assumptions are weak reversibility, one linkage class,
bimolecularity, and the additional pure-complex condition. The new theorem
keeps the first three and drops only the fourth. For every initial state,
weak reversibility makes its reachable population set a closed communicating
class. A nonabsorbing class is therefore covered by the positive-recurrence
conclusion, and an absorbing initial state gives the point-mass case, exactly
as in their proof of Theorem 6.1. “Contains their positive-recurrence
conclusion as a special case” is also correct but unnecessarily weaker.

## 2. ACK Example 4.1

The primary source gives the directed cycle

\[
 A\xrightarrow{\kappa_1}A+B
 \xrightarrow{\kappa_2}A+C
 \xrightarrow{\kappa_3}C
 \xrightarrow{\kappa_4}2B
 \xrightarrow{\kappa_5}A.
\]

It takes $x_0=(1,0,0)$ and $x_n=(n,1,0)$, explicitly noting that
$x_n$ is reachable from $x_0$ through sequential occurrences of reactions
1 and 5. For the unshifted entropy-like function $V$ in their equation (8),
the generator is exactly

\[
 \mathcal A V(x_n)=\kappa_1 n(2\log2-1)\longrightarrow+\infty.
\]

Thus the directive's reproduction of the example and the claimed failure of
the one-step unshifted drift are exact. The primary source does not supply the
new marked-target episode calculation. Any claim of
$-\alpha\log n+O(1)$ must therefore rest on the separate symbolic derivation
and deterministic test required by the revision directive.

## 3. Prior citation for symmetric population reachability

The appropriate archival citation is:

> Loïc Paulevé, Gheorghe Craciun, and Heinz Koeppl, “Dynamical Properties of
> Discrete Reaction Networks,” *Journal of Mathematical Biology* 69(1),
> 55--72 (2014), DOI
> <https://doi.org/10.1007/s00285-013-0686-2>.

Primary accessible record:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC3835780/>.

Their Definition 1.4 calls a discrete reaction network *recurrent* when
$x\to^*x'$ implies $x'\to^*x$. Lemma 4.5 reduces this to reversing each
single reaction from its post-reaction population, and Lemma 4.6 concludes
that every weakly reversible reaction network is recurrent. The proof is the
same residual-population lift used in the proposed lemma. The article's
discussion also identifies the transition graph with the stochastic
mass-action reachability graph when every enabled channel has positive rate.

Recommended sentence:

> This reversible-reachability property is also recorded as recurrence of the
> underlying discrete reaction network by
> \citet[Definition~1.4 and Lemmas~4.5--4.6]{PauleveCraciunKoeppl2014}; the
> elementary lifting proof is included to distinguish this combinatorial use
> of “recurrence” from positive recurrence of the continuous-time Markov
> chain.

This citation supports the closure strengthening without suggesting that the
paper's positive-recurrence theorem was already known. The property requires
weak reversibility but neither one linkage class nor bimolecularity.

## 4. MSC 2020

The official MSC 2020 database is
<https://mathscinet.ams.org/mathscinet/msc/msc2020.html>. It gives:

- **60J27:** Continuous-time Markov processes on discrete state spaces;
- **60J28:** Applications of continuous-time Markov processes on discrete
  state spaces;
- **60J74:** Jump processes on discrete state spaces;
- **92C42:** Systems biology, networks;
- **37N25:** Dynamical systems in biology [see also 92-XX].

Recommended ordering:

> **Primary:** 60J27.  
> **Secondary:** 60J28, 60J74, 92C42.

Code 37N25 remains a valid MSC 2020 code, but it is less specific to this
discrete-state CTMC theorem and is redundant with 92C42. Dropping it produces
the cleanest classification. Retaining it as a final secondary code would not
be factually wrong.

## 5. Xu arXiv record

The official record checked on 10 August 2026 is
<https://arxiv.org/abs/2409.05340>:

- author: Chuang Xu;
- displayed title: *On the Regulary of Reaction Systems*;
- current version: arXiv:2409.05340v2 [q-bio.MN], revised 9 May 2026;
- cross-list: math.PR;
- arXiv DOI: <https://doi.org/10.48550/arXiv.2409.05340>.

No version later than v2 and no title correction were displayed on the audit
date. The bibliography should reproduce the official title and explicitly
mark the displayed word:

> Title as displayed on arXiv; “Regulary” [sic]. Version 2, revised 9 May
> 2026.

Xu proves regularity in the stochastic and deterministic senses for every
second-order endotactic mass-action system and, as a consequence, every
bimolecular weakly reversible mass-action system. For the CTMC this is a
nonexplosion result. The accurate comparison is:

> Nonexplosion is known for the broader bimolecular weakly reversible class
> by Xu. The present proof recovers nonexplosion for its one-linkage subclass
> but contributes positive recurrence.

## 6. Agazzi and the ConStRAINeD announcement

Official sources checked:

- University of Geneva conference program, talk on 10 June 2022:
  <https://www.unige.ch/jpe75conference/program.html>;
- SIAM AG25 official abstract book, abstract MS111:
  <https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf>;
- ConStRAINeD results page, accessed 10 August 2026:
  <https://constrained.polito.it/publications/>.

The 2022 program announces the two-dimensional positive-recurrence result as
joint work of Andrea Agazzi, Jonathan C. Mattingly, David F. Anderson, and
Daniele Cappelletti. The 2025 abstract states the positive-recurrence result
but does not supply a coauthor list. The current ConStRAINeD page supplies the
five-author list---Andrea Agazzi, David F. Anderson, Daniele Cappelletti,
Lucie Laurence, and Jonathan C. Mattingly---and item 16 lists *A proof of
the chemical recurrence conjecture in two dimensions* as **in preparation**.
The page's exposition describes the proof as complete.

An official-domain/arXiv search did not locate a public manuscript on the
audit date. The calibrated wording is:

> The ConStRAINeD project page lists a five-author proof of the chemical
> recurrence conjecture in two dimensions as in preparation. We did not
> locate a public manuscript as of 10 August 2026. The announced result covers
> two species with broader network structure, whereas the present theorem
> allows an arbitrary finite number of species but assumes bimolecularity and
> one linkage class. The results are complementary; neither supersedes the
> other on the public evidence presently available.

Do not write that no manuscript exists, and do not attribute the five-author
list to either conference abstract.

## 7. Bibliography metadata audit

The DOI-bearing items were checked against their publisher records and DOI
metadata; arXiv and event/project items were checked against their official
records. Fields currently in `manuscript/references.bib` agree as follows.

| BibTeX key | Primary record checked | Result |
|---|---|---|
| `AndersonKim2018` | DOI 10.1137/17M1161427, SIAM J. Appl. Math. 78(5), 2692--2713 | Authors, title, year, volume, issue, pages, DOI verified. |
| `AndersonCappellettiKim2020` | DOI 10.1017/jpr.2020.28, J. Appl. Probab. 57(3), 792--810 | Authors, title, year, volume, issue, pages, DOI verified. |
| `AndersonKurtz2015` | Springer DOI 10.1007/978-3-319-16895-1 | Authors, title, series, Springer Cham, year, DOI verified. |
| `AndersonCraciunKurtz2010` | DOI 10.1007/s11538-010-9517-4 | Authors, title, Bull. Math. Biol. 72(8), 1947--1970 verified. |
| `AndersonCappellettiKimNguyen2020` | DOI 10.1016/j.spa.2020.07.012 | Published archival metadata, including SPA 130(12), 7218--7259, verified. |
| `AndersonCappellettiFanKim2025` | DOI 10.1137/24M1665933 | Authors, title, SIAM J. Appl. Dyn. Syst. 24(2), 1668--1710 verified; `{Markov}`, the displayed math, and the CRN phrase are case-protected. |
| `WiufXu2023` | arXiv:2012.07954v3, 24 January 2023 | Authors, title, current version and category verified; no archival journal publication was located. |
| `Xu2026` | arXiv:2409.05340v2 | Official displayed title, author, version date, category, URL, and arXiv DOI verified; `[sic]` note added. |
| `Agazzi2022Talk` | Official University of Geneva program | Speaker, title, date, venue, and four-person joint-work statement verified. |
| `Agazzi2025Talk` | Official SIAM AG25 abstract book, MS111 | Speaker, title, meeting dates and abstract locator verified. |
| `ConStRAINeDResults` | Official project results page | Corporate source, title, item 16 status, URL, and 10 August 2026 access date verified. |
| `HornJackson1972` | DOI 10.1007/BF00251225 | Authors, title, Arch. Ration. Mech. Anal. 47(2), 81--116 verified. |
| `AndersonCraciunGopalkrishnanWiuf2015` | DOI 10.1007/s11538-015-0102-8 | Authors, title, Bull. Math. Biol. 77(9), 1744--1767 verified. |
| `AndersonCappellettiKoyamaKurtz2018` | DOI 10.1007/s11538-018-0473-8 | Authors, title, Bull. Math. Biol. 80(10), 2561--2579 verified. |
| `Anderson2011Boundedness` | DOI 10.1007/s10910-011-9886-4 | Author, title, J. Math. Chem. 49(10), 2275--2290 verified. |
| `BorosHofbauer2020` | DOI 10.1137/19M1248431 | Authors, accents, title, SIAM J. Appl. Dyn. Syst. 19(1), 352--365 verified. |
| `PauleveCraciunKoeppl2014` | DOI 10.1007/s00285-013-0686-2 | Added; authors, accents, title, J. Math. Biol. 69(1), 55--72 verified. |
| `Norris1997` | Cambridge DOI 10.1017/CBO9780511810633 | Author, book title, series number 2, publisher, year, ISBN and DOI verified. |
| `MeynTweedie2009` | Cambridge DOI 10.1017/CBO9780511626630 | Authors, second edition, publisher, year, ISBN and DOI verified. |
| `Asmussen2003` | Springer DOI 10.1007/b97236 | Author, title, second edition, series volume 51, Springer New York, year, ISBN and DOI verified. |

### Bibliography edits made in Version 1.1

1. Added `PauleveCraciunKoeppl2014` for the state-cycle/closed-reachability
   lemma.
2. Added the literal `[sic]` and version explanation to `Xu2026` without
   changing the official title.
3. Updated the ConStRAINeD access date to 10 August 2026.
4. Protected `{Markov}` and `{Stochastic Reaction Networks}` in the 2025 SIAM
   title while retaining the protected $\mathbb Z^d$ expression.

No DOI, author-list, journal, volume, issue, or page correction was otherwise
required.
