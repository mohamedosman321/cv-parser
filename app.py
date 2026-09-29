import html
import requests
import streamlit as st

DEFAULT_URL = ""

st.set_page_config(page_title="CV PARSER", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Mono:wght@400;700&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background: #FFE500;
    color: #000;
}
#MainMenu, header, footer { visibility: hidden; }
.block-container { max-width: 760px; padding-top: 3rem; padding-bottom: 6rem; }

.title {
    font-family: 'Archivo Black', sans-serif;
    font-size: clamp(3.5rem, 12vw, 6.5rem);
    line-height: 0.9;
    text-transform: uppercase;
    margin: 0 0 1rem;
}
.title span {
    background: #FF3EA5; color: #000;
    border: 5px solid #000; box-shadow: 10px 10px 0 #000;
    padding: 0 0.6rem; display: inline-block; transform: rotate(-2deg);
}
.sub {
    display: inline-block; background: #000; color: #FFE500;
    padding: 0.4rem 0.9rem; font-weight: 700; text-transform: uppercase;
    transform: rotate(1deg); margin-bottom: 2.5rem;
}

[data-testid="stFileUploaderDropzone"] {
    background: #00E0FF; border: 5px dashed #000; border-radius: 0;
    box-shadow: 8px 8px 0 #000; padding: 2rem;
}
[data-testid="stFileUploaderDropzone"] * { color: #000 !important; font-weight: 700; }
[data-testid="stFileUploaderDropzone"] button {
    background: #fff; border: 4px solid #000; border-radius: 0;
    box-shadow: 4px 4px 0 #000; text-transform: uppercase;
}

[data-testid="stExpander"] {
    background: #fff; border: 4px solid #000; border-radius: 0;
    box-shadow: 6px 6px 0 #000; margin-top: 2rem;
}
[data-testid="stExpander"] summary { font-weight: 700; text-transform: uppercase; }
[data-testid="stExpander"] input {
    border: 3px solid #000 !important; border-radius: 0 !important; background: #fff;
}

.stButton > button {
    font-family: 'Archivo Black', sans-serif; font-size: 1.6rem; text-transform: uppercase;
    background: #FF3EA5; color: #000; border: 5px solid #000; border-radius: 0;
    box-shadow: 8px 8px 0 #000; padding: 0.7rem 2.5rem; margin-top: 2rem;
    transition: transform 0.05s, box-shadow 0.05s;
}
.stButton > button:hover { background: #B6FF00; color: #000; border: 5px solid #000; }
.stButton > button:active { transform: translate(8px, 8px); box-shadow: 0 0 0 #000; }

[data-testid="stAlert"] {
    background: #fff; border: 4px solid #000; border-radius: 0;
    box-shadow: 6px 6px 0 #000; color: #000;
}

.name {
    font-family: 'Archivo Black', sans-serif; font-size: clamp(2.2rem, 8vw, 4rem);
    line-height: 1; text-transform: uppercase; background: #FF3EA5;
    border: 5px solid #000; box-shadow: 10px 10px 0 #000;
    padding: 1rem 1.2rem; margin-top: 3.5rem; transform: rotate(-1deg);
}
.email {
    background: #000; color: #B6FF00; font-weight: 700; padding: 0.7rem 1.2rem;
    margin: 1.2rem 0 0 2rem; display: inline-block; transform: rotate(1deg);
}
.card { border: 5px solid #000; box-shadow: 10px 10px 0 #000; padding: 1.2rem 1.4rem; margin-top: 2.8rem; }
.card.edu { background: #00E0FF; transform: rotate(0.6deg); }
.card.exp { background: #B6FF00; transform: rotate(-0.6deg); }
.card.skl { background: #fff; transform: rotate(0.4deg); }
.label {
    font-family: 'Archivo Black', sans-serif; font-size: 1.8rem; text-transform: uppercase;
    background: #000; color: #fff; display: inline-block; padding: 0 0.6rem; margin-bottom: 0.8rem;
}
.item { border-top: 3px solid #000; padding: 0.7rem 0; font-weight: 700; }
.chip {
    display: inline-block; border: 3px solid #000; box-shadow: 4px 4px 0 #000;
    padding: 0.2rem 0.7rem; margin: 0.4rem 0.6rem 0.4rem 0; font-weight: 700;
}
.chip.c0 { background: #FFE500; }
.chip.c1 { background: #FF3EA5; }
.chip.c2 { background: #00E0FF; }
.chip.c3 { background: #B6FF00; }
[data-testid="stExpander"] label,
[data-testid="stExpander"] label p { color: #000 !important; font-weight: 700; }
[data-testid="stExpander"] input { color: #000 !important; -webkit-text-fill-color: #000; }
[data-testid="stExpander"] summary { background: #fff; }
</style>
""", unsafe_allow_html=True)


def item_text(item):
    if isinstance(item, dict):
        return " / ".join(str(v) for v in item.values() if v)
    return str(item)


def as_list(items):
    if not items:
        return []
    return items if isinstance(items, list) else [items]


def rows_card(title, items, css_class):
    items = as_list(items)
    if not items:
        return
    rows = "".join(f'<div class="item">{html.escape(item_text(i))}</div>' for i in items)
    st.markdown(
        f'<div class="card {css_class}"><div class="label">{title}</div>{rows}</div>',
        unsafe_allow_html=True,
    )


def skills_card(items):
    items = as_list(items)
    if not items:
        return
    chips = "".join(
        f'<span class="chip c{n % 4}">{html.escape(item_text(s))}</span>'
        for n, s in enumerate(items)
    )
    st.markdown(
        f'<div class="card skl"><div class="label">Skills</div><div>{chips}</div></div>',
        unsafe_allow_html=True,
    )


st.markdown('<div class="title"><span>CV</span> PARSER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Drop a PDF. Get the goods.</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("", type="pdf", label_visibility="collapsed")

with st.expander("Connection"):
    url = st.text_input("Server URL", value=DEFAULT_URL)

if uploaded and st.button("PARSE!"):
    with st.spinner("KAGGLE IS THINKING..."):
        try:
            r = requests.post(
                url.rstrip("/") + "/parse",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=600,
            )
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    if "error" in data:
        st.error(data["error"])
        st.code(data.get("raw", ""))
        st.stop()

    st.markdown(f'<div class="name">{html.escape(str(data.get("full_name", "")))}</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="email">{html.escape(str(data.get("email", "")))}</div>',
                unsafe_allow_html=True)
    rows_card("Education", data.get("education"), "edu")
    rows_card("Experience", data.get("experience"), "exp")
    skills_card(data.get("skills"))