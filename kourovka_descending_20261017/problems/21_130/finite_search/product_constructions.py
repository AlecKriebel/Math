#!/usr/bin/env python3
"""Exact row-path lifting of stored finite certificates, no heuristic search."""
from datetime import datetime,timezone
import itertools
import json
import math
from pathlib import Path
from search import addition_table,coordinates
from verify import verify_file


def encode(vector,p):
    return sum(x*p**i for i,x in enumerate(vector))


def span(basis,p,dim):
    return {tuple(sum(c*v[i] for c,v in zip(coeff,basis))%p for i in range(dim)) for coeff in itertools.product(range(p),repeat=len(basis))}


def basis_for(vectors,p,dim):
    basis=[]; generated={tuple([0]*dim)}
    for v in vectors:
        if tuple(v) not in generated:
            basis.append(tuple(v)); generated=span(basis,p,dim)
    return basis


def cut_edge(cycle,u,v):
    n=len(cycle); i=cycle.index(u)
    if cycle[(i+1)%n]==v:
        return [cycle[(i-k)%n] for k in range(n)]
    assert cycle[(i-1)%n]==v
    return [cycle[(i+k)%n] for k in range(n)]


def base_paths(p,gdim):
    q=p**gdim
    whole=list(range(q))
    if p==5 and gdim==1:
        punctured=[1,2,4,3]
    elif p==3 and gdim==2:
        punctured=[2,5,4,6,1,7,8,3]
    else: raise ValueError('unsupported exact base')
    edges={frozenset((whole[i],whole[(i+1)%q])) for i in range(q)}
    u,v=next((punctured[i],punctured[(i+1)%len(punctured)]) for i in range(len(punctured)) if frozenset((punctured[i],punctured[(i+1)%len(punctured)])) in edges)
    return cut_edge(whole,u,v),cut_edge(punctured,u,v)


def lift_complement(mask,p,dim,gdim):
    q=p**dim; missing=[v for v in range(q) if not mask>>v&1]
    if not missing: return list(range(q)),{'method':'natural_mixed_radix'}
    b=coordinates(missing[0],[p]*dim)
    differences=[tuple((x-y)%p for x,y in zip(coordinates(v,[p]*dim),b)) for v in missing[1:]]
    hb=basis_for(differences,p,dim)
    hdim=dim-gdim
    if len(hb)>hdim: return None,{'affine_complement_rank':len(hb),'maximum_supported_rank':hdim}
    standards=[tuple(int(i==j) for i in range(dim)) for j in range(dim)]
    for v in standards:
        if len(hb)==hdim: break
        if v not in span(hb,p,dim): hb.append(v)
    gb=[]
    for v in standards:
        if len(gb)==gdim: break
        if v not in span(hb+gb,p,dim): gb.append(v)
    assert len(gb)==gdim
    ordered_basis=gb+hb
    forward={}
    for x in range(q):
        coeff=coordinates(x,[p]*dim)
        ambient=tuple((b[i]+sum(c*v[i] for c,v in zip(coeff,ordered_basis)))%p for i in range(dim))
        forward[x]=encode(ambient,p)
    assert len(set(forward.values()))==q
    inverse={v:k for k,v in forward.items()}
    gq=p**gdim; hq=p**hdim
    missing_canonical=[inverse[v] for v in missing]
    assert all(v%gq==0 for v in missing_canonical)
    deleted_rows={v//gq for v in missing_canonical}
    whole_path,punctured_path=base_paths(p,gdim)
    cycle=[forward[g+gq*h] for h in range(hq) for g in (punctured_path if h in deleted_rows else whole_path)]
    z=cycle.index(0); cycle=cycle[z:]+cycle[:z]
    return cycle,{'method':'exact_row_path_lift','p':p,'G_dimension':gdim,'H_dimension':hdim,'affine_origin':b,'G_basis':gb,'H_basis':hb,'deleted_rows':sorted(deleted_rows),'whole_base_path':whole_path,'punctured_base_path':punctured_path}


def main():
    root=Path(__file__).parent/'larger_samples'
    prior=json.loads((root/'rescue_summary.json').read_text())
    original=json.loads((root/'summary.json').read_text())
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'groups':[]}
    original_lookup={g['group']:g for g in original['groups']}
    for group in prior['groups']:
        label=group['group']; path=root/(label+'.jsonl'); rows=[json.loads(s) for s in path.read_text().splitlines()]; header=rows[0]; records={r['mask']:r for r in rows[1:]}; moduli=header['moduli']; remaining=[]; rescued=[]
        if moduli==[3,3,3,3]: p,dim,gdim=3,4,2
        elif moduli==[5,5,5]: p,dim,gdim=5,3,1
        else:
            report['groups'].append({'group':label,'found_witnesses':len(records),'remaining_unknown':group['remaining_unknown'],'rescued':[],'attempted_subsets':original_lookup[label]['attempted_subsets']}); continue
        for item in group['remaining_unknown']:
            mask=item['mask']; cycle,details=lift_complement(mask,p,dim,gdim)
            if cycle is None: remaining.append({**item,'product_lift':details})
            else:
                records[mask]={'mask':mask,'cycle':cycle,'categories':item['categories'],**details}; rescued.append({'mask':mask,**details})
        header['covered_subsets']=len(records)
        path.write_text('\n'.join(json.dumps(x,separators=(',',':')) for x in [header,*[records[k] for k in sorted(records)]])+'\n')
        verified=verify_file(path)
        result={'group':label,'found_witnesses':len(records),'remaining_unknown':remaining,'rescued':rescued,'verification':verified,'attempted_subsets':original_lookup[label]['attempted_subsets']}
        report['groups'].append(result)
        print(label,':',len(rescued),'product-lift rescues;',len(remaining),'unknown;',len(records),'certificates',flush=True)
    (root/'final_summary.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')

if __name__=='__main__': main()
