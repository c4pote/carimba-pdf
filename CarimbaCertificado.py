# -*- coding: utf-8 -*-
#Imports do projeto
import src

#Import realizado para utilizar a funcao Sleep
import time

#Obtendo pasta de que o programa vai percorrer para carimbar os documentos
path = src.Repositorios.repo('Producao') #Mudar para Producao para percorrer a pasta com os certificados.

def main():
	#print ('Execução {}'.format(str(execucoes))) # Exibi para o usuario o andamento do programa.
	arquivoscarimbar = src.Carimbador.percorrer(path) #Carrega a listagem de arquivos para carimbar em um array
	for arqcarimbar in arquivoscarimbar['.pdf']: #For para percorrer os arquivos que vao ser carimbados.
		try:
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
	return	arquivoscarimbar
		

if __name__ == "__main__":
	print('Carimba Certificados')
	print(path)
	# Utilizado para contar as execucoes de pesquisa de novos arquivos para carimbar.
	execucoes = 1
	#Verifica de tempos em tempos novos arquivos para carimbar.
	while True: # LOOP infinito para manter o programa sempre rodando.
		carimbados = main() # AQUI COMECA O PROGRAMA.
		contagem = len(carimbados['.pdf'])
		if  contagem > 0: 
			print ('Execução {} realizada com sucesso, no total {} arquivos foram carimbados nessa execução'.format(str(execucoes),str(contagem))) 
			execucoes = execucoes + 1 #INCREMENTA A EXECUCAO DO PROGRAMA.	 
		#time.sleep(60) # AGUARDA 60 SEGUNDOS ANTES DE REINICIAR O PROGRAMA