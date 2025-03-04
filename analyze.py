import connection
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Função para buscar dados
def fetch_data(sql):
    conn = connection.conn()  # Conectar ao banco de dados
    read = pd.read_sql(sql, conn)  # Ler dados SQL no pandas DataFrame
    conn.close()  # Fechar conexão
    return read

def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    return "break"

# Consultas SQL
sql_seller = "SELECT SELLER_CITY, SELLER_STATE, COUNT(*) AS total FROM SELLER GROUP BY SELLER_STATE"
df_seller = fetch_data(sql_seller)

sql_customer = "SELECT CUSTOMER_CITY, CUSTOMER_STATE, COUNT(*) AS total FROM CUSTOMERS GROUP BY CUSTOMER_STATE"
df_customer = fetch_data(sql_customer)

sql_products =  """
                    SELECT OI.ORDERS_ID, P.PRODUCT_CATEGORY_NAME, COUNT(*) AS total
                    FROM ORDERS_ITENS OI
                    INNER JOIN PRODUCTS P ON OI.PRODUCT_ID = P.PRODUCT_ID
                    GROUP BY OI.ORDERS_ID
                    HAVING total > 9
                    AND PRODUCT_CATEGORY_NAME != "";
                """

df_products = fetch_data(sql_products)  # Evitar sobrescrição de df_customer

# Configuração da janela principal
root = tk.Tk()
root.title("Análise de Dados Simples")
root.attributes('-fullscreen', True)
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Criar as abas
nav = ttk.Notebook(root)
frame_bar = ttk.Frame(nav)
frame_pie = ttk.Frame(nav)
frame_table = ttk.Frame(nav)

nav.add(frame_bar, text="Gráfico de Barras")
nav.add(frame_pie, text="Gráfico de Pizza")
nav.add(frame_table, text="Lista de Cidades")
nav.pack(expand=True, fill="both")
root.bind("<F11>", toggle_fullscreen)

# Gráfico de Barras
# Gráfico Vendedores
fig1, ax1 = plt.subplots(figsize=(6, 4))
ax1.bar(df_seller["SELLER_STATE"], df_seller["total"], color="blue")
ax1.set_title("Vendedores")
ax1.set_xlabel("Estado")
ax1.set_ylabel("Número de Vendedores")
ax1.tick_params(axis='x', rotation=45)

# Gráfico Clientes
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.bar(df_customer["CUSTOMER_STATE"], df_customer["total"], color="green")
ax2.set_title("Clientes")
ax2.set_xlabel("Estado")
ax2.set_ylabel("Número de Clientes")
ax2.tick_params(axis='x', rotation=45)

canvas1 = FigureCanvasTkAgg(fig1, master=frame_bar)
canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas1.draw()
canvas2 = FigureCanvasTkAgg(fig2, master=frame_bar)
canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas2.draw()

#Gráfico Pizza
fig3, ax3 = plt.subplots(figsize=(6,4))
ax3.pie(df_products["total"], labels=df_products['PRODUCT_CATEGORY_NAME'], autopct = '%1.1f%%', startangle=90)
ax3.set_title('Lista das melhores vendas por categoria de produtos')

canvas3 = FigureCanvasTkAgg(fig3, master=frame_pie)
canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas3.draw()

#Lista de Cidades dos vendedores
tree = ttk.Treeview(frame_table, columns=("Cidade", "Estado", "Total"), show="headings")
tree.heading("Cidade", text="Cidade")
tree.heading("Estado", text="Estado")
tree.heading("Total", text="Total de Vendedores")
tree.column("Cidade", width=250)
tree.column("Estado", width=100)
tree.column("Total", width=100)


for index, row in df_seller.iterrows():
    tree.insert("", "end", values=(row["SELLER_CITY"], row["SELLER_STATE"], row["total"]))

tree.pack(fill=tk.BOTH, expand=True)

button = ttk.Label(frame, text="Aperte f11 para ajustar a tela")
button.pack()
root.mainloop()