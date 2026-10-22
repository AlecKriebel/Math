# Slowly growing image inradius: accepted qualified partial work

Problem **2305005 / AMR-022-5005**, rank **1034**. Status: **unsolved, 5/5 substantive proof-attempt turns**. This is a source-free publication of unchanged author work and its independent acceptance audit, with a separate integrity/replay wrapper.

## Mathematical scope

The slowly widening polar-complement domain D has d_D(r) tending to infinity and an arbitrarily prescribed divergent upper envelope. The domain theorem attributed to Fernández in the inspected Hayman–Lingham collection supplies some holomorphic map into D with unbounded Taylor coefficients. Its actual image need only be a subset of D. The construction does **not** establish that this map's own inradius d_f(r) tends to infinity. Domain inradius, actual-image inradius, a divergent limsup, and a divergent limit are distinct assertions.

The upper-envelope-only obstruction is **conditional on the historical theorem as stated in the inspected collection**. Fernández's original full proof was unavailable. No onto version of that theorem is asserted or verified. Consequently the literal-limit problem remains unresolved in this investigation.

Other accepted partials are the Bloch/Cauchy bounds; dense onto approximation with the required coefficient-category density explicitly unproved; the logarithm-squared Cayley-map parabola example, whose coefficients decay; and the lacunary candidate's entire-plane image obstruction. [PR #807](https://github.com/AlecKriebel/Math/pull/807) concerns a different shrinking-inradius/decay target.

Read [the publication acceptance summary](ACCEPTANCE.md), [the complete author report](author/REPORT.md), and [the independent audit](audit/AUDIT.md). There is no full solution, originality certification, or worldwide current-openness certification.

## Frozen evidence and chronology

The eight files in `author/`, five files in `audit/`, their original ZIP archives, and both original freeze receipts are byte-preserved. Historical author statements that an audit was pending, and historical flags saying publication had not occurred, record the original freeze. The subsequent independent audit accepts the qualified partials unchanged. This wrapper supplies the current publication context without rewriting that history.

Only authored mathematics, authored audit materials, finite fixtures, and public verification metadata are included. Source documents, dataset contents, and private coordination material are absent. Historical corpus/record/PDF byte matches remain historical evidence; a default public replay does not reproduce those absent inputs.

## Trust and replay

Use Python 3.12+ as an ordinary nonroot POSIX user. Obtain the SHA-256 of `BOOTSTRAP.py` independently from the PR description or verified commit, verify it **before executing any packet code**, then run:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

The bootstrap pins the publication manifest and verifier. The verifier checks a closed recursive inventory, exact file lengths/hashes, unchanged acceptance pins, both ZIP member inventories and bytes, strict JSON parsing including duplicate/nonfinite/overflow rejection, and exact integer and boolean types. It replays 6,806 author finite checks and 63 author negative rejections, plus 20,510 independent finite checks and 111 independent negative rejections. Accepted scripts are executed only after authentication, with a sanitized environment and a read-only working directory. Direct verification uses a read-only copy; corruption harnesses use disposable writable fixtures and independently exercise genuine nonroot read-only copies. Fresh outputs are compared by exact types and values against the frozen historical expectations, adjusted only for the actual nonroot UID and the intentionally absent source inputs.

After authenticating the bootstrap and checking `mutation_tests.py` against its authenticated manifest entry, run the publication-level controls in each mode:

    python -I -S -B mutation_tests.py --root . --bootstrap-sha256 TRUSTED_BOOTSTRAP_SHA256
    python -I -S -B -O mutation_tests.py --root . --bootstrap-sha256 TRUSTED_BOOTSTRAP_SHA256
    python -I -S -B -OO mutation_tests.py --root . --bootstrap-sha256 TRUSTED_BOOTSTRAP_SHA256

Each invocation checks corruptions, schema/type boundaries, archives, linked roots/ancestors, read-only relocation, and hostile Python-import environment/working-directory controls in its selected mode. The same frozen author/audit harnesses also check their own three-mode controls.

Fresh source bindings, original Fernández-proof verification, and analytic existence-proof computation are explicitly `NOT_RUN`. Finite controls and hash matches do not prove the analytic existence statements or close the remaining gap. No network access, package installation, repository write, merge, release, or DOI registration is performed by these scripts.
