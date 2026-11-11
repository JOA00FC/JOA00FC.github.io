#!/usr/bin/env python3
"""JOA00FC Film 1.0 — deterministic XMP/CUBE generator.
Developed with assistance from ChatGPT. Requires Python 3 + NumPy.
The XMP and display-referred LUT share an art direction, not an identical renderer.
"""
from pathlib import Path
import hashlib
import json
import uuid
import xml.etree.ElementTree as ET
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'pacote'
VERSION = '1.0'
WEIGHTS = np.array([0.2126, 0.7152, 0.0722])

def tone(x, mono=False):
    return (0.015 if mono else 0.018) + (0.970 if mono else 0.960) * (
        x - (0.035 if mono else 0.025) * np.sin(2 * np.pi * x))

def transform(rgb, mono=False):
    """Input/output normalized display RGB, SDR. Not a Log/HDR transform."""
    rgb = np.asarray(rgb, dtype=np.float64)
    if mono:
        y = rgb @ np.array([0.28, 0.62, 0.10])
        return np.repeat(tone(y, True)[..., None], 3, axis=-1)
    out = tone(rgb)
    y = out @ WEIGHTS
    out = y[..., None] + 0.88 * (out - y[..., None])
    # Modest warmth in midtones, fading toward black and white.
    weight = 4 * y * (1 - y)
    out += weight[..., None] * np.array([0.014, 0.003, -0.011])
    # Analytically bounded for valid input; clipping is only a defensive guard.
    return np.clip(out, 0, 1)

def make_cube(mono, n):
    label = 'Mono_Soft' if mono else 'Color_Soft'
    folder = PACK / '02_LUT_VIDEO' / str(n)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'JOA00FC_Film_{label}_{n}.cube'
    # CUBE ordering: red varies fastest, blue slowest.
    b, g, r = np.meshgrid(*([np.linspace(0, 1, n)] * 3), indexing='ij')
    grid = np.stack([r, g, b], axis=-1).reshape(-1, 3)
    values = transform(grid, mono)
    assert np.isfinite(values).all() and values.min() > 0 and values.max() < 1
    header = f'''# JOA00FC Film {VERSION} | JOA00FC — desenvolvido com auxilio do ChatGPT
# SDR display-referred RGB / Rec.709. Not a Log or HDR conversion.
# Color only: grain and vignette must be added separately.
# See CREDITOS_E_USO.txt. Independent design; no Instagram assets included.
TITLE "JOA00FC Film {label} v{VERSION}"
LUT_3D_SIZE {n}
DOMAIN_MIN 0.0 0.0 0.0
DOMAIN_MAX 1.0 1.0 1.0
'''
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write(header)
        np.savetxt(f, values, fmt='%.7f')
    return path

