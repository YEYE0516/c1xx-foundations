"""Derive strong / soft / on for an accent so the set passes WCAG on a given canvas.
usage: python3 -I build/derive-accent.py '#54B8AB' '#f7f5f0'
"""
import sys, colorsys, json
def h2rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def rgb2h(c): return '#%02x%02x%02x' % tuple(round(max(0,min(1,x))*255) for x in c)
def lum(c):
    f=lambda x: x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4
    r,g,b=c; return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def contrast(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
def darken_to(c, canvas, target=4.5):
    h,l,s=colorsys.rgb_to_hls(*c)
    for i in range(200):
        cand=colorsys.hls_to_rgb(h, max(0,l-i*0.005), min(1, s+ i*0.002))
        if contrast(cand, canvas) >= target: return cand
    return cand
def mix(a,b,t): return tuple(a[i]*(1-t)+b[i]*t for i in range(3))
def derive(base_hex, canvas_hex, ink='#121310', paper='#f7f5f0'):
    base, canvas = h2rgb(base_hex), h2rgb(canvas_hex)
    strong = darken_to(base, canvas)
    soft = mix(base, canvas, 0.86)
    on = ink if contrast(h2rgb(ink), base) >= contrast(h2rgb(paper), base) else paper
    return {"base": base_hex.lower(), "strong": rgb2h(strong), "soft": rgb2h(soft), "on": on,
            "contrast": {"base_on_canvas": round(contrast(base,canvas),2), "strong_on_canvas": round(contrast(strong,canvas),2), "on_on_base": round(contrast(h2rgb(on), base),2)}}
if __name__ == "__main__":
    print(json.dumps(derive(sys.argv[1], sys.argv[2]), indent=1))
