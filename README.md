# Awesome Data Science Package

This package features easy to use data processing routines.

## Usage

```python
from from adsp.text.preprocess import TextCleaner
text_cleaner = TextCleaner(remove_urls=True,
                           lowercase=True,
                           remove_special_chars=True,
                           remove_digit_blocks=False,
                           remove_whitespaces=True,
                           fix_contractions=True)
text_cleaner.clean("""<b>This is as easy as 123&nbsp;</b> Isn't it?""")
# Output: 'this is as easy as 123 is not it?'
```

There is more, you can remove diacritics, stopwords, html tags, etc.
In addition, you can also specify custom special character pattern in regex or as a list of characters.
