import re
import json
from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm
from datasets import load_dataset

DATASET_NAME = "natural_questions"
SPLITS = ["train", "validation"]

DATA_PATH = Path(__file__).parent / "data"


@dataclass
class Offset:
    start: int
    end: int

    def __contains__(self, item):
        if self.start <= item.start <= item.end <= self.end:
            return True
        return False


@dataclass
class Token:
    text: str
    is_html: bool = False
    start_byte: int = None
    end_byte: int = None

    def __post_init__(self):
        self.offset = Offset(self.start_byte, self.end_byte)


@dataclass
class Candidate:
    top_level: bool = False
    start_byte: int = None
    end_byte: int = None

    def __post_init__(self):
        self.offset = Offset(self.start_byte, self.end_byte)
        self.tokens = []

    @property
    def text(self):
        t = " ".join(tkn.text for tkn in self.tokens if not tkn.is_html)
        t = t.strip()
        t = re.sub(r" +", r" ", t)
        return t


@dataclass
class Entry:
    id: str
    document: dict
    question: dict
    long_answer_candidates: dict
    annotations: dict

    def __post_init__(self):
        self.tokens = [
            Token(tkn, is_html, s_byte, e_byte)
            for e_byte, is_html, s_byte, tkn in zip(*self.document["tokens"].values())
        ]

        self.candidates = [
            Candidate(top_level, s_byte, e_byte)
            for e_byte, _, s_byte, _, top_level in zip(*self.long_answer_candidates.values())
        ]

    def _build_document(self):
        n_chars = len(self.document["html"])
        chars = [" "] * n_chars
        for tkn in self.tokens:
            if not tkn.is_html:
                chars[tkn.offset.start: tkn.offset.end] = tkn.text
        document = "".join(chars).strip()
        document = re.sub(r" +", r" ", document)
        return document

    def _build_candidates(self):
        for candidate in self.candidates:
            for token in self.tokens:
                if token.offset in candidate.offset:
                    candidate.tokens.append(token)
        return [cand.text for cand in self.candidates]

    def format(self) -> dict:
        document = self._build_document()
        candidates = self._build_candidates()
        l_answer_id = self.annotations["long_answer"][0]["candidate_index"]
        short_answers = [answer["text"] for answer in self.annotations["short_answers"]]
        result = {
            "id": self.id,
            "question": self.question["text"],
            "document": document,
            "candidates": candidates,
            "long_answer": candidates[l_answer_id],
            "short_answers": short_answers,
            "yes_no_answer": self.annotations["yes_no_answer"]
        }
        return result


def main():
    nq = load_dataset(DATASET_NAME)
    for split in SPLITS:
        data = nq[split]

        split_path = DATA_PATH / split
        split_path.mkdir(exist_ok=True, parents=True)

        for entry in tqdm(data):
            result = Entry(**entry).format()
            opath = split_path / f"{result['id']}.json"
            json.dump(result, opath.open("w"), indent=4)


if __name__ == "__main__":
    main()
