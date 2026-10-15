# Independent repair acceptance criteria

Scope: verification-only repair of the existing PR436 / problem2569 / KOU21.60 claim at source head c7805ab0804f50c6f4b0d1dda99e433dbb702ae2. No new proof search, priority audit, paper creation, source-status decision, external outreach, or remote mutation.

Hypothesis: replacing the finite verifiers' essential Python asserts with explicit runtime failures preserves every original test, input, loop, predicate and failure message while making those checks survive Python -O. It must not enlarge the mathematical claim, bypass failed predicates, overwrite public baseline outputs, or report unexecuted checks as passes.

Acceptance requires:
1. Read full builder, runner, source and repaired verifier bytes before execution; pin their SHA-256 hashes and source head provenance.
2. Every original Assert maps one-for-one to if not (same test): raise AssertionError(same message), including chain comparisons, loop conditions, lazy message evaluation and no-message exceptions. All other AST semantics and source mathematical constants remain unchanged. No assert or __debug__ elision in repaired code.
3. Execute only separately copied private inputs and use fresh private output paths. Match successful original and repaired baselines under normal/-O Python, including every relevant stored result and exact finite-check count. Record commands, return codes, stdout, stderr, environment and durations.
4. Test at least one independently constructed false mathematical invariant in repaired code under both modes. A success banner or zero return code must never survive a real invariant violation. Canned false-condition probes alone are insufficient.
5. Verify input hashes before/after and do not mutate sealed originals or shared repaired artifacts. Review the existing reproduction execution record only after independently recording criteria.
6. State strongest verified result, defects and exact residual gaps. Distinguish runtime robustness from independent mathematical proof. Completion refers only to this repair audit.
