module Usecases
  module Settlement
    class CreatePayment
      def initialize(settlement_session)
        @settlement_session = settlement_session
      end

      def execute(params)
        payment = @settlement_session.payments.create!(
          amount: params[:amount],
          paid_by_id: params[:paid_by_id],
          title: params[:title],
          description: params[:description]
        )

        params[:participants].each do |participant|
          payment.payment_participants.create!(
            user: User.find(participant[:id]),
            weight: participant[:weight]
          )
        end

        payment
      end
    end
  end
end
