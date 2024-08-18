require "test_helper"

class SettlementControllerTest < ActionDispatch::IntegrationTest
  setup do
    @settlement_session = settlement_sessions(:one)
  end

  test "should create settlement" do
    assert_difference("SettlementSession.count") do
      post settlements_url, params: {
        settlement: {
          title: @settlement_session.title,
          visibility_scope: @settlement_session.visibility_scope
        },
        participants: [
          {
            name: "John Doe",
            role: "participant"
          },
          {
            name: "Jane Doe",
            role: "organizer"
          }
        ]
      }, as: :json
    end

    assert_response :success
  end

  test "should show settlement" do
    get settlement_url(@settlement_session), as: :json
    assert_response :success
  end

  test "should update settlement" do
    put settlement_url(@settlement_session), params: {
      settlement: {
        title: @settlement_session.title,
        visibility_scope: @settlement_session.visibility_scope
      },
      participants: [
        {
          id: @settlement_session.settlement_session_participants.first.user_id,
          name: "John Doe",
          role: "participant"
        },
        {
          name: "Jack Doe",
          role: "organizer"
        }
      ]
    }, as: :json
    assert_response :success

    @settlement_session.reload
    assert_equal "Jack Doe", @settlement_session.settlement_session_participants.find_by(role: "organizer").user.name
  end

  test "should destroy settlement" do
    assert_difference("SettlementSession.count", -1) do
      delete settlement_url(@settlement_session), as: :json
    end

    assert_response :success
  end

  test "should create payment for settlement" do
    assert_difference("Payment.count") do
      post payments_settlement_url(@settlement_session), params: {
        amount: 100,
        description: "Payment for settlement session",
        paid_by_id: @settlement_session.settlement_session_participants.first.user_id,
        title: "Payment",
        description: "Payment for settlement session",
        participants: [
          {
            id: @settlement_session.settlement_session_participants.first.user_id,
            weight: 1
          },
          {
            id: @settlement_session.settlement_session_participants.last.user_id,
            weight: 2
          }
        ]
      }, as: :json
    end

    assert_response :success
  end

  test "should destroy payment for settlement" do
    payment = @settlement_session.payments.create!(
      amount: 100,
      paid_by_id: @settlement_session.settlement_session_participants.first.user_id,
      title: "Payment",
      description: "Payment for settlement session"
    )

    assert_difference("Payment.count", -1) do
      delete settlement_payment_path(@settlement_session, payment), as: :json
      assert response.body.include?("Payment deleted successfully"), response.body
    end

    assert_response :success
  end
end
