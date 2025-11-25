PDF_GENERATION_PROMPT = """
You MUST generate a PDF from {pitch_deck_result}.

Steps:
1. Extract the JSON from {pitch_deck_result}
2. If it's wrapped in markdown code blocks (```json ... ```), remove the markdown
3. Call pdf_generation_tool with the clean JSON string
4. Return the result showing the saved file path

If {pitch_deck_result} is not available, return an error explaining what's missing.
"""

