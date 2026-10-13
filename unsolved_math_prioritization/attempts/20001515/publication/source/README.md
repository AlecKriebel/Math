# A two-cube cubulation of the AIM free-by-cyclic example

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.

This standalone LaTeX source produces the six-page research note. Compile with
`tectonic preprint.tex`, or a standard LaTeX installation supporting the packages
in its preamble. The bibliography is contained in the source; no external data
or bibliography file is required.

The note constructs a finite locally CAT(0) unit cube complex with cell counts
(1,7,8,2) and fundamental group

    <a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>.

Its universal cover gives a free proper cocompact cubical action of the exact
group in AIM Question 5.2. The positive final b matters. The nearby workshop
formula b -> aba is distinguished. The note also gives a qualitative existence
deduction using established WPD, Morse, completion, and gluing tools, with the
target-specific hypotheses checked. Historical firstness, absolute novelty,
minimal cell count/dimension, and virtual specialness are not claimed.

The accompanying verification archive independently packages the exact finite
data, three optimization-safe standard-library Python programs, historical
baseline outputs, provenance, and a driver that regenerates those outputs from
clean temporary copies. Finite checks supplement the written global proof.

Extensive AI assistance was used in discovery, drafting, and internal independent
adversarial review. This research is unrefereed, with no external human peer
review and no proof-assistant certification. Original author materials are
licensed under CC BY 4.0; see LICENSE. Foreign primary-source bodies are not
included. BIBLIOGRAPHY_POINTERS.json supplies source locators and access limits.
