def have_tail(text: str) -> bool:
    tails_characters = {
    'g', 'j', 'p', 'q', 'y',  # Lowercase letters with tails
    '₲', '₭', '₿',  # Currency symbols with tails (example)
    'ƒ', '₣', '₰',  # Other symbols with tails (example)
    '↙', '↧', '↲',  # Arrows and other symbols (example)
    }
    for letter in text:
        if letter in tails_characters:
            return True
    return False