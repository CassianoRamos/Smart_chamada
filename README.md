# Sistema de Controle de Presença com Raspberry Pi

## Descrição do Projeto

Este projeto visa otimizar o processo de chamada de presença nas salas de aula, utilizando um sistema automatizado com leitor de digital (ou RFID no MVP) e uma interface simples. O sistema permitirá que professores e alunos registrem suas entradas e saídas de forma prática, sem a necessidade de interromper as atividades para realizar a chamada manualmente.

## Objetivo Geral

Automatizar o sistema de chamada nas aulas, substituindo o método tradicional de verificação de presença por um processo mais eficiente, baseado em leitura biométrica ou RFID.

## Objetivos Específicos

- **Automatizar o processo de chamada**: Utilizar um leitor de digital (ou RFID) e uma tela de confirmação para registrar a presença de alunos e professores ao entrar e sair da sala.
- **Integração com Raspberry Pi**: Implementar o sistema em uma Raspberry Pi 4, possibilitando a comunicação entre o leitor de digital (ou RFID) e o banco de dados que armazenará as informações de presença.
- **Modalidades de aula**: O professor poderá definir a modalidade da aula (normal, prova ou trabalho) no início da sessão.
- **Interface Simples**: A tela touch será utilizada no produto final para confirmar informações e definir horários.

## Descrição do Produto Final

O sistema será composto por:

- **Raspberry Pi 4**
- **Leitor de Digital**: Os alunos e professores escanearão suas digitais para registrar entrada e saída.
- **Tela Touch**: Usada pelo professor para definir o horário de início e término da aula, além da modalidade.
- **Banco de Dados**: Para armazenamento das digitais e informações de presença.

### Funcionamento

1. Ao entrar na sala, o professor escaneia sua digital e informa o horário de início e a modalidade da aula (prova, trabalho ou aula normal).
2. Os alunos escaneiam suas digitais ao entrar na sala para registrar sua presença.
3. Para registrar a saída, basta escanear a digital novamente e marcar a opção de saída.
4. Ao final da aula, o professor escaneia sua digital para registrar o término da aula e contabilizar automaticamente as presenças.

## MVP (Produto Mínimo Viável)

O MVP será uma versão simplificada do sistema completo, com as seguintes características:

- Substituição do **leitor de digital** por **RFID**, utilizando TAGs para alunos e professores.
- **Sem tela touch**: As opções de modalidade e horário serão configuradas manualmente.
- **Raspberry Pi 4** com integração ao leitor de RFID.

## Tecnologias Utilizadas

- **Raspberry Pi 4**
- **Leitor de Digital** ou **RFID** (para o MVP)
- **Python** para desenvolvimento do sistema
- **Flask** (se houver necessidade de interface web)
- **Banco de Dados** para armazenamento de digitais e presenças


