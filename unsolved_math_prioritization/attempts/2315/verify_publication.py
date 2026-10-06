#!/usr/bin/env python3
"""Fail-closed static publication-integrity verifier. Not mathematical validation."""
import json
PINS=json.loads('{\n  "packs": [\n    {\n      "tag": "AUTHOR",\n      "folder": "author_original",\n      "archive": {\n        "path": "RAINBOW_QUADRILATERAL_2315_AUTHOR_SAFE_FREEZE.zip",\n        "bytes": 15279,\n        "sha256": "2cc0a33b99299d2581cdd4bec4c13e804c5d5537953ab2344bcbdbd8ed1d9a5c"\n      },\n      "manifest": {\n        "path": "RAINBOW_QUADRILATERAL_2315_AUTHOR_EXTERNAL_MANIFEST.json",\n        "bytes": 2199,\n        "sha256": "958facb1869ac5d64c91c1099ca1cc874d4968f09408c1f8117db543808e2124"\n      },\n      "members": [\n        {\n          "path": "PROOFS.md",\n          "bytes": 12868,\n          "sha256": "129ffa669d8e12aa759f6b8ade41093dc97160f90f468a2f8a518e961393ea96"\n        },\n        {\n          "path": "README.md",\n          "bytes": 1205,\n          "sha256": "48316e4eba1d0e7c5f0fbb654a56cbb6b1c93f22cc1985ba2038e09db40d5026"\n        },\n        {\n          "path": "REPORT.md",\n          "bytes": 5526,\n          "sha256": "a94b24013b683981b2735176ff9a62293d0be412bc0fd9752cd559256fdb8345"\n        },\n        {\n          "path": "RESEARCH_LOG.md",\n          "bytes": 2725,\n          "sha256": "4f3c32a2c09dde3823acdbb9095a0fc04171ae4c779cd7037f54a15b772afa72"\n        },\n        {\n          "path": "SOURCE_PROVENANCE.json",\n          "bytes": 5819,\n          "sha256": "532025f51265ec5b6f885fcc19b743abaae17791e8825dfdbf2148aa580c9f1a"\n        },\n        {\n          "path": "STATUS.md",\n          "bytes": 1828,\n          "sha256": "56f5bdb1f4db36b37d1539c66a3933e39a22a5295c51b047dbdcdcbb70f6829f"\n        },\n        {\n          "path": "VERIFICATION_METADATA.json",\n          "bytes": 3302,\n          "sha256": "7e370dbcfdf69c0a96caf19880f648c7fb71e6114e50bb4db176f7a76bffa951"\n        }\n      ]\n    },\n    {\n      "tag": "INDEPENDENT_AUDIT",\n      "folder": "independent_audit",\n      "archive": {\n        "path": "RAINBOW_QUADRILATERAL_2315_INDEPENDENT_AUDIT_SAFE.zip",\n        "bytes": 32984,\n        "sha256": "c337d4d8b45003545087ea5bc440abf9600aea5ca4d031d8ae32012ecf1429bc"\n      },\n      "manifest": {\n        "path": "RAINBOW_QUADRILATERAL_2315_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json",\n        "bytes": 2956,\n        "sha256": "dbe267d99f1bd4702dc8cd40745e6af4692ae5fd9a8517397b005608a925aced"\n      },\n      "members": [\n        {\n          "path": "AUDIT_VERIFICATION_METADATA.json",\n          "bytes": 8183,\n          "sha256": "429fdf6945b6f4a4bcc561b83fb610a93be218e5728c4b9c0db990f802b3a3e5"\n        },\n        {\n          "path": "EXACT_ACCEPTANCE.json",\n          "bytes": 2017,\n          "sha256": "a7a85f30b385ebd40b4f8b9bc32d772335ff3d1ef0bd781060d1473f60195300"\n        },\n        {\n          "path": "EXACT_ACCEPTANCE.md",\n          "bytes": 3653,\n          "sha256": "97407c8ecde6e00dfa925194fca9786ad9dd47e26d5b39a2daf956189e41df21"\n        },\n        {\n          "path": "INDEPENDENT_AUDIT.md",\n          "bytes": 21553,\n          "sha256": "4f9e8263203d7471e3737765d56827fd7dca1d892feadbbb373e2140bce4a5f1"\n        },\n        {\n          "path": "README.md",\n          "bytes": 1053,\n          "sha256": "7931edc02835da5abba10ebc487643a731722831d2fa8a400faead6219bc4052"\n        },\n        {\n          "path": "author_original/AUTHOR_EXTERNAL_MANIFEST.json",\n          "bytes": 2199,\n          "sha256": "958facb1869ac5d64c91c1099ca1cc874d4968f09408c1f8117db543808e2124"\n        },\n        {\n          "path": "author_original/PROOFS.md",\n          "bytes": 12868,\n          "sha256": "129ffa669d8e12aa759f6b8ade41093dc97160f90f468a2f8a518e961393ea96"\n        },\n        {\n          "path": "author_original/README.md",\n          "bytes": 1205,\n          "sha256": "48316e4eba1d0e7c5f0fbb654a56cbb6b1c93f22cc1985ba2038e09db40d5026"\n        },\n        {\n          "path": "author_original/REPORT.md",\n          "bytes": 5526,\n          "sha256": "a94b24013b683981b2735176ff9a62293d0be412bc0fd9752cd559256fdb8345"\n        },\n        {\n          "path": "author_original/RESEARCH_LOG.md",\n          "bytes": 2725,\n          "sha256": "4f3c32a2c09dde3823acdbb9095a0fc04171ae4c779cd7037f54a15b772afa72"\n        },\n        {\n          "path": "author_original/SOURCE_PROVENANCE.json",\n          "bytes": 5819,\n          "sha256": "532025f51265ec5b6f885fcc19b743abaae17791e8825dfdbf2148aa580c9f1a"\n        },\n        {\n          "path": "author_original/STATUS.md",\n          "bytes": 1828,\n          "sha256": "56f5bdb1f4db36b37d1539c66a3933e39a22a5295c51b047dbdcdcbb70f6829f"\n        },\n        {\n          "path": "author_original/VERIFICATION_METADATA.json",\n          "bytes": 3302,\n          "sha256": "7e370dbcfdf69c0a96caf19880f648c7fb71e6114e50bb4db176f7a76bffa951"\n        }\n      ]\n    },\n    {\n      "tag": "EXACT_ACCEPTANCE",\n      "folder": "exact_acceptance",\n      "archive": {\n        "path": "RAINBOW_QUADRILATERAL_2315_EXACT_ACCEPTANCE_SAFE.zip",\n        "bytes": 6417,\n        "sha256": "d1ed5c6620bac395cd012c1dedeed43c7af006ec5d1199d00c73e5452057d023"\n      },\n      "manifest": {\n        "path": "RAINBOW_QUADRILATERAL_2315_EXACT_ACCEPTANCE_EXTERNAL_MANIFEST.json",\n        "bytes": 1316,\n        "sha256": "f3da866162c1090e0f5c916b72761d792fc7ba9b926a7d6c4ce6544821a608f7"\n      },\n      "members": [\n        {\n          "path": "AUDIT_VERIFICATION_METADATA.json",\n          "bytes": 8183,\n          "sha256": "429fdf6945b6f4a4bcc561b83fb610a93be218e5728c4b9c0db990f802b3a3e5"\n        },\n        {\n          "path": "EXACT_ACCEPTANCE.json",\n          "bytes": 2017,\n          "sha256": "a7a85f30b385ebd40b4f8b9bc32d772335ff3d1ef0bd781060d1473f60195300"\n        },\n        {\n          "path": "EXACT_ACCEPTANCE.md",\n          "bytes": 3653,\n          "sha256": "97407c8ecde6e00dfa925194fca9786ad9dd47e26d5b39a2daf956189e41df21"\n        }\n      ]\n    }\n  ],\n  "receipt": {\n    "bytes": 1740,\n    "sha256": "6cc8cdc08ff25ec25aef5d45ddd2919cc5a9052ca579dc4d54d6f96a413f1bbc"\n  },\n  "queue_base": {\n    "bytes": 392513,\n    "sha256": "be0b59c8866f1a7e55cb6be1924fff339c1fb9ce7a58122b55c9a077da6b7e52"\n  },\n  "queue_new": {\n    "bytes": 392515,\n    "sha256": "96a18c246c494b64d8f062193280131246ac64662c9e34de8e51d14cef693743"\n  }\n}\n')
import argparse, hashlib, io, json, stat, sys, zipfile
from pathlib import Path, PurePosixPath
H=lambda b:hashlib.sha256(b).hexdigest()
def need(v,why):
    if not v:raise ValueError(why)
