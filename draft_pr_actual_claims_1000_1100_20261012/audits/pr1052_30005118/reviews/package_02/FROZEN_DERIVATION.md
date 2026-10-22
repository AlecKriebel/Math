# Independent frozen derivation

This deduction was written before reading candidate mathematical text or earlier verdicts. It uses only the assigned target and the named external integer-hardness interface; the bounded density interface must still be audited directly.

## Exact decision problems and assumptions
For every unbounded positive integer n, input B is a subset of the SAME cyclic group Z/nZ and asks whether some A in that group satisfies B=A+A, with ALL ordered pairs including a=a. Sparse input gives binary n and sorted binary canonical residues; dense input gives all n incidence bits. No claim is made about vector spaces F_p^d or distinct-summand recognition. NP-completeness implies polynomial deterministic recognition iff P=NP, not a proved separation.

## Integer normalization
For nonempty finite integer S, any root T must be finite: fix any u in T and the injective map x -> x+u places T inside the finite set S-u. If S=T+T then min S=2 min T. Thus odd t=min S, even if negative, gives NO. If t is even, C=S-t has min 0 and max M=max S-min S; T is a root of S iff T-t/2 is a root of C. In a root U of C, min U=0, so 0 in U and U subset C. Empty S has precisely the empty root and is YES. All arithmetic above is binary-polynomial even for negative t.

## Universal cyclic root control
Let n be positive odd, 0 in nonempty C subset [0,M], and n>2M. Suppose C=A+A in Z/nZ. Because 0 is represented there are a,-a in A. Canonical diagonal residues d=2a mod n and e=-2a mod n belong to C. Their integer sum is congruent 0 mod n and lies in [0,2M], hence is exactly 0. Thus d=e=0. Since multiplication by 2 is invertible in the odd cyclic group, a=0; consequently 0 in A. It follows for EVERY root, without choosing a specially bounded root, that every canonical a in A lies in C, by a=a+0. Every ordinary sum of canonical elements lies in [0,2M] subset [0,n-1], so reduction modulo n causes no wrap. The two containments in cyclic equality are therefore precisely the two containments in ordinary integer equality. Conversely any integer root of C has min0, is contained in C, and all sums are at most M; reducing it gives a cyclic root. This establishes equivalence, not just a one-way witness construction.

Boundaries: n=1,M=0 satisfies the lemma and represents {0} with {0}; M=0 gives no difficulty. Oddness is essential for control of EVERY root: for even n, A={n/2} represents {0} yet 0 is absent. Strict n>2M is necessary to exclude d+e=n. Translated integer roots must shift by t/2, not by t. Nonempty normalized C always contains 0.

## Total reduction
Use fixed NO instance (5,{0,1}) for odd-minimum inputs. Its parameters obey the restriction; the lemma reduces it to the impossible integer root of {0,1}: a root contains0, any representation of1 forces1 in it, but then2 is a sum. Use (3,empty) for empty input in the unrestricted target, or (3,{0}) in the nonempty restricted target; both are YES. Otherwise normalize and choose n=max(3,2M+1). This is odd and exceeds2M, preserves YES/NO, and output satisfies 2b<n for every canonical b. Binary sparse length is polynomial in source bit length since n has O(log(M+1)) bits and normalization preserves cardinality. This observation alone does NOT establish a polynomial dense reduction; for that the direct AFWS construction must have M polynomial numerically in formula input length.

## NP membership
For any n and any nonempty root A, fix a0 in A. Translation a -> a+a0 is injective into B, so |A|<=|B|. Sparse certificates therefore use at most |B| residues, each O(log n) bits. Computing all pair sums, including diagonal pairs, and checking exact equality with sorted B is polynomial in sparse input length. Empty B has empty certificate. Dense certificates use n bits and enumeration of all n² pairs is polynomial in n-bit input length. n=1 is supported in both.

## External dependency and remaining check
Sparse hardness follows if the credited AFWS integer self-sumset theorem supplies exactly this unrestricted integer problem. Dense hardness follows only from a directly verified numeric-range bound after variable identifier relabeling and constant-size edge handling. The planned numeric interface is n<=2^57(v+c)^4. Its gadget mechanism and constants are not proved by this frozen deduction. It must be checked against primary source text. Exact cyclic priority and worldwide-open status remain unknown; these do not follow from the mathematics.
