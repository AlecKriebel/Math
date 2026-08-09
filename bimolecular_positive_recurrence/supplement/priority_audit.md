# Narrow literature and priority audit

**Audit date:** 9 August 2026
**Question searched:** positive recurrence on every closed communicating class for every positive rate vector in a finite **binary/bimolecular weakly reversible network with one linkage class**, without requiring each species to occur in a pure unary or pure double complex.

## Conclusion

No archival paper or publicly available preprint located in this audit proves the exact arbitrary-dimensional theorem stated in Version 0.3. The nearest direct published predecessor is Anderson, Cappelletti, and Kim (2020), which proves the binary one-linkage case under the additional assumption that, for each species, the complex set contains a multiple of that species. A complementary theorem for weakly reversible networks with **two species** has been publicly announced and is listed as in preparation, but no manuscript was publicly available on the audit date. The calibrated positioning is therefore:

> This resolves the binary single-linkage case without the pure-species-complex hypothesis.

This is an evidence-based priority statement, not a claim that a search can prove the absence of all unpublished or unindexed work. The manuscript does not use “first,” “landmark,” or “complete” without scope qualifiers. The announced two-species result and Version 0.3 address complementary parameter regimes: the announced result allows broader network structure in two species, while Version 0.3 allows an arbitrary finite number of species under binary molecularity and one linkage class. Their scopes overlap in the two-species binary single-linkage case.

## Primary sources

### Anderson and Kim (2018)

David F. Anderson and Jinsu Kim, “Some network conditions for positive recurrence of stochastically modeled reaction networks,” *SIAM Journal on Applied Mathematics* 78 (2018), 2692–2713, DOI `10.1137/17M1161427`.

The paper formulates the positive-recurrence program for weakly reversible stochastic mass-action systems and proves structural sufficient conditions, principally for binary systems. It does not prove the exact theorem of Version 0.3.

### Anderson, Cappelletti, and Kim (2020)

David F. Anderson, Daniele Cappelletti, and Jinsu Kim, “Stochastically modeled weakly reversible reaction networks with a single linkage class,” *Journal of Applied Probability* 57 (2020), 792–810, DOI `10.1017/jpr.2020.28`.

The published abstract states two additional assumptions: the system is binary, and for each species there is a complex that is a multiple of that species. In a binary network, the latter means a unary or pure double complex. Version 0.3 retains binary molecularity and one linkage class while removing this second assumption.

The 2020 paper’s method studies an \(n\)-step embedded chain. Version 0.3 instead marks the actual target channel, uses a residual log-factorial potential, propagates terminal rarity along a fixed target-following path, and obtains terminal rarity by an exhaustive logarithmic top-complex alternative.

### Anderson and Kurtz (2015)

David F. Anderson and Thomas G. Kurtz, *Stochastic Analysis of Biochemical Systems*, Springer, 2015, DOI `10.1007/978-3-319-16895-1`.

This is used for standard stochastic-reaction-network and CTMC background. The final paper nevertheless proves its embedded-chain-to-CTMC and nonexplosion conversion directly.

### Xu (2026 revision)

Chuang Xu, “On the Regulary of Reaction Systems,” arXiv:`2409.05340`, version 2, 9 May 2026.

Public record: <https://arxiv.org/abs/2409.05340>.

The paper proves regularity/nonexplosion for every bimolecular weakly reversible stochastic mass-action system. Its introduction explicitly says that the bimolecular positive-recurrence case had not been closed and distinguishes nonexplosion from positive recurrence. This is consistent with the novelty position of Version 0.3 and also confirms that a nonexplosion theorem alone does not settle the present result.

### Announced two-species theorem (2022-present)

The theorem was publicly announced by 2022.  The official program for the
Jean-Pierre Eckmann 75 Conference at the University of Geneva lists Andrea
Agazzi’s 10 June 2022 talk “Weakly reversible chemical reaction networks are
recurrent in 2d,” states that the conjecture is answered affirmatively in two
dimensions, and names Jonathan C. Mattingly, David F. Anderson, and Daniele
Cappelletti as collaborators:
<https://www.unige.ch/jpe75conference/program.html>.  Cappelletti's official
staff page also records recurrence talks in June 2022 and February, March, and
June 2023: <https://staff.polito.it/daniele.cappelletti/tags/recurrence/>.

