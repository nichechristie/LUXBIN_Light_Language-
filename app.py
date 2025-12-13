"""
LUXBIN - Photonic Binary Language Demo
A language where colors are letters and shades are grammar
"""

import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

# LUXBIN Alphabet (26 letters A-Z)
ALPHABET = {
    'A': 0.0, 'B': 5.625, 'C': 11.25, 'D': 16.875, 'E': 22.5,
    'F': 28.125, 'G': 33.75, 'H': 39.375, 'I': 45.0, 'J': 50.625,
    'K': 56.25, 'L': 61.875, 'M': 67.5, 'N': 73.125, 'O': 78.75,
    'P': 84.375, 'Q': 90.0, 'R': 95.625, 'S': 101.25, 'T': 106.875,
    'U': 112.5, 'V': 118.125, 'W': 123.75, 'X': 129.375, 'Y': 135.0,
    'Z': 140.625
}

# Reverse mapping
REVERSE_ALPHABET = {v: k for k, v in ALPHABET.items()}

# Grammar mappings
PARTS_OF_SPEECH = {
    'Noun': 100,
    'Verb': 75,
    'Adjective': 50,
    'Modifier': 30,
    'Control': 0
}

TENSES = {
    'Present': 70,
    'Past': 40,
    'Future': 85,
    'Conditional': 90
}


def hsl_to_rgb(h, s, l):
    """Convert HSL to RGB (0-255)"""
    s = s / 100.0
    l = l / 100.0

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


def encode_text_to_luxbin(text, part_of_speech='Noun', tense='Present'):
    """Encode text to LUXBIN color sequence"""
    text = text.upper()
    saturation = PARTS_OF_SPEECH.get(part_of_speech, 100)
    lightness = TENSES.get(tense, 70)

    colors = []
    for char in text:
        if char == ' ':
            colors.append((0, 0, 0))  # Black for space
        elif char in ALPHABET:
            hue = ALPHABET[char]
            rgb = hsl_to_rgb(hue, saturation, lightness)
            colors.append(rgb)
        else:
            colors.append((128, 128, 128))  # Gray for unknown

    return colors


def create_color_strip(colors, width=800, height=100):
    """Create image showing color sequence"""
    if not colors:
        return Image.new('RGB', (width, height), 'black')

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    block_width = width // len(colors)

    for i, color in enumerate(colors):
        x1 = i * block_width
        x2 = x1 + block_width
        draw.rectangle([x1, 0, x2, height], fill=color)

    return img


def create_hue_wheel(size=400):
    """Create visual hue wheel showing alphabet"""
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = size // 2 - 20

    # Draw color wheel
    for i in range(360):
        angle = i * np.pi / 180
        hue = i
        rgb = hsl_to_rgb(hue, 100, 70)

        x1 = center + int((radius - 30) * np.cos(angle))
        y1 = center + int((radius - 30) * np.sin(angle))
        x2 = center + int(radius * np.cos(angle))
        y2 = center + int(radius * np.sin(angle))

        draw.line([x1, y1, x2, y2], fill=rgb, width=2)

    # Add letter labels
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        font = ImageFont.load_default()

    for letter, hue in ALPHABET.items():
        angle = (hue - 90) * np.pi / 180  # Adjust for top = 0°
        label_radius = radius + 30
        x = center + int(label_radius * np.cos(angle))
        y = center + int(label_radius * np.sin(angle))

        # Draw letter
        bbox = draw.textbbox((x, y), letter, font=font)
        draw.text((x - (bbox[2] - bbox[0]) / 2, y - (bbox[3] - bbox[1]) / 2),
                  letter, fill='black', font=font)

    return img


