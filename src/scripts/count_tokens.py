"""
      Called at summarizer.py

"""
import tiktoken


def count_num_tokens(text, model) -> int:
    """
    Returns the number of tokens in the given text.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
