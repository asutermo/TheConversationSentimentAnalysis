from dataclasses import dataclass

@dataclass
class TextBlobArticleSentiment:
    title: str
    polarity: float
    subjectivity: float

    def __str__(self):
        return f"{self.title} - Polarity: {self.polarity}, Subjectivity: {self.subjectivity}"