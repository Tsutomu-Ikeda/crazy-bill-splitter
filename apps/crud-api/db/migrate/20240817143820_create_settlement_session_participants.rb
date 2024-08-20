class CreateSettlementSessionParticipants < ActiveRecord::Migration[7.2]
  def change
    create_table :settlement_session_participants do |t|
      t.references :settlement_session, type: :uuid, null: false, foreign_key: true
      t.references :user, type: :uuid, null: false, foreign_key: true
      t.datetime :joined_at, null: false
      t.integer :role, null: false
      t.integer :settlement_status, null: false

      t.timestamps
    end
  end
end
