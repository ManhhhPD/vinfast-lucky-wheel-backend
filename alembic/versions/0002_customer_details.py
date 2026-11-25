"""Add customer contact details and update the campaign prize."""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("spin_results", sa.Column("phone_number", sa.String(30), nullable=True))
    op.add_column("spin_results", sa.Column("address", sa.String(500), nullable=True))
    op.execute(sa.text("UPDATE prizes SET name = 'Tiền mặt 200.000đ' WHERE code = 'combo'"))


def downgrade():
    op.execute(sa.text("UPDATE prizes SET name = 'Combo Mũ + thảm lót sàn' WHERE code = 'combo'"))
    op.drop_column("spin_results", "address")
    op.drop_column("spin_results", "phone_number")
