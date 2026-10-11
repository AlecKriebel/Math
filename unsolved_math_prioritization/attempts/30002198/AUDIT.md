# Mathematical audit of the Nichols scope correction

## Verdict and mathematical scope

The accepted proof establishes that the literal assertion about every finite-dimensional Nichols algebra, using only quantum integers in grading steps 1 and 2, is false. Its counterexample is the standard diagonal Cartan A3 construction over the complex numbers at a primitive fifth root. The result is a scope correction. It does not resolve the intended conjecture for absolutely simple Yetter–Drinfeld modules, determine that conjecture's current status, or claim novelty.

The full mathematical proof is in [PROOF.md](PROOF.md), which is byte-identical to the accepted authored proof. The complete substantive acceptance findings are retained in [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md).

## Source scope

The closing sentence of Lochmann's OWR contribution is broad when isolated. The surrounding discussion and earlier labeled conjecture restrict the setting, including absolute irreducibility. Vendramin's later notes explicitly state absolute simplicity and trace the conjecture to the October 2012 meeting. Thus the extraction loses surrounding scope; this packet does not allege deletion of a hypothesis from the closing sentence itself.

The primary scope sources are [the official OWR report, printed pp. 2901–2902](https://ems.press/content/serial-article-files/46419) and [Vendramin's author-hosted notes, pp. 6–7](https://leandrovendramin.org/notes/rauischholzhausen2014.pdf). Their full bibliographic identities, retrieval times, inspected locations and PDF byte/hash identities are recorded in [SOURCE_PINS.json](SOURCE_PINS.json).

## Construction and theorem applicability

The proof explicitly defines the diagonal braiding, verifies the braid equation, and realizes it over the finite abelian group (Z/5Z)^3 through three characters and homogeneous degrees. The support generates that group. Each coordinate line is nevertheless stable under both action and coaction, so the degree-one Yetter–Drinfeld module is a direct sum of three nonzero subobjects. Connectedness of the A3 diagram does not make this module simple.

The proof applies [Andruskiewitsch–Schneider, Pointed Hopf algebras, §6.1 and Theorem 6.13](https://arxiv.org/pdf/math/0110136v1), with characteristic zero, algebraically closed field, N=5>2, root-of-unity matrix entries, diagonal value q, adjacent pair products q^-1, and nonadjacent products 1. The primary theorem supplies the ordered PBW basis. The proof explains the endpoint and ordering conventions and uses Lemma 6.4 for the alternative bracketings. The later [Andruskiewitsch–Angiono description, §§4.1.1–4.1.4](https://arxiv.org/pdf/1707.08387v1) corroborates the explicit specialization. No unrelated lower bound on prime divisors of the realization group's order is imposed.

There are six positive interval roots, with ordinary degrees 1,1,1,2,2,3. Each has self-braiding order 5. PBW exponents run independently from 0 through 4, giving dimension 15625 and Hilbert polynomial (5)_t^3 (5)_(t^2)^2 (5)_(t^3), of degree 40. The proof distinguishes the ordinary grading from a regrading and does not substitute the root-scalar calculation for the cited PBW theorem.

## Universal obstruction

The Hilbert polynomial equals Phi_5^6 Phi_10^2 Phi_15. In particular, Phi_15 occurs with multiplicity 1 and Phi_3 with multiplicity 0. The proof establishes for arbitrary positive integer parameters that an allowed factor in t or t^2 which vanishes at a primitive fifteenth root must vanish at a primitive cube root. Products cannot cancel the resulting Phi_3 factor. Parameters 1 and empty products are handled explicitly. Consequently the argument excludes every finite product of the proposed form; it does not depend on a bounded factor search.

Exact remainders are H mod Phi_3 = 5+5t and H mod Phi_15 = 0. The dimension-at-one argument supplies an additional obstruction, since any nontrivial parameter would have to be a power of 5. The example still has a cyclotomic factorization and a product of quantum integers when grading step 3 is allowed.

## Exact verification and source integrity

Preparation rechecked the accepted audit manifest against its trusted SHA-256, then checked every listed audit artifact, the frozen candidate descriptor and all its listed inputs, and all four audit source PDFs. All 22 recorded byte/hash checks passed. Three source PDFs were also verified byte-for-byte against their earlier source copies; the fourth is the separately pinned earlier primary PBW reference.

The accepted exact checker was rerun unchanged in normal Python, -O and -OO. All modes passed, all seven existing controls passed, and each output was byte-identical to the accepted audit receipt. The checks use explicit failure conditions rather than assertions that disappear under optimization. The Hilbert coefficients were recomputed both by polynomial multiplication and by all 15625 PBW exponent tuples. The arithmetic uses integers, including polynomial divisions; no floating-point root tests are used.

The seven controls cover changed braiding data, removal and replacement of the degree-3 factor, the admissible factors (15)_t and (15)_(t^2), and same-size mutation and truncation of the candidate. Full aggregate results and receipt hashes are in [VERIFICATION.json](VERIFICATION.json). The executable checker and raw per-degree coefficient table are excluded from the public packet.

These checks establish exact finite arithmetic and byte integrity. They do not mechanically prove the cited PBW theorem, interpret the source documents, or replace the universal mathematical argument. The source inspection descriptions are the accepted audit's recorded history; preparation verified the pinned bytes without claiming a new source download or a new visual inspection.

## Editorial and publication boundary

The proof is unchanged. The acceptance report retains every verdict, substantive finding, mathematical condition, limitation and seven-control description. Its edits remove a local candidate filename and private multi-candidate descriptor information, replace local-only inventory references with the public inventory, and clarify historical audit versus preparation actions. Source metadata edits remove local paths and internal copy aliases while preserving public source identities and verification history. Public provenance appears in [EDITORIAL_MAP.json](EDITORIAL_MAP.json).

The public directory is a closed inventory of authored mathematical text and aggregate verification metadata. It excludes copied source documents, extracted text, page images, raw coefficient tables, executable scripts and private coordination material. Its [manifest](MANIFEST.json) lists every public payload by exact bytes and SHA-256; the manifest itself is bound by a separate preparation seal outside the public directory. No remote publication, Git operation or queue edit is performed by this preparation.
