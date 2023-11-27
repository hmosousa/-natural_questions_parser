# Natural Questions Parser

## Overview

This repository contains a script designed to parse the [Natural Questions](https://huggingface.co/datasets/natural_questions) dataset. The Natural Questions dataset comprises entries annotated with start and end byte offsets for each answer. Our script, `main.py`, performs two primary functions:

1. **Extraction**: It extracts content from the HTML page associated with each dataset entry.
2. **Transformation**: It transforms the annotations into a text format for easier accessibility and understanding.

## Example Transformation

The script converts entries in the dataset from their original format to a more friendly format. For example, the entry in `example.json` is transformed into the one presented below:

```json
{
    "id": "4549465242785278785",
    "question": "when is the last episode of season 8 of the walking dead",
    "document": "The Walking Dead (season 8) - Wikipedia The Walking Dead (...)",
    "candidates": [
        "The Walking Dead (season 8)",
        "Promotional poster",
        "(...)"
    ],
    "long_answer": "No. overall No. in season (...) March 18, 2018 (...)",
    "short_answers": [["March 18, 2018"]],
    "yes_no_answer": [-1]
}
```

## Usage Instructions

1. Clone the repository to your local machine.
2. Create a virtual environment: `python3.11 -m venv .venv`
3. Activate the environment: `source .venv/bin/activate`
4. Install dependencies: `pip install datasets==2.15.0`
5. Run the `main.py` script: `python main.py`

## Performance and Output

- **Runtime**: Please note that the script takes approximately one day to run, depending on your system's capabilities.
- **Output**: The results of the parsing are published on the [HuggingFace Hub](https://huggingface.co/datasets/hugosousa/natural_questions_parsed).

## Contributions and Issues

Contributions to this project are welcome! If you have suggestions for improvement or have identified issues, please submit a pull request or open an issue in this repository.
