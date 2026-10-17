# Detached reconstruction replay entry-point correction

2026-10-17. The root found a nonmathematical replay-instruction defect after
the source-only adversary sealed its report: its orchestrator used a relative
scratch path both as a subprocess working directory and as a script prefix.
Thus the report's relative-scratch command fails. Absolute source, scratch and
output paths work; the root used them for the complete fresh successful replay.
No mathematical statement or sealed result changes.

`reconstruction_replay.py` is the corrected current entry point. It resolves
paths before calling the unchanged sealed orchestrator and rejects overlapping
source/scratch directories; any output must remain inside scratch. From this audit
folder, a complete fresh replay is:

```text
python3 reconstruction_replay.py --source reviews/source_question_family --scratch _local/reconstruction_replay --output _local/reconstruction_replay/RESULT.json
```

The arithmetic-only write-free worker is available with `--worker`. It performs
finite diagnostics, not authentication or the entire mutation suite. The full
orchestrator copies the sealed checker into scratch and checks all three Python
modes and 18 deliberate mutations. Historical reports and scripts remain exact;
read this correction alongside the earlier relative-path instruction. Portable
release replay instructions will identify their precise supported entry points.
