# Scraper Placa e Renavam

## Instalação

```sh
conda create -n scraper-placa-renavam python=3.6.12
conda activate scraper-placa-renavam
pip install -r requirements
```

## Execução

* Alterar o user data dir para a pasta desejada.
    options.add_argument('user-data-dir=<Seu Diretorio>')
* Rodar o script 
    ```sh
    python main.py
    ```