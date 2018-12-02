class ModifyEngineers < ActiveRecord::Migration[5.1]
  def change
  	add_column :engineers, :firstname, :string
  	add_column :engineers, :lastname, :string
  	remove_column :engineers, :name, :string

  end
end
