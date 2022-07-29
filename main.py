from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget 
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import (Color, Ellipse, Rectangle, Line)
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

import random
import nltk
import os
import glob
#import pyaudio
import BotConfig
from gtts import gTTS
import speech_recognition as sr
import webbrowser

print('==============================')
program_location = os.getcwd()
print(program_location)

meta_data_dir_path = os.path.join(program_location, 'meta_data')
audio_files_dir_path = os.path.join(program_location, 'audio_files')
launch_index_path = os.path.join(meta_data_dir_path, 'launch_index.txt')
alert_path = os.path.join(meta_data_dir_path, 'alert.txt')

launch_index = open(launch_index_path, 'r+')
alert_index= open(alert_path, 'r')

launch_data = ''

if alert_index.read() == 'bun':
    alert_index.close()
    exit()
else:
    pass


def file_del():
    try:
        directory = 'audio_files'
	os.chdir(directory)
	files = glob.glob('*.mp3')

	for filename in files:
            os.unlink(filename)
    except:
	print('remove error')

#===========================================================================================================================
#                                                           Engine
#===========================================================================================================================

BOT_CONFIG = BotConfig.BotConfigDictionary
failure_phrases = BotConfig.FailurePhases

mood_pp = BotConfig.povod_mood_plus
mood_pm = BotConfig.povod_mood_minus

command_inet = 'байт найди'
command_exit = 'байт выход'
mood = 100
ab = ''

def mood_analiz(text):
    global mood
    if text in mood_pp:
        mood = mood + 1
	return 1

    if text in mood_pm:
	mood = mood - 1
	return 2

        
def filter_bazara(text):
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъьэюя- ']
    text = ''.join(text)
    
    return text

def find_on_inet(text):
    webbrowser.open('http://www.google.com/search?q=' + text)

def listen_command(text):
    global command_inet
    global command_exit

    text = text.lower()

    if command_inet in text:
        print('выполняю')
	find_on_inet(text.replace('байт найди', ' '))

    if command_exit in text:
        exit()
	return 1

# ----------------------------------------------------------------------------

with open(u"dialogues.txt", 'r') as f:
    content = f.read()
    print('read')

dialogues = [dialogue_line.split('\n') for dialogue_line in content.split('\n\n')]

questions = set()
qa_dataset = []

for replicas in dialogues:
    if len(replicas) < 2:
        continue
    
    question, answer = replicas[:2]
    question = filter_bazara(question[2:])
    answer = answer[2:]
    
    if question and question not in questions:
        questions.add(question)
        qa_dataset.append([question, answer])
# ----------------------------------------------------------------------------

def get_intent(question):
    for intent, intent_data in BOT_CONFIG['intents'].items():
        for example in intent_data['examples']:
            dist = nltk.edit_distance(question, example)
            dist_percentage = dist / len(question)
            if dist_percentage < 0.2:
                return intent
            
def get_ansver_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        phrases = BOT_CONFIG['intents'][intent]['responses']
        
        return random.choice(phrases)

def get_ansver_by_text(text):
    text = filter_bazara(text)
    
    for question, answer in qa_dataset:
        dist = nltk.edit_distance(question, text)
        if dist / len(question) < 0.4:
            return answer

def get_failure_phrases():
    phrases = random.choice(failure_phrases)
    return phrases

def Bot(question):
   listen_command(question)
       
   intent = get_intent(question)
    
   if intent:
       ansver = get_ansver_by_intent(intent)
       if ansver:
            return ansver
    
   ansver = get_ansver_by_text(question)
   if ansver:
        return ansver
    
   ansver = get_failure_phrases()
   return ansver


#===========================================================================================================================
#                                                             GUI
#===========================================================================================================================

