# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os
#import shutil

debug=False


def tratarlote(lotesemtratar):
	lotetratado = lotesemtratar.replace('-CARTA','')
	lotetratado = lotetratado.replace('CARTA','')
	return lotetratado
#Obtendo o Sistema Operacional
#import platform
#so = platform.system()

def moverarquivo(arquivoorigem):
	#MOVENDO ARQUIVO DE ORIGEM
	arquivo= (os.path.split(arquivoorigem))
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
		#os.rename(arquivoorigem,"ORIGINAL/"+arquivoorigem)
		
	except:
		if debug:
			print("arquivoscarimbar")



	#if so == 'Linux':
	#		os.rename(arquivoorigem,"ORIGINAL/"+arquivoorigem)
	#elif so == 'Windows':
	#	if debug:
	#		print ('Windows')
	arquivodestino = os.path.join(diretorio,"ORIGINAL",lote) +".pdf" 
	print (arquivodestino)
	os.rename(arquivoorigem,arquivodestino)
		#shutil.move(arquivoorigem,arquivoscarimbar)
		#shutil.copy("C:\\Users\\Lucas.Oliveira\\Documents\\CarimbaCertificadoPython\\BN\\18\\24XX\\","C:\\Users\\Lucas.Oliveira\\Documents\\CarimbaCertificadoPython\\BN\\18\\24XX\\ORIGINAL\\"+arquivoorigem)
	#else:
	#	return 'Sistema Operacional sem suporte. Host: ' + platform.node() + ' Sistema: ' + so
	#return 'Movido com Sucesso!'


def carimbaPDF(arquivoorigem,line1,line2):
	arquivo= (os.path.split(arquivoorigem))
	#print(os.path.splitext(abc[1]))
	diretorio= arquivo[0]
	arquivo= (os.path.splitext(arquivo[1]))
	lote= arquivo[0]
	packet = io.BytesIO()
	# Criando um novo PDF com Reportlab
	can = canvas.Canvas(packet, pagesize=A4)
	# move the origin up and to the left
	can.translate(inch,inch)
	# Define fonte e largura
	can.setFont("Helvetica", 15)
	# Mudar cor
	can.setStrokeColorRGB(0,0,0)
	can.setFillColorRGB(1,0,1)

	# Desenhando linha que separa o lote das observacoes
	can.line(-0.66*inch,-0.69*inch,-0.66*inch,0.8*inch)

	# Desenhando Retangulo para parecer um carimbo
	can.rect(-0.9*inch,-0.7*inch,0.7*inch,1.5*inch, fill=0)
	# Rotacionando carimbo para utilizar a margem e nao sobrepor muito os dados do documento
	can.rotate(90)
	# Mudando a Cor do texto para Azul
	can.setFillColorRGB(0,0,0.77)
	# Dados do Carimbo
	can.drawString(-0.63*inch,  0.7 *inch,  '{: >11}'.format(tratarlote(lote)))
	can.drawString(-0.66*inch,  0.46 *inch, '{: >14}'.format(line1))
	can.drawString(-0.66*inch,  0.26 *inch, '{: >14}'.format(line2))

	
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
		page = existing_pdf.getPage(numero_pagina)
		page.mergePage(new_pdf.getPage(0))
		output.addPage(page)
	# Escrevendo o arquivo de destino
	
	#outputStream = open(lote + "-C.pdf", "wb")
	tempor= diretorio + "\\" + lote + "-C.pdf"
	outputStream = open(tempor, "wb")
	if debug:
		print(tempor)
	output.write(outputStream)
	outputStream.close()


	f.close()
	#moverarquivo(arquivoorigem)
path = 'B:\\MATRIZ\\CERTIFICADOS'
#path = 'C:\\Users\\gustavo.lima\\Desktop\\CERTIFICADOS'
#path = 'C:\\Users\\Lucas.Oliveira\\Documents\\CarimbaCertificadoPython\\BN'


def percorrer():

	filearrays = { '.pdf':[],'-C.pdf':[], 'lotes':[]}
	for root, dirs, files in os.walk(path): #aqui o 
		for file in files:
			filename, fileext = os.path.splitext(file)
			if fileext in filearrays:
				#print (file.endswith('-C.pdf'))
				if not(root.endswith('ORIGINAL')):
					if not(file.endswith('-C.pdf')):
						filearrays[fileext].append(os.path.join(root,file))
					else:
						filearrays['-C.pdf'].append(os.path.join(root,file))
	return filearrays

def main():
	execucoes = 0
	#PARA FICAR O TEMPO TODO VERIFICANDO POR NOVOS ARQUIVOS E CARIMBANDO
	while True:
		execucoes = execucoes + 1
		print ('Execução {}'.format(str(execucoes)))
		arquivoscarimbar=percorrer()
		for arqcarimbar in arquivoscarimbar['.pdf']:
			carimbaPDF(arqcarimbar,"Rastreabilidade", "Jatinox")
			try:
				moverarquivo(arqcarimbar)
			except:
				print ('O arquivo abaixo está sendo utilizado por outro usuário e será movido assim que fechar o arquivo')
				print(arqcarimbar)
		#carimbaPDF("BN\\18\\24XX\\BN18-2400.pdf","BN18-2400","Rastreabilidade","Jatinox")
		#carimbaPDF("original.pdf", "BN10-202", "Rastreabilidade", "Jatinox ")
		time.sleep(120) # AGUARDA 60 SEGUNDOS ANTES DE REINICIAR O PROGRAMA

if __name__ == "__main__":
	main()