module Presentation::DeSerializers::Settlement
  class Params
    def initialize(params)
      @params = params
    end

    def execute
      @params.require(:settlement).permit(
        :title,
        :visibility_scope,
      ).merge(@params.permit(participants: %i[ id name role ]))
    end
  end
end
