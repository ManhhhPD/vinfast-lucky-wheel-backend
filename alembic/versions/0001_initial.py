"""Create prize catalog and spin results; seed campaign probabilities."""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    prizes = op.create_table(
        "prizes",
        sa.Column("code", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("probability_bp", sa.Integer(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.CheckConstraint("probability_bp >= 0", name="ck_prizes_probability_nonnegative"),
    )
    op.create_table(
        "spin_results",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("player_name", sa.String(100), nullable=False),
        sa.Column("prize_code", sa.String(64), sa.ForeignKey("prizes.code"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("client_ip", sa.String(64), nullable=True),
    )
    rows = [
        ("cash_100k", "Tiền mặt 100.000đ", 2500),
        ("cash_300k", "Tiền mặt 300.000đ", 2000),
        ("cash_500k", "Tiền mặt 500.000đ", 1500),
        ("voucher_1m", "Voucher 1 triệu mua phụ kiện", 1500),
        ("combo", "Combo Mũ + thảm lót sàn", 2500),
        ("feliz_2027", "Xe Feliz 2027", 0),
    ]
    op.bulk_insert(prizes, [dict(code=code, name=name, probability_bp=weight, sort_order=i, is_active=True) for i, (code, name, weight) in enumerate(rows)])


def downgrade():
    op.drop_table("spin_results")
    op.drop_table("prizes")
