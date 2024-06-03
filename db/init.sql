CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Create table to store products
CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price INTEGER NOT NULL,
  stock INTEGER NOT NULL,
  rating REAL NOT NULL DEFAULT 0,
  tsv tsvector DEFAULT NULL
)

-- Create tsvector index
CREATE INDEX IF NOT EXISTS tsv_idx ON products USING GIN (tsv);

-- Update tsvector when product name changes
CREATE FUNCTION update_tsvector() RETURNS trigger AS $$
BEGIN
  NEW.tsv := to_tsvector('simple', unaccent(NEW.name));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON products FOR EACH ROW EXECUTE FUNCTION update_tsvector();

-- Create table to store documents embeddings
CREATE TABLE IF NOT EXISTS documents (
  id uuid primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector (1536) -- 1536 works for OpenAI embeddings, change if needed
);

-- Create a function to search for documents
create function document_match (
  query_embedding vector (1536),
  filter jsonb default '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding;
end;
$$;