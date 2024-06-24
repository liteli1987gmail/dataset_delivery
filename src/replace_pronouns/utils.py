import os


import tiktoken
from icecream import ic
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .api import get_completion

MAX_TOKENS_PER_CHUNK = (
    1000  # if text is more than this many tokens, we'll break it up into
)
# discrete chunks to translate one chunk at a time


# 马斯克的新闻https://r.jina.ai/https://36kr.com/p/2776646712673414

def one_pronoun_replacement(
    text: str,country: str) -> str:
    """
    Replace personal pronouns in the provided text with corresponding names using an LLM.

    Args:
        text (str): The text containing pronouns to be replaced.
        country(str): The country name where the task begins.
    Returns:
        str: The text with pronouns replaced by corresponding names.
    """

    system_message = f"任务的最终目标是制作数据集,任务中涉及的内容均来自{country}，按照以下步骤进行思考和行动，最终将替换后的结果字符串填入到<modified text>标签中。let's think step by step."


    replacement_prompt = f"""
    <step1>制作数据集的时候，从网页中拉取新闻信息，将新闻信息中的人称代词转为人名、追加时间，
    以构成事实性的信息，比如时间、地点、人物名词、做了什么、获得了什么结果。
    请你将以下<Text>标签内的新闻帮我将代词转换的结果填入括号中。</step1>  
    <step2>将括号内的名词替换原来的代词或名字，使用<modified text> </modified text>标签包裹。</step2> 。
    step1和step2保持后台思考，不需输出思考的步骤或者结果，最终你输出<modified text> </modified text>标签内的内容。
    <Text>: 
    {text}
    </Text>
    <modified text>:"""

    prompt = replacement_prompt.format(text=text,country=country)

    # Assume get_completion is a function that sends the prompt to the LLM and returns the result
    modified_text = get_completion(prompt, system_message=system_message)
    
    return modified_text


def num_tokens_in_string(
    input_str: str, encoding_name: str = "cl100k_base"
) -> int:
    """
    Calculate the number of tokens in a given string using a specified encoding.

    Args:
        str (str): The input string to be tokenized.
        encoding_name (str, optional): The name of the encoding to use. Defaults to "cl100k_base",
            which is the most commonly used encoder (used by GPT-4).

    Returns:
        int: The number of tokens in the input string.

    Example:
        >>> text = "Hello, how are you?"
        >>> num_tokens = num_tokens_in_string(text)
        >>> print(num_tokens)
        5
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(input_str))
    return num_tokens

def replace_pronouns_names(
    source_text,
    country,
    max_tokens=MAX_TOKENS_PER_CHUNK,
):
    """Translate the source_text from source_lang to target_lang."""

    num_tokens_in_text = num_tokens_in_string(source_text)
    ic("计算文本的token数量：")
    ic(num_tokens_in_text)

    if num_tokens_in_text < max_tokens:
        ic("短小的文本，直接替换")

        final_translation = one_pronoun_replacement(
            source_text,country
        )

        return final_translation

