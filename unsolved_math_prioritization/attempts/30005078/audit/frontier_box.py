"""Add the already-proved explicit box to the frozen author result.

Pass an initialized author MonomialQuotient. The author source is unchanged.
The box bounds minimal points only, not the whole unbounded regularity region.
"""
import math

def frontier_box(quotient):
    caps=[max((g[j] for g in quotient.generators),default=0)
          for j in range(quotient.nvars)]
    q=math.prod(quotient.block_sizes)
    return tuple((-len(block),q+sum(caps[j]-1 for j in block))
                 for block in quotient.blocks)

def regularity_with_box(quotient,kind='module',check_complex=False):
    result=quotient.regularity(kind=kind,check_complex=check_complex)
    result['minimal_element_box']=frontier_box(quotient)
    return result
