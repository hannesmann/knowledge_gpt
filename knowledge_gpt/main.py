# Hur kör man skiten utan streamlit? Jag har problem med package management som jag inte förstår mig på.
import streamlit as st

# Programmet är nu nedbantat till det yttersta. Ingen GUI används och inga funktioner som är beroende av streamlit används längre.
# Jag vill eventuellt snygga till lite här inne senare, men som det är nu funkar det åtminstone.
from io import BytesIO

# Ingen av dessa har något med Streamlit att göra. Den funktionen i core some hade med caching att göra implementerade en del streamlitprylar, men verkar inte vara nödvändiga för att programmet skall fungera.
from knowledge_gpt.core.parsing import read_file
from knowledge_gpt.core.chunking import chunk_file
from knowledge_gpt.core.embedding import embed_files
from knowledge_gpt.core.qa import query_folder
from knowledge_gpt.core.utils import get_llm

# Behåller detta för tydlighetens skull.
EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

def knowledge_gpt_test(openai_api_key):
    # Detta är bara en fil som ligger i samma folder för tillfället, men den kan givetvis skickas in lite hur som helst.
    uploaded_file = open('testdocu.pdf', "rb")

    # Självförklarligt.
    model = "gpt-4"

    # Detta är överblivet sedan jag tog bort streamlit, men det är bara booleska värden som jag låtit ligga här tills vidare.
    # Överväg att helt enkelt ta bort skiten helt från att behövas i query_folder().
    return_all_chunks = 1
    show_full_doc = 1

    # Felhantering. Det fanns mer sådan i källkoden men det sköttes via streamlit och inte med Exception handling på det här viset.
    try:
        file = read_file(uploaded_file)
    except Exception as e:
        print("FILE READ ERROR: ", e)

    # Stänger den uppladdade filen här då efter föregående steg behöver den inte vara öppen längre.
    uploaded_file.close()

    # Chonky boi.
    chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

    folder_index = embed_files(
            files=[chunked_file],
            embedding=EMBEDDING if model != "debug" else "debug",
            vector_store=VECTOR_STORE if model != "debug" else "debug",
            openai_api_key=openai_api_key,
            )

    # Detta är vår query, helt enkelt en textsträng. Den kan såklart skickas in dynamiskt om man önskar, men är hårdkodad för testsyften atm.
    query = "tell me about this document and then include an unrelated, short joke at the end. Finish by including the word mousepad at the very end of your response."

    # Call till get_llm() som ger oss all vi vill ha. Upprepade calls med andra queries kan såklart göras.
    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
    result = query_folder(
            folder_index=folder_index,
            query=query,
            return_all=return_all_chunks,
            llm=llm,
        )

    return result.answer

