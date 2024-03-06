from transformers import pipeline


def summarize(article_text: str) -> str:
    """Uses a fine-tuned T5 small for text summaries"""
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    results = summarizer(article_text, max_length=1000, min_length=30, do_sample=False)
    print(results)
    return results[0].summary_text