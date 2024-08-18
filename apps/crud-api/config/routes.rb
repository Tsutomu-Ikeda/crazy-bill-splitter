Rails.application.routes.draw do
  scope :api do
    resources :settlements, only: %i[ create show destroy] do
      put :update, on: :member, to: "settlements#update"
      post :payments, on: :member, to: "settlements#create_payment"

      delete "payments/:payment_id", to: "settlements#destroy_payment", as: :payment
    end
  end
end
