# Calc_diluicao_automatico
 
# Aplicativo Geminni

## Descrição

O Aplicativo Geminni é uma aplicação de análise de imagens que permite ao usuário selecionar uma pasta contendo imagens e processá-las através de várias etapas, incluindo conversão para escala de cinza, aplicação de blur, detecção de bordas e linhas horizontais. O resultado final é exibido na interface do usuário.

## Funcionalidades

- **Seleção de Pasta:** Permite ao usuário selecionar uma pasta contendo imagens para análise.
- **Visualização de Imagens:** Exibe a imagem original e permite a navegação entre as imagens na pasta selecionada.
- **Processamento de Imagens:**
  - **Blur:** Aplica diferentes níveis de blur às imagens em escala de cinza.
  - **Contraste:** Aplica diferentes níveis de contraste às imagens com blur.
  - **Detecção de Bordas:** Detecta bordas nas imagens com contraste.
  - **Linhas Horizontais:** Detecta e exibe as maiores linhas horizontais nas imagens com bordas.
- **Exibição de Resultados:** Exibe a imagem final processada com as linhas horizontais detectadas.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `numpy`
  - `Pillow`
  - `opencv-python`
  - `flet`

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/aplicativo-geminni.git
   cd aplicativo-geminni
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

1. Execute o aplicativo:
   ```sh
   python aplicativo_geminni.py
   ```

2. Na interface do usuário, clique em "Selecionar Pasta" para escolher a pasta contendo as imagens que deseja analisar.

3. Navegue pelas imagens usando os botões "Imagem anterior" e "Próxima imagem".

4. Siga as etapas de processamento de imagem (blur, contraste, bordas, linhas horizontais) e visualize os resultados na interface.

## Estrutura do Código

- **Importações:** Importa todas as funções e bibliotecas necessárias do arquivo [`todas_bibliotecas_e_funcoes.py`].
- **Funções de Processamento:**
  - [`numpy_to_base64`]: Converte um array NumPy para uma imagem PNG em base64.
  - [`main`]: Função principal que configura a interface do usuário e define os manipuladores de eventos.
  - [`get_directory_result`]: Manipula a seleção de pasta e carrega as imagens.
  - [`proxima`] e [`anterior`]: Navega entre as imagens na pasta selecionada.
  - [`processar_blur`], [`processar_PB`], [`processar_vales`], [`processar_horizontal`], [`processar_imagem_final`]: Funções que aplicam diferentes etapas de processamento de imagem.
- **Elementos da Interface do Usuário:** Define os elementos da interface, como botões, colunas e linhas, e os adiciona à página.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato

Para mais informações, entre em contato com [seu-email@exemplo.com](mailto:seu-email@exemplo.com).