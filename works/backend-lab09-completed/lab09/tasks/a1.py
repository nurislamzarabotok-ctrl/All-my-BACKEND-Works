# A1 · Optional, null, required. Run: python check.py a1
from pydantic import BaseModel, ConfigDict, ValidationError


class PatchA(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = None


class PatchB(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None


class PatchC(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = ""


def check() -> None:
    bodies = [{}, {"text": None}, {"txt": "hi"}]
    print(f"{'':8}{'{}':10}{'{\"text\": null}':18}{'{\"txt\": \"hi\"}':16}")
    for model in (PatchA, PatchB, PatchC):
        row = []
        for body in bodies:
            try:
                model(**body)
                row.append("OK")
            except ValidationError:
                row.append("422")
        print(f"{model.__name__[-1]:8}{row[0]:10}{row[1]:18}{row[2]:16}")
