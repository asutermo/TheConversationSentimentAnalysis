from dataclasses import dataclass

@dataclass
class ArticleSentiment:
    title: str
    link: str
    polarity: float
    subjectivity: float
    text: str = None
    summarization: str = None

    def __str__(self):
        return f"{self.title} - Polarity: {self.polarity}, Subjectivity: {self.subjectivity}"