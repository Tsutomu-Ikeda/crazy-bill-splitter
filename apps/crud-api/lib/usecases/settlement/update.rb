module Usecases
  module Settlement
    class Update
      def initialize(settlement_session)
        @settlement_session = settlement_session
      end

      def execute(params)
        @settlement_session.update!(
          title: params[:title],
          visibility_scope: params[:visibility_scope]
        )

        registered_participants = params[:participants].map do |participant|
          if participant[:user_id] && registered_participant = User.find(participant[:user_id])
            registered_participant.update!(name: participant[:name])
          else
            registered_participant = User.create!(name: participant[:name])
          end

          {
            id: registered_participant.id,
            name: registered_participant.name,
            role: participant[:role]
          }
        end

        @settlement_session.settlement_session_participants.destroy_all
        settlement_session_participants = registered_participants.map do |participant|
          @settlement_session.settlement_session_participants.create(
            user_id: participant[:id],
            joined_at: Time.zone.now,
            role: participant[:role],
            settlement_status: :created
          )
        end

        @settlement_session.reload
      end
    end
  end
end
