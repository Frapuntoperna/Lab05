import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    contatore = ft.Text(value='0')

    def diminuisci(e):
        if int(contatore.value) > 0:
            contatore.value = str(int(contatore.value)-1)
            contatore.update()

    def aumenta(e):
        contatore.value = str(int(contatore.value)+1)
        contatore.update()

    testo_tipo = ft.TextField('tipo strumento')
    testo_marca = ft.TextField('marca strumento')
    testo_anno = ft.TextField('anno strumento')

    testo_meno = ft.IconButton(icon=ft.Icons.REMOVE,
                                on_click = diminuisci,
                                bgcolor='red'
                                )

    testo_piu = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click = aumenta,
        bgcolor = 'green'
        )



    riga_testo_inserimento_strumento=ft.Row([testo_tipo, testo_marca, testo_anno, testo_meno, contatore, testo_piu])

    def aggiungi_nuovo_strumento(e):
        if testo_tipo.value.strip()!='':
            tipo = str(testo_tipo.value.strip())
        else:
            raise alert.show_alert("❌ Il tipo di strumento deve essere valido.")

        if testo_marca.value.strip()!='':
            marca = str(testo_marca.value.strip())
        else:
            raise alert.show_alert("❌ La marca dello strumento deve essere valida.")

        try:
            anno = int(testo_anno.value.strip())
            if anno<10:
                raise alert.show_alert("❌ L'anno dello strumento deve essere valido.")
        except ValueError:
            alert.show_alert("❌ L'anno di acquisto deve essere un valore numerico valido.")
            return

        if contatore.value.strip()!='0':
            valore= int(contatore.value.strip())
        else:
            raise alert.show_alert("❌ Il valore dello strumento deve essere valido.")

        deposito.aggiungi_strumento(tipo, marca, anno, valore)

        testo_tipo.value=''
        testo_marca.value=''
        testo_anno.value=''
        contatore.value='0'

        aggiorna_lista_strumenti()
        page.update()

    bottone_aggiungi_strumento = ft.ElevatedButton('Aggiungi strumento',
                                           on_click=aggiungi_nuovo_strumento
                                           )

    riga_bottone = ft.Row([bottone_aggiungi_strumento],
                          alignment=ft.MainAxisAlignment.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text('aggiungi nuovo strumento', size=20),
        riga_testo_inserimento_strumento,
        riga_bottone,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
