CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price INTEGER NOT NULL,
  stock INTEGER NOT NULL,
  rating REAL NOT NULL DEFAULT 0,
  tsv tsvector DEFAULT NULL
);

CREATE INDEX IF NOT EXISTS tsv_idx ON products USING GIN (tsv);

CREATE FUNCTION update_tsvector() RETURNS trigger AS $$
BEGIN
  NEW.tsv := to_tsvector('simple', unaccent(NEW.name));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON products FOR EACH ROW EXECUTE FUNCTION update_tsvector();

CREATE TABLE IF NOT EXISTS documents (
  id uuid primary key,
  content text,
  metadata jsonb,
  embedding vector (1536)
);

CREATE FUNCTION IF NOT EXISTS document_match (
  query_embedding vector (1536),
  FILTER jsonb default '{}'
) RETURNS TABLE (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
  RETURN query
  SELECT
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE metadata @> FILTER
  ORDER BY documents.embedding <=> query_embedding;
END;
$$;