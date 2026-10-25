#!/usr/bin/env python3
"""Read-only evidence audit; --write-receipt writes only this bundle's receipt."""
from pathlib import Path
import argparse, datetime, hashlib, json, re, subprocess

E = Path(__file__).resolve().parent
P = E.parents[1]

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        while b := f.read(1048576): h.update(b)
    return h.hexdigest()

def read(name): return json.loads((E / name).read_text())
def bound(p, b): return p.is_file() and p.stat().st_size == b['bytes'] and sha(p) == b['sha256']
def norm(s): return ' '.join(s.split())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-receipt', action='store_true')
    args = ap.parse_args()
    problems = []
    baseline = read('preservation-before.json')
    for r in baseline['files']:
        if not bound(Path(r['path']), r): problems.append({'kind':'preservation','path':r['path']})
    shots = read('screenshot-manifest.json')['captures']
    if len(shots) != len({r['file'] for r in shots}): problems.append({'kind':'duplicate_capture_path'})
    for r in shots:
        p = E / r['file']
        if not bound(p, r): problems.append({'kind':'screenshot','path':r['file']})
        out = subprocess.check_output(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(p)],text=True)
        dims = [int(re.search(r'pixelWidth: (\d+)',out)[1]),int(re.search(r'pixelHeight: (\d+)',out)[1])]
        if dims != [r['width'],r['height']] or dims not in [[390,844],[2056,1146]]:
            problems.append({'kind':'image_dimensions','file':r['file']})
        if 'narrow' in r['label']:
            m = r['metrics']
            if [m['width'],m['height'],m['visualWidth']] != [390,844,390]:
                problems.append({'kind':'narrow_metrics','file':r['file']})
            if '-pdf-' not in r['label'] and m['scrollWidth'] != 390:
                problems.append({'kind':'article_horizontal_overflow','file':r['file']})
    downloads = read('actual-download-verification.json')['files']
    if len(downloads) != 6 or len({r['tab_id'] for r in downloads}) != 6:
        problems.append({'kind':'download_tab_count'})
    for r in downloads:
        b = {'bytes':r['bytes'],'sha256':r['expected_sha256']}
        for name in ['path','site_path','source_path']:
            if not bound(Path(r[name]),b): problems.append({'kind':'download_binding','path':r[name]})
    specs = read('expected-records.json')['records']
    events = read('browser-events.json')
    for s in specs:
        for size in ['desktop','narrow']:
            key = s['short']+'-'+size+'-actual-Research-return'
            rs = [r for r in events if r['step']==key]
            if len(rs)!=1 or rs[0]['url']!='https://aleckriebel.com/research/' or rs[0]['count']!=55:
                problems.append({'kind':'index_return','step':key})
            elif not all(any(e['title']==x['title'] and e['url']==x['url'] for e in rs[0]['entries']) for x in specs):
                problems.append({'kind':'new_index_links','step':key})
        follow = [r for r in events if r['step']==s['short']+'-index-link-follow']
        pdf = [r for r in events if r['step']==s['short']+'-actual-full-window-PDF-link']
        if len(follow)!=1 or follow[0]['url']!=s['url'] or len(pdf)!=1 or pdf[0]['url']!=s['url']+s['pdf']:
            problems.append({'kind':'actual_link_follow','record':s['record']})
        pubpath = P / 'papers' / s['record'] / 'publication.json'
        pub = json.loads(pubpath.read_text())
        dom = (E/(s['short']+'-recovered-article.dom.txt')).read_text()
        for key in ['abstract','plain_language','result','why_it_works','limitations','ai_disclosure','edition_note','collaboration']:
            vals = pub[key] if isinstance(pub[key],list) else [pub[key]]
            for i,v in enumerate(vals):
                if norm(v) not in norm(dom): problems.append({'kind':'complete_browser_prose','record':s['record'],'field':key,'paragraph':i+1})
    cleanup = read('browser-cleanup.json')
    if cleanup['remaining_own'] or not cleanup['all_original_ids_urls_preserved'] or not cleanup['all_created_ids_absent_from_final_inventory']:
        problems.append({'kind':'cleanup'})
    if (E/'evidence-manifest.json').is_file():
        for r in read('evidence-manifest.json')['files']:
            if not bound(E/r['file'],r): problems.append({'kind':'manifest','file':r['file']})
        if sha(E/'evidence-manifest.json') != read('SEAL.json')['evidence_manifest_sha256']:
            problems.append({'kind':'seal'})
    result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_custody_and_record_checks_pass':not problems,
        'preservation_paths':len(baseline['files']),'public_site_files':baseline['public_site_files'],'screenshots':len(shots),
        'unique_capture_paths':len({r['file'] for r in shots}),'actual_browser_downloads':len(downloads),'distinct_download_tabs':len({r['tab_id'] for r in downloads}),
        'actual_Research_returns':6,'index_entries':55,'owned_tabs_closed':cleanup['created_count'],'original_tabs_preserved':cleanup['protected_tab_count'],
        'visual_adjudication':'Separate raw frames support desktop/narrow article/PDF results; this script checks custody, dimensions and records, not pixel semantics or mathematical proof.',
        'native_sheet_or_overall_programme_PASS_claimed':False,'problems':problems}
    if args.write_receipt: (E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return bool(problems)

if __name__=='__main__': raise SystemExit(main())
