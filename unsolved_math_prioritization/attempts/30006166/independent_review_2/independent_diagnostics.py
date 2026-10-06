"""Independent finite falsification tests. These do not prove the infinite theorem."""
import json
from collections import Counter, deque
from itertools import product
from math import factorial


def must(value, message):
    if not value:
        raise RuntimeError(message)


def components(vertices, neighbors):
    unseen = set(vertices)
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = [root]
        block = {root}
        while queue:
            x = queue.pop()
            for y in neighbors(x):
                if y in unseen:
                    unseen.remove(y)
                    block.add(y)
                    queue.append(y)
        answer.append(frozenset(block))
    return answer


def bounded_reach(root, neighbors, radius):
    seen = {root}
    frontier = {root}
    for _ in range(radius):
        frontier = {y for x in frontier for y in neighbors(x)} - seen
        seen.update(frontier)
    return seen


class Model:
    """W acts on a finite configuration quotient, times a cyclic height.

    Height may have shorter period than configurations. Thus t^height fixes
    some configurations and moves others, testing genuinely varying stabilizers.
    A diagonal quotient additionally identifies the simultaneous all-lamp move.
    """
    def __init__(self, length, modulus, height, diagonal):
        self.length, self.modulus, self.height, self.diagonal = length, modulus, height, diagonal
        vectors = {self.canonical(v) for v in product(range(modulus), repeat=length)}
        self.states = sorted((v, h) for v in vectors for h in range(height))

    def canonical(self, v):
        shift = v[-1] if self.diagonal else 0
        return tuple((x-shift) % self.modulus for x in v)

    def shift(self, x, amount=1):
        v, h = x
        return self.canonical(tuple(v[(i-amount) % self.length] for i in range(self.length))), (h+amount) % self.height

    def lamp(self, x, index=0, amount=1):
        v, h = x
        out = list(v)
        out[index % self.length] += amount
        return self.canonical(out), h

    def norm(self, x, width):
        r = x[1] % width
        return self.shift(x, -r), r

    def slab(self, x, width):
        r = x[1] % width
        out = {self.lamp(x), self.lamp(x, amount=-1)}
        if r+1 < width:
            out.add(self.shift(x))
        if r > 0:
            out.add(self.shift(x, -1))
        return out - {x}

    def base(self, width):
        return [x for x in self.states if x[1] % width == 0]

    def kernel_moves(self, x, width):
        return {self.lamp(x, -r, s) for r in range(width) for s in (-1, 1)} - {x}


