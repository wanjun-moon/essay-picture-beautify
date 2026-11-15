#!/usr/bin/env python3
"""Plot authentic CSV series and optional interval columns; save SVG, PDF, PNG.

CSV format: x,series,value[,lower,upper] with one row per observed point.
No interpolation or data fabrication. Requires pandas and matplotlib.
"""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PALETTE=['#3979B7','#DF8A35','#369D95','#AA6BA4','#7769AC','#5D6570','#C35C57','#65934D']
MARKERS=['o','s','^','D','v','P','X','h']

def make_plot(data_path,output_prefix,xlabel,ylabel,kind,width_mm,height_mm):
    df=pd.read_csv(data_path)
    mandatory={'x','series','value'}
    if not mandatory.issubset(df.columns):raise ValueError(f'CSV requires {sorted(mandatory)}')
    if df[list(mandatory)].isnull().any().any():raise ValueError('Null x/series/value is not allowed')
    for col in ['value','lower','upper']:
        if col in df.columns:df[col]=pd.to_numeric(df[col],errors='raise')
    has_interval={'lower','upper'}.issubset(df.columns)
    if (('lower' in df.columns) != ('upper' in df.columns)):
        raise ValueError('Provide both lower and upper columns')
    if has_interval and ((df.lower>df.value)|(df.value>df.upper)).any():
        raise ValueError('Each interval must contain value')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','pdf.fonttype':42})
    fig,ax=plt.subplots(figsize=(width_mm/25.4,height_mm/25.4),layout='constrained')
    for i,(name,sub) in enumerate(df.groupby('series',sort=False)):
        try:sub=sub.sort_values('x')
        except TypeError:pass
        color=PALETTE[i%len(PALETTE)]; marker=MARKERS[i%len(MARKERS)]
        x=sub['x'].to_numpy();y=sub.value.to_numpy(dtype=float)
        if kind=='interval':
            if not has_interval:raise ValueError('interval kind requires lower and upper')
            error=[y-sub.lower.to_numpy(dtype=float),sub.upper.to_numpy(dtype=float)-y]
            ax.errorbar(x,y,yerr=error,label=str(name),fmt=marker,ms=4,color=color,capability=0) if False else ax.errorbar(x,y,yerr=error,label=str(name),fmt=marker,ms=4,color=color,capsize=2)
        elif kind=='line':
            ax.plot(x,y,label=str(name),color=color,linewidth=1.4,marker=marker,markersize=3.5)
            if has_interval:ax.fill_between(x,sub.lower.to_numpy(dtype=float),sub.upper.to_numpy(dtype=float),color=color,alpha=.15)
    ax.set_xlabel(xlabel);ax.set_ylabel(ylabel);ax.grid(alpha=.18,linewidth=.5)
    ax.spines[['top','right']].set_visible(False)
    if df.series.nunique()>1:ax.legend(frameon=False,fontsize=7,ncol=min(3,df.series.nunique()))
    output_prefix=Path(output_prefix);output_prefix.parent.mkdir(parents=True,exist_ok=True)
    for ext in ('svg','pdf','png'):fig.savefig(output_prefix.with_suffix('.'+ext),dpi=300)
    plt.close(fig)
    return [output_prefix.with_suffix('.'+e) for e in ('svg','pdf','png')]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv',type=Path);p.add_argument('output_prefix',type=Path)
    p.add_argument('--x-label',default='X');p.add_argument('--y-label',default='Value')
    p.add_argument('--kind',choices=['line','interval'],default='line')
    p.add_argument('--width-mm',type=float,default=180);p.add_argument('--height-mm',type=float,default=100)
    a=p.parse_args()
    for f in make_plot(a.csv,a.output_prefix,a.x_label,a.y_label,a.kind,a.width_mm,a.height_mm):print(f)
if __name__=='__main__':main()