def pin(b,p,label):need((len(b),H(b))==(p['bytes'],p['sha256']),label+' byte/hash mismatch')
def safe(n):
    p=PurePosixPath(n)
    need(n and not p.is_absolute() and all(x not in ('','.','..') for x in n.split('/')) and '\\' not in n and ':' not in n,'unsafe path')
    return p
def inspect(ab,mb,p):
    pin(ab,p['archive'],'archive');pin(mb,p['manifest'],'external manifest');m=json.loads(mb)
    need(m['archive']==p['archive'] and m['problem_id']==2315 and m['problem_number']=='EP-810' and m['selection_rank']==903,'manifest identity')
    need(m['members']==p['members'],'immutable member pins');names=[e['path'] for e in p['members']]
    need(len(names)==len(set(names))==m['member_count'],'member uniqueness');out={}
    with zipfile.ZipFile(io.BytesIO(ab)) as z:
        need(len(z.infolist())==len(names) and set(z.namelist())==set(names),'archive inventory');need(z.testzip() is None,'CRC')
        for e in p['members']:
            n=e['path'];path=safe(n);need(path.suffix in ('.md','.json'),'frozen format');i=z.getinfo(n);mode=i.external_attr>>16
            need(stat.S_IFMT(mode) in (0,stat.S_IFREG) and not mode&0o111 and not i.flag_bits&1,'unsafe member mode');b=z.read(n);pin(b,e,n);b.decode('utf-8')
            if path.suffix=='.json':json.loads(b)
            out[n]=b
    return out

