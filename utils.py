from sqlalchemy import create_engine

# engine para consultas no banco de dados
conn = create_engine('mssql+pyodbc://@localhost/ContosoRetailDW?driver=ODBC+Driver+17+for+SQL+Server')