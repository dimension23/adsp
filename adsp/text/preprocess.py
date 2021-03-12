import re
import unicodedata
import contractions
from typing import List
from spacy.lang.en import stop_words as spacy_en_stopwords
import warnings

warnings.filterwarnings("ignore")


class TextCleaner:
    def __init__(
        self,
        remove_custom_chars: bool = False,
        remove_urls: bool = True,
        remove_html_tags: bool = True,
        remove_diacritics: bool = True,
        remove_digits: bool = False,
        remove_digit_blocks: bool = False,
        fix_contractions: bool = True,
        remove_special_chars: bool = True,
        remove_stopwords: bool = False,
        remove_whitespaces: bool = True,
        lowercase: bool = True,
    ):
        self.custom_chars: List[str] = ["_x000d_", "\\xa0"]
        self.special_chars_pattern: str = "[^A-Za-z0-9.,?_@\n]+"
        self.stop_words: List[str] = spacy_en_stopwords.STOP_WORDS
        self.remove_custom_chars = remove_custom_chars
        self.remove_urls = remove_urls
        self.remove_html_tags = remove_html_tags
        self.remove_diacritics = remove_diacritics
        self.remove_digits = remove_digits
        self.remove_digit_blocks = remove_digit_blocks
        self.fix_contractions = fix_contractions
        self.remove_special_chars = remove_special_chars
        self.remove_stopwords = remove_stopwords
        self.remove_whitespaces = remove_whitespaces
        self.lowercase = lowercase

    def _remove_custom_chars(self, text: str) -> str:
        """
        Removes charracters listed in self.custom_chars
        """
        patterns = "|".join([x for x in self.custom_chars])
        return re.sub(patterns, "", str(text), flags=re.IGNORECASE)

    def _remove_urls(self, text: str) -> str:
        """
        Removes strings starting with http
        """
        pattern = r"http\S+"
        return re.sub(pattern, " ", str(text))

    def _remove_html_tags(self, text: str) -> str:
        """
        Removes html tags and other related elements
        """
        pattern = r"""
        (?x)                                          # Turn on free-spacing
        <[^>]+>                                       # Remove <html> tags
        | &([a-z0-9]+|\#[0-9]{1,6}|\#x[0-9a-f]{1,6}); # Remove &nbsp;
        """
        return re.sub(pattern, " ", str(text))

    def _remove_diacritics(self, text: str) -> str:
        """
        Replaces accents with plain alphabets
        """
        nfkd_form = unicodedata.normalize("NFKD", text)
        return "".join([char for char in nfkd_form if not unicodedata.combining(char)])

    def _remove_digits(self, text: str) -> str:
        """
        Removes any occurence of digits from the text
        Example: "7th Street" becomes "th Street"
        """
        return re.sub(r"\d+", " ", str(text))

    def _remove_digit_blocks(self, text: str) -> str:
        """
        Removes isolated block of digits
        Example: "Transferred 60 files" becomes "Transferred files"
        """
        return re.sub(r"\b\d+\b", " ", str(text))

    def _fix_contractions(self, text: str) -> str:
        """
        Expands contractions
        Example: "won't" becomes "would not"
        """
        try:
            return contractions.fix(str(text))
        except:
            return ""

    def _remove_special_chars(self, text: str) -> str:
        """
        Removes special characters as defined by the pattern in self.special_chars_pattern
        """
        pattern = re.compile(self.special_chars_pattern)
        text = re.sub(pattern, " ", text)
        return text

    def _remove_left_padded_special_chars(self, text: str) -> str:
        """
        Removes special charaters with whitespace on left
        Example: "apples , oranges, mangoes" becomes "apples oranges, mangoes"
        """
        pattern = re.compile("\ +[^A-Za-z0-9\n]")
        text = re.sub(pattern, " ", text)
        return text

    def _remove_stopwords(self, text: str) -> str:
        """
        Removes stopwords as defined by self.stop_words
        """
        pattern = r"""
        (?x)                                      # Set flag to allow verbose regexps
        \w+(?:-\w+)*                              # Words with optional internal hyphens 
        | \s*                                     # Any space
        | [][!"#$%&'*+,-./:;<=>?@\\^():_`{|}~]    # Any symbol 
        """
        symbol = " "
        return "".join(
            t if t not in self.stop_words else symbol for t in re.findall(pattern, text)
        )

    def _remove_whitespaces(self, text: str) -> str:
        """
        Removes tabs, newlines and any kind of space characters
        """
        return " ".join(re.sub("\xa0", " ", str(text)).split())

    def _lowercase(self, text: str) -> str:
        """
        Lowercase all text
        """
        return str(text).lower()

    def _remove_extra_whitespaces(self, text: str) -> str:
        """
        Reduces multiple whitespaces to single whitespace
        """
        return re.sub(" +", " ", text)

    def clean(self, text):
        text = self._fix_contractions(text) if self.fix_contractions else text
        text = self._remove_custom_chars(text) if self.remove_custom_chars else text
        text = self._remove_urls(text) if self.remove_urls else text
        text = self._remove_html_tags(text) if self.remove_html_tags else text
        text = self._remove_diacritics(text) if self.remove_diacritics else text
        text = self._remove_digits(text) if self.remove_digits else text
        text = self._remove_digit_blocks(text) if self.remove_digit_blocks else text
        text = self._remove_special_chars(text) if self.remove_special_chars else text
        text = self._lowercase(text) if self.lowercase else text
        text = self._remove_stopwords(text) if self.remove_stopwords else text
        text = self._remove_whitespaces(text) if self.remove_whitespaces else text
        text = self._remove_left_padded_special_chars(text)
        text = self._remove_extra_whitespaces(text)
        return text.strip()
