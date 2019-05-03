class PadronizaLote(object):
	def __init__(self):
		return 1

	#para tratar o lote deixando ele visualmente melhor e removendo informacoes que nao utilizamos para lote.
	def padronizar(lotesemtratar):
		lotetratado= lotesemtratar.replace('-CARTA','')
		lotetratado= lotetratado.replace('CARTA','')# exemplos para outros casos
		lotetratado= lotetratado.replace(' ','')#todos os espaços existentes, principalmente os casos "BN  
		lotetratado= str(lotetratado[:2]) + ' ' + str(lotetratado[2:])# Coloca um espaco entre Tipo e Lote
		return lotetratado
