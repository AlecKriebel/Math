# Supplement: proof interfaces and reproducible finite evidence

The universal claim is the exact integral divisor for all n in the README. The paper supplies its proof directly. This supplement distinguishes algebraic obligations from finite evidence and historical provenance.

1. Forest products: paired incidence wedges kill cycles; a tree is a unimodular basis of its block's zero-sum lattice, and the two basis-change determinants square to +1. Fixed internal trees are not summed.
2. Exact transfer: the exponential is a product of `1+a_ij q_ij`, with one term per subset. Components missing Y lack top X degree. Replacement by a Y-rooted star is an identity for one selected product; every X pair has coefficient +1 and leaves exactly `f_Q`.
3. Constant image: `U={u:u1=0}`, `dim U=n-1`; `W=Lambda(U tensor Q^2)^SL2`. The weight-zero E-kernel calculation, noncrossing tensor leading Dyck words and normalized antisymmetrization prove all-degree quadratic generation. Every q monomial is zero or an arbitrary partition forest state, so the full Bell map Phi is onto and constant.
4. Dimensions and character: `d_r=binom(m,r)^2-binom(m,r-1)binom(m,r+1)` sums to `C_n`. Degree symmetry and torus permutation/scalar weights give `det rho(g)=(det g)^C_n` for m>0. The n=1 boundary is direct.
5. Gaussian order: with D the row-sum diagonal, B=D^-1 A and S the symmetric zero-sum Schur complement, `G_A=(det D) M_S rho(B|U) H_D` in that order. The normalized lowering factor and raising factor preserve W, are degree-triangular with identity diagonal, and have determinant 1. `B1=1` gives `det(B|U)=det A/det D`. The quotient determinant is `(det A)^C_n` with constant +1.
6. Rings: temporary inversion of generic row sums occurs only in Q(a_ij). The forest formula already defines a polynomial operator on a constant space, so the identity holds at every specialization. A constant rational kernel basis and lifts give a polynomial complementary block. Primitivity and Gauss's lemma descend Q-divisibility to Z-divisibility, including a zero quotient.

## Fresh finite checks

The transfer code uses Python plus SymPy. From `evidence/fresh_20261013/transfer_01`, the authored CHECKS.md gives the exact invocations and RUN_RECEIPTS.json pins actual interpreter, command, times and exit status. It enumerates graph/exterior models and generic symbolic T determinants for n=1,2,3; tests n=4 transfer/factorization and all internal-tree choices; and detects wrong order, wrong normalization and X-only components. Its saved outputs are actual fresh executions, not reconstructed historical outputs.

From `evidence/fresh_20261013/invariant_01`, run `python3 -B verify_invariants.py --mode all --max-m 6 --max-n 7 --max-r 6 --output CHECK_RESULTS.json`. This standard-library code uses exact arithmetic, checks SL2 operators, Bell-image ranks through n=7, matching tensors, determinant characters, explicit exterior sections and failure controls. The packaged saved output is the family's original fresh run, with code hash and timestamp. Run new checks to a new output file if preserving those bytes. The expected run need not be quick; the package includes the complete existing outputs and derivations.

These commands describe reproducibility; the preparation agent did not rerun the fresh families' algorithms. All n is proved by the derivation, not finite ranges. The 9 October ten-file edition supplied no executable and its omitted calculations were not replayed. Family PASS verdicts certify their own pinned stage and exact family interfaces, not this newly authored paper. The dated preparation checks and stage-specific AI reviews are identified by their scope and frozen inputs in `REVIEW_HISTORY.json` and `EVIDENCE_INDEX.json`; they are not human refereeing, journal acceptance, formal certification or submission/publication records.

## Source comparison and evidence limits

The exact same-theorem Ferudun source and qualified 9/11 October chronology are in the dated addendum, paper abstract/theorem/introduction/bibliography and metadata. Its core divisor proof was compared by the priority family; its additional exactness computations were not reproduced. Li–Yan full body remains unknown, CSS 2017 and citation/version chains remain partial, and discovery independence/publicity/priority remain unknown.

Authored proof exposition and code are CC BY 4.0. Third-party bodies and extracted full text are excluded. Receipt hashes of excluded sources are provenance, not permission to redistribute them or a claim of fresh reading by the preparation agent. No human peer review or formal certification is asserted.

## Terminal whole review and execution boundary

The second fresh complete review in `evidence/whole_20261014/package_02/REPORT.md` and `VERDICT.json` passed with zero actionable P0–P3 issues. The root adopted its whole report and exact output seal. The 14 October terminal acceptance is administrative: unchanged authored terminal copies and state/history/navigation were appended; the reviewed source/PDF/metadata and prior proofs/checkers/outputs remain byte-identical. Current readiness is true, published is false, root final administrative verification remains pending, and services are blocked by preceding PR1032. The copied seals preserve hashes for private/omitted inputs; `evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json` gives individual omission reasons.

The historical graph comparator uses an assertion with union side effects, so optimized Python removes necessary operations. Reproduction of that comparator is supported only by the documented ordinary Python commands. Review02 optimized evidence applies to its newly explicit checks and side-effect-free exterior operations, with the historical comparator excluded. This limitation is preserved; terminal administration does not change checker code or certify the unsupported optimized mode.
