class Owner < ApplicationRecord

#	has_many :owners
#	has_many :users, through: :owners

  belongs_to :company
  belongs_to :user

	has_shortened_urls



end
