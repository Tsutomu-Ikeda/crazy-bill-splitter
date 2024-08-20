class SettlementSession < ApplicationRecord
  enum :visibility_scope, { public: 0, invited_only: 100 }, prefix: :visibility

  has_many :settlement_session_participants
  has_many :participants, through: :settlement_session_participants, source: :user

  has_many :payments
end
