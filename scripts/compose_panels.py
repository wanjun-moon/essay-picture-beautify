#!/usr/bin/env python3
"""Create SVG figure panels embedding original image bytes unmodified.

JSON config: {"columns": 2,"tile_width_px":360,"tile_height_px":240,
"gap_px":14,"panels":[{"image":"a.png","label":"(a) Input", "crop":[x,y,w,h]}]}
Crop is optional. Cropping uses an SVG viewport; original data remains embedded.
"""
import argparse
import base64
import json
import mimetypes
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
from PIL import Image

SUPPORTED={'image/png','image/jpeg','image/webp','image/tiff','image/gif'}
def compose(cfg_path,out_path):
    cfg_path=Path(cfg_path);out_path=Path(out_path)
    cfg=json.loads(cfg_path.read_text(encoding='utf-8'))
    panels=cfg['panels'];cols=int(cfg.get('columns',2));tw=int(cfg.get('tile_width_px',360));th=int(cfg.get('tile_height_px',240));gap=int(cfg.get('gap_px',14))
    if cols<1 or tw<1 or th<1 or gap<0 or not panels:raise ValueError('Invalid layout')
    label_height=30;rows=(len(panels)+cols-1)//cols
    total_w=cols*tw+(cols-1)*gap;total_h=rows*(th+label_height)+(rows-1)*gap
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">', '<rect width="100%" height="100%" fill="white"/>']
    for i,panel in enumerate(panels):
        path=(cfg_path.parent/panel['image']).resolve();raw=path.read_bytes()
        mime=mimetypes.guess_type(str(path))[0]
        if mime not in SUPPORTED:raise ValueError(f'Unsupported image: {path.name}')
        with Image.open(path) as im:iw,ih=im.size
        crop=panel.get('crop',[0,0,iw,ih]);cx,cy,cw,ch=map(int,crop)
        if cx<0 or cy<0 or cw<=0 or ch<=0 or cx+cw>iw or cy+ch>ih:raise ValueError('Crop outside source image')
        x=(i%cols)*(tw+gap);y=(i//cols)*(th+label_height+gap)
        scale=min(tw/cw,th/ch);dw=cw*scale;dh=ch*scale
        px=x+(tw-dw)/2;py=y+(th-dh)/2
        clip=f'clip{i}';parts.append(f'<defs><clipPath id="{clip}"><rect x="{px}" y="{py}" width="{dw}" height="{dh}"/></clipPath></defs>')
        uri='data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii')
        parts.append(f'<image x="{px-cx*scale}" y="{py-cy*scale}" width="{iw*scale}" height="{ih*scale}" preserveAspectRatio="none" clip-path="url(#{clip})" xlink:href="{uri}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" fill="none" stroke="#8a9299" stroke-width="1"/>')
        parts.append(f'<text x="{x+tw/2}" y="{y+th+20}" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="15" fill="#26323b">{escape(str(panel.get("label", "")))}</text>')
    parts.append('</svg>');out_path.parent.mkdir(parents=True,exist_ok=True);out_path.write_text('\n'.join(parts),encoding='utf-8')
    ET.parse(out_path)
    return out_path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('config',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();print(compose(a.config,a.output))
if __name__=='__main__':main()
