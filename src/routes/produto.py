from flask import Blueprint, jsonify, request
from src.models.produto import Produto, Pedido, ItemPedido, Coupon, db
from sqlalchemy import desc, asc
from decimal import Decimal

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produtos', methods=['GET'])
def get_produtos():
    # Parâmetros de busca e ordenação
    busca = request.args.get('busca', '')
    ordenar_por = request.args.get('ordenar_por', 'nome')  # nome, preco
    ordem = request.args.get('ordem', 'asc')  # asc, desc
    categoria = request.args.get('categoria', '')
    
    query = Produto.query.filter(Produto.ativo == True)
    
    # Filtro de busca por nome
    if busca:
        query = query.filter(Produto.nome.ilike(f'%{busca}%'))
    
    # Filtro por categoria
    if categoria:
        query = query.filter(Produto.categoria == categoria)
    
    # Ordenação
    if ordenar_por == 'preco':
        if ordem == 'desc':
            query = query.order_by(desc(Produto.preco))
        else:
            query = query.order_by(asc(Produto.preco))
    else:  # ordenar por nome
        if ordem == 'desc':
            query = query.order_by(desc(Produto.nome))
        else:
            query = query.order_by(asc(Produto.nome))
    
    produtos = query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@produto_bp.route('/produtos', methods=['POST'])
def create_produto():
    try:
        data = request.json
        
        # Validações
        if not data.get('nome') or len(data['nome']) < 3 or len(data['nome']) > 60:
            return jsonify({'erro': 'Nome deve ter entre 3 e 60 caracteres'}), 400
        
        if not data.get('preco') or float(data['preco']) < 0.01:
            return jsonify({'erro': 'Preço deve ser maior que 0.01'}), 400
        
        if not data.get('categoria'):
            return jsonify({'erro': 'Categoria é obrigatória'}), 400
        
        if data.get('estoque') is None or int(data['estoque']) < 0:
            return jsonify({'erro': 'Estoque deve ser maior ou igual a 0'}), 400
        
        # Verificar se SKU já existe (se fornecido)
        if data.get('sku'):
            produto_existente = Produto.query.filter_by(sku=data['sku']).first()
            if produto_existente:
                return jsonify({'erro': 'SKU já existe'}), 400
        
        produto = Produto(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            preco=Decimal(str(data['preco'])),
            estoque=int(data['estoque']),
            categoria=data['categoria'],
            sku=data.get('sku'),
            image_url=data.get('image_url')
        )
        
        db.session.add(produto)
        db.session.commit()
        return jsonify(produto.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict())

@produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    try:
        produto = Produto.query.get_or_404(produto_id)
        data = request.json
        
        # Validações
        if data.get('nome') and (len(data['nome']) < 3 or len(data['nome']) > 60):
            return jsonify({'erro': 'Nome deve ter entre 3 e 60 caracteres'}), 400
        
        if data.get('preco') and float(data['preco']) < 0.01:
            return jsonify({'erro': 'Preço deve ser maior que 0.01'}), 400
        
        if data.get('estoque') is not None and int(data['estoque']) < 0:
            return jsonify({'erro': 'Estoque deve ser maior ou igual a 0'}), 400
        
        # Verificar se SKU já existe (se fornecido e diferente do atual)
        if data.get('sku') and data['sku'] != produto.sku:
            produto_existente = Produto.query.filter_by(sku=data['sku']).first()
            if produto_existente:
                return jsonify({'erro': 'SKU já existe'}), 400
        
        # Atualizar campos
        produto.nome = data.get('nome', produto.nome)
        produto.descricao = data.get('descricao', produto.descricao)
        if data.get('preco'):
            produto.preco = Decimal(str(data['preco']))
        if data.get('estoque') is not None:
            produto.estoque = int(data['estoque'])
        produto.categoria = data.get('categoria', produto.categoria)
        produto.sku = data.get('sku', produto.sku)
        produto.image_url = data.get('image_url', produto.image_url)
        
        db.session.commit()
        return jsonify(produto.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    try:
        produto = Produto.query.get_or_404(produto_id)
        produto.ativo = False  # Soft delete
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = db.session.query(Produto.categoria).filter(Produto.ativo == True).distinct().all()
    return jsonify([cat[0] for cat in categorias])

@produto_bp.route('/cupom/validar', methods=['POST'])
def validar_cupom():
    data = request.json
    codigo = data.get('codigo', '').upper()
    
    # Procura cupom no banco
    cupom = Coupon.query.filter_by(codigo=codigo, ativo=True).first()
    if cupom:
        return jsonify({
            'valido': True,
            'desconto': float(cupom.desconto),
            'tipo': cupom.tipo
        })
    else:
        return jsonify({'valido': False, 'erro': 'Cupom inválido'})

@produto_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    try:
        data = request.json
        itens = data.get('itens', [])
        cupom = data.get('cupom', '').upper()
        
        if not itens:
            return jsonify({'erro': 'Pedido deve ter pelo menos um item'}), 400
        
        total_original = Decimal('0')
        itens_pedido = []
        
        # Validar itens e calcular total
        for item in itens:
            produto = Produto.query.get(item['produto_id'])
            if not produto:
                return jsonify({'erro': f'Produto {item["produto_id"]} não encontrado'}), 400
            
            if produto.estoque < item['quantidade']:
                return jsonify({'erro': f'Estoque insuficiente para {produto.nome}'}), 400
            
            subtotal = produto.preco * item['quantidade']
            total_original += subtotal
            
            itens_pedido.append({
                'produto': produto,
                'quantidade': item['quantidade'],
                'preco_unitario': produto.preco
            })
        
        # Aplicar cupom (procura no DB)
        desconto = Decimal('0')
        cupom_usado = None
        if cupom:
            cupom_obj = Coupon.query.filter_by(codigo=cupom, ativo=True).first()
            if cupom_obj and cupom_obj.tipo == 'percentual':
                desconto = total_original * Decimal(str(float(cupom_obj.desconto)))
                cupom_usado = cupom_obj.codigo
        
        total_final = total_original - desconto
        
        # Criar pedido
        pedido = Pedido(
            total_original=total_original,
            desconto=desconto,
            total_final=total_final,
            cupom_usado=cupom_usado
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obter o ID do pedido
        
        # Criar itens do pedido e reduzir estoque
        for item_data in itens_pedido:
            item = ItemPedido(
                pedido_id=pedido.id,
                produto_id=item_data['produto'].id,
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario']
            )
            db.session.add(item)
            
            # Reduzir estoque
            item_data['produto'].estoque -= item_data['quantidade']
        
        db.session.commit()
        
        return jsonify({
            'pedido': pedido.to_dict(),
            'itens': [item.to_dict() for item in pedido.itens]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.order_by(desc(Pedido.data_pedido)).all()
    return jsonify([pedido.to_dict() for pedido in pedidos])

@produto_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return jsonify({
        'pedido': pedido.to_dict(),
        'itens': [item.to_dict() for item in pedido.itens]
    })

