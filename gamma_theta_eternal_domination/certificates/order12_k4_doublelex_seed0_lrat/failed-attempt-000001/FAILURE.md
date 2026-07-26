# Preserved failed certificate attempt 000001

The strict full-stream binary normalizer completed successfully. It parsed
1,378,975 records, found one final empty addition, rejected no malformed
encoding, removed 738,121 deletion records, and wrote the addition-only
candidate stream. The subsequent *extra* raw-stream forward diagnostic,
which was stronger than and unnecessary for the requested pipeline, exited
80 under warning-fatal mode at the start of forward verification.

This attempt made no proof claim. Its exact normalized candidate, report,
stdout, stderr, child-resource records, and run lock are preserved here. The
production pipeline was corrected to use the soundness chain actually
required for a deletion-bearing raw stream:

1. strict full-stream parse and addition-only normalization;
2. warning-fatal RUP-only forward replay of the normalized stream;
3. warning-fatal RUP-only backward LRAT conversion; and
4. fresh `lrat-check` replay.

No frozen instance, theorem, source, test, review, solver-result, or raw-proof
artifact was modified.
