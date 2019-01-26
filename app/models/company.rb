class Company < ApplicationRecord
  has_many :owners
  belongs_to :user


end
