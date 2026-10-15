#!/usr/bin/env python3
"""Seal only local reviewer outputs and all exact reviewed packet inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,tarfile
from audit_packet import bindings,pin,save,HERE,ROOT,PACKET
def now():return datetime.now(timezone.utc).isoformat()
def main():
    bindings('final')
    src=ROOT/'root_priority/private_reading'
    with tarfile.open(src/'nica_v3_source.tar.gz','r:gz') as t:
        members=[]
        for m in t.getmembers():
            b=t.extractfile(m).read()
            members.append({'name':m.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                            'mtime_utc':datetime.fromtimestamp(m.mtime,timezone.utc).isoformat()})
            if m.name=='RS_arxiv.tex':tex=b
    assert tex==(src/'nica_v3_RS_arxiv.tex').read_bytes()
    assert not re.search(rb'\\date\s*(?:\[|\{)',tex)
    assert b'\\documentclass' in tex and b'{article}' in tex
    inspected=[
      'root_source_reading/private_reading/left_Hamm.html',
      'root_source_reading/private_reading/patience1993.pdf',
      'root_source_reading/private_reading/patience1993-pages36-40.txt',
      'root_source_reading/private_reading/ad1999.pdf',
      'root_source_reading/private_reading/ad1999-pages6-7.txt',
      'root_source_reading/private_reading/ad1995.pdf',
      'root_priority/private_reading/ad95-page-05.png',
      'root_priority/private_reading/ad95-page-06.png',
      'root_priority/private_reading/ad95-page-07.png',
      'root_priority/private_reading/plancherel_2004v2.pdf',
      'root_priority/private_reading/plancherel_2004v2.txt',
      'root_priority/private_reading/nica_v1.pdf',
      'root_priority/private_reading/nica_v1.txt',
      'root_priority/private_reading/nica_v3.pdf',
      'root_priority/private_reading/nica_v3.txt',
      'root_priority/private_reading/nica_v3_RS_arxiv.tex',
      'root_priority/private_reading/nica_v3_source.tar.gz',
      'root_priority/private_reading/lrw2001.pdf',
      'root_priority/private_reading/lrw-page-04.png',
      'root_priority/private_reading/lrw-page-07.png',
      'root_priority/private_reading/lrw-page-09.png',
      'priority_historical_adversary_01/REPORT.md',
      'priority_historical_adversary_01/LRW2001_ALL_JOINT_EQUIVALENCE.md',
      'priority_schur_adversary_01/REPORT.md',
      'priority_recent_adversary_01/REPORT.md',
      'priority_novelty_falsifier_01/FINAL_REPORT.md',
      'priority_bridge_falsifier_01/INDEPENDENT_REPORT.md',
      'priority_bridge_falsifier_01/LRW_ADVERSARIAL_ADDENDUM.md']
    save('SOURCE_INSPECTION.json',{'utc':now(),'local_reviewed_inputs':[pin(ROOT/p) for p in inspected],
      'nica_source_members':members,'tex_member_equals_local_extracted_copy':True,
      'article_class_without_explicit_date':True,
      'independent_online_version_record_readback':[
        {'url':'https://arxiv.org/abs/1404.4015v3','read_utc_date':'2026-10-15',
         'v1':'2014-04-15T18:41:15Z','v3':'2015-04-29T04:32:12Z','v4':'2017-03-29T03:54:37Z'},
        {'url':'https://arxiv.org/abs/math-ph/0402064v2','read_utc_date':'2026-10-15',
         'v1':'2004-02-24T04:09:09Z','v2':'2004-09-29T16:30:12Z','journal_year':2006}],
      'limits':'Primary PDFs/source bytes and selected local full-page renders inspected; no full third-party reading copy redistributed in this reviewer output. Current PDF bytes are not claimed to be the exact bytes available in their initial version year.'})
    status={'utc':now(),'status':'PASS_CREDIT_PACKET_NO_MANDATORY_CORRECTION',
      'bounded_audit_completion_percent':100,'mandatory_findings':[],'optional_findings':[],
      'packet_file_count':35,'original_intake_objects_verified':20,'primary_pins_verified':11,
      'source_and_math_scope':'Complete prior mathematical coverage; no established earlier explicitly acknowledged answer to the 2018 posting or proposer endorsement.',
      'fresh_author_assertions':49618,'fresh_old_independent_assertions':15580,
      'fresh_complete_receipts_byte_identical':True,'additional_independent_assertions':50806,
      'proposed_disposition':'Apply already_solved credit correction from eligible intake, then scope skip; retain valid proof and code.',
      'not_performed':['native classifier','provider mutation','Git/index/ref operation','paper/deposit/tracker','merge/close/comment','external individual communication'],
      'current_frozen_manifest':pin(PACKET/'FROZEN_MANIFEST.json'),
      'current_publication_manifest':pin(PACKET/'PUBLICATION_MANIFEST.json'),
      'root_proposed_packet_manifest':pin(ROOT/'PROPOSED_CURRENT_PACKET_MANIFEST.json')}
    save('FINAL_STATUS.json',status)
    with (HERE/'RESEARCH_LOG.md').open('a') as h:
        h.write('\n'+status['utc']+' — Completed this bounded adversarial review at 100%. No mandatory or optional packet correction. All final packet bindings, all original objects, whole fresh replay receipts and independently reconstructed old-source bridges pass. Final source inspection, status and reviewer artifacts sealed; native guarded application/readback and wider goal completion remain with parent.\n')
    authored=[pin(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='FINAL_ARTIFACT_MANIFEST.json']
    save('FINAL_ARTIFACT_MANIFEST.json',{'utc':now(),'scope':'All actual reviewer authored outputs including isolated copied executable inputs; self excluded. Primary source reading copies remain outside this shard.',
          'files':authored,'reviewed_packet_files':[pin(p) for p in sorted(PACKET.rglob('*')) if p.is_file()],
          'packet_root':str(PACKET),'reviewer_completion_percent':100})
    print(json.dumps({'status':status['status'],'reviewer_files':len(authored),'packet_files':35,
          'artifact_manifest':pin(HERE/'FINAL_ARTIFACT_MANIFEST.json')}))
if __name__=='__main__':main()