def make_xmp(mono):
    ns = {'x':'adobe:ns:meta/', 'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
          'crs':'http://ns.adobe.com/camera-raw-settings/1.0/'}
    for k, v in ns.items(): ET.register_namespace(k, v)
    def tag(p, n): return '{' + ns[p] + '}' + n
    label = 'Mono Soft' if mono else 'Color Soft'
    name = 'JOA00FC Film - ' + label
    root = ET.Element(tag('x','xmpmeta'))
    rdf = ET.SubElement(root, tag('rdf','RDF'))
    desc = ET.SubElement(rdf, tag('rdf','Description'), {tag('rdf','about'):''})
    attrs = {
        'PresetType':'Normal','Cluster':'','UUID':uuid.uuid5(uuid.NAMESPACE_URL, 'https://joa00fc.github.io/filmes/'+label+'/1.0').hex.upper(),
        'SupportsAmount':'True','SupportsColor':'True','SupportsMonochrome':'True',
        'SupportsHighDynamicRange':'False','SupportsNormalDynamicRange':'True',
        'SupportsSceneReferred':'True','SupportsOutputReferred':'True',
        'CameraModelRestriction':'','Copyright':'JOA00FC | Desenvolvido com auxilio do ChatGPT',
        'ContactInfo':'https://joa00fc.github.io/filmes/',
        'Version':'15.0','ProcessVersion':'11.0','HasSettings':'True',
        'AutoTone':'False','Contrast2012':'0','Highlights2012':'-12',
        'Shadows2012':'6','Whites2012':'-4','Blacks2012':'0',
        'Texture':'0','Clarity2012':'2','Dehaze':'0','Vibrance':'0',
        'Saturation':'0' if mono else '-12',
        'ConvertToGrayscale':'True' if mono else 'False',
        'ToneCurveName2012':'Custom',
        'ParametricShadows':'0','ParametricDarks':'0','ParametricLights':'0','ParametricHighlights':'0',
        'ParametricShadowSplit':'25','ParametricMidtoneSplit':'50','ParametricHighlightSplit':'75',
        'GrainAmount':'16' if mono else '12','GrainSize':'22','GrainFrequency':'40',
        'PostCropVignetteAmount':'-8','PostCropVignetteMidpoint':'40',
        'PostCropVignetteRoundness':'0','PostCropVignetteFeather':'85',
        'PostCropVignetteStyle':'1','PostCropVignetteHighlightContrast':'20',
        'SplitToningShadowHue':'0' if mono else '35',
        'SplitToningShadowSaturation':'0' if mono else '3',
        'SplitToningHighlightHue':'0' if mono else '45',
        'SplitToningHighlightSaturation':'0' if mono else '5',
        'SplitToningBalance':'0',
        'ColorGradeMidtoneHue':'0','ColorGradeMidtoneSat':'0',
        'ColorGradeShadowLum':'0','ColorGradeMidtoneLum':'0','ColorGradeHighlightLum':'0',
        'ColorGradeBlending':'50','ColorGradeGlobalHue':'0','ColorGradeGlobalSat':'0','ColorGradeGlobalLum':'0',
    }
    # Deliberately do not set Exposure, WB, crop, optics, camera profile or sharpening.
    for hue in ['Red','Orange','Yellow','Green','Aqua','Blue','Purple','Magenta']:
        for action in ['Hue','Saturation','Luminance']:
            attrs[f'{action}Adjustment{hue}']='0'
    if mono:
        attrs['AutoGrayscaleMix']='False'
        for hue, val in dict(Red=6,Orange=8,Yellow=2,Green=-4,Aqua=-5,Blue=-8,Purple=0,Magenta=0).items():
            attrs['GrayMixer'+hue]=str(val)
    for k, v in attrs.items(): desc.set(tag('crs',k), v)
    for k, v in [('Name',name),('Group','JOA00FC Film'),('Description',
          'Filme suave em preto e branco neutro. v1.0.' if mono else 'Filme suave, cores contidas e calor discreto. v1.0.')]:
        elem = ET.SubElement(desc,tag('crs',k))
        alt = ET.SubElement(elem,tag('rdf','Alt'))
        ET.SubElement(alt,tag('rdf','li'),{'{http://www.w3.org/XML/1998/namespace}lang':'x-default'}).text=v
    for channel in ['', 'Red', 'Green', 'Blue']:
        curve=ET.SubElement(desc,tag('crs','ToneCurvePV2012'+channel))
        seq=ET.SubElement(curve,tag('rdf','Seq'))
        xs=list(range(0,256,16))+[255] if channel=='' else [0,255]
        for x in xs:
            y=int(round(float(tone(x/255,mono))*255)) if channel=='' else x
            ET.SubElement(seq,tag('rdf','li')).text=f'{x}, {y}'
    ET.indent(root,space='  ')
    folder=PACK/'01_LIGHTROOM_XMP'
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/f'JOA00FC_Film_{label.replace(" ","_")}.xmp'
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
    return path

def validate():
    report={'version':VERSION, 'xmp_validation':'XML and required preset fields; not tested inside Adobe Lightroom',
            'lut_validation':'Bounds, neutral B&W, monotonic neutral ramp, table dimensions and red-fastest ordering',
            'input':'SDR display RGB / Rec.709; convert Log, HLG or PQ before LUT',
            'art_direction_match':'XMP and CUBE are separate implementations; not pixel-identical', 'luts':[]}
    ramp=np.repeat(np.linspace(0,1,65536)[:,None],3,axis=1)
    for mono in [False,True]:
        v=transform(ramp,mono)
        assert np.all(np.diff(v,axis=0)>0)
        if mono: assert np.max(np.ptp(v,axis=1))==0
    for p in sorted(PACK.rglob('*.cube')):
        lines=p.read_text().splitlines()
        n=int(next(l.split()[1] for l in lines if l.startswith('LUT_3D_SIZE')))
        v=np.array([[float(t) for t in l.split()] for l in lines if l and l[0].isdigit()])
        assert v.shape==(n**3,3) and np.isfinite(v).all()
        assert v.min()>0 and v.max()<1
        report['luts'].append({'file':str(p.relative_to(PACK)),'rows':len(v),'min':float(v.min()),'max':float(v.max())})
    ids=[]
    for p in sorted(PACK.rglob('*.xmp')):
        tree=ET.parse(p); crs='{http://ns.adobe.com/camera-raw-settings/1.0/}'
        d=tree.find('.//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')
        assert d.get(crs+'PresetType')=='Normal'
        ids.append(d.get(crs+'UUID'))
        assert crs+'Exposure2012' not in d.attrib and crs+'WhiteBalance' not in d.attrib
    assert len(set(ids))==2
    (PACK/'VALIDACAO.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    files=sorted(p for p in PACK.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    (PACK/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(PACK))+'\n' for p in files))
    print(json.dumps({'files':len(files)+1,'validation':'passed','lut_count':len(report['luts'])}))

if __name__=='__main__':
    for mono in [False,True]:
        make_xmp(mono)
        for n in [33,65]: make_cube(mono,n)
    validate()
