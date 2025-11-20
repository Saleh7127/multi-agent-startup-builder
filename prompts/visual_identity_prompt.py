VISUAL_IDENTITY_PROMPT = """
Create visual identity. Use logo_generation_tool.generate_brand_logo (required: brand_name, creative_brief). Return JSON only:

{
  "brand_essence": {"tagline": "Tagline", "voice": "Voice", "story": "Story"},
  "audience_moodboard": ["Mood1"],
  "color_palette": [{"name": "Name", "hex": "#RRGGBB", "usage": "Usage", "emotion": "Emotion"}],
  "typography": [{"family": "Family", "role": "Heading|Body|Accent", "fallbacks": ["Fallback1"], "usage_notes": "Notes"}],
  "imagery_guidelines": ["Guideline1"],
  "logo_assets": {
    "concept": "Concept",
    "generation_parameters": {"brand_name": "Name", "creative_brief": "Brief", "visual_style": "Style", "color_palette": "Palette"},
    "generated_files": ["Path1"],
    "handoff": ["Step1"]
  },
  "usage_examples": ["Example1"],
  "risks_or_questions": ["Risk1"]
}
"""

