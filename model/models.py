from pydantic import BaseModel, Field, RootModel
from typing import List, Union, Optional, List, Dict, Any


class Metadata(BaseModel):
    Summary: List[str] = Field(default_factory=list, description="A brief summary of the document.")
    Title: str
    Author: str
    DateCreated: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]
    SentimentTone: str

class ChangeFormat(BaseModel):
    Page: str
    Change: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass
