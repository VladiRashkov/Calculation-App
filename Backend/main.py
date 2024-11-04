from fastapi import FastAPI, UploadFile, HTTPException, status, Header, Depends, File, Form
from sqlalchemy.orm import Session
import csv
import io
from database import SessionLocal, Request, Result, User
from auth import create_access_token, verify_password, get_user, hash_password
from models import Token
from auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

@app.get("/admin/requests")
async def get_all_requests(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    requests = db.query(Request).filter(Request.user == current_user).all()
    return [
        {"id": req.id, "user": req.user, "request_name": req.request_name, "file_reference": req.file_reference} 
        for req in requests
    ]

@app.get("/admin/results/{request_id}")
async def get_results(request_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    results = db.query(Result).join(Request).filter(Request.id == request_id, Request.user == current_user).all()
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this request or you don't have access.")
    
    return [{"id": res.id, "result_value": res.result_value} for res in results]




@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    '''This is an example of functional programming.
        It is designed to complete a specific task'''
    existing_user = get_user(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(password)
    '''Example of OOP programming below
    Here we use the attributes encapsulated for the class user
    We create an instance of the class to use apply reusability and abstraction'''
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@app.post("/token", response_model=Token)
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user(db, username)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout():
    """Logs the user out. This could be used for logging activity but does not invalidate the token."""
    return {"message": "Logged out successfully"}


@app.post("/api/compute")
async def compute(
    request_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    
    existing_file = db.query(Request).filter(Request.file_reference == file.filename).first()
    if existing_file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A file with the same name already exists. Please use a different filename."
        )

    
    existing_request = db.query(Request).filter(Request.request_name == request_name).first()
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A request with the same name already exists. Please use a different request name."
        )


    request_entry = Request(
        user=current_user,
        request_name=request_name,
        file_reference=file.filename
    )
    db.add(request_entry)
    db.commit()
    db.refresh(request_entry)

    
    file_content = await file.read()
    file_stream = io.StringIO(file_content.decode())

    first_line = file_stream.readline()
    if ';' in first_line:
        delimiter = ';'
    elif ',' in first_line:
        delimiter = ','
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CSV format. The file must contain either ';' or ',' as a delimiter."
        )

    file_stream.seek(0)

    reader = csv.reader(file_stream, delimiter=delimiter)

    total_sum = 0.0

    for row in reader:
        try:
            A = float(row[0])
            O = row[1]
            B = float(row[2])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data in file. Make sure A and B are numbers."
            )

        if O == "+":
            total_sum += A + B
        elif O == "-":
            total_sum += A - B
        elif O == "*":
            total_sum += A * B
        elif O == "/":
            if B == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Division by zero is not allowed."
                )
            total_sum += A / B
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported operation '{O}'. Supported operations are +, -, *, /."
            )

    result_entry = Result(request_id=request_entry.id, result_value=total_sum)
    db.add(result_entry)
    db.commit()

    return {"result": total_sum}
