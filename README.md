# Mini Internship Portal

MiniInternPortal – FastAPI və PostgreSQL istifadə edərək hazırlanmış, istifadəçilərin CV-lərini yüklədiyi, adminlərin isə bu CV-ləri yükləyə, statusunu dəyişə və AI köməyi ilə uyğunluq dərəcəsini təyin edə bildiyi bir internship platformasıdır.

🚀 Xüsusiyyətlər
📝 İstifadəçilər CV yükləyə bilər
📥 Admin CV-ni yükləyə və baxa bilər
🟢🟡🔴 Admin statusu (approved, rejected, pending) dəyişə bilər
🔐 Admin üçün JWT token ilə login/register sistemi
🤖 AI ilə CV uyğunluq dərəcəsi (cosine similarity + SentenceTransformer)

🛠 Texnologiyalar
Backend: Python, FastAPI
Database: PostgreSQL
AI: SentenceTransformer (all-MiniLM-L6-v2)
PDF Processing: pdfplumber
Auth: OAuth2 + JWT
Frontend üçün: CORS açıqdır (React/JS frontend ilə uyğun işləyir)

⚙️ Qurulum (Local)
1. .env faylı yaradın:
HOST=localhost
PORT=5432
DATABASE=miniinternportal
USER=postgres
PASSWORD=your_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

2. Əlavə Python paketlərini quraşdırın:
pip install fastapi uvicorn psycopg2-binary python-dotenv passlib[bcrypt] python-jose pdfplumber numpy sentence-transformers python-multipart

3. PostgreSQL verilənlər bazasını və cədvəlləri yaradın:
# database.py faylında qeyd olunan kodları açıb bir dəfə çalışdırın:
# CREATE DATABASE miniinternportal;
# CREATE TABLE applicants (...);
# CREATE TABLE admin (...);

📡 API Endpoint-lər
🔐 Admin
POST /admin_register – Admin qeydiyyat
POST /admin/login – Admin login (JWT token qaytarır)
GET /admin/applicants – Bütün müraciətləri görmək
GET /admin/applicants/{id} – Müraciət detalı
PUT /admin/applicants/{id}/status – Status dəyişmək
GET /admin/applicants/{id}/download – CV faylını yükləmək
Bu endpoint-lərə JWT token tələb olunur (Authorization: Bearer <token>)

👤 İstifadəçi
POST /submit – CV yüklə (FormData ilə: username, email, cv)

🤖 AI Uyğunluq Sistemi
POST /match – CV ilə job id uyğunluğunu ölç (FormData ilə job_id, cv)

İstifadə üçün vacancies.py faylında job_requirements dict olmalıdır. (Gələckdə daha rahat üsul ilə, məsələn DataBase ilə əvəzləmək mümkündür):
job_requirements = {
    1: {
        "title": "Backend Developer",
        "description": "Looking for someone with FastAPI, PostgreSQL skills..."
    },
    ...
}

🔐 Token Authentication (JWT)
Login sonrası dönən token frontend tərəfindən hər sorğuya Authorization başlığı ilə əlavə olunmalıdır:
Authorization: Bearer <your_token_here>

📂 Layihə Strukturu
.
├── main.py              # FastAPI tətbiqi
├── database.py          # PostgreSQL bağlantısı
├── security.py          # Hashing və JWT token funksiyaları
├── openaiapi.py         # CV oxuma və AI uyğunluq hesablaması
├── schemas.py           # Pydantic modellər
├── vacancies.py         # Job məlumatları (AI üçün)
├── .env                 # Mühit dəyişkənləri

📌 Gələcəkdə əlavə edilə bilər
Email ilə təsdiq sistemi
Admin dashboard frontend (React.js)
Uyğunluğa görə avtomatik sıralama
CV PDF-lərini önizləmə

👨‍💻 Müəllif
Famil Eyvazlı
📍 Baku, Azərbaycan
💼 Entrepreneur, Developer
📷 Instagram: https://www.instagram.com/thisisfamill/
💼 LinkedIn: www.linkedin.com/in/famil-eyvazlı8080












