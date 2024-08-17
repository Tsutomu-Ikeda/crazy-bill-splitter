require "test_helper"

class GroupTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
  test "should not save group without name" do
    group = Group.new
    assert_not group.save
  end

  test "should save group with name" do
    group = Group.new(name: "Group 1")
    assert group.save
  end
end
