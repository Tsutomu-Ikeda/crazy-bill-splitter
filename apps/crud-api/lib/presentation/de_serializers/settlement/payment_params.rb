module Presentation::DeSerializers::Settlement
  class PaymentParams
    def initialize(params)
      @params = params
    end

    def execute
      @params.permit(
        :amount,
        :paid_by_id,
        :title,
        :description,
      ).merge(@params.permit(participants: %i[ id weight ]))
    end
  end
end
