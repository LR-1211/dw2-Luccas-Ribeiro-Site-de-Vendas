#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.produto import Produto, Coupon, db
from decimal import Decimal

def populate_database():
    with app.app_context():
        # Criar tabelas (se necessário) e limpar dados existentes
        db.create_all()
        Produto.query.delete()
        Coupon.query.delete()
        
        # Produtos de exemplo para loja escolar
        produtos = [
            {
                'nome': 'Caderno Universitário 200 folhas',
                'descricao': 'Caderno universitário com 200 folhas pautadas, capa dura',
                'preco': Decimal('15.90'),
                'estoque': 50,
                'categoria': 'Cadernos',
                'sku': 'CAD001',
                'image_url': '/static/assets/caderno.jpg'
            },
            {
                'nome': 'Caneta Esferográfica Azul',
                'descricao': 'Caneta esferográfica com tinta azul, escrita suave',
                'preco': Decimal('2.50'),
                'estoque': 100,
                'categoria': 'Canetas',
                'sku': 'CAN001',
                'image_url': '/static/assets/caneta.jpg'
            },
            {
                'nome': 'Lápis HB Nº2',
                'descricao': 'Lápis grafite HB número 2, ideal para escrita e desenho',
                'preco': Decimal('1.20'),
                'estoque': 80,
                'categoria': 'Lápis',
                'sku': 'LAP001',
                'image_url': '/static/assets/lapis.jpg'
            },
            {
                'nome': 'Borracha Branca',
                'descricao': 'Borracha branca macia, não mancha o papel',
                'preco': Decimal('1.50'),
                'estoque': 60,
                'categoria': 'Borrachas',
                'sku': 'BOR001',
                'image_url': '/static/assets/borracha.jpg'
            },
            {
                'nome': 'Régua 30cm',
                'descricao': 'Régua transparente de 30cm com medidas em centímetros',
                'preco': Decimal('3.80'),
                'estoque': 40,
                'categoria': 'Réguas',
                'sku': 'REG001',
                'image_url': '/static/assets/regua.jpg'
            },
            {
                'nome': 'Estojo Escolar',
                'descricao': 'Estojo escolar com dois compartimentos, várias cores',
                'preco': Decimal('12.90'),
                'estoque': 25,
                'categoria': 'Estojos',
                'sku': 'EST001',
                'image_url': '/static/assets/estojo.jpg'
            },
            {
                'nome': 'Marcador Fluorescente Amarelo',
                'descricao': 'Marcador fluorescente amarelo para destacar textos',
                'preco': Decimal('4.20'),
                'estoque': 35,
                'categoria': 'Marcadores',
                'sku': 'MAR001',
                'image_url': '/static/assets/marcador.jpg'
            },
            {
                'nome': 'Folha Sulfite A4 - Pacote 500 folhas',
                'descricao': 'Pacote com 500 folhas sulfite A4, 75g/m²',
                'preco': Decimal('18.50'),
                'estoque': 20,
                'categoria': 'Papéis',
                'sku': 'PAP001',
                'image_url': '/static/assets/papel.jpg'
            },
            {
                'nome': 'Cola Bastão 40g',
                'descricao': 'Cola em bastão 40g, ideal para papel e cartolina',
                'preco': Decimal('5.90'),
                'estoque': 45,
                'categoria': 'Colas',
                'sku': 'COL001',
                'image_url': '/static/assets/cola.jpg'
            },
            {
                'nome': 'Calculadora Científica',
                'descricao': 'Calculadora científica com 240 funções, display de 2 linhas',
                'preco': Decimal('45.90'),
                'estoque': 15,
                'categoria': 'Calculadoras',
                'sku': 'CAL001',
                'image_url': '/static/assets/calculadora.jpg'
            },
            {
                'nome': 'Mochila Escolar',
                'descricao': 'Mochila escolar resistente com compartimento para notebook',
                'preco': Decimal('89.90'),
                'estoque': 12,
                'categoria': 'Mochilas',
                'sku': 'MOC001',
                'image_url': '/static/assets/mochila.jpg'
            },
            {
                'nome': 'Agenda Escolar 2025',
                'descricao': 'Agenda escolar 2025 com calendário e espaço para anotações',
                'preco': Decimal('22.90'),
                'estoque': 30,
                'categoria': 'Agendas',
                'sku': 'AGE001',
                'image_url': '/static/assets/agenda.jpg'
            }
        ]
        
        for produto_data in produtos:
            produto = Produto(**produto_data)
            db.session.add(produto)
        # Criar cupom ALUNO10
        cupom = Coupon(codigo='ALUNO10', desconto=Decimal('0.10'), tipo='percentual', ativo=True)
        db.session.add(cupom)
        
        db.session.commit()
        print(f"Banco de dados populado com {len(produtos)} produtos!")

if __name__ == '__main__':
    populate_database()

