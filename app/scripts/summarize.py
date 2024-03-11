from transformers import pipeline

# todo use transformers.js and/or langchain
def summarize_light(article_text: str) -> str:
    """Uses a fine-tuned T5 small for text summaries"""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    results = summarizer(article_text[:1024], max_length=1024, min_length=30, do_sample=False)
    print(results)
    return results[0]['summary_text']