import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
import datetime
import re

DATABASE_URL = "postgresql://postgres:Rroch%402019@localhost/gymlog_db"
URL_ALVO = "https://pt.wikipedia.org/wiki/Club_de_Regatas_Vasco_da_Gama"

def get_connection():
    try:
        engine = create_engine(DATABASE_URL)
        return engine.connect()
    except Exception as e:
        print(f"Erro fatal de conexão: {e}")
        return None

def clean_text(text_content):
    if not text_content: return ""
    clean = re.sub(r'\[.*?\]', '', text_content)
    clean = clean.replace('\n', ' ').replace('\xa0', ' ')
    return clean.strip()

def run_scraper():
    conn = get_connection()
    if not conn: return
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} 
        req = urllib.request.Request(URL_ALVO, headers=headers)
        
        status_code = 0
        html_content = ""
        
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            html_content = response.read().decode('utf-8')

        insert_meta_sql = text("""
            INSERT INTO Scraping_Metadata (target_url, status_code, access_timestamp)
            VALUES (:url, :status, :time)
            RETURNING meta_id;
        """)
        
        result = conn.execute(insert_meta_sql, {
            'url': URL_ALVO, 
            'status': status_code,
            'time': datetime.datetime.now()
        })
        current_meta_id = result.fetchone()[0]
        conn.commit()

        soup = BeautifulSoup(html_content, 'html.parser')
        
        all_tables = soup.find_all('table')
        target_table = None
        
        for table in all_tables:
            table_text = table.get_text()
            if "Alcunhas" in table_text or "Mascote" in table_text or "Fundação" in table_text:
                target_table = table
                break
        
        if not target_table:
            target_table = soup.find('table', class_='infobox vcard')

        if not target_table:
            raise Exception("Não foi possível encontrar a tabela de dados.")

        extracted_data = []
        rows = target_table.find_all('tr')
        
        for row in rows:
            header = row.find('th')
            value = row.find('td')
            
            if header and value:
                key_text = clean_text(header.get_text())
                val_text = clean_text(value.get_text())
                
                if key_text and val_text and len(key_text) < 50:
                    extracted_data.append({
                        'meta_id': current_meta_id,
                        'key': key_text[:100], 
                        'val': val_text[:200]
                    })
            
            elif not header:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    key_text = clean_text(cells[0].get_text())
                    val_text = clean_text(cells[1].get_text())
                    if key_text and val_text and len(key_text) < 50:
                        extracted_data.append({
                            'meta_id': current_meta_id,
                            'key': key_text[:100], 
                            'val': val_text[:200]
                        })

        if extracted_data:
            insert_data_sql = text("""
                INSERT INTO Scraping_Data (meta_id, info_key, info_value)
                VALUES (:meta_id, :key, :val)
            """)
            conn.execute(insert_data_sql, extracted_data)
            conn.commit()
        else:
            print(">>> Aviso: A tabela foi encontrada, mas a extração falhou. O layout do HTML pode ser muito complexo.")

    except Exception as e:
        print(f">>> ERRO: {e}")
        conn.rollback()
        try:
            conn.execute(text("INSERT INTO Scraping_Errors (target_url, error_message) VALUES (:u, :m)"), 
                         {'u': URL_ALVO, 'm': str(e)})
            conn.commit()
        except:
            pass
    
    finally:
        conn.close()

def generate_report():
    conn = get_connection()
    if not conn: return

    print("\n" + "="*30)
    print("Relatório final da página:")
    print("="*30)

    query_report = text("""
        SELECT D.info_key, D.info_value
        FROM Scraping_Metadata AS M
        INNER JOIN Scraping_Data AS D ON M.meta_id = D.meta_id
        WHERE M.target_url = :url
        ORDER BY M.access_timestamp DESC, D.data_id ASC
        LIMIT 20;
    """)

    result = conn.execute(query_report, {'url': URL_ALVO})
    rows = result.fetchall()

    if rows:
        for row in rows:
            print(f"{row.info_key}: {row.info_value}")
    else:
        print("Nenhum dado para exibir.")

    conn.close()

if __name__ == "__main__":
    run_scraper()
    generate_report()