import re


class ExtratorURL:
    def __init__(self, url):
        self.url = self.sanitiza_url(url) # 'Sanitiza' para trazer a URL em formato valido
        self.valida_url()

    def sanitiza_url(self, url): #Retornar formato dispensando espaços vazios
        if type(url) == str:
            return url.strip()
        else:
            return ""

    def valida_url(self):  #Verificar se a URL está vazia ou não
        if not self.url:
            raise ValueError("A URL está vazia")

        padrao_url = re.compile('(http(s)?://)?(www.)?bytebank.com(.br)?/cambio')
        match = padrao_url.match(self.url)
        if not match:
            raise ValueError("A URL não é válida.")

    def get_url_base(self):
        indice_interrogacao = self.url.find('?') # '?' Indice da URL - que separa URL base e URL parametros
        url_base = self.url[:indice_interrogacao]  #Pegar URL base (do começo até o indice interrogação)
        return url_base

    def get_url_parametros(self):
        indice_interrogacao = self.url.find('?') # '?' Indice da URL - que separa URL base e URL parametros
        url_parametros = self.url[indice_interrogacao + 1:] #Pegar URL de parametros (uma posição após o indice interrogação até o final da URL)
        return url_parametros

    def get_valor_parametro(self, parametro_busca):
        indice_parametro = self.get_url_parametros().find(parametro_busca) #Na URL parametros, pegar o parametro de busca
        indice_valor = indice_parametro + len(parametro_busca) + 1  #Pegar o resultado da busca, parametro de busca + 1 posição
        indice_e_comercial = self.get_url_parametros().find('&', indice_valor)
        if indice_e_comercial == -1:
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_e_comercial]
        return valor

url = "bytebank.com/cambio?quantidade=100&moedaOrigem=real&moedaDestino=dolar"
extrator_url = ExtratorURL(url)

VALOR_DOLAR = 4.96 # 1 dólar = 4.96 reais
moeda_origem = extrator_url.get_valor_parametro("moedaOrigem")
moeda_destino = extrator_url.get_valor_parametro("moedaDestino")
quantidade = extrator_url.get_valor_parametro("quantidade")

valor_usuario = (float(quantidade))
valor_final = (float(valor_usuario / VALOR_DOLAR))

print("O valor de {} reais convertidos em dólar será de {:.2f}".format(valor_usuario, valor_final))
