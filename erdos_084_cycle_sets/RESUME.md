# Resume guide

This is the operational handoff for the paused Erdős Problem 84 cycle-set
program.

> **Stop state:** the lower-bound target
> \(f(n)/2^{n/2}\to\infty\) remains open. No published asymptotic bound was
> improved. The program produced an all-\(m\) twin-boundary identity and exact
> finite Hall data, but it remains at least two global mechanisms away from a
> solution.

Read [`STATUS.md`](STATUS.md), then
[`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md), before restarting any lane. The status
file is the concise checkpoint; the ledger is the authoritative scope record.

## Five-minute exact smoke test

From the repository root, run:

```sh
python3 -m unittest discover -s erdos_084_cycle_sets/tests -v
python3 erdos_084_cycle_sets/src/signature_counts.py --max-k 4
python3 -m json.tool \
  erdos_084_cycle_sets/outputs/reference_counts.json >/dev/null
```

At the pause checkpoint all five unit tests passed, the small exact counts
were reproduced, and the reference JSON parsed successfully. Larger exact
programs and the independent Hall commands are listed in
[`experiments/hall_matching/README.md`](experiments/hall_matching/README.md).
The largest bounded representation run used about 715 MB at \(m=7\), so the
published checkpoint does not require additional hardware. More hardware
could extend the finite table, but it would not supply either missing global
mechanism and is not a meaningful reason to resume the program.

## What survived

1. The protected fan construction and exact recurrence
   \[
   S_{m+1}\geq8S_m+2E_m.
   \]
2. Exact full-family counts through \(m=10\), supporting but not proving
   \(mE_m\geq S_m\).
3. The Boolean down-set formulation of the trace-to-excess bridge.
4. The all-\(m\) twin-boundary identity
   \[
   g_m(P)=2|\mathcal B_P|
   -\bigl(|\mathcal A_P|-|\mathcal A_P\vee V(P)|\bigr)
   \]
   and the canonical join-commuting embedding of every safe collision fibre
   into the corresponding unsafe fibre.
5. Exact falsification of the one-local-edit representation graph at
   \(m=6,7\).
6. The representation-aware Hamming-two matching conjecture, verified only
   for \(3\leq m\leq7\).

## What remains missing

Two logically separate theorem-strength mechanisms are still required:

1. a trace lower bound such as
   \[
   \sum_{P\ni1}R_m(P)\gg\frac{8^m}{m};
   \]
2. a uniform trace-to-excess bridge, such as the Boolean down-set inequality
   or an equivalent canonical congestion-two charge.

The earlier collision-energy route is not a plausible substitute:
\(Q_m/W_m=8.28,15.58,30.39\) at \(m=8,9,10\). The orbit route is also
secondary because the explicit four-run family suggests its proposed fixed
constant may decay like \(1/m\).

## Do not resume with

- enumeration at \(m=8\) or beyond merely to extend the Hall table;
- edit radii larger than Hamming two;
- further repair-template or alternating-path mining;
- more random searches for a matching without an accompanying infinite
  invariant;
- any claim of novelty for the protected construction before the full 2026
  Dunås thesis has been compared line by line.

## Definition of a justified resumption

Resume only if at least one of the following appears independently:

1. an abstract Hall or uncrossing theorem proving the Hamming-two matching
   uniformly in \(m\);
2. a direct canonical congestion-two charge;
3. a proof of the trace lower bound, which would make the bridge the final
   remaining step;
4. a theorem on a quantitatively large class of parameters that already gives
   a nonsummable contribution to \(E_m/8^m\).

Finite matching success alone does not satisfy this standard. A successful
resumption must deliver an infinite lemma with the correct asymptotic scale,
not a larger table.

## Reproduction entry points

- [`proofs/PROTECTED_CONSTRUCTION.md`](proofs/PROTECTED_CONSTRUCTION.md) —
  protected reduction and recurrence;
- [`proofs/SHADOW_PROGRAM.md`](proofs/SHADOW_PROGRAM.md) — trace, down-set,
  twin-boundary, and Hall formulations;
- [`experiments/hall_matching/CONCLUSION.md`](experiments/hall_matching/CONCLUSION.md)
  — bounded experiment verdict;
- [`experiments/hall_matching/README.md`](experiments/hall_matching/README.md)
  — exact commands and finite certificates.

The complete Hall experiment deliberately stops at \(m=7\). Preserve that
boundary unless a theorem, not another enumeration target, justifies
crossing it.
