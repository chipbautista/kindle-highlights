# 📖✏️ Kindle Highlights: From My Clippings to Streamlit

This project implements an end-to-end project that:
1. parses book highlights from Kindle's `My Clippings.txt` file
2. stores them in a database
3. extracts book metadata from [Google Books API](https://developers.google.com/books)
4. runs topic modeling (and other analytics) transforms on them
5. and displays the data in a Streamlit app using [Streamlit Cloud](https://streamlit.io/cloud) free hosting.

## 🛠 Setup
### Packages
Main packages used are: Dagster, SQLAlchemy, pandas, scikit-learn, and Streamlit.
This project uses Poetry as its package manager.

Dependencies are documented in `pyproject.toml`, and specific versions are pinned in `poetry.lock`.

To install, run **`poetry install`**

Once installed, activate the virtual environment: **`poetry shell`**

### SQLite DB and clippings folder
By default, this project uses SQLite as its database, and will look for Kindle's `My Clippings.txt` file in `clippings_dropbox` folder. 

Run **`make init`** to initialize a `highlights.db` file and create a `clippings_dropbox` folder.
Afterwards, copy your `My Clippings.txt` file to the created folder.

### Env variables and secrets
Setup **env variables**: creating a `.env` file. See `.env.example` for the variables.

Setup **Streamlit secrets**: editing the `.secrets.toml.example` file, then move and rename it to `.streamlit/secrets.toml`

### For deployment
Deploying an app additionally requires the ff.:
1. An AWS service account that allows read/writes to S3.
2. A [Streamlit Cloud](https://streamlit.io/cloud) account

In Streamlit Cloud UI, copy the contents of your local `secrets.toml` file and set `ENV` to `'prod'`


## 🗂 Folder Structure
- `etl/` - contains [Dagster](https://dagster.io) pipeline code
- `src/` - contains [SQLAlchemy](https://www.sqlalchemy.org) database models and migrations
- `pages/` - contains Streamlit pages, following [Streamlit's multipage format](https://blog.streamlit.io/introducing-multipage-apps/)

# Running the whole thing
## 🔁 Run Pipelines
There are three pipelines:
1. `import_kindle_clippings` - parses the most recent file in `clippings_dropbox` folder (by default), cleans up some text, and loads the data into an SQLite DB
2. `get_google_books_metadata` - extracts metadata from Google Books. This includes book cover, synopsis, etc.
3. `run_topic_modeling` - Uses [Top2Vec](https://github.com/ddangelov/Top2Vec) to vectorize and extract topic models from the highlights. Additionally transforms the embeddings to 2d vectors for plotting.

### Using dagit
Run `dagit -f etl/jobs.py`.
By default, this will open up the server on http://localhost:3000.

❗️ The above pipelines should be run in order.

## 🎈 Running the Streamlit app
### 💻 Locally
Simply run: `streamlit run Highlights.py`

### ☁️ On the cloud (using Streamlit Cloud)
Before deploying on the cloud, make sure you have copies of the DB and topic model files in your S3 bucket:
1. the SQLite DB file: (default `highlights.db`)
2. Topic model file: (default `models/topic_model`)
3. tSNE vectors file: (default `models/tsne_vectors.pkl`)

This will be automatically done if you set the `upload_to_s3` op configs to True when running pipelines #2 and #3 -- You can do this on the dagit Launchpad. Example config:
```
ops:
  upload_highlights_db_to_s3:
    config:
      upload_to_s3: True
```

If not, you can manually upload them like so:
- `aws s3 cp highlights.db s3://<YOUR BUCKET NAME HERE>/highlights.db`
- `aws s3 cp models/topic_model s3://<YOUR BUCKET NAME HERE>/topic_model`
- `aws s3 cp models/tsne_vectors.pkl s3://<YOUR BUCKET NAME HERE>/tsne_vectors.pkl`

assuming that you have your CLI configured to use AWS. If not, run `aws configure` first.

