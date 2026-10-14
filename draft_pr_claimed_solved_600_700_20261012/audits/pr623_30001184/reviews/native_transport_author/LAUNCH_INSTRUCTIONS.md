# Parent launch after fresh independent acceptance

This invocation captures the reviewed launcher once, checks its frozen SHA-256 before any launcher statement executes, and executes those same bytes. The launcher does the same for the adapter, which does the same for the repository kit. The approved inline Python text is the root of trust; no cached local module is reused.

Replace only the command/authorized flags on the first line. This author performed local checks and read-only preflight only. Do not enable stage/publish before the fresh independent review is accepted.

```sh
python3 -B - check <<'PY'
import hashlib
from pathlib import Path
import types
path = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/audits/pr623_30001184/reviews/native_transport_author/run_native_transport.py')
source = path.read_bytes()
if hashlib.sha256(source).hexdigest() != '16ac53b7127971de17c0948783fbc23ccc6854c7720e7e63cbd585305df7bf3b':
    raise SystemExit('Reviewed bootstrap differs; nothing was executed')
module = types.ModuleType('__main__')
module.__file__ = str(path)
exec(compile(source, str(path), 'exec', dont_inherit=True), module.__dict__)
PY
```

Other first-line choices after acceptance:

```text
python3 -B - preflight
python3 -B - stage --execute-own-draft --confirm-id 23356540
python3 -B - inspect
python3 -B - publish --execute-own-draft --confirm-id 23356540
python3 -B - inspect --check-doi
```

Keep the same captured/hash-checked here-document after each first line. Preserve the native journal after any interrupted/unknown write. Inspect makes no API mutation but the kit may save a locally confirmed publication receipt.
