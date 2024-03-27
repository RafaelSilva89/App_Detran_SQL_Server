# https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html
# https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent
import pyodbc
import os
import streamlit as st
import pandas    as pd
#from langchain.llms                              import OpenAI
#from langchain_experimental.agents               import create_pandas_dataframe_agent
#from langchain_openai                            import OpenAI
from langchain.agents.agent_types                 import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai                             import ChatOpenAI
from translate                                    import Translator
from htmlTemplates                                import css, bot_template, user_template
from dotenv                                       import load_dotenv

def get_query():
    input_text = st.chat_input("Ask a question about your documents...")
    return input_text

if 'historico' not in st.session_state:
    st.session_state['historico'] = []

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def chat_rh(question, api_key, driver, server, database, uid, pwd, table_name):
    #llm = OpenAI(api_key=api_key)
    #agent = create_pandas_dataframe_agent(llm, dataframe, verbose=True)
    #agent = create_pandas_dataframe_agent(OpenAI(temperature=0), dataframe, verbose=True)

    dados_conexao = (f"Driver={driver};"
                     f"Server={server};"
                     f"Database={database};"
                     f"UID={uid};"
                     f"PWD={pwd};")
    conn = pyodbc.connect(dados_conexao)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    resultados = cursor.fetchall()
    resultados_em_listas = [list(tupla) for tupla in resultados]
    nomes_colunas = [descricao[0] for descricao in cursor.description]
    dataframe = pd.DataFrame(resultados_em_listas, columns=nomes_colunas)

    for coluna in dataframe.columns:
        # Tentativa de converter a coluna para numérico, com erros resultando em NaN
        coluna_numerica = pd.to_numeric(dataframe[coluna], errors='coerce')
        # Se nenhum valor foi convertido para NaN, significa que todos podem ser convertidos para inteiros
        if not coluna_numerica.isnull().any():
            dataframe[coluna] = coluna_numerica.astype(int)
    #gpt-3.5-turbo-0125 - gpt-3.5-turbo-0613
    agent = create_pandas_dataframe_agent(ChatOpenAI(api_key=api_key, temperature=0, model="gpt-3.5-turbo-0125"),
                                          dataframe, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS, )
    answer = agent.run(question.upper())

    conn.close()
    return answer

def add_to_history(question, answer):
    st.session_state['chat_history'].append({'pergunta': question, 'resposta': answer})

st.set_page_config(
    page_title="Chat SQL Server",
    page_icon="🚀",
)
def main():
    load_dotenv()
    st.title("Chat SQL Server 🚀")
    st.write(css, unsafe_allow_html=True)
    with st.sidebar:
        #st.sidebar.header("Configurações")

        api_key = os.getenv("OPENAI_API_KEY")
        #api_key = st.sidebar.text_input("Chave da API:", "insira_sua_chave_aqui", type="password")

        server = st.sidebar.text_input("Chave do Server:", "insira_sua_chave_aqui")
        driver = st.sidebar.text_input("Chave do Driver:", "insira_sua_chave_aqui")
        database = st.sidebar.text_input("Chave do Database:", "insira_sua_chave_aqui")
        uid = st.sidebar.text_input("Chave do UID:", "insira_sua_chave_aqui")
        pwd = st.sidebar.text_input("Chave do PWD:", "insira_sua_chave_aqui", type="password")
        table_name = st.sidebar.text_input("Nome da tabela:", "insira_sua_chave_aqui")

        st.markdown('''
                        - [Streamlit](https://streamlit.io/)
                        - [LangChain](https://python.langchain.com/)
                        - [OpenAI](https://platform.openai.com/docs/models) LLM Model
                        - [Pandas Dataframe](https://python.langchain.com/docs/integrations/toolkits/pandas)
                        ''')
        #st.write('Also check out my portfolio for amazing content [Rafael Silva](https://rafaelsilva89.github.io/portfolioProjetos/#)')

    question = get_query()

    if api_key != "insira_sua_chave_aqui" and all(
            variable is not None and variable != "" for variable in [driver, server, database, uid, pwd, table_name]):
        if isinstance(question, str):  # Verifica se question é uma string
            try:
                answer = chat_rh(question, api_key, driver, server, database, uid, pwd, table_name)
                translator = Translator(to_lang='pt')
                translated_response = translator.translate(answer)
                add_to_history(question, translated_response)
            except Exception as e:
                st.error(f"Erro ao executar a consulta: {str(e)}")
    else:
        st.warning("Por favor, preencha todos os campos.")

    # Exibir histórico de conversas
    for item in st.session_state['chat_history']:
        st.write(user_template.replace("{{MSG}}", item['pergunta']), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", item['resposta']), unsafe_allow_html=True)

if __name__ == "__main__":
    main()