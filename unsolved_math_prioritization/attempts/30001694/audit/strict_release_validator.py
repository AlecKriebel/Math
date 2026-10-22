#!/usr/bin/env python3
"""Controlling validator for the exact historical packet, independent of its verifiers.
Run: python strict_release_validator.py ORIGINAL.zip [--controls]
Uses the adjacent independent_controls.py; no original code is imported or executed.
Checks remain active under python -O. All original input is read-only.
"""
import argparse, csv, hashlib, io, json, re, zipfile
from pathlib import Path
import independent_controls as independent

ARCHIVE_SHA256='20635fa3e641d5df4ae3ad88bc439a9aed34d31d6eac8dcbcf563087c7f8e1fc'
ARCHIVE_BYTES=61552
CERT_SHA256='d99ad6afbf115cb369514b08313bc32f88a57899641bb4b50ba6272f5b32e1d0'
CERT_BYTES=281944
PAYLOAD={'PRIOR_ATTEMPT_CHECKS.json','PROOFS.md','README.md','RESEARCH_LOG.md','SOURCE_VERIFICATION.json','STATUS.json','computation/certificate.csv','computation/summary.json','computation/tests.txt','computation/verification.json','compute.py','test_checks.py','verify.py','verify_manifest.py'}
HEADER=['mask','s','max_side_squared','block_x','block_y','x0','y0','x1','y1','x2','y2','x3','y3']

class Invalid(ValueError):pass

def require(condition,message):
    if not condition:raise Invalid(message)

def unique_object(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'duplicate JSON key: '+k);out[k]=v
    return out

def parse_json(raw):return json.loads(raw,object_pairs_hook=unique_object)

def expected_data():
    result={}
    for mask in range(1,65536):
        if independent.admissible_euler(independent.cells(mask)):
            s,m,b,sq,axis=independent.analyze(mask)
            result[mask]={'s':s,'m':m,'squares':{q for q,z in sq if z==m}}
    require(len(result)==9349,'independent admissibility count changed')
    return result

def certificate(raw,expected):
    reader=csv.reader(io.StringIO(raw.decode('utf-8'),newline=''))
    require(next(reader,None)==HEADER,'incorrect certificate header')
    rows={}
    for line,fields in enumerate(reader,start=2):
        require(len(fields)==len(HEADER),f'incorrect column count at line {line}')
        require(all(re.fullmatch(r'-?(?:0|[1-9][0-9]*)',x) is not None and str(int(x))==x for x in fields),f'noncanonical integer at line {line}')
        r=dict(zip(HEADER,map(int,fields)));mask=r['mask']
        require(1<=mask<=65535,f'out-of-domain mask: {mask}')
        require(mask not in rows,f'duplicate mask: {mask}')
        rows[mask]=r
    require(len(rows)==9349,f'incorrect row count: {len(rows)}')
    require(set(rows)==set(expected),'certificate key set differs from independently admissible set')
    for mask,r in rows.items():
        e=expected[mask];s=r['s'];m=r['max_side_squared']
        require((s,m)==(e['s'],e['m']),f'incorrect maxima: {mask}')
        ox,oy=r['block_x'],r['block_y']
        require(0<=ox<=4-s and 0<=oy<=4-s,f'block outside box: {mask}')
        block=sum(1<<(4*(oy+j)+ox+i) for j in range(s) for i in range(s))
        require(mask&block==block,f'block witness has absent cell: {mask}')
        q=tuple((r[f'x{i}'],r[f'y{i}']) for i in range(4))
        require(q==tuple(sorted(q)) and q in e['squares'],f'incorrect maximum square witness: {mask}')
        require(2*m>=s*s,f'target failure: {mask}')
    return {'row_count':len(rows),'exact_key_domain':True,'duplicate_free':True,'full_admissible_set_equality':True,'all_maxima_and_witnesses_match':True}

