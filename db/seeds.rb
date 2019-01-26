# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
#AdminUser.create!(email: 'admin@example.com', password: 'password', password_confirmation: 'password') if Rails.env.development?

@users = []

@users[0] = User.create!(email: 'slafontaine10@gmail.com', password: 'password', password_confirmation: 'password') 
@users[1] = User.create!(email: 'serge.lafontaine@analog.com', password: 'password', password_confirmation: 'password') 
@users[2] = User.create!(email: 'serge_lafontaine@hotmail.com', password: 'password', password_confirmation: 'password') 


@companies = ["ABCD", "EFGH", "IJKL", "MNOP", "QRST", "UVWX", "YZAB", "CDEF", "GHIJ", "KLMN", "OPQR", "STUV", "WXYZ"]




@companies.each do |company|

 @users.each do |user|

	c = Company.create!(name: company, user_id: user.id)


			e1 = Owner.create!(firstname: 'Jos', lastname:'Blow', company_id: c.id, user_id: user.id)
			e2 = Owner.create!(firstname: 'James', lastname:'Black', company_id: c.id, user_id: user.id)
			e3 = Owner.create!(firstname: 'Bob', lastname:'Yellow', company_id: c.id, user_id: user.id)
			e4 = Owner.create!(firstname: 'Serge', lastname:'White', company_id: c.id, user_id: user.id)
			e5 = Owner.create!(firstname: 'Wayne', lastname:'Brown', company_id: c.id, user_id: user.id)
			e6 = Owner.create!(firstname: 'John', lastname:'Orange', company_id: c.id, user_id: user.id)
			e7 = Owner.create!(firstname: 'Phil', lastname:'Purple', company_id: c.id, user_id: user.id)
	 	

			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e1, fresh: true, category: "LTM4601")
			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e2, fresh: true, category: "LTM4625")
			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e3, fresh: true, category: "LTM4644")
			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e4, fresh: true, category: "LTM4601")
			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e5, fresh: true, category: "LTM4601")
			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e6, fresh: true, category: "LTM4601")
			Shortener::ShortenedUrl.generate("http://www.cnn.com", owner: e7, fresh: true, category: "LTM4601")



 end

end


