# Independent reconstruction before any previous verdict/report

The literal target asks for a Markov formulation in which all braid states have even strand count. The current manuscript chooses ordinary oriented unframed closure and supplies both classical and virtual cases. The source must be checked for context that would require a stronger notion of local moves or another closure.

The proposed mechanism is a path transport, not an invariant computation: map an unrestricted tagged braid (m,w) to itself if m is even, or to (m+1,w sigma_m) if m is odd. This map preserves closure and fixes the desired even-state endpoints. A known complete unrestricted Markov path therefore gives an even path if every unrestricted edge has a valid explicit lift.

Independent edge table:
- Fixed-count defining relation: apply it unchanged in the old context, retaining sigma_m if the count was odd. All relation indices remain valid under right inclusion.
- Conjugation b -> a b a^-1: use C at even count. At odd count use BC because a and b have indices <= m-1 and the newly appended sigma_m is separate.
- Stabilization (m,b) -> (m+1,b g_m): at even m the target is odd, giving (m,b) -> (m+2,b g_m sigma_(m+1)) = D; at odd m the source is padded, giving (m+1,b sigma_m) -> (m+1,b g_m) = T. Signs and virtual stabilization matter; inverses of these arrows handle destabilization.
- Right virtual exchange at total count m: a sigma_(m-1)^-1 b sigma_(m-1) <-> a v_(m-1) b v_(m-1), with indices(a,b)<=m-2. This is R at even m, BR at N=m+1 at odd m; the BR block bound becomes N-3.
- Left virtual exchange at total count m: shift only the old a,b by one; the exchange uses index 1. This is L at even m and BL at N=m+1 at odd m. At odd m the shifted blocks reach N-2, so the retained sigma_(N-1) may fail to commute with their end generators. The proof must not commute that tail. The displayed BL formula appends the tail without commuting it and is the direct edge image.

Soundness is separate: C is unrestricted conjugation; BC stabilizes two conjugate odd prefixes; T compares allowed stabilizations of one odd prefix; D is two allowed stabilizations; R/L are unrestricted exchanges; BR/BL stabilize both exchange endpoints. No use of unrestricted completeness is needed to prove this direction.

Boundary obligations: m>=1 suffices for nonempty links. The one-strand empty word pads to (2,sigma_1), the unknot. Empty words with distinct positive even tags represent different unlinks, so tags must be preserved. At N=2 the BC blocks are empty and R/L are trivial; odd exchange first occurs at m=3, giving BR/BL N>=4. A separate zero-strand empty state would represent the empty link. A supplied unrestricted certificate max count M maps to max count 2 ceil(M/2); no chain-search complexity follows.

Initial hypothesis: the theorem is a correct conditional consequence of the exact classical and virtual imported Markov presentations. Remaining critical checks: exact source Problem42 context, exact signs/shift/support of Kamada's two exchange directions, source priority and accessibility, code/theorem scope, archive reproducibility, PDF visual integrity, licenses and metadata. No conclusion about novelty can be deduced merely from this elementary mechanism.
