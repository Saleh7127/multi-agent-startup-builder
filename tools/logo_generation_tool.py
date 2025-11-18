"""Tooling for generating branded logo concepts via Gemini image models."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from google import genai
from google.adk.tools import FunctionTool


load_dotenv()

_client = genai.Client()


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "logo"


def generate_brand_logo(
    *,
    brand_name: str,
    creative_brief: str,
    visual_style: str = "modern minimal vector logo",
    color_palette: str = "",
    output_dir: str = "generated_assets/logos",
) -> dict:
    """Generate branded logo files using Gemini image generation.

    Args:
        brand_name: Company or product name to showcase in the logo.
        creative_brief: Describes audience, tone, motifs, and differentiators.
        visual_style: Optional stylistic direction to bias the render.
        color_palette: Optional palette notes (hex codes or descriptors).
        output_dir: Directory where generated image files should be saved.

    Returns:
        Dictionary including the resolved prompt, saved file paths, and notes.
    """

    palette_instruction = (
        f" Use this palette: {color_palette}." if color_palette and color_palette.strip() else ""
    )

    prompt = (
        f"Design a brand-ready 2D vector style logo for {brand_name}. "
        f"Creative direction: {creative_brief}. Visual style: {visual_style}."
        f"{palette_instruction} Deliver a transparent background, high contrast"
        " mark suitable for web and print.".strip()
    )

    try:
        response = _client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt],
        )
    except Exception as exc:  # pragma: no cover - surfaced to agent
        return {
            "prompt": prompt,
            "saved_files": [],
            "notes": ["Image generation failed", str(exc)],
        }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files: List[str] = []
    notes: List[str] = []
    slug = _slugify(brand_name)

    for index, part in enumerate(response.parts, start=1):
        if getattr(part, "text", None):
            notes.append(part.text)
            continue

        if getattr(part, "inline_data", None):
            image = part.as_image()
            filename = output_path / f"{slug}_logo_{index}.png"
            image.save(filename)
            saved_files.append(str(filename))

    if not saved_files:
        notes.append("No binary image data returned by model.")

    return {
        "prompt": prompt,
        "saved_files": saved_files,
        "notes": notes,
    }


logo_generation_tool = FunctionTool(generate_brand_logo)

