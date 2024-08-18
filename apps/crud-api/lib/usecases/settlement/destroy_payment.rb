module Usecases
  module Settlement
    class DestroyPayment
      def initialize(settlement_session)
        @settlement_session = settlement_session
      end

      def execute(params)
        payment = @settlement_session.payments.find(params[:payment_id])

        payment.payment_participants.destroy_all
        payment.destroy!
      end
    end
  end
end
