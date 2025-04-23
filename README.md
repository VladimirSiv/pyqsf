# PyQSF

PyQSF is a lightweight Python wrapper for parsing Qualtrics Survey Files (`.qsf`). It helps you navigate survey structure, including questions, blocks, and flow.

> ⚠️ Note: Mapping is not fully implemented. You may need to extend functionality based on your specific use case and the types of survey elements involved. Contributions are welcome!

## How It Works

Survey elements like questions are returned in the logical order defined by the `Flow` and `Blocks` structure in the QSF file. For more information on how QSF file works check [Quickstart Guide to understanding the Qualtrics Survey File](https://gist.github.com/ctesta01/d4255959dace01431fb90618d1e8c241).

## Quick Example

```
from pyqsf import QualtricsSurveyFile

qsf = QualtricsSurveyFile("<path-to-qsf-file>")

# Iterate through questions
for question in qsf.questions:
    print(question.description)
    print(question.id)
    # Attributes vary depending on question type

# Iterate through blocks
for block in qsf.blocks: # Process each block
    pass
```
