debug=False
import os
class SalvaOrigem(object):
	def __init__(self):
		print('Inicializando...')

	def destino(arquivoorigem):
		#MOVENDO ARQUIVO DE ORIGEM
		arquivo = (os.path.split(arquivoorigem))
		diretorio = arquivo[0]
		arquivo = (os.path.splitext(arquivo[1]))
		lote = arquivo[0]

		arquivodestino = os.path.join(diretorio,"ORIGINAL",lote) + ".pdf" 

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
			print("Erro ao verificar existencia de diretorio ORIGINAL")

		return arquivodestino

	def mover(arquivoorigem):
		if debug: 
			print('Movendo arquivo origem para a pasta ORIGINAL')
		
		print(arquivoorigem)
		
		arquivodestino = SalvaOrigem.destino(arquivoorigem)
		
		#Verificando se existe arquivo de destino
		#Caso exista a instrução abaixo vai remover para que que seja possivel mover o arquivo original
		if os.path.isfile(arquivodestino):
			os.remove(arquivodestino)
		
		#Movendo o arquivo de origem para a pasta de ORIGINAL dentro do diretorio onde arquivo foi carimbado
		os.rename(arquivoorigem,arquivodestino)
