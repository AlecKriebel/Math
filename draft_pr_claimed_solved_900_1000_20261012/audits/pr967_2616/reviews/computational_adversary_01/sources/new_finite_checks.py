"""New finite reconstructions: coordinate signatures, size spectra, arbitrary fibers.

Does not import or execute any original verifier. Infinite conclusions are in
MATHEMATICAL_RECONSTRUCTION.md, not inferred from these finite enumerations.
"""
import datetime, itertools, json, sys
from collections import Counter

def require(ok, message):
    if not ok: raise RuntimeError(message)

def powerset(seq):
    seq = tuple(seq)
    return tuple(frozenset(c) for k in range(len(seq)+1)
                 for c in itertools.combinations(seq, k))

def color(n):
    m = n+1
    exponent = 0
    while m % 2 == 0:
        m //= 2
        exponent += 1
    return exponent

def signatures():
    space = powerset(range(4))
    groups = {a:powerset(a) for a in space}
    # A coset fixes exactly the coordinates outside its subgroup support.
    cosets = {(s,a):frozenset(s.symmetric_difference(u) for u in groups[a])
              for s,a in itertools.product(space,repeat=2)}
    membership=0
    for s,a,x in itertools.product(space,repeat=3):
        require((x in cosets[s,a]) == (x-a == s-a), 'coset fixed signature')
        membership += 1
    mixed=0
    for s,t,a,b in itertools.product(space,repeat=4):
        both = cosets[s,a] & cosets[t,b]
        require(bool(both) == (s-(a|b) == t-(a|b)), 'compatibility of fixed signatures')
        if both:
            x=(s-a)|(t-b)
            require(x in both, 'explicit compatible representative')
            require(both == cosets[x,a&b], 'intersection coset')
        # Minkowski sum is exactly the subgroup for A union B translated by s+t.
        sums=frozenset(x.symmetric_difference(y) for x in cosets[s,a] for y in cosets[t,b])
        require(sums == cosets[s.symmetric_difference(t),a|b], 'coset sum exact formula')
        mixed += 1
    return dict(signature_memberships=membership,mixed_intersection_and_sum_pairs=mixed)

def size_spectra():
    space = powerset(range(8))
    groups = {a:powerset(a) for a in space}
    cases=0; bounded_failures=0
    for s,a in itertools.product(space,repeat=2):
        actual={len(s.symmetric_difference(t)) for t in groups[a]}
        expected=set(range(len(s-a),len(s-a)+len(a)+1))
        require(actual == expected, 'exact whole coset size spectrum')
        actual_colors={color(n) for n in actual}
        require(actual_colors == {color(n) for n in expected}, 'whole coset color spectrum')
        if 4 not in actual_colors: bounded_failures += 1
        cases += 1
    targets=0
    # Explicit next cardinality in a prescribed 2-adic class, with minimality.
    for s in range(129):
        for j in range(10):
            modulus=2**(j+1); residue=2**j-1
            q=s+((residue-s)%modulus)
            require(q>=s and color(q)==j, 'target size')
            require(all(color(n)!=j for n in range(s,q)), 'least admissible size')
            targets+=1
    return dict(coset_size_spectra=cases,finite_cosets_missing_color4=bounded_failures,
                closed_form_minimal_targets=targets)

def arbitrary_fibers():
    # Exhaust every map of four abstract points into three labels and every
    # assignment to three disjoint blocks or unused. No maximum representation.
    maps=0; assignments=0; nonempty_selected=0
    for mapping in itertools.product(range(3),repeat=4):
        capacities=Counter(mapping); maps+=1
        for labels in itertools.product(range(4),repeat=4):
            blocks=[{x for x,label in enumerate(labels) if label==n+1} for n in range(3)]
            images=[{mapping[x] for x in b} for b in blocks]
            for y in range(3):
                require(sum(y in m for m in images)<=capacities[y], 'fiber occurrence bound')
            chosen=[]; used=set()
            for n,m in enumerate(images):
                if m and used.isdisjoint(m):
                    chosen.append(n); used.update(m)
            parity=[set().union(*(images[n] for n in chosen[p::2])) for p in range(2)]
            require(parity[0].isdisjoint(parity[1]),'disjoint parity images')
            for p in range(2):
                permitted=set(range(3))-parity[p]
                for n in chosen[p::2]:
                    require(all(mapping[x] not in permitted for x in blocks[n]), 'entire block fiber exclusion')
            assignments+=1; nonempty_selected += bool(chosen)
    # Actual maxima: repeated maxima across many different, unbounded-size
    # finite blocks. These 400 blocks partition a finite initial support list.
    blocks=[]; low=1
    for n in range(400):
        blocks.append(tuple(range(low,low+n+1)));low+=n+1
    images=[{x.bit_length()-1 for x in b} for b in blocks]
    counts=Counter(y for m in images for y in m)
    require(all(v<=2**y for y,v in counts.items()), 'concrete maxima fiber bound')
    chosen=[]; used=set()
    for n,m in enumerate(images):
        if used.isdisjoint(m):chosen.append(n);used.update(m)
    require(any(v>1 for v in counts.values()),'repeated maximum fixture is nontrivial')
    require(len(chosen)>=8,'nontrivial thinning fixture')
    parity=[set().union(*(images[n] for n in chosen[p::2])) for p in range(2)]
    for p in range(2):
        forbidden=parity[p]
        for n in chosen[p::2]:
            require(all(x.bit_length()-1 in forbidden for x in blocks[n]),'all elements excluded')
    return dict(abstract_maps=maps,abstract_block_assignments=assignments,
                assignments_selecting_nonempty_block=nonempty_selected,
                growing_blocks=400,growing_block_total_elements=low-1,
                repeated_maximum_occurrences=dict(sorted(counts.items())),
                greedy_selected_original_indices=chosen)

def principal_boundary():
    # A finite principal filter has a coordinate common to all neighborhoods.
    # This detects Hausdorff and density failures; it is NOT a free-U model.
    universe=frozenset(range(4));p=2
    sets=[a for a in powerset(universe) if p in a]
    common=set.intersection(*(set(a) for a in sets))
    require(common=={p},'principal common coordinate')
    require(all(frozenset({p}) in powerset(a) for a in sets), 'nonzero not separated from identity')
    require(3 not in {color(len(t)) for t in powerset({p})},'large color absent')
    return dict(principal_failure_detected=True,free_ultrafilter_modeled=False)

def main():
    result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                optimization=sys.flags.optimize,
                coordinate_signature_checks=signatures(),support_size_checks=size_spectra(),
                finite_fiber_checks=arbitrary_fibers(),principal_boundary=principal_boundary(),
                infinite_proof_mechanized=False,free_ultrafilter_simulated=False)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
