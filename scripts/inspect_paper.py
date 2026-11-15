#!/usr/bin/env python3
"""Extract candidate figure captions and figure references from a research PDF.

Requires PyMuPDF. This is a discovery aid, not a substitute for visual review.
"""
import argparse
import csv
import re
from pathlib import Path
import fitz

CAPTION = re.compile(r'(?im)^\s*(?:Fig(?:ure)?\.?|图)\s*(\d+[a-z]?)\s*[.:：]\s*(.+)')
REFERENCE = re.compile(r'(?i)\b(?:fig(?:ure)?\.?)\s*(\d+[a-z]?)\b')

def inspect(path):
    document = fitz.open(path)
    result = []
    for index, page in enumerate(document):
        text = page.get_text('text', sort=True)
        found = CAPTION.findall(text)
        refs = sorted(set(REFERENCE.findall(text)), key=lambda x:(int(re.match(r'\d+',x).group()), x))
        result.append({'page': index + 1, 'captions': ' | '.join(f'{n}: {s.strip()}' for n,s in found),
                       'figure_references': ', '.join(refs), 'image_objects': len(page.get_images(full=True))})
    document.close()
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path)
    parser.add_argument('--output',type=Path,help='CSV output path')
    parser.add_argument('--around',type=int,help='Print candidate pages mentioning this figure number and adjacent pages')
    args=parser.parse_args()
    rows=inspect(args.pdf)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    if args.around is not None:
        hits={r['page'] for r in rows if re.search(r'(?i)\b(?:fig(?:ure)?\.?)\s*'+str(args.around)+r'\b',r['captions']+' '+r['figure_references'])}
        nearby={n for p in hits for n in (p-1,p,p+1) if 1<=n<=len(rows)}
        rows=[r for r in rows if r['page'] in nearby]
    for r in rows:
        if r['captions'] or r['figure_references'] or r['image_objects']:
            print(f"Page {r['page']:>3} | Images {r['image_objects']:>2} | Captions {r['captions'][:180]} | Refs {r['figure_references']}")
if __name__=='__main__':main()
