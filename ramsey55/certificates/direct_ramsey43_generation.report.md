# Direct unrestricted \(R(5,5)\) CNF generation

Date: 2026-07-23
Scope: generation and structural/semantic validation only; no SAT solve was
started.

## Result

The deterministic direct \(n=43\) instance was generated successfully.
It is a global edge-variable formulation, not a fixed-core completion:

- 903 primary variables \(x_{ij}\), one for every unordered vertex pair;
- 962,598 five-vertex subsets;
- exactly two 10-literal clauses per five-subset;
- 1,925,196 Ramsey clauses;
- sound degree interval \(18 \leq d(v) \leq 24\);
- 64,500 sequential-counter auxiliary variables;
- 126,936 degree clauses;
- 65,403 variables and 2,052,132 clauses in total;
- 90,311,307 bytes on disk.

Generation took 8.269379 seconds wall time and 5.228663 seconds CPU time.
The generator recorded a peak resident set size of 28,852,224 bytes.  Its
conservative pre-generation file-size ceiling was 141,534,241 bytes, against
16,071,766,016 free bytes.  No global solver was invoked.

Evidence label: **CERTIFIED (encoding identity only)**.  The independent
checker reconstructed all 2,052,132 clauses in order, found no missing or
extra clauses, checked all declared counts, and reproduced the CNF hash in
7.032152 seconds.  This says nothing about whether the formula is SAT or
UNSAT.

## Encoding

Primary variables are ordered by lexicographic unordered vertex pairs:
\((0,1),(0,2),\ldots\).  For every five-set \(S\), with its ten edge variables
\(E(S)\), the clauses are

\[
\bigvee_{e\in E(S)} \neg x_e
\qquad\text{and}\qquad
\bigvee_{e\in E(S)} x_e.
\]

The first forbids a \(K_5\); the second forbids an independent five-set.

The degree bounds use \(R(4,5)=R(5,4)=25\).  For any vertex \(v\), its
neighborhood contains neither a \(K_4\) nor an independent five-set, so
\(d(v)\leq24\).  Its non-neighborhood contains neither a \(K_5\) nor an
independent four-set, so \(n-1-d(v)\leq24\), giving \(d(v)\geq n-25=18\).
The theorem dependency is independently formalized in
[Gauthier--Brown, arXiv:2404.01761](https://arxiv.org/abs/2404.01761).

Each at-most constraint uses forward prefix-threshold variables.  Clauses
force every reached threshold forward and prohibit threshold \(k+1\).
For a primary assignment with at most \(k\) true input literals, assigning
each auxiliary to its exact prefix threshold gives a satisfying extension;
with more than \(k\), forward induction forces the prohibited overflow
variable.  Lower degree bounds are at-most bounds on negated incident-edge
literals.

## Tests and independent check

`tests/direct_ramsey_cnf_tests.py` passed all seven tests:

- edge-variable bijection through order 14;
- exact \(n=43\) counts;
- all 33,868 labeled graphs through order 6 checked exhaustively against a
  direct graph predicate;
- all 382 primary assignments across 50 small production-counter instances,
  with every auxiliary assignment exhaustively considered;
- the same 382-assignment exhaustive audit repeated against the independent
  checker's separate counter implementation;
- exact paired 10-literal clauses at order 5;
- deterministic in-memory generation.

The production artifact was then checked by
`verify/direct_ramsey_cnf_check.py`, which imports none of the generator code
and reconstructs the edge map, five-set clauses, degree bounds, auxiliary
allocation, and counter clauses independently.

Reproduction commands:

```text
python3 tests/direct_ramsey_cnf_tests.py -v
python3 src/direct_ramsey_cnf.py --order 43 --estimate-only
python3 src/direct_ramsey_cnf.py --order 43 \
  --output certificates/direct_ramsey43.cnf \
  --metadata certificates/direct_ramsey43.metadata.json
python3 verify/direct_ramsey_cnf_check.py \
  certificates/direct_ramsey43.cnf --order 43 \
  --output results/verification/direct_ramsey43_cnf_check.json
```

## SHA-256

| Artifact | SHA-256 |
|---|---|
| `src/direct_ramsey_cnf.py` | `97e4ce41b6172702e8a0e7e1bdb3ad58aaed464b1687689cb7eacadebcea2b8c` |
| `verify/direct_ramsey_cnf_check.py` | `99e8d79d9daead363eb99f8bab28d4a7e07610c2b574b5c01f615b7a118e92b0` |
| `tests/direct_ramsey_cnf_tests.py` | `4f450ebb821354b968fcc4b9a76c1fb3b1c8b98f6234d3fb15974d62e65d9bdd` |
| `certificates/direct_ramsey43.cnf` | `141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1` |
| `certificates/direct_ramsey43.metadata.json` | `88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c` |
| `results/verification/direct_ramsey43_cnf_check.json` | `7bf6d5847734d54763099ae59ff186086aaf78d8a75545c65ce5518ab31ad007` |

The report itself is intentionally excluded from its internal hash table; its
hash is reported alongside the handoff.
