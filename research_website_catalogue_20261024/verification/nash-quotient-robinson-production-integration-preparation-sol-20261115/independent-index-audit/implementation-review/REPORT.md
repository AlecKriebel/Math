# Independent review of the prepared exact14 helpers

Scope: full-body independent reading of `exact14_lib.py`, `preflight.py`, `install_exact.py`, and `hooks/pre-push`. This review concerns production-control mechanics only. It does not adopt scientific conclusions or authorize execution. Completion estimate: 100% of the requested static mechanism review and permitted pure checks.

## Findings and corrections

The first reading found three concrete issues, promptly reported to the preparation owner: new leaves used unconditional replacement and could clobber a file appearing after the absence check; publication trusted target entries from a mutable runtime index rather than the approved immutable commit; and bounded commit-message validation occurred after copies and object writes. The owner corrected these. The final bodies use atomic no-clobber hard-link publication for twelve additions, recheck aggregate baseline bytes before replacement, derive all fourteen shared-index entries from the approved commit tree, compare each mode/blob with sealed payloads, and validate the message in the initial root gate.

A later reading found that hook byte sealing alone did not enforce executable mode. A non-executable pre-push hook could be skipped by Git. The final helper requires exact 0555 mode and executable access immediately before guarded push; root adoption also binds 0555 mode. The observed hook is 0555. The owner additionally corrected the audit gate to the actual independently sealed `SEAL.json` and fixed exact seal digest; this review confirmed that correction in the final complete source reading.

## Mechanisms verified by inspection

- Exact14 scope is bound to the sealed stage contract and manifest: twelve new leaves and only two aggregate replacements. The whole stage namespace, paired payload bytes, source namespaces, qualified core bindings, public baseline, configuration files, and expected 593/87/88 to 605/90/91 counts are checked.
- Missing execution flag and absent root adoption reject before runtime creation, public copies, or Git commands. Root adoption binds the stage, actual audit seal, exact preparation seal/code bodies, baseline parent/branch/counts, protected index capture, path list, and installation authority. Publication requires a second exact root approval of the pending commit/tree/parent/path/protected-record receipt.
- The commit index is separate and initialized by `read-tree HEAD` without worktree updates. Raw blob construction bypasses filters; cacheinfo updates name only the fourteen targets. The resulting complete diff, sole parent BASE, target modes, and exact target blob IDs are checked.
- The shared index is cloned, updated only with entries derived from that immutable approved commit, and parsed as strict SHA1/DIRC v2. Unsupported flags, stages, formats, and extensions reject. Full protected raw entries are compared byte-for-byte, including stat data, modes, object IDs, flags, paths, and padding. The target cardinality and twelve-entry count increase are checked before replacement.
- The actual shared index is replaced only while owning an exclusively created index lock and after a fresh whole-index/HEAD check. Cleanup compares the lock inode and device before unlinking, so it will not remove a different regular lock. TREE cache data can change; no opaque unsupported extension is silently accepted.
- Inherited Git routing/config variables are stripped. Other hooks are disabled. Push uses an explicit single commit-to-master refspec, no force option, no automatic tags, mirror disabled, and submodule recursion disabled. The sole controlled pre-push guard remains enabled and checks the actual advertised remote-old BASE, approved local commit, master destination, remote name, and destination URL digest. Git receive-pack's expected-old-ID check supplies the subsequent race check, as documented in the prior sealed addendum.

## Checks performed

All four complete bodies passed syntax parsing. Eighteen permitted pure checks passed: fifteen hook stdin cases and three execution/adoption-gate cases. Hook cases cover accepted exact parent/commit, named local ref to the same approved OID, remote rewind, advance, absent ref, wrong commit/ref/remote/URL, extra or absent records, malformed input, deletion, and missing authority environment. Gate cases confirm missing execution, absent installation adoption, and absent publication adoption reject while `run-state` remains absent. The test runner invokes no Git command and uses an inert example URL string without contacting it.

Source size, mode, and SHA256 pins are in `pure-check-results.json`. No website, Git object, Git index, Git ref, remote, deployment, or external-human action occurred. No old sealed audit file was edited.

## Remaining limits

This is static review plus pure checks, not an authorized end-to-end Git/index/push run. The runtime protected-entry comparisons and exact-tree checks must still pass during a later authorized execution. The advisory index lock cannot prevent noncooperating writes to other files. The combined file/index/local-ref/remote operation is not one transaction; a failure after mutation must be inspected through runtime receipts rather than automatically reset. No production authority is supplied by this review.

The final revision also corrects receipt read-verify-read races: root adoption and root commit approval now hash and parse the same retained byte buffer. This correction was re-read in both complete changed bodies, and the eighteen pure checks were rerun against the final stable code. No unresolved blocking implementation finding remains in this audit's scope. Sealed stage/code/receipt files must remain unchanged during execution; this assumption is separate from ordinary Git index-lock cooperation.

## Exact final source pins

| File | Bytes | Mode | SHA256 |
| --- | ---: | --- | --- |
| exact14_lib.py | 16505 | 0644 | 11be1d96dcc69919b0fcbcb673e56fec5f01d95ac8e257a908f66bbe679fd874 |
| preflight.py | 1768 | 0644 | 339d0fa4d51a388befeb567e9d8f844dbb2aa9c6df4e276f36fdda6d62dab219 |
| install_exact.py | 12353 | 0644 | c6e5ab488ef42d311179ee6503e627d3860e9a8ec13c90bcdd538fa542cae722 |
| hooks/pre-push | 925 | 0555 | f165472879ca2073e41c070789abc86c7bdf09b96b8c980dcd2f8964309f038d |
