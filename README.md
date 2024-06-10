
# LAB 05 : GraphQL vs REST: Um Experimento Controlado

## Enunciado:

### Introdução
A linguagem de consulta GraphQL, proposta pelo Facebook como metodologia de implementação de APIs Web, representa uma alternativa às populares APIs REST. Baseada em grafos, a linguagem permite que usuários consultem banco de dados na forma de schemas, de modo que se possa exportar a base e realizar consultas num formato definido pelo fornecedor da API. Por outro lado, APIs criados com base em abordagens REST baseiam-se em endpoints: operações pré-definidas que podem ser chamadas por clientes que desejam consultar, deletar, atualizar ou escrever um dado na base. Desde o seu surgimento, vários sistemas realizaram a migração entre ambas as soluções, mantendo soluções compatíveis REST, mas oferecendo os benefícios da nova linguagem de consulta proposta. Entretanto, **não está claro quais os reais benefícios da adoção de uma API QraphQL em detrimento de uma API REST.** Nesse contexto, o objetivo deste laboratório é realizar um **experimento controlado** para avaliar quantitativamente os benefícios da adoção de uma API GraphQL. Especificamente, as seguintes perguntas devem ser respondidas:

- **RQ1.** Respostas à consultas GraphQL são mais rápidas que respostas à consultas REST?
- **RQ2.** Respostas à consultas GraphQL tem tamanho menor que respostas à consultas REST?

### Metodologia

Para tanto, espera-se que a cada sprint o grupo realize algumas das seguintes etapas:

#### 1. Desenho do Experimento

Nessa etapa, realize o desenho do seu experimento, definindo (pelo menos) cada um dos tópicos a seguir:
 - Hipóteses Nula e Alternativa
 - Variáveis Dependentes
 - Variáveis Independentes
 - Tratamentos
 - Objetos Experimentais
 - Tipo de Projeto Experimental
 - Quantidade de Medições
 - Ameaças à Validade
 
#### 2. Preparação do Experimento
Em seguida, realize o que for necessário para aplicação dos tratamentos (desenvolvimento de scripts, consultas, escolha de bibliotecas, entre outros). Monte todo o cenário experimental, com base na definição anterior. 

#### 3. Execução do Experimento
Siga cuidadosamente os passos do plano, realizando as medições e aplicando os tratamentos.

#### 4. Análise de Resultados
Inicialmente, realize uma revisão dos valores obtidos, com objetivo de validar as suas medições e observar se algum valor parece fora do esperado. Realize ajustes, se necessário.

Em seguida, analise o conjunto de dados com os princípios estatísticos mais adequados.

#### 5. Relatório Final
Por fim, elabore um documento que apresente (i) uma introdução que descreva as hipóteses levantadas; (ii) a metodologia que você utilizou para executar seu experimento, detalhando todos os aspectos necessários para possibilitar a reprodução e replicação do seu experimento (inclua o ambiente em que os trials foram realizados); (iii) os resultados obtidos para cada uma das perguntas, bem como as respostas estatísticas obtidas; (iv) a discussão final sobre os resultados obtidos.

### Processo de Desenvolvimento
Sprints e Datas de Entrega:
#### Lab05S01:
  - Desenho do experimento, (Passo 1);
  - Peparação (Passo 2).
#### Lab05S02:
- Execução do experimento (Passos 3);
- Análise dos resultados e produção do relatório final (Passos 4 e 5).

**Prazo final:** 19/06 | **Valor total:** 20 pontos

## Integrantes do grupo:

* Frederico dos Santos
* Gabriel de Souza
* Gabriel Lima de Souza
* Nikolas Augusto Vieira Louret

## Artefatos:

* [Relatório](docs/README.md)
* [Scripts](scripts)
* [Conjunto de dados](scripts/dataset)
  
