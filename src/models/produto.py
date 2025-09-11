from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(50), nullable=False)
    sku = db.Column(db.String(50), nullable=True, unique=True)
    image_url = db.Column(db.String(255), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': float(self.preco),
            'estoque': self.estoque,
            'categoria': self.categoria,
            'sku': self.sku,
            'image_url': self.image_url,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'ativo': self.ativo
        }

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_original = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    total_final = db.Column(db.Numeric(10, 2), nullable=False)
    cupom_usado = db.Column(db.String(20), nullable=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pendente')

    def __repr__(self):
        return f'<Pedido {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'total_original': float(self.total_original),
            'desconto': float(self.desconto),
            'total_final': float(self.total_final),
            'cupom_usado': self.cupom_usado,
            'data_pedido': self.data_pedido.isoformat() if self.data_pedido else None,
            'status': self.status
        }

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    
    pedido = db.relationship('Pedido', backref=db.backref('itens', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('itens_pedido', lazy=True))

    def __repr__(self):
        return f'<ItemPedido {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'preco_unitario': float(self.preco_unitario),
            'produto': self.produto.to_dict() if self.produto else None
        }


class Coupon(db.Model):
    __tablename__ = 'coupon'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    desconto = db.Column(db.Numeric(10, 4), nullable=False)  # e.g. 0.10
    tipo = db.Column(db.String(20), nullable=False, default='percentual')
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Coupon {self.codigo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'desconto': float(self.desconto),
            'tipo': self.tipo,
            'ativo': self.ativo
        }

