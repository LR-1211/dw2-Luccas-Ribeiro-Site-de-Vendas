import random
from datetime import datetime
from models import Product, Order, OrderItem
from database import SessionLocal

def seed_db():
    db = SessionLocal()
    
    categories = ["Cadernos", "Canetas", "Mochilas", "Acessórios"]
    products = [
        {
            "nome": f"Produto {i}",
            "descricao": f"Descrição do Produto {i}",
            "preco": round(random.uniform(5.00, 249.90), 2),
            "estoque": random.randint(0, 20),
            "categoria": random.choice(categories),
            "sku": f"SKU-{i}"
        }
        for i in range(1, 21)
    ]
    
    for product in products:
        db.add(Product(**product))
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_db()