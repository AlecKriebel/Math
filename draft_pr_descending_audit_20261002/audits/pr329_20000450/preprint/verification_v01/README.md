# Full fifth torsion of the regular-pentagon pencil

Companion verification materials for Alec Kriebel's research note. The theorem concerns the explicitly scaled regular-pentagon side product in manuscript.tex, the circle Q=X^2+Y^2-T^2, the pencil P+lambda*T*Q^2, and origin [0:1:0]. Characteristic zero is assumed. The exact elliptic finite range is lambda outside {0,-5sqrt(5),-phi^5}. Field assertions concern lambda in K=Q(sqrt(5)), or the explicitly stated generic base K(lambda).

Extract the archive to a new folder. With Python 3.10 or later and SymPy 1.14.0 available to that interpreter, run:

    python3 -B verify.py

For the independent arithmetic identity, norm, matrix and finite-field controls alone, no third-party package is needed:

    python3 -B verify.py --suite arithmetic

The complete integrity inventory is checked in both modes. Full mode runs nine positive programs and four deliberately false arithmetic variants; arithmetic mode runs one positive program and the same four variants. Actual child exits, empty stderr and complete mathematical output equality are required. No network access, package installation or writes inside the extracted bundle occur. Python optimization (-O/-OO) is explicitly rejected, including direct execution of the exported assertion-based programs. To select another interpreter use --python /absolute/path/to/python.

programs/ contains the original candidate checker and independently developed source geometry, quotient geometry, normalization, generic chord law, direct finite group law, twist/model, optional quintic factor and arithmetic controls. PORTABILITY.json pins every original body and describes the public derivative exactly. Guards protect assertions; the optional quintic program reads the included independently derived coefficient record. The historical originals remain unchanged. expected/ contains complete mathematical outputs. Only explicitly declared native UTC metadata and the chord program's interpreter provenance field are omitted from deterministic comparisons. Version numbers, coefficients, counts, signs, boundary statements and all other mathematical fields are compared.

The classical full-level modular cover remains a cited mathematical input; symbolic identities and finite-field samples do not independently prove its moduli interpretation. SUPPLEMENT.md records the universal reasoning, strongest verified results and limitations. SOURCE_REFERENCES.json identifies the actual primary versions and operative reading scopes. The bounded priority report documents literature and chronology limits; absence of a matching search hit is not a firstness or continuing-openness certificate. Raw third-party PDFs, scans, full primary quotations, private imported reports, dependency installations and private native audit records are omitted. Hashes verify integrity relative to the supplied package, not historical authenticity or human peer review.

The source already observes the infinity subgroup. This package computes the full25-point kernel and division field for the specified regular-pentagon model. Nonregular/star variants, arbitrary torsors without a rational point, local solubility and Tate-Shafarevich constructions are outside the theorem. Finite-field controls include boundary cases in other characteristics as counterexamples to extrapolation; they do not extend the characteristic-zero theorem.

AI tools were used extensively in derivation, computation, literature research, writing, reproduction and adversarial review. The note is unrefereed; automated reviews are not independent external human peer review, and no human peer review or formal proof-assistant certification is claimed.
