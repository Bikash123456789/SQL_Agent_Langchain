import os
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env
load_dotenv()

# Load OpenAI API Key
openai_key = os.getenv("OPENAI_API_KEY")

# Load Snowflake credentials
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

# Build the Snowflake SQLAlchemy URI
snowflake_uri = (
    f"snowflake://{quote_plus(user)}:{quote_plus(password)}@{account}/"
    f"{database}/{schema}?warehouse={warehouse}"
)


# Replace SQLite with Snowflake here
db = SQLDatabase.from_uri(snowflake_uri)

# Load LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_key)

# Create LangChain SQL Agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)


# Interface to call from FastAPI or Streamlit
def run_query(user_input: str) -> str:
    try:
        result = agent_executor.run(user_input)
        return result
    except Exception as e:
        return f"Error : {str(e)}"