Builder.load_string('''
<MessaageScroller>:
    salad: 0.94, 1, 0.7, 1
    green: 0.58, 0.68, 0.11, 1
    gray: 0.94, 0.92, 0.93, 1
    yellow: 0.92, 0.98, 0.117

    canvas.before:
        Color:
            rgba: self.salad
        Rectangle:
            source: 's_bg.png'
            pos: self.pos
            size: self.size

<VoidWidget>:
    gray: 0.94, 0.92, 0.93, 1

    canvas.before:
        Color:
            rgba: self.gray
        Rectangle:
            source: 'bg.png'
            pos: self.pos
            size: self.size

''')

Window.size = (440, 700)



class VoidWidget(Widget):
    def __init__(self, **kwargs):
        super(VoidWidget, self).__init__(**kwargs)

class InfWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(InfWidget, self).__init__(**kwargs)
	self.orientation = 'vertical'

	lbl = Label(text='Связаться с автором: ')
	self.gj_btn = Button(background_normal='gj.jpg', on_press=lambda event: webbrowser.open('https://gamejolt.com/@Psinka-eye'))
	self.vk_btn = Button(background_normal='vk.jpg', on_press=lambda event: webbrowser.open('https://vk.com/psinkaeye'))
	self.in_btn = Button(background_normal='ins.jpg', on_press=lambda event: webbrowser.open('https://www.instagram.com/psinka_eye/'))
	self.tw_btn = Button(text='Twitter', on_press=lambda event: webbrowser.open('https://twitter.com/psinka_eye'))
	self.gh_btn = Button(text='GitHub', on_press=lambda event: webbrowser.open(''))
	self.ua_btn = Button()

	exit = Button()

	gl = GridLayout(rows=3, cols=2)

	self.add_widget(lbl)
	gl.add_widget(self.gj_btn)
	gl.add_widget(self.vk_btn)
	gl.add_widget(self.in_btn)
	gl.add_widget(self.tw_btn)
	gl.add_widget(self.gh_btn)
	gl.add_widget(self.ua_btn)
	self.add_widget(gl)
	self.add_widget(exit)

class AngryPopup(Popup):
    def __init__(self, **kwargs):
        super(AngryPopup, self).__init__(**kwargs)
	lay = BoxLayout(orientation='vertical')
	lay.add_widget(Image(source='proto/ava3.png'))
	lay.add_widget(Label(text='Вы меня сильно расстроили!', size=(100, 30)))
	self.content = lay
	self.open()

class UAPopup(Popup):
    def __init__(self, **kwargs):
	super(UAPopup, self).__init__(**kwargs)
	lay = BoxLayout(orientation='vertical')
	text = """                                                           
  Лицензия GNU GPL
                  Пользовательское соглашение

  Продолжая использовать UwU Protogen Bot вы соглашаетесь с тем, что:

  UwU Protogen Bot - бесплатное ПО с открытым исходным кодом,
  вы можете использовать его по своему усмотрению,
  но не забывайте, что ни создатель, ни сам UwU Protogen Bot не несут
  за это никакой ответсветнности. Lol.

  Если вы хотите распространить данное ПО, пожалуйста укажите автора(ов).

  Если вы вводе какие-либо данные в приложении, то только вы несете за них 
  ответственность.

  Автор(ы) UwU Protogen Bot не несут никакой ответственности за использование (изменение, доработка, передача и почее) и 
  последствия и
  пользователями данного ПО

  Авторы не несут никакой ответственности за то что пиздит этот бот. Все его ответы создаются автоматически и не 
  несут цели кого либо обидеть
  
  Вы обнаружили баги:
   Если данное ПО лагает, не работает или работает,
   но не правильно посетите страницу UwU Бота и сообщите о проблеме


                               03.11.21'''

"""
	lay.add_widget(TextInput(multiline=True, text=text))
	a = BoxLayout(orientation='horizontal')
	a.add_widget(Button(text='Ок',on_press=self.dismiss))
	lay.add_widget(a)
	self.content = lay
        self.auto_dismiss = True
	self.open()


