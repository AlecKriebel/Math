# Bounded priority search ledger

Date: 2026-10-21 UTC. Purpose: independently verify the supplied source leads and test the exact older-example implication; not an exhaustive current-literature review.

The following six search strings were used in two web search calls:

1. `"Theorem H" "Fang" "IM" entire functions`
2. `"IM" "b" "k" "Fang" "Zalcman" "2003" entire functions`
3. `"Normal families and uniqueness theorems for entire functions" "273" "283"`
4. `"Redundant Picard-Fuchs system for Abelian integrals" Novikov Yakovenko 2001`
5. `"IM" "Fang" "k" "b" "Sauer" Schweizer 2026`
6. `"IM-Sharing" "Theorem H"`

The first call recovered the original EMS report and substantial unrelated work using other “Theorem H” labels. Those unrelated results were not used as evidence. The second call recovered the Fang–Zalcman publisher search metadata, arXiv metadata for Novikov–Yakovenko, and an institutional bibliographic record. The targeted 2026 string did not return a sufficiently identified relevant primary body; no assertion about a 2026 result is made in this review. Raw second-call output is preserved privately in `sources/BOUNDED_SEARCH_2_RAW.json`.

Direct source operations, independent of search ranking:

- Opened and independently downloaded the supplied EMS publisher PDF. Read the full relevant contribution, printed 501–503; visually inspected 502–503.
- Opened and independently downloaded the supplied IM PAN publisher PDF. Read all nine pages for scope; visually inspected printed 68–69 and 75. The direct older-family implication uses Example 1 on 68. The functional-template comparison uses Theorem 1.2(d) on 68–69. The issue and received/final-form dates are visible in the primary body.
- Opened and independently downloaded the Cornell author PDF. Read Section 5.4 and its short proof; visually inspected author pages 1 and 27. Read the cited Chademan bibliographic entry. No original Chademan full text was obtained.
- Opened arXiv metadata, then independently downloaded the explicitly versioned `math/0001111v1` PDF. Visually inspected its author page 26. The same shape theorem occurs as Proposition 5 there; it is Proposition 7 on author page 27 in the byte-distinct Cornell author file. The arXiv submission date is 20 January 2000; both bodies have internal date 19 January 2000. Full unrelated Picard–Fuchs arguments were not reviewed.
- Opened the Fang–Zalcman 2003 publisher page; direct open returned HTTP 403. Its full body was not obtained. Publisher search metadata/abstract were seen. They are not substitutes for a full-body read.
- Opened the Chang–Fang publisher abstract and downloaded its HTML. Read the abstract, received/accepted/online/issue dates and scope. It is a nonzero-a, same-value result. Full body was subscription-only through this route.
- DOI redirects for the 2009 paper and 2007 report were not accessible through the web tool, but the independently retrieved publisher PDFs themselves supplied the required body evidence. Web screenshots of the EMS PDF failed; local Poppler renderings supplied visual verification.
- An attempted IM PAN landing-page route was inaccessible. It was not used for any content claim; the supplied publisher PDF route succeeded.

Positive result: the dated 2009 Example 1 family at B=2b directly gives a full target k=2 counterexample by differentiation, independently of its different printed predicate. This establishes already available counterexample material for the original universal assertion.

Limits: no verified earlier paper explicitly naming the identical OWR question; no earliest-recognition claim; no firstness certificate for exact all-order target-specific classification or resonance parameter; no conclusion that nonzero-a or transcendental-k=2 restrictions are open in all current literature. These limits do not weaken the direct positive implication above.
