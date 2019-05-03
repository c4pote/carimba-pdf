import Carimba
import wx.adv
import wx
#Import realizado para utilizar a funcao Sleep
import time

#Imports do projeto
import src

#Carregando Configuraçoes
global settings 
settings = src.Settings.config()
global refresh 
refresh = False
global wait 
wait = settings[1]

global TRAY_ICON 
TRAY_ICON = settings[3] #Obtem imagem para colocar como icone.


TRAY_TOOLTIP = settings[2] #Obtem o nome que vai ficar no icone


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon, wx.Frame):

    def __init__(self, frame):
        print('Carimba Certificados')
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)



    def CreatePopupMenu(self):
        menu = wx.Menu()
        if app.status:
            create_menu_item(menu, 'Stop', self.on_stop)
        else:
            create_menu_item(menu, 'Start', self.on_start)
            
        menu.AppendSeparator()
        create_menu_item(menu, 'Config Refresh', self.on_refresh)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        app.count = 0
        print ('Tray icon foi clicado')

    def on_stop(self, event):
        app.status = False
        print ('Stop')

    def on_start(self, event):
        print ('Start')
        app.status = True

    def on_refresh(self, event):
        global refresh
        global wait
        global settings
        print('Refresh')
        settings = src.Settings.config()
        wait = settings[1]

        refresh = False
        app.refresh = True
      


    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()
        app.keepGoing = False

class App(wx.App):
    def MainLoop(self):
        # Create an event loop and make it active.  If you are
        # only going to temporarily have a nested event loop then
        # you should get a reference to the old one and set it as
        # the active event loop when you are done with this one...
        evtloop = wx.GUIEventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)
        #count = 1
        while self.keepGoing:
            
            # This inner loop will process any GUI events
            # until there are no more waiting.
            while evtloop.Pending():
                evtloop.Dispatch()

            time.sleep(0.10)
            #evtloop.ProcessIdle()

            self.count = self.count + 1
                   
            #PARA FICAR O TEMPO TODO VERIFICANDO POR NOVOS ARQUIVOS E CARIMBANDO
            #if (self.STATUS_CARIMBA): # LOOP infinito para manter o programa sempre rodando.
            if self.count > int(wait):
                print('Carimbando....')
                Carimba.main(settings) 
                print('Acabou...')
                self.count = 0
            wx.EventLoop.SetActive(old)



    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        self.keepGoing = True
        self.count = 0
        self.status = True
        return True


app = App(False)
app.MainLoop()

