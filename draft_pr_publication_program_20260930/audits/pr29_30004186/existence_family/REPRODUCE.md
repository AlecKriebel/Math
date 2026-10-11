# Reproduce the sealed existence-family controls

Runtime used: `/usr/bin/python3`, Python 3.9.6, SymPy 1.14.0. No installation was performed. ORIGINAL_VALIDATION.json records every original file's Git blob, SHA-256 and exact-head comparison. REPLAY_RECEIPT.json records the three isolated legacy commands and output hashes. CONTROL_RESULTS.json records the fresh 55 assertions and clearly separates exact polynomial identities from 23 finite floating observations.

Do not run legacy writers in `source_snapshot` or edit a sealed receipt. For a fresh run, copy the own control and original legacy script bytes into a new ignored directory and run them there:

```python
from pathlib import Path
import json, shutil, subprocess
p=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr29_30004186/existence_family')
s=p.parent/'source_snapshot'
jobs=[(p/'existence_controls.py',55),
      (s/'check_identities.py',20),
      (s/'independent_review/independent_checks.py',135)]
for index,(script,expected) in enumerate(jobs):
    folder=p/'ignoredtmp'/'fresh_reproduction'/str(index)
    folder.mkdir(parents=True,exist_ok=True)
    copied=folder/script.name
    shutil.copyfile(script,copied)
    result=subprocess.run(['/usr/bin/python3',str(copied)],cwd=folder,
                          capture_output=True,text=True,check=True)
    receipt=json.loads(result.stdout)
    assert receipt.get('assertions',receipt.get('passed'))==expected
    print(script.name,expected,'PASS')
```

The exact-head checks are read-only Git comparisons with `5ac4a57e08dd72a6f16768f2288b9c0349999431` and base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; `validate_original.py` fully specifies them. Its archived receipt is the record of this run. Source PDF URLs, locators, downloaded-byte hashes and extractor version are in SOURCE_LEDGER.json; foreign copies remain ignored. EARLY_SEAL.json and FINAL_SEAL.json bind the written independence and final report. MANIFEST.json excludes itself and ignoredtmp and records hashes of all own artifacts.