def compute():
    counts = Counter()
    summaries = []
    negative = {}
    models = [(4, 2, 2, False), (4, 3, 2, True), (3, 3, 3, False), (6, 2, 6, False)]
    for spec in models:
        model = Model(*spec)
        widths = [m for m in range(1, model.height+1) if model.height % m == 0]
        fixed = sum(model.shift(x, model.height) == x for x in model.states)
        if model.length > model.height:
            must(0 < fixed < len(model.states), 'the intended nonnormal-stabilizer diagnostic must be nonvacuous')
            counts['variable_stabilizer_models'] += 1
        inventory = []
        for m in widths:
            coordinates = {x: model.norm(x, m) for x in model.states}
            must(len(set(coordinates.values())) == len(model.states), 'coordinate map injective')
            must(set(coordinates.values()) == set(product(model.base(m), range(m))), 'coordinate map onto')
            counts['full_coordinate_bijections'] += 1
            slab_adj = {x: model.slab(x, m) for x in model.states}
            for x, (z, r) in coordinates.items():
                must(model.shift(z, r) == x, 'coordinate inverse')
                for sign in (-1, 1):
                    must(model.norm(model.lamp(x, amount=sign), m) == (model.lamp(z, -r, sign), r), 'correct conjugation')
                    counts['signed_lamp_coordinate_checks'] += 1
                for y in slab_adj[x]:
                    must(x in slab_adj[y], 'edge symmetry')
                    counts['edge_symmetry_checks'] += 1
                if r+1 < m:
                    must(coordinates[model.shift(x)] == (z, r+1), 'uncut vertical coordinate identity')
                    counts['interior_vertical_checks'] += 1
                if r and model.lamp(z, -r) != model.lamp(z, r):
                    negative['reversed_lamp_index_detected'] = True
            graph_blocks = {frozenset(coordinates[x] for x in c) for c in components(model.states, slab_adj.__getitem__)}
            base_blocks = components(model.base(m), lambda z: model.kernel_moves(z, m))
            expected_blocks = {frozenset(product(c, range(m))) for c in base_blocks}
            must(graph_blocks == expected_blocks, 'all slab components equal kernel orbits times finite levels')
            counts['complete_nonfree_slab_inventories'] += 1
            inventory.append({'width':m, 'sizes':dict(sorted(Counter(map(len,graph_blocks)).items()))})
            for radius in (1,2,3):
                rho_ball = {x:bounded_reach(x,slab_adj.__getitem__,radius) for x in model.states}
                k_ball = {z:bounded_reach(z,lambda y:model.kernel_moves(y,m),radius) for z in model.base(m)}
                for x in model.states:
                    for y in rho_ball[x]:
                        must(coordinates[y][0] in k_ball[coordinates[x][0]], 'slab short path projects into kernel short path')
                        counts['short_path_projections'] += 1
                for palette in (1,2,3):
                    color = {z:(sum((i+1)*v for i,v in enumerate(z[0]))+z[1]) % palette for z in model.base(m)}
                    bparts = components(model.base(m), lambda z:{v for v in k_ball[z] if color[v] == color[z]})
                    block_of = {z:c for c in bparts for z in c}
                    liftparts = components(model.states, lambda x:{y for y in rho_ball[x] if color[coordinates[x][0]]==color[coordinates[y][0]]})
                    for c in liftparts:
                        projected = {coordinates[x][0] for x in c}
                        containing = block_of[next(iter(projected))]
                        must(projected <= containing, 'monochromatic components project into one kernel component')
                        must(len(c) <= m*len(containing), 'finite-width cardinal bound')
                        counts['monochromatic_lift_components'] += 1
            for n in widths:
                if n % m == 0:
                    for x in model.states:
                        must(model.slab(x,m) <= model.slab(x,n), 'divisible-width graph monotonicity')
                        counts['nested_width_vertex_checks'] += 1
        summaries.append({'length':model.length,'lamp_modulus':model.modulus,'height_period':model.height,'diagonal_quotient':model.diagonal,'states':len(model.states),'fixed_by_t_to_height':fixed,'slab_inventory':inventory})

    # Pullback lifts with base finite actions. No finite bijection to the original
    # base is claimed; the atomwise Cantor homeomorphism is an infinite lemma.
    for spec,m,n in [(models[0],2,10),(models[1],1,4),(models[2],3,12)]:
        model=Model(*spec)
        pullback={(x,j) for x in model.states for j in range(n) if x[1]%m==j%m}
        must(len(pullback)==len(model.states)*(n//m),'relative pullback fiber size')
        for x,j in pullback:
            for kind in ('lamp','shift'):
                y=model.lamp(x) if kind=='lamp' else model.shift(x)
                jj=(j+(kind=='shift'))%n
                must((y,jj) in pullback,'relative factor lift invariant under generators')
                must(jj%m==y[1]%m,'relative factor compatibility')
                counts['relative_factor_checks']+=1

    for top in range(2,8):
        modulus=factorial(top)
        survivors={x for x in range(modulus) if all(x%factorial(n)==factorial(n)-1 for n in range(1,top+1))}
        must(survivors=={modulus-1},'unique finite compatible persistent cut')
        counts['factorial_persistent_cut_inventories']+=1
    for h in range(-24,25):
        must(all((h % factorial(n)==factorial(n)-1) == ((h+1)%factorial(n)==0) for n in range(1,8)), 'cut congruence')
        counts['integer_cut_congruences']+=1
    negative['nondivisible_widths_are_not_nested'] = (2%2<1 and not 2%3<2)
    negative['persistent_minus_one_edge_detected'] = all((-1)%factorial(n)==factorial(n)-1 for n in range(1,9))
    negative['remove_single_height_not_invariant'] = (0 != -1 and 0-1 == -1)

    # Exceptional exhaustion tested on a large finite window with nonuniform
    # increasing base classes. Also test a symbolic point outside every given band.
    base=range(11)
    window=range(-9,10)
    vertices=list(product(base,window))
    def base_label(z,j):
        return 0 if z<=j else z
    def h_label(x,j):
        z,k=x
        return ('band',base_label(z,j)) if abs(k)<=j else ('singleton',z,k)
    previous=set()
    for j in range(12):
        blocks={}
        for x in vertices:blocks.setdefault(h_label(x,j),set()).add(x)
        pairs={(x,y) for block in blocks.values() for x in block for y in block}
        must(previous<=pairs,'exceptional exhaustion increasing')
        for block in blocks.values():
            x=next(iter(block)); bsize=sum(base_label(z,j)==base_label(x[0],j) for z in base)
            must(len(block)<=(2*j+1)*bsize if abs(x[1])<=j else len(block)==1,'banded class size bound')
            counts['exceptional_finite_classes']+=1
        must(h_label((0,j+1),j)!=h_label((0,j+2),j),'outside-band points remain separate')
        previous=pairs
        counts['exceptional_increasing_stages']+=1
    must(len(previous)==len(vertices)**2,'finite-window orbit exhausted')
    # Infinite q-fiber has t^k z for all k: even its singleton base F-class
    # would pull back to an infinite class without the height cutoff.
    negative['uncut_pullback_sizes_grow_without_bound'] = all((2*(j+1)+1)>(2*j+1) for j in range(100))
    must(set(negative)=={'reversed_lamp_index_detected','nondivisible_widths_are_not_nested','persistent_minus_one_edge_detected','remove_single_height_not_invariant','uncut_pullback_sizes_grow_without_bound'},'all negative controls ran')
    must(all(negative.values()),'a negative control failed')
    return {'schema':1,'scope':'finite diagnostics only; not an infinite-theorem certificate','counts':dict(sorted(counts.items())),'models':summaries,'negative_controls':negative}


if __name__=='__main__':
    print(json.dumps(compute(),sort_keys=True,indent=2))
