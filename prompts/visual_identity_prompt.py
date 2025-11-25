VISUAL_IDENTITY_PROMPT = """
Create visual identity. Use logo_generation_tool.generate_brand_logo (required: brand_name, creative_brief). Keep concise. Return JSON only:

{
  "brand_essence": {"tagline": "Brief", "voice": "Brief", "story": "1-2 sentences"},
  "color_palette": [{"name": "Name", "hex": "#RRGGBB", "usage": "Brief"}],
  "typography": [{"family": "Family", "role": "Heading|Body|Accent"}],
  "imagery_guidelines": ["G1", "G2"],
  "logo_assets": {
    "concept": "Brief",
    "generation_parameters": {"brand_name": "Name", "creative_brief": "Brief", "visual_style": "Style"},
    "generated_files": ["Path1"]
  },
  "usage_examples": ["E1", "E2"],
  "risks": ["R1"]
}
"""

