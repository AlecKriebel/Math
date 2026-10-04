# Verification package: Wajnryb's fixed-generator Artin A5 quotient

This package accompanies *Fixed-generator positive factorizations in Wajnryb's Artin A5 quotient*, by Alec Kriebel (ORCID 0009-0001-9320-500X).

The exact input is a positive word in the five standard generators of B6, representing c² in the quotient by c=h. The result is four strict Hurwitz classes of lengths 20/30/40 (counts 1/1/2), or three classes with simultaneous conjugation. Arbitrary conjugate-factor or geometric factorizations are outside this input universe.

Run python3 verify_package.py with Python 3.10+ and g++ supporting C++17. It verifies the closed package manifest, all 810 length-20 action records, every one of the 90,921 length-30 certificate records, the original author/reviewer replays, and two separate backward-graph implementations. It uses only the standard library and writes generated files to a temporary directory.

The reference/ folder contains the complete immutable four-turn original candidate, including its historical manifests. Historical pending-status sentences describe their checkpoint and are superseded by the accompanying research note. The publication checker verifies the finite packet; it does not prove the cited geometric length bound or inspect source PDFs. Four substantive author turns suffice; no fifth turn is fabricated.

The certificates/ folder stores full word/action data losslessly compressed. Hashes protect bytes; they do not replace exact word equalities or the written completeness arguments. independent_20_30.py is a separately reconstructed reverse-graph and labeled-strand control, not an import of candidate code. It includes a count-vector collision outside the coaccessible graph and a relator mutation as negative controls. independent_ranks1_6.py independently uses descending generator order and explicit predecessor exploration across ranks1..6, compares every edge, and reruns the C++ certificate. Both sources and their complete expected receipts are supplied; the package verifier reruns both and compares their entire rank-six record bytes. The rank1..5 record files are additional exact controls, not a claim for rank7.

The priority report credits Matsumoto's exact group presentation, Sato's prior length spectrum, and Casson's general twice-per-pair assertion reported by Elrifai–Morton. Novelty of the exact complete orbit classification is not certified by a negative literature search. Original primary works are linked and hash-described, not redistributed.

AI tools were used extensively in development, writing, execution, literature audit, and adversarial review. This package and the accompanying preprint have not received external human peer review.
