from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.core.database import _get_connection

# Cria o Blueprint do Flask para o inventário
inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/dashboard')
def dashboard():
    """Lista todos os produtos no dashboard"""
    produtos = []
    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                # Busca os dados atualizados do SQL
                cur.execute("SELECT id, nome, categoria, preco, estoque_sistema FROM produtos ORDER BY id DESC")
                for p in cur.fetchall():
                    produtos.append({
                        "id": p[0], 
                        "nome": p[1], 
                        "categoria": p[2], 
                        "preco": p[3], 
                        "estoque": p[4]
                    })
    except Exception as e:
        print(f"❌ Erro ao buscar produtos: {e}")
    
    return render_template('dashboard.html', produtos=produtos)

@inventory_bp.route('/criar', methods=['POST'])
def criar_produto():
    """Recebe dados do formulário e salva no PostgreSQL"""
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    preco = request.form.get('preco')
    estoque = request.form.get('estoque')

    # Lógica de Inserção no Banco de Dados
    if nome and preco:
        try:
            with _get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO produtos (nome, categoria, preco, estoque_sistema) 
                        VALUES (%s, %s, %s, %s)
                        """,
                        (nome, categoria, float(preco), int(estoque))
                    )
                conn.commit() # Salva as alterações
                print(f"✅ Produto {nome} cadastrado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inserir produto: {e}")
    
    # Redireciona de volta para a lista (atualiza a tela)
    return redirect(url_for('inventory.dashboard'))

@inventory_bp.route('/deletar/<int:id>')
def deletar_produto(id):
    """Remove um produto pelo ID"""
    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM produtos WHERE id = %s", (id,))
            conn.commit()
            print(f"🗑️ Produto {id} removido.")
    except Exception as e:
        print(f"❌ Erro ao deletar: {e}")
    
    return redirect(url_for('inventory.dashboard'))