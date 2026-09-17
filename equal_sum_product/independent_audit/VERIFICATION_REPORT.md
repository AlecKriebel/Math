# Independent verification report

Date: 17 September 2026 UTC. Mathematical and computational verification: **100% complete**.
Publication and deployment are tracked separately in `../RESEARCH_LOG.md`.

**Verdict: correct.** The supplied nonexistence theorem and stronger ordinary-SP
inequality have complete elementary proofs. All numerical controls and stated
computational scopes were independently checked and reproduced. No mathematical
gap or substantive correction was found.

## Exact result

For a finite matrix of globally distinct positive integers with m >= 3 rows,
common row sum S, and common column product P, the note proves mS/P < 2.
Consequently S=P is impossible. For n >= 2 columns the one-row case is also
impossible, and the supplied two-row construction works with S=P=840. Thus the
DeVincentis equal-value conjecture is true in the original problem's domain.
The 1-by-1 case is excluded from the “only two rows” formulation.

The main proof selects three rows, uses each omitted integer factor >= 1,
bounds pairwise reciprocal products by reciprocal squares, and uses global
distinctness to bound their sum by 2-1/M < 2. The selected row sums require the
same quantity to be at least 3, a contradiction. The stronger proposition
uses two cyclic neighbors per row and counts every reciprocal square exactly
once. Neither proof relies on finite computation.

## Review families and independence

| Review | Mechanism and evidence | Outcome and remaining gap |
|---|---|---|
| [Direct proof referee](proof_referee.md) | Reconstructed every inequality, cyclic index count, and boundary; independent rational checks | Both proofs correct; no mathematical gap |
| [Alternative/adversarial referee](alternate_referee.md) | Derived an all-row AM–GM argument before reading the proof; also a separate two-column pigeonhole argument | Independently establishes mS/P <= sum a_ij^(-(m-1)) < 2; no gap |
| [Computation referee](computation_referee.md) | Reviewed all code, certificates, counts, original integrity, and full reproduction; independently implemented checks | All arithmetic and implementation checks passed; no computational gap |
| Primary-agent review | Checked both proofs and all reports, source definitions, selected-set cardinality variant, original PDF and website transcription | Agrees with approval; publication scope kept explicit |

Reviewers did not read one another's reports before reaching their initial
verdicts. The AM–GM argument independently reaches the same broad reciprocal
bound mechanism, so it is not represented as an unrelated proof family.
The limited pigeonhole route only handles two columns; it is not used to claim
unrestricted nonexistence. All reviews are within an AI-assisted workflow.

## Reproduced evidence

- All 39 entries in the supplied SHA-256 manifest pass. All 40 original files,
  including the manifest, are preserved unchanged; see `IMPORTED_FILES.json`.
- All seven reproduction stages pass under Python 3.14.6 on Darwin arm64.
  All 33 supplied checker tests pass. The exact-audit output matches the supplied
  original output byte for byte.
- The original audit checks the symbolic identity, 64,000 ordered triples,
  4,095 nonempty subsets, 512 telescoping bounds, 360 higher-row arrays comprising
  2,340 columns, and an exact probe using 101-digit integers.
- Added independent checks pass 283,932 comparisons against the matrix
  definition, 200 accepted permutations of the positive control, 19,551 rational
  column inequalities, and all 8,191 nonempty subsets of {1,...,13}.
- A separate degree-bounded polynomial certificate uses the 3-by-3-by-3 grid
  {0,1,2}^3. Degree at most two in each variable makes these exact evaluations
  sufficient to prove the identity by successive polynomial interpolation.
- Every matrix certificate was recomputed. The positive control has row sums
  840, ten column products 840, twenty distinct positive entries, and total
  reciprocal sum exactly 2. Ordinary-SP, repeated-entry, scaling, and corruption
  controls fail precisely the intended equal-value or distinctness conditions.

Checkable artifacts: `computation/independent_checks.py`,
`computation/independent_checks.json`, `computation/original_hash_audit.json`,
`computation/reproduction_console.txt`, and `computation/reproduced_logs/`.
The original tests were run in an isolated copy because they refresh logs.
The temporary copy and PDF preview PNGs are excluded from Git.

## Adversarial boundaries

The proof allows the entry 1, N=1, the m=3 empty product, arbitrary dimensions,
and arbitrarily large integers. It also excludes n=1 when m>=3. Global
distinctness is needed: the 3-by-4 all-2 array has sum=product=8. The proof does
not extend to arbitrary positive real entries, where omitted factors could be
less than one. Two rows legitimately obey a reciprocal rather than a
reciprocal-square identity. Scaling does not preserve sum/product equality in
general, since sums scale by c and products by c^m.

The audit's cardinality bound for k distinct entries is valid: sorting them
gives a_i >= i, hence sum 1/a_i^2 <= sum_(i=1)^k 1/i^2 <= 2-1/k. This is not
an illicit substitution of the count for the largest entry.

The only observed typo is a source comment describing 10^100+{3,7,11} as
100-digit numbers. They have 101 digits, as the note and outputs correctly
state. Original bytes were retained; no mathematical repair is necessary.

## Source, scope, and priority

The [November 2002 primary source](https://erich-friedman.github.io/mathmagic/1102.html)
was opened during this audit. It defines SP matrices by globally distinct
positive integers, equal row sums, and equal column products; it attributes
the equality-case conjecture and two-row construction to Joseph DeVincentis.
The [unsolved list, item 8](https://erich-friedman.github.io/mathmagic/unsolved.html)
continued to display that conjecture on 17 September 2026 UTC.

Additional searches used the queries “sum-product matrices” “conjecture”,
“DeVincentis” “reciprocal” matrices, “sum product” “matrices” “row sums”
“column products” proof, “DeVincentis” “matrices” “proof”,
“sum-product matrices” “squares”, and “sum-product matrices” “two rows”.
No earlier resolution was found in the inspected results. This is a limited
search, not an exhaustive claim to historical priority.

The theorem does not solve all minimum-entry or dimension questions on the
original page, classify all two-row solutions, or independently prove that 840
is the smallest possible common value. The publication does not claim these.
No external correspondence, human peer review, or proof-assistant verification
was performed. The original package's historical statements of unpublished
status remain dated provenance, not descriptions of the later public release.

## Artifact presentation

All three pages of the original PDF were rendered and visually inspected;
the displayed formulas and prose agree with its TeX source and are legible.
The website includes the full main proof, the stronger cyclic inequality,
boundary cases, reproducibility links, and explicit scope/priority statements.
The website PDF is a byte-for-byte copy of the supplied PDF. Website integration
and public deployment evidence are recorded in the publication research log.
