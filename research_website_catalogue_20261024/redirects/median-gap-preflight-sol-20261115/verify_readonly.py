#!/usr/bin/env python3
"""Pure offline custody: standard library only; no project-code imports or execution."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

O=Path(__file__).resolve().parent
EXCLUDED={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
COMMIT='1ef94e0144b2b6a7f42868154d6c3f11b3ec6d41'
TREE='4b890b5e4f583ed562ba7291ae367c6ff70c5090'
N=0


def need(ok,message):
    global N
    N+=1
    if not ok:raise RuntimeError(message)


def sha(b):return hashlib.sha256(b).hexdigest()


def load(p):return json.loads(p.read_text())


def bound(row,root=None):
    if root:
        n=row['path'];p=PurePosixPath(n)
        need(not p.is_absolute() and '..' not in p.parts and str(p)==n,'Unsafe owned path')
        path=root/n;need(path.resolve().is_relative_to(root),'Owned escape')
    else:path=Path(row['path']);need(path.is_absolute(),'External binding not absolute')
    need(path.is_file() and not path.is_symlink(),'Missing or symlink input')
    b=path.read_bytes();need(len(b)==row['bytes'],'Byte size changed')
    need(sha(b)==row['SHA256'],'Byte hash changed: '+str(path))
    return path


def obj(kind,oid):
    p=O/'git-objects'/f'{kind}-{oid}.raw';need(p.is_file(),'Missing native Git object')
    b=p.read_bytes();need(hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid,'Native Git object mismatch')
    return b


def tree(oid):
    b=obj('tree',oid);out=[];i=0
    while i<len(b):
        j=b.index(b' ',i);k=b.index(b'\0',j);need(k+21<=len(b),'Truncated native tree')
        out.append((b[i:j].decode(),b[j+1:k].decode(),b[k+1:k+21].hex()));i=k+21
    need(i==len(b),'Native tree tail')
    return out


def main(preseal):
    m=load(O/'OWNED_MANIFEST.json');need(m['excluded_terminal_files']==sorted(EXCLUDED),'Owned exclusions')
    paths=set()
    for r in m['files']:
        p=bound(r,O);need(r['path'] not in paths,'Duplicate owned entry');paths.add(r['path'])
    need(paths=={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}-EXCLUDED,'Owned completeness')
    inputs=load(O/'INPUT_MANIFEST.json')['files'];seen=set()
    for r in inputs:
        bound(r);need(r['path'] not in seen,'Duplicate external binding');seen.add(r['path'])
    pin=load(O/'REMOTE_PIN.json');need(pin['remote_commit']==COMMIT and pin['remote_docs_tree']==TREE,'Opening release identity')
    need((O/'raw/remote-main-start.stdout').read_text().split()[0]==COMMIT,'Actual remote raw response')
    commit=obj('commit',COMMIT);root=commit.splitlines()[0].decode().split()[1]
    roots=tree(root);need(any(n=='docs' and oid==TREE and mode in ['40000','040000'] for mode,n,oid in roots),'Commit/root/docs binding')
    leaves={}
    def walk(oid,prefix):
        for mode,name,child in tree(oid):
            path=prefix+'/'+name
            if mode in ['40000','040000']:walk(child,path)
            else:leaves[path]=(mode,'blob',child)
    walk(TREE,'docs')
    rows=load(O/'CURRENT_BLOB_BINDINGS.json');need(len(rows)==254,'Complete released docs leaf count')
    need(leaves=={r['path']:(r['mode'],r['kind'],r['blob']) for r in rows},'Actual tree leaves and source-blob bindings')
    bypath={r['path']:r for r in rows}
    for r in rows:
        p=O/'corpus'/f"{r['blob']}.raw"
        if p.exists():
            b=p.read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'],'Native text blob hash')
            need(sha(b)==r['sha256'] and len(b)==r['bytes'],'Current raw text SHA/size')
    prior=O.parents[1]/'redirects/three-paper-preflight-sol-20261115'
    s=load(prior/'SEAL.json');need(sha((prior/'OWNED_MANIFEST.json').read_bytes())==s['OWNED_MANIFEST_SHA256'],'Prior seal/manifest')
    old={r['path']:r for r in load(prior/'OWNED_MANIFEST.json')['files']}
    for n in ['HISTORICAL_DOCS_BINDINGS.json','CURRENT_DOCS_DELTA.json','REMOTE_DOCS_TREE_GET.json','REUSED_EXTRACT_BINDINGS.json']:
        b=(prior/n).read_bytes();need(len(b)==old[n]['bytes'] and sha(b)==old[n]['SHA256'],'Selected prior sealed payload')
    api=json.loads(load(prior/'REMOTE_DOCS_TREE_GET.json')['structuredContent']['content'])
    need(api['sha']==TREE and api['truncated'] is False,'Exact reused complete current tree')
    need({'docs/'+r['path']:(r['mode'],r['type'],r['sha']) for r in api['tree'] if r['type']=='blob'}==leaves,'No current delta from reused corpus')
    reused=load(O/'REUSED_EXTRACT_BINDINGS.json');need(len(reused)==76 and sum(r['pages'] for r in reused)==854,'Bounded reused PDF corpus')
    for r in reused:
        q=bypath[r['public_path']];need(q['blob']==r['pdf_blob'] and q['sha256']==r['pdf_sha256'],'Reused PDF exact object identity')
        p=Path(r['path']);b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Reused complete extraction unchanged')
    c=load(O/'CORPUS_RECEIPT.json');need(c['new_PDF_extractions']==0 and c['total_identity_search_representations']==260,'No extraction campaign')
    hits=load(O/'SEARCH_RESULTS.json');need(hits['hit_representation_counts']['118_record_DOI_concept']==hits['hit_representation_counts']['118_exact_title']==hits['hit_representation_counts']['118_distinctive']==0,'118 bounded negative')
    need(hits['hit_representation_counts']['118_broad']==1 and hits['hits']['118_broad'][0]['public_path']=='docs/papers/hadamard-668-lp333/paper.pdf','118 false-hit boundary')
    assets=load(O/'CANDIDATE_ASSETS.json')
    for a in assets:
        p=Path(a['snapshot']);need(p.resolve().is_relative_to(O),'Candidate outside own root');b=p.read_bytes()
        need(sha(b)==a['SHA256'] and len(b)==a['bytes'],'Candidate SHA/size')
        need(obj('blob',a['blob'])==b and bypath[a['path']]['blob']==a['blob'],'Actual candidate released blob')
    ownpdf=(O/'candidate-evidence/paper.pdf').read_bytes();ownzip=(O/'candidate-evidence/source-and-verification.zip').read_bytes()
    native=load(O/'NATIVE_PDF_IDENTITIES.json');gap=next(r for r in native if r['record_id']=='22983513')
    need(Path(gap['native_published_PDF']).read_bytes()==ownpdf and gap['pages']==3,'Actual published PDF byte identity')
    need(any(r['page']==3 and r['URI']=='https://aleckriebel.github.io/Math/papers/strict-dirichlet-gap/' for r in gap['all_URI_annotations_in_page_order']),'Explicit native project URI')
    comparisons=load(O/'NATIVE_ASSET_COMPARISONS.json')
    for a in comparisons:
        if a['record_id']=='23385145':need(a['equal_SHA256_current_docs_paths']==[],'Unexpected118 asset match')
        elif a['native_asset_key']=='source-and-verification.zip':need(Path(a['native_path']).read_bytes()==ownzip,'Actual published ZIP byte identity')
    live=load(O/'raw/live-legacy-article.receipt.json');need(live['status']==200 and live['body_identical_to_released_HTML'] is True,'Live legacy article observation')
    need((O/'raw/live-legacy-article.body').read_bytes()==(O/'candidate-evidence/index.html').read_bytes(),'Live HTML exact bytes')
    before=load(O/'PRESERVATION_BEFORE.json');after=load(O/'PRESERVATION_AFTER.json')
    need(after['index_SHA256']==before['index_SHA256'] and after['HEAD_bytes']==before['HEAD_bytes'],'Shared index/HEAD preservation')
    need(after['local_HEAD_main']==before['local_refs_stdout'].splitlines()[:2],'Shared HEAD/main preservation')
    closing=load(O/'CLOSING_REMOTE_PIN.json');need(closing['docs_tree']==TREE,'Closing actual remote docs changed')
    v=load(O/'CUSTOM_VERDICT.json');need(v['redirects_written']==[] and v['replacement_live_verification_performed'] is False,'Preflight task boundary')
    need(v['records']['23385145']['disposition']=='BOUNDED_NEGATIVE_NO_GENUINE_CORRESPONDING_ARTICLE_LOCATED','118 disposition')
    need(v['records']['22983513']['legacy_URL']=='https://aleckriebel.github.io/Math/papers/strict-dirichlet-gap/' and v['records']['22983513']['redirect_authorized_now'] is False,'119 qualified positive')
    if not preseal:
        s=load(O/'FINAL_SEAL.json');need(s['OWNED_MANIFEST_SHA256']==sha((O/'OWNED_MANIFEST.json').read_bytes()),'Final manifest seal')
        need(s['REPORT_SHA256']==sha((O/'REPORT.md').read_bytes()) and s['CUSTOM_VERDICT_SHA256']==sha((O/'CUSTOM_VERDICT.json').read_bytes()),'Final dispositions seal')
    print(json.dumps({'verdict':'PASS','mode':'preseal' if preseal else 'sealed','checks':N,'owned_payloads':len(paths),'external_byte_bindings':len(inputs),'released_docs_blobs':254,'reused_PDF_extractions':76,'new_PDF_extractions':0,'network_requests':0,'writes':0,'source_or_scientific_code_executions':0},sort_keys=True))


if __name__=='__main__':
    need(sys.argv[1:] in [[],['--preseal']],'Usage: verify_readonly.py [--preseal]')
    main(sys.argv[1:]==['--preseal'])
