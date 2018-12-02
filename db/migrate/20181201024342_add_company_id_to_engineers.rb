class AddCompanyIdToEngineers < ActiveRecord::Migration[5.1]
  def change
    add_column :engineers, :company_id, :integer
  end
end
