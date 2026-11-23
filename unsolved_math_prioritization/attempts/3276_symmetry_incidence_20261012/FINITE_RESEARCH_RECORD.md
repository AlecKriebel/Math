Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Fourth-pass bounded tournament packet

Row 1754 / problem 3276 / OPG-1808. Read `FINITE_CANDIDATE_REPORT.md` for the exact completed result, `FINITE_PROOFS.md` for the reduction and soundness of every pruning rule, and `the original operational record` for the credited primary source.

This packet adds actual-edge incidence-domain filtering to the previously accepted proper-interval search. It has no dependency on copying private source documents into the deliverable. Prior packets are unchanged. No remote or queue changes were made in this lane.

## Reproduction

A C++17 compiler (`g++`) and Python 3 are required. From the packet directory:

- original implementation replay under normal Python compiles all C++ sources in a temporary directory and freshly reruns the entire bounded search, both reachability engines, independent literal oracles, known-model harnesses, malformed-input gates, source mutations, and result mutations. General order ten is the dominant runtime; allow time for complete execution. There is no time or node cap on genuine searches.
- original implementation replay under Python -O and original implementation replay under Python -OO do the same with optimized Python. These original commands supported reproduction in the original packet; see `the original operational record` for what was actually executed in this packet.
- recorded-result validation under normal Python checks the recorded result schema, exact accepted scopes, counters, and result-mutation gates. It does not rerun searches or hostile source-code mutations. `-O` and `-OO` may be used in the same way.
- externally pinned integrity verification under normal Python verifies every packet file against the external manifest pin. It does not rerun any computation. Obtain the expected pin from the delivery message or external pin file, not from a newly changed manifest.

`--record` freshly executes the complete replay and prints the resulting JSON. None of these commands needs to modify packet files. Validation failures use explicit exceptions and are not disabled by Python optimization flags.

Direct candidate examples after compilation:

- the original candidate invocation (--n 10): complete general order-ten reduced search with all four necessary conditions.
- the original candidate invocation (--n 9 --fresh): same scope, using Warshall closure.
- the original candidate invocation (--n 5 --allow-rainbow --allow-predecessor --no-interval): incidence-only satisfiable control.
- the original candidate invocation (--n 9 --no-incidence): omit the new rule; output scope explicitly records this.
- the original candidate invocation (--n 12 --periodic): a different, potentially long-running single-word scope. No completed periodic order-twelve result is delivered here.

The source permits larger exploratory scopes up to order fifteen; CLI support is not evidence that any such scope was completed. Only the exact scopes in the verified report and result records are conclusions of this packet.
