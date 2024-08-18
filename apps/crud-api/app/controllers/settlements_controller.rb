class SettlementsController < ApplicationController
  before_action :set_settlement_session, only: %i[ show update destroy create_payment ]

  def show
    render json: Serializers::Settlement::Detail.new(@settlement_session).serialize
  end

  def create
    settlement_session = Usecases::Settlement::Create.new.execute(settlement_session_params)

    render json: settlement_session
  end

  def update
    Usecases::Settlement::Update.new(@settlement_session).execute(settlement_session_params)

    render json: @settlement_session
  rescue ActiveRecord::RecordInvalid => e
    render json: { errors: e.record.errors }, status: :unprocessable_entity
  end

  def destroy
    Usecases::Settlement::Destroy.new(@settlement_session).execute

    render json: {
      message: "Settlement session deleted successfully"
    }
  end

  def create_payment
    payment = Usecases::Settlement::CreatePayment.new(@settlement_session).execute(payment_params)

    render json: payment
  end

  def destroy_payment
    settlement_session = SettlementSession.find(params[:settlement_id])
    Usecases::Settlement::DestroyPayment.new(settlement_session).execute(params)

    render json: {
      message: "Payment deleted successfully"
    }
  end

  private
    def set_settlement_session
      @settlement_session = SettlementSession.find(params[:id])
    end

    def settlement_session_params
      params.require(:settlement).permit(
        :title,
        :visibility_scope,
      ).merge(params.permit(participants: %i[ id name role ]))
    end

    def user_params
      params.require(:user).permit(:name)
    end

    def payment_params
      params.permit(
        :amount,
        :paid_by_id,
        :title,
        :description,
      ).merge(params.permit(participants: %i[ id weight ]))
    end

    def members_params
      params.require(:members).permit(:id, :name, :role)
    end
end
