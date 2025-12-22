"""initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ingredientes
    op.create_table(
        'ingredientes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('unidade_padrao', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ingredientes_id'), 'ingredientes', ['id'], unique=False)
    op.create_index(op.f('ix_ingredientes_nome'), 'ingredientes', ['nome'], unique=True)

    # Receitas
    op.create_table(
        'receitas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('tempo_preparo', sa.Integer(), nullable=True),
        sa.Column('rendimento', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_receitas_id'), 'receitas', ['id'], unique=False)
    op.create_index(op.f('ix_receitas_nome'), 'receitas', ['nome'], unique=False)

    # IngredienteReceita
    op.create_table(
        'ingrediente_receita',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receita_id', sa.Integer(), nullable=False),
        sa.Column('ingrediente_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Numeric(10, 2), nullable=False),
        sa.Column('unidade', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['ingrediente_id'], ['ingredientes.id'], ),
        sa.ForeignKeyConstraint(['receita_id'], ['receitas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ingrediente_receita_id'), 'ingrediente_receita', ['id'], unique=False)

    # Pedidos
    op.create_table(
        'pedidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('NOVO', 'EM_PRODUCAO', 'PRONTO', 'ENTREGUE', 'CANCELADO', name='statuspedido'), nullable=False),
        sa.Column('data_entrega', sa.Date(), nullable=False),
        sa.Column('horario', sa.Time(), nullable=True),
        sa.Column('local', sa.String(), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('preco_total', sa.Numeric(10, 2), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pedidos_id'), 'pedidos', ['id'], unique=False)
    op.create_index(op.f('ix_pedidos_cliente'), 'pedidos', ['cliente'], unique=False)
    op.create_index(op.f('ix_pedidos_data_entrega'), 'pedidos', ['data_entrega'], unique=False)
    op.create_index(op.f('ix_pedidos_status'), 'pedidos', ['status'], unique=False)

    # ItensPedido
    op.create_table(
        'itens_pedido',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('receita_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('unidade', sa.String(), nullable=True),
        sa.Column('personalizacoes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ),
        sa.ForeignKeyConstraint(['receita_id'], ['receitas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_itens_pedido_id'), 'itens_pedido', ['id'], unique=False)

    # Estoque
    op.create_table(
        'estoque',
        sa.Column('ingrediente_id', sa.Integer(), nullable=False),
        sa.Column('quantidade_atual', sa.Numeric(10, 2), nullable=False),
        sa.Column('custo_unitario', sa.Numeric(10, 2), nullable=True),
        sa.Column('ponto_reposicao', sa.Numeric(10, 2), nullable=True),
        sa.ForeignKeyConstraint(['ingrediente_id'], ['ingredientes.id'], ),
        sa.PrimaryKeyConstraint('ingrediente_id')
    )

    # MovimentacoesEstoque
    op.create_table(
        'movimentacoes_estoque',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ingrediente_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.Enum('ENTRADA', 'SAIDA', 'AJUSTE', name='tipomovimentacao'), nullable=False),
        sa.Column('quantidade', sa.Numeric(10, 2), nullable=False),
        sa.Column('motivo', sa.String(), nullable=True),
        sa.Column('data', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['ingrediente_id'], ['ingredientes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movimentacoes_estoque_id'), 'movimentacoes_estoque', ['id'], unique=False)
    op.create_index(op.f('ix_movimentacoes_estoque_ingrediente_id'), 'movimentacoes_estoque', ['ingrediente_id'], unique=False)
    op.create_index(op.f('ix_movimentacoes_estoque_data'), 'movimentacoes_estoque', ['data'], unique=False)

    # AgendaEntrega
    op.create_table(
        'agenda_entregas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('data_hora', sa.DateTime(), nullable=False),
        sa.Column('local', sa.String(), nullable=True),
        sa.Column('responsavel', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pedido_id')
    )
    op.create_index(op.f('ix_agenda_entregas_id'), 'agenda_entregas', ['id'], unique=False)
    op.create_index(op.f('ix_agenda_entregas_pedido_id'), 'agenda_entregas', ['pedido_id'], unique=True)
    op.create_index(op.f('ix_agenda_entregas_data_hora'), 'agenda_entregas', ['data_hora'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_agenda_entregas_data_hora'), table_name='agenda_entregas')
    op.drop_index(op.f('ix_agenda_entregas_pedido_id'), table_name='agenda_entregas')
    op.drop_index(op.f('ix_agenda_entregas_id'), table_name='agenda_entregas')
    op.drop_table('agenda_entregas')
    op.drop_index(op.f('ix_movimentacoes_estoque_data'), table_name='movimentacoes_estoque')
    op.drop_index(op.f('ix_movimentacoes_estoque_ingrediente_id'), table_name='movimentacoes_estoque')
    op.drop_index(op.f('ix_movimentacoes_estoque_id'), table_name='movimentacoes_estoque')
    op.drop_table('movimentacoes_estoque')
    op.drop_table('estoque')
    op.drop_index(op.f('ix_itens_pedido_id'), table_name='itens_pedido')
    op.drop_table('itens_pedido')
    op.drop_index(op.f('ix_pedidos_status'), table_name='pedidos')
    op.drop_index(op.f('ix_pedidos_data_entrega'), table_name='pedidos')
    op.drop_index(op.f('ix_pedidos_cliente'), table_name='pedidos')
    op.drop_index(op.f('ix_pedidos_id'), table_name='pedidos')
    op.drop_table('pedidos')
    op.drop_index(op.f('ix_ingrediente_receita_id'), table_name='ingrediente_receita')
    op.drop_table('ingrediente_receita')
    op.drop_index(op.f('ix_receitas_nome'), table_name='receitas')
    op.drop_index(op.f('ix_receitas_id'), table_name='receitas')
    op.drop_table('receitas')
    op.drop_index(op.f('ix_ingredientes_nome'), table_name='ingredientes')
    op.drop_index(op.f('ix_ingredientes_id'), table_name='ingredientes')
    op.drop_table('ingredientes')
    op.execute('DROP TYPE IF EXISTS statuspedido')
    op.execute('DROP TYPE IF EXISTS tipomovimentacao')

