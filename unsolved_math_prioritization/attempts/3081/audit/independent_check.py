#!/usr/bin/env python3
"""Independent exact audit of pinned original, with optional private input checks.
Only the standard library is used. No original checker is imported.
"""
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import stat
import sys
import zipfile
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parent
AUTHOR_NAME = 'EMPTY_MONOCHROMATIC_3081_AUTHOR_SAFE_FREEZE.zip'
EXTERNAL_NAME = 'EMPTY_MONOCHROMATIC_3081_AUTHOR_EXTERNAL_MANIFEST.json'
AUTHOR_PIN = (15603, '0edf7b3e9c4b7cfc72c0f194cc9a62da4ecf6d946b63e7d1b74e6c4afda41fd1')
EXTERNAL_PIN = (1917, '5d974f4db3baa61297b08dfb753550956951b6c983b5cefe937ec6cc8efec885')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(raw):
    return {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()}

def require_pin(raw, pin, name):
    need((len(raw),hashlib.sha256(raw).hexdigest())==pin, name+' external pin mismatch')

def pinned_members(archive, manifest):
    raw = Path(archive).read_bytes(); external = Path(manifest).read_bytes()
    require_pin(raw,AUTHOR_PIN,'author archive')
    require_pin(external,EXTERNAL_PIN,'author external manifest')
    m=json.loads(external)
    need(m['archive']['name']==AUTHOR_NAME,'archive identity')
    need(digest(raw)=={k:m['archive'][k] for k in ('bytes','sha256')},'external archive metadata')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist(); entries=m['members']
        need(len(names)==len(set(names))==10,'duplicate/missing archive entries')
        need(set(names)=={x['name'] for x in entries},'external member set')
        blobs={}
        for info in z.infolist():
            n=info.filename
            need(n not in ('','.','..') and '/' not in n and '\\' not in n,'unsafe ZIP path')
            need(stat.S_ISREG(info.external_attr>>16),'nonregular ZIP member')
            need(not info.flag_bits & 1,'encrypted ZIP member')
            blobs[n]=z.read(n)
        for row in entries:
            need(digest(blobs[row['name']])=={k:row[k] for k in ('bytes','sha256')},'external member digest')
    internal=json.loads(blobs['MANIFEST.json'])['files']
    need(len(internal)==9 and len({x['name'] for x in internal})==9,'internal membership')
    need({x['name'] for x in internal}|{'MANIFEST.json'}==set(blobs),'internal/external member set')
    for row in internal:
        need(digest(blobs[row['name']])=={k:row[k] for k in ('bytes','sha256')},'internal member digest')
    return blobs

def cross(u,v):
    return u[0]*v[1]-u[1]*v[0]

def sub(u,v):
    return (u[0]-v[0],u[1]-v[1])

def barycentric(p,a,b,c):
    # Solve p=a+u(b-a)+v(c-a), independently from the author's sign/area predicates.
    ab,ac,ap=sub(b,a),sub(c,a),sub(p,a)
    d=cross(ab,ac)
    need(d!=0,'degenerate triangle')
    u=F(cross(ap,ac),d); v=F(cross(ab,ap),d)
    return (1-u-v,u,v)

def strict(p,a,b,c):
    return all(t>0 for t in barycentric(p,a,b,c))

def validate_points(points):
    need(all(type(p) is list and len(p)==2 and all(type(v) is int for v in p) for p in points),'integer points')
    need(len(set(map(tuple,points)))==len(points),'duplicate point')
    dets=[cross(sub(points[b],points[a]),sub(points[c],points[a])) for a,b,c in itertools.combinations(range(len(points)),3)]
    need(all(d!=0 for d in dets),'collinear triple')
    return dets

def enumerate_mono(points,colors):
    rows=[]
    for tri in itertools.combinations(range(len(points)),3):
        if len({colors[i] for i in tri})!=1:continue
        interior=[i for i in range(len(points)) if i not in tri and strict(points[i],*(points[j] for j in tri))]
        rows.append({'vertices':list(tri),'inside':interior})
    return rows