def inputs(a,meta):
    out=dict(corpus_checks=dict(performed=False),source_checks=dict(performed=False),queue_checks=dict(performed=False))
    if any((a.catalog,a.problems,a.reports)):
        need(all((a.catalog,a.problems,a.reports)),'all three complete corpora required');objs=[]
        for f,e in zip((a.catalog,a.problems,a.reports),meta['inputs']):
            b=Path(f).read_bytes();pin(b,e,'complete input '+e['label']);o=json.loads(b);need(type(o).__name__==e['top_level_type'] and len(o)==e['top_level_count'],'full input structure');objs.append(o)
        c,rs,reports=objs;cs=[x for x in c if str(x.get('id'))=='2315'];rr=[x for x in rs if str(x.get('id'))=='2315'];need(len(cs)==len(rr)==1,'unique target');c=cs[0];r=rr[0]
        need(c['rank']==903 and r['problem_number']=='EP-810' and c['problem_number']=='EP-810','exact target');report=reports.get('EP-810',{});need(report=={},'empty report');sb=r['statement'].encode();pair=json.dumps([r,report],sort_keys=True).encode()
        need(H(sb)==meta['statement_sha256']==c['statement_hash'],'statement identity');pin(pair,meta['complete_record_report_pair'],'complete record/report pair');need(H(pair)==c['review_hash'],'catalog pair identity')
        out['corpus_checks']=dict(performed=True,complete_files=3,counts=[len(x) for x in objs],exact_target=2315,rank=903,unique_target=True,complete_pair_bytes=len(pair),complete_pair_sha256=H(pair),statement_sha256=H(sb),inherited_report_empty=True,contents_emitted=False)
    if a.sources_directory:
        found={H(f.read_bytes()):f.stat().st_size for f in Path(a.sources_directory).glob('*.pdf') if f.is_file()};need(len(meta['source_files'])==6,'six PDF metadata entries')
        for e in meta['source_files']:need(found.get(e['sha256'])==e['bytes'],'source PDF pin')
        out['source_checks']=dict(performed=True,pdf_count=6,all_pins_match=True,source_contents_emitted=False,fresh_retrieval=False,theorem_inspection_repeated=False)
    if a.queue_base or a.queue_current:
        need(a.queue_base and a.queue_current,'both queue inputs required');b=Path(a.queue_base).read_bytes();n=Path(a.queue_current).read_bytes();pin(b,PINS['queue_base'],'base queue');pin(n,PINS['queue_new'],'new queue');bl=b.splitlines(keepends=True);nl=n.splitlines(keepends=True)
        need(len(bl)==len(nl),'queue lines');idx=[i for i,(x,y) in enumerate(zip(bl,nl)) if x!=y];need(len(idx)==1,'single changed queue row');i=idx[0]
        need(bl[i].startswith(b'| 903 | 2315 / EP-810 |') and nl[i].startswith(b'| 903 | 2315 / EP-810 |'),'queue row identity');bc=bl[i].split(b'|');nc=nl[i].split(b'|');need(len(bc)==len(nc) and [i for i,(x,y) in enumerate(zip(bc,nc)) if x!=y]==[8,9],'only Status/Turns');need(nc[8]==b' unsolved ' and nc[9]==b' 5/5 ','canonical queue status')
        out['queue_checks']=dict(performed=True,changed_rows=1,changed_cells=['Status','Turns'],findings_preserved=True,all_unrelated_bytes_preserved=True)
    return out

