from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from database import get_db
from fastapi.responses import StreamingResponse
import io
from fastapi.middleware.cors import CORSMiddleware
from openaiapi import extract_text_from_pdf_bytes, get_embedding, cosine_similarity
from vacancies import job_requirements
from schemas import StatusUpdate, Admin, Admin_login
import base64
import re
from security import hash_password, verify_password, create_access_token, get_current_admin
from datetime import timedelta


app = FastAPI()


ORIGINS = {
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
}


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.put("/admin/applicants/{applicant_id}/status", tags=["Admin"])
def update_applicant_status(applicant_id: int, status_update: StatusUpdate, current_admin: str = Depends(get_current_admin)):
    try:
        mydb, mycursor_user, _ = get_db()

        if status_update.status not in ["approved", "rejected", "pending"]:
            raise HTTPException(status_code=400, detail="Wrong status value")

        mycursor_user.execute(
            "UPDATE applicants SET status = %s WHERE id = %s",
            (status_update.status, applicant_id)
        )
        mydb.commit()

        return {"message": "Status uğurla dəyişdirildi"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/admin/applicants/{applicant_id}/download", tags=["Admin"])
def download_cv(applicant_id: int, current_admin: str = Depends(get_current_admin)):
    try:
        mydb, mycursor_user, _ = get_db()
        mycursor_user.execute(
            "SELECT filename, cv FROM applicants WHERE id = %s",
            (applicant_id,)
        )
        row = mycursor_user.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="CV not found")

        filename, base64_data = row
        
        cleaned_base64 = re.sub(r'\s+', '', base64_data)
        
        missing_padding = len(cleaned_base64) % 4
        if missing_padding:
            cleaned_base64 += '=' * (4 - missing_padding)

        file_bytes = base64.b64decode(cleaned_base64)
        
        return StreamingResponse(
            io.BytesIO(file_bytes),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/submit", tags=["User"])
async def submit_user(username: str = Form(...), email: str = Form(...), cv: UploadFile = File(...)):
    
    try:
        mydb, mycursor_user, _ = get_db()
        
        file_data = await cv.read()
        filename = cv.filename

        file_base64 = base64.b64encode(file_data).decode("utf-8")
        
        mycursor_user.execute("""
            INSERT INTO applicants (name, email, filename, cv)
            VALUES (%s, %s, %s, %s)
        """, (username, email, filename, file_base64))
        mydb.commit()
        
        return {"message": "User submitted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/admin/applicants", tags=["Admin"])
def get_applicants(current_admin: str = Depends(get_current_admin)):
    mydb, mycursor_user, _ = get_db()
    mycursor_user.execute("SELECT id, name, email, filename FROM applicants")
    rows = mycursor_user.fetchall()
    applicants = []
    for row in rows:
        applicants.append({
            "id": row[0],
            "name": row[1],
            # "email": row[2],
            # "filename": row[3]
        })

    mycursor_user.close()
    mydb.close()

    return {"applicants": applicants}

@app.get("/admin/applicants/{applicant_id}", tags=["Admin"])
def get_applicant_detail(applicant_id: int, current_admin: str = Depends(get_current_admin)):
    try:
        mydb, mycursor_user, _ = get_db()
        mycursor_user.execute(
            "SELECT id, name, email, filename FROM applicants WHERE id = %s",
            (applicant_id,)
        )
        row = mycursor_user.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Applicant not found")
        
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "filename": row[3]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/admin/panel", tags=["Admin"])
def admin_panel(current_admin: str = Depends(get_current_admin)):
    return get_applicants()

@app.post("/admin/login", tags=["Admin"])
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        mydb, _, mycursor_admin = get_db()
        
        mycursor_admin.execute(
            "SELECT id, password FROM admin WHERE name = %s", 
            (form_data.username,)
        )
        row = mycursor_admin.fetchone()

        if row is None:
            raise HTTPException(status_code=401, detail="User not found")

        admin_id, hashed_password = row

        if not verify_password(form_data.password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=timedelta(minutes=60)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/match", tags=["AI"])
async def match_uploaded_cv_with_job(
    job_id: int = Form(...),
    cv: UploadFile = File(...) 
):
    if job_id not in job_requirements:
        raise HTTPException(status_code=404, detail="Job ID not found.")

    try:
        job_text = job_requirements[job_id]["description"]

        file_data = await cv.read()
        cv_text = extract_text_from_pdf_bytes(file_data)

        cv_emb = get_embedding(cv_text)
        job_emb = get_embedding(job_text)

        similarity = cosine_similarity(cv_emb, job_emb)
        similarity_percent = round(similarity * 100, 2)

        return {
            "job_id": job_id,
            "job_title": job_requirements[job_id]["title"],
            "similarity_score": similarity,
            "similarity_percent": similarity_percent,
            "message": f"Fitting score: {similarity_percent}%"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/admin_register", tags=["Admin"])
def admin_register(admin: Admin):
    mydb, _, mycursor_admin = get_db()
    hashed_password = hash_password(admin.password)

    mycursor_admin.execute(
        "INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)", 
        (admin.name, admin.email, hashed_password)
    )
    mydb.commit()
    return {"message": "Admin registered successfully"}
