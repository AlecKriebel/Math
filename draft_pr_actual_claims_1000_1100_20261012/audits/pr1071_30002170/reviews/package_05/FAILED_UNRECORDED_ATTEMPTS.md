# Actual failed and interrupted review-harness attempts

These are review-harness events, not candidate findings. They are retained and not converted into successful checks. Full later child argv/stdout/stderr/exits, including expected rejections and the first failed custody suite, are in COMMANDS.jsonl and its individually named raw streams.

1. Tool chunk 0c4223: embedded `python3 -` exited 1 during creation of the first derivation text. The enclosing shell continued its diagnostic commands and returned 0. stdout of the embedded Python was empty. stderr was a SyntaxError at stdin line12, ending `SyntaxError: invalid decimal literal`; the long offending line was the Fourier-regularity paragraph containing `f'''`, which prematurely ended a triple-single-quoted Python literal. The intended derivation was then saved directly by apply_patch before reading earlier reports. This was a reviewer quoting error; no paper or other input was edited.

2. Tool chunk 6a821e: argv `python3 -B -` with stdin:

```python
import sys
sys.path.insert(0,'reviews/package_05')
from run05 import run,R
run('interface-suite',['/opt/homebrew/bin/python3','-B',R/'interfaces05.py'],cwd=R)
```

The outer process exited1, stdout empty. Its stderr was:

```text
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/reviews/package_05/run05.py", line 15, in run
    out.write_bytes(proc.stdout);err.write_bytes(proc.stderr)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py", line 796, in write_bytes
    with self.open(mode='wb') as f:
         ~~~~~~~~~^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py", line 771, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OSError: [Errno 28] No space left on device: '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/reviews/package_05/interface-suite.stdout'
```

The recorder had already captured completed inner commands through `py311-normal-clean-verify`. It did not persist the outer child interface-suite returncode or its raw streams. Those are UNKNOWN, and this initial suite is not counted as complete. The partial 1,136,413-byte newly generated ZIP remains an owned failed-attempt artifact. Cause deeper than the actual Errno28 is UNKNOWN.

3. Tool chunk b383a0: shell command began `python3 -B - <<'PY'` for a proposed owned-output inventory/cleanup. Shell exited1 before Python launched, stdout empty, stderr exactly:

```text
zsh:1: can't create temp file for here document: no space left on device
```

No inventory or cleanup from that command executed. A later no-heredoc inventory emitted all eight duplicate identities to tool output f180fe before deletion. The subsequent cleanup succeeded and retained OWNED_DUPLICATE_CLEANUP.json. Only this review's new exact duplicate ZIP/PDF outputs were removed, 8,217,736 logical bytes. The seven viewed page PNGs were retained.

4. Tool chunk 864aed: a `python3 -B -c` command attempted to write FAILED_ATTEMPTS.json and append a checkpoint. It exited1, stdout empty. The traceback's terminal frames were:

```text
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py", line 809, in write_text
    with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py", line 771, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OSError: [Errno 28] No space left on device: 'reviews/package_05/FAILED_ATTEMPTS.json'
```

The same tool call's following apply_patch failed with `Exit code: 1`, empty normal output and `Failed to write file /Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/reviews/package_05/interfaces05.py`. The edit was later applied successfully after free space increased. No failed receipt-file creation is asserted successful.

5. Tool chunk 203eda: `df -h .` succeeded, showing386MiB; following `ls -l reviews/package_05/interfaces05.py reviews/package_05/FAILED_ATTEMPTS.json` returned1 because FAILED_ATTEMPTS.json did not exist. stderr: `ls: reviews/package_05/FAILED_ATTEMPTS.json: No such file or directory`. The interfaces source remained present. This is consistent with event4.

6. Tool chunk e8f161: a diagnostic `python3 -B -` printed source-array schemas and then exited1 with stdout retaining the successfully printed rows. stderr ended `File "<stdin>", line 11, in <module>` / `IndexError: list index out of range`. The diagnostic omitted the `rows` container used by package03's freeze. The final custody reader handles records/files/rows/unchanged_records explicitly. No incomplete diagnostic was counted as custody validation.

7. Full recorded command `custody-suite01` exited1: source/copy checks had reached the historical-prefix check, where the review harness incorrectly associated the83-row stage with history/preparation01 (which actually has50). Its full stderr/argv are retained in custody-suite01.stderr and COMMANDS.jsonl. Direct inspection identified the correct50/83/116/128/140 historical snapshots, and custody-suite02 completed successfully. This was a reviewer stage-map error, not a candidate defect.

The final report distinguishes these observed facts from unknown deeper disk causes. No failed attempt involved Git, services, outreach, candidate repair, old-input deletion, or changing an earlier sealed report. Full tool transcripts retain the original shell payloads and long diagnostic source lines; this human-readable event ledger does not claim to replace those transcripts byte-for-byte.