def encode_demo(text, pos, tense):
    """Main encoding function"""
    colors = encode_text_to_luxbin(text, pos, tense)
    strip = create_color_strip(colors)

    # Create description
    desc = f"**LUXBIN Encoding**\n\n"
    desc += f"Text: `{text}`\n\n"
    desc += f"Grammar: {pos} (Saturation: {PARTS_OF_SPEECH[pos]}%), "
    desc += f"{tense} (Lightness: {TENSES[tense]}%)\n\n"
    desc += f"**Color Sequence:** {len(colors)} symbols\n\n"

    # List each letter with its color
    for i, char in enumerate(text.upper()):
        if char == ' ':
            desc += "` ` → Black (word boundary)\n\n"
        elif char in ALPHABET:
            desc += f"`{char}` → Hue {ALPHABET[char]:.1f}° (RGB: {colors[i]})\n\n"

    return strip, desc


def create_grammar_guide():
    """Create visual guide for grammar rules"""
    img = Image.new('RGB', (600, 400), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_title = font = ImageFont.load_default()

    y = 20

    # Title
    draw.text((20, y), "LUXBIN Grammar Rules", fill='black', font=font_title)
    y += 40

    # Saturation (Parts of Speech)
    draw.text((20, y), "Saturation → Part of Speech", fill='black', font=font)
    y += 30

    for pos, sat in PARTS_OF_SPEECH.items():
        rgb = hsl_to_rgb(180, sat, 70)  # Use cyan hue for demo
        draw.rectangle([20, y, 70, y + 20], fill=rgb, outline='black')
        draw.text((80, y + 3), f"{pos}: {sat}%", fill='black', font=font)
        y += 30

    y += 20

    # Lightness (Tense)
    draw.text((20, y), "Lightness → Tense/Mode", fill='black', font=font)
    y += 30

    for tense, light in TENSES.items():
        rgb = hsl_to_rgb(180, 100, light)  # Use cyan hue for demo
        draw.rectangle([20, y, 70, y + 20], fill=rgb, outline='black')
        draw.text((80, y + 3), f"{tense}: {light}%", fill='black', font=font)
        y += 30

    return img


# Create Gradio interface
with gr.Blocks(title="LUXBIN - Photonic Binary Language", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # ⚛️ LUXBIN - Photonic Binary Language

    **A language where colors are letters and shades are grammar**

    - **Hue (0°-360°)** = Letter identity (A-Z)
    - **Saturation** = Part of speech (Noun, Verb, etc.)
    - **Lightness** = Tense/mode (Present, Past, etc.)
    - **Timing** = Word and sentence boundaries

    ---
    """)

    with gr.Tabs():
        # Tab 1: Encoder
        with gr.Tab("📤 Encode Text to LUXBIN"):
            gr.Markdown("### Convert text into photonic color sequences")

            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        label="Enter Text",
                        placeholder="HELLO WORLD",
                        value="HELLO"
                    )

                    pos_input = gr.Dropdown(
                        choices=list(PARTS_OF_SPEECH.keys()),
                        value="Noun",
                        label="Part of Speech (Saturation)"
                    )

                    tense_input = gr.Dropdown(
                        choices=list(TENSES.keys()),
                        value="Present",
                        label="Tense/Mode (Lightness)"
                    )

                    encode_btn = gr.Button("🎨 Encode to LUXBIN", variant="primary")

                with gr.Column():
                    color_output = gr.Image(label="LUXBIN Color Sequence")
                    desc_output = gr.Markdown()

            encode_btn.click(
                fn=encode_demo,
                inputs=[text_input, pos_input, tense_input],
                outputs=[color_output, desc_output]
            )

            gr.Markdown("""
            **How to read:**
            - Each color block = one letter
            - Black = space (word boundary)
            - Hue = which letter (A-Z)
            - Saturation = grammatical role
            - Lightness = tense
            """)

        # Tab 2: Alphabet Reference
        with gr.Tab("🎨 Alphabet & Hue Wheel"):
            gr.Markdown("### Visual reference for the LUXBIN alphabet")

            wheel_img = create_hue_wheel()
            gr.Image(value=wheel_img, label="LUXBIN Hue Wheel (26 Letters)")

            gr.Markdown("""
            **How it works:**
            - 360° hue spectrum divided into 64 symbols
            - A-Z occupy first 26 positions
            - Step size: 5.625° per symbol
            - A = 0° (red), Z = 140.625° (greenish-blue)
            """)

            # Show alphabet table
            gr.Markdown("### Complete Alphabet")

            alphabet_html = "<table style='width:100%'><tr>"
            for i, (letter, hue) in enumerate(ALPHABET.items()):
                if i % 6 == 0 and i > 0:
                    alphabet_html += "</tr><tr>"
                rgb = hsl_to_rgb(hue, 100, 70)
                alphabet_html += f"<td style='background-color:rgb{rgb}; padding:10px; text-align:center; border:1px solid black;'><b>{letter}</b><br>{hue:.1f}°</td>"
            alphabet_html += "</tr></table>"

            gr.HTML(alphabet_html)

        # Tab 3: Grammar Guide
        with gr.Tab("📚 Grammar Rules"):
            gr.Markdown("### LUXBIN grammar encoded in light properties")

            grammar_img = create_grammar_guide()
            gr.Image(value=grammar_img, label="Grammar Visual Guide")

            gr.Markdown("""
            ### Encoding Rules

            **Binary Layer:**
            - Each symbol = 6 bits (0-63)
            - Binary indexes photonic states
            - Not direct letter encoding

            **Photonic Layer:**
            - Hue = semantic identity (which letter/symbol)
            - Saturation = grammatical role
            - Lightness = temporal/modal information

            **Temporal Layer:**
            - 100ms = letter duration
            - 200ms dark = word boundary
            - 500ms dark = sentence end

            **Modifiers:**
            - +10% darker = plural
            - -10% lighter = negation
            - Rapid flicker = emphasis
            - Smooth fade = completion
            """)

        # Tab 4: About
        with gr.Tab("ℹ️ About LUXBIN"):
            gr.Markdown("""
            # About LUXBIN

            **LUXBIN** is a photonic binary language where semantic information is encoded directly in the physical properties of light.

            ## Key Concepts

            1. **Physics as Syntax**: Light parameters carry meaning
            2. **Parallel Channels**: Multiple layers of information in one photon
            3. **Non-Linear Encoding**: Not a cipher, but a genuine language

            ## Applications

            - **Assistive Technology**: Non-verbal communication
            - **Secure Communication**: Line-of-sight only, hard to intercept
            - **Extreme Environments**: Underwater, space, RF-denied zones
            - **Human-Machine Interfaces**: Direct photonic signaling

            ## Technical Details

            - **Alphabet Size**: 26 letters + 38 extended symbols
            - **Color Space**: HSL (Hue, Saturation, Lightness)
            - **Binary Base**: 6-bit indexing (64 total symbols)
            - **Grammar Layers**: Saturation, Lightness, Temporal

            ## Implementation

            - **Hardware**: ESP32 + WS2812 RGB LEDs
            - **Software**: Python encoder/decoder
            - **Perception**: Trainable by humans in ~30 minutes

            ## Status

            LUXBIN is a complete language specification ready for:
            - Hardware prototyping
            - Human perception testing
            - Standardization
            - Publication

            ---

            **Created by:** Nicholechristie
            **Version:** 1.0
            **License:** Open Specification
            """)

    # Examples
    gr.Markdown("---")
    gr.Markdown("### 🚀 Try These Examples")

    gr.Examples(
        examples=[
            ["HELLO WORLD", "Noun", "Present"],
            ["TEST", "Verb", "Past"],
            ["AI LANGUAGE", "Noun", "Future"],
            ["QUANTUM", "Adjective", "Present"],
        ],
        inputs=[text_input, pos_input, tense_input],
        outputs=[color_output, desc_output],
        fn=encode_demo,
        cache_examples=True
    )

# Launch
if __name__ == "__main__":
    demo.launch()
