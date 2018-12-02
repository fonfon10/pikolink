class CreateUrlContacts < ActiveRecord::Migration[5.1]
  def change
    create_table :url_contacts do |t|
      t.integer :user_id
      t.integer :engineer_id

      t.timestamps
    end
  end
end
