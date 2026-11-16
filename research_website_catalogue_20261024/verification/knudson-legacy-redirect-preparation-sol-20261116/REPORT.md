# Knudson private legacy redirect preparation

**Private exact-article payload prepared; no execution authority.** `redirect.html` is intended solely to replace `docs/papers/knudson-gradient-path/index.html` after separate root review and live-target verification. The target is still not live-verified: https://aleckriebel.com/research/knudson-persistence-gradient-counterexample/

The genuine old article is the frozen 9,900-byte body, SHA256 `dfd99fb66a6af4ccbaa1e7d68be154b5b6584ebb848f8656916471ece0a0b3fb`, Git blob `57052af62f42198bba171d9ad3b955e74bc15572`. Its exact canonical is `https://aleckriebel.github.io/Math/papers/knudson-gradient-path/`. Actual whole old HTML and the frozen 15,708-byte staged target were personally read. INITIAL.json snapshots all seven old IDs, the explicit `#verify` link, all twenty staged target IDs, and exact source pins. The staged and adopted private MAIN remain byte-identical: 9,364 bytes, SHA256 `09e06ef22ff8a17c84b1a7e4eb7d2e6cd758cce01028329d9091dc47816d0377`. No copy or anchor was added to either page.

The seven root-supplied semantic mappings are:

| Old ID | Target ID | Rationale |
| --- | --- | --- |
| `example-title` | `result-heading` | Old filtration/counterexample heading maps to the new filtration and counterexample heading. |
| `graph-title` | `result-heading` | Old SVG title names interval a–c–d–b; new result text describes that same interval graph. |
| `graph-desc` | `result-heading` | Old SVG description gives vertices and filtration times; new result text gives the interval and exact filtration order. |
| `fixed-title` | `cancellation-heading` | Old fixed-field section explains why cancellation changes the field; new cancellation heading and text retain that distinction. |
| `verify` | `downloads` | Old explicit #verify navigation is the verifier/download section; new downloads section supplies the original source-and-verification ZIP. |
| `verify-title` | `downloads-heading` | Old verifier heading maps to the new original-files-and-citation heading, including the original verification ZIP. |
| `status-title` | `scope-heading` | Old attribution/scope heading maps to the new scope, credit and priority-limits heading. |

The payload uses one fixed HTTPS destination and `location.replace`. It concatenates the current query without parsing it. The original raw hash is retained unless one URI decoding succeeds and finds a case-exact own property among the seven known IDs; unknown IDs, prototype-property names and decoding failures fall through unchanged. Destination IDs are fixed values. No input becomes markup or a destination host.

The head supplies the canonical, `noindex, follow`, and a zero-second refresh inside `noscript`; an ordinary body link points to the same canonical. The no-script refresh cannot race the JavaScript navigation. No-script fallback and ordinary link use the fixed canonical; query/hash preservation and known-fragment mapping are not certified for that fallback. No old article body, asset or catalogue redirect is duplicated.

Verification was a single bounded inline data comparison for source pins, seven-to-twenty ID coverage and exact MAIN preservation, followed by reading the complete actual payload and static inspection of the HTML/JavaScript. No saved helper, JavaScript runtime, browser, renderer, live HTTP check, scientific/native program or old helper was run. Source pins were checked unchanged at sealing.

Only this new private folder was written. No W/docs/Git/API/Sheet/source mutation, deployment or external-human contact occurred. Root must separately verify the actual live destination and authorize any later exact article replacement. The prepared payload grants no production authority. Completed 100% private preparation at 2026-11-16T14:15:27.788145+00:00; quiescent.
