module Usecases
  module Settlement
    class Destroy
      def initialize(settlement_session)
        @settlement_session = settlement_session
      end

      def execute
        @settlement_session.payments.each do |payment|
          payment.payment_participants.destroy_all
          payment.destroy!
        end
        @settlement_session.settlement_session_participants.destroy_all
        @settlement_session.destroy!
      end
    end
  end
end
