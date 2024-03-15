from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def get_text(file):
  with open(file) as f:
    text = f.read()
    f.close()
  return text


def get_text_chunks(text):
  text_splitter = CharacterTextSplitter(separator="\n",
                                        chunk_size=1000,
                                        chunk_overlap=200,
                                        length_function=len)
  chunks = text_splitter.split_text(text)
  return chunks


def get_vectorstore(text_chunks):
  embeddings = OpenAIEmbeddings()
  vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
  return vectorstore


def get_conversation_chain(vectorstore):
  llm = ChatOpenAI()
  memory = ConversationBufferMemory(memory_key='chat_history',
                                    return_messages=True)
  conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, retriever=vectorstore.as_retriever(), memory=memory)
  return conversation_chain


def handle_userinput(conversation, user_question):
  response = conversation({'question': user_question})
  chat_history = response['chat_history']
  return chat_history


def query(user_question):
  file = 'about_company.txt'

  raw_text = get_text(file)
  text_chunks = get_text_chunks(raw_text)
  vectorstore = get_vectorstore(text_chunks)
  conversation = get_conversation_chain(vectorstore)
  chat_history = handle_userinput(conversation, user_question)
  output = chat_history[-1].content

  return output
