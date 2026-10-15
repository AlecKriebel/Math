# Edition acceptance and exact scope

## Accepted complete negative result

On 9 October 2026, an independent mathematical/source audit accepted the complete negative result for the source-corrected, dimension-independent formulation of problem 30004909 / OWR-8415356-020. A separate complete reading of the proof and audit accepted the same scope.

The disproved assertion asks for one fixed alpha>0, independent of both f and the finite ground set V, such that each normalized nonnegative monotone submodular f:2^V→R has an ordinary matroid M on V with r_M(S)/alpha <= f(S) <= alpha r_M(S) for every subset S. Normalized here means f(empty)=0 and f({i})=1 for each element.

The proof f(S)=sqrt(|S|) gives alpha >= n^(1/6). At a basis of total rank R the lower inequality gives R <= alpha²; at the full set the upper inequality gives sqrt(n) <= alpha R <= alpha³. This disproves a dimension-independent constant. All function hypotheses and all degeneracies are checked in the complete manuscript.

The same manuscript determines the optimal factor within the square-root family: minimize max(sqrt(R),sqrt(n)/R) over 1<=R<=n. Uniform ranks attain this optimum, giving exact n^(1/6) sharpness when n is a cube. The rational family g_m(empty)=0 and g_m(S)=1+(|S|-1)/m for nonempty S on m² elements gives alpha²+alpha >= m and alpha >= n^(1/4)/sqrt(2). This is one basis/full-set approach with two input families.

## Preserved proof and selected audit

REPORT.md is preserved byte-for-byte: 7,119 bytes, SHA-256 0e5cc70ca135c8eb9c271ebc65019af92d62e7ade8ff24de5886de9f05721c52. No proof step, qualification or bibliographic paragraph has been replaced by a summary.

SOURCE_AUDIT.md preserves the complete mathematical/source audit except for private repository/corpus-history and deduplication details. Its replacement notice identifies that editorial selection and retains the original one-approach budget. All adversarial checks, source observations, literature-search limits and the mathematical disposition are unchanged. The selected ARTIFACT_MANIFEST.json records the actual public edition identities and omits supplementary computational and private-history identities.

## Source and acceptance boundaries

- The original source includes alpha in the denominator of the lower comparison. The proof does not exploit the corpus's missing denominator.
- The dimension-independent interpretation is explicit here; the source itself does not separately write a quantifier over V.
- Approximation is by one ordinary matroid rank on the same ground set. No result is asserted for sums of ranks, weighted ranks, expanded ground sets, a scalar-rescaled output class, or a different intended question.
- Sharpness of n^(1/6) is a statement about the square-root family only. No optimal exponent for the entire normalized submodular class is claimed.
- The separate oracle-learning problem in Goemans–Harvey–Iwata–Mirrokni is not identified with this output-restricted question or used to infer the negative answer.
- The literature search was bounded. No novelty, research-priority, exhaustive-literature or prior-current-open-status claim is made.
- AI-assisted acceptance is not external human peer review, journal acceptance or formal proof-assistant verification.

The accepted mathematical result is complete within that precise scope. Approach 1/5 is retained; no queue edit, merge or release is part of this edition.
