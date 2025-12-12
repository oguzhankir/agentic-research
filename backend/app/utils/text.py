import re

def clean_json_response(content: str) -> str:
    """
    Cleans LLM output to extract just the JSON part.
    Removes markdown code blocks likes ```json ... ```.
    """
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    return content.strip()

def clean_html_response(content: str) -> str:
    """
    Cleans LLM output to extract just the HTML part.
    Removes markdown code blocks likes ```html ... ```.
    """
    if "```html" in content:
        content = content.replace("```html", "").replace("```", "")
    elif "```" in content:
        content = content.replace("```", "")
    return content.strip()
