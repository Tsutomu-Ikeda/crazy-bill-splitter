module Presentation::Serializers::Settlement
  class Detail
    def initialize(settlement_session)
      @settlement_session = settlement_session
    end

    def execute
      {
        id: @settlement_session.id,
        title: @settlement_session.title,
        visibility_scope: @settlement_session.visibility_scope,
        participants: @settlement_session.participants.map do |participant|
          {
            id: participant.id,
            name: participant.name,
            role: @settlement_session.settlement_session_participants.find_by(user_id: participant.id).role
          }
        end,
        payments: @settlement_session.payments.map do |payment|
          {
            id: payment.id,
            title: payment.title,
            description: payment.description,
            amount: payment.amount,
            paid_by: {
              id: payment.paid_by.id,
              name: payment.paid_by.name
            },
            participants: payment.participants.map do |participant|
              {
                id: participant.id,
                name: participant.name,
                weight: payment.payment_participants.find_by(user_id: participant.id).weight
              }
            end
          }
        end
      }
    end
  end
end
