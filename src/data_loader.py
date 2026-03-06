from langchain_text_splitters import MarkdownHeaderTextSplitter

def data_loader(data):
  with open(data, encoding='utf-8') as f:
    resume = f.read()

  headers_to_split_on = [
      (r"\#", "Header_1"),
      (r"\##", "Header_2"),
  ]

  markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

  md_headers_splits = markdown_splitter.split_text(resume)
  return md_headers_splits
