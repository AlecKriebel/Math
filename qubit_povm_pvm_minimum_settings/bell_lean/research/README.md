# Optional numerical discovery

`rank_three_discovery.py` records the floating-point experiment that suggested
the coupled direction in `docs/RANK_THREE_STRESS_TEST.md`. It requires NumPy.
It is not part of the verification suite, and its output is not used to accept
any exact result. No numerical result is substituted for a symbolic identity.

The reproducible verification command, using the existing SymPy dependency, is:

```bash
python3 scripts/semantic_audit.py --suite saddle
```
