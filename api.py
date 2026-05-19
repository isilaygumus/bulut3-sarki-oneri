from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from google.cloud import bigquery
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

client = bigquery.Client(project="sarki-oneri")
query = "SELECT * FROM `sarki-oneri.sarki_dataset.sarkilar`"
df = client.query(query).to_dataframe()

df = df.dropna().reset_index(drop=True)
silinecekler = ['Unnamed: 0', 'id', 'Track', 'Artist', 'Album', 'mode', 'key', 'Key']
dusurulecekler = [col for col in silinecekler if col in df.columns]
ozellik_df = df.drop(columns=dusurulecekler)
sayisal_sutunlar = ozellik_df.select_dtypes(include=['float64', 'int64']).columns

matris = cosine_similarity(MinMaxScaler().fit_transform(df[sayisal_sutunlar]))

@app.get("/")
def anasayfa():
    return FileResponse('index.html')


@app.get("/oner/{sarki_adi}")
def oner(sarki_adi: str):
    if sarki_adi not in df['Track'].values:
        return {"oneriler": []}

    idx = df[df['Track'] == sarki_adi].index[0]
    skorlar = sorted(list(enumerate(matris[idx])),
                     key=lambda x:x[1],
                     reverse=True)[1:11]

    return {"oneriler": [f"{df.iloc[i[0]]['Track']} - {df.iloc[i[0]]['Artist']}" for i in skorlar]}
