class SettlementSessionParticipant < ApplicationRecord
  enum :role, { organizer: 0, participant: 100 }, suffix: :role
  enum :settlement_status, { created: 0, confirmation_requested: 100, confirmed: 200, cancelled: 900 }, prefix: :settlement

  belongs_to :settlement_session
  belongs_to :user
end
