#!/usr/bin/env python3
"""Read-only custody/record audit. --write-receipt writes only this bundle."""
from pathlib import Path
import argparse, datetime, hashlib, json, re, subprocess

E = Path(__file__).resolve().parent
P = E.parents[1]

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        while b := f.read(1048576): h.update(b)
    return h.hexdigest()

def read(n): return json.loads((E / n).read_text())
def bound(p, r): return p.is_file() and p.stat().st_size == r['bytes'] and sha(p) == r['sha256']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-receipt', action='store_true')
    args = ap.parse_args()
    problems = []
    before = read('preservation-before.json')
    for r in before['files']:
        if not bound(Path(r['path']), r): problems.append({'kind':'original_binding', 'path':r['path']})
    shots = read('screenshot-manifest.json')['captures']
    adjudication = {r['file']:r for r in read('visual-adjudication.json')['frames']}
    if len(shots) != len({r['file'] for r in shots}): problems.append({'kind':'duplicate_capture_path'})
    for r in shots:
        p = E / r['file']
        if not bound(p,r): problems.append({'kind':'screenshot_binding','file':r['file']})
        t = subprocess.check_output(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(p)],text=True)
        dims = [int(re.search(r'pixelWidth: (\d+)',t)[1]), int(re.search(r'pixelHeight: (\d+)',t)[1])]
        if dims != [r['width'],r['height']]: problems.append({'kind':'physical_dimension_binding','file':r['file']})
        if adjudication[r['file']]['use'] == 'positive_observed_component' and 'narrow' in r['label']:
            m = r['metrics']
            if dims != [390,844] or [m['width'],m['height'],m['visualWidth']] != [390,844,390]:
                problems.append({'kind':'positive_narrow_dimension','file':r['file']})
            if '-pdf-' not in r['label'] and m['scrollWidth'] != 390:
                problems.append({'kind':'positive_article_overflow','file':r['file']})
    downloads = read('actual-download-verification.json')['files']
    if len(downloads) != 6 or len({r['tab_id'] for r in downloads}) != 6:
        problems.append({'kind':'download_count_or_distinct_tabs'})
    for r in downloads:
        b = {'bytes':r['bytes'],'sha256':r['expected_sha256']}
        for key in ['path','source_path','site_path']:
            if not bound(Path(r[key]),b): problems.append({'kind':'saved_source_site_binding','path':r[key]})
    specs = read('expected-records.json')['records']
    observed = read('dom/browser-full-body-sections.json')
    section_checks = 0
    for s in specs:
        stage = json.loads((P/'verification/local-cubic-fps-hessian-stage-sol-20261025'/('public-sections-'+s['record']+'.json')).read_text())
        if stage['sections'] != s['accepted_sections']: problems.append({'kind':'accepted_section_binding','record':s['record']})
        copies = [x for x in observed if x['record'] == s['record']]
        if len(copies) != 2: problems.append({'kind':'fresh_article_observation_count','record':s['record']})
        for c in copies:
            byid = {x['id']:x for x in c['data']['sections']}
            if c['data']['url'] != s['url']: problems.append({'kind':'body_url','record':s['record']})
            for t in s['accepted_sections']:
                section_checks += 1
                if byid.get(t['id']) != t: problems.append({'kind':'exact_actual_section','record':s['record'],'section':t['id']})
    events = read('browser-events.json')
    for s in specs:
        for size in ['desktop','narrow-managed390']:
            key=s['short']+'-'+size+'-index-link-follow'
            found=[r for r in events if r['step']==key]
            if len(found)!=1: problems.append({'kind':'title_follow_count','step':key}); continue
            r=found[0]
            url=r.get('url',r.get('after',{}).get('url'))
            if url!=s['url']: problems.append({'kind':'title_follow_url','step':key})
            if size!='desktop' and [r['after']['width'],r['after']['height']]!=[390,844]: problems.append({'kind':'narrow_follow_metrics','step':key})
            key=s['short']+'-'+size+'-actual-Research-return'
            found=[r for r in events if r['step']==key]
            if len(found)!=1: problems.append({'kind':'return_count','step':key}); continue
            r=found[0]
            if r.get('url',r.get('after',{}).get('url'))!='https://aleckriebel.com/research/' or r['count']!=60:
                problems.append({'kind':'return_url_or_entries','step':key})
            if not all(any(a['title']==t['title'] and a['url']==t['url'] for a in r['entries']) for t in specs):
                problems.append({'kind':'three_exact_index_links','step':key})
            if size!='desktop' and [r['after']['width'],r['after']['height']]!=[390,844]: problems.append({'kind':'narrow_return_metrics','step':key})
        pdf=[r for r in events if r['step']==s['short']+'-actual-full-window-PDF-link']
        if len(pdf)!=1 or pdf[0]['url']!=s['url']+s['pdf']: problems.append({'kind':'actual_pdf_link_arrival','record':s['record']})
    cleanup=read('browser-cleanup.json')
    if cleanup['remaining_own'] or not cleanup['all_original_ids_urls_preserved'] or not cleanup['all_created_ids_absent_from_final_inventory']:
        problems.append({'kind':'cleanup'})
    if [cleanup['final_desktop']['width'],cleanup['final_desktop']['height']] != [2056,1146]: problems.append({'kind':'desktop_restoration'})
    if (E/'evidence-manifest.json').is_file():
        for r in read('evidence-manifest.json')['files']:
            if not bound(E/r['file'],r): problems.append({'kind':'manifest','file':r['file']})
        if sha(E/'evidence-manifest.json')!=read('SEAL.json')['evidence_manifest_sha256']: problems.append({'kind':'seal'})
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_custody_and_record_checks_pass':not problems,
        'original_bindings':len(before['files']),'current_public_site_files':before['public_site_files'],
        'raw_captures':len(shots),'unique_capture_paths':len({r['file'] for r in shots}),
        'excluded_raw_captures':sum(r['use']=='excluded_from_positive_gate' for r in adjudication.values()),
        'actual_downloads':len(downloads),'distinct_download_tabs':len({r['tab_id'] for r in downloads}),
        'exact_fresh_article_section_checks':section_checks,'required_actual_Research_returns':6,'index_entries':60,
        'owned_tabs_closed':cleanup['created_count'],'original_tabs_preserved':cleanup['protected_tab_count'],
        'scope':'Custody, actual records and dimensions only; separate raw-frame visual adjudication establishes presentation. No mathematical proof, physical phone, native Sheet or whole-programme completion claim.',
        'problems':problems}
    if args.write_receipt: (E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return bool(problems)

if __name__=='__main__': raise SystemExit(main())
