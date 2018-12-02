# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
AdminUser.create!(email: 'admin@example.com', password: 'password', password_confirmation: 'password') if Rails.env.development?

User.create!(email: 'slafontaine10@gmail.com', password: 'password', password_confirmation: 'password') 
User.create!(email: 'serge.lafontaine@analog.com', password: 'password', password_confirmation: 'password') 
User.create!(email: 'serge_lafontaine@hotmail.com', password: 'password', password_confirmation: 'password') 

u1 = User.first
u2 = User.last

c1 =Company.create!(name: 'ABCDE', user_id: u1.id)
c2 = Company.create!(name: 'ACME', user_id: u1.id)
c3 = Company.create!(name: 'ADI', user_id: u2.id)
c4 = Company.create!(name: 'LTC', user_id: u2.id)
c5 = Company.create!(name: 'XYZ', user_id: u2.id)


e1 = Engineer.create!(firstname: 'Jos', lastname:'Blow', company_id: c1.id, user_id: u1.id)
e2 = Engineer.create!(firstname: 'Wayne', lastname:'Gretzky', company_id: c1.id, user_id: u1.id)
e3 = Engineer.create!(firstname: 'Mario', lastname:'Lemieux', company_id: c2.id, user_id: u1.id)
e4 = Engineer.create!(firstname: 'Jos', lastname:'Sakic', company_id: c3.id, user_id: u1.id)
e5 = Engineer.create!(firstname: 'Bill', lastname:'Black', company_id: c3.id, user_id: u1.id)
e6 = Engineer.create!(firstname: 'Jos', lastname:'White', company_id: c4.id, user_id: u1.id)
e7 = Engineer.create!(firstname: 'Simon', lastname:'Yellow', company_id: c5.id, user_id: u1.id)



Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e1, fresh: true)
Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e2, fresh: true)
Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e3, fresh: true)
Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e4, fresh: true)
Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e5, fresh: true)
Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e6, fresh: true)
Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e7, fresh: true)
