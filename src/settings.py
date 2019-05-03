class Settings:

	def __init__(seft):
		return self

	def config():
		path = ''
		wait = ''
		tray_tooltip = 'Carimba Certificado Jatinox' 
		tray_icon = 'carimbador.png' 
		tray_icon_exec = 'carimbador2.png' 

		f = open('settings.txt', 'r')
		for line in f:
			if line.split('=')[0] == 'path':
				path = line.split('=')[1]
				#Removendo quebras de linha CL RF
				path = path.replace('\n', '')
				path = path.replace('\r', '')
				continue

			if line.split('=')[0] == 'wait':
				wait = line.split('=')[1]
				if int(wait) < 20:
					wait = 20 #Minimo para evitar que o programa fique o tempo todo buscando.
				continue
		f.close()
		return [path, wait, tray_tooltip, tray_icon, tray_icon_exec]