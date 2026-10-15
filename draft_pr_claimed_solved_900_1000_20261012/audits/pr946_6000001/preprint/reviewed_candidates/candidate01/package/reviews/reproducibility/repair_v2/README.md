# Use the repaired PR946 replay tools

Authenticate the final v2 manifest from a trusted separate record, then authenticate these four regular tooling files before executing the launcher:

- `launch_portable_gate.py`: `0199b8c7c481527121813c6d3c57a5acd2e598e8a5223acba69eb2161235d3b8`
- `portable_gate.py`: `65f2d6b7f96f9994d073d7bf3741af5dcfc92ac6fe9f9aaadf224d25016e5b57`
- `portable_worker.py`: `fe5a88a4e5c5a8a6e95ad4b729a0427366f33eabbb512017a06ce362e2739fa2`
- `compare_results.py`: `85c7a936c3333a6dc283bb46525589f21ab11584f0cde88c745286fb364bbd4b`

Keep the four tools outside PACKET. PACKET contains exactly the original unchanged 33 files rooted at PUBLIC_MANIFEST.json. SCRATCH is an existing writable real directory with no linked ancestor. Use the existing Python environment with SymPy 1.14.0 and NumPy 2.3.5; the tested Python version was 3.14.6.

```sh
python -I -S -B /absolute/path/launch_portable_gate.py /absolute/path/PACKET \
  --gate /absolute/path/portable_gate.py \
  --gate-sha256 65f2d6b7f96f9994d073d7bf3741af5dcfc92ac6fe9f9aaadf224d25016e5b57 \
  --worker /absolute/path/portable_worker.py \
  --worker-sha256 fe5a88a4e5c5a8a6e95ad4b729a0427366f33eabbb512017a06ce362e2739fa2 \
  --comparator /absolute/path/compare_results.py \
  --comparator-sha256 85c7a936c3333a6dc283bb46525589f21ab11584f0cde88c745286fb364bbd4b \
  --scratch /absolute/path/SCRATCH
```

The launcher itself must already be a trusted regular script. It safely rejects FIFO gate, worker and comparator arguments before executing those inputs. Do not give an untrusted script path directly to Python and expect script code to validate the interpreter's earlier open. All tooling inputs have a 262,144-byte cap; original packet files have their exact known-size limits.

Outer O/OO are supported; workers remain zero. The isolated poisoned-environment run has actual outer zero, not two. The original strict replay failure and missing native turn provenance remain documented in the unchanged v1 report. ADDENDUM.md explains the repair, executed checks and trust assumptions. No OS sandbox is supplied.
