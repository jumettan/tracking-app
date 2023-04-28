# tracking-app
ohjelma on tehty Python 3.9.13 versiolla.
ohjelma seuraa pelaajan edistymistä
lataa tiedosto koneellesi.
siirry joko komentokehoteella tiedostoon tai avaa suoraan vscodessa.
kirjoita alla olevat komennot terminaaliin. tiedosto on sijainti näyttää kutakuinkin tältä(C:\jtn\jtn\tracking_app)
 python -m venv venv
venv\Scripts\activate
 pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
 uvicorn main:app --reload

 avaa alla oleva endpoint selaimeesi
# http://127.0.0.1:8000/docs
