#!/usr/bin/env python3
"""Offline source authentication and finite diagnostics; written proof is decisive.

No network, subprocess, source-author code, service action, or credential access.
All guards survive -O/-OO. The density m of C minus {+-1} is NOT numerically evaluated.
"""
import argparse
import hashlib
import json
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
COUNTS = {}


def require(value, label):
    if not value:
        raise RuntimeError(label)


def count(label):
    COUNTS[label] = COUNTS.get(label, 0) + 1


def readj(name):
    return json.loads((BASE / name).read_text())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pair(x, y=0):
    return F(x), F(y)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def norm(a):
    return a[0]**2 + a[1]**2


def div(a, b):
    n = norm(b)
    require(n > 0, 'complex denominator nonzero')
    c = mul(a, (b[0], -b[1]))
    return c[0]/n, c[1]/n


def dec(x):
    x = F(x)
    return Decimal(x.numerator) / Decimal(x.denominator)


def close(a, b):
    return abs(a-b) <= Decimal('1e-70') * max(Decimal(1), abs(a), abs(b))


def expected_failure(call, label):
    try:
        call()
    except RuntimeError:
        count('rejected_wrong_science')
    else:
        raise RuntimeError('bad control escaped: '+label)


def anchors():
    binding = readj('INPUT_BINDING.json')
    require(binding['head'] == '32e8b9914ed26fbba30c102f7ce109458b0d521c', 'head')
    require(len(binding['files']) == 6, 'six actual PR files')
    for e in binding['files']:
        b = (BASE / e['local']).read_bytes()
        require(len(b) == e['bytes'] and sha(b) == e['sha256'], 'PR SHA256 '+e['local'])
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == e['git_blob_sha1'], 'Git blob identity')
        count('authenticated_PR_blobs')
    for e in readj('AUTHENTICATED_INPUTS.json')['files']:
        b = (BASE/e['path']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'], 'input pin '+e['path'])
        count('authenticated_local_inputs')
    for e in readj('ROOT_ANCHORS.json')['files']:
        b=(ROOT/e['path']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'], 'external root anchor '+e['path'])
        count('authenticated_root_anchors')
    manifest=readj('private/pr_source/ARTIFACT_MANIFEST.json')
    for e in manifest['files']:
        b=(BASE/'private/pr_source'/e['path']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'], 'submitted manifest')
    retrieval=readj('private/primary/RETRIEVAL.json')
    for key,expected in [('original','8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),('he_tang','83b2cb1d7579ab337630c9613018ffd6816d5a5628f0aa475e74832c1e14946f')]:
        e=next(e for e in retrieval if e['key']==key)
        require(e['status']==200 and e['sha256']==expected, 'fresh versioned primary')
        require(sha((BASE/e['file']).read_bytes())==expected, 'actual primary bytes')
    meta=readj('private/primary/datacite.json')['data']['attributes']
    require(meta['doi']=='10.48550/arxiv.2603.16676' and meta['types']['resourceTypeGeneral']=='Preprint', 'preprint DOI identity')
    require([c['familyName'] for c in meta['creators']]==['He','Tang'], 'source authors')


def diagnostics():
    inputs=readj('CONTROL_INPUTS.json')
    one=pair(1)
    for astr in inputs['mobius_a']:
        a=F(astr)
        require(0<a<F(1,2), 'a range')
        for z0 in inputs['disk_points']:
            z=pair(*z0);den=sub(one,mul(pair(a),z))
            require(norm(z)<1, 'disk interior')
            phi=div(sub(z,pair(a)),den)
            require((1-norm(phi))*norm(den)==(1-a*a)*(1-norm(z)), 'Mobius disk identity')
            require(norm(phi)<1 and div(add(phi,pair(a)),add(one,mul(pair(a),phi)))==z, 'Mobius inverse')
            h=pair(F(1,1000));zh=add(z,h)
            require(norm(zh)<1, 'difference quotient interior')
            phih=div(sub(zh,pair(a)),sub(one,mul(pair(a),zh)))
            require(sub(phih,phi)==div(mul(h,pair(1-a*a)),mul(sub(one,mul(pair(a),zh)),den)), 'exact derivative numerator')
            count('exact_mobius_interior')
        for z0 in inputs['circle_points']:
            z=pair(*z0)
            require(norm(z)==1 and norm(div(sub(z,pair(a)),sub(one,mul(pair(a),z))))==1, 'Mobius circle')
            count('exact_mobius_boundary')
    for w0 in inputs['left_halfplane_points']:
        w=pair(*w0);require(w[0]<0, 'left halfplane')
        c=div(add(w,one),sub(w,one))
        require(norm(c)<1, 'Cayley disk')
        require((1-norm(c))*norm(sub(w,one))==-4*w[0], 'Cayley normalization')
        require(div(add(c,one),sub(c,one))==w, 'Cayley inverse')
        # |c'|/(1-|c|^2) = 1/(-2 Re w); denominators rational.
        require(F(2)/norm(sub(w,one))/(1-norm(c))==1/(-2*w[0]), 'curvature -4 factor')
        count('exact_cayley_halfplane')
    with localcontext() as context:
        context.prec=85
        last=Decimal(0)
        for n in inputs['dyadic_exponents']:
            a=Decimal(2)**(-n);ell=(1/a).ln()
            puncture=1/(2*a*ell)
            single=(1-a*a)/(2*a*ell)
            require(close(puncture*(1-a*a),single), 'one puncture transform')
            require(close(1/(2*ell),puncture*a), 'exponential covering identity')
            require(close(2*single,(1-a*a)/(a*ell)), 'two singles sum')
            # m is factored OUT: this computes Q_lower/m, never Q or m.
            normalized=(1/a)/(2*single)
            require(close(normalized,ell/(1-a*a)), 'normalized lower quotient')
            require(normalized>Decimal(n)/2 and normalized>last, 'dyadic divergence certificate diagnostic')
            last=normalized
            for rstr in inputs['radii']:
                radius=dec(rstr);require(radius>0, 'positive radius')
                physical=radius*a
                direct=(1-a*a)/(2*physical*ell)
                require(close(direct,single/radius), 'physical puncture radius formula')
                for factorstr in inputs['normalization_factors']:
                    factor=dec(factorstr)
                    scaled=(factor/(radius*a))/(2*factor*single/radius)
                    require(close(scaled,normalized), 'normalization and radius quotient cancellation')
                    count('decimal_radius_normalization')
            count('dyadic_formula_checks')
        expected_failure(lambda: require(F(15,16)==1, 'omitted derivative must fail at a=1/4'), 'missing Mobius derivative')
        expected_failure(lambda: require(close(single,2*single), 'mixed curvature normalization must fail'), 'mixed normalization')
    # Abstract positive cover derivatives pG = pH*f imply lambdaG>=lambdaH.
    for phstr in inputs['positive_parameters']:
        ph=F(phstr)
        for fstr in inputs['schwarz_derivatives']:
            f=F(fstr);require(0<f<=1, 'Schwarz derivative')
            pg=ph*f
            require(1/pg>=1/ph, 'correct inclusion direction')
            if f<1:require(1/pg>1/ph, 'strict abstract derivative example')
            count('exact_cover_direction')
    expected_failure(lambda: require(F(1)/F(1,4)<=F(1)/F(1,2),'reversed monotonicity'), 'wrong inclusion direction')
    # For every positive formal m and finite A>0, integer n>2A/m and a=2^-n
    # suffice, since log 2 = integral_1^2 dt/t > 1/2. No actual m is sampled.
    for mstr in inputs['positive_parameters']:
        formal_m=F(mstr)
        for astr in inputs['thresholds']:
            A=F(astr);q=2*A/formal_m
            n=max(2,q.numerator//q.denominator+1)
            require(formal_m*F(n,2)>A and F(1,2**n)<F(1,2), 'exact quantified dyadic choice')
            count('formal_positive_m_quantifiers')
    expected_failure(lambda: require(F(2)/F(1,4)==F(1,4)*2, 'wrong scaling'), 'multiply rather than divide')
    for astr in inputs['mobius_a']:
        a=F(astr);punctures=[pair(a),pair(-a)]
        for x0,y0 in inputs['topology_endpoints']:
            x,y=pair(*x0),pair(*y0)
            require(norm(x)<1 and norm(y)<1 and x not in punctures and y not in punctures,'valid path endpoints')
            # A finite rational diagnostic of the analytic off-finitely-many-lines argument.
            def cross(u,v):return u[0]*v[1]-u[1]*v[0]
            found=None
            for k in range(2,100):
                t=pair(F(1,k),F(1,k*k))
                if norm(t)<1 and all(cross(sub(t,x),sub(p,x))!=0 and cross(sub(t,y),sub(p,y))!=0 for p in punctures):
                    found=t;break
            require(found is not None,'two segment path avoiding punctures')
            count('rational_path_constructions')


def accounting():
    aliases=readj('ALIASES.json')
    source=readj('ROOT_ANCHORS.json')
    ledger=json.loads((ROOT/'raw/pr1273/ledger_live.json').read_text())
    rows=ledger['response']['values']
    require(len(rows)==191 and ledger['response']['range'].endswith('A1:AQ1178'), 'root full requested range snapshot')
    hits=[]
    for n,row in enumerate(rows,1):
        for a in aliases['direct']:
            if any(a.casefold() in str(cell).casefold() for cell in row):hits.append((n,a))
    require(not hits,'unexpected direct target ledger alias')
    broad=[n for n,row in enumerate(rows,1) if any('fuchs' in str(c).casefold() for c in row)]
    require(broad==[61,92,103], 'all broad Fuchs rows exposed')
    distinct_records={
        23267641:('23267640','On Seven Conjectures of Fuchs on Billiard Trajectories in Regular Polygons and Geodesics on the Regular Dodecahedron'),
        23308905:('23308904',"A cone-angle proof of Fuchs's labelled length-ratio conjecture"),
        23384007:('23384006','A parity-selected endpoint theorem for the regular dodecahedron'),
        23389367:('23389366','Parallel short trajectories in regular polygons: a type convention and signed angle law'),
    }
    for record,(concept,title) in distinct_records.items():
        d=json.loads((ROOT/f'raw/pr1273/zenodo_{record}.json').read_text())
        require(str(d['id'])==str(record) and d['conceptrecid']==concept and d['doi']==f'10.5281/zenodo.{record}' and d['metadata']['title']==title, 'exact reasoned distinct-record identity')
        count('distinct_account_record_bodies')
    proposal=readj('LITERAL_FOUR_CELL_PROPOSAL.json')
    require(isinstance(proposal,list) and len(proposal)==4 and all(type(s) is str for s in proposal) and proposal[1]=='', 'literal four cells blank B')
    require(proposal[2]=='https://doi.org/10.48550/arXiv.2603.16676', 'existing exact preprint DOI')
    disposition=readj('ACCOUNTING_DISPOSITION.json')
    require(disposition['publication_ready'] is False and disposition['new_publication'] is False and disposition['root_adopted'] is False,'no readiness or adoption')
    count('literal_row_checked')


def package():
    m=readj('MANIFEST.json')
    excluded=set(m['self_exclusions'])
    expected={e['path'] for e in m['files']}
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}-excluded
    require(actual==expected, 'closed package exact file membership')
    for p in BASE.rglob('*'):require(not p.is_symlink(),'no package symlinks')
    for e in m['files']:
        b=(BASE/e['path']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'], 'closed payload '+e['path'])
    require(sum(p.stat().st_blocks*512 for p in BASE.rglob('*') if p.is_file())<=25*1024**2,'25MiB allocation cap')
    count('closed_package_readback')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-package',action='store_true')
    parser.add_argument('--deliberate-bad-guard',action='store_true')
    args=parser.parse_args()
    anchors();diagnostics();accounting()
    if args.deliberate_bad_guard:require(False,'deliberate optimization-safe failure')
    if args.verify_package:package()
    print(json.dumps({'status':'PASS','optimize':sys.flags.optimize,'counts':COUNTS,'checker_sha256':sha(Path(__file__).read_bytes()),'proof_role':'finite diagnostics supplement written proof; no value for m computed; no service action'},sort_keys=True))


if __name__=='__main__':main()
