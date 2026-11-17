The exact reviewed helper is UNFIT_FOR_EXECUTION. Static review is 100% complete
for this assigned source audit; one concrete defect prevents an execution-ready
conclusion. The original 1279-line helper, SHA256
06ce7edaf8edd2dcda4e78ce0e5e259efc1bbb867df00daf2765d155b5c47122,
and its entire 14-file preparation packet remain unchanged. This is a source
implementation issue, not a scientific or staged-content defect.

The blocking finding is detailed in FINDINGS.md: git() captures literal streams
at line 483, omits stdout when opaque=True at line 484, and raises on a failing
exit at line 486. Failed opaque commands with nonempty stdout retain only its
hash. Parser failures after successful opaque reads can likewise lose the exact
stream. Routing, complete tree listings and TREE batch object reads use this
path. stderr is retained. This contradicts PLAN.json's literal-stream failure
contract. The independent adversarial control review identified the same gap.
No command was executed to demonstrate the branch, and no source repair occurred.

The remainder of the static source review found no additional concrete defect
within the reviewed contract. The following mechanisms are present in the actual
source; they remain unexecuted:

| Mechanism | Source lines and verified reasoning |
| --- | --- |
| Entry and interpreter | The no-argument literal default exits at 10–12 before project reads. Active CPython 3.14/non-optimized validation at 15–16 precedes active imports. The exact four-argument guard at 1247 precedes project-plan loading at 1248. Import defines the outer function and imports built-in sys only. |
| Authority | 366–453 bind exact helper/PLAN, actual stage/audit control buffers, complete stage-audit namespace and whole root adoption semantics, actual literal schemas/statuses, explicit root resolutions, phase/action, fresh 64-hex nonce, serialization assertions and expiry no longer than one hour. No generic PASS or invented audit criterion count is substituted. |
| Scope and content | 607–672 derive exact 15 Git paths / 13 additions / 2 aggregate replacements / 6 directories from pinned actual TARGETS and full candidate. Entire 788 untargeted old files, 381 directory modes/root0750, 17 DS_Store and inherited 0600/0666 modes remain constrained. Candidate bytes inherit original article dates/version/rights/disclosures from the accepted stage; no article date rewrite exists. |
| Complete aggregates | 548–605 re-decode actual CollectionPage.mainEntity.ItemList, all 130 old raw/typed JSON and whole HTML units, 131 whole XML nodes and namespace-aware parsed nodes, and exact 3/1 closed-span full-buffer forward/reverse proofs. Exact raw HTML preserves its concatenated parser-data events. |
| Installation | 892–1066 require separate retained locks and fresh absent runtime; 961–991 durably prepare 15 held buffers, two complete relative aggregate backups, 13 leaf absences, six directory absences and native recovery material before website writes. Held parent chains and original leaf identities fence each exact target. Additions use exclusive Darwin rename; only two aggregates use replacement. Whole public/native/source/stage/audit fences repeat. |
| Raw index and TREE | 691–846 and 1109–1141 preserve all 58728 untargeted whole raw records, construct only 15 intentional zero-stat stage-0 100644 records, preserve complete TREE bytes and checksum, reconstruct all cached subtree semantics, and compare separate private checking indices without refreshing native stat fields. Private semantic maps derive foreign staging before/after rather than assuming it absent. |
| Commit and push | 1112–1147 start the commit index from exact parent HEAD and verify all untouched commit-tree leaves plus exact 13A2M. 1157–1209 hold an exclusive native index.lock, validate a single-parent commit and root-supplied author/committer/date, CAS local master and atomically replace only the controlled raw index. 1097–1100 and 1212–1228 check exact routing/remote parent, ancestry, one explicit ordinary nonforce COMMIT:refs/heads/master push, exact remote successor and complete local postchecks. |
| Failure and limits | There is no automatic retry, cleanup or rollback. The implementation retains locks, backups, prepared buffers, journal and partial state, subject to the concrete opaque-stdout defect above. Root serialization remains an operational assumption; ordinary nonforce push has no expected-parent server lease and snapshot observations cannot close every network race. |

One separate saved, fully read 184-line passive custody reader ran once, exit 0,
with empty literal streams. It invokes no production or scientific program and
no Git/network command. The complete 14-file source preparation, 1635-file/
770-child-directory stage, successful 22-file stage audit, all twelve protected
source/private roots, six root controls, native M/W HEAD/index/config/local heads,
whole website public/configuration and actual modes/topology match their fixed
guards and remain identical before/after. Runtime is still absent.

Its independent raw-data check confirms native index v2 / 58730 records / valid
whole checksum, 58728 untargeted records, sole whole TREE 35878 bytes and payload
35870 bytes, 983 nodes / 977 valid / the exact six existing invalid paths and the
actual pinned hashes. It does not execute the helper's semantic reconstruction
or query Git objects; future runtime semantics have not been empirically tested.

Two initial read-only file-discovery commands assumed PLAN.md and failed with
FileNotFoundError; actual discovery identified PLAN.json. Their literal reported
errors are retained in DISCOVERY_ERRORS.md. They were neither helper runs nor
failed invocations of the saved custody reader. No helper/default/mode/import,
AST, compile, help or test ran. No ignore/runtime/authority creation, Git write,
network, M/W/source/other-packet mutation, Sheet/deploy/redirect or contact occurred.

A corrected helper requires a new source packet and review. This audit grants
no execution permission, publication, deployment, actual UI/embedded PDF/live,
scientific/copy/priority or future-action certificate. follow_up null; AA and
actual publication date null.
