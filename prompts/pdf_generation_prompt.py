PDF_GENERATION_PROMPT = """
Generate PDF from {pitch_deck_result}.

Extract JSON from {pitch_deck_result} (remove markdown code blocks if present). Call pdf_generation_tool with the JSON string. Return the result.
"""