Agazzi’s later abstract with the same title, presented at the July 2025 SIAM
Conference on Applied Algebraic Geometry, announces positive recurrence for
continuous-time Markov chains arising from weakly reversible mass-action
networks. The abstract is publicly available on page 79 of the conference
abstract book:
<https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf>.

The ConStRAINeD project’s current results page describes this as a proof of the chemical recurrence conjecture in dimension two and lists the in-preparation work as:

> A. Agazzi, D. F. Anderson, D. Cappelletti, L. Laurence, J. C. Mattingly, “A proof of the chemical recurrence conjecture in two dimensions.”

Public project record: <https://constrained.polito.it/publications/>.

No paper or preprint for this announced result was located as of 9 August 2026. It is therefore recorded as a material public priority fact, not treated as an archival theorem whose hypotheses and proof can be independently compared in full. Based on the public description, it is broader with respect to molecularity and linkage structure but restricted to two species. It neither supplies nor displaces the arbitrary-dimensional binary single-linkage theorem of Version 0.3.

## Later and neighboring work checked

The audit additionally checked:

- Anderson, Cappelletti, Fan, and Kim (2025), “A New Path Method for Exponential Ergodicity of Markov Processes on \(\mathbb Z^d\), with Applications to Stochastic Reaction Networks,” DOI `10.1137/24M1665933`;
- Xu (2026), “Exponential ergodicity of first order endotactic stochastic reaction systems,” arXiv:`2601.00176`;
- Wiuf and Xu (2023), “Classification and threshold dynamics of stochastic reaction networks,” arXiv:`2012.07954v3`;
- works on product-form stationary distributions, strongly endotactic networks, mixing times, and reaction-network translations that cite the 2018 or 2020 papers;
- citation lists and exact-phrase searches for the marked-target factorial identity, target-following paths, and the unrestricted binary one-linkage statement.

Apart from the announced two-species result recorded separately above, these works concern stronger rates under additional Lyapunov hypotheses, first-order or one-dimensional systems, product forms, other structural classes, or general ergodicity tools. No located archival paper or public preprint states the exact arbitrary-dimensional theorem or uses the target-augmented residual factorial mechanism.

## Exact comparison

| Topic | Nearest published status | Announced two-species result | Version 0.3 |
|---|---|---|---|
| Weakly reversible | Required | Required | Required |
| Number of species | Arbitrary finite | Two | Arbitrary finite |
| Linkage classes | One | Apparently unrestricted | One |
| Maximum molecularity | Two | Apparently unrestricted | Two |
| Positive rates | Arbitrary | Arbitrary | Arbitrary |
| Closed communicating classes | Covered | Public description does not expose full formulation | Covered |
| Each species in \(S_i\) or \(2S_i\) | Required in 2020 | Not indicated | Not required |
| Boundary/lattice classes | Class-wise | Cannot assess without manuscript | Class-wise |
| Public proof available | Yes | No; in preparation | Yes |
| Full arbitrary-dimensional conjecture | Open | Not claimed | Not claimed |

## Proof-mechanism search

Searches were run for combinations of:

- target-augmented or marked-target stochastic reaction chain;
- residual factorial/log-factorial potential;
- \(\log((x)_t/(x)_s)\) source/target identity;
- target-following reaction paths and random-time drift;
- binary single-linkage positive recurrence without pure-species complexes.

No prior public source with this mechanism was located.

## Recommended manuscript wording

Use:

> We prove the binary one-linkage positive-recurrence theorem without the pure-species-complex hypothesis imposed in Anderson, Cappelletti, and Kim (2020).

Or:

> This resolves the binary single-linkage case without the pure-species-complex hypothesis.

Avoid unqualified claims that the full positive-recurrence conjecture is resolved.

## Scope that remains open in this paper

- multiple linkage classes;
- complexes of molecularity three or higher;
- the full positive-recurrence conjecture;
- product-form stationary distributions;
- exponential ergodicity and mixing-time bounds.
