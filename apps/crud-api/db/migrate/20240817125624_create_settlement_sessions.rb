class CreateSettlementSessions < ActiveRecord::Migration[7.2]
  def change
    create_table :settlement_sessions, id: :uuid do |t|
      t.string :title, null: false
      t.integer :visibility_scope, null: false

      t.timestamps
    end
  end
end
