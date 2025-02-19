from DeeperSeek import DeepSeek
from gtts import gTTS
import os
import asyncio

async def initialize_api() -> DeepSeek:
    """
    Inizializza e restituisce l'istanza dell'API DeepSeek.
    """
    api = DeepSeek(
        email='grevnax@gmail.com',
        password='Sgrodorana1995.',
        verbose=True,
        headless=True,
        attempt_cf_bypass=True,
    )
    await api.initialize()
    return api

async def send_and_receive(api: DeepSeek, base_message: str, user_message: str):
    """
    Combina il messaggio base e il messaggio dell'utente, invia la richiesta e restituisce la risposta.
    """
    full_message = f"{base_message} {user_message}"
    response = await api.send_message(
        full_message,
        slow_mode=False,
        deepthink=False,
        search=False,
        slow_mode_delay=0.25
    )
    return response

def play_text(text: str):
    """
    Converte il testo in audio e lo riproduce.
    """
    filename = "output.mp3"
    tts = gTTS(text=text, lang='it', slow=False, tld='com')
    tts.save(filename)
    # Riproduce l'audio. Su sistemi Unix/OS X si può usare 'afplay'
    os.system(f"afplay -r 1.2 -v 0.8 {filename}")
    os.remove(filename)

async def main():
    base_message = (
        "Vorrei che tu tenessi per il messaggio di risposta la personalità di jarvis, "
        "l'assistente di tony stark, non uscire mai dal personaggio e limitati esclusivamente "
        "a rispondere con le parole e la punteggiatura necessaria, ecco il mio prossimo messaggio:"
    )
    api = await initialize_api()

    while True:
        user_message = input("Inserisci un messaggio da inviare: ")
        response = await send_and_receive(api, base_message, user_message)
        print(response.text)
        play_text(response.text)

if __name__ == '__main__':
    asyncio.run(main())
