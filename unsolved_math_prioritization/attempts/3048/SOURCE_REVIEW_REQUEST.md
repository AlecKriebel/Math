# Independent source-resolution review request

Review the proposed already_solved 0/5 disposition for 3048 / OPG-37226. This is a literature-verification packet, not a new five-turn proof search. No new theorem or historical priority is claimed.

Read SOURCE_STATUS.md and the original OPG statement. Check the exact flattening operation: both rows contribute their entries once, and the lower row is not initially used as multiplicity weights. Confirm that canonical frequency tables lift a multiset cycle to an array cycle after one step, without enlarging its period. Positive integers are atomic, with no splitting into decimal digits and no bounded-label assumption.

The publisher's record for Eliahou–Erickson (2013), DOI 10.1016/j.disc.2012.11.014, explicitly states eventual periodicity for nonnegative multisets and period at most three. Full 2013 text was not retrieved. The accessible primary PDF arXiv:2004.00209v1 is local under sources. Section 3 defines f(S)=[S]+mu(S); Corollary 4.5.1 gives eventual periodicity, and Corollary 5.5.1 on p10 states that every cycle has at most three terms. Theorems 5.3 and 5.5 supply its classification. Check those source hypotheses and the distinction between cycle period and number of entries. No independent certification of all source classifications, external figures or the stronger numerical preperiod bound is claimed.

Run python verify_source_alignment.py and compare stdout exactly with SOURCE_CHECKS.json. Its finite cases only test formulation consistency and examples. Verify the frozen manifest and source hashes. Please give an explicitly scoped PASS or FAIL for the source-backed disposition, including any required correction or residual access limitation. Preserve frozen bytes.
