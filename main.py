import CarimbaCertificado
import wx.adv
import wx
#Import realizado para utilizar a funcao Sleep
import time

TRAY_TOOLTIP = 'Carimba Certificado Jatinox' 
TRAY_ICON = 'carimbador.png' 


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_IDLE, self.OnIdle)




    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Iniciar', self.on_start)
        create_menu_item(menu, 'Parar', self.on_stop)
        menu.AppendSeparator()
        create_menu_item(menu, 'Sair', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        app.count = 0
        print ('Tray icon foi clicado')

    def OnIdle(self, event):
        print ('onidle')
        self.idleCtrl.SetValue(str(self.count))
        self.count = self.count + 1

    def OnCloseWindow(self, event):
        app.keepGoing = False
        self.Destroy()


    def on_stop(self, event):
        app.STATUS_CARIMBA = False
        print ('Stop')

    def on_start(self, event):
        print ('Start')
        app.STATUS_CARIMBA = True


    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

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
            evtloop.ProcessIdle()

            self.count = self.count + 1
                   
            #PARA FICAR O TEMPO TODO VERIFICANDO POR NOVOS ARQUIVOS E CARIMBANDO
            if (self.STATUS_CARIMBA): # LOOP infinito para manter o programa sempre rodando.
                if self.count > 50:
                    print ('Executando...') # Exibi para o usuario o andamento do programa.
                    CarimbaCertificadoV9.main() 
                    self.count = 0
            wx.EventLoop.SetActive(old)



    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        self.keepGoing = True
        self.count = 0
        self.STATUS_CARIMBA = True
        return True


app = App(False)
app.MainLoop()


