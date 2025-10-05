# Datalogger Multifuncional com Labrador 32

## 📖 Visão Geral

Este repositório contém o código-fonte e a documentação de um datalogger multifuncional desenvolvido para a placa de prototipagem **Labrador 32**. O projeto foi criado como parte da residência tecnológica **EmbarcaTech** no Instituto Federal do Piauí - Campus Picos.

O objetivo principal é monitorar, de forma autônoma, variáveis ambientais críticas (temperatura, umidade e luminosidade) em ambientes controlados, como uma granja, e registrar esses dados em um cartão microSD para análise posterior.

## ✨ Funcionalidades Principais

- **Coleta de Múltiplos Sensores**: Lê dados simultaneamente dos sensores **AHT10** (temperatura e umidade) e **BH1750** (luminosidade). 
- **Armazenamento Local**: Salva todas as leituras em um arquivo `.txt` em um cartão microSD, com timestamps precisos para cada registro.
- **Registro Periódico**: Realiza a coleta e o salvamento dos dados em intervalos de tempo configuráveis (o padrão é 60 segundos).
- **Robustez**: O script inclui tratamento de erros para falhas de leitura dos sensores e falhas na escrita do arquivo, garantindo a continuidade da operação.
- **Fácil Configuração**: As principais variáveis, como o barramento I2C, o intervalo de log e o caminho do cartão SD, podem ser facilmente alteradas no início do script.

## 🛠️ Hardware Utilizado

- **Placa de Processamento**: Labrador 32 
- **Sensor de Temperatura e Umidade**: AHT10 
- **Sensor de Luminosidade**: BH1750 
- **Módulo de Armazenamento**: Cartão MicroSD 

Ambos os sensores operam no barramento I2C (`/dev/i2c-2`), simplificando as conexões elétricas.

## 🔧 Como Utilizar

### Pré-requisitos

Certifique-se de que sua placa Labrador 32 tenha o Python 3 e as seguintes bibliotecas instaladas:

```bash
pip install smbus2 periphery
```

### Execução

1.  Clone este repositório para a sua placa:
    ```bash
    git clone https://github.com/MatheusGODZILLA/datalogger-multifuncional.git
    cd datalogger-multifuncional
    ```
2.  Verifique as variáveis de configuração no topo do arquivo `datalogger_matheus_teste.py` e ajuste o `SD_CARD_PATH` se necessário.
3.  Execute o script:
    ```bash
    python3 datalogger_matheus_teste.py
    ```
4.  O terminal exibirá as leituras em tempo real, e os dados serão salvos no arquivo `dados_sensores.txt` no cartão microSD. 
5.  Para encerrar a execução, pressione `Ctrl+C`. 

### Formato do Log

Cada linha no arquivo de log segue o formato:
`[DD-MM-YYYY HH:MM:SS] | Luminosidade: X.XX Lux | Temperatura: Y.Y C | Umidade: Z.Z %` 

## 💡 Desafios e Aprendizados

- Um dos principais desafios foi gerenciar a comunicação I2C com sensores que possuem diferentes requisitos de interação, o que levou ao uso de duas bibliotecas distintas: `smbus2` para o BH1750 e `periphery` para o AHT10. 

- Houve também uma tentativa inicial de integrar o sensor de distância **VL53L0X**, que foi abandonada devido à falta de documentação estável em Python para a plataforma, destacando a importância do suporte da comunidade no desenvolvimento de sistemas embarcados.

## 🚀 Melhorias Futuras

  - Adicionar conectividade Wi-Fi para enviar dados para uma plataforma de IoT (nuvem). 
  - Desenvolver um dashboard para visualização dos dados em tempo real. 
  - Implementar um sistema de alertas para notificar quando os sensores registrarem valores fora de uma faixa segura. 
