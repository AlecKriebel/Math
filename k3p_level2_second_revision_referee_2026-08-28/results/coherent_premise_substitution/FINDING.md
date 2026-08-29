# Direct coherent premise-substitution finding

## Evidence status

The original execution recorded in `COMMANDS.md` and `TRANSCRIPT.txt` is
**uncredited and superseded**: `env -i` removed inherited variables but did not
enforce filesystem or network isolation.  Every result credited below comes
from the default-deny replay in `COMMANDS_SANDBOXED.md` and
`TRANSCRIPT_SANDBOXED.txt`.

## Result

Under the frozen default-deny macOS sandbox profile,
`build_global_transfer.py` and `verify_global_transfer.py` both returned
`PASS` after `CUT_GLOBAL_LOGIC_REPORT.json` was replaced in a fresh disposable
copy by a deliberately proof-free and internally contradictory fixture.

This was a coherent producer-level substitution: the producer regenerated
`GLOBAL_TRANSFER_CERTIFICATE.json`, and the certificate bound the substituted
fixture's actual SHA-256
`f82a8f610a73a878896d471dfc2f6928b4d03e1afd1b3b2cb5aa05e34e959ca0`.
The independent verifier then accepted that regenerated certificate.

The fixture deliberately:

- changes the schema and verdict;
- asserts a contradictory `PASS` label while retaining
  `reverse_inclusion_proved=false`;
- deletes the containment identity and all genuine source/target metadata;
- explicitly says that no proof is supplied; and
- replaces the complete provenance hash map by `{}`.

It preserves only the three downstream-tested values:

1. `generic_cut_consequences.proved_inclusion = Cut(N_prime)_subseteq_Cut(N)`;
2. `generic_cut_consequences.reverse_inclusion_proved = false`; and
3. `directed_relation.target_regular_not_assumed = true`.

The producer reads only items 1 and 3 at
`build_global_transfer.py:252-271`.  The verifier checks all three at
`verify_global_transfer.py:345-370`; neither validates the report schema,
verdict, blocked status, proof, or provenance.  The regenerated D1 step also
retains the stale `isotropic-JC generic recovery` reason from
`build_global_transfer.py:177-181`.

## Logical boundary

This test directly proves acceptance by the producer and its advertised
independent verifier.  It does not claim that an unresealed changed file passes
the adversarial/release/theorem-manifest layers: those layers contain fixed
hashes and reject byte drift.  Passing those outer layers would require the
downstream hash records to be resealed.  Their byte locks therefore protect a
particular unsupported premise serialization; they do not make these two
semantic consumers independently validate the premise.

## Credited isolation evidence

The credited replay used `sandbox-exec` with `SANDBOX_PROFILE.sb`, whose first
operative rule is `(deny default)`.  The package process received exactly ten
non-secret environment variables.  Before any package script ran, the frozen
reviewer probe established:

- a TCP connection attempt failed with `EPERM`;
- listing the existing `/Users/alec/.ssh` directory failed with `EPERM`;
- reading the existing sibling `/Users/alec/Documents/Math/AGENTS.md` failed
  with `EPERM`;
- listing the concurrent `package_copy/review_runs` directory failed with
  `EPERM`;
- reading the source builder succeeded with its expected SHA-256, while trying
  to create a marker in `package_copy` failed with `EPERM`; and
- a write-and-read round trip inside the disposable test tree succeeded.

The only allowed write subtree was
`tmp/coherent-premise-substitution-sandboxed.QeuPXv`; package source and the
pinned virtual environment were read-only.  The active referee verification
continued separately in `package_copy/review_runs/.../workspace`.  Relevant
source mtimes and sizes were identical before and after.  The accepted
sandboxed certificate is frozen as
`GLOBAL_TRANSFER_CERTIFICATE.sandboxed.accepted.json`.  The disposable tree
was deleted after all evidence was frozen.

Profile SHA-256:
`20a84f5162d7379fa52083d3f7edca9369b42faf5574187fe196a9d70f27154c`.
Probe SHA-256:
`f37f376d088eb721787d84bc2ced17fb2baa98d5010bdbcbc17c82fe6379a93b`.
