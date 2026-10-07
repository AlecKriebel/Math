# Deterministic algorithms over represented finite fields

This is an unpublished, attributed research and verification record. It establishes the explicit finite-field consequences of OpenAI's prime-field factorization theorem on the mathematical proof-review basis recorded in the dependency ledger. It does not claim a new independent prime-field solution or new Berlekamp/Shoup/Rai machinery. Production Zenodo publication and tracker insertion are withheld because the priority audits have not established a genuinely new in-scope extension.

## Exact result and limitations

Let p be a promised or checked prime in binary, h a supplied monic irreducible polynomial of degree m>=1 over F_p, K=F_p[t]/h, and f a nonzero dense degree-n polynomial over K. The reductions return the leading coefficient and distinct monic irreducible factors with all multiplicities, using at most mn prime-factor calls (trace version) or n calls (direct p-fixed version), of degrees at most n, with polynomial nonoracle overhead in n,m,ceil(log2 p). Squarefree and inverse coefficient Frobenius handling include p=2, repeated factors and m=1. Constants have no factors; zero is rejected.

Shoup's published reduction constructs prescribed-degree irreducibles over F_p. The also-published degree-md lift then constructs a degree-d irreducible over the supplied K and hence the explicit quotient extension K[x]/g. Degree d is a numeric dense-output parameter, not log d. These deductions require no integer-factorization oracle, primitive root, randomness or GRH when instantiated with the cited prime-field theorem. The huge upstream branch has not been executed and no practical efficiency is claimed. Fixed-r roots follow by factoring dense x^r-a in poly(numeric r); no poly(log r) claim or new quadratic consequence is made.

OpenAI family142's required analytic input is family029 Theorem1.2 over arbitrary cyclotomic fields containing μ12. Family003's narrower Dirichlet/Eisenstein-field Lean scope is insufficient to replace it. Separate manual source audits found no substantive gap in the needed geometric and analytic proofs. This is not a formal verification; no Lean build was reproduced for this effort. Source hashes and exact proof-review limitations are preserved.

## Reading and reproduction

- manuscript/main.tex is a standalone source with inline bibliography; manuscript/paper.pdf is an actual exported five-page PDF, not merely an editor preview. REFERENCES.bib preserves the supplied upstream manuscript-specific citations.
- CURRENT_THEOREM.md and DEPENDENCY_LEDGER.md distinguish target, imported result and verified reduction.
- agent_notes/extension_reduction.md and construction_reduction.md give proofs, pseudocode, dimensions, oracle counts and bit lengths.
- agent_notes/prime_field_audit.md, analytic_dependencies.md and geometric_falsification.md record independent attempts to falsify pivotal inputs.
- agent_notes/priority_audit.md and reviews/priority_independent.md provide positively documented prior reductions and publication limits.
- code/ contains standard-library Python reference implementations, examples and exact independent comparisons. Bundled prime-root oracles enumerate p only in capped toy examples: they cannot supply the uniform prime-field theorem.

From code/, with Python 3.10 or later, run:

```sh
python3 -m unittest -v test_finite_fields.py
python3 examples.py
python3 extension_direct_verify.py
python3 extension_crosscheck.py
python3 construction_reduction_examples.py
```

The original construction-example command emits data/construction_examples.json relative to the parent project; clean reproduction instructions will copy the authored file set preserving that directory. Small tests enumerate field elements or trial divisors only for validation. Current evidence includes 377 monic input checks, 346 independent direct/trace comparisons, and six construction fixtures. These counts overlap and must not be added as disjoint coverage.

To export the PDF from standalone source, run `tectonic -X compile manuscript/main.tex --outdir manuscript`, then use the generated main.pdf. The built-in editor/compiler has also compiled the same source successfully. Tectonic and fonts are external build dependencies, not redistributed package files.

## Provenance, rights and disclosure

Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. No affiliation or coauthor is asserted. Newly authored prose, proofs, audits and data are offered under CC BY 4.0; newly authored Python code under MIT, matching the repository's established publication-package convention. See LICENSES.md and LICENSE_CODE.txt. No third-party manuscript or source tree is an intended publication attachment.

AI tools were used extensively for research, drafting and verification. Automated adversarial reviews are not conventional human peer review or refereeing. The record has not undergone conventional human peer review. Upstream AI-produced work is cited as OpenAI according to its supplied citation information. No external individual was contacted.

No Zenodo draft or public record has been created for this effort, no DOI has been assigned, and no tracker row has been written. The persistent publication goal remains incomplete. This README is not a publication receipt.
