class Company < ApplicationRecord
  has_many :engineers
  belongs_to :user


end
