import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
src=Path(sys.argv[1]).read_text(encoding="utf-8"); out=sys.argv[2]
page_html='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'+src+'</body></html>'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    pg=b.new_page(viewport={"width":1280,"height":900})
    errs=[]; pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.set_content(page_html); pg.wait_for_timeout(1500)
    pg.screenshot(path=f"{out}/c-hero.png",clip={"x":0,"y":0,"width":1280,"height":880})
    lad=pg.locator(".tech").bounding_box(); pg.screenshot(path=f"{out}/c-tech.png",clip=lad,full_page=True)
    lp=pg.locator(".loop").bounding_box(); ex=pg.locator(".exec").bounding_box()
    pg.screenshot(path=f"{out}/c-lower.png",clip={"x":0,"y":ex["y"]-20,"width":1280,"height":lp["y"]+lp["height"]-ex["y"]+40},full_page=True)
    print("errors",errs)
    pg2=b.new_page(viewport={"width":390,"height":844}); pg2.set_content(page_html); pg2.wait_for_timeout(1200)
    pg2.screenshot(path=f"{out}/c-phone1.png")
    t=pg2.locator(".tech").bounding_box(); pg2.screenshot(path=f"{out}/c-phone2.png",clip={"x":0,"y":t["y"],"width":390,"height":1300},full_page=True)
    pg3=b.new_page(viewport={"width":820,"height":900}); pg3.set_content(page_html); pg3.wait_for_timeout(1200)
    print("820 sw",pg3.evaluate("document.documentElement.scrollWidth"))
    pg3.screenshot(path=f"{out}/c-tab.png",full_page=True)
    b.close()
