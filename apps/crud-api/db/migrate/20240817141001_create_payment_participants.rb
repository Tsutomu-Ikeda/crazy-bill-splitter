class CreatePaymentParticipants < ActiveRecord::Migration[7.2]
  def change
    create_table :payment_participants do |t|
      t.references :payment, type: :uuid, null: false, foreign_key: true
      t.references :user, type: :uuid, null: false, foreign_key: true
      t.integer :weight, null: false

      t.timestamps
    end
  end
end
