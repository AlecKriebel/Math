# Soundness of the hole7 addition-only recovery

The immutable source proof has SHA-256
`7ceb4a63d393d8ff6fec33569c6284fee61533be4f15fd733777b85b08ee2b85` and contains
284,317 additions and 263,162 deletion
records.  The recovery parser accepted only canonical ASCII DRAT records,
preserved every addition byte-for-byte and in order, and removed exactly the
deletion records.  The resulting proof has SHA-256
`e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9` and contains 284,317 additions,
no deletions, and one final empty clause.

The original wrapper's exit 80 is explained by pinned checker source lines
806--811 and 1409.  In forward mode, DRAT-trim preserves a clause currently
serving as a pseudo-unit reason and ignores a requested deletion; `-W` maps
that ignored optimization instruction to `HARDWARNING=80`.  The first trigger
is source proof line 2375, `d -741 -1 -12 -17 0`, immediately after unit
addition `-741 0`.  A retained verbose diagnostic reproduced exit
80 and the exact warning without reaching `s VERIFIED`.

Deletion records are proof-database optimization instructions, not derived
clauses.  Removing them cannot weaken reverse unit propagation: every clause
that would have been deleted remains available.  Soundness does not rest on
that observation alone.  Pinned DRAT-trim
`31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` replayed the complete addition-only proof
against CNF `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` with `-I -f -W -U -t 600`, exited zero,
emitted exactly one warning-free `s VERIFIED`, and reported zero RAT lemmas in
the core.  Thus the retained proof is a checked RUP-only refutation of the
exact full-bank `hole7` formula.

This certificate excludes only the exact `hole7` order-12, parameter-three
template formula.  The graph-theoretic theorem additionally depends on the
separate encoding-soundness and structural-template coverage proofs.  It does
not by itself exclude `hole5`, larger orders, other parameters, or resolve the
universal gamma-theta conjecture.
