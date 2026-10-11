# Sequential fresh preprint review 02

Independent review of PR364 / problem30004048, restricted to the original claimed-solved queue entry. All reviewer writes are confined to this folder. No external communication, submission modification, Git/index/ref operations, uploads, installations, or tracker operations are authorized here.

The reviewer reads primary sources, manuscript and original Turn 3 before other analytical verdicts or candidate execution. The independently reasoned mathematical assessment is sealed before examining modern checkers and supplied audit verdicts. Finite controls supplement universal reasoning.

Raw acquisitions, renders, complete process streams and acquisition drivers are private evidence. Closure will bind the exact namespace with named self-exclusions; after passing closure no namespace writes are allowed.

`verify_review.py` is the read-only full-namespace verifier. The exact one-shot **writing** closure driver is `private/close_review.py`; it creates the manifest, captures the preseal verification, and writes the final seal. The parent must read this driver before it is launched. Neither file is a portable submission checker, and neither changes the four fixed submission artifacts.

The seven entries in `REPLAY_RECEIPT.json` bind whole native stdout/stderr streams, source hashes, literal argv/cwd, and literal absolute `expected_file` paths. Those paths resolve to this review's isolated execution package, except the package verifier's independently reconstructed expected output at `private/package_expected.json`. They are evidence paths from these executions, not relocatable paths.

The one-shot driver creates `MANIFEST.json` and runs the verifier in `PASS_PRESEAL` mode. Its full native streams and receipt are saved under `private/closure_001/`. It then writes `FINAL_SEAL.json` and runs the same verifier in `PASS_SEALED` mode, returning that final output in memory. The complete pre/post verifier objects must agree after changing only the status value from `PASS_PRESEAL` to `PASS_SEALED`; their raw bytes therefore differ. The final seal binds the manifest and all three excluded preseal capture files. The seal excludes itself and requires an external parent receipt to bind its bytes. The manifest lists these five exact self-exclusions, with no directory exclusions. No writes anywhere within this namespace are permitted after the final seal.
