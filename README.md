# CV Parser

Upload a PDF CV and get the name, email, education, experience and skills back as structured data.

## How it works

```
Streamlit (your computer) -> ngrok -> FastAPI on Kaggle -> Mistral-Nemo -> JSON
```

The model runs on Kaggle GPUs. The Streamlit app runs locally and sends the PDF to Kaggle through an ngrok tunnel.

## Stack

LangChain, Mistral-Nemo-Instruct-2407, FastAPI, ngrok, Streamlit

## Setup

**On Kaggle**
1. Open `kaggle_notebook.ipynb` in a Kaggle notebook.
2. Turn Internet **On** and set the accelerator to **GPU T4 x2**.
3. Add a secret named `NGROK_TOKEN` (your token from dashboard.ngrok.com) and attach it to the notebook.
4. Run all cells and copy the URL printed by the last cell.

**On your computer**
```bash
pip install -r requirements.txt
streamlit run app.py
```
1. Open **Connection** and paste the ngrok URL.
2. Upload a PDF (try `test_cv_omar_hassan.pdf`).
3. Click **PARSE!**.

## Output

```json
{
  "full_name": "Omar Hassan",
  "email": "omar.hassan@example.com",
  "education": ["..."],
  "skills": ["..."],
  "experience": ["..."]
}
```

## Limits

- Needs a running Kaggle session. A new session gives a new URL.
- A parse takes about 1 to 3 minutes.
- Tested on a small set of CVs. Accuracy is not measured yet.

## Next steps

- Test on more CV formats and measure accuracy
- Add a JSON download button
- Support several CVs at once
