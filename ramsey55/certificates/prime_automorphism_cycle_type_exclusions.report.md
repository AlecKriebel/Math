# Certified prime-order automorphism cycle-type exclusions

Evidence status: **THREE NEW CERTIFIED CYCLE-TYPE EXCLUSIONS; ALL
PRIME-ORDER TYPES AT LEAST 23 EXCLUDED; CLASSIFICATION INCOMPLETE**

This report concerns hypothetical order-43 graphs containing neither a
5-clique nor an independent 5-set. It does not decide arbitrary order-43
graphs and does not change the bound \(43\le R(5,5)\le46\).

## Exact certificate results

Any permutation of cycle type \(p^c1^{43-pc}\) is conjugate to the canonical
permutation used by the orbit generator. Relabeling preserves the Ramsey
property. The three formulas below therefore encode the complete indicated
cycle types. They use one Boolean variable per edge orbit and contain no
additional symmetry-breaking clauses or degree lemmas.

For every formula, an independently written checker reconstructed the
canonical permutation, all 903 edge assignments to orbits, all
\(\binom{43}{5}=962{,}598\) five-set orbit signatures, the deduplicated
positive and negative clauses, and the metadata.

| cycle type | variables | clauses | CNF SHA-256 | Glucose conflicts |
|---|---:|---:|---|---:|
| \(19^2 1^5\) | 57 | 95,752 | `2ae53ed6f28a776bb72e3d758d740b3ceace08801cf0a6b28088a4a4bb1e5c2f` | 425 |
| \(17^2 1^9\) | 87 | 106,800 | `c945599f5938385d5ffb918e7ce2c2969de2e9a0d7913d6624db0aeea77ad58f` | 1,662 |
| \(11^3 1^{10}\) | 123 | 172,110 | `2ed2f0f830a63912d879b45237c0a1829a1f829c9074c81e67f4aceb1be46b7c` | 52,789 |

Pinned Glucose3 produced an UNSAT DRAT proof for each formula. `drat-trim`
accepted each proof and converted it to LRAT; `lrat-check` independently
accepted each LRAT proof against the same independently matched CNF.

| cycle type | DRAT bytes | DRAT SHA-256 | LRAT bytes | LRAT SHA-256 |
|---|---:|---|---:|---|
| \(19^2 1^5\) | 9,193 | `a16bc8fdb19d4725f478ddb2461c371703d95636eee43198a9a8595910ec4d41` | 600,801 | `7180a54dd25009aca4904fcbf4dd1d7b5ea2c917ce031a19aff51f0bc1f7999c` |
| \(17^2 1^9\) | 57,181 | `297239d06317f031a8e9bd385493feb441f308e99757661e99d66dc1db9c655e` | 854,933 | `387c38f75ebde2c3e7f66a487c97b08082d03afe953bcd930dc8ad93e5f2614a` |
| \(11^3 1^{10}\) | 3,767,339 | `bc2359707733d91ac922b251f474cfe88e6a01af2bd216a3c1dca038425b2475` | 8,014,919 | `20e1cacca12b268ef7a174672ce7acf6f7d7cb5bdbf05737ac5475bd67e07bfa` |

Thus none of the three indicated cycle types can occur.

## Elementary large-prime exclusions

The degree theorem from \(R(4,5)=R(5,4)=25\) gives
\(18\le d(v)\le24\) for every vertex. If \(v\) is fixed by an automorphism
of prime order \(p\), then it sees either all or none of each moved
\(p\)-cycle. Consequently

\[
 d(v)=pm+d_F,
\]

where \(m\) is the number of moved cycles seen by \(v\) and \(d_F\) is its
degree inside the fixed-vertex graph.

For types \(29^1 1^{14}\), \(31^1 1^{12}\), \(37^1 1^6\), and
\(41^1 1^2\), no choice of \(m\) and \(d_F\) lies in \([18,24]\), so each
type is impossible. The same calculation excludes \(13^3 1^4\).

For type \(23^1 1^{20}\), partition the 20 fixed vertices into:

- \(L\), those adjacent to the moved cycle, which have fixed-graph degree
  0 or 1; and
- \(H\), those nonadjacent to the moved cycle, which have fixed-graph
  degree 18 or 19.

Write \(\ell=|L|\). Counting fixed-graph edges between \(L\) and \(H\)
gives

\[
  (20-\ell)(\ell-1)\le e(L,H)\le\ell
\]

for \(\ell\ge1\), with the lower bound interpreted as zero for
\(\ell=0\). The only feasible integer values are
\(\ell\in\{0,1,19,20\}\). Complementation exchanges \(L\) and \(H\), so
it suffices to consider \(\ell=0,1\).

If \(\ell=0\), the complement of the fixed graph has maximum degree one.
Its independence number is at least
\(\lceil20/(1+1)\rceil=10\), so the original fixed graph contains a
10-clique. If \(\ell=1\), the lone low-degree vertex misses at least 18 of
the 19 vertices in \(H\); each such vertex must be adjacent to all other
18 vertices of \(H\), forcing \(H\) to be a 19-clique. Both cases
contradict the absence of a 5-clique. Thus \(23^1 1^{20}\) is impossible.

The already certified circulant exclusion is exactly the remaining
large-prime type \(43^1\). Therefore every prime-order cycle type with
\(p\ge23\) is excluded.

## Exact boundary of the result

For a prime \(p\), every cycle type
\(p^c1^{43-pc}\), \(1\le c\le\lfloor43/p\rfloor\), is a distinct case.
The machine-readable coverage audit enumerates all such cases rather than
silently identifying an automorphism order with one cycle type.

The following types remain uncovered by the certificates and elementary
arguments audited here:

- \(2^c1^{43-2c}\) for \(1\le c\le21\);
- \(3^c1^{43-3c}\) for \(1\le c\le14\);
- \(5^c1^{43-5c}\) for \(1\le c\le8\);
- \(7^c1^{43-7c}\) for \(1\le c\le6\);
- \(11^1 1^{32}\) and \(11^2 1^{21}\);
- \(13^1 1^{30}\);
- \(17^1 1^{26}\);
- \(19^1 1^{24}\).

In particular, this is not a proof that a hypothetical Ramsey graph on 43
vertices is asymmetric.
