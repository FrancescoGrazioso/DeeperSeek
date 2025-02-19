import os
import asyncio
from DeeperSeek import DeepSeek
from DeeperSeek.internal.objects import Response
from gtts import gTTS

BASE_MESSAGE = (
    "Vorrei che tu tenessi per il messaggio di risposta la personalità di jarvis, "
    "l'assistente di tony stark, non uscire mai dal personaggio e limitati esclusivamente "
    "a rispondere con le parole e la punteggiatura necessaria, ecco il mio prossimo messaggio:"
)

SMART_HOME_PREFIXES = ("accendi", "accendere", "spegni", "spegnere")


async def initialize_api() -> DeepSeek:
    """
    Inizializza e restituisce l'istanza dell'API DeepSeek.
    """
    api = DeepSeek(
        email="grevnax@gmail.com",
        password="Sgrodorana1995.",
        verbose=True,
        headless=True,
        attempt_cf_bypass=True,
    )
    await api.initialize()
    return api


async def send_and_receive(api: DeepSeek, user_message: str) -> Response:
    """
    Combina il messaggio base e il messaggio dell'utente, invia la richiesta e restituisce la risposta.
    """
    full_message = f"{BASE_MESSAGE} {user_message}"
    response = await api.send_message(
        full_message,
        slow_mode=False,
        deepthink=False,
        search=False,
        slow_mode_delay=0.25,
    )
    return response


def handle_smart_home() -> Response:
    """
    Gestisce i comandi per la smart home.
    """
    return Response(text="Fatto, sir!")


async def execute_command(api: DeepSeek, user_message: str) -> Response:
    """
    Esegue il comando basato sul messaggio dell'utente.
    Se il messaggio inizia con un comando smart home, restituisce una risposta predefinita.
    Altrimenti invia il messaggio all'API DeepSeek e restituisce la risposta ricevuta.
    """
    if any(user_message.lower().startswith(prefix) for prefix in SMART_HOME_PREFIXES):
        return handle_smart_home()
    return await send_and_receive(api, user_message)


def play_text(text: str) -> None:
    """
    Converte il testo in audio e lo riproduce.
    """
    filename = "output.mp3"
    tts = gTTS(text=text, lang="it", slow=False, tld="com")
    tts.save(filename)
    # Su macOS si può usare 'afplay'; per altri sistemi sostituire il comando appropriato.
    os.system(f"afplay -r 1.25 -v 0.8 {filename}")
    os.remove(filename)


async def main():
    api = await initialize_api()
    while True:
        user_message = input("Inserisci un messaggio da inviare: ").strip()
        if not user_message:
            continue
        response = await execute_command(api, user_message)
        if response and response.text:
            print(response.text)
            play_text(response.text)
        else:
            print("Nessuna risposta ricevuta.")


if __name__ == "__main__":
    asyncio.run(main())
