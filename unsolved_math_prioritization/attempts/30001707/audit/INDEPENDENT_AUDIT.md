# Independent mathematical and adversarial audit: 30001707

Date: 2026-10-06. Catalog rank: 834. Source identifier: OWR-4799-003.

## Decision

**Accept the authored mathematics as a limited source correction and explicitly convention-dependent examples. Reject an unqualified execution-boundary acceptance of the original verifier. Accept the separately patched derivative only through the isolated, externally pinned bootstrap described below. The general original one-way conjecture is unresolved by this work. No novelty claim is accepted.**

All nine actual author files were read before execution. The original freeze and its external manifest retain their original bytes. The correction is an actual unified patch, applied to a fresh extraction and checked byte-for-byte against the derivative. This audit neither publishes nor changes a repository.

## Identity and source evidence

The complete catalog (15,458 entries), complete problem corpus (15,458 entries), and complete research corpus (6,701 entries) were independently parsed. Each catalog/problem match was unique. The statement SHA-256 is d28d8df9d1d3d79d826cef2afa90a7e2e950c5f05b5c8328e13a2776a156fbef. The complete record plus exact problem-number report lookup, serialized with Python's default json.dumps and sort_keys=True, hashes to da0a54359ba5daa882a41290f0cdcd1ec0361a37951c4182ca733abf4878b92d. Both equal the catalog pins. The report lookup is empty. IDENTITY_AUDIT.json records the independently recomputed corpus hashes and sizes without reproducing records.

The four accessible source PDFs were independently fetched successfully and all four byte counts and hashes match the author metadata. The institutional OWR PDF is 806,927 bytes, SHA-256 b42bf54238d545255dfdd9e544f7f62269f02be6c1c4381fb0fa0640e0a38f2a. The contribution and a page-467 rendering were inspected. The exact live problem page was not accessible to the web tool; its present contents remain unverified. Authentication of the supplied corpus is not a successful live-page comparison.

The historical prior-attempt searches in PROVENANCE.json were not independently rerun; they remain bounded author-reported search history. They establish neither novelty nor absence of prior work. No acceptance depends on such an inference.

## Mathematical review

### Source direction and quantifiers

