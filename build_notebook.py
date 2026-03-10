import json
import os

with open("quiz_generation.py", "r", encoding="utf-8") as f:
    quiz_code = f.read()

with open("main.py", "r", encoding="utf-8") as f:
    main_code = f.read()

with open("evaluate_models.py", "r", encoding="utf-8") as f:
    eval_code = f.read()

notebook = {
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# Text Summarization and Automated Quizzes Ecosystem\n",
        "This notebook unifies the pipeline to save all modeling artifacts and generated resources to the `output/` directory.\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [
        "import os\n",
        "os.makedirs('output', exist_ok=True)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["## Step 1: Question & Flashcard Generation"]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [line + "\n" for line in quiz_code.split("\n")]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["## Step 2: FastAPI Backend (Main) API"]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [line + "\n" for line in main_code.split("\n")]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["## Step 3: Benchmark & Evaluation"]
    },
    {
      "cell_type": "code",
      "execution_count": None,
      "metadata": {},
      "outputs": [],
      "source": [line + "\n" for line in eval_code.split("\n")]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {"name": "ipython", "version": 3},
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.10.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}

with open("code.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("code.ipynb successfully generated!")
