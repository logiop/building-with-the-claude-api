# Importa la funzione load_dotenv dal modulo dotenv
# Serve per leggere le variabili d'ambiente dal file .env
from dotenv import load_dotenv

# Importa il modulo os per accedere alle variabili d'ambiente
import os

# Carica le variabili d'ambiente dal file .env nella memoria del programma
# Questo rende disponibile ANTHROPIC_API_KEY senza doverla scrivere nel codice
load_dotenv()

# Importa la classe Anthropic dal modulo anthropic
# Questa classe permette di comunicare con l'API di Claude
from anthropic import Anthropic

# Crea un'istanza del client Anthropic
# Utilizza automaticamente la variabile d'ambiente ANTHROPIC_API_KEY per autenticarsi
client = Anthropic()

# Specifica quale modello di Claude vogliamo usare
# In questo caso usiamo Claude Sonnet 5 (veloce e efficiente)
model = "claude-sonnet-5"


# FUNZIONE: get_text_content
# Scopo: estrarre il testo dalla risposta di Claude
# Perché?: Claude Sonnet 5 può restituire diversi tipi di blocchi (text, thinking, etc.)
# Questa funzione estrae solo il testo, ignorando i "thinking blocks"
def get_text_content(response):
    # response è un oggetto che contiene la risposta di Claude

    # for block in response.content:
    # Cicla attraverso ogni blocco (block) nella risposta di Claude
    # response.content è una lista di blocchi che Claude ha inviato
    for block in response.content:

        # if block.type == "text":
        # Controlla se il tipo di blocco è "text" (testo)
        # Ignora altri tipi come "thinking" (i pensieri interni di Claude)
        if block.type == "text":

            # return block.text
            # Restituisce il testo del blocco e esce dalla funzione
            # Usiamo return perché vogliamo il primo blocco di testo trovato
            return block.text

    # return ""
    # Se non trova nessun blocco di tipo "text", restituisce una stringa vuota
    # Questo evita errori se la risposta non contiene testo
    return ""


# FUNZIONE: main
# Scopo: gestire la conversazione interattiva tra l'utente e Claude
def main():

    # messages = []
    # Crea una lista vuota per salvare la cronologia della conversazione
    # Ogni messaggio sarà un dizionario con "role" (user/assistant) e "content" (testo)
    messages = []

    # print("🤖 Chat con Claude (scrivi 'exit' per uscire)\n")
    # Stampa un messaggio di benvenuto con emoji
    # \n aggiunge una riga vuota dopo il messaggio
    print("🤖 Chat con Claude (scrivi 'exit' per uscire)\n")

    # while True:
    # Crea un ciclo infinito che continua finché l'utente non digita "exit"
    while True:

        # user_input = input("You: ").strip()
        # input("You: ") legge quello che l'utente digita da tastiera
        # .strip() rimuove gli spazi bianchi all'inizio e alla fine (es: "  ciao  " diventa "ciao")
        # user_input ora contiene il testo digitato dall'utente
        user_input = input("You: ").strip()

        # if user_input.lower() == "exit":
        # Controlla se l'utente ha digitato "exit" (indipendentemente da maiuscole/minuscole)
        # .lower() converte il testo in minuscolo per il confronto (EXIT, Exit, exit diventano tutti "exit")
        if user_input.lower() == "exit":

            # print("Goodbye! 👋")
            # Stampa un messaggio di arrivederci
            print("Goodbye! 👋")

            # break
            # Esce dal ciclo while e termina il programma
            break

        # if not user_input:
        # Controlla se l'utente ha digitato qualcosa
        # Se la stringa è vuota (l'utente ha solo premuto Enter), "not user_input" è True
        if not user_input:

            # continue
            # Salta il resto del ciclo e ricomincia da capo
            # Ignora i messaggi vuoti
            continue

        # messages.append({"role": "user", "content": user_input})
        # Aggiunge il messaggio dell'utente alla lista di cronologia
        # "role": "user" indica che è un messaggio dell'utente
        # "content": user_input è il testo che l'utente ha scritto
        # append() aggiunge l'elemento alla fine della lista
        messages.append({"role": "user", "content": user_input})

        # print("Claude is thinking...")
        # Stampa un messaggio per indicare che il programma sta aspettando la risposta di Claude
        print("Claude is thinking...")

        # try:
        # Inizia un blocco try-except per gestire gli errori
        # Se accade un errore, il programma non si blocca, ma lo cattura
        try:

            # response = client.messages.create(
            # Chiama il metodo create() del client Anthropic
            # Questo invia una richiesta all'API di Claude e restituisce la risposta
            response = client.messages.create(

                # model=model,
                # Specifica quale modello usare (claude-sonnet-5)
                model=model,

                # max_tokens=500,
                # Limita la lunghezza della risposta a massimo 500 token
                # 1 token ≈ 4 caratteri
                max_tokens=500,

                # messages=messages,
                # Passa tutta la cronologia della conversazione all'API
                # In questo modo Claude ricorda i messaggi precedenti
                messages=messages,
            )

            # answer = get_text_content(response)
            # Estrae il testo dalla risposta di Claude usando la funzione definita sopra
            # answer ora contiene il testo della risposta
            answer = get_text_content(response)

            # print(f"Claude: {answer}\n")
            # Stampa la risposta di Claude
            # f"..." è una f-string che permette di inserire variabili con {variabile}
            # \n aggiunge una riga vuota dopo la risposta
            print(f"Claude: {answer}\n")

            # messages.append({"role": "assistant", "content": answer})
            # Aggiunge la risposta di Claude alla cronologia della conversazione
            # "role": "assistant" indica che è un messaggio di Claude
            # "content": answer è il testo della risposta
            # Questo permette a Claude di ricordare la propria risposta nel prossimo messaggio
            messages.append({"role": "assistant", "content": answer})

        # except Exception as e:
        # Se accade un errore nel blocco try, lo cattura qui
        # Exception è il tipo di errore generico, e e è la variabile che contiene l'errore
        except Exception as e:

            # print(f"Error: {e}\n")
            # Stampa il messaggio di errore per far sapere all'utente cosa è andato male
            print(f"Error: {e}\n")

            # messages.pop()
            # Rimuove l'ultimo messaggio dalla lista (il messaggio dell'utente)
            # Facciamo questo perché la richiesta è fallita, quindi non vogliamo salvare il messaggio
            messages.pop()


# if __name__ == "__main__":
# Questo controllo verifica se il file viene eseguito direttamente (non importato in un altro file)
# "__main__" è il nome speciale dato al file principale quando viene eseguito
if __name__ == "__main__":

    # main()
    # Chiama la funzione main() per avviare il programma
    main()
