class ChangeUrlContactsToOwners < ActiveRecord::Migration[5.1]
  def change
  	rename_table :url_contacts, :owners

  end
end
