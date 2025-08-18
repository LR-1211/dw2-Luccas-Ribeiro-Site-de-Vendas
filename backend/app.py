from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from models import Base, Product, Order, OrderItem
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request and response
class ProductCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    categoria: str
    sku: Optional[str] = None

class ProductResponse(ProductCreate):
    id: int

class CouponValidation(BaseModel):
    cupom: str
    subtotal: float

class OrderItemCreate(BaseModel):
    produto_id: int
    quantidade: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    cupom: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/produtos", response_model=List[ProductResponse])
def get_products(search: Optional[str] = None, categoria: Optional[str] = None, sort: Optional[str] = None):
    with SessionLocal() as db:
        query = db.query(Product)
        if search:
            query = query.filter(Product.nome.ilike(f"%{search}%"))
        if categoria:
            query = query.filter(Product.categoria == categoria)
        if sort:
            if sort == "nome":
                query = query.order_by(Product.nome)
            elif sort == "preco":
                query = query.order_by(Product.preco)
        return query.all()

@app.post("/produtos", response_model=ProductResponse)
def create_product(product: ProductCreate):
    with SessionLocal() as db:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

@app.put("/produtos/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductCreate):
    with SessionLocal() as db:
        db_product = db.query(Product).filter(Product.id == id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        return db_product

@app.delete("/produtos/{id}")
def delete_product(id: int):
    with SessionLocal() as db:
        db_product = db.query(Product).filter(Product.id == id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        db.delete(db_product)
        db.commit()
        return {"detail": "Produto removido"}

@app.post("/cupom/validar")
def validate_coupon(cupom_validation: CouponValidation):
    if cupom_validation.cupom == "ALUNO10" and cupom_validation.subtotal >= 50.00:
        return {"desconto": 0.10}
    raise HTTPException(status_code=400, detail="Cupom inválido ou subtotal insuficiente")

@app.post("/carrinho/confirmar")
def confirm_order(order: OrderCreate):
    with SessionLocal() as db:
        # Implementar lógica de confirmação de pedido
        pass  # Placeholder for order confirmation logic

# Adicione mais rotas conforme necessário.