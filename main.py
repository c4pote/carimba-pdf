# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter, PdfFileReader
import io

#IMPORT UTILIZADO NO SLEEP
import time

#Reportlab Básico
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

#Polegadas e Centimetros para responsividade.
from reportlab.lib.units import inch
from reportlab.lib.units import cm

#Cores para habilitar transparencia
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color

#trabalhando com imagem para adicionar o logo da jatinox
from reportlab.lib.utils import ImageReader
from reportlab.lib import utils
from reportlab.platypus import Frame, Image

import os


#path = 'B:\\MATRIZ\\CERTIFICADOS'
#path = 'C:\\Users\\Lucas.Oliveira\\Documents\\CarimbaCertificadoPython'
path = 'C:\\Users\\gustavo.lima\\Desktop\\CERTIFICADOS'

debug=False

#logo = ImageReader('C:\\Users\\gustavo.lima\\Desktop\\CERTIFICADOS\\logo.png')
logo = ImageReader('logo.png')


#Redimensiona Imagem
def get_image(path, width=1*cm):
	img = utils.ImageReader(path)
	iw, ih = img.getSize()
	aspect = ih / float(iw)
	return Image(path, width=width, height=(width * aspect))


#para tratar o lote deixando ele visualmente melhor e removendo informacoes que nao utilizamos para lote.
def tratalote(lotesemtratar):
	lotetratado= lotesemtratar.replace('-CARTA','')
	lotetratado= lotetratado.replace('CARTA','')# exemplos para outros casos
	lotetratado= lotetratado.replace(' ','')#todos os espaços existentes, principalmente os casos "BN  
	lotetratado= str(lotetratado[:2]) + ' ' + str(lotetratado[2:])# Coloca um espaco entre Tipo e Lote
	return lotetratado


def moverarquivo(arquivoorigem):
	#MOVENDO ARQUIVO DE ORIGEM
	arquivo = (os.path.split(arquivoorigem))
	diretorio= arquivo[0]
	arquivo= (os.path.splitext(arquivo[1]))
	lote= arquivo[0]

	try:
		pasta = (os.path.join(diretorio,"ORIGINAL"))
		if os.path.isdir(pasta): # vemos se este diretorio ja existe
			if debug:
				print ('Ja existe uma pasta com esse nome!')
		else:
			if debug:
				print ('Pasta criada com sucesso!')
			os.mkdir(pasta)
		
	except:
		if debug:
			print("arquivoscarimbar")


	arquivodestino = os.path.join(diretorio,"ORIGINAL",lote) +".pdf" 
	print (arquivodestino)

	#AQUI VOCE DEVE CRIAR A VERIFICACAO DE EXISTENCIA DO ARQUIVO DESTINO, CASO O MESMO EXISTA REMOVER ANTES DA PROXIMA FUNCAO OS.RENAME.
	if os.path.isfile(arquivodestino):
		os.remove(arquivodestino)
		
	os.rename(arquivoorigem,arquivodestino)


