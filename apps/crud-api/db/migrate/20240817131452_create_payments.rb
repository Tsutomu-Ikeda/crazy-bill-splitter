class CreatePayments < ActiveRecord::Migration[7.2]
  def change
    create_table :payments, id: :uuid do |t|
      t.references :settlement_session, type: :uuid, null: false, foreign_key: true
      t.references :paid_by, type: :uuid, null: false, foreign_key: { to_table: :users }
      t.string :title, null: false
      t.text :description
      t.integer :amount, null: false

      t.timestamps
    end
  end
end
