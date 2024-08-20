class ApplicationController < ActionController::API
  around_action :auto_begin_transaction

  private

  def auto_begin_transaction
    ApplicationRecord.transaction do
      yield
    end
  end
end
