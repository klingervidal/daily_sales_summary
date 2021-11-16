import sys
import PySimpleGUI as sg
import csv_analyser


sg.theme("DarkTeal10")


def create_main_window():
    layout = [
        [   
            sg.Text("Selecione o seu arquivo CSV"),
            sg.In(key="-FILE-"),
            sg.FileBrowse("Selecionar", file_types=(("ALL files", "*.csv"),))
        ],
        [
            sg.Text("")
        ],
        [
            sg.Button("Analisar dados de vendas", key="-START-", size=(20,1), button_color=('white', 'SeaGreen4')),
            sg.Button("Finalizar Programa", key="-FINISH-", size=(20,1), button_color=('white', 'firebrick4'))
        ]
    ]

    window = sg.Window("Análise de Dados de Vendas", layout)

    return window


def create_second_window(filepath):
    sales = csv_analyser.analyse(filepath, 'df')

    list_sales = sales.values.tolist()

    sales_analisys = csv_analyser.analyse(filepath, 'dict')

    wrost_qty_sales = sales[sales["Count Sale"] == sales_analisys['min_qty']['value']]["Date"]
    wrost_qty_sales = wrost_qty_sales.values.tolist()

    best_qty_sales = sales[sales["Count Sale"] == sales_analisys['max_qty']['value']]["Date"]
    best_qty_sales = best_qty_sales.values.tolist()

    layout = [
        [   
            sg.Text("Vendas no Período Selecionado:")
        ],
        [   
            sg.Table(values=list_sales, headings=['Data', 'Total em Vendas', 'Quantidade de Vendas', 'Valor Médio por Venda', 'Maior Venda do Dia', 'Menor Venda do Dia'], num_rows=min(20, len(list_sales)))
        ],
        [
            sg.Text("")
        ],
        [
            sg.Text(f"Dia com pior valor total em vendas: {sales_analisys['min_value']['data']}, com {sales_analisys['min_value']['value']}")
        ],
        [
            sg.Text(f"Dia com melhor valor total em vendas: {sales_analisys['max_value']['data']}, com {sales_analisys['max_value']['value']}")
        ],
        [
            sg.Text(f"Dia(s) com pior quantidade total de vendas: {wrost_qty_sales}, com {sales_analisys['min_qty']['value']} venda(s) cada dia")
        ],
        [
            sg.Text(f"Dia(s) com melhor quantidade total de vendas: {best_qty_sales}, com {sales_analisys['max_qty']['value']} venda(s) cada dia")
        ],
        [
            sg.Text("")
        ],
        [   
            sg.Button("Voltar", key="-BACK-", button_color=('white', 'orange')),
            sg.Button("Finalizar Programa", key="-FINISH-", button_color=('white', 'firebrick4'))
        ]
    ]

    window = sg.Window("Análise de Dados de Vendas", layout, location=(200,20), size=(1025,700))

    return window

main_window = create_main_window()
active_window = main_window

# Managing windows
while True:
    event, values = active_window.read()

    if event == "-START-":
        main_window.hide()
        active_window = create_second_window(values["-FILE-"])
    
    elif event == "-BACK-":
        active_window.hide()
        active_window = create_main_window()
    
    elif event == "-FINISH-":
        active_window.close()

    # Closes if the user requires the window to close
    if event == sg.WIN_CLOSED:
        break