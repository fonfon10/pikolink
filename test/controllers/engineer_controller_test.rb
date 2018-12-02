require 'test_helper'

class EngineerControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get engineer_index_url
    assert_response :success
  end

  test "should get new" do
    get engineer_new_url
    assert_response :success
  end

  test "should get create" do
    get engineer_create_url
    assert_response :success
  end

  test "should get edit" do
    get engineer_edit_url
    assert_response :success
  end

end
