# Голосовой ассистент КЕША 1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser

# настройки
opts = {
    "alias": ('пятница', 'кеш', 'инокентий', 'иннокентий', 'кишун', 'киш',
              'кишаня', 'кяш', 'кяша', 'кэш', 'кэша'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
        "wc": ('запусти варкрафт', 'запусти warcraft', 'запусти вов', 'запусти войну', 'запусти вовку',
               'открой варкрафт', 'открой warcraft', 'открой вов', 'открой войну', 'открой вовку'),
        "ow": ('запусти овервотч', 'запусти ов', 'запусти overwatch','запусти ow',
               'открой овервотч', 'открой ов', 'открой overwatch','открой ow'),
        "ds3": ('запусти дарк соулс', 'запусти дээс', 'запусти дс','запусти dark souls', 'запусти ds',
                'запусти дарк соулс 3', 'запусти дээс 3', 'запусти дс 3','запусти dark souls 3', 'запусти ds 3',
                'запусти дарк соулс три', 'запусти дээс три', 'запусти дс три','запусти dark souls три', 'запусти ds три',
                'открой дарк соулс', 'открой дээс', 'открой дс', 'открой dark souls', 'открой ds',
                'открой дарк соулс 3', 'открой дээс 3', 'открой дс 3', 'открой dark souls 3', 'открой ds 3',
                'открой дарк соулс три', 'открой дээс три', 'открой дс три', 'открой dark souls три',
                'открой ds три'),
        "twitch": ('открой твич', 'открой twitch', 'кто стримит', 'покажи кто стримит',
                   'запусти твич', 'запусти twitch'),
        "yt": ('открой ютуб', 'открой youtube','открой ютьюб', 'открой ютюб',
               'запусти ютуб', 'запусти youtube','запусти ютюб'),
        "gmail": ('открой почту'),
        "transl": ('открой переводчик'),
        "itc": ('покажи новости IT', 'покажи новости айти',
                'открой itcua', 'открой айтисиюа', 'открой itc', 'открой айтиси'),
        "google": ('мне нужно загуглить', 'открой гугл', 'открой google',
                   'мне нужно загуглить кое что', 'мне нужно загуглить кое-что',
                   'мне нужно кое что загуглить', 'мне нужно  кое-что загуглить'),
        "ggle": ('загугли', 'найди'),
        "vk": ('открой вк','открой вэка','открой вконтакте','открой в тентакле',
               'открой втентакле'),
        "rottr": ('запусти лару крофт', 'запусти Rise of the Tomb Raider',
                  'запусти томб райдер', 'запусти tomb raider', 'запусти райз оф зе томб райдер',
                  'открой лара крофт', 'открой Rise of the Tomb Raider',
                  'открой томб райдер', 'открой tomb raider', 'открой райз оф зе томб райдер'),
        "weather": ('какая будет завтра погода','что там по погоде',
                    'скажи какая завтра будет погода', 'какая сегодня будет погода',
                    'скажи какая сегодня будет погода', 'какая погода сегодня', 'какая погода завтра',
                    'какая будет погода сегодня', 'какая будет погода завтра',
                    'какая погода будет сегодня', 'какая погода будет завтра'),
        "python": ('открой пайтон', 'открой python', 'открой питон',
                   'запусти пайтон', 'запусти python', 'запусти питон'),
        "visual": ('открой вижуал', 'открой visual', 'открой с++', 'открой си плюс плюс', 'открой Microsoft Visual Studio',
                  'запусти вижуал', 'запусти visual', 'запусти с++', 'запусти си плюс плюс', 'запусти Microsoft Visual Studio'),
        "mCAD": ('открой маткад', 'открой mathCAD',
                 'запусти маткад', 'запусти mathCAD')
    }
}


# функции
def speak(what):
    speak_engine = pyttsx3.init()
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        webbrowser.open_new_tab("https://play.google.com/music/listen#/ap/auto-playlist-recent")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Колобок повесился. Тебе смешно? А мне нет")

    elif cmd == 'wc':
        os.system("E:\\games\\wow\\World_of_Warcraft\\World_of_Warcraft_Launcher.exe")

    elif cmd == 'ow':
        os.system("E:\\games\\Overwatch\\Overwatch_Launcher.exe")

    elif cmd == 'ds3':
        os.startfile(r"E:\games\Steam\steamapps\common\DARK SOULS III\Game\DarkSouls3.exe")

    elif cmd == 'twitch':
        webbrowser.open_new_tab("https://www.twitch.tv/directory")

    elif cmd == 'yt':
        webbrowser.open_new_tab("https://www.youtube.com")

    elif cmd == 'gmail':
        webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")

    elif cmd == 'transl':
        webbrowser.open_new_tab("https://translate.google.com/?hl=ru#view=home&op=translate&sl=en&tl=ru")

    elif cmd == 'itc':
        webbrowser.open_new_tab("https://itc.ua")

    elif cmd == 'google':
        webbrowser.open_new_tab("https://www.google.com")

    elif cmd == 'ggle':

        webbrowser.open_new_tab("https://www.google.com/search?q=")

    elif cmd == 'vk':
        webbrowser.open_new_tab("https://vk.com/feed")

    # elif cmd == 'rottr':
        # os.system("E:\\games\\Rise_of_TR\\Rise_of_tr.exe")

    elif cmd == 'weather':
        webbrowser.open_new_tab("https://www.google.com/search?q=погода&rlz=1C1SQJL_ruUA842UA842&oq=погода&aqs=chrome..69i57j0l4j69i60.1703j1j0&sourceid=chrome&ie=UTF-8")

    elif cmd == 'python':
        os.system("")

    # elif cmd == 'visual':
        # os.system("C:\\Program Files (x86)\\Microsoft_Visual_Studio\\2019\\Professional\\Common7\\IDE\\devenv.exe")


    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)



# Только если у вас установлены голоса для синтеза речи!
# voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[4].id)

# forced cmd test
# speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

speak("Доброго времени суток")
speak("Пятница слушает")

# stop_listening = r.listen_in_background(m, callback)
# while True: time.sleep(0.1) # infinity loop

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)