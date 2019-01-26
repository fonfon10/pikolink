class RenameEngineerToOwner < ActiveRecord::Migration[5.1]
   def change
     rename_table :engineers, :owners
   end 
end
