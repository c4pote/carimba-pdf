# -*- coding: utf-8 -*-
#Imports do projeto
import src

def main(settings):
	#Obtendo pasta para percorrer do arquivo Settings.txt
	path = settings[0]

	#print ('Execução {}'.format(str(execucoes))) # Exibi para o usuario o andamento do programa.
	arquivoscarimbar = []

	arquivoscarimbar = src.Carimbador.percorrer(path) #Carrega a listagem de arquivos para carimbar em um array
	for arqcarimbar in arquivoscarimbar['.pdf']: #For para percorrer os arquivos que vao ser carimbados.
		try:
			print(arqcarimbar)
			src.Carimbador.carimbaPDF(arqcarimbar,"NR","") #Chamando funcao que carimba os documentos.
		except:
			print ('Houve um erro e o arquivo {} não pode ser carimbado.'.format(str(arqcarimbar))) 
			#Esse continue evita que a funcao de mover seja executada.
			#Como apresentou algum problema em carimbar o arquivo nao deve ser enviado para a pasta original
			continue

		try:
			src.SalvaOrigem.mover(arqcarimbar) # Chamando funcao que move o arquivo original para pasta correta.
		except:
			print ('O arquivo abaixo está sendo utilizado por outro usuário e será movido assim que fechar o arquivo')
			print(arqcarimbar)

	contagem = len(arquivoscarimbar['.pdf'])
	if  contagem > 0: 
		print ('No total {} arquivos foram carimbados nessa execução'.format(str(contagem))) 

	return	arquivoscarimbar
		