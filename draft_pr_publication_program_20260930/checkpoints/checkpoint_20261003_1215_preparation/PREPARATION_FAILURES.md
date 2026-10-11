# Preparation failures and source corrections

No proposed checkpoint helper was executed. No failure below is an actual ROOT checkpoint attempt or approval.

The first metadata-inventory tool wrapper was rejected before subprocess launch with `SyntaxError: missing ) after argument list`. Its JavaScript wrapper was corrected. There was no child PID or filesystem output to invent.

A read-only inventory calculation then rejected a manifest member before SCOPE publication. The returned diagnostic was:

```
Traceback (most recent call last):
  File "<stdin>", line 24, in <module>
  File "<stdin>", line 21, in family
AssertionError
```

The actual closed PR48/49 manifests omit per-member mode fields; their frozen files have full0444 modes. The calculation was corrected to require observed0444 only when the manifest has no explicit mode field. Explicit integer and octal-string modes were still checked exactly. Every selected manifest body/member was subsequently checked, and the exact SCOPE catalogue was published. This was preparer filesystem metadata work, with no Git mutation or proposed checkpoint execution; no capture PID/clock is reconstructed or claimed.

ROOT personally read the initial unexecuted production source and identified excessive retained readonly index stdout. The source now truthfully hashes complete readonly enumeration stdout in memory without retaining it, keeps full stderr, and adds disk preflight bounds. This is a source-review correction, not a runtime failure. Further text inspection corrected phase-specific prelaunch names and restored the new index lock's full mode after body flush. No historical mathematical/operational capture or closed family was changed.
