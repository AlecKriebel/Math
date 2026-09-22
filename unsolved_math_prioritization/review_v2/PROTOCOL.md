# Individual five-turn desk review protocol

Review every assigned record individually. This is a short semantic desk review,
not a solution attempt or a keyword scoring exercise. No external communication.
The target is a full novel proof/counterexample in five substantive turns of
ChatGPT6 Astra, with modest exact checks only. Exclude large exhaustive searches
from the working queue. Do not guarantee success. No favored collection, including
Kourovka, receives an automatic bonus.

Read the complete statement in each input batch, metadata, upstream research
summary and any available remaining-gap excerpt. For missing definitions or a
truncated prior gap, inspect the full cached record when it matters. Source status
is evidence, not a verified theorem. Already-solved or claimed-solved entries get
a short exclusion/review disposition, never a new proof claim. The user clarified
the inclusion filter: exclude already-solved problems; keep unresolved ones.
Review all statuses so every record has an individual disposition.

Output a JSON array to `reviews_<shard>.json` (append safely by reading the prior
array, extending it, then atomically replacing it). Each record has:

- `id`: exact string numeric upstream ID.
- `impact`: integer 1–10, cardinal utility (1 narrow fact, 3 substantive specialist
  contribution, 5 field-level technique/result, 7 major bridge, 10 foundational).
  Difficulty does not by itself establish impact.
- `p_solve`: subjective probability of full, independently checkable resolution
  in five turns, conditional on valid/open scope. Prefer restrained bands such as
  0.0001, .001, .005, .01, .03, .08, .15; >.15 requires a particularly concrete
  short proof route. Not an empirical model calibration.
- `p_valid_open`: probability the exact target is well-posed, unresolved and novel
  based on the supplied evidence; uncertainty is allowed.
- `route`: `proof`, `hybrid`, `large_search`, or `unclear`.
- `decision`: `candidate`, `defer`, `exclude`, or `repair`.
- `note`: one concise, individual sentence (roughly 15–35 words) naming a plausible
  proof mechanism AND the central obstacle, or the specific exclusion reason.

Use upstream difficulty as imperfect evidence; age may raise impact modestly but
also signals resistance. The parent applies a bounded, disclosed age modifier to
impact separately. Do not double-count age or give L1/L2 blind trust. Historical
original statements, AI partial-result titles, and bundled questions are traps:
score the entire exact target, not a convenient subcase. A reduction to an equally
hard unknown is not a route. Computational objects do not imply exhaustive search
is required: distinguish structural proofs from enumerating enormous spaces.

Process all records, including low-priority/solved/malformed entries. Do not use
code/regex/template rules to write the semantic notes or pretend the work is
finished early. Code may package your individually authored scores/notes. Each
batch is small enough to reason over in context. Checkpoint every batch. Report
counts and any important pattern to the parent. Only edit your assigned output
and optional `log_<shard>.md`; other files are shared and owned by the parent.
