# Claims ledger

| ID | Claim | Status |
|---|---|---|
| C01 | A fan on a path with spoke positions \(X\) has cycle-length set \(\Delta(X)+2\). | PROVED |
| C02 | The protected construction gives \(h(2M)\ge2^{M-3k-1}S_k\). | PROVED |
| C03 | \(S_{m+1}\ge8S_m\). | PROVED |
| C04 | \(S_{m+1}\ge8S_m+2E_m\) for the defined union-shadow gain. | PROVED |
| C05 | \(S_k=10,102,1020,9906,93198,854156,7674138\) for \(1\le k\le7\). | EXACTLY VERIFIED BY `src/signature_counts.py` |
| C06 | \(E_m=7,67,508,4082,30527,234374,1698857\) for \(1\le m\le7\). | EXACTLY VERIFIED BY `src/signature_counts.py` |
| C07 | For \(1\le m\le7\), the trace totals are \(2,12,94,710,4986,35594,254496\). | EXACTLY VERIFIED BY `src/signature_counts.py` |
| C08 | The trace total is \(\gg8^m/m\). | CONJECTURAL |
| C09 | The sharp bound \(Q_m\le mW_m\) holds. | REFUTED AT \(m=8\) |
| C10 | \(S_m/8^m\to\infty\). | CONJECTURAL |
| C11 | The program solves Erdős Problem 84. | NOT ESTABLISHED |
| C12 | The weaker averaged bound \(Q_m=O(mW_m)\) holds. | EMPIRICALLY IMPLAUSIBLE: \(Q_m/W_m=8.28,15.58,30.39\) FOR \(m=8,9,10\) |
| C13 | The Boolean down-set inequality (D) in `proofs/SHADOW_PROGRAM.md` holds. | EXACTLY VERIFIED THROUGH \(m=10\); UNPROVED |
| C14 | The restricted distinct count satisfies \(D_m\gg8^m/m\). | CONJECTURAL; SMALL-CASE SUPPORT BUT LARGER DIAGNOSTICS DECLINE |
| C15 | \(mE_m\ge S_m\) for all sufficiently large \(m\). | EXACTLY VERIFIED FOR \(2\le m\le10\); UNPROVED |
| C16 | The complementary-rank inequality (R) in `proofs/SHADOW_PROGRAM.md` holds for \(m\ge5\). | REFUTED AT \(m=9,k=9\) |
| C17 | Low alternating-defect parameters have total \(S_m\)-mass \(o(8^m)\). | PROVED BY ENTROPY COUNTING |
| C18 | The orbit-boundary inequality (O) holds with \(c=1/2\). | REFUTED AT \(m=10\) |
| C19 | The generator and shadow system has the ordered Toeplitz-row form (T1)--(T2). | PROVED BY REWRITING DEFINITIONS |
| C20 | The down-set total \(H_m\) is coordinatewise nondecreasing. | EXACTLY VERIFIED THROUGH \(m=10\); CONJECTURAL IN GENERAL |
| C21 | The safe/unsafe deletion identity (DC) in `proofs/SHADOW_PROGRAM.md` holds. | PROVED BY PARTITIONING ON THE \(-m\) COORDINATE |
| C22 | Every rotation/complement orbit has total excess at least half its number of distinct elements. | PROVED |
| C23 | \(g_m(P)\ge0\) whenever \(V(P)\) contains no reflected pair. | REFUTED AT \(m=10\), \(P=[10]\) |
| C24 | Under the reindexing (C1)--(C2), cyclic shifts align Toeplitz row parts but shift both fixed markers. | PROVED BY DIRECT REINDEXING |
| C25 | The four-run orbit values listed in `proofs/APERIODIC_ORBIT_PROGRAM.md` are exact. | EXACTLY VERIFIED BY `src/targeted_orbit.cpp`; THEIR ASYMPTOTIC INTERPRETATION IS CONJECTURAL |
| C26 | The additive orbit defect bound (AD) holds. | PROVED |
| C27 | The empty/full orbit satisfies \(\Lambda>m/12\). | PROVED |
| C28 | The orbit-boundary inequality (O) holds for some fixed \(c>0\). | CONJECTURAL; FOUR-RUN DATA SUGGEST \(\Lambda\asymp1/m\) AND MAY REFUTE IT |

No numerical observation may be promoted without updating this ledger and
recording its verifier.
