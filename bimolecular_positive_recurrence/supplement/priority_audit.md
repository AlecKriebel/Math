# Narrow literature and priority audit

**Audit date:** 6 August 2026  
**Question searched:** positive recurrence on every closed communicating class for every positive rate vector in a finite **binary/bimolecular weakly reversible network with one linkage class**, without requiring each species to occur in a pure unary or pure double complex.

## Conclusion

No archival paper or current preprint located in this audit proves the exact theorem stated in Version 0.2. The nearest direct predecessor is Anderson, Cappelletti, and Kim (2020), which proves the binary one-linkage case under the additional assumption that, for each species, the complex set contains a multiple of that species. The calibrated positioning is therefore:

> This resolves the binary single-linkage case without the pure-species-complex hypothesis.

This is an evidence-based priority statement, not a claim that an exhaustive search can logically prove absence of all unpublished or unindexed work. The manuscript does not use “first,” “landmark,” or “complete” without scope qualifiers.

## Primary sources

### Anderson and Kim (2018)

David F. Anderson and Jinsu Kim, “Some network conditions for positive recurrence of stochastically modeled reaction networks,” *SIAM Journal on Applied Mathematics* 78 (2018), 2692–2713, DOI `10.1137/17M1161427`.

The paper formulates the positive-recurrence program for weakly reversible stochastic mass-action systems and proves structural sufficient conditions, principally for binary systems. It does not prove the exact theorem of Version 0.2.

### Anderson, Cappelletti, and Kim (2020)

David F. Anderson, Daniele Cappelletti, and Jinsu Kim, “Stochastically modeled weakly reversible reaction networks with a single linkage class,” *Journal of Applied Probability* 57 (2020), 792–810, DOI `10.1017/jpr.2020.28`.

The published abstract states two additional assumptions: the system is binary, and for each species there is a complex that is a multiple of that species. In a binary network, the latter means a unary or pure double complex. Version 0.2 retains binary molecularity and one linkage class while removing this second assumption.

The 2020 paper’s method studies an \(n\)-step embedded chain. Version 0.2 instead marks the actual target channel, uses a residual log-factorial potential, propagates terminal rarity along a fixed target-following path, and obtains terminal rarity by an exhaustive logarithmic top-complex alternative.

### Anderson and Kurtz (2015)

David F. Anderson and Thomas G. Kurtz, *Stochastic Analysis of Biochemical Systems*, Springer, 2015, DOI `10.1007/978-3-319-16895-1`.

This is used for standard stochastic-reaction-network and CTMC background. The final paper nevertheless proves its embedded-chain-to-CTMC and nonexplosion conversion directly.

### Xu (2026 revision)

Chuang Xu, “On the Regulary of Reaction Systems,” arXiv:`2409.05340`, version 2, 9 May 2026.

The paper proves regularity/nonexplosion for every bimolecular weakly reversible stochastic mass-action system. Its introduction explicitly says that the bimolecular positive-recurrence case had not been closed and distinguishes nonexplosion from positive recurrence. This is consistent with the novelty position of Version 0.2 and also confirms that a nonexplosion theorem alone does not settle the present result.

## Later and neighboring work checked

The audit additionally checked:

- Anderson, Cappelletti, Fan, and Kim (2025), “A New Path Method for Exponential Ergodicity of Markov Processes on \(\mathbb Z^d\), with Applications to Stochastic Reaction Networks,” DOI `10.1137/24M1665933`;
- Xu (2026), “Exponential ergodicity of first order endotactic stochastic reaction systems,” arXiv:`2601.00176`;
- Wiuf and Xu (2023), “Classification and threshold dynamics of stochastic reaction networks,” DOI `10.1017/apr.2022.20`;
- works on product-form stationary distributions, strongly endotactic networks, mixing times, and reaction-network translations that cite the 2018 or 2020 papers;
- citation lists and exact-phrase searches for the marked-target factorial identity, target-following paths, and the unrestricted binary one-linkage statement.

These works concern stronger rates under additional Lyapunov hypotheses, first-order or one-dimensional systems, product forms, other structural classes, or general ergodicity tools. None located source states the exact theorem or uses the target-augmented residual factorial mechanism.

## Exact comparison

| Topic | Nearest prior status | Version 0.2 |
|---|---|---|
| Weakly reversible | Required | Required |
| Linkage classes | One | One |
| Maximum molecularity | Two | Two |
| Positive rates | Arbitrary | Arbitrary |
| Closed communicating classes | Covered | Covered |
| Each species in \(S_i\) or \(2S_i\) | Required in 2020 | Not required |
| Boundary/lattice classes | Class-wise | Class-wise |
| Multiple linkage classes | Not resolved by this comparison | Not claimed |
| Molecularity above two | Not resolved | Not claimed |
| Full Anderson–Kim conjecture | Open | Not claimed |

## Proof-mechanism search

Searches were run for combinations of:

- target-augmented or marked-target stochastic reaction chain;
- residual factorial/log-factorial potential;
- \(\log((x)_t/(x)_s)\) source/target identity;
- target-following reaction paths and random-time drift;
- binary single-linkage positive recurrence without pure-species complexes.

No prior source with this mechanism was located.

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
