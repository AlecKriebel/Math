# Independent manuscript-first reconstruction

UTC: 2026-11-16T08:46:09+00:00. Estimated scientific review completion: 25%. This is a source-only initial assessment, not clearance. Current peer mathematical findings, programs/results and foreign proofs have not yet been opened by root.

## Personally inspected source

Read the complete actual 229-line, 10658-byte published TeX (SHA256 ccf85ea52eb1d2003b69344e23e5c4641f851b22155bc95cbe01775ca41b2cab), complete three-page PDF text, and all three fresh 110-dpi PDF rasters. The unchanged 68077-byte PDF has SHA256 3ee2635930d4d107ff80cde1dfb7f8c57752fa833d0d212ba15c4ef7d4cdd81d. The printed date is 3 October 2026. These views establish the actual manuscript's symbols, including antimorphic rather than morphic involution and strict alternating blocks.

## Exact hypothesis and conclusion

Let theta be an antimorphic involution of A*, with A an arbitrary alphabet. Positive integers p,q need not be minimal. An alternating theta-period p means that w is a prefix of the infinite repetition of u theta(u), for a length-p block u. It does not mean an arbitrary concatenation of u and theta(u). Set d=gcd(p,q). For L=|w| at least p+q-d, the length-d prefix v satisfies that w is a prefix of the repetition of v theta(v). Fixed letters of the induced letter involution, ordinary reversal, equal periods and divisibility cases are included.

## Reconstructed mechanism and checks

1. Theta sends the empty word to itself, is bijective and sends nonempty words to nonempty words. If a letter image factored into two nonempty words, applying theta would factor that letter into two nonempty images, impossible. Thus theta is reversal followed by an involutive letter permutation sigma.
2. Given a length-p prefix u, the bi-infinite repetition of u theta(u) has period 2p and obeys s[-1-i]=sigma(s[i]). This identity follows directly in each of the two residue blocks, including fixed or swapped letters.
3. Its restriction to [-L,L-1] is exactly theta(w)w. This is the same finite word for either period; the proof never identifies the two unseen bi-infinite extensions. Truncated final blocks cause no problem.
4. The length hypothesis implies L>=max(p,q) and 2L>=2p+2q-2d. The reflected word has ordinary periods 2p and 2q, so ordinary Fine-Wilf gives ordinary period 2d.
5. The central interval [-d,d-1] is theta(v)v. For a nonnegative index i, take its residue r modulo 2d and choose the central representative r if r<d, otherwise r-2d. The chain of period-2d steps stays within the finite interval. This recovers the specific alternating phase, rather than merely an unspecified ordinary 2d-period.
6. The claimed sharpness is a uniform obstruction only. With reversal, w=abb, p=2,q=3,d=1, both alternating prefixes occur at length3, one below the claimed sufficient threshold4, whereas alternating period1 would be constant. No pairwise sharp threshold for every p,q, alphabet or involution is claimed.

For an independent check on the classical dependency, root reconstructed an elementary ordinary Fine-Wilf proof. Assume p<=q and first use N=p+q-d letters. Contract all p-step equality chains to residues modulo p. The available q-step edges start at i=0,...,p-d-1, inducing edges i to i+q modulo p. The full addition-by-q permutation consists of d cycles, one for each residue modulo d. Omission of the last d starts removes exactly one directed edge in each cycle, leaving that cycle connected as an undirected path (including cycles of length one or two). Thus all indices with the same residue modulo d are equal. For a longer word, subsequent indices attach by p-steps to the initial interval. This proves the ordinary dependency without assuming an unsupported stronger theorem. Actual historical sources and exact attribution still require inspection.

## Falsification families and remaining gaps

- Letter-image lemma: empty alphabet and nonempty-image reasoning.
- Common extension: negative indexing, truncations, reflection sign and center orientation.
- Finite period transfer: threshold arithmetic and steps remaining inside the interval.
- Equal, divisible and nonminimal periods, shortest permitted words and fixed letters.
- Sharpness: verify the two explicit prefixes and avoid claiming pairwise optimality.
- Exact historical target: unnumbered conjecture after Theorem23, distinguished from numbered Conjecture27.
- Prior reflection/doubled-period mechanisms and later palindromic periodicity results: compare actual hypotheses, lengths and phase information.
- Native verification code: inspect complete actual code before any possible execution; existing finite controls cannot prove the universal theorem or priority.
- Bounded literature/access limitations: no firstness claim from failed searches or inaccessible versions.

No internal mathematical defect found in this first reading. Primary-source attribution, independent/adversarial evidence, artifact custody and code consistency remain open. No new experiment, native checker or old helper was run. Follow-up defaults to none; public copy, website, Git and spreadsheet authority remain absent.
