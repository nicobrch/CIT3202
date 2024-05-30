# Use the official PostgreSQL image from the Docker Hub
FROM postgres:14

# Environment variables to set the default PostgreSQL user and database
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=datasciencea

# Install necessary packages and the pgvector extension
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-14

RUN git clone https://github.com/pgvector/pgvector.git /usr/src/pgvector \
    && cd /usr/src/pgvector \
    && make \
    && make install

# Clean apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the SQL script to initialize the database
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Expose port
EXPOSE 5432