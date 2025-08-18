from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(60), nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoria = Column(String(20), nullable=False)
    sku = Column(String, unique=True, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    subtotal = Column(Float, nullable=False)
    desconto = Column(Float, default=0.0)
    total_final = Column(Float, nullable=False)
    cupom_aplicado = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    nome = Column(String(60), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    pedido = relationship("Order", back_populates="itens")
    produto = relationship("Product")