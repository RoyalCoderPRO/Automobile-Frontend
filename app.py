import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Automobile Engine & Body Explorer",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom styling to ensure seamless full-width display
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            max-width: 100%;
        }
        iframe {
            border: none;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def get_base64_image(image_path: Path) -> str:
    """Reads an image file and returns base64 data URI."""
    suffix = image_path.suffix.lower().replace(".", "")
    mime_type = "jpeg" if suffix in ["jpg", "jpeg"] else suffix
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{mime_type};base64,{encoded}"

def prepare_html_with_embedded_assets(html_file: Path) -> str:
    """Reads HTML and replaces local image references with base64 data URIs."""
    html_content = html_file.read_text(encoding="utf-8")
    directory = html_file.parent
    
    # Replace all local image references in the directory
    for img_file in directory.glob("*.*"):
        if img_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".svg", ".webp", ".gif"]:
            filename = img_file.name
            if filename in html_content:
                data_uri = get_base64_image(img_file)
                html_content = html_content.replace(f'"{filename}"', f'"{data_uri}"')
                html_content = html_content.replace(f"'{filename}'", f"'{data_uri}'")
                
    return html_content

def main():
    workspace_dir = Path(__file__).parent.resolve()
    html_file = workspace_dir / "engine_explorer.html"
    
    if not html_file.exists():
        st.error(f"HTML file not found at: {html_file}")
        return
    
    html_content = prepare_html_with_embedded_assets(html_file)
    
    # Render component with full height
    components.html(html_content, height=920, scrolling=True)

if __name__ == "__main__":
    main()

