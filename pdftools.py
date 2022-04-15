from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config


class TestApp(App):
    def build(self):
        return Button(text='Hello World')

class Toolkit(App):
    def build(self):
        Config.set('graphics', 'resizable', True)
        Config.set('graphics', 'width', 300)
        Config.set('graphics', 'height', 50)
        # layout
        self.layout = GridLayout(cols=2)
        left = GridLayout(cols=2)
        self.layout.add_widget(left)

        self.src = Button(text='File to replace...')
        self.dst = Button(text='Replace with...')
        self.fire = Button(text='Start', size_hint_x=None, width=80)
        self.pages = TextInput(text='Pages to replace...')
        self.replaced = TextInput(text='Replaced pages')
        left.add_widget(self.src)
        left.add_widget(self.pages)
        left.add_widget(self.dst)
        left.add_widget(self.replaced)

        self.layout.add_widget(self.fire)
        # bind event
        self.src.bind(on_press=self.open)

        return self.layout

    def open(self, instance):
        fc = FileChooserListView()
        popup = Popup(title='Please select a file', content=fc)
        popup.open()

class Replace(App):
    def build(self):
        button = Button(text='Start')
        button.bind(on_release=self.replace)
        return button
    
    def replace(self, instance):
        with open('conf.txt', 'r') as fi:
            files = [f.strip() for f in fi.readlines()]
            srcFile, srcFile1 = files[0], files[1]
            dstFile = 'replaced.pdf'
            import PyPDF2 as pdf

            src = pdf.PdfFileReader(srcFile)
            total = src.getNumPages()
            src2 = pdf.PdfFileReader(srcFile1)
            dst = pdf.PdfFileWriter()
            for page in range(total - 1):
                dst.addPage(src.getPage(page))
            dst.addPage(src2.getPage(0))
            fo = open(dstFile, 'wb+')
            dst.write(fo)
            fo.close()

Replace().run()
