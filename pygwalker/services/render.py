import os
import sys
import json
import base64
import zlib
from typing import Dict, List, Any

from jinja2 import Environment, PackageLoader, FileSystemLoader

from pygwalker._constants import ROOT_DIR
from pygwalker.utils.encode import DataFrameEncoder


# if getattr(sys, 'frozen', False):
#     # we are running in a bundle
# else:
#     loader = PackageLoader("pygwalker")
loader = PackageLoader("pygwalker")
jinja_env = Environment(
    loader=loader,
    autoescape=(()),  # select_autoescape()
)

ROOT_DIR = "pygwalker"
def gwalker_script() -> str:
    with open(os.path.join("pygwalker", 'templates', 'dist', 'pygwalker-app.iife.js'), 'r', encoding='utf8') as f:
        gwalker_js = f.read()
    return gwalker_js


def get_max_limited_datas(datas: List[Dict[str, Any]], byte_limit: int) -> List[Dict[str, Any]]:
    if len(datas) > 1024:
        smp0 = datas[::len(datas)//32]
        smp1 = datas[::len(datas)//37]
        avg_size = len(json.dumps(smp0, cls=DataFrameEncoder)) / len(smp0)
        avg_size = max(avg_size, len(json.dumps(smp1, cls=DataFrameEncoder)) / len(smp1))
        n = int(byte_limit / avg_size)
        if len(datas) >= 2 * n:
            return datas[:n]
    return datas


def render_gwalker_iframe(gid: int, srcdoc: str) -> str:
    return jinja_env.get_template("pygwalker_iframe.html").render(
        gid=gid,
        srcdoc=srcdoc,
    )


def render_gwalker_html(gid: int, props: Dict) -> str:
    walker_template = jinja_env.get_template("walk.js")
    js_list = [
        "var exports={}, module={};",
        gwalker_script(),
        walker_template.render(gwalker={'id': gid, 'props': json.dumps(props, cls=DataFrameEncoder)})
    ]
    js = "\n".join(js_list)
    template = jinja_env.get_template("index.html")
    html = f"{template.render(gwalker={'id': gid, 'script': js})}"
    return html


def get_dsl_wasm() -> str:
    """get compressed wasm code(base64) for dsl to sql"""
    wasm_file_path = os.path.join(ROOT_DIR, 'templates', 'dsl_to_sql.wasm')
    with open(wasm_file_path, 'rb') as f:
        wasm_content = f.read()

    content = zlib.compress(base64.b64encode(wasm_content))

    return base64.b64encode(content).decode()
