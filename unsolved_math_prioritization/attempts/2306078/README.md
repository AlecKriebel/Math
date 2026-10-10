# Function Theory 6.78: a complete classical consequence

Target 2306078 / AMR-022-6078, rank 686. Disposition: **already_solved**, after **3/5 substantive approaches**. The exact stated problem follows from Jacques Dufresnoy's 1941 theorem. No novelty is claimed.

For every holomorphic injective function on the open unit disk with `f(0)=0` and complex derivative `f'(0)=1`, the minimum spherical area of its image is **one half of the sphere**, uniquely attained by `f(z)=z`. This is `2*pi` for unit-sphere density `4/(1+|w|^2)^2`, or `pi/2` for density `1/(1+|w|^2)^2`. There is no extra convexity, coefficient-reality, boundedness, degree, or boundary-regularity assumption.

## Evidence and credit

- [Full authored proof](author/PROOF.md), including a direct Dufresnoy specialization and a separate univalent derivation from standard spherical isoperimetry
- [All three substantive approaches](author/APPROACH_LOG.md), including the limitations of the first two
- [Full independent adversarial audit](audit/AUDIT.md)
- [Public source verification](author/SOURCE_VERIFICATION.json) and [independent source inspection](audit/PUBLIC_SOURCE_AUDIT.json)

The governing statement is Hayman–Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), Problem 6.78, printed page 145, using the class on printed page 114. Its historical editorial update does not establish present open status.

The load-bearing antecedent is Jacques Dufresnoy, *Sur les domaines couverts par les valeurs d'une fonction méromorphe ou algébroïde* (1941), [Section 27, printed pages 218–220](https://www.numdam.org/item/ASENS_1941_3_58__179_0/). The audit independently retrieved matching complete PDF bytes and inspected the local theorem, proof, equality formula, and relevant definitions and dependencies. It did not audit the entire 82-page paper or reprove spherical isoperimetry from foundations. Injectivity identifies covering area with image-set area. The full-sphere endpoint and the complex derivative normalization are treated explicitly.

All nine author files and nine audit files are preserved byte-for-byte. Earlier statements such as “audit pending,” “publication_ready: false,” or “no remote writes” remain accurate historical records of those frozen stages. The subsequent independent audit passed without required mathematical corrections. Its numeric `already_solved = 1` is a Boolean classification, not an approach count.

## Reproduce

From this directory run `python verify_publication.py --replay --selftest`. Python 3 and SymPy 1.14.0 reproduce the exact symbolic outputs. The integrity-only command `python verify_publication.py` uses the standard library. It pins both nested manifests, verifies all original and audit bytes, and rejects extra files (including under `__pycache__`), empty directories, symbolic links, unsafe or duplicate metadata, and changed disposition or credit.

All writing control scripts run from temporary copies. The replay requires byte-identical results for 46 author checks with six algebraic mutation rejections, and 42 independent checks with eight algebraic mutation rejections. It also reruns the audit's four frozen-binding negative controls. These finite checks support the written analytic proof; they are not proof-assistant formalization or a global audit of the classical paper.

## Publication boundary

Only authored mathematics, code, audit material, and public verification metadata are included. Source PDFs/text/images, corpus records, private source files, and private coordination material are excluded. No fresh full-corpus comparison is claimed.

The queue patch changes only this row's Status to `already_solved`, Turns to `3/5`, and its previously blank Findings to the credited full-scope result. Every other queue byte, including the existing header and links, is preserved. The queue generator and other ledgers are untouched. This is a draft PR, with no merge, release, DOI, or outreach.
