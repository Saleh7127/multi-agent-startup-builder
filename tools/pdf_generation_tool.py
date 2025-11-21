"""Tooling for generating PDF pitch decks from JSON data."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

from fpdf import FPDF
from google.adk.tools import FunctionTool


def _slugify(value: str) -> str:
    """Convert a string to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "pitch-deck"


def _clean_bullets(text: str) -> str:
    """Replace unsupported bullet characters with dashes."""
    if not isinstance(text, str):
        return text
    # Replace various bullet characters with dash
    return text.replace("•", "-").replace("▪", "-").replace("▫", "-").replace("‣", "-").replace("⁃", "-")


def _add_section(pdf: FPDF, title: str, content: list[str] | str, is_metrics: bool = False) -> None:
    """Add a section to the PDF."""
    # Add section title
    pdf.set_font("Arial", "B", 14)
    pdf.ln(5)
    pdf.cell(0, 10, title, ln=1)
    pdf.ln(2)
    
    # Add content
    pdf.set_font("Arial", "", 11)
    
    if isinstance(content, str):
        # Handle string content
        pdf.multi_cell(0, 6, content, ln=1)
    elif isinstance(content, list):
        # Handle list of bullets
        for item in content:
            if item:
                cleaned_item = _clean_bullets(str(item))
                pdf.cell(5, 6, "-", ln=0)
                pdf.multi_cell(0, 6, cleaned_item, ln=1)
                pdf.ln(1)
    pdf.ln(3)


def generate_pitch_deck_pdf(
    *,
    pitch_deck_data: str,
    output_dir: str = "generated_assets/pitch_decks",
    filename: str = "",
) -> dict:
    """Generate a PDF pitch deck from JSON data.

    Args:
        pitch_deck_data: JSON string containing pitch deck data.
        output_dir: Directory where the PDF should be saved.
        filename: Optional custom filename. If empty, will be generated from company name.

    Returns:
        Dictionary with the saved file path and any notes.
    """
    try:
        # Parse JSON string
        data = json.loads(pitch_deck_data)

        # Extract company name for filename
        company_name = data.get("company_name", "startup")
        if not filename or not filename.strip():
            slug = _slugify(company_name)
            filename = f"{slug}_pitch_deck.pdf"
        else:
            # Ensure filename has .pdf extension
            filename = filename.strip()
            if not filename.endswith(".pdf"):
                filename = f"{filename}.pdf"

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        filepath = output_path / filename

        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set fonts
        pdf.set_font("Arial", "B", 20)
        
        # Title page
        pdf.cell(0, 20, company_name, ln=1, align="C")
        pdf.ln(5)
        
        tagline = data.get("tagline", "")
        if tagline:
            pdf.set_font("Arial", "", 14)
            pdf.cell(0, 10, _clean_bullets(tagline), ln=1, align="C")
        
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        elevator_pitch = data.get("elevator_pitch", "")
        if elevator_pitch:
            pdf.multi_cell(0, 6, _clean_bullets(elevator_pitch), ln=1, align="C")

        # Add sections
        sections = data.get("sections", [])
        for section in sections:
            pdf.add_page()
            title = _clean_bullets(section.get("title", ""))
            bullets = section.get("bullets", [])
            _add_section(pdf, title, bullets)

        # Add metrics snapshot
        metrics = data.get("metrics_snapshot", {})
        if metrics:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Key Metrics", ln=1)
            pdf.ln(5)
            
            for category, items in metrics.items():
                if items:
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, category.replace("_", " ").title(), ln=1)
                    pdf.set_font("Arial", "", 11)
                    for item in items:
                        if item:
                            cleaned_item = _clean_bullets(str(item))
                            pdf.cell(5, 6, "-", ln=0)
                            pdf.multi_cell(0, 6, cleaned_item, ln=1)
                            pdf.ln(1)
                    pdf.ln(3)

        # Add investment ask
        investment = data.get("investment_ask", {})
        if investment:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Investment Ask", ln=1)
            pdf.ln(5)
            
            pdf.set_font("Arial", "B", 12)
            amount = investment.get("amount", "")
            if amount:
                pdf.cell(0, 8, f"Amount: {amount}", ln=1)
                pdf.ln(2)
            
            use_of_funds = investment.get("use_of_funds", [])
            if use_of_funds:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Use of Funds:", ln=1)
                pdf.set_font("Arial", "", 11)
                for item in use_of_funds:
                    if item:
                        cleaned_item = _clean_bullets(str(item))
                        pdf.cell(5, 6, "-", ln=0)
                        pdf.multi_cell(0, 6, cleaned_item, ln=1)
                        pdf.ln(1)
                pdf.ln(2)
            
            milestones = investment.get("milestones", [])
            if milestones:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Milestones:", ln=1)
                pdf.set_font("Arial", "", 11)
                for item in milestones:
                    if item:
                        cleaned_item = _clean_bullets(str(item))
                        pdf.cell(5, 6, "-", ln=0)
                        pdf.multi_cell(0, 6, cleaned_item, ln=1)
                        pdf.ln(1)
                pdf.ln(2)
            
            timeline = investment.get("timeline", "")
            if timeline:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, f"Timeline: {_clean_bullets(timeline)}", ln=1)

        # Add call to action
        cta = data.get("call_to_action", "")
        if cta:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Next Steps", ln=1)
            pdf.ln(5)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 6, _clean_bullets(cta), ln=1)

        # Add risks/diligence
        risks = data.get("risks_or_diligence", [])
        if risks:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Risks & Diligence", ln=1)
            pdf.ln(5)
            pdf.set_font("Arial", "", 11)
            for risk in risks:
                if risk:
                    cleaned_risk = _clean_bullets(str(risk))
                    pdf.cell(5, 6, "-", ln=0)
                    pdf.multi_cell(0, 6, cleaned_risk, ln=1)
                    pdf.ln(1)

        # Save PDF
        pdf.output(str(filepath))

        return {
            "saved_file": str(filepath),
            "notes": ["PDF pitch deck generated successfully"],
        }

    except json.JSONDecodeError as e:
        return {
            "saved_file": "",
            "notes": [f"Failed to parse JSON: {str(e)}"],
        }
    except Exception as e:
        return {
            "saved_file": "",
            "notes": [f"PDF generation failed: {str(e)}"],
        }


pdf_generation_tool = FunctionTool(generate_pitch_deck_pdf)

