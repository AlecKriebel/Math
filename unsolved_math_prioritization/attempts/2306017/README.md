# Function Theory Problem 6.17

**Result: already solved in the literature.** Aharonov, Shapiro and Solynin (1999) resolved the exact prescribed-second-coefficient minimum-area problem; their 2006 Theorem 4 restates the result and credits that paper.

For \(a=|a_2|\), the minimum is \(\pi(1+2a^2)\) when \(0\le a\le1/2\), and \(27\pi/[8(2-a)^2]\) when \(1/2<a<2\).

- [PROOF.md](PROOF.md): the explicit extremal, the typically-real Dirichlet-energy lower bound, and a coefficient comparison using ordinary conformal radius.
- [SOURCE_GATE.md](SOURCE_GATE.md): exact source coverage, the unresolved biangle-source discrepancy, and verification limits.
- [RESEARCH_LOG.md](RESEARCH_LOG.md): the substantive investigation and subsequent correction of its comparison argument.
- [verify_exact.py](verify_exact.py): exact symbolic identities; run with Python and SymPy.
- [verification.json](verification.json): recorded algebra-check results.

The full-class minimum is reconstructed using identified classical theorem inputs. Full-class uniqueness in the nontrivial range is not independently proved here. The original 1999 proof was unavailable; the 2001 and 2006 papers were read as author-posted OCR. The ordinary conformal-radius source was inspected as page images. No new theorem or priority is claimed.

Primary references: [1999](https://doi.org/10.1007/BF02791132), [2006](https://doi.org/10.1007/BF02790271), [Dubinin 1994](https://www.mathnet.ru/eng/rm1153).
