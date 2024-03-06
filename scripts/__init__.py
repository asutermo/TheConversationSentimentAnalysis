from dataclasses import dataclass

@dataclass
class TextBlobArticleSentiment:
    title: str
    link: str
    polarity: float
    subjectivity: float
    text: str

    def __str__(self):
        return f"{self.title} - Polarity: {self.polarity}, Subjectivity: {self.subjectivity}"