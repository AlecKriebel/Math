# Proposed focused verification repair

Do not change any frozen original bytes as part of this review. In a subsequent verification-only revision, put this guard at the beginning of each executable, before computations and result writes:

```python
import sys

if sys.flags.optimize:
    raise SystemExit(
        "Verification requires assertions enabled; run Python without -O/-OO "
        "and without PYTHONOPTIMIZE."
    )
```

An explicit conditional remains effective under optimization. Merely adding another assertion would repeat the defect. Updating all 82 assertions to explicit checks is a stronger alternative, but the guard is sufficient to prevent false certificates from the supported entry points.

After the revision, ordinary outputs must remain byte-identical to the frozen historical JSON. `python -O` and `PYTHONOPTIMIZE=1 python` must exit nonzero before writing any result file. Re-run the five preserved fault controls to show that no unsupported mode emits success. Document the supported command and the exact Python/SymPy versions used. No new mathematical search or extra author proof attempt is required for this repair.
