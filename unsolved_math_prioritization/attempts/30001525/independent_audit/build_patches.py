#!/usr/bin/env python3
"""Produce reviewable local patches; do not alter the frozen packet."""
from pathlib import Path
import ast, difflib
ROOT = Path(__file__).resolve().parent
PACKET = ROOT.parent / 'packet'
src = (PACKET / 'verify.py').read_text()
lines = src.splitlines(keepends=True)
for node in sorted((n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assert)), key=lambda n:n.lineno, reverse=True):
    if node.lineno != node.end_lineno:
        raise RuntimeError('Unexpected multiline assertion; review manually')
    expression = ast.get_source_segment(src, node.test)
    indent = ' ' * node.col_offset
    lines[node.lineno-1] = indent + f"check({expression}, 'Original verification condition at line {node.lineno}')\n"
hardened = ''.join(lines)
hardened = hardened.replace('MAX_DEGREE = 80\n', '''MAX_DEGREE = 80

def check(condition, label):
    """Unlike assert, correctness checks must remain active under python -O."""
    if not condition:
        raise RuntimeError('Verification failed: ' + label)
''')
(ROOT/'patched'/'verify.py').write_text(hardened)
old = (PACKET/'PROOF.md').read_text()
new = old.replace('merging the equal width-four profiles has coefficient binomial(4,2)=6, which is even [GSS, Theorem 6.8].', 'the two equal profiles supported on four letters have combinatorial widths 2 and 2 in [GSS, Definition 6.3], and therefore their merged coefficient is binomial(4,2)=6, which is even [GSS, Theorem 6.8].')
needle = '### 3.4 An explicit deterministic selection rule'
supplement = '''### Compatible lifts preserve the individual skyline source

Here “higher Bockstein on a skyline class” uses the surviving mod-2
cohomology class as source, as in the coefficient Bockstein spectral sequence.
It does not require division of the differential of the unmodified canonical
Fox–Neuwirth cochain. This distinction is essential, and the result does not
assert that stronger chain-level property.

For a free R-cochain complex, the corrections needed through page three can be
written explicitly. Start with a fixed integral lift c of the chosen mod-2
cocycle and write dc=2b. If d1[c]=0, choose h with b-dh even. Then
c4=c-2h has dc4=4b2. If d2[c]=0 on E2, there is a mod-2 cocycle u and a
cochain q such that b2-du_tilde/2-dq is even, where u_tilde is an integral
lift of u. Thus c8=c4-2u_tilde-4q has dc8 divisible by 8. These corrections
are even, so c4 and c8 reduce to the original individual mod-2 cocycle.
Dividing their differentials produces integral cycles killed by 4 or 8.
Changing a lift with the same mod-2 reduction changes the resulting normalized
class by a class killed by 2 or 4, respectively. No sum of distinct skyline
source classes is introduced by these lift corrections.

In the cyclic-basis argument, coefficient reduction embeds H^d(R)/2H^d(R)
into H^d(F2), by the coefficient long exact sequence. The selected primary
reductions are independent in im(d1), while each selected secondary reduction
is nonzero in ker(d1)/im(d1). Together with the cyclic-factor counts this
justifies generation and independence of the actual integral classes, rather
than only independence of associated-graded classes.

'''
if needle not in new:
    raise RuntimeError('Missing proof insertion point')
new = new.replace(needle,supplement+needle)
(ROOT/'patched'/'PROOF.md').write_text(new)
diff = ''.join(difflib.unified_diff(src.splitlines(keepends=True),hardened.splitlines(keepends=True),fromfile='packet/verify.py',tofile='patched/verify.py'))
diff += ''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='packet/PROOF.md',tofile='patched/PROOF.md'))
(ROOT/'PATCHES.diff').write_text(diff)
print('Prepared assertion-independent verifier and mathematical clarification patches.')
