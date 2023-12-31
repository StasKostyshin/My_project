import time
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def record_and_recognize_audio(*args: tuple):
    recognizer = speech_recognition.Recognizer() #####
    microphone = speech_recognition.Microphone() #####
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""
        print(time.ctime())
        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            speak('Listening...')
            audio = recognizer.listen(microphone, 60, 60 )

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            speak('Can you check if your microphone is on, please?')
            return

        # использование online-распознавания через Google
        try:
            speak('Started recognition...')
            recognized_data = recognizer.recognize_google(audio, language="ru").title()
            os.remove("microphone-results.wav")

        except speech_recognition.UnknownValueError:
            pass
        # в случае проблем с доступом в Интернет происходит попытка
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            speak("Trying to use offline recognition...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
# Переключение на оффлайн-распознавание речи :return: распознанная фраза
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists("vosk-model-small-ru-0.4"):
            print("Please download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)
        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()
                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        speak("Sorry, speech service is unavailable. Try again later")
    return recognized_data.title()

def main():
    voice_input = record_and_recognize_audio()
    print(voice_input)
    return voice_input

if __name__ == '__main__':
    main()
