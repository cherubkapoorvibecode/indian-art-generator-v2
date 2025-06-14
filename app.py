import streamlit as st
import openai
import requests
from io import BytesIO

# Set config FIRST and only ONCE
st.set_page_config(page_title="Indian Art Styles Generator", layout="wide")

# App UI
st.title("🎨 Indian Art Styles from a Word")
st.write("✅ App loaded")  # Debug line
st.write("Enter a word and see how it inspires 3 Indian art forms.")

# Secure API key input
api_key = st.text_input("OpenAI API Key", type="password")
word = st.text_input("Inspiration Word", max_chars=30)

art_prompts = {
    "Mughal Painting": (
        "A traditional Indian Mughal miniature painting in intricate detail, inspired by the theme '{word}'. "
        "Royal figures, Persian-style floral borders, and ornate architecture, painted with natural pigments and gold leaf on textured handmade wasli paper. "
        "Visible brushwork, layered color tones, and realistic shadows create a museum-quality appearance."
    ),
    
    "Madhubani": (
        "A hand-painted Madhubani folk art illustration inspired by the theme '{word}', created using traditional Mithila techniques. "
        "Painted with natural dyes and inks on handmade paper, it includes detailed symbolic motifs like animals, plants, and deities in vibrant, tightly patterned compositions. "
        "Visible pen and brush strokes, slightly uneven lines, and organic imperfections add to the authenticity of the physical painting."
    ),
    
    "S.H. Raza": (
        "An abstract geometric painting in the style of S.H. Raza, inspired by the theme '{word}'. "
        "Bold concentric circles, triangles, and squares rendered in vivid acrylic paint — deep reds, blacks, ochres, and blues — on raw textured canvas. "
        "Visible brushstrokes, layered pigment buildup, and matte finish evoke the tactile feel of a hand-painted modernist canvas with spiritual symbolism."
    )
}

def generate_image(api_key, prompt):
    openai.api_key = api_key
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="standard",
        response_format="url"
    )
    img_url = response.data[0].url
    img_resp = requests.get(img_url)
    return img_resp.content

if st.button("Generate Art"):
    if not api_key or not word:
        st.error("Please provide both an API key and a word.")
    else:
        st.write("🎨 Generating... please wait ~10 sec")

        cols = st.columns(3)
        for i, (style_name, style_prompt) in enumerate(art_prompts.items()):
            with cols[i]:
                st.markdown(f"#### {style_name}")
                prompt = style_prompt.replace("{word}", word)
                img_bytes = generate_image(api_key, prompt)
                st.image(img_bytes, use_container_width=True)
                st.download_button(
                    label="Download",
                    data=img_bytes,
                    file_name=f"{style_name.replace(' ', '_')}_{word}.png",
                    mime="image/png"
                )
