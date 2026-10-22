# Equal power-equation counts do not detect the solvable radical

## Disposition

**Kourovka Notebook 21.134 (UnsolvedMath ID 2643): already resolved in the literature, both parts negatively. Research-attempt turns: 0/5.**

The October 2026 Notebook explicitly records the prior resolution and credits J. G. Thompson. This package is an attributed source certificate, not a new solution or a claim of independent discovery.

Thompson's pair, in the ATLAS notation used by Yu Li and Wujie Shi, is

\[
H=L_3(4):2_2,\qquad G=2^4:A_7.
\]

Here the subscript in \(2_2\) distinguishes an outer involution in ATLAS notation; it does **not** mean an elementary abelian group of order four. Both groups have order 40,320. They have equal element-order counts, while their solvable radicals have orders 1 and 16 respectively. Therefore they are not isomorphic, although \(H\) is almost simple.

- [SOURCE_CERTIFICATE.md](SOURCE_CERTIFICATE.md): exact target, primary sources, published count data, and the deductions settling both parts
- [verify_counts.py](verify_counts.py): transparent arithmetic checks on the published table
- [verification.json](verification.json): reproducible output
- [RESEARCH_LOG.md](RESEARCH_LOG.md): dated source-check log and turn accounting
- [status.json](status.json): machine-readable disposition and limits

Run the arithmetic check with `python3 verify_counts.py` from this folder. It reads no network or private inputs. It does not construct either finite group or independently reproduce the published MAGMA enumeration.

This source-checking package was prepared with AI assistance for Alec Kriebel's research queue. The counterexample is credited to Thompson, as recorded by Li–Shi and the Notebook editors. No new mathematical result, formal proof-assistant verification, or human peer review is claimed. An independent review of this package remains pending.
