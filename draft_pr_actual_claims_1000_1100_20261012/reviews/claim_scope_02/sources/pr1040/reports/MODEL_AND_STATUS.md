# Model and status of the reconstructed findings

## Target

Problem identifiers: O7b, 8400008, AMR-083-0008. The target is a classical uniform randomized oracle reduction from full integer factorization to C7.

For every positive integer m, C7(m) is the unique positive pair (r,s) such that

    m = r^2 s,
    v_p(r) = floor(v_p(m)/2),
    v_p(s) = v_p(m) mod 2.

Thus s is the parity squarefree part, not the radical. The factors r and s need not be coprime; C7(27)=(3,3). C7(1)=(1,1).

The requested reduction must satisfy all of the following.

1. It works on every positive integer input n, with the empty factorization for n=1.
2. On every allowed random tape it halts and returns either the correct complete prime factorization or the explicit failure symbol `?`. It never returns an incorrect or incomplete factorization as success.
3. For some fixed constant c, its worst-case bit work, oracle query count, query lengths, and random tape length are bounded polynomially in the input length ell. The stipulated random tape bound is at most ell^c, with usual harmless adjustments for finitely many small inputs.
4. At least half of the uniformly drawn allowed random tapes are successful. A fixed bounded tape can be used, padding unused bits; an unbounded expected-time procedure alone does not meet this requirement.
5. The guarantee holds for every correct oracle implementation of the specified function, not merely a favorable oracle or a promise distribution of inputs.

The squarefree-input results are a restriction of this target, not a solution on all positive integers. A verified proper factor on one branch is also not yet a full-factorization guarantee.

## Status ledger

- Original problem: unresolved, 2/5 turns; unchanged by this reconstruction.
- Turn 1: reported independently accepted before interruption. Its findings are reconstructed here; the old report and audit bytes were not recovered, so no old hash or newly independent acceptance is asserted.
- Turn 2: preliminary and unaccepted. The reconstructed candidate proofs have been checked locally, but no independent acceptance has been obtained.
- Recovery: verification of already reported directions only. No new approach, publication, queue change, or new research turn.

## What is established and what is not

The normal-form theorem is unconditional on squarefree n. The valuation-invariance theorem is limited to its specified operations and its initial tags. The probability estimate additionally requires freshly sampled independent variables, normalized low-degree polynomial tags, and a pathwise degree budget. It bounds success together with absence of coefficient splits only when the specified model forces success to have a corresponding hit.

The turn-2 sign argument is conditional on obtaining a nonempty relation with a sign-blind selector and on the stated sampling law. It does not supply a polynomial relation-acquisition algorithm or a half-success probability for the whole reduction. The fixed-batch relation algorithm does not eliminate adaptive C7 queries or arbitrary use of their integer answers. The transporter lemma assumes a second equal-norm representation already exists and is available.

These are scope restrictions and obstructions to the explored routes. They neither resolve O7b nor establish a lower bound against unrestricted classical bit algorithms.
