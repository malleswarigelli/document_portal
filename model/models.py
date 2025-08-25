from pydantic import BaseModel, Field
from typing import List, Union


class Metadata(BaseModel):
    Summary: List[str] = Field(default_factory=list, description="A brief summary of the document.")
    Title: str
    Author: str
    DateCreated: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]
    SentimentTone: str