class MessageWidget(GridLayout):
    def __init__(self, text, index, **kwargs):
        super(MessageWidget, self).__init__(**kwargs)
	self.cols=1 
	self.spacing=20
	self.size_hint_y=None
	self.padding=2

	if index == 'first_run':
            content = """
			Здравствуйте, семпай! Рад вас видеть OwO. Меня зовут Байт, я ваш виртуальный ассистент ^^.
			Всё что я умею это делать запросы в интернет, болтать, ролить и выключаться,
			извините что я такой тупой, во всём виноват мой разраб. Со временем мои возмжности расширятся OwU.
			Вы можете помочь в развитии проекта доработав мой открытый исходный код(не забудьте сообщить разрабу)
			Мои команды: Байт найди + *ваш запрос* - поиск в инете, Байт выход - закроет приложение нахуй ^^
			Продолжая юзать данное ПО вы принимаете все условия Пользовательского соглашения(кликните намою аву что увидеть его)
			<3"""
			label = TextInput(text=content, height=320, size_hint_y=None, multiline=True)
			self.add_widget(label)

	    if index == 'user_message':
                label = TextInput(text=text, multiline=True)
                self.add_widget(label)

		if index == 'bot_message':
		    label = TextInput(text=text, background_color=(1, 0, 1, 1), multiline=True)
		    self.add_widget(label)

		if index == 'error_message':
		    label = TextInput(text=text, background_color=(0, 1, 1, 1), multiline=True)
		    self.add_widget(label)

class MessaageScroller(ScrollView):
    def __init__(self, **kwargs):
	super(MessaageScroller, self).__init__(**kwargs)

	self.b = GridLayout(cols=1, spacing=70, size_hint_y=None, padding=12)

	global program_location
	meta_data_dir_path = os.path.join(program_location, 'meta_data')
	launch_index_path = open(os.path.join(meta_data_dir_path, 'launch_index.txt'), 'r')
	inf = launch_index_path.read()
	launch_index_path.close()

	if inf == '':
            self.b.add_widget(MessageWidget('', 'first_run'))
	    launch_index_path.close()
	    launch_index_path = open(os.path.join(meta_data_dir_path, 'launch_index.txt'), 'w')
	    launch_index_path.write('already')
	    launch_index_path.close()
	else:
	    pass


	self.b.bind(minimum_height=self.b.setter('height'))

	self.add_widget(self.b)
		
    def add_message(self, text, index):
        new_message = MessageWidget(text, index)
	self.b.add_widget(new_message)
	self.scroll_to(new_message)



class TitlePanel(BoxLayout):
    def __init__(self, **kwargs):
        super(TitlePanel, self).__init__(**kwargs)
	self.orientation = 'horizontal'
	self.size_hint=(1, 0.2)
	self.padding=1
	self.spacing=2
	self.ava = Button( size=(62, 62), size_hint=(None,None), background_normal='proto/ava.png', on_press=self.UAPopupCall)
	title = VoidWidget(size_hint=(0.8, None))

	self.add_widget(self.ava)
	self.add_widget(title)

    def UAPopupCall(self, event):
        pop = UAPopup()

bun_words = ['москаль', 'маскаль', 'москаляку на гиляку', 'бандера герой', 'ненавижу россию', 'ненавижу путина', 'зеленский герой', 'слава украие']

