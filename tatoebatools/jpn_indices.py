import csv
import logging

from .config import DATA_DIR
from .utils import lazy_property
from .version import Version

logger = logging.getLogger(__name__)


class JpnIndices:
    """Equivalent of the "B lines" in the Tanaka Corpus file distributed 
    by Jim Breen. For more info see:
    https://www.edrdg.org/wiki/index.php/Tanaka_Corpus#Current_Format_.28WWWJDIC.29 
    Each entry is associated with a pair of Japanese/English sentences. 
    """

    _table = "jpn_indices"
    _filename = f"jpn_{_table}.tsv"
    _dir = DATA_DIR.joinpath(_table)
    _path = _dir.joinpath(_filename)

    def __iter__(self):

        try:
            with open(self.path) as f:
                fieldnames = [
                    "sentence_id",
                    "meaning_id",
                    "text",
                ]

                rows = csv.DictReader(
                    f, delimiter="\t", escapechar="\\", fieldnames=fieldnames
                )
                for row in rows:
                    yield JpnIndex(**row)
        except OSError:
            msg = (
                f"no data locally available for the "
                f"'{JpnIndices._table}' table."
            )

            logger.warning(msg)

    @property
    def filename(self):
        """Get the name of the datafile.
        """
        return JpnIndices._filename

    @property
    def path(self):
        """Get the path of the datafile.
        """
        return JpnIndices._path

    @lazy_property
    def version(self):
        """Get the version of the downloaded data of these sentences.
        """
        with Version() as vs:
            return vs[self.filename]


class JpnIndex:
    """Each entry is associated with a pair of Japanese/English sentences. 
    """

    def __init__(self, sentence_id, meaning_id, text):
        # sentence_id refers to the id of the Japanese sentence.
        self._sid = sentence_id
        # meaning_id refers to the id of the English sentence.
        self._mid = meaning_id
        #
        self._txt = text

    @property
    def sentence_id(self):
        """Get the id of the Japanese sentence. 
        """
        return int(self._sid)

    @property
    def meaning_id(self):
        """Get the id of the English sentence. 
        """
        return int(self._mid)

    @property
    def text(self):
        """Get the text of the entry. 
        """
        return self._txt