def verify(root,a):
    root=Path(root);need(root.is_dir() and not root.is_symlink(),'package root');packs={};count=0
    for p in PINS['packs']:
        packs[p['tag']]=inspect((root/'archives'/p['archive']['path']).read_bytes(),(root/'archives'/p['manifest']['path']).read_bytes(),p);pack=packs[p['tag']]
        for n,b in pack.items():
            f=root/p['folder']/n;need(f.is_file() and not f.is_symlink() and f.read_bytes()==b,'loose member equality')
        actual={f.relative_to(root/p['folder']).as_posix() for f in (root/p['folder']).rglob('*') if f.is_file()};need(actual==set(pack),'loose inventory');count+=len(pack)
    orig=packs['AUTHOR'];audit=packs['INDEPENDENT_AUDIT'];accpack=packs['EXACT_ACCEPTANCE']
    need(all(audit['author_original/'+n]==b for n,b in orig.items()),'nested original identity')
    need(audit['author_original/AUTHOR_EXTERNAL_MANIFEST.json']==(root/'archives'/PINS['packs'][0]['manifest']['path']).read_bytes(),'nested original manifest');need(all(audit[n]==b for n,b in accpack.items()),'separate acceptance identity')
    acc=json.loads(accpack['EXACT_ACCEPTANCE.json']);meta=json.loads(audit['AUDIT_VERIFICATION_METADATA.json']);rb=(root/'INDEPENDENT_AUDIT_RECEIPT.json').read_bytes();pin(rb,PINS['receipt'],'independent receipt');receipt=json.loads(rb)
    for x in (acc,meta,receipt):need(x['problem_id']==2315 and x['problem_number']=='EP-810' and x['selection_rank']==903,'bound target')
    for x in (acc,receipt):need(x['disposition']=='UNSOLVED_SCOPED_PARTIALS_ACCEPTED' and x['approaches_used']==x['approach_limit']==5 and not x['full_solution'] and x['mandatory_corrections']==[] and not x['correction_derivative_created'],'accepted scope')
    pin((root/'archives'/PINS['packs'][0]['archive']['path']).read_bytes(),acc['accepted_author_archive'],'accepted author');pin((root/'archives'/PINS['packs'][0]['manifest']['path']).read_bytes(),acc['accepted_author_external_manifest'],'accepted original manifest');pin(orig['PROOFS.md'],acc['accepted_proofs_member'],'accepted proofs')
    need(acc['author_bytes_unchanged'] and not any(acc[k] for k in ('global_current_status_certified','novelty_certified','human_peer_review','formal_verification')),'acceptance boundaries');need(len(acc['accepted_claims'])==6 and 'at most s' in acc['palette_source_caveat'],'palette caveat')
    for key,p in [('full_audit',PINS['packs'][1]),('exact_acceptance',PINS['packs'][2])]:
        need(receipt[key]['archive']==p['archive'] and receipt[key]['external_manifest']==p['manifest'] and receipt[key]['member_count']==len(p['members']),'receipt archive binding')
    need(receipt['original_preserved'] and not receipt['novelty_claim'],'receipt scope');need(meta['executables_in_author_payload']==meta['executables_in_audit_payload']==0,'no math executable')
    provenance=json.loads(orig['SOURCE_PROVENANCE.json']);need([(e['bytes'],e['sha256']) for e in provenance['sources']]==[(e['bytes'],e['sha256']) for e in meta['source_files']],'source provenance pins')
    pub=json.loads((root/'PUBLICATION_METADATA.json').read_bytes());need(pub['problem_id']==2315 and pub['queue_status']=='unsolved' and pub['turns']=='5/5' and pub['approaches_used']==pub['approach_limit']==5 and pub['available_palette_at_most_s'] and not any(pub[k] for k in ('full_solution','novelty_claimed','global_current_status_certified','palette_minimum_equality_certified','mathematical_executable_present','correction_derivative_created')),'publication scope')
    mf=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes());names=[e['path'] for e in mf['files']];need(len(names)==len(set(names)) and mf['problem_id']==2315,'publication manifest');actual={f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()};need(actual==set(names)|{'PUBLICATION_MANIFEST.json'},'full publication inventory')
    for f in root.rglob('*'):need(not f.is_symlink(),'publication symlink')
    for e in mf['files']:
        n=e['path'];safe(n);f=root/n;need(f.resolve().is_relative_to(root.resolve()),'publication path');pin(f.read_bytes(),e,'publication '+n)
    result=dict(status='PASS',optimization_level=sys.flags.optimize,archives=3,archive_member_occurrences=count,loose_members=count,nested_author_members=7,separate_acceptance_members=3,exact_acceptance_bindings=True,receipt_bindings=True,full_publication_inventory=True,mathematical_validation=False,scope='Static bytes, archive safety, identity and scope checks only; no mathematical execution or proof certification.')
    result.update(inputs(a,meta));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    for n in ('catalog','problems','reports','sources-directory','queue-base','queue-current'):p.add_argument('--'+n)
    a=p.parse_args();print(json.dumps(verify(a.root,a),indent=2,sort_keys=True))
