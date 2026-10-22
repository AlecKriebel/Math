"""Independent read-only input audit; writes result only next to this source."""
from pathlib import Path, PurePosixPath
import hashlib,json,stat,zipfile,io

HERE=Path(__file__).resolve().parent;CASE=HERE.parent
REPO=Path('/Users/alec/Documents/Math')
def need(x,s):
    if not x:raise AssertionError(s)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def regular(root,p):
    q=PurePosixPath(p);need(not q.is_absolute() and q.parts and all(x not in ('.','..','') for x in q.parts) and str(q)==p,'relative path '+p)
    p=root/p;need(p.resolve()==p.absolute() and stat.S_ISREG(p.lstat().st_mode),'regular canonical '+str(p));return p.read_bytes()
def matches(b,r):return pin(b)=={k:r[k] for k in ('bytes','sha256')}
def main():
    path='publication_adoption_01/FROZEN_SCIENTIFIC_PACKAGE_MANIFEST_01.json'
    raw=regular(CASE,path);need(pin(raw)=={'bytes':43359,'sha256':'b8efc3c62035cb99bebe2dbbc37417717a7191e3be0db1c4fbf0eaaebc438e74'},'root specified freeze')
    m=json.loads(raw);seal=json.loads(regular(CASE,'publication_adoption_01/EXTERNAL_SEAL_01.json'))
    need(seal['manifest_pin']==pin(raw),'external seal binding')
    rows=m['files'];names=[r['case_path'] for r in rows]
    need(len(rows)==146==m['file_count']==seal['file_count'] and len(set(names))==len(names) and names==sorted(names),'selection inventory')
    need(sum(r['bytes'] for r in rows)==1788974==m['total_bytes']==seal['total_bytes'],'selection bytes')
    bodies={r['case_path']:regular(CASE,r['case_path']) for r in rows}
    for r in rows:need(matches(bodies[r['case_path']],r),'selected body '+r['case_path'])
    families=[]
    for g in m['original_authored_family_mapping']:
        fm=bodies[g['manifest_case_path']];need(matches(fm,g),'original manifest '+g['family'])
        rr=json.loads(fm)['files'];need(len(rr)==len(g['rows']),'mapping closure')
        for a,b in zip(rr,g['rows']):
            old=a.get('path',a.get('relative_path'));need(old==b['original_relative_path'],'mapping order')
            need(matches(bodies[b['case_path']],a),'mapped payload')
            # Confirm alias is identical to its preserved original, too.
            need(bodies[b['case_path']]==regular(CASE,g['family']+'/'+old),'preserved original identity')
        families.append({'family':g['family'],'payloads':len(rr),'manifest_pin':pin(fm)})
    pubs=[]
    for r in m['existing_published_files']:
        b=regular(REPO,r['path']);need(matches(b,r),'published body '+r['path'])
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(oid==r['sha'],'published native blob')
        pubs.append({'path':r['path'],'pin':pin(b),'native_blob':oid})
    pre=REPO/'draft_pr_descending_audit_20261002/audits/pr211_5100063/preprint'
    arc=(pre/'k904a-source-verification.zip').read_bytes();src=json.loads((pre/'SOURCE_MANIFEST.json').read_bytes())
    wrap='k904a_outer_focal_inverse_product/'
    z=zipfile.ZipFile(io.BytesIO(arc));need(z.testzip() is None,'ZIP CRC');need(len(z.infolist())==151,'ZIP entries')
    data={}
    for e in z.infolist():
        need(e.filename.startswith(wrap),'exact wrapper');n=e.filename[len(wrap):];p=PurePosixPath(n)
        need(str(p)==n and not p.is_absolute() and '..' not in p.parts and n not in data and not e.is_dir(),'ZIP canonical duplicate')
        need(stat.S_IFMT(e.external_attr>>16) in (0,stat.S_IFREG),'ZIP regular type');data[n]=z.read(e)
    need(set(data)=={r['path'] for r in src['files']}|{'SOURCE_MANIFEST.json'},'ZIP full closure')
    need(data['SOURCE_MANIFEST.json']==(pre/'SOURCE_MANIFEST.json').read_bytes(),'ZIP own source manifest body')
    for r in src['files']:need(matches(data[r['path']],r),'ZIP payload '+r['path'])
    custody=json.loads(bodies['native_custody_01/public/CUSTODY_IDENTITIES.json'])
    coverage=custody['original_history_exact_coverage']['records'];need(len(coverage)==19,'original19 coverage')
    for r in coverage:
        rel=r['original_path'].split('attempts/5100063/',1)[1]
        b=data['pr_update/5100063/history/original_submission_20261015/'+rel]
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(oid==r['original_git_blob']==r['archive_git_blob'],'original raw native identity')
    # Actual already-read provider responses; summaries alone are not identities.
    prv=CASE/'provider_readback_01/_private';rec=json.loads((prv/'ACTUAL_PUBLIC_ZENODO_RECORD.json').read_bytes())
    metadata=json.loads((pre/'metadata.json').read_bytes());dep=json.loads((pre/'deposit.json').read_bytes())
    need(dep['metadata']==metadata,'metadata/deposit equality')
    need(str(rec['id'])=='23394004' and rec['doi']=='10.5281/zenodo.23394004','existing DOI')
    need(rec['metadata']['title']==metadata['title'] and rec['metadata']['version']==metadata['version'],'provider title/version')
    need(rec['metadata']['creators'][0]['name']==metadata['creators'][0]['name'],'provider author')
    for field in ('title','publication_date','description','access_right','creators','keywords','version'):
        need(rec['metadata'][field]==metadata[field],'provider complete metadata field '+field)
    need(rec['metadata']['resource_type']['type']==metadata['upload_type'] and rec['metadata']['resource_type']['subtype']==metadata['publication_type'] and rec['metadata']['license']['id']==metadata['license'],'provider normalized type/license')
    for name,local in [('k904a-outer-focal-inverse-areas.pdf','manuscript.pdf'),('k904a-source-verification.zip','k904a-source-verification.zip')]:
        need((prv/('ACTUAL_PUBLIC_'+name)).read_bytes()==(pre/local).read_bytes(),'downloaded public body')
    row=json.loads((prv/'ACTUAL_GWS_ROW109.json').read_bytes())
    table=json.loads((prv/'ACTUAL_GWS_DOI_COLUMN.json').read_bytes())
    need(row['range']=="'Math Puzzles'!A109:D109" and len(row['values'])==1 and len(row['values'][0])==4,'tracker exact range/shape')
    need(row['values'][0][0]=='https://arxiv.org/abs/2004.12497v11' and row['values'][0][2]=='https://doi.org/10.5281/zenodo.23394004','tracker identifiers')
    matches_rows=[i for i,r in enumerate(table['values'],1) if any('23394004' in str(v) for v in r)]
    need(matches_rows==[109],'tracker unique DOI109')
    return {'schema':'review02-independent-input-audit-v1','status':'PASS','frozen_manifest':pin(raw),'external_seal':pin(regular(CASE,'publication_adoption_01/EXTERNAL_SEAL_01.json')),'selected_files':len(rows),'selected_bytes':sum(r['bytes'] for r in rows),'families':families,'publication_files':pubs,'ZIP':{'CRC':'PASS','regular_wrapped_entries':len(data),'source_pins':len(src['files']),'original_raw_native_blobs_matched':len(coverage)},'provider':{'DOI':rec['doi'],'created':rec['created'],'all_deposit_metadata_fields_match':True,'downloaded_PDF_ZIP_equal':True,'tracker_range':row['range'],'unique_DOI_rows':matches_rows,'historical_review_wording_not_new_review_authority':True,'tracker_row_pin':pin((prv/'ACTUAL_GWS_ROW109.json').read_bytes()),'tracker_column_pin':pin((prv/'ACTUAL_GWS_DOI_COLUMN.json').read_bytes())},'limits':'No live network/native/provider/tracker read; existing freshly recorded response bytes audited. Does not establish original visibility or worldwide priority.'}
if __name__=='__main__':
    r=main();(HERE/'INPUT_INTEGRITY.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('status','selected_files','selected_bytes','families','ZIP')},indent=2))
