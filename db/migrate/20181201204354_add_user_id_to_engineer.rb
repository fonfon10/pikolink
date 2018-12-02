class AddUserIdToEngineer < ActiveRecord::Migration[5.1]
  def change
    add_column :engineers, :user_id, :integer
  end
end
