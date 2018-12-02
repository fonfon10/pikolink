class User < ApplicationRecord


#	has_many :owners
#	has_many :engineers, through: :owners
	has_many :companies
	has_many :engineers


  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable


#	has_shortened_urls



end
