# Car-Insurance-API

**Car Insurance API** este o aplicație web dezvoltată în **Flask**, care gestionează mașini, proprietari, polițe de asigurare și reclamații auto.  
Include toate endpointurile cerute în specificație, testare automată și un job în fundal care verifică polițele expirate în ziua curentă folosind **APScheduler**.

## Funcționalități principale
- Gestionare proprietari și mașini
- Polițe de asigurare (start_date, end_date, provider)
- Reclamații (date, descriere, sumă, auto `created_at`)
- Verificare valabilitate poliță la o dată (`/insurance-valid`)
- Istoric mașină (polițe + reclamații, în ordine cronologică)
- Job de fundal care detectează polițele expirate (`policy_expired`)
- Testare automată cu `pytest`

 ## Stack tehnic

- **Flask**
- **SQLAlchemy**
- **Alembic** 
- **APScheduler**
- **Pydantic**
- **pytest**
- **SQLite**

## Instalare și rulare

### 1. Instalează dependențele
pip install -r requirements.txt

### 2. Configurează fișierul .env
DATABASE_URL=sqlite:///./car_insurance.db
SCHEDULER_ENABLED=true
LOG_LEVEL=INFO

### 3. Rulează aplicația
flask run

## Testare automată
pytest -q

## Scheduler (job automat)
La pornirea aplicației (flask run), APScheduler rulează un job la fiecare 10 minute.
Jobul detectează polițele care expiră în ziua curentă.
