from zapv2 import ZAPv2
from pprint import pprint
import time, sys

# Cria uma instância do ZAPv2 config. para usar o ZAP Proxy rodando na URL digitada
zap = ZAPv2(proxies={'http': 'http://localhost:8061/'}) # Ex: http://localhost:8061/

# Limpa a sessão p/ evitar dados acumulados de execuções anteriores
zap.core.new_session(name=None, overwrite=True)

# Verifica se foram passados 2 argumentos (nome do script e o alvo)
if len(sys.argv) != 2:
    print('Passagem de argumentos insuficientes!')
    sys.exit(1)

# Segundo argumento passado é o alvo 
alvo = sys.argv[1]

try:
    # Faz uma requisição HTTP para garantir que o alvo está acessível pelo ZAP
    zap.urlopen(alvo)
except Exception as e:
    print(f'Não foi possível estabelecer uma conexão com o alvo {alvo} ==> {e}')
    sys.exit(1)

# Tempo de início
inicio = time.time()

# Inicia o processo de "spidering" (raspagem/mapeamento de links) no alvo 
id_spider = zap.spider.scan(alvo)
time.sleep(2)

# Aguarda processo de 'spidering' ser concluído
while int(zap.spider.status(id_spider)) < 100:
    print('Mapeamento em ' + str(zap.spider.status(id_spider)) + '%...') # SPIDER
    time.sleep(2)
print('Mapeamento concluído!')
time.sleep(5)

print('\nEscaneando alvo %s' % alvo)
# Inicia o processo de varredura de segurança
id_varredura = zap.ascan.scan(alvo)

# Aguarda varredura de segurança ativa ser concluída 
while int(zap.ascan.status(id_varredura)) < 100:
    print('Varredura em ' + str(zap.ascan.status(id_varredura)) + '%...')
    time.sleep(5)
print('Varredura conluída!')
print('\nHosts encontrados: ' + ', '.join(zap.core.hosts)) 

# Tempo de fim
fim = time.time()

zap.spider.stop(id_spider)
zap.ascan.stop(id_varredura)

# Calcula duração do tempo
tempo_total = (fim - inicio)/60
print(f'\nTempo total do processo: {tempo_total:.2f} min')

#print('\nAlertas de segurança:')
#pprint(zap.core.alerts())

# Gera relatório HTML com os resultados
html = zap.core.htmlreport()
with open('teste.html', 'w') as f:
    f.write(html)

print('\nRelatório gerado com sucesso!')
