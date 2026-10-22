#!/usr/bin/env python3
"""Rehash complete supplied inputs and pinned PDFs; emits metadata only."""
import argparse,hashlib,json,subprocess,tempfile,unicodedata
from pathlib import Path

def require(ok,message):
    if not ok: raise ValueError(message)
def h(b): return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--catalog',required=True,type=Path); ap.add_argument('--problems',required=True,type=Path); ap.add_argument('--reports',required=True,type=Path); ap.add_argument('--pdf-dir',required=True,type=Path); a=ap.parse_args()
    expected=json.loads((Path(__file__).parent/'INPUT_SOURCE_CHECKS.json').read_text())
    loaded=[]; checks=[]
    for p,e in zip([a.catalog,a.problems,a.reports],expected['input_files']):
        require(p.is_file() and not p.is_symlink(),'Invalid input')
        b=p.read_bytes(); require(len(b)==e['bytes'] and h(b)==e['sha256'],'Complete input identity mismatch: '+e['logical_name']); loaded.append(json.loads(b)); checks.append({'logical_name':e['logical_name'],'match':True})
    c=[x for x in loaded[0] if str(x['id'])=='2894']; r=[x for x in loaded[1] if str(x['id'])=='2894']; require(len(c)==len(r)==1,'Nonunique exact ID')
    require(c[0]['rank']==917,'Wrong rank'); report=loaded[2].get(r[0]['problem_number'],{})
    require(r[0]['problem_number']=='KP-4.18' and report=={},'Identity/report mismatch')
    require(h(r[0]['statement'].encode())==expected['statement_sha256'],'Statement mismatch')
    require(h(json.dumps([r[0],report],sort_keys=True).encode())==expected['complete_record_report_pair_sha256'],'Default sorted JSON pair mismatch')
    names={'K3':'k3.pdf','HU':'hu_v1.pdf','KNV':'knv_v2.pdf','KP':'kp_v2.pdf','NNP':'nnp_v4.pdf'}
    for e in expected['source_bytes']:
        p=a.pdf_dir/names[e['key']]; require(p.is_file() and not p.is_symlink(),'Invalid PDF'); b=p.read_bytes(); require(len(b)==e['bytes'] and h(b)==e['sha256'],'PDF identity mismatch: '+e['key'])
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'statement.txt'; subprocess.run(['pdftotext','-f','204','-l','204','-layout',str(a.pdf_dir/'k3.pdf'),str(out)],check=True,capture_output=True)
        text=out.read_text(); start=text.index('Problem 4.18.')+len('Problem 4.18.'); end=text.index('Remarks.',start)
        norm=lambda s: ''.join(c for c in unicodedata.normalize('NFKC',s).lower() if c.isalnum())
        require(norm(text[start:end])==norm(r[0]['statement']),'Primary PDF statement mismatch')
        require(h(norm(text[start:end]).encode())==expected['primary_normalized_sha256'],'Normalized statement pin mismatch')
    print(json.dumps({'result':'pass','complete_corpus_inputs':3,'exact_record_report_pair_verified':True,'pdfs':5,'primary_pdf_statement_verified':True,'raw_content_emitted':False,'mathematical_theorems_certified':False},sort_keys=True))
if __name__=='__main__': main()
