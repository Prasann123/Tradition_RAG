from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter

def get_parser(config: dict):
    """Builds a text splitter (parser) based on the config. Used for document ingestion."""
    parser_type = config.get("parser_type", "recursive")
    chunk_size = int(config.get("chunk_size", 1000))
    chunk_overlap = int(config.get("chunk_overlap", 100))

    if parser_type == "simple":
        return CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    else:
        return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)