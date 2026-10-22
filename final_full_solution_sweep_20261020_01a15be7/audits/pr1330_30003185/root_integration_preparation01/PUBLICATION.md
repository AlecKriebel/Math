# Current paper and preserved historical reader

The current paper is **Logarithmic Bray sampling in symplectic and orthogonal groups**, Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X), v1.0.0, 22 October 2026. Read the complete [11-page paper](publication/bray-sp-o.pdf) and [editable source and reproduction instructions](publication/source/README.md). The [source archive](publication/bray-sp-o-source-and-verification.zip), [upload kit](publication/bray-sp-o-upload-kit.zip) and metadata are the same reviewed package. A DOI is not assigned by this pointer; publication and recording require separate verified actions.

For every odd prime-power q and all sufficiently large natural dimensions n, for every actual prescribed strong involution t in natural Sp, O, SO or Omega, the paper proves separate unconditional c/log n strong-eigenspace marginals for inv(tt^g). Each eigenspace event is separate. The bounds are 1/(40000 log n) in Sp and 1/(5000000 log n) in O/SO/Omega; the exact half-spinor refinement supplies the admissible orthogonal event. With confidence at least 1-delta, O(log n(1+log(1/delta))) independent uniform samples generate a subgroup containing the actual C_G(t)''. This is a group-sample bound, not a total-runtime theorem. The generation threshold is absolute and existential. No all-dimension, characteristic-two, projective/order-four-lift, similitude, simultaneous-strength or fixed-multiplier vanishing-error extension is claimed.

GL/GU are prior work of Dixon-Praeger-Seress and Glasby-Praeger-Roney-Dougal; their methods and earlier class-generation/diagonal-escape strategies are credited. The current paper's claimed contribution is Sp/O. The exact original question is OWR37/2016, pp2160-2161. The [dependency map](publication/source/DEPENDENCIES.md) states the precise published Burness/Liebeck-Pyber-Shalev imports and standard classical-group background. Their entire foundational proofs are not re-certified here. The [priority note](publication/source/PRIORITY.md) reports bounded comparisons; no worldwide-firstness certificate or unread-edition identity is asserted. An inspected preprint is not silently substituted for an inaccessible publisher body.

AI tools were extensively involved in mathematical research, proof development, computation, manuscript preparation and adversarial auditing. This is an unrefereed preprint and has not undergone formal independent human peer review. Prose is CC BY4.0 and code is MIT, as supplied in the package.

The original PR's 33 files under corrected_reader/ (27) and public/ (6) are preserved byte for byte as a historical edition, including conditional bridge text, source corrections and recorded finite outputs. Their manifests inventory those exact subtrees; the 27-file and six-file counts do not describe this expanded project or the current publication/source/ directory. They contain no distributed verification programs. Their historic finite-execution reports are recorded evidence, not a new execution claim for the complete earlier suite. Do not relax their manifests to ignore additional files or apply a subtree manifest to the whole project.

For the current independent finite diagnostics, use only the dedicated 14-member scientific source directory:

    cd publication/source
    python3 -I -S -B exact_checks.py --expected CHECK_RESULTS.json
    python3 -I -S -B -O exact_checks.py --expected CHECK_RESULTS.json
    python3 -I -S -B -OO exact_checks.py --expected CHECK_RESULTS.json
    python3 -I -S -B build_release.py --output /an/absent/bray-release

The release builder verifies its exact source namespace and reproduces six release products from the frozen PDF; it does not compile TeX or prove the theorem. Use an absent output directory. Finite diagnostics substantiate selected interfaces and cannot establish the universal theorem by enumeration. Compilation, historical evidence, package reconstruction, current mathematical review and live publication checks have distinct scopes.
