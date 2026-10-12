# Initial analytic mathematical verdict, frozen before prior audit/control exposure

UTC: 2026-10-04T01:47:07+00:00. Best-guess overall review completion: 30%.

## Exposure boundary

Since the accepted source-only gate, I have read only the released manuscript TEX, its complete extracted PDF text, all three rendered PDF pages, and PDF metadata. I listed filenames in the parent preprint folder to resolve an incorrect guessed ZIP filename; I have not read its builder/verifier, ZIP members, deposit metadata, prior verdicts, control code, output, or priority audits. I copied/hashes-pinned the ZIP and metadata without reading their contents. The earlier copy attempt failed only because I guessed the archive basename; neither source/PDF content nor parent files were changed. The release record now uses the actual archive basename.

## Verdict: the submitted universal proof is mathematically valid

The claim matches Target A in my source-first baseline and the root's explicit catalogue mapping. It maintains the prescribed alternating conclusion and allows arbitrary alphabets, fixed letters, and nonminimal periods. The length hypothesis with p,q>0 implies L>=max(p,q), excluding epsilon automatically and justifying all prefix choices. The involution-to-letter-permutation lemma uses no finite-alphabet or fixed-point-free hypothesis.

I independently checked the central extension mechanism. For each original period p, the alternating two-sided sequence has reflection s[-1-i]=sigma(s[i]); hence its restriction to [-L,L-1] is the same concrete finite word theta(w)w, for either p or q. No unobserved positive continuation is equated across roots. Both ordinary doubled periods are valid, even when they equal the whole extended length. The ordinary Fine–Wilf length is exactly doubled: 2L>=2p+2q-2d. The resulting ordinary 2d-period alone would not justify an alternating d-period, but the concrete central 2d-block theta(v)v and the continuous congruence chains inside [-L,L-1] provide precisely the missing phase. For a residue r>=d, the letter at r-2d is sigma(v[2d-1-r]); the displayed final formula is correct. Short final blocks are included.

The uniform sharpness proposition is correct as worded: under plain reversal, abb has alternating periods 2 and 3 and fails alternating period 1 at length 3=2+3-1-1. The period q=3 equals the word length, which is expressly allowed by the source definition. This proves a uniform one-step obstruction, not sharpness for every parameter pair or every involution. The manuscript states that limitation accurately.

No analytic mathematical blocker was found. This is an automated independent assessment, not external human review and not a priority verdict. Literature comparisons and all packaging/reproducibility claims remain unverified at this freeze.

## Independently designed falsifiers (not read or imported from the package)

1. A literal word oracle constructs repeated u+theta(u) blocks and truncates; it does not use constraint graphs or the submitted residue implementation. Exhaustively test binary reversal and reverse-exchange to length 9, ternary identity and exchange-with-fixed-letter to length 7, and quaternary two-exchange involution to length 6. For every word and every p<=L, check equivalence between alternating p-periodicity and ordinary 2p-periodicity of theta(w)w. For every unordered pair of accepted periods whose threshold is met, check actual alternating gcd-periodicity.
2. Explicit witnesses cover the abb sharpness example; swapped-letter w=abab,p=2,q=3 shows that ordinary d-periodicity is too strong while alternating d-periodicity holds. Test equality and divisibility, empty-word exclusion, nonminimal periods, all possible final truncations within the exhaustive domains, and both fixed and exchanged letters.
3. Definition substitution negative control: under reversal, abba has general theta-periods 2 and 3, but not alternating period 3 and not alternating period 1. A verifier conflating independent block choice with alternating blocks must be rejected by this witness.
4. Orientation negative control: for w=abb,p=2, the submitted theta(w)w has ordinary period 4 while w theta(w)=abbbba does not. A mistaken reflection placement must be caught.
5. Search for a morphic-involution counterexample at the shorter length formula using the same literal-block oracle with letterwise transformation. Its existence would validate that antimorphic order reversal is a material hypothesis; absence in the finite domain alone would not extend the theorem.
6. PDF visual review: all equations, theorem labels, references, page boundaries and hyperlinks must remain readable. Investigate the unusually long sharpness proposition statement on page 2 for overflow rather than relying on extraction.

## Remaining work

Open the actual archive only after this freeze; inspect every member and all relevant scripts/metadata; independently capture default and full native runs including both streams and compare all output bytes; inspect primary references and precise literature claims; check public/private exclusions and create read-only replay/hash verifiers and a concrete one-shot closure plan. No postclosure writes or seal are authorized yet.