The [original contribution, p. 467](https://publications.mfo.de/bitstream/handle/mfo/3224/OWR_2011_09.pdf?isAllowed=y&sequence=1) states the geometric zero-or-one condition as sufficient for a multiplicity-free restriction, with Q assumed to be a well-defined irreducible unitary representation. The concern is noncompact reductive G and H. A separate family converse is given without a general saturation specification. Therefore the authenticated catalog's single-orbit equivalence is a strengthening, not a faithful one-way transcription. Neither an almost-everywhere direct-integral multiplicity nor a finite list of discrete summands can replace the source's all-geometric-orbits condition.

This is a correction to formulation, not a general proof or disproof of the source conjecture. The compact CP² example alone is outside the stated noncompact focus. The central extension tests an explicitly broader reductive-family interpretation but does not identify the intended orbit assignment or parameter domain.

### CP² and the quantization convention

The chosen convention Q(CP²,O(1))=H⁰(CP²,O(1)) is ordinary uncorrected holomorphic quantization. Its three coordinate linear forms transform in the dual defining representation. Their circle weights are -1, 0, 1, each once, so the bounded commutant is the algebra of diagonal scalars. SU(3) irreducibility and H multiplicity-freeness are correctly distinguished. The positive Fubini–Study/KKS sign can be chosen compatibly with the specified rank-one projector realization. Reversing the sign reverses the weights and moment coordinate, preserving the claims. This does not identify this orbit assignment with a half-form or rho-shifted convention.

The moment coordinate is p₀-p₂. Outside [-1,1] there are no points; its endpoints have exactly one coordinate point each. At every |c|<1, the admissible s interval has length (1-|c|)/2, so it is nonempty and has continuum cardinality. The displayed square-root coordinates lie in the level. The invariant p₂=s injects that interval into the orbit quotient. The quotient has at most continuum cardinality because CP² does. This establishes the claimed exact cardinalities without finite inference. In particular c=0 is integral. The three distinct weights give only the coordinate fixed points; critical values are -1,0,1, so c=1/2 is regular. Failure is neither a nonintegral-value artifact nor exclusively a singular-level artifact.

This is a valid counterexample to the single-level converse under the stated quantization. It cannot refute the forward implication because its geometric antecedent fails.

### Tensor powers and family limits

For degree k, the weight equation d-a=j and degree equation a+b+d=k yield b=k-j-2a for j≥0, giving floor((k-j)/2)+1 choices; exchanging a,d handles j<0. Outside |j|≤k there are none. Thus the stated all-k formula is valid. The independent check multiplies the three generating series by dynamic programming, rather than importing the author's monomial-enumeration implementation, and agrees through k=128. This is additional finite corroboration, not the proof of the formula. At k=2 the zero-weight space contains two independent monomials; every k≥2 fails multiplicity-freeness. The single-level example is not a scaling-family counterexample.

For A=R₊ under multiplication, log identifies the group with R and every t gives a unitary character. The product SU(3)×A is connected, noncompact, linear and reductive; for example, use the real defining SU(3) representation and the block diag(a,a⁻¹). The central factor acts trivially on each base orbit and by its character on the equivariant point line. The product representation remains irreducible, while its restriction has three distinct characters. Distinct t give distinct coadjoint orbits. Since A acts trivially on the base and the projected central coordinate is fixed, the quotient at (c,t) is the same CP² quotient.

Consequently the arbitrary-real-parameter-family assertion is false under this specified product convention. The example uses compact coadjoint orbits and a compact semisimple factor, is not a scaling family, and has nonsimple G. It is not a resolution of an intended formulation excluding those cases or using a different orbit-to-representation assignment. No additional hidden restrictions are assumed.

### Noncompact benchmark and prior credit

For a>0 and C=a²+x², X(x,u) with lower-left entry u>0 and upper-right entry -C/u has determinant a² and belongs to the positive elliptic sheet. To verify it is genuinely in the required orbit, take

    g = [[sqrt(a/u), x/sqrt(a*u)], [0, sqrt(u/a)]].

Then det(g)=1 and g[[0,-a],[a,0]]g⁻¹=X(x,u). This also proves the whole displayed sheet is a single SL(2,R) orbit. Diagonal conjugation sends u to r⁻²u; for any positive u₁,u₂ choose r²=u₁/u₂. Every real x occurs and every level is one orbit. With the trace pairing the restricted coordinate is 2x, an immaterial nonzero scaling. The all-a geometric calculation does not assert a quantization for every real a: the cited representation statement concerns the allowed discrete-series parameters.

The multiplicity-one continuous branching law is already in [Kobayashi–Nasrin 2003, Section 4, equations (4.2)–(4.5)](https://www.ms.u-tokyo.ac.jp/~toshi/texpdf/karpe.pdf). It is credited, not newly established here.

[Kobayashi–Nasrin 2018, Theorem A](https://arxiv.org/abs/1805.09713) has the stated noncompact simple Hermitian and holomorphic symmetric-pair setting, with connected H and the scalar elliptic condition. Fact 2.1 gives a prior scalar-type lowest-weight multiplicity-free restriction theorem, in fact for symmetric pairs more generally. The paper ties the geometry to the 2011 announcement and explains difficulties with a universal reductive orbit correspondence. The report correctly does not upgrade this to arbitrary reductive pairs.

[Paradan 2015](https://ems.press/journals/jems/articles/11978) imposes its holomorphic/properness and restriction hypotheses; quantization of a reduced space is not its point cardinality. [Hochs–Song–Yu](https://arxiv.org/abs/1805.02297) treats compact K. [Nasrin's 2024 chapter](https://link.springer.com/chapter/10.1007/978-981-97-7666-5_4) was checked only at abstract/metadata level; no access or general theorem is inferred from its existence. No latest exhaustive open-status claim is made.

## Reproduced integrity defect and actual correction

The original verify.py imports hashlib before its inventory check. In both normal and -O runs, adding a benign diagnostic hashlib.py caused that file to execute and create its marker before verification failed. A nonzero exit code therefore did not mean rejection before untrusted code execution. The author's existing controls pass but do not test this attack. The original archive contains no such shadow module; its historical bytes are preserved. The flaw is in the hostile-directory execution boundary, not the mathematics or the observed original check output.

AUTHOR_PATCH.diff changes only README.md, certificate.py, controls.py and verify.py. Every Python entry point first requires isolated/no-site flags. All verifier/certificate child processes use -I -S. The certificate pin is updated to its patched bytes. The expected JSON and all mathematical prose remain byte-identical. Missing-flag guards do not repair an already unsafe interpreter startup; the mandatory external launch flags are essential.

ISOLATED_VERIFY.py is the publication entry point. It runs with a trusted Python interpreter under -I -S, checks its own nonsymlink type, verifies a hardcoded corrected-manifest digest, and rejects every extra/missing/nonregular package node and every member mismatch before launching any package code. The package-root symlink, wrapper-entrypoint symlink, manifest symlink, cache, FIFO, broken symlink, changed certificate/verifier, forged/rehashed manifests, import shadows, and hostile archives are tested. PYTHONPATH and site customization diagnostics are ignored in valid isolated runs, with markers absent.

This is a reproducibility/integrity boundary for a trusted interpreter and quiescent filesystem. It is not a sandbox against a malicious Python installation, operating system, concurrently mutating filesystem, or replacement of the independently trusted receipt/bootstrap itself. Hashes are meaningful only when their trust anchor is supplied independently.

## Executed acceptance

Both independent runner modes, normal and -O, completed with the same counts:

- Original: verify.py and controls.py each pass under normal/-O, and two before-patch import-shadow executions are positively reproduced.
- Corrected: eight positive records, including normal/-O relocation, inherited controls, and poisoned-environment isolation. Each inherited controls replay includes four positive and 38 negative tests.
- Independent hostile controls: 58, including ten distinct hostile ZIP cases rejected before extraction. Every tested corrected marker remains absent.
- Independent mathematical checks: generating-series coefficients for degrees 0–128 and 198 rational points over 33 interior CP² levels.
- The actual unified patch was applied to fresh original bytes. All nine resulting members match the corrected derivative; isolated wrapper replay passes normal/-O.

ACCEPTANCE.json, ACCEPTANCE_OPTIMIZED.json and PATCH_APPLICATION.json contain the full executed records. Results do not constitute formal proof of representation theory or of an uncountable set cardinality, and do not certify the original conjecture.

## Publication boundary

Permitted contents of this audit are authored mathematical audit text, authored code/patches, exact acceptance records, and public-source/dataset verification metadata. No copied source PDFs, source text extracts, rendered source pages, dataset records, private-source material, or private coordination is included. Preserve the original author freeze as historical evidence; do not label its self-verifier as fail-closed under hostile imports. Publish the corrected derivative and isolated bootstrap with this qualification. No repository publication was performed by this audit.