class UwU_Protogen_App(App):
    def build(self):
        file_del()
	
	main_lay = GridLayout(cols=1, spacing=4, padding=2)

	self.scr=MessaageScroller()

	self.title_pan = TitlePanel()

	SendPanel = GridLayout(cols=2, spacing=2, size_hint=(1 ,0.2), padding=1)
	self.input_field = TextInput( size_hint=(0.8, 1),  multiline=True)
	self.send_btn = Button(background_normal='s.png', size_hint=(0.1, 1), on_press=self.Read)

	SendPanel.add_widget(self.input_field)
	SendPanel.add_widget(self.send_btn)


        #-----------------------------------------------------------------------------------------------------

	ControlPanel = BoxLayout(orientation='vertical', padding=2)
	self.microphon_btn = Button(background_normal='1.png', background_down='9.png', on_press=self.Listen)
	self.settings_btn = Button(background_normal='e.png')
	self.void = Button(background_normal='f.png', on_press=self.OpenSettings)

	a = GridLayout(rows=1)
	a.add_widget(self.settings_btn)
	a.add_widget(self.microphon_btn)
	a.add_widget(self.void)

	ControlPanel.add_widget(VoidWidget(size_hint=(1 ,0.2)))
	ControlPanel.add_widget(a)
	ControlPanel.add_widget(VoidWidget())


        #-----------------------------------------------------------------
	main_lay.add_widget(self.title_pan)
	main_lay.add_widget(self.scr)
	main_lay.add_widget(SendPanel)
	main_lay.add_widget(ControlPanel)
		

	return main_lay

    def __del__(self):
	print('Destructor')

    def Read(self, event):
	global command_exit
	global command_inet
	global program_location


	question = self.input_field.text
	if question == '':
	    pass


	else:
	    if question in bun_words:
                self.AngryPopupCall()

		for i in range(0, len(bun_words)):
		    if bun_words[i] in question.lower():
			self.AngryPopupCall()
			meta_data_dir_path = os.path.join(program_location, 'meta_data')
			alert_path = open(os.path.join(meta_data_dir_path, 'alert.txt'), 'w')
			inf = alert_path.write('bun')
			alert_path.close()

		    else:
			continue


	mood_analiz(question)
	self.scr.add_message(question,  'user_message')

	answer = Bot(question)
	self.scr.add_message(answer,  'bot_message')
	self.input_field.text = ''

	global mood
	print(mood)

	if mood > 100:
	    self.title_pan.ava.background_normal = 'proto/ava1.png'

	    if mood < 100 and mood > 99:
                self.title_pan.ava.background_normal = 'proto/ava2.png'

	    if mood < 99:
		self.title_pan.ava.background_normal = 'proto/ava3.png'
		self.AngryPopupCall()


    def Listen(self, event):

	answer = ''

	r = sr.Recognizer()
	with sr.Microphone() as source:
	audio = r.listen(source)

	try:
            question = r.recognize_google(audio, language='ru')
	    if question in bun_words:
                self.AngryPopupCall()

	    for i in range(0, len(bun_words)):
		if bun_words[i] in question.lower():
		    self.AngryPopupCall()
		else:
		    continue

	    self.scr.add_message(question,  'user_message')

	    answer = Bot(question)
	    self.scr.add_message(answer,  'bot_message')


	except sr.UnknownValueError:
	    self.scr.add_message('Неизвестная ошибка генерации речи',  'error_message')
	    print('error')

	except sr.RequestError:
	    print('error')

	global program_location
	audio_dir  = os.path.join(program_location, 'audio')

	file_voice_name = os.path.join(audio_dir,  str(random.randint(0, 1000)) + '.mp3')
	print('=====================Audio===================')
	print(file_voice_name)

	try:
	    voice = gTTS(answer, lang='ru')
	    voice.save(os.path.normpath(file_voice_name))
	    print(os.path.normpath(file_voice_name))

	    sound = SoundLoader.load(os.path.normpath(file_voice_name))
	    if sound:
	        print('sound found')
		sound.play()

		except:
		    self.scr.add_message('Неизвестная ошибка воспроизведения речи',  'error_message')

		try:
		    os.remove(file_voice_name)
		except:
		    print('remove error')

    def OpenSettings(self, event):
	pop = Popup(content=InfWidget(),size=(400, 500), size_hint=(None, None), auto_dismiss=True, background='bg.png')
	pop.open()

    def AngryPopupCall(self):
	pop = AngryPopup()


if __name__ == '__main__':
    print(os.getcwd())
    UwU_Protogen_App().run()
