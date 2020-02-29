# POODLE

Indexador específico de links na web.

<img src="https://user-images.githubusercontent.com/36716898/75551278-9ab9cb00-5a12-11ea-8158-458f2ba095b6.png" width="100%"></img>


## Descrição
Poodle é um software desenvolvido em Python para realizar a indexação de links de uma forma específica.

Para a realização de uma basta três informações são necessárias.

* Busca - palavra chave que será verificada nas páginas
* Inicio - url inicial, onde o algoritmo vai iniciar a busca.
* Camadas - Quantidade de camadas que o algoritmo vai visitar.


### Definição de camadas.

As camadas referem-se aos links que serão visitados pelo algoritmo, como mostra a descrição abaixo.

Ao visitar um site, o algoritmo localiza todos as urls que o site em questão faz referência, assim que o site em destaque for finalizado, as urls coletadas serão visitadas uma a uma, e assim sucessivamente até que o número de camadas alcance o limite e todos as urls coletadas sejam visitadas.

Observe a imagem abaixo, a cada site visitado novas urls são encontradas. O primeiro site, ou seja, o início foi apelidado de **a**, a cada camada percorrida uma nova letra é adicionada ao final, definindo quantas camadas foram percorridas, e qual a camada mãe.

<img src="https://user-images.githubusercontent.com/36716898/75596066-b30b0380-5a6d-11ea-9749-b8b3a39b0456.png" width="100%"></img>


## Screenshots



### Página inicial

Página onde a busca é realizada.

<img src="https://user-images.githubusercontent.com/36716898/75551278-9ab9cb00-5a12-11ea-8158-458f2ba095b6.png" width="100%"></img>

Página inicial com uma camada acrescentada. 

<img src="https://user-images.githubusercontent.com/36716898/75551277-9a213480-5a12-11ea-935f-ed16500a63b6.png" width="100%"></img>

### Apresentação

Apresentação dos resultados encontrados.

<img src="https://user-images.githubusercontent.com/36716898/75551276-9a213480-5a12-11ea-9182-fc7697535ecc.png" width="100%"></img>

### Log

Registro de todos os sites visitados pelo algoritmo.

<img src="https://user-images.githubusercontent.com/36716898/75551272-98f00780-5a12-11ea-937c-87b2f797a038.png" width="100%"></img>

