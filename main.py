from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from database import get_db
from fastapi.responses import StreamingResponse
import io


app = FastAPI()


class StatusUpdate(BaseModel):
    status: str  

@app.put("/admin/applicants/{applicant_id}/status", tags=["Admin"])
def update_applicant_status(applicant_id: int, status_update: StatusUpdate):
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
def download_cv(applicant_id: int):
    try:
        mydb, mycursor_user, _ = get_db()
        mycursor_user.execute(
            "SELECT filename, cv FROM applicants WHERE id = %s",
            (applicant_id,)
        )
        row = mycursor_user.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="CV not found")

        filename, file_data = row

        return StreamingResponse(
            io.BytesIO(file_data),
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

        mycursor_user.execute("""
            INSERT INTO applicants (name, email, filename, cv)
            VALUES (%s, %s, %s, %s)
        """, (username, email, filename, file_data))
        mydb.commit()
        
        return {"message": "User submitted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


class Admin(BaseModel):
    name: str
    password: str
    
@app.get("/admin/applicants", tags=["Admin"])
def get_applicants():
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
def get_applicant_detail(applicant_id: int):
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
def admin_panel():
    return get_applicants()
    

@app.post("/admin", tags=["Admin"])
def admin(admin: Admin):
    if admin.name == "admin" and admin.password == "password":
        return admin_panel()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})


