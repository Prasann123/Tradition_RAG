Example of when to use which type of  chunking mechanism

RecursiveCharacterTextSplitter might split like this:

Chunk 1: "Climate change is caused by greenhouse gases. These gases include CO2..."
Chunk 2: "...and methane. The effects of climate change include rising sea levels..."
SemanticChunker would try to keep related concepts together:

Chunk 1: "Climate change is caused by greenhouse gases. These gases include CO2 and methane." (complete section on causes)
Chunk 2: "The effects of climate change include rising sea levels..." (starts new chunk for effects)
When to Use Each
Use RecursiveCharacterTextSplitter: When processing speed matters, for simpler documents, or when you don't need semantic understanding
Use SemanticChunker: For complex documents with diverse topics, when preserving concept integrity is critical, and when processing time isn't a constrain