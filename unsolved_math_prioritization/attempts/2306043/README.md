# Function Theory 6.43: audited logarithmic-coefficient partials

Problem 2306043 / AMR-022-6043, queue rank 683. Publication disposition: **unsolved, 5/5**, zero discoveries, no full-class proof or counterexample, and no novelty claim. This is an AI-assisted, independently AI-audited partial investigation, not peer review or a formal proof certificate.

For each fixed normalized univalent function f, with log(f(z)/z) = 2 sum gamma_n z^n, the target is whether sum n|gamma_n|r^n = O_f((1-r)^(-1)). A constant uniform over the full class is not silently assumed.

## Retained results and exact gap

- The general de Branges–Milin deduction retains an unbounded square-root-logarithm loss. The target is equivalent to a linear bound on the coefficient partial sums.
- Starlike functions of order sigma have the sharp bound (1-sigma)r/(1-r). These are proper subclasses.
- For positive Hayman index, the published Bazilevich inequality implies both the normalized radial majorant and normalized coefficient partial sums tend to 1. This is a deduction from a known theorem, with no novelty claim. The general zero-index case outside the covered subclasses remains unresolved.
- A fixed infinite Rudin–Shapiro block model meets signed-growth and Milin-energy constraints while violating the absolute-majorant bound. Its associated holomorphic map is **proved non-univalent**. It is not a counterexample in S. The independent audit certifies a critical point strictly between 49/100 and 51/100 using a bound on the entire infinite tail.

The [five complete arguments](freeze/public/README.md) and [full independent audit](independent_audit/INDEPENDENT_AUDIT.md) are preserved byte-for-byte. Their historical words `exhausted`, `audit pending`, and `no remote writes` describe the frozen research stage. For publication the queue uses `unsolved`, `5/5`; no additional research turn has been used.

## Verification and limits

Run from any working directory with Python 3.10+ and its standard library:

    python3 /path/to/2306043/verify_publication.py
    python3 -O /path/to/2306043/verify_publication.py
    python3 /path/to/2306043/verify_negative_controls.py

The wrapper rejects extra/missing files, symlinks, duplicate or unsafe manifest paths, duplicate JSON keys, and altered bytes. It pins both frozen manifests and replays the original 2,945 assertions and the independent 8,564 assertions in ordinary and optimized modes, comparing the complete stored JSON results. The audit count includes 8,500 mathematical/algebraic controls and 64 integrity/replay assertions. Finite checks corroborate formulas; the infinite conclusions rest on the written arguments and stated theorem inputs.

Hayman's original 1980 construction was not inspected; its use remains attributed to the inspected Hayman–Lingham update. Full original proofs of the imported de Branges–Milin, starlike, and Bazilevich results, including Duren–Schiffer's later variational argument, were not independently reconstructed. The original problem website was inaccessible; bounded literature-search silence does not certify current global open status. Source PDF hashes bind inspected cached bytes, not a fresh publication-stage download. Original source-corpus bytes were not freshly rematched.

Fresh publication checks found no matching attempt on main, state-ledger entry, PR for the numeric ID, exact problem number or logarithmic-coefficient title, or branch for the numeric ID, logarithmic, or Aharonov terms. The base is 28128d274d780c814005596ee293141f80e3f2c2. Only this row's Status, Turns, and Findings cells change; the literal existing queue header and every other byte are preserved.

Only authored mathematics, code, audit material, and public verification metadata are included. Source PDFs/text, dataset contents, and private coordination are excluded. No release, DOI, merge, or outreach is part of this draft publication.
