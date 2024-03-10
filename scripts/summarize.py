from transformers import pipeline

# todo use transformers.js
def summarize_light(article_text: str) -> str:
    """Uses a fine-tuned T5 small for text summaries"""
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    results = summarizer(article_text[:512], max_length=512, min_length=30, do_sample=False)
    print(results)
    return results[0]['summary_text']