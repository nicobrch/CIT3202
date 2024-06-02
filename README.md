# Multi-functional LLM Agent 🤖

This project consists of a Multi-functional LLM Agent using the latest GPT LLM model, that's cappable of doing function calling such as SQL queries and similarity search on documents, all of that hosted on a Postgres database using the pgvector extension.\\

As of now, it's presented as a costumer service solution for the e-commerce "Geekz", answering questions such as FAQ and product information from the existing database, given a web interface using the Streamlit framework.

## Dependencies 🛠️

<p align="center"><img src="https://static.vecteezy.com/system/resources/previews/022/227/364/non_2x/openai-chatgpt-logo-icon-free-png.png" alt="GPT" height="48"> <img src="https://www.freecodecamp.org/news/content/images/2024/03/1700940849777.png" alt="Langchain" height="48"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1200px-Postgresql_elephant.svg.png" alt="Postgres" height="48"> <img src="https://seeklogo.com/images/S/supabase-logo-DCC676FFE2-seeklogo.com.png" alt="Supabase" height="48"></p>

## Run 🚀

This project runs on two external providers, GPT for the text generation and Supabase for the database hosting solution. Considering this, we need to create a .env file with the following format:

```env
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
```

Then, we can run the application by executing the following commands:

```bash
pip install -r requirements.txt    # Install python dependencies
cd src                             # Move to src directory
streamlit run app.py               # Run web interface
```

## Modifying documents 📄

The docs shall be in `.txt` format in the `docs` directory. Make sure to tokenize the documents first using `tokenizer.py`. Then, we use GPT's embedding model to transform the documents into vectors and finally we load the documents into the vector database.
