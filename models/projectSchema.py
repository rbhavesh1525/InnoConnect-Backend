from pydantic import BaseModel, field_validator

MIN_WORDS = 5
MAX_WORDS = 500

TEXT_FIELDS = ["project_title", "description", "problem_statement", "solution_overview"]


def _count_words(text: str) -> int:
    return len(text.strip().split()) if text.strip() else 0


class ProjectSubmission(BaseModel):
    project_title: str
    description: str
    problem_statement: str
    solution_overview: str
    industry_category: str

    @field_validator("project_title", "description", "problem_statement", "solution_overview")
    @classmethod
    def validate_word_count(cls, value: str, info) -> str:
        wc = _count_words(value)
        field_label = info.field_name.replace("_", " ")
        if wc < MIN_WORDS:
            raise ValueError(
                f"'{field_label}' must have at least {MIN_WORDS} words (got {wc})."
            )
        if wc > MAX_WORDS:
            raise ValueError(
                f"'{field_label}' must have at most {MAX_WORDS} words (got {wc})."
            )
        return value

