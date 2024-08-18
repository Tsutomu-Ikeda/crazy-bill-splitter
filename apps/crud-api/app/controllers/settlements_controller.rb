class SettlementsController < ApplicationController
  before_action :set_settlement_session, only: %i[ show update destroy create_payment ]

  def show
    render json: Presentation::Serializers::Settlement::Detail.new(@settlement_session).execute
  end

  def create
    de_serialized_params = Presentation::DeSerializers::Settlement::Params.new(params).execute
    settlement_session = Usecases::Settlement::Create.new.execute(de_serialized_params)

    render json: settlement_session
  end

  def update
    de_serialized_params = Presentation::DeSerializers::Settlement::Params.new(params).execute
    Usecases::Settlement::Update.new(@settlement_session).execute(de_serialized_params)

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
    de_serialized_params = Presentation::DeSerializers::Settlement::PaymentParams.new(params).execute
    payment = Usecases::Settlement::CreatePayment.new(@settlement_session).execute(de_serialized_params)

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
end