def witness(cert):
    points,colors=cert['points'],cert['colors']
    need(len(points)==len(colors)==8,'eight points')
    need(all(type(c) is int and c in (0,1) for c in colors),'binary colors')
    need(sum(colors)==4,'balanced colors')
    dets=validate_points(points)
    rows=enumerate_mono(points,colors)
    need(rows==cert['monochromatic_triangles'],'independent interior mismatch')
    need(len(rows)==8 and all(len(r['inside'])==1 and colors[r['inside'][0]]!=colors[r['vertices'][0]] for r in rows),'opposite blockers')
    e0=sum(not r['inside'] for r in rows); e1=sum(len(r['inside'])==1 for r in rows)
    need(e0==cert['E0']==0 and e1==cert['E1']==8,'witness counts')
    coloring_counts=[]
    for mask in range(256):
        co=[(mask>>i)&1 for i in range(8)]
        rr=enumerate_mono(points,co)
        empty=sum(not r['inside'] for r in rr); almost=sum(len(r['inside'])<=1 for r in rr)
        major=max(sum(co),8-sum(co)); minor=8-major
        need(3*empty>=major*max(major-minor-2,0),'discrepancy inequality')
        need(3*almost>=major*max(major-2-minor//2,0),'almost-empty inequality')
        coloring_counts.append((empty,almost))
    # Recompute empty triangles in each induced subset, rather than use the original interior list.
    histogram={}; expectation=F(0)
    for mask in range(256):
        selected=[i for i in range(8) if (mask>>i)&1]
        pp=[points[i] for i in selected]; cc=[colors[i] for i in selected]
        count=sum(not r['inside'] for r in enumerate_mono(pp,cc))
        histogram[count]=histogram.get(count,0)+1
        expectation+=F(count,256)
    need(expectation==F(1,2),'thinning subset expectation')
    weights=[]
    for row in rows:
        weights.append({'vertices':row['vertices'],'inside':row['inside'][0], 'barycentric':[str(v) for v in barycentric(points[row['inside'][0]],*(points[j] for j in row['vertices']))]})
    return {'E0':e0,'E1':e1,'orientations':len(dets),'minimum_absolute_determinant':min(map(abs,dets)),'all_colorings_checked':256,'subsets_recomputed':256,'thinning_expectation':str(expectation),'subset_empty_count_histogram':histogram,'barycentric_certificates':weights}

def family():
    results=[]
    for k in range(1,31):
        p=[[2*i,2*i*i] for i in range(-k,k+1)]; q=[0,1]; r=len(p)
        validate_points(p+[q])
        blocked=[]
        for tri in itertools.combinations(range(r),3):
            if strict(q,*(p[i] for i in tri)):blocked.append(tri)
        expected={(k-i,k,k+j) for i in range(1,k+1) for j in range(1,k+1)}
        need(set(blocked)==expected and len(blocked)==k*k,'family triangle classification')
        fan_hits=[]
        for pivot in range(r):
            cyclic=[(pivot+j)%r for j in range(1,r)]
            fan=[(pivot,cyclic[j],cyclic[j+1]) for j in range(r-2)]
            hit=sum(strict(q,*(p[i] for i in tri)) for tri in fan)
            need(hit==1,'per-pivot face uniqueness');fan_hits.append(hit)
        need(sum(fan_hits)==r,'incidence multiplicity')
        results.append({'k':k,'red_points':r,'E1':len(blocked),'E0':math.comb(r,3)-len(blocked),'blocked_fan_incidences':sum(fan_hits)})
    return results

def controls(cert):
    results=[]
    for mode in ('wrong_blocker','duplicate','collinear','unbalanced','wrong_E0','same_color_blocker'):
        x=copy.deepcopy(cert)
        if mode=='wrong_blocker':x['monochromatic_triangles'][0]['inside']=[1]
        if mode=='duplicate':x['points'][0]=x['points'][1].copy()
        if mode=='collinear':x['points'][0]=[2*x['points'][1][j]-x['points'][2][j] for j in range(2)]
        if mode=='unbalanced':x['colors'][0]=1
        if mode=='wrong_E0':x['E0']=1
        if mode=='same_color_blocker':x['colors'][0],x['colors'][4]=x['colors'][4],x['colors'][0]
        try:witness(x)
        except ValueError as e:results.append({'case':mode,'rejected':True,'diagnostic':str(e)})
        else:raise ValueError('control accepted: '+mode)
    # Reject edge/vertex points under strict containment, accept a known positive interior.
    a,b,c=[0,0],[4,0],[0,4]
    for p in ([0,0],[2,0],[0,2],[2,2]):need(not strict(p,a,b,c),'boundary counted as interior')
    need(strict([1,1],a,b,c),'interior excluded')
    results.append({'case':'strict_boundary_predicate','rejected_boundary_points':4,'interior_control':True})
    return results

def corpora(directory,blobs):
    if directory is None:return {'requested':False}
    gate=json.loads(blobs['CORPUS_GATE.json']); data={}; public={}
    for key,filename in [('catalog','catalog.json'),('problems','problems.json'),('reports','research_results.json')]:
        raw=(Path(directory)/filename).read_bytes(); expected=gate['corpora'][key]
        need(digest(raw)==expected['digest'],'corpus full-file digest: '+key)
        obj=json.loads(raw); need(len(obj)==expected['entries'],'corpus entry count: '+key)
        data[key]=obj;public[key]={'digest':digest(raw),'entries':len(obj)}
    cat=[x for x in data['catalog'] if str(x.get('id'))=='3081']
    rec=[x for x in data['problems'] if str(x.get('id'))=='3081']
    need(len(cat)==len(rec)==1,'unique exact ID')
    need(cat[0]['rank']==926 and cat[0]['problem_number']==rec[0]['problem_number']=='OPG-2435','exact ID/rank/number')
    need('OPG-2435' not in data['reports'],'report absence')
    pair=hashlib.sha256(json.dumps([rec[0],{}],sort_keys=True).encode()).hexdigest()
    need(pair==gate['exact_pair_sha256']==cat[0]['review_hash'],'unprojected default serialized pair')
    return {'requested':True,'verified':True,'corpora':public,'unique_id':3081,'rank':926,'problem_number':'OPG-2435','report_absent':True,'exact_pair_sha256':pair}

def sources(directory,blobs):
    if directory is None:return {'requested':False}
    rows=[]
    for row in json.loads(blobs['SOURCE_VERIFICATION.json'])['retrievals']:
        if row.get('status')!=200:continue
        actual=digest((Path(directory)/row['filename']).read_bytes())
        need(actual=={k:row[k] for k in ('bytes','sha256')},'source full bytes: '+row['filename'])
        rows.append({'filename':row['filename'],'digest':actual,'verified':True})
    return {'requested':True,'verified':True,'count':len(rows),'files':rows}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,default=ROOT/AUTHOR_NAME)
    p.add_argument('--external-manifest',type=Path,default=ROOT/EXTERNAL_NAME)
    p.add_argument('--corpus-dir');p.add_argument('--source-dir');p.add_argument('--skip-family',action='store_true')
    a=p.parse_args();blobs=pinned_members(a.archive,a.external_manifest); cert=json.loads(blobs['certificate.json'])
    result={'status':'PASS','author_archive_pin_verified':True,'author_external_manifest_pin_verified':True,'exact_original_members':10,'geometry':witness(cert),'independent_controls':controls(cert),'family':family() if not a.skip_family else 'skipped by request','corpora':corpora(a.corpus_dir,blobs),'sources':sources(a.source_dir,blobs),'scope':'Exact finite verification supplements the written all-k proof; no asymptotic advance.'}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,TypeError,zipfile.BadZipFile) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