def carimbaPDF(arquivoorigem,line1,line2):

	#Controla se vai usar o logotipo ou as duas linhas de parametro de entrada no carimbo.
	usa_logotipo = True

	arquivo = (os.path.split(arquivoorigem)) #Ex arquivoorigem = c:\certificado\BN\arquivo.pdf entao arquivo vai receber no primeiro array 'c:\certificado\BN\' e no segundo 'arquivo.pdf'
	diretorio= arquivo[0]
	arquivo = (os.path.splitext(arquivo[1])) #Utilizando o mesmo ex acima aqui receber no primeiro array 'arquivo' e no segundo '.pdf'
	lote = arquivo[0] #Carregamos o nome do arquivo que será carimbado no PDF do certificado.
	
	packet = io.BytesIO()
	# Criando um novo PDF com Reportlab
	can = canvas.Canvas(packet, pagesize=A4)
	# move the origin up and to the left
	can.translate(inch,inch)
	# Define fonte e largura
	can.setFont("Helvetica", 15)
	# Mudar cor da Moldura para Perto
	can.setStrokeColorRGB(0,0,0)
	
	# Desenhando Retangulo para parecer um carimbo
	# CASO NAO TENHA A INFORMACAO NA LINHA 2 O RETANGULO VAI SER REDUZIDO.
	if usa_logotipo:
		#Retangulo para LOGO
		# FUNDO BRANCO TRANSPARENTE COM BORTA PRETA
		can.setFillColor(Color(255,255,255, alpha=0.5))
		can.rect(-0.94*inch,-0.7*inch,0.7*inch,1.5*inch, fill=1)
		#REMOVENDO A TRANSPARENCIA.
		can.setFillColor(Color(255,255,255, alpha=1))
		line2 = '' # REMOVENDO INFORMACAO DAS LINHAS POIS O LOGOTIPO VAI UTILIZAR O ESPACO DESTINADO A ESSE RECURSO QUANDO HABILITADO
		
		# Desenhando linha que separa o lote do Logo
		can.line(-0.73*inch,-0.7*inch,-0.73*inch,0.8*inch)
		
		# Desenhando linha que separa logo da linha 1
		can.line(-0.73*inch,-7,-0.23*inch,-7)
		
	elif line2 == "":
		#Retangulo para quando a linha 2 esta nula
		can.rect(-0.94*inch,-0.7*inch,0.4*inch,1.5*inch, fill=1)
	else:
		#Retangulo quando a linha 2 foi preenchida e nao vai usar logo.
		can.rect(-0.94*inch,-0.7*inch,0.6*inch,1.5*inch, fill=1)

	# Rotacionando carimbo para utilizar a margem e nao sobrepor muito os dados do documento
	can.rotate(90)

	# Mudando a Cor do texto para Azul e removendo transparencia.
	can.setFillColor(Color(0,0,0.77, alpha=1))
	
	# Dados do Carimbo
	can.drawString(-0.60*inch,  0.76 *inch,  '{: >12}'.format(tratalote(lote)))
	#can.drawString(-0.78*inch,  0.58 *inch, '{: >14}'.format(line1))
	
	can.drawString(-0.49*inch,  0.40 *inch, '{: >14}'.format(line1))
	can.drawString(-0.68*inch,  0.38 *inch, '{: >14}'.format(line2))

	#ADD LOGO JATINOX
	if usa_logotipo:
		#LOGO CENTRALIZADO
		#frame = Frame(-0.96*inch, -1.19 *inch, 5*cm, 5*cm, showBoundary=0)
		#LOGO ALINHADO A ESQUERDA
		frame = Frame(-1.38*inch, -1.19 *inch, 5*cm, 5*cm, showBoundary=0)
		story = []
		#Redimensionando Imagem do LOGO JATINOX para 2cm mantendo proporção
		story.append(get_image('logo.png', width=1.4*cm))
		frame.addFromList(story, can)

    #Adicionando Autoria e Titulo
	can.setAuthor("JATINOX")
	can.setTitle("CERTIFICADO JATINOX")


	can.save() 

	#mover para o inicio o buffer StringIO
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	
	# Leitura do PDF de ORIGEM
	f=open(arquivoorigem, "rb")
	existing_pdf = PdfFileReader(f)
	output = PdfFileWriter()

	#Tratando arquivos encriptados
	if existing_pdf.isEncrypted:
	    existing_pdf.decrypt('')


	#Carimbando as paginas
	#Obtendo quantidade de paginas no documento original
	paginas = existing_pdf.getNumPages()
	# Copiando e carimbando todas as paginas.
	for numero_pagina in range(paginas):
		page = existing_pdf.getPage(numero_pagina) #Cria uma pagina clone do arquivo origem
		page.mergePage(new_pdf.getPage(0)) #Adiciona o carimbo criado no canvas na nova pagina criada.
		output.addPage(page) #Salva a pagina carimbada na variavel de output
	
	# Escrevendo o arquivo de destino
	tempor = diretorio + "\\" + lote + "-C.pdf" # tempor = variável temporaria
	outputStream = open(tempor, "wb")
	if debug:
		print(tempor)
	output.write(outputStream)
	outputStream.close()


	f.close()

def percorrer():

	filearrays = { '.pdf':[],'-C.pdf':[], 'lotes':[]} # Cria um array de variaveis para armazenar documentos suportados.
	for root, dirs, files in os.walk(path): #Funcao recursiva que percore as pastas apartir de um caminho.
		for file in files: #Obtem um arquivo do array de arquivos encontrados na funcao os.walk
			filename, fileext = os.path.splitext(file) #corto o caminho do arquivo por sua extencao. (ex: c:\pasta\arquivo.pdf fica filename =  c:\pasta\arquivo fileext = .pdf )
			if fileext in filearrays: # Se a extencao encontrada tem o mesmo nome que uma das variaveis contidas em filearrays então.
				#print (file.endswith('-C.pdf'))
				if not(root.endswith('ORIGINAL')): #Verifica se nao é a pasta original, isso é necessário para evitar que o sistema carimbe os arquivos que já foram carimbados.
					if not(file.endswith('-C.pdf')): #O nome do arquivo não termina com a extensão '-C.pdf'
						filearrays[fileext].append(os.path.join(root,file)) #Grava na variavel filearrays com extensão correspondente.
					else:
						filearrays['-C.pdf'].append(os.path.join(root,file)) #Grava na variavel filearrays com extensão '-C.pdf'
	return filearrays # Retorno a lista de filearrays categorizados por extensao .pdf ou -C.pdf e seus respectivos nomes na variavel lote.

def main():
	arquivoscarimbar = percorrer() #Carrega a listagem de arquivos para carimbar em um array
	for arqcarimbar in arquivoscarimbar['.pdf']: #For para percorrer os arquivos que vao ser carimbados.
		#carimbaPDF(arqcarimbar,"Numero", "Rastreabilidade") #Chamando funcao que carimba os documentos.
		print('Carimbando Certificados')
		carimbaPDF(arqcarimbar,"NR","") #Chamando funcao que carimba os documentos.
		try:
			print('Movendo Certificado Original para pasta Origem')
			moverarquivo(arqcarimbar) # Chamando funcao que move o arquivo original para pasta correta.
		except:
			print ('O arquivo abaixo está sendo utilizado por outro usuário e será movido assim que fechar o arquivo')
			print(arqcarimbar)
	#Liberando a memoria que foi carregada com os caminhos dos arquivos encontrado.
	arquivoscarimbar = ''				
	
	
	#time.sleep(60) # AGUARDA 60 SEGUNDOS ANTES DE REINICIAR O PROGRAMA

