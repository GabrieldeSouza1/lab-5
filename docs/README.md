# Relatório
Relatório final para o laboratório da criação de um estudo controlado para a comparação das APIs GrafhQL vs REST.

## Introdução
A linguagem de consulta GraphQL, proposta pelo Facebook como metodologia de implementação de APIs Web, representa uma alternativa às populares APIs REST. Baseada em grafos, GraphQL permite que usuários consultem bancos de dados na forma de _schemas_, possibilitando exportar a base e realizar consultas em um formato definido pelo fornecedor da API. Por outro lado, APIs REST são baseadas em _endpoints_: operações pré-definidas que podem ser chamadas por clientes que desejam consultar, deletar, atualizar ou escrever um dado na base. Desde o seu surgimento, vários sistemas têm migrado de soluções REST para GraphQL, mantendo compatibilidade com REST, mas oferecendo os benefícios da nova linguagem de consulta proposta. Entretanto, os reais benefícios da adoção de GraphQL em detrimento de REST ainda não estão claros.

Nesse contexto, este estudo visa realizar um experimento controlado para avaliar quantitativamente os benefícios da adoção de uma API GraphQL. Especificamente, este artigo busca responder às seguintes perguntas:
  1. **RQ1:** As respostas às consultas GraphQL são mais rápidas que as respostas às consultas REST?
  2. **RQ2:** As respostas às consultas GraphQL têm tamanho menor que as respostas às consultas REST?

Para responder as perguntas de pesquisa, foram formuladas as seguintes hipóteses:

### Hipóteses Nula e Alternativa

#### Hipótese Nula (H0):
  - RQ1 H0: Não há diferença significativa no tempo de resposta entre consultas GraphQL e REST.
  - RQ2 H0: Não há diferença significativa no tamanho das respostas entre consultas GraphQL e REST.
   
#### Hipótese Alternativa (H1):
  - RQ1 H1: Há uma diferença significativa no tempo de resposta entre consultas GraphQL e REST.
  - RQ2 H1: Há uma diferença significativa no tamanho das respostas entre consultas GraphQL e REST.

## Metodologia
A pesquisa realizada neste estudo possui caráter quantitativo e descritivo. Busca-se medir, a partir dos valores de métricas coletadas, o desempenho de APIs GraphQL em comparação com APIs REST, especificamente em termos de tempo de resposta e tamanho das respostas. O caráter quantitativo está presente, pois os valores das métricas coletadas são analisados e traduzidos em números para se chegar a possíveis conclusões sobre a eficiência e eficácia das duas abordagens de API. Para a realização da pesquisa, foi contruído um experimento controlado especificado nas seguintes subseções:

### Desenho do experimento
O desenho do experimento visa estabelecer uma metodologia clara e replicável para avaliar o desempenho das APIs GraphQL e REST. Neste estudo, foram utilizadas consultas específicas à API do GitHub para comparar o tempo de resposta e o tamanho das respostas entre os dois tipos de API.

#### Variáveis do Experimento
As variáveis do experimento foram selecionadas para permitir uma comparação direta e objetiva entre as APIs GraphQL e REST. As variáveis dependentes e independentes do estudo são:

##### Variáveis Dependentes:
  - **Tempo de resposta:** Tempo necessário para a API retornar uma resposta após o recebimento de uma consulta (medido em milissegundos);
  - **Tamanho da resposta:** Tamanho total dos dados retornados pela API em resposta a uma consulta (medido em bytes).
    
##### Variáveis Independentes:
  - **Tipo de API (GraphQL ou REST)**: Consulta realizada utilizando GraphQL ou REST;
  - **Tipo de consulta**: Complexidade e quantidade de dados requisitados.

#### Tratamentos
Os tratamentos no experimento referem-se às diferentes condições sob as quais as medições serão realizadas. Neste estudo, foram definidas duas consultas equivalentes realizadas tanto via GraphQL quanto via REST, separadas por nível de complexidade para abranger vários escopos. Os tratamentos são:
  - **Query Simples:** Buscar o número de _Pull Request_ dos 100 repositórios mais populares do GitHub, além do nome da organização e do reposiório e número de estrelas;
  - **Query Complexa:** Buscar alguns dados dos 100 primeiros _Pull Requests_ do repositório mais popular no presente momento, o [FreeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp).

A consulta simples envolve a requisição de poucos campos à API, enquanto consultas complexas envolvem vários campos com relacionamentos e, portanto, retornam mais dados.

#### Objetivos Experimentais
Os objetos experimentais são os _endpoints_ da API do GitHub usados nas consultas especificadas.

#### Tipo de Projeto Experimental
O experimento segue um projeto do tipo _crossing_, em que cada _endpoint_ é consultado tanto via GraphQL quanto via REST. Esta abordagem permite comparar diretamente os resultados das duas tecnologias de API em condições controladas.

#### Quantidade de Medições
Para garantir a validade dos resultados, foram realizadas pelo menos 10 consultas em cada método (GraphQL e REST). A média das consultas foi calculada para obter uma representação precisa dos tempos de resposta e tamanhos das respostas. Essa quantidade de medições é suficiente para minimizar a influência de variáveis externas e fornecer uma base sólida para a análise estatística.

#### Ameaças à Validade
As ameaças à validade são fatores que podem comprometer a precisão e a generalização dos resultados do experimento. No contexto deste estudo, as ameaças à validade identificadas são:

##### Ameaças à Validade Interna:
  - **Variações no Ambiente:** O desempenho das APIs pode variar de acordo com fatores não controláveis como a carga do servidor, latência da rede e disponibilidade dos recursos.
    
##### Ameaças à Validade Externa:
  - **Generalização Limitada:** Os resultados são específicos para a API do GitHub e podem não se aplicar a outras APIs ou contextos.




