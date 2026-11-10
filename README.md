\# 🌿 KrishiMitra: AI crop doctor for farmers



Take a photo of a sick leaf, get the likely disease, simple treatment steps and spoken advice in \*\*English, Hindi or Kannada\*\*.



\## The problem

Small farmers often can't identify crop diseases in time. Expert help is far away, and most apps are English-only and text-heavy. FAO estimates pests and plant diseases destroy up to 40% of food crops globally every year.



\## What it does

1\. The farmer uploads or captures a leaf photo and picks a language.

2\. A vision AI model identifies the crop and disease with a confidence score.

3\. The app shows symptoms, treatment steps and a safety warning in the chosen language.

4\. The advice is read aloud (cloud text-to-speech), so no reading is needed.

5\. Low-confidence results show a helpline number instead of guessing.



\## Tech stack

\- \*\*Backend:\*\* Python, FastAPI

\- \*\*AI:\*\* Google Gemini vision models (with automatic fallback across models)

\- \*\*Voice:\*\* gTTS (Kannada, Hindi, English)

\- \*\*Frontend:\*\* single-page mobile-friendly HTML/JS



\## Run it locally

```bash

git clone https://github.com/AnanyaK-arch12/krishimitra.git

cd krishimitra

python -m venv venv

venv\\Scripts\\activate          # Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

```

Create a `.env` file (see `.env.example`) with your free key from https://aistudio.google.com/apikey:

```

GEMINI\_API\_KEY=your\_key\_here

```

Start the app and open http://127.0.0.1:8000/app/

```bash

uvicorn backend.main:app --reload

```



\## Screenshots

\_Add screenshots here.\_



\## Limitations and safety

\- Diagnosis is a suggestion, not a certified result. The app never gives pesticide doses and advises confirming with a local agriculture officer.

\- Currently supports tomato and paddy leaves.

\- Needs an internet connection. Offline mode is on the roadmap.



\## Roadmap

Voice questions (mic input), more crops, offline mode, weather alerts, government scheme information.



\## Team

Team Members 
1.Ananya K
2.Gayathri
3.Chaithra S Uchil

Demo video link : https://youtu.be/NBKBavWeYqc

