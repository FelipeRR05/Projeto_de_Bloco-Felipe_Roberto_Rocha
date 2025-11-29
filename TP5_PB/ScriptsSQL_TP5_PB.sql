BEGIN;

-- 1. Tabela de Metadados
CREATE TABLE Scraping_Metadata (
    meta_id SERIAL PRIMARY KEY,
    target_url TEXT NOT NULL,
    access_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_code INTEGER
);

-- 2. Tabela de Dados
CREATE TABLE Scraping_Data (
    data_id SERIAL PRIMARY KEY,
    meta_id INTEGER,
    info_key TEXT,
    info_value TEXT,
    FOREIGN KEY (meta_id) REFERENCES Scraping_Metadata(meta_id)
);

-- 3. Tabela de Erros
CREATE TABLE Scraping_Errors (
    error_id SERIAL PRIMARY KEY,
    target_url TEXT,
    error_message TEXT,
    error_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

END;