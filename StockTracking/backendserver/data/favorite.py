from sqlalchemy import create_engine
import sqlite3

# define database engines
sqlite_engine = create_engine(
    'sqlite:///database.db',
    convert_unicode=True,
    echo=True
)
# conn = sqlite3.connect('StockTracking/database.db')
# cursor = conn.cursor()


def add_favorite(id, ticker):
    create_favorite_db = """
    CREATE TABLE IF NOT EXISTS favorite(
       id INTEGER,
       favorite_stock VARCHAR(5),
       PRIMARY KEY (id, favorite_stock),
       FOREIGN KEY (id) REFERENCES user(id)
    )
    """
    cursor.execute(create_favorite_db)

    add_favorite_stock = """
    INSERT INTO favorite (id, favorite_stock)
    VALUES({__id__}, '{__ticker__}')
    """
    cursor.execute(add_favorite_stock.format(__id__=id, __ticker__=ticker))
    conn.commit()


def read_favorite(id):
    read_favorite_stock = """
    SELECT * 
    FROM favorite
    WHERE id = {__id__}
    """
    ticker = []
    q_results = cursor.execute(read_favorite_stock.format(__id__=id))
    for res in q_results:
        ticker.append(res[1])
    return ticker


if __name__ == '__main__':
    # conn = sqlite3.connect('../../database.db')
    # cursor = conn.cursor()
    # add_favorite(11, 'MSFT')
    # print(read_favorite(11))
    pass