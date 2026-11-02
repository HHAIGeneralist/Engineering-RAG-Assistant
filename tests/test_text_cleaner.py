from src.text_cleaner import clean_text

def test_clean_text_repairs_line_hyphenation():
    assert clean_text("engi-\nneering") == "engineering"
