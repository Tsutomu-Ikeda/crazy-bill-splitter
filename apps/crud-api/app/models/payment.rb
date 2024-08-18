class Payment < ApplicationRecord
  belongs_to :settlement_session
  belongs_to :paid_by, class_name: :User

  has_many :payment_participants
  has_many :participants, through: :payment_participants, source: :user
end