def package_members(members):
    require(set(members)==PAYLOAD|{'MANIFEST.json'},'exact package member set mismatch')
    manifest=parse_json(members['MANIFEST.json'])
    require(set(manifest['files'])==PAYLOAD,'exact manifest key set mismatch')
    for path in sorted(PAYLOAD):
        raw=members[path];bound=manifest['files'][path]
        require(len(raw)==bound['bytes'],f'byte-count mismatch: {path}')
        require(hashlib.sha256(raw).hexdigest()==bound['sha256'],f'hash mismatch: {path}')
    return {'payload_files':len(PAYLOAD),'all_payload_hashes_match':True,'exact_inventory_match':True}

def load_archive(path):
    raw=path.read_bytes()
    require(len(raw)==ARCHIVE_BYTES,'archive byte-count mismatch')
    require(hashlib.sha256(raw).hexdigest()==ARCHIVE_SHA256,'archive hash mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),'duplicate archive member names')
        members={n:z.read(n) for n in names}
    return members

def controls(members,expected):
    original=members['computation/certificate.csv'];rows=list(csv.reader(io.StringIO(original.decode())));out={}
    def encode(rows):
        f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerows(rows);return f.getvalue().encode()
    variants={}
    for label,value in [('extra_mask_zero','0'),('extra_mask_65536','65536'),('extra_mask_negative','-1')]:
        r=[x[:] for x in rows];z=r[1][:];z[0]=value;r.append(z);variants[label]=encode(r)
    r=[x[:] for x in rows];r.append(r[1][:]);variants['duplicate_mask']=encode(r)
    variants['missing_row']=encode(rows[:1]+rows[2:])
    r=[x[:] for x in rows];r[1][2]='2';variants['altered_maximum']=encode(r)
    r=[x[:] for x in rows];r[1][1]='2';variants['altered_s']=encode(r)
    r=[x[:] for x in rows];r[1][5]='99';variants['altered_square_vertex']=encode(r)
    r=[x[:] for x in rows];r[1][3]='99';variants['altered_block_origin']=encode(r)
    r=[x[:] for x in rows];r[1][0]='5';variants['equal_count_inrange_invalid_mask']=encode(r)
    r=[x[:] for x in rows];r[0][2]='side';variants['altered_header']=encode(r)
    r=[x[:] for x in rows];r[1].append('0');variants['extra_column']=encode(r)
    r=[x[:] for x in rows];r[1][0]='01';variants['noncanonical_integer']=encode(r)
    for label,raw in variants.items():
        try:certificate(raw,expected)
        except Invalid as e:out[label]={'rejected':True,'reason':str(e)}
        else:raise Invalid('negative control unexpectedly accepted: '+label)
    for label,key in [('extra_nested_manifest','extra/MANIFEST.json'),('extra_ordinary_file','extra.txt')]:
        changed=dict(members);changed[key]=b'unmanifested data'
        try:package_members(changed)
        except Invalid as e:out[label]={'rejected':True,'reason':str(e)}
        else:raise Invalid('inventory control unexpectedly accepted: '+label)
    try:parse_json(b'{"files":{},"files":{}}')
    except Invalid as e:out['duplicate_manifest_json_key']={'rejected':True,'reason':str(e)}
    else:raise Invalid('duplicate JSON key accepted')
    changed=dict(members);changed['README.md']+=b'changed'
    try:package_members(changed)
    except Invalid as e:out['altered_payload_bytes']={'rejected':True,'reason':str(e)}
    else:raise Invalid('altered payload accepted')
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--controls',action='store_true');a=p.parse_args()
    members=load_archive(a.archive);pk=package_members(members);raw=members['computation/certificate.csv']
    require(len(raw)==CERT_BYTES and hashlib.sha256(raw).hexdigest()==CERT_SHA256,'exact certificate binding mismatch')
    expected=expected_data();cert=certificate(raw,expected)
    result={'controlling_validator':'strict_release_validator.py','input_archive_sha256':ARCHIVE_SHA256,'input_archive_bytes':ARCHIVE_BYTES,'certificate_sha256':CERT_SHA256,'certificate_bytes':CERT_BYTES,'package':pk,'certificate':cert,'author_verifiers_used':False,'passed':True}
    if a.controls:result['negative_controls']=controls(members,expected)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
