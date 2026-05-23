import os
import base64
import streamlit as st
import streamlit.components.v1 as components


# ==========================================
# LOAD GLOBAL CSS
# ==========================================

def load_css(
    file_path="static/style.css"
):

    if not os.path.exists(
        file_path
    ):

        st.warning(
        f"CSS file not found: {file_path}"
        )

        return


    with open(
        file_path,
        encoding="utf-8"
    ) as f:

        st.markdown(
        f"""
        <style>
        {f.read()}
        </style>
        """,

        unsafe_allow_html=True
        )



# ==========================================
# LOCAL FONT INJECTION
# ==========================================

def inject_local_font(

    font_path,

    font_name="AdobeClean"

):

    if not os.path.exists(
        font_path
    ):

        return


    with open(
        font_path,
        "rb"
    ) as f:

        encoded=base64.b64encode(
            f.read()
        ).decode()


    ext=os.path.splitext(
        font_path
    )[1].lower()


    mime_types={

        ".otf":"font/otf",

        ".ttf":"font/ttf",

        ".woff":"font/woff",

        ".woff2":"font/woff2"

    }


    formats={

        ".otf":"opentype",

        ".ttf":"truetype",

        ".woff":"woff",

        ".woff2":"woff2"

    }


    mime=mime_types.get(
        ext,
        "font/otf"
    )


    fmt=formats.get(
        ext,
        "opentype"
    )


    st.markdown(
f"""

<style>

@font-face{{

font-family:
'{font_name}';

src:
url(
data:{mime};
base64,
{encoded}
)

format(
'{fmt}'
);

font-weight:
100 900;

font-style:
normal;

}}

</style>

""",

unsafe_allow_html=True
)



# ==========================================
# WEBRTC STYLE PATCH
# ==========================================

def inject_webrtc_styles():

    font_path=os.path.join(
        os.getcwd(),
        "static",
        "AdobeClean.otf"
    )


    if not os.path.exists(
        font_path
    ):

        return


    with open(
        font_path,
        "rb"
    ) as font_file:

        encoded_font=(
            base64
            .b64encode(
                font_file.read()
            )
            .decode()
        )


    components.html(
f"""

<script>

(function patchWebRTCStyles(){{

function injectIntoIframe(
iframe
){{

try{{

const doc=
iframe.contentDocument||
iframe.contentWindow.document;


if(
!doc||
!doc.head
)
return;


if(

doc.head.querySelector(
'#webrtc-custom-style'
)

)
return;


const style=
doc.createElement(
'style'
);


style.id=
'webrtc-custom-style';


style.textContent=`

@font-face{{

font-family:
'AdobeClean';

src:
url(
data:font/otf;
base64,
{encoded_font}
)

format(
'opentype'
);

}}



.MuiButtonBase-root,
.MuiButton-root,
.MuiButton-contained,
.MuiButton-text{{

border-radius:
15px!important;

font-family:
'AdobeClean',
sans-serif!important;

letter-spacing:
0.05em!important;

}}

`;

doc.head.appendChild(
style
);

}}

catch(e){{

console.warn(
"[WebRTC Patch]",
e
);

}}

}}



function patch(){{

const parentDoc=
window.parent.document;


const iframes=
parentDoc.querySelectorAll(
'iframe'
);


iframes.forEach(
iframe=>{{

if(

iframe.src&&
iframe.src.includes(
'webrtc'
)

){{

if(

iframe.contentDocument&&
iframe.contentDocument.readyState==="complete"

){{

injectIntoIframe(
iframe
);

}}

else{{

iframe.addEventListener(
'load',

()=>injectIntoIframe(
iframe
)

);

}}

}}

}}

);

}}

patch();

}})();

</script>

""",

height=0
)