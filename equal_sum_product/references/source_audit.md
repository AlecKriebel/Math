# Source and later-result audit

Date: 14 September 2026. The public sources were inspected using the web tool.

## Primary records inspected

1. Erich Friedman, *Problem of the Month (November 2002)*,
   https://erich-friedman.github.io/mathmagic/1102.html
   The definition requires globally distinct positive integers, common row
   sums, and common column products. The additional question requires the
   two common values to agree. The page attributes the two-row example and
   the conjecture excluding other row counts to Joseph DeVincentis. Its
   two-row entries are transcribed in `certificates/source_two_rows.json`.
2. Erich Friedman, *Unsolved Problems from Math Magic*, item 8,
   https://erich-friedman.github.io/mathmagic/unsolved.html
   At inspection, the list continued to display the equality-case statement
   as a conjecture.

## Executed queries

Before any construction search, followed by a second audit after finding the
proof (no large construction search was ultimately necessary):

```text
"Joseph DeVincentis" "sum" "product" matrix
"sum-product matrices" "rows" conjecture
"sum-product" "DeVincentis"
"sum-product matrix"
"sum-product matrices" -site:patents.justia.com -"SCALAR INJECTION" -"Theory Problems" -"Template Numerical"
"common sum" "common product" "two rows"
"DeVincentis" "matrices" "conjecture"
"sum-product matrices" proof
"sum-product matrix" "reciprocal"
"1102.html" "proof" "sum"
"sum-product matrices" "proof" -patents
"DeVincentis" "reciprocal"
"DeVincentis" "matrices" "solved"
"Friedman" "sum-product" "inequality"
```

The relevant results located were the original page and its separate
unsolved list. Other returned hits concerned matrix-ring sum-product
estimates, sum-product networks, unrelated DeVincentis mentions, or unrelated
uses of the words. None supplied a later resolution of this exact target.
No unrelated result is used as evidence for the mathematical theorem.

## Limitations

The search does not establish exhaustive historical novelty. A prior proof
could be unindexed, differently described, or private. The mathematical
conclusion is established by the supplied direct proof, not by the source's
current status. No private correspondence, independent external review,
publication, or communication was undertaken.

No copyrighted source page is redistributed; the references, factual
mathematical statements, and numerical controls suffice for reproduction.
