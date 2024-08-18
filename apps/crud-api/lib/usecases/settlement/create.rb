module Usecases
  module Settlement
    class Create
      def execute(params)
        settlement_session = SettlementSession.create(
          title: params[:title],
          visibility_scope: params[:visibility_scope]
        )

        registered_participants = params[:participants].map do |participant|
          if participant[:id] && registered_participant = User.find(participant[:id])
            if participant[:name]
              registered_participant.update!(name: participant[:name])
            end
          else
            registered_participant = User.create!(name: participant[:name])
          end

          {
            id: registered_participant.id,
            role: participant[:role]
          }
        end

        settlement_session.settlement_session_participants.destroy_all
        settlement_session_participants = registered_participants.map do |participant|
          settlement_session.settlement_session_participants.create(
            user_id: participant[:id],
            joined_at: Time.zone.now,
            role: participant[:role],
            settlement_status: :created
          )
        end

        settlement_session
      end
    end
  end
end
