# Portable replay of the unchanged PR946 original packet

Read REPORT.md before interpreting PASS. This gate supports bounded finite consistency and preserves the original strict-replay failure; it does not prove the global theorem or certify native proof-turn accounting.

Authenticate these three tooling files against a trusted separate record before executing any of them:

- `portable_gate.py`: `88906172dc1d71a99eb35f5ca1a601ba3b85d3d0f0f88f27042fb2f98ac5d026`
- `portable_worker.py`: `140e8efd37dec71df69a2935d5c54861bf20cc65091b05fb5de3735267d7cf68`
- `compare_results.py`: `85c7a936c3333a6dc283bb46525589f21ab11584f0cde88c745286fb364bbd4b`

Use a Python environment already containing SymPy 1.14.0 and NumPy 2.3.5. The checked environment used Python 3.14.6. Do not install or change an environment for this audit. PACKET must contain exactly the unchanged original 33-file subtree, rooted at its PUBLIC_MANIFEST.json; keep these tools outside PACKET. SCRATCH is an existing writable real directory with no linked ancestor.

```sh
python -I -S -B /absolute/path/portable_gate.py /absolute/path/PACKET \
  --gate-sha256 88906172dc1d71a99eb35f5ca1a601ba3b85d3d0f0f88f27042fb2f98ac5d026 \
  --worker /absolute/path/portable_worker.py \
  --worker-sha256 140e8efd37dec71df69a2935d5c54861bf20cc65091b05fb5de3735267d7cf68 \
  --comparator /absolute/path/compare_results.py \
  --comparator-sha256 85c7a936c3333a6dc283bb46525589f21ab11584f0cde88c745286fb364bbd4b \
  --scratch /absolute/path/SCRATCH
```

Outer -O and -OO are supported. Children always run at optimization zero. The optional --worker-optimize 1/2, --test-corrupt-copy and --test-false-assert switches are negative controls and must reject. Environment optimization is ignored by -I; do not call that inherited optimized assertion execution.

No network, copied scholarly source, native queue write or OS sandbox is involved. External trust anchors and the local runtime/site packages are trusted. Detailed process receipts and exact limitations are in evidence/ and REPORT.md. The curated audit manifest excludes private scratch, source bodies, runtime files and copied original packet trees.
